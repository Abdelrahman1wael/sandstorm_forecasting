"""
==============================================================================
DustML Unified Deep Model Architecture
Coupled AI-GAMFS Backbone + ST-GNN Advection Corridors + Quantile Heads + Hazard Heads
==============================================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any

from .aigamfs_backbone import CoupledAIGAMFSEncoder
from .st_gnn import SpatioTemporalGNN


class DustMLUnifiedDeepModel(nn.Module):
    """
    World-class End-to-End Deep Spatiotemporal Architecture.
    Integrates:
      1. Coupled AI-GAMFS multi-modal encoder (NWP fluid dynamics + Satellite AOD)
      2. ST-GNN bidirectional diffusion network (14 East Asian dust corridor nodes)
      3. Point-wise multi-scale feature fusion
      4. Multi-lead quantile regression heads (P10, P50, P90)
      5. Cost-sensitive hazard classification head (5 classes)
    """

    def __init__(
        self,
        n_stations: int = 14,
        n_lead_times: int = 6,
        n_classes: int = 5,
        nwp_channels: int = 6,
        sat_channels: int = 3,
        node_features_dim: int = 12,
        hidden_dim: int = 64
    ):
        super().__init__()
        self.n_stations = n_stations
        self.n_lead_times = n_lead_times
        self.n_classes = n_classes
        self.hidden_dim = hidden_dim

        # 1. Multi-modal foundation encoder
        self.backbone = CoupledAIGAMFSEncoder(
            nwp_channels=nwp_channels,
            sat_channels=sat_channels,
            embed_dim=hidden_dim
        )

        # 2. Spatio-Temporal Corridor GNN
        self.st_gnn = SpatioTemporalGNN(
            node_in_dim=node_features_dim,
            hidden_dim=hidden_dim,
            out_dim=hidden_dim
        )

        # 3. Fusion of [Global Context + Node State + ST-GNN Corridor State]
        # Total dimension: hidden_dim + node_features_dim + hidden_dim
        fused_dim = hidden_dim * 2 + node_features_dim
        self.fusion_mlp = nn.Sequential(
            nn.Linear(fused_dim, hidden_dim * 2),
            nn.LayerNorm(hidden_dim * 2),
            nn.GELU(),
            nn.Dropout(0.15),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim)
        )

        # 4. Multi-lead Quantile Heads (P10, P50, P90)
        # Predicts [B, N, Leads] for each quantile
        self.p50_head = nn.Linear(hidden_dim, n_lead_times)
        self.p10_offset_head = nn.Linear(hidden_dim, n_lead_times)
        self.p90_offset_head = nn.Linear(hidden_dim, n_lead_times)

        # 5. Multi-lead Hazard Classification Head [B, N, Leads, NClasses]
        self.hazard_head = nn.Linear(hidden_dim, n_lead_times * n_classes)

    def forward(
        self,
        nwp_grid: torch.Tensor,
        sat_grid: torch.Tensor,
        seq_features: torch.Tensor,
        current_node_features: torch.Tensor,
        adj_matrix: torch.Tensor
    ) -> Dict[str, torch.Tensor]:
        """
        Args:
          nwp_grid: [B, 6, 16, 16]
          sat_grid: [B, 3, 32, 32]
          seq_features: [B, 24, 14, 12]
          current_node_features: [B, 14, 12]
          adj_matrix: [14, 14]
        """
        B = nwp_grid.size(0)
        N = self.n_stations

        # 1. Extract global multi-modal background: [B, Hidden]
        global_repr = self.backbone(nwp_grid, sat_grid)

        # 2. Extract corridor advection state: [B, N, Hidden]
        corridor_repr = self.st_gnn(seq_features, adj_matrix)

        # 3. Expand global representation across all stations: [B, N, Hidden]
        global_expanded = global_repr.unsqueeze(1).expand(-1, N, -1)

        # 4. Concatenate and fuse
        concat_feats = torch.cat([global_expanded, current_node_features, corridor_repr], dim=-1)
        latent_nodes = self.fusion_mlp(concat_feats) # [B, N, Hidden]

        # 5. Quantile regression with monotonic guarantee: P10 <= P50 <= P90
        raw_p50 = F.softplus(self.p50_head(latent_nodes)) # [B, N, Leads]
        p10_delta = F.softplus(self.p10_offset_head(latent_nodes))
        p90_delta = F.softplus(self.p90_offset_head(latent_nodes))

        p50 = raw_p50
        p10 = torch.clamp(p50 - p10_delta, min=0.0)
        p90 = p50 + p90_delta

        # 6. Hazard classification logits: [B, N, Leads, Classes]
        hazard_raw = self.hazard_head(latent_nodes) # [B, N, Leads * Classes]
        hazard_logits = hazard_raw.view(B, N, self.n_lead_times, self.n_classes)

        return {
            "p50": p50,
            "p10": p10,
            "p90": p90,
            "interval_width": p90 - p10,
            "hazard_logits": hazard_logits,
            "latent_nodes": latent_nodes,
            "global_context": global_repr
        }
