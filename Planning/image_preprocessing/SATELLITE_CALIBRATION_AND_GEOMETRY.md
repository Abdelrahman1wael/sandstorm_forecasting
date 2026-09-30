# 📐 Satellite Radiometric Calibration & Geometric Correction
### *Transforming Raw Digital Numbers (DN) into Calibrated TOA Reflectance & Brightness Temperature*
**Sensor Suite:** MODIS (Terra/Aqua), FY-4A/4B AGRI, Himawari-8/9 AHI  
**Processing Level:** Level 1A / Level 1B $\longrightarrow$ Georeferenced Calibrated Radiance  
**Output Target:** Top-of-Atmosphere (TOA) Reflectance $\rho_{\text{TOA}}$ & Brightness Temperature $T_b$

---

## 🎯 1. Operational Goal & Scientific Importance

Raw satellite telemetry files store measurements as raw integer **Digital Numbers (DN)** produced by onboard detector analog-to-digital converters (e.g., 12-bit or 14-bit unsigned integers: $0 \le \text{DN} \le 4095$ or $16383$).

Direct use of raw DN leads to catastrophic model failure because:
1. **Sensor Degradation & Drift:** Optical detector sensitivity degrades over orbital lifespan (e.g., Terra MODIS optics have degraded by $> 15\%$ since launch in 1999).
2. **Solar Geometry Variations:** Radiance reaching the sensor varies dynamically with solar zenith angle $\theta_0$ and seasonal Earth-Sun astronomical distance $d_{\text{ES}}$.
3. **Bow-Tie Effect:** For cross-track scanning instruments like MODIS, detector footprints expand and overlap toward the swath edges (expanding from $1\text{ km}$ at nadir to $2.0 \times 4.8\text{ km}$ at $\pm 55^\circ$ scan angle), duplicating pixels and distorting desert plume geography.

This stage converts raw DN into physically calibrated, normalized **TOA Reflectance** (solar bands) and **Planck Brightness Temperature** (thermal infrared bands), while rectifying orbital swath geometry.

---

## 📐 2. Mathematical Formulations

### 2.1 Reflectance Calibration (Solar Reflective Bands: $0.4\mu\text{m} - 2.2\mu\text{m}$)
Converts raw integer DN into dimensionless Top-of-Atmosphere (TOA) bidirectional reflectance factor ($\rho_{\text{TOA}}$):

$$\rho_{\text{TOA}}(\lambda) = \frac{\pi \cdot L_{\text{TOA}}(\lambda) \cdot d_{\text{ES}}^2}{E_{\text{sun}}(\lambda) \cdot \cos(\theta_0)}$$

Where:
* $L_{\text{TOA}}(\lambda)$: Calibrated spectral radiance ($\text{W}\cdot\text{m}^{-2}\cdot\text{sr}^{-1}\cdot\mu\text{m}^{-1}$):
  $$L_{\text{TOA}}(\lambda) = \text{scale\_factor} \times (\text{DN} - \text{add\_offset})$$
* $d_{\text{ES}}$: Earth-Sun distance in Astronomical Units (AU) at Julian day $\text{JD}$:
  $$d_{\text{ES}} \approx 1.0 - 0.01672 \cdot \cos\left(\frac{2\pi (\text{JD} - 4)}{365.256}\right)$$
* $E_{\text{sun}}(\lambda)$: Mean extraterrestrial solar spectral irradiance at 1 AU.
* $\theta_0$: Solar Zenith Angle at the target pixel $(x, y)$.

---

### 2.2 Thermal Radiative Calibration & Planck Inversion (IR Bands: $3.7\mu\text{m} - 13.5\mu\text{m}$)
Thermal infrared channels measure terrestrial and atmospheric blackbody emission. Radiance $L_{\text{therm}}$ is converted into equivalent **Brightness Temperature ($T_b$)** in Kelvin ($K$) by inverting the Planck Radiation Law:

$$T_b = \frac{c_2}{\lambda \cdot \ln\left(1 + \frac{c_1}{\lambda^5 \cdot L_{\text{therm}}}\right)}$$

Where:
* $c_1 = 2 \pi h c^2 = 1.191042 \times 10^8 \ \text{W}\cdot\mu\text{m}^4\cdot\text{m}^{-2}\cdot\text{sr}^{-1}$ (First radiation constant).
* $c_2 = \frac{h c}{k_B} = 1.438775 \times 10^4 \ \mu\text{m}\cdot\text{K}$ (Second radiation constant).
* $\lambda$: Central band wavelength (e.g., $11.03\mu\text{m}$ for MODIS Band 31, $12.02\mu\text{m}$ for Band 32).
* Sensor-specific band temperature adjustment:
  $$T_b^* = A + B \cdot T_b$$
  *(Where $A$ and $B$ are empirical sensor calibration coefficients accounting for finite filter bandwidth).*

---

### 2.3 Bow-Tie Effect Rectification (MODIS Specific)
The MODIS scan mirror sweeps a $\pm 55^\circ$ swath width of $2,330\text{ km}$. Toward the scan margins, consecutive 10-detector scans overlap by up to $50\%$.

```
Scan N:    ==================== (Nadir: 1 km pixel) ====================
Scan N+1:  ==================== (Margin: 4.8 km pixel, 50% overlap) ====================
```

**Correction Protocol:**
1. Pixel positions along each 10-scan line are computed using exact satellite ephemeris angles.
2. Overlapping duplicate pixels at scan angles $|\theta| > 35^\circ$ are trimmed using the **nearest-to-nadir selection rule** or resampled via elliptical Gaussian aperture weighting.

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Description / Physical Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `sensor` | `str` | `'MODIS_Terra'` | `'MODIS_Terra'`, `'MODIS_Aqua'`, `'FY4A_AGRI'` | Target satellite platform. |
| `solar_zenith_limit` | `float` | `80.0` | `70.0 - 85.0` | Maximum solar zenith angle ($\theta_0$ degrees). Pixels beyond $80^\circ$ (terminator twilight) are masked. |
| `bowtie_trim_angle` | `float` | `38.0` | `35.0 - 45.0` | Scan angle threshold (degrees) where bow-tie edge decimation initiates. |
| `scale_factor` | `float` | Sensor-specific | Read from HDF attributes | Multiplicative gain scalar converting integer DN to physical radiance. |
| `add_offset` | `float` | Sensor-specific | Read from HDF attributes | Additive offset intercept in calibration formula. |
| `target_projection`| `str` | `'EPSG:4326'` | `'EPSG:4326'`, `'EPSG:4490'` | Geodetic reference system for remapped grid. |

---

## 📥 4. Input File Specifications

* **MODIS L1B:** `MOD021KM` (Terra) / `MYD021KM` (Aqua) HDF4 format. Contains calibrated radiances for Bands 1–36.
* **MODIS Geolocation:** `MOD03` / `MYD03` HDF4 format. Contains exact latitude, longitude, solar zenith, solar azimuth, sensor zenith, and sensor azimuth for every $1\text{ km}$ pixel.
* **FY-4A/B L1:** `FY4A-_AGRI--_N_DISK_1047E_L1B` HDF5 format.

---

## 💡 5. Automated Python Processing Script

```python
import numpy as np
import h5py

def calibrate_modis_l1b(rad_dn: np.ndarray, scale: float, offset: float) -> np.ndarray:
    """
    Converts raw integer DN to calibrated TOA spectral radiance.
    """
    valid_mask = (rad_dn >= 0) & (rad_dn <= 32767)
    radiance = np.where(valid_mask, scale * (rad_dn - offset), np.nan)
    return radiance

def radiance_to_brightness_temperature(radiance: np.ndarray, wavelength_um: float) -> np.ndarray:
    """
    Planck Radiation Inversion to Brightness Temperature (Kelvin).
    """
    c1 = 1.191042e8  # W * um^4 / (m^2 * sr)
    c2 = 1.438775e4  # um * K
    
    with np.errstate(invalid='ignore', divide='ignore'):
        val = 1.0 + (c1 / ((wavelength_um ** 5) * np.maximum(radiance, 1e-4)))
        bt = c2 / (wavelength_um * np.log(val))
    
    # Physical terrestrial bounds: 180K (-93C) to 340K (+67C)
    bt_clipped = np.clip(bt, 180.0, 340.0)
    return bt_clipped

def compute_toa_reflectance(radiance: np.ndarray, solar_zenith_deg: np.ndarray, es_dist_au: float, esun: float) -> np.ndarray:
    """
    Converts solar channel radiance to bidirectional TOA reflectance factor [0, 1.2].
    """
    cos_sza = np.cos(np.radians(solar_zenith_deg))
    cos_sza = np.maximum(cos_sza, 0.1) # Mask twilight
    
    rho_toa = (np.pi * radiance * (es_dist_au ** 2)) / (esun * cos_sza)
    return np.clip(rho_toa, 0.0, 1.2)
```
