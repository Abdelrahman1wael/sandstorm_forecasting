"""
==============================================================================
Spatio-Temporal Graph Neural Network (ST-GNN)
Modeling Non-Euclidean Dust Transport Advection along East Asian Corridors
==============================================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class GraphDiffusionLayer(nn.Module):
    """
    Bidirectional Graph Diffusion Convolution Layer.
    Applies Chebyshev polynomial approximation of graph Laplacian:
    P_0 = I (Local node self-evolution)
    P_1 = D_out^-1 * A (Forward advection downstream)
    P_2 = D_in^-1 * A^T (Reverse source-tracking upstream)
    """

    def __init__(self, in_features: int, out_features: int, k_hops: int = 2):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.k_hops = k_hops
        # Weights for each diffusion support: P_0 (self), P_1 (forward), P_2 (backward)
        self.weights = nn.Parameter(torch.Tensor(k_hops + 1, in_features, out_features))
        self.bias = nn.Parameter(torch.Tensor(out_features))
        self._init_weights()

    def _init_weights(self):
        nn.init.xavier_uniform_(self.weights)
        nn.init.zeros_(self.bias)

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        """
        x: [Batch, Nodes, InFeatures]
        adj: [Nodes, Nodes]
        """
        N = adj.size(0)
        I = torch.eye(N, device=adj.device, dtype=adj.dtype)

        # Forward transition matrix (row-normalized)
        d_out = torch.sum(adj, dim=1, keepdim=True).clamp(min=1e-5)
        P_fwd = adj / d_out

        # Backward transition matrix (column-normalized)
        d_in = torch.sum(adj, dim=0, keepdim=True).clamp(min=1e-5)
        P_bwd = (adj.T) / (d_in.T)

        supports = [I, P_fwd, P_bwd]

        out = 0.0
        for k, P in enumerate(supports[:self.k_hops + 1]):
            # Graph propagation: P * x -> [Batch, Nodes, InFeatures]
            propagated = torch.einsum("nm,bmf->bnf", P, x)
            # Linear transform: propagated * W_k -> [Batch, Nodes, OutFeatures]
            transformed = torch.matmul(propagated, self.weights[k])
            out = out + transformed

        return F.leaky_relu(out + self.bias, negative_slope=0.15)


class SpatioTemporalGNN(nn.Module):
    """
    ST-GNN Core:
      Combines Graph Diffusion with Temporal Gated Recurrent Units (GRU)
      to propagate dust plumes through time and space.
    """

    def __init__(self, node_in_dim: int = 12, hidden_dim: int = 64, out_dim: int = 64):
        super().__init__()
        self.hidden_dim = hidden_dim

        # Input feature projection
        self.node_proj = nn.Linear(node_in_dim, hidden_dim)

        # Spatiotemporal diffusion layers
        self.gcn1 = GraphDiffusionLayer(hidden_dim, hidden_dim)
        self.gcn2 = GraphDiffusionLayer(hidden_dim, hidden_dim)

        # Temporal GRU cell over sequence history
        self.gru = nn.GRU(hidden_dim, hidden_dim, batch_first=True)

        # Output projection
        self.out_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim)
        )

    def forward(self, seq_features: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        """
        seq_features: [Batch, SeqLen=24, Nodes=14, Feats=12]
        adj: [Nodes=14, Nodes=14]
        Returns: [Batch, Nodes, OutDim]
        """
        B, T, N, F = seq_features.shape

        # Flatten batch and time to dispatch spatial graph convolution: [B*T, N, F]
        x_flat = seq_features.reshape(B * T, N, F)
        h = self.node_proj(x_flat)
        h = self.gcn1(h, adj)
        h = self.gcn2(h, adj) # [B*T, N, Hidden]

        # Reshape back to temporal sequence: [B, T, N, Hidden] -> permute to [(B*N), T, Hidden]
        h = h.reshape(B, T, N, self.hidden_dim).permute(0, 2, 1, 3).reshape(B * N, T, self.hidden_dim)

        # Temporal evolution via GRU
        _, h_last = self.gru(h) # [1, B*N, Hidden]
        h_last = h_last.squeeze(0).reshape(B, N, self.hidden_dim) # [B, N, Hidden]

        # Final corridor state
        corridor_repr = self.out_head(h_last) # [B, N, OutDim]
        return corridor_repr
