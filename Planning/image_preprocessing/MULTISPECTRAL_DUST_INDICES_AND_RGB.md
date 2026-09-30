# 🎨 Multispectral Dust Indices & WMO 24-Bit Dust RGB Composites
### *Formulations for NDDI, IDDI, DAI and Standardized False-Color Satellite Imagery*
**Spectral Range:** Ultraviolet ($0.35\mu\text{m}$), Visible ($0.47\mu\text{m}$), SWIR ($2.13\mu\text{m}$), Thermal IR ($8.7\mu\text{m} - 12.0\mu\text{m}$)  
**Standard Authority:** World Meteorological Organization (WMO) / EUMETSAT  
**Output Target:** 3-Channel Dense Visual Feature Rasters for Convolutional Foundation Models

---

## 🎯 1. Operational Goal & Scientific Importance

Single-band satellite imagery is inadequate for training deep convolutional vision encoders because surface topography and atmospheric aerosols blend together. 

By combining multiple optical and thermal infrared bands into **normalized mathematical ratios** and **calibrated 24-bit RGB composites**:
1. **Spectral Disambiguation:** Dust is differentiated from snow cover, water clouds, high cirrus, and bare ground through differential absorption.
2. **Standardized Deep Learning Inputs:** Forms the calibrated 3-channel visual raster `[B, 3, 32, 32]` fed into the **Coupled AI-GAMFS Vision Encoder** in Main Line B.

---

## 📐 2. Mathematical Formulations of Key Dust Indices

```
                         Spectral Reflectance & Emission Signatures:
                         -------------------------------------------
      Band:                  Mineral Dust:          Water Cloud:          Vegetation:
      Blue (0.47 μm)         Low (Strong Absorp.)   High (Scattering)     Low (Chlorophyll Absorp.)
      SWIR (2.13 μm)         High (High Albedo)     Moderate              Low (Leaf Water Absorp.)
      IR (10.8 μm - 12.0 μm) Negative BTD           Positive BTD          Near Zero
```

---

### 2.1 Normalized Difference Dust Index (NDDI)
Formulated by Qu et al. (2006) for MODIS, taking advantage of the large spectral contrast between blue light ($0.47\mu\text{m}$, Band 3) and shortwave infrared ($2.13\mu\text{m}$, Band 7):

$$\text{NDDI} = \frac{\rho_{2.13\mu\text{m}} - \rho_{0.47\mu\text{m}}}{\rho_{2.13\mu\text{m}} + \rho_{0.47\mu\text{m}}}$$

* **$\text{NDDI} > +0.28$:** Airborne Mineral Dust Plume.
* **$\text{NDDI} \approx 0.0$:** Meteorological Clouds (clouds exhibit high reflectance in both bands).
* **$\text{NDDI} < -0.05$:** Dense Vegetation or Water Bodies.

---

### 2.2 Infrared Dust Difference Index (IDDI)
Used extensively on geostationary satellites (FY-4A/B, Himawari) to track diurnal dust transport without sunlight. Dust plumes absorb upward thermal emission from the heated desert floor, making the satellite observe a cooler brightness temperature:

$$\text{IDDI}(x, y, t) = T_{b, \text{clear\_max}}(11.0\mu\text{m}) - T_{b, \text{observed}}(11.0\mu\text{m})$$

Where $T_{b, \text{clear\_max}}$ is the maximum clear-sky brightness temperature composite observed over the preceding 15 days at the same solar hour.
* **$\text{IDDI} > 15.0\text{ K}$:** Dense sandstorm lifting and optical obscuration.

---

### 2.3 Ultraviolet Absorbing Aerosol Index (AAI / UVAI)
Retrieved from TROPOMI ($354\text{ nm}$ and $388\text{ nm}$), measuring the residual between observed UV reflectance and pure Rayleigh scattering:
$$\text{AAI} = -100 \left[ \log_{10}\left(\frac{I_{354}^{\text{obs}}}{I_{388}^{\text{obs}}}\right) - \log_{10}\left(\frac{I_{354}^{\text{calc}}}{I_{388}^{\text{calc}}}\right) \right]$$
* **$\text{AAI} > 2.0$:** Elevated absorbing desert dust or smoke, even when floating over low cloud decks.

---

## 🎨 3. WMO / EUMETSAT 24-Bit Dust RGB Composite Recipe

The internationally recognized WMO standard for visual tracking of sand and dust storms maps thermal infrared brightness temperature differences into Red, Green, and Blue channels:

| Color Channel | Physical Band Difference | Min Clipping ($K$) | Max Clipping ($K$) | Gamma ($\gamma$) | Visual Interpretation |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **RED** | $\text{BTD}(12.0\mu\text{m} - 10.8\mu\text{m})$ | $-4.0\text{ K}$ | $+2.0\text{ K}$ | $1.0$ | Silicate mineral dust optical depth. |
| **GREEN**| $\text{BTD}(10.8\mu\text{m} - 8.7\mu\text{m})$ | $0.0\text{ K}$ | $+15.0\text{ K}$ | $2.5$ | Particle phase and optical thickness. |
| **BLUE** | $T_b(10.8\mu\text{m})$ | $261.0\text{ K}$ | $+289.0\text{ K}$| $1.0$ | Surface and cloud top temperature. |

### Color Interpretation Guide:
* 🟪 **Bright Magenta / Vibrant Pink:** **Active Sand and Dust Storm** (High Red, Moderate Green, Low Blue).
* 🟥 **Dark Red / Ochre:** Thin airborne dust haze or high-altitude dust transport.
* 🟦 **Light Cyan / Blue:** Warm desert bare ground during clear daytime.
* 🟫 **Dull Brown / Orange:** Thick water droplet clouds.
* ⬛ **Black / Dark Red:** Cold high-altitude ice cirrus tops.

---

## ⚙️ 4. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Description |
| :--- | :---: | :---: | :---: | :--- |
| `nddi_threshold` | `float` | `0.28` | `0.25 - 0.35` | Minimum NDDI value confirming mineral dust. |
| `rgb_gamma_green`| `float` | `2.5` | `2.0 - 2.8` | Non-linear gamma exponent expanding contrast for Green channel. |
| `red_min_k` | `float` | `-4.0` | `-5.0 to -3.0` | Lower thermal clamping limit for $\text{BTD}_{12-11}$ in Red channel. |
| `red_max_k` | `float` | `2.0` | `1.0 - 3.0` | Upper thermal clamping limit for $\text{BTD}_{12-11}$ in Red channel. |
| `green_min_k` | `float` | `0.0` | `0.0 - 1.0` | Lower thermal clamping limit for $\text{BTD}_{11-8.7}$ in Green channel. |
| `green_max_k` | `float` | `15.0` | `12.0 - 18.0` | Upper thermal clamping limit for $\text{BTD}_{11-8.7}$ in Green channel. |
| `blue_min_k` | `float` | `261.0` | `255.0 - 265.0` | Lower temperature limit for $T_b(10.8\mu\text{m})$ in Blue channel. |
| `blue_max_k` | `float` | `289.0` | `285.0 - 295.0` | Upper temperature limit for $T_b(10.8\mu\text{m})$ in Blue channel. |

---

## 💡 5. Automated Python Composite & Index Generator

```python
import numpy as np

def compute_nddi(rho_blue_047: np.ndarray, rho_swir_213: np.ndarray) -> np.ndarray:
    """
    Computes Normalized Difference Dust Index (NDDI).
    """
    denom = rho_swir_213 + rho_blue_047
    with np.errstate(invalid='ignore', divide='ignore'):
        nddi = (rho_swir_213 - rho_blue_047) / np.maximum(denom, 1e-4)
    return np.clip(nddi, -1.0, 1.0)

def generate_wmo_dust_rgb(bt_8_7: np.ndarray, bt_10_8: np.ndarray, bt_12_0: np.ndarray) -> np.ndarray:
    """
    Renders standard 24-bit WMO Dust RGB composite [Height, Width, 3].
    Output normalized in [0.0, 1.0].
    """
    # 1. Red Channel: BTD(12.0 - 10.8), Range [-4.0, 2.0], Gamma = 1.0
    r_diff = bt_12_0 - bt_10_8
    red = (r_diff - (-4.0)) / (2.0 - (-4.0))
    red = np.clip(red, 0.0, 1.0)

    # 2. Green Channel: BTD(10.8 - 8.7), Range [0.0, 15.0], Gamma = 2.5
    g_diff = bt_10_8 - bt_8_7
    green = (g_diff - 0.0) / (15.0 - 0.0)
    green = np.clip(green, 0.0, 1.0)
    green = green ** (1.0 / 2.5)  # Apply non-linear gamma expansion

    # 3. Blue Channel: BT(10.8), Range [261.0, 289.0], Gamma = 1.0
    blue = (bt_10_8 - 261.0) / (289.0 - 261.0)
    blue = np.clip(blue, 0.0, 1.0)

    # Stack into 3-channel RGB image
    rgb_composite = np.stack([red, green, blue], axis=-1)
    return rgb_composite
```
