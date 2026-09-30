# ☁️ Cloud Masking & Cloud-vs-Dust Discrimination
### *Infrared Split-Window Brightness Temperature Differencing (BTD) & Tri-Spectral Tests*
**Core Physical Law:** Reststrahlen Absorption Bands of Silicate Minerals ($\text{SiO}_2$)  
**Target Modalities:** MODIS Bands 29 ($8.5\mu\text{m}$), 31 ($11.0\mu\text{m}$), 32 ($12.0\mu\text{m}$) / FY-4A AGRI Bands 11, 12, 13  
**Output Target:** Binary Cloud Exclusion Mask & Calibrated Mineral Dust Confidence Flag

---

## 🎯 1. The Core Scientific Challenge

In satellite remote sensing of arid environments, **separating airborne sandstorms from meteorological clouds is notoriously difficult**:
1. **Visible Channel Ambiguity:** Both mineral dust plumes and low-level stratocumulus clouds exhibit high top-of-atmosphere reflectance in visible spectrums ($\rho_{0.65\mu\text{m}} > 0.25$).
2. **Bright Desert Backgrounds:** The underlying desert surface (e.g., Taklamakan dunes) has higher albedo than the airborne dust itself, causing standard automated cloud masks (such as MOD35) to falsely flag sandstorms as thick cirrus clouds and mask them out.

DustML overcomes this using **Thermal Infrared Split-Window Radiative Transfer**.

---

## 📐 2. Physical Principles & Mathematical Formulations

```
                  Wavelength Dependence of Refractive Index (k):
                  ---------------------------------------------
  Medium:         At 11.0 μm:           At 12.0 μm:           Resulting BTD (11μm - 12μm):
  Mineral Dust:   Low Absorption (k=0.1) High Absorption (k=0.3)  NEGATIVE  (BTD < -0.5 K)
  Water/Ice Cloud:High Absorption (k=0.3) Lower Absorption (k=0.2) POSITIVE  (BTD > +0.5 K)
```

### 2.1 The Split-Window BTD Test
Silicate minerals (quartz, feldspar, illite) dominant in East Asian desert sands possess a distinct **Reststrahlen absorption band** near $9\text{--}12\mu\text{m}$. 

Because silicate dust absorbs thermal infrared radiation more efficiently at $12.0\mu\text{m}$ than at $11.0\mu\text{m}$, the observed brightness temperature at $11\mu\text{m}$ is colder than at $12\mu\text{m}$ when looking down through an elevated dust plume:

$$\text{BTD}_{11 - 12} = T_b(11.0\mu\text{m}) - T_b(12.0\mu\text{m})$$

* **$\text{BTD}_{11 - 12} < -0.5\text{ K}$:** Characteristic signature of **Mineral Dust Plume**.
* **$\text{BTD}_{11 - 12} > +0.5\text{ K}$:** Signature of **Ice Cirrus or Water Droplet Cloud**.
* **$-0.5\text{ K} \le \text{BTD}_{11 - 12} \le +0.5\text{ K}$:** Clear-sky ground surface.

---

### 2.2 Tri-Spectral Dust-Cirrus Separation Test
Thin ice cirrus clouds over cold mountain plateaus (Tibetan Plateau, Qilian Mountains) can occasionally produce slightly negative $\text{BTD}_{11-12}$. To prevent false alarms, a **Tri-Spectral Difference Test** is applied using the $8.5\mu\text{m}$ channel:

$$\text{BTD}_{8.5 - 11} = T_b(8.5\mu\text{m}) - T_b(11.0\mu\text{m})$$

Because quartz has an extremely strong absorption peak at $8.5\mu\text{m}$, mineral dust exhibits:
$$\text{Dust Condition}: \quad \left(\text{BTD}_{11 - 12} < -0.5\text{ K}\right) \ \land \ \left(\text{BTD}_{8.5 - 11} > -2.0\text{ K}\right) \ \land \ \left(T_b(11.0\mu\text{m}) > 265\text{ K}\right)$$

*If $T_b(11.0\mu\text{m}) < 240\text{ K}$ ($-33^\circ\text{C}$), the target is definitively classified as high-altitude convective cloud tops or thick cirrus, overriding the dust flag.*

---

### 2.3 Water Vapor Correction
High atmospheric moisture (column water vapor $> 2.5\text{ g/cm}^2$) in southern and eastern China attenuates thermal infrared radiation and shifts $\text{BTD}_{11-12}$ toward positive values. The split-window threshold is dynamically adjusted based on NWP total column water vapor ($\text{TCWV}$):

$$\text{BTD}_{\text{threshold}} = -0.50 + 0.15 \cdot \text{TCWV} \quad (\text{Kelvin})$$

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `btd_dust_cutoff` | `float` | `-0.50` | `-1.20 to -0.30` | Maximum $\text{BTD}_{11-12}$ (Kelvin) for flagging mineral dust. More negative values increase precision. |
| `cloud_top_temp_min` | `float` | `265.0` | `255.0 - 273.0` | Minimum $T_b(11\mu\text{m})$ (Kelvin). Temperatures below this indicate high-altitude cold cloud tops. |
| `btd_cirrus_min` | `float` | `-2.0` | `-3.0 to -1.0` | Lower bound on $\text{BTD}_{8.5-11}$ separating dust from ice crystals. |
| `tcwv_coeff` | `float` | `0.15` | `0.10 - 0.25` | Dynamic threshold relaxation per $\text{g/cm}^2$ of atmospheric water vapor. |
| `spatial_filter_size`| `int` | `3` | `3 - 5` | Kernel size for $3 \times 3$ morphological opening to eliminate single-pixel sensor noise. |

---

## 📥 4. Input & Output Matrix Dimensions

### Input Rasters (2D float32 Arrays):
* `bt_8_5`: Brightness Temperature at $8.5\mu\text{m}$ (Kelvin)
* `bt_11_0`: Brightness Temperature at $11.0\mu\text{m}$ (Kelvin)
* `bt_12_0`: Brightness Temperature at $12.0\mu\text{m}$ (Kelvin)
* `tcwv`: Total Column Water Vapor ($\text{g/cm}^2$, from ECMWF ERA5)

### Output Masks (2D uint8 Arrays):
* `dust_mask`: `1` = Confirmed Mineral Dust Plume, `0` = No Dust.
* `cloud_mask`: `1` = Opaque Cloud Deck (must be gap-filled in Stage 3), `0` = Clear/Dust.

---

## 💡 5. Automated Python Discrimination Algorithm

```python
import numpy as np
from scipy.ndimage import binary_opening

def classify_dust_and_clouds(
    bt_8_5: np.ndarray,
    bt_11_0: np.ndarray,
    bt_12_0: np.ndarray,
    tcwv: np.ndarray = None
) -> dict:
    """
    Thermal Infrared Multi-Spectral Cloud vs. Dust Classifier.
    """
    # 1. Compute Split-Window Differences
    btd_11_12 = bt_11_0 - bt_12_0
    btd_85_11 = bt_8_5 - bt_11_0

    # 2. Dynamic thresholding for atmospheric moisture
    if tcwv is not None:
        threshold = -0.50 + 0.15 * np.clip(tcwv, 0.0, 4.0)
    else:
        threshold = -0.50

    # 3. Cloud Mask: Very cold cloud tops or positive split-window
    is_cold_cloud = bt_11_0 < 255.0
    is_water_cloud = (btd_11_12 > 1.2) & (bt_11_0 < 280.0)
    cloud_mask = is_cold_cloud | is_water_cloud

    # 4. Mineral Dust Mask:
    # Negative split-window + Warm enough to be in lower troposphere + Silicate tri-spectral test
    is_dust = (
        (btd_11_12 < threshold) &
        (bt_11_0 >= 265.0) &
        (btd_85_11 > -2.5) &
        (~cloud_mask)
    )

    # 5. Morphological cleaning: Remove single-pixel salt-and-pepper noise
    cleaned_dust_mask = binary_opening(is_dust, structure=np.ones((3, 3))).astype(np.uint8)

    return {
        "dust_mask": cleaned_dust_mask,
        "cloud_mask": cloud_mask.astype(np.uint8),
        "btd_11_12": btd_11_12
    }
```
