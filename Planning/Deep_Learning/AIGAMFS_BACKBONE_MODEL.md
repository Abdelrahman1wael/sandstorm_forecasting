# 🛰️ Coupled AI-GAMFS Backbone: Technical Specification & Parameter Guide
### *Multi-Modal Planetary Aerosol-Meteorology Foundation Vision Encoder*
**Model Family:** Multi-Modal Convolutional Vision Encoder with Adaptive Gated Fusion  
**Implementation:** `torch.nn.Module` (`CoupledAIGAMFSEncoder`)  
**File Location in Codebase:** [`Ai Pipline/models/deep_learning/aigamfs_backbone.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/deep_learning/aigamfs_backbone.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
Traditional sandstorm forecasting models treat gridded numerical wind fields and high-resolution satellite imagery in isolation. 

The **Coupled AI-GAMFS Foundation Backbone** extracts a unified planetary atmospheric representation $\mathbf{h}_{\text{global}} \in \mathbb{R}^{d_{\text{embed}}}$ by simultaneously encoding:
1. **Atmospheric Fluid Dynamics:** 6-channel NWP grids ($U_{10}, V_{10}, Z_{850}, T_{2\text{m}}, Q_{850}, \text{PBLH}$) capturing synoptic pressure gradients, thermal lapse rates, and boundary layer mixing.
2. **Aerosol Earth Observation Rasters:** 3-channel satellite imagery (Aerosol Optical Depth, Dust Aerosol Index, Brightness Temperature Difference) capturing active airborne dust plumes.
3. **Cross-Modal Adaptive Sigmoid Gating:** Dynamically modulates reliance between NWP physics and satellite imagery depending on cloud cover conditions.

---

## 📐 2. Mathematical Formulation & Architecture

```
         NWP Fluid Grid [B, 6, 16, 16]                 Satellite Raster [B, 3, 32, 32]
                       │                                              │
                       ▼                                              ▼
              Conv2D (6 -> 32, k=3, s=1)                     Conv2D (3 -> 32, k=3, s=2)
              BatchNorm2d + GELU                             BatchNorm2d + GELU
                       │                                              │
                       ▼                                              ▼
              Conv2D (32 -> 64, k=3, s=2)                    Conv2D (32 -> 64, k=3, s=2)
              BatchNorm2d + GELU                             BatchNorm2d + GELU
                       │                                              │
                       ▼                                              ▼
              AdaptiveAvgPool2d(1, 1)                        AdaptiveAvgPool2d(1, 1)
              Flatten + Linear(64 -> Embed)                  Flatten + Linear(64 -> Embed)
                       │                                              │
                       ▼                                              ▼
                  h_nwp [B, 128]                                 h_sat [B, 128]
                       │                                              │
                       └──────────────────────┬───────────────────────┘
                                              ▼
                                 Concatenation [B, 256]
                                              │
                        ┌─────────────────────┴─────────────────────┐
                        ▼                                           ▼
             Sigmoid Gate: g = σ(W_g * Concat)            Residual: W_proj * Concat
                        │                                           │
                        └─────────────────────┬─────────────────────┘
                                              ▼
                          Gated Blend: g * h_nwp + (1 - g) * h_sat
                                              │
                                              ▼
                          LayerNorm(Residual_Proj + Gated_Blend)
                                              │
                                              ▼
                                 h_global ∈ R^(B x 128)
```

### 2.1 The Cross-Modal Gating Mechanism
Optical satellite sensors cannot penetrate dense cloud decks (e.g., cirrus shield along a cold front). When overcast, AOD pixels are flagged as missing or corrupted. 

The gating mechanism computes continuous scalar weights $g \in (0, 1)$ per batch:

$$\mathbf{g} = \sigma\left(\mathbf{W}_g \left[\mathbf{h}_{\text{nwp}} \, \| \, \mathbf{h}_{\text{sat}}\right] + \mathbf{b}_g\right)$$
$$\mathbf{h}_{\text{fused}} = \text{LayerNorm}\left(\mathbf{W}_{\text{proj}} \left[\mathbf{h}_{\text{nwp}} \, \| \, \mathbf{h}_{\text{sat}}\right] + \mathbf{g} \odot \mathbf{h}_{\text{nwp}} + (1 - \mathbf{g}) \odot \mathbf{h}_{\text{sat}}\right)$$

* **Overcast Storm Conditions ($\mathbf{g} \to 1.0$):** Backbone shifts weight to NWP dynamical equations, unaffected by clouds.
* **Clear Skies with Visible Dust Plume ($\mathbf{g} \to 0.0$):** Backbone shifts weight to true satellite aerosol optical depth measurements.

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `nwp_channels` | `int` | `6` | `4 - 12` | Number of physical dynamic atmospheric channels in the NWP grid. |
| `sat_channels` | `int` | `3` | `1 - 6` | Number of spectral bands / aerosol indices from satellite sensors. |
| `embed_dim` | `int` | `128` | `64 - 256` | Dimensionality of the output global planetary embedding $\mathbf{h}_{\text{global}}$. |
| `kernel_size` | `int` | `3` | `3 - 5` | Size of the 2D spatial convolution receptive field. |
| `stride` | `int` | `2` | `1 - 2` | Stride for downsampling spatial feature maps. |
| `padding` | `int` | `1` | `1 - 2` | Symmetric zero-padding ensuring edge boundary preservation. |
| `act_fn` | `str` | `'GELU'` | `'GELU'`, `'SiLU'` | Activation function providing smooth non-linear gradient propagation. |
| `norm_type` | `str` | `'BatchNorm2d'` | `'BatchNorm'`, `'LayerNorm'` | Normalizes intermediate channel activations across batch instances. |

---

## 📥 4. Input Tensors & Channel Layout

1. **`nwp_grid` (Tensor: `[B, 6, 16, 16]`):**
   * Channel 0: $U_{10}$ (Zonal 10m wind velocity, $\text{m/s}$)
   * Channel 1: $V_{10}$ (Meridional 10m wind velocity, $\text{m/s}$)
   * Channel 2: $Z_{850}$ (850 hPa Geopotential Height, $\text{gpm}$)
   * Channel 3: $T_{2\text{m}}$ (2m Surface Temperature, $\text{K}$)
   * Channel 4: $Q_{850}$ (Specific Humidity, $\text{kg/kg}$)
   * Channel 5: $\text{PBLH}$ (Planetary Boundary Layer Height, $\text{m}$)
2. **`sat_grid` (Tensor: `[B, 3, 32, 32]`):**
   * Channel 0: FY-4 / MODIS Aerosol Optical Depth ($550\text{ nm}$ AOD)
   * Channel 1: Dust Aerosol Index (DAI absorbing ratio)
   * Channel 2: Brightness Temperature Difference ($\text{BTD}_{11\mu\text{m} - 12\mu\text{m}}$)

---

## 📤 5. Output Representation

* **Global Atmospheric Embedding:** $\mathbf{h}_{\text{global}} \in \mathbb{R}^{B \times d_{\text{embed}}}$.
* Broadcast and concatenated to all 14 corridor station nodes in Phase 5 to provide macroscopic planetary context.

---

## 💡 6. PyTorch Implementation Code

Exemplar implementation from `Ai Pipline/models/deep_learning/aigamfs_backbone.py`:

```python
import torch
import torch.nn as nn

class CoupledAIGAMFSEncoder(nn.Module):
    def __init__(self, nwp_channels=6, sat_channels=3, embed_dim=128):
        super().__init__()
        self.embed_dim = embed_dim

        # 1. Atmospheric fluid dynamics grid encoder [B, 6, 16, 16] -> [B, Embed]
        self.nwp_conv = nn.Sequential(
            nn.Conv2d(nwp_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.GELU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.GELU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(64, embed_dim)
        )

        # 2. Satellite AOD raster encoder [B, 3, 32, 32] -> [B, Embed]
        self.sat_conv = nn.Sequential(
            nn.Conv2d(sat_channels, 32, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.GELU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.GELU(),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(64, embed_dim)
        )

        # 3. Cross-modal adaptive gate
        self.fusion_gate = nn.Sequential(
            nn.Linear(embed_dim * 2, embed_dim),
            nn.Sigmoid()
        )
        self.fusion_proj = nn.Linear(embed_dim * 2, embed_dim)
        self.layer_norm = nn.LayerNorm(embed_dim)

    def forward(self, nwp_grid, sat_grid):
        h_nwp = self.nwp_conv(nwp_grid)
        h_sat = self.sat_conv(sat_grid)

        concat = torch.cat([h_nwp, h_sat], dim=-1)
        gate = self.fusion_gate(concat)
        
        # Adaptive gated fusion
        fused = gate * h_nwp + (1.0 - gate) * h_sat
        output = self.layer_norm(self.fusion_proj(concat) + fused)
        return output
```
