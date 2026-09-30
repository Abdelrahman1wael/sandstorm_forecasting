# 🌌 Deep Learning Models Suite: Main Line B
### *End-to-End Multi-Modal Foundation Model, Coupled AI-GAMFS, ST-GNN Corridors & Physics-Informed Neural Networks (PINN)*
**Discipline:** Environmental Engineering (环境工程) • Atmospheric Deep Learning  
**Platform:** DustML Forecasting System (北京科技大学 • USTB)

---

## 🌟 Overview of Deep Learning Architecture

In the DustML platform, **Main Line B** represents an **end-to-end, multi-modal deep foundation framework** that maps planetary atmospheric fluid dynamics, high-resolution satellite optical depth imagery, and historical sensor time series directly to future spatial dust concentration fields and hazard alert tiers ($3\text{--}15$ days lead time).

It directly eliminates unphysical deep learning hallucinations by enforcing **atmospheric mass continuity PDEs** and **Owen's aerodynamic saltation threshold ($u_* > u_{*t}$)** inside PyTorch gradient backpropagation.

---

## 📂 Deep Learning Directory Catalog

| Model Document | Architecture Family | Operational Goal in DustML | Key Strengths & Role |
| :--- | :--- | :--- | :--- |
| **[`AIGAMFS_BACKBONE_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Deep_Learning/AIGAMFS_BACKBONE_MODEL.md)** | Multi-Modal Vision & Planetary CNN | Ingests 6-channel NWP dynamic fluid grids and 3-channel satellite AOD rasters via adaptive sigmoid gating. | Extracts multi-scale planetary atmospheric features; balances satellite imagery with fluid dynamics under cloud vs clear skies. |
| **[`ST_GNN_CORRIDOR_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Deep_Learning/ST_GNN_CORRIDOR_MODEL.md)** | Spatio-Temporal Graph Neural Network | Models non-Euclidean dust plume advection along 14 East Asian transport corridor nodes. | 3-support bidirectional Chebyshev diffusion ($P_0$ self, $P_1$ forward downstream, $P_2$ reverse upstream) + temporal GRU memory. |
| **[`PINN_CONSERVATION_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Deep_Learning/PINN_CONSERVATION_MODEL.md)** | Physics-Informed Neural Network (PINN) | Physics loss regularizer penalizing mass discontinuity and sub-threshold aerodynamic emissions. | Enforces Owen (1964) saltation flux ($u_* > u_{*t}$), 2D advective mass conservation PDEs, and strict non-negativity. |
| **[`DEEP_QUANTILE_HEAD_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Deep_Learning/DEEP_QUANTILE_HEAD_MODEL.md)** | Non-Crossing Monotonic Quantile Head | Predicts multi-lead uncertainty envelopes ($P_{10}, P_{50}, P_{90}$) across $L$ forward steps. | Uses cumulative softplus delta parameterization to mathematically guarantee $0 \le P_{10} \le P_{50} \le P_{90}$ without quantile crossing. |
| **[`DEEP_HAZARD_HEAD_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Deep_Learning/DEEP_HAZARD_HEAD_MODEL.md)** | Multi-Lead Focal Hazard Classifier | Outputs 5-tier CMA severity category logits across all lead horizons $[B, N, L, 5]$. | Trained with Class-Weighted Focal Loss ($\gamma = 2.0, \alpha = 10.0$) to overcome extreme class imbalance ($< 0.8\%$ storms). |
| **[`UNIFIED_DEEP_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Deep_Learning/UNIFIED_DEEP_MODEL.md)** | Master Hybrid Spatiotemporal Foundation | Integrates AI-GAMFS + ST-GNN + Multi-Scale Feature Fusion + Monotonic Quantiles + Hazard Heads. | Fully differentiable end-to-end model trained on multi-task loss with scheduled curriculum warm-up. |

---

## 🏗️ End-to-End Deep Architecture Workflow

```
+---------------------------------------------------------------------------------------------------+
|                            DUSTML MAIN LINE B: END-TO-END DEEP FLOW                               |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [NWP Grids: B x 6 x 16 x 16]         [Satellite AOD: B x 3 x 32 x 32]   [Sequence: B x 24 x 14 x 12]
|               │                                      │                                 │          |
|               ▼                                      ▼                                 │          |
|     (NWP Conv2D Backbone)                  (Sat Conv2D Backbone)                       │          |
|               │                                      │                                 │          |
|               └──────────────────┬───────────────────┘                                 │          |
|                                  ▼                                                     │          |
|                 [Coupled AI-GAMFS Gated Fusion Gate]                                   │          |
|                                  │                                                     │          |
|                                  v                                                     v          |
|                  Global Atmospheric Representation               [ST-GNN 14-Node Corridor Diffusion|
|                       h_global ∈ R^(B x Hidden)                       h_corridor ∈ R^(B x N x Hidden)|
|                                  │                                                     │          |
|                                  └──────────────────┬──────────────────────────────────┘          |
|                                                     ▼                                             |
|                                     [Multi-Scale Point-Wise Fusion]                               |
|                                        h_latent ∈ R^(B x N x Hidden)                              |
|                                                     │                                             |
|                         ┌───────────────────────────┴───────────────────────────┐                 |
|                         ▼                                                       ▼                 |
|           [Monotonic Quantile Head]                               [Cost-Sensitive Hazard Head]    |
|      0 <= P10 <= P50 <= P90 (Leads 1..L)                           5-Tier CMA Logits [B, N, L, 5] |
|                         │                                                       │                 |
|                         └───────────────────────────┬───────────────────────────┘                 |
|                                                     ▼                                             |
|                                     [PINN Physics Loss Regularizer]                               |
|                       Loss = Huber(Data) + 0.15*L_mass + 0.20*L_saltation + 0.10*L_neg            |
+---------------------------------------------------------------------------------------------------+
```
