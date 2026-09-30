# 🏛️ DustML Unified Deep Model: Technical Specification & Parameter Guide
### *End-to-End Multi-Modal Foundation Model Integrating AI-GAMFS, ST-GNN & PINN*
**Model Family:** Unified Deep Spatiotemporal Neural Architecture  
**Implementation:** `torch.nn.Module` (`DustMLUnifiedDeepModel`)  
**File Location in Codebase:** [`Ai Pipline/models/deep_learning/unified_model.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/deep_learning/unified_model.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Master Foundation Model
The `DustMLUnifiedDeepModel` is the **flagship deep neural network** of the platform. It integrates all deep learning components into a single differentiable architecture trained end-to-end:

1. **Planetary Multi-Modal Vision:** Simultaneously processes NWP fluid dynamic grids and satellite AOD rasters via the **Coupled AI-GAMFS Backbone**.
2. **Corridor Graph Advection:** Tracks directed non-Euclidean plume transport across 14 nodes via the **Spatio-Temporal Graph Neural Network (ST-GNN)**.
3. **Multi-Scale Feature Fusion:** Unites global planetary context, local station measurements, and corridor advection states into enriched latent node embeddings.
4. **Multi-Lead Monotonic Quantiles:** Produces non-crossing uncertainty intervals ($P_{10} \le P_{50} \le P_{90}$) across all forecast lead times.
5. **Cost-Sensitive Hazard Warnings:** Predicts official 5-tier CMA severity levels.
6. **Physics Regularization:** Constrained by the **PINN Loss Module** enforcing Owen's saltation threshold and mass continuity PDEs.

---

## 🏗️ 2. Architectural Blueprint & Data Flow

```
Inputs:
├── nwp_grid:         [B, 6, 16, 16]   (Atmospheric dynamics: U, V, Z, T, Q, PBLH)
├── sat_grid:         [B, 3, 32, 32]   (Satellite imagery: AOD, DAI, BTD)
├── seq_features:     [B, 24, 14, 12]  (24h sequence history across 14 nodes)
├── current_node:     [B, 14, 12]      (Current station boundary state)
└── adj_matrix:       [14, 14]         (Corridor transport adjacency)
                            │
     ┌──────────────────────┴──────────────────────┐
     ▼                                             ▼
[Coupled AI-GAMFS Backbone]               [ST-GNN Corridor Engine]
     │                                             │
     ▼                                             ▼
Global Context: h_global [B, 64]          Corridor State: h_corridor [B, 14, 64]
     │                                             │
     ▼ (expand across N=14 nodes)                  │
[B, 14, 64]                                        │
     │                                             │
     └──────────────────────┬──────────────────────┘
                            ▼
          Concatenation: [h_global, current_node, h_corridor]
                     Dim: 64 + 12 + 64 = 140
                            │
                            ▼
                    [Point-Wise Fusion MLP]
               Linear(140->128) -> LayerNorm -> GELU -> Dropout(0.15)
               Linear(128->64)  -> LayerNorm
                            │
                            ▼
               Latent Nodes: h_latent [B, 14, 64]
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
   [Monotonic Quantile Head]     [Hazard Classification Head]
   p50 = softplus(W_50 * h)      hazard_logits = W_h * h
   p10 = clamp(p50 - Δ_10)       [B, 14, Leads, 5]
   p90 = p50 + Δ_90
   [B, 14, Leads] each
```

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `n_stations` | `int` | `14` | `10 - 50` | Number of topological corridor monitoring nodes. |
| `n_lead_times` | `int` | `6` | `1 - 15` | Number of simultaneous forecast horizons (e.g. 24h, 72h, 120h, 168h, 240h, 360h). |
| `n_classes` | `int` | `5` | Fixed (5) | Number of CMA national warning levels. |
| `nwp_channels` | `int` | `6` | `4 - 12` | Input channels in the numerical weather grid. |
| `sat_channels` | `int` | `3` | `1 - 6` | Input spectral channels in satellite raster swaths. |
| `node_features_dim`| `int` | `12` | `8 - 24` | Dimension of physical measurements recorded at each station. |
| `hidden_dim` | `int` | `64` | `32 - 128` | Internal latent dimensionality across backbone, ST-GNN, and fusion layers. |
| `fusion_dropout` | `float` | `0.15` | `0.10 - 0.25` | Dropout probability in the multi-scale fusion MLP. |

---

## 📥 4. Input & Output Tensor Schema

### Input Tensors:
* `nwp_grid`: `torch.Tensor` of shape `[Batch, 6, 16, 16]` (float32)
* `sat_grid`: `torch.Tensor` of shape `[Batch, 3, 32, 32]` (float32)
* `seq_features`: `torch.Tensor` of shape `[Batch, 24, 14, 12]` (float32)
* `current_node_features`: `torch.Tensor` of shape `[Batch, 14, 12]` (float32)
* `adj_matrix`: `torch.Tensor` of shape `[14, 14]` (float32)

### Output Dictionary:
* `"p50"`: `torch.Tensor` `[Batch, 14, Leads]` — Median expected $\text{PM}_{10}$ concentration.
* `"p10"`: `torch.Tensor` `[Batch, 14, Leads]` — Lower uncertainty bound (non-negative).
* `"p90"`: `torch.Tensor` `[Batch, 14, Leads]` — Upper uncertainty bound (severe risk).
* `"interval_width"`: `torch.Tensor` `[Batch, 14, Leads]` — Uncertainty spread ($P_{90} - P_{10}$).
* `"hazard_logits"`: `torch.Tensor` `[Batch, 14, Leads, 5]` — 5-tier classification logits.
* `"latent_nodes"`: `torch.Tensor` `[Batch, 14, 64]` — Enriched spatiotemporal station embeddings.
* `"global_context"`: `torch.Tensor` `[Batch, 64]` — Planetary atmospheric context vector.

---

## 💡 5. Master PyTorch Implementation Code

Exemplar implementation from `Ai Pipline/models/deep_learning/unified_model.py`:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

from .aigamfs_backbone import CoupledAIGAMFSEncoder
from .st_gnn import SpatioTemporalGNN

class DustMLUnifiedDeepModel(nn.Module):
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
    ):
        B = nwp_grid.size(0)
        N = self.n_stations

        # Extract global representation and corridor advection
        global_repr = self.backbone(nwp_grid, sat_grid) # [B, Hidden]
        corridor_repr = self.st_gnn(seq_features, adj_matrix) # [B, N, Hidden]

        # Expand global representation across all stations
        global_expanded = global_repr.unsqueeze(1).expand(-1, N, -1)

        # Fuse representations
        concat_feats = torch.cat([global_expanded, current_node_features, corridor_repr], dim=-1)
        latent_nodes = self.fusion_mlp(concat_feats) # [B, N, Hidden]

        # Monotonic non-crossing quantiles: P10 <= P50 <= P90
        raw_p50 = F.softplus(self.p50_head(latent_nodes))
        p10_delta = F.softplus(self.p10_offset_head(latent_nodes))
        p90_delta = F.softplus(self.p90_offset_head(latent_nodes))

        p50 = raw_p50
        p10 = torch.clamp(p50 - p10_delta, min=0.0)
        p90 = p50 + p90_delta

        # Hazard classification logits
        hazard_raw = self.hazard_head(latent_nodes)
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
```
