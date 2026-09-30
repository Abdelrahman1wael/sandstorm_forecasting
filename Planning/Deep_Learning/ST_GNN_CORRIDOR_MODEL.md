# 🌐 Spatio-Temporal Graph Neural Network (ST-GNN): Technical Specification & Parameter Guide
### *Non-Euclidean Dust Plume Advection & Bidirectional Corridor Diffusion*
**Model Family:** Spatio-Temporal Graph Neural Network (GNN + Recurrent Memory)  
**Implementation:** `torch.nn.Module` (`SpatioTemporalGNN`, `GraphDiffusionLayer`)  
**File Location in Codebase:** [`Ai Pipline/models/deep_learning/st_gnn.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/deep_learning/st_gnn.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
Standard Convolutional Neural Networks (CNNs) treat geographic space as flat, Euclidean 2D grids ($H \times W$). However, atmospheric dust plumes **do not diffuse uniformly in all directions**. Their physical transport is tightly constrained by topography into narrow mountain passes and river valleys:
* The **Hexi Corridor (河西走廊)** bottleneck between the Qilian Mountains and Heli Mountains.
* The gap between the **Yin Mountains and Helan Mountains** funnelling sand from the Badain Jaran and Tengger deserts into the North China Plain.

The **ST-GNN Corridor Model** explicitly structures the East Asian dust transport network as a **directed topological graph ($\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathbf{A})$)** with 14 critical nodes:
1. **Bidirectional Graph Diffusion:** Models both downstream forward advection ($P_1$) and upstream source attribution ($P_2$).
2. **Temporal Recurrent Memory (GRU):** Propagates plume momentum across the preceding 24 hours of sensor history.

---

## 🗺️ 2. The 14-Node East Asian Dust Corridor Graph

```
[Node 0: Taklamakan] ─────► [Node 2: Dunhuang] ─────► [Node 3: Zhangye (Hexi Corridor)]
                                                                  │
[Node 1: Badain Jaran] ───► [Node 4: Wuwei] ◄────────────────────┘
                                   │
                                   ▼
[Node 5: Tengger] ────────► [Node 6: Yinchuan (Ningxia Plain)]
                                   │
                                   ├─────────────────────────────┐
                                   ▼                             ▼
                        [Node 7: Hohhot (Inner Mongolia)] [Node 9: Yan'an (Loess Plateau)]
                                   │                             │
                                   ▼                             ▼
                        [Node 8: Zhangjiakou Gate]        [Node 12: Xi'an / Guanzhong]
                                   │                             │
                                   ▼                             ▼
                        [Node 10: Beijing Capital]        [Node 13: Qinling Barrier / Chengdu]
                                   │
                                   ▼
                        [Node 11: Shijiazhuang / Jinan (North China Plain)]
```

---

## 📐 3. Mathematical Formulation: Bidirectional Graph Diffusion

Traditional graph convolutions use symmetric Laplacians ($\mathbf{D}^{-1/2} \mathbf{A} \mathbf{D}^{-1/2}$) appropriate for undirected graphs. Because atmospheric advection is **directional** (driven by prevailing northwest winds), ST-GNN utilizes a **3-support Chebyshev decomposition**:

### 3.1 Transition Matrices
1. **$P_0 = \mathbf{I}$ (Local Self-Evolution):** Station-specific local dust generation and gravitational deposition.
2. **$P_1 = \mathbf{D}_{\text{out}}^{-1} \mathbf{A}$ (Forward Downstream Advection):** Wind carrying dust from desert emission sources to downstream cities:
   $$(\mathbf{D}_{\text{out}})_{ii} = \sum_{j} A_{ij}$$
3. **$P_2 = \mathbf{D}_{\text{in}}^{-1} \mathbf{A}^T$ (Reverse Upstream Source Tracking):** Tracing downwind pollution back to its source:
   $$(\mathbf{D}_{\text{in}})_{jj} = \sum_{i} A_{ij}$$

### 3.2 Bidirectional Diffusion Layer
For node feature matrix $\mathbf{X} \in \mathbb{R}^{B \times N \times F}$:

$$\mathbf{H}^{(l+1)} = \text{LeakyReLU}\left(\sum_{k=0}^2 P_k \mathbf{H}^{(l)} \mathbf{W}_k + \mathbf{b}\right)$$

Where $\mathbf{W}_0, \mathbf{W}_1, \mathbf{W}_2 \in \mathbb{R}^{F_{\text{in}} \times F_{\text{out}}}$ are independent learnable transformation weights for self, forward, and backward advection.

### 3.3 Temporal Sequence Encoding via GRU
For each station $i$, the time sequence of spatial graph embeddings $[\mathbf{h}_{1, i}, \mathbf{h}_{2, i}, \dots, \mathbf{h}_{T, i}]$ across $T=24\text{ hours}$ is processed by a Gated Recurrent Unit:

$$\mathbf{z}_t = \sigma\left(\mathbf{W}_z \mathbf{x}_t + \mathbf{U}_z \mathbf{h}_{t-1}\right)$$
$$\mathbf{r}_t = \sigma\left(\mathbf{W}_r \mathbf{x}_t + \mathbf{U}_r \mathbf{h}_{t-1}\right)$$
$$\tilde{\mathbf{h}}_t = \tanh\left(\mathbf{W} \mathbf{x}_t + \mathbf{U} (\mathbf{r}_t \odot \mathbf{h}_{t-1})\right)$$
$$\mathbf{h}_t = (1 - \mathbf{z}_t) \odot \mathbf{h}_{t-1} + \mathbf{z}_t \odot \tilde{\mathbf{h}}_t$$

---

## ⚙️ 4. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `node_in_dim` | `int` | `12` | `8 - 24` | Number of physical dynamic attributes recorded at each corridor node. |
| `hidden_dim` | `int` | `64` | `32 - 128` | Latent embedding width for spatial graph diffusion and GRU memory. |
| `out_dim` | `int` | `64` | `32 - 128` | Final dimensionality of the corridor advection representation. |
| `k_hops` | `int` | `2` | `1 - 3` | Diffusion neighborhood radius. $K=2$ allows 2-hop corridor information transfer. |
| `gru_layers` | `int` | `1` | `1 - 2` | Number of stacked GRU recurrent layers across the 24-hour sequence. |
| `negative_slope`| `float` | `0.15` | `0.05 - 0.20` | LeakyReLU slope for negative gradient flow. |
| `dropout` | `float` | `0.15` | `0.05 - 0.30` | Dropout probability preventing edge co-adaptation. |

---

## 📥 5. Input Tensors & Adjacency Matrix

1. **`seq_features` (Tensor: `[B, 24, 14, 12]`):**
   * $B$: Batch size.
   * $T=24$: Hourly time steps over the past 24 hours.
   * $N=14$: Corridor monitoring nodes.
   * $F=12$: Historical particulate $\text{PM}_{10}$, $U_{10}, V_{10}$, surface friction velocity $u_*$, threshold $u_{*t}$, relative humidity, soil moisture, boundary layer height.
2. **`adj_matrix` (Tensor: `[14, 14]`):**
   * Normalized directed spatial adjacency matrix weighted by distance and prevailing wind corridor azimuth.

---

## 📤 6. Output Representation

* **Corridor Advection State:** $\mathbf{h}_{\text{corridor}} \in \mathbb{R}^{B \times 14 \times d_{\text{out}}}$.
* Encapsulates the downstream dust plume momentum advancing along the geographic corridor.

---

## 💡 7. PyTorch Implementation Code

Exemplar implementation from `Ai Pipline/models/deep_learning/st_gnn.py`:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class GraphDiffusionLayer(nn.Module):
    def __init__(self, in_features, out_features, k_hops=2):
        super().__init__()
        self.k_hops = k_hops
        # Weights for P0 (self), P1 (forward downstream), P2 (backward upstream)
        self.weights = nn.Parameter(torch.Tensor(k_hops + 1, in_features, out_features))
        self.bias = nn.Parameter(torch.Tensor(out_features))
        nn.init.xavier_uniform_(self.weights)
        nn.init.zeros_(self.bias)

    def forward(self, x, adj):
        N = adj.size(0)
        I = torch.eye(N, device=adj.device, dtype=adj.dtype)

        # Forward transition (out-degree row normalized)
        d_out = torch.sum(adj, dim=1, keepdim=True).clamp(min=1e-5)
        P_fwd = adj / d_out

        # Backward transition (in-degree column normalized)
        d_in = torch.sum(adj, dim=0, keepdim=True).clamp(min=1e-5)
        P_bwd = adj.T / d_in.T

        supports = [I, P_fwd, P_bwd]
        out = 0.0
        for k, P in enumerate(supports[:self.k_hops + 1]):
            propagated = torch.einsum("nm,bmf->bnf", P, x)
            transformed = torch.matmul(propagated, self.weights[k])
            out = out + transformed

        return F.leaky_relu(out + self.bias, negative_slope=0.15)


class SpatioTemporalGNN(nn.Module):
    def __init__(self, node_in_dim=12, hidden_dim=64, out_dim=64):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.node_proj = nn.Linear(node_in_dim, hidden_dim)
        self.gcn1 = GraphDiffusionLayer(hidden_dim, hidden_dim)
        self.gcn2 = GraphDiffusionLayer(hidden_dim, hidden_dim)
        self.gru = nn.GRU(hidden_dim, hidden_dim, batch_first=True)
        self.out_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim)
        )

    def forward(self, seq_features, adj):
        B, T, N, F = seq_features.shape
        # Flatten batch and time to process graph diffusion
        flat_x = seq_features.view(B * T, N, F)
        h = self.node_proj(flat_x)
        h = self.gcn1(h, adj)
        h = self.gcn2(h, adj)
        
        # Reshape to sequence for GRU: [B*N, T, Hidden]
        h_seq = h.view(B, T, N, self.hidden_dim).permute(0, 2, 1, 3).contiguous()
        h_seq = h_seq.view(B * N, T, self.hidden_dim)
        
        _, h_final = self.gru(h_seq)
        h_final = h_final.squeeze(0).view(B, N, self.hidden_dim)
        return self.out_head(h_final)
```
