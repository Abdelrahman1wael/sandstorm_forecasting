# 🗺️ Spatial Regridding, Normalization & PyTorch Tensor Construction
### *Standardizing Satellite Rasters into Deep Learning Tensor Batches `[B, 3, 32, 32]`*
**Target Domain:** East Asia ($70^\circ\text{E} - 135^\circ\text{E}, \ 25^\circ\text{N} - 55^\circ\text{N}$)  
**Output Geometry:** Standard WGS84 Regular Grid (`EPSG:4326`)  
**Target Architecture:** Coupled AI-GAMFS Vision Encoder (`Ai Pipline/models/deep_learning/aigamfs_backbone.py`)

---

## 🎯 1. Operational Goal & Scientific Importance

Raw satellite swaths have variable dimensions (e.g., MODIS granules are $2030 \times 1354$ pixels, FY-4A disk scans are $2748 \times 2748$ pixels), arbitrary orbital projection geometries, and heterogeneous numeric ranges.

To feed satellite observations into deep convolutional neural networks (such as the `CoupledAIGAMFSEncoder`), the data must undergo **standardized spatial harmonization**:
1. **Bounding Box Cropping:** Restrict geographic coverage strictly to the East Asian dust source and transport domain ($70^\circ\text{E} - 135^\circ\text{E}, \ 25^\circ\text{N} - 55^\circ\text{N}$).
2. **Conservative & Bilinear Resampling:** Interpolate irregular swaths onto a uniform grid preserving aerosol mass gradients.
3. **Statistical Scaling:** Robust min-max normalization into $[0.0, 1.0]$ to prevent vanishing/exploding gradients in convolutional layers.
4. **PyTorch Tensor Serialization:** Pack multi-channel imagery into batch tensors of shape `[Batch, Channels=3, Height=32, Width=32]`.

---

## 📐 2. The 3-Channel Satellite Tensor Architecture

The Coupled AI-GAMFS Vision Backbone expects a 3-channel input tensor representing complementary optical and thermodynamic properties of the dust storm:

```
+---------------------------------------------------------------------------------------------------+
|                        THE 3-CHANNEL DEEP SATELLITE TENSOR ARCHITECTURE                           |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  CHANNEL 0: Normalized Aerosol Optical Depth (AOD_550)                                            |
|  • Physical Source: MODIS Deep Blue / FY-4A AGRI inverted 550nm AOD (gap-filled)                  |
|  • Physical Role: Quantifies column atmospheric dust mass and optical extinction.                 |
|  • Normalization: AOD_norm = clip(AOD / 5.0, 0.0, 1.0)                                           |
|                                                                                                   |
|  CHANNEL 1: Normalized Difference Dust Index (NDDI)                                               |
|  • Physical Source: Spectral ratio (ρ_2.13μm - ρ_0.47μm) / (ρ_2.13μm + ρ_0.47μm)                  |
|  • Physical Role: Separates mineral dust from clouds and vegetated ground.                        |
|  • Normalization: NDDI_norm = clip((NDDI - (-0.2)) / (0.8 - (-0.2)), 0.0, 1.0)                   |
|                                                                                                   |
|  CHANNEL 2: Thermal Infrared Split-Window (BTD_11-12)                                             |
|  • Physical Source: Brightness temperature difference T_b(11.0μm) - T_b(12.0μm)                  |
|  • Physical Role: Detects silicate Reststrahlen absorption (negative BTD) day and night.          |
|  • Normalization: BTD_norm = clip((BTD - (-4.0)) / (4.0 - (-4.0)), 0.0, 1.0)                     |
+---------------------------------------------------------------------------------------------------+
```

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `lon_min` | `float` | `70.0` | Fixed ($70.0^\circ\text{E}$) | Western boundary (Pamir Plateau / West Tarim Basin). |
| `lon_max` | `float` | `135.0` | Fixed ($135.0^\circ\text{E}$) | Eastern boundary (Northeastern China / Korean Peninsula). |
| `lat_min` | `float` | `25.0` | Fixed ($25.0^\circ\text{N}$) | Southern boundary (Sichuan Basin / Yangtze River valley). |
| `lat_max` | `float` | `55.0` | Fixed ($55.0^\circ\text{N}$) | Northern boundary (Mongolian Plateau / Southern Siberia). |
| `target_height` | `int` | `32` | `16 - 256` | Raster height for neural network input tensor ($H=32$). |
| `target_width` | `int` | `32` | `16 - 256` | Raster width for neural network input tensor ($W=32$). |
| `resampling_method`| `str` | `'bilinear'` | `'bilinear'`, `'area'` | Resampling algorithm (`'bilinear'` for smooth continuous fields). |
| `aod_ceiling` | `float` | `5.0` | `4.0 - 5.0` | Maximum AOD value mapped to $1.0$. |
| `btd_min_k` | `float` | `-4.0` | `-5.0 to -3.0` | Lower thermal clamping limit for $\text{BTD}_{11-12}$ (Kelvin). |
| `btd_max_k` | `float` | `4.0` | `2.0 - 5.0` | Upper thermal clamping limit for $\text{BTD}_{11-12}$ (Kelvin). |

---

## 📥 4. Geometric Resampling Pipeline

```
Raw Swath Array [H_raw, W_raw] with Lon/Lat Coordinates
                           │
                           ▼
              [Spatial Bounding Box Clip]
              Keep: 70°E <= Lon <= 135°E  and  25°N <= Lat <= 55°N
                           │
                           ▼
          [Regular Grid Bilinear Interpolation]
          Target Grid: 32 x 32 regular latitude-longitude cells
                           │
                           ▼
                [Channel Normalization]
          Channel 0: AOD / 5.0                ∈ [0.0, 1.0]
          Channel 1: (NDDI + 0.2) / 1.0       ∈ [0.0, 1.0]
          Channel 2: (BTD + 4.0) / 8.0        ∈ [0.0, 1.0]
                           │
                           ▼
                 [Stacking & Conversion]
             NumPy Array [3, 32, 32] (float32)
                           │
                           ▼
            PyTorch Tensor Batch [B, 3, 32, 32]
```

---

## 💡 5. Automated Python Tensor Builder

```python
import numpy as np
import torch
from scipy.ndimage import zoom

def assemble_satellite_tensor(
    aod_gap_filled: np.ndarray,
    nddi: np.ndarray,
    btd_11_12: np.ndarray,
    target_shape: tuple = (32, 32)
) -> torch.Tensor:
    """
    Transforms multi-spectral rasters into normalized PyTorch tensor [3, 32, 32].
    """
    # 1. Resample to standard target resolution (32x32)
    current_h, current_w = aod_gap_filled.shape
    zoom_factors = (target_shape[0] / current_h, target_shape[1] / current_w)
    
    aod_resampled = zoom(aod_gap_filled, zoom_factors, order=1)
    nddi_resampled = zoom(nddi, zoom_factors, order=1)
    btd_resampled = zoom(btd_11_12, zoom_factors, order=1)

    # 2. Channel 0: Normalized AOD [0.0, 1.0]
    ch0_aod = np.clip(aod_resampled / 5.0, 0.0, 1.0).astype(np.float32)

    # 3. Channel 1: Normalized NDDI [0.0, 1.0]
    # NDDI ranges from -0.2 (vegetation) to 0.8 (extreme dust)
    ch1_nddi = np.clip((nddi_resampled - (-0.2)) / (0.8 - (-0.2)), 0.0, 1.0).astype(np.float32)

    # 4. Channel 2: Normalized BTD [0.0, 1.0]
    # BTD ranges from -4.0K (dense dust) to +4.0K (clouds)
    ch2_btd = np.clip((btd_resampled - (-4.0)) / (4.0 - (-4.0)), 0.0, 1.0).astype(np.float32)

    # 5. Stack into 3D array: [3, 32, 32]
    stacked = np.stack([ch0_aod, ch1_nddi, ch2_btd], axis=0)

    # 6. Convert to PyTorch float32 tensor
    tensor = torch.from_numpy(stacked)
    return tensor
```
