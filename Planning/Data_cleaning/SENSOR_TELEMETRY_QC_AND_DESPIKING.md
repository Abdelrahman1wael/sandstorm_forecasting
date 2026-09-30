# 🔍 Sensor Telemetry Quality Control & Despiking
### *Detecting Mechanical Flatlines, Negative Baseline Drift & Electronic Artifact Spikes*
**Sensor Modalities:** Beta-Attenuation (BAM), Tapered Element Oscillating Microbalance (TEOM), Ultrasonic Anemometers  
**Target Indicators:** $\text{PM}_{10}, \text{PM}_{2.5}$, 10m Wind Speed, Atmospheric Pressure, Relative Humidity  
**Output Target:** Certified Non-Corrupted Continuous Physical Telemetry Streams

---

## 🎯 1. Operational Goal & Real-World Sensor Failures

Ground monitoring stations in northwest China operate in harsh desert and sub-zero conditions (temperatures from $-30^\circ\text{C}$ to $+45^\circ\text{C}$, severe grit abrasion). These environmental extremes produce three pervasive failure modes:

1. **Mechanical Flatlines (Frozen Sensors):** Dust ingress jams the mechanical filter tape feeder in Beta-Attenuation Monitors, or telemetry software loops, outputting identical numbers (e.g., exactly $42.00 \ \mu\text{g/m}^3$) for days.
2. **Negative Baseline Calibration Drift:** Rapid nocturnal cooling shifts optical baseline voltages, causing sensors to log impossible negative concentrations (e.g., $-18.5 \ \mu\text{g/m}^3$).
3. **Electronic Noise Spikes vs. Synoptic Sandstorm Peaks:** Insects entering the sampling inlet, electrical surges, or localized nearby vehicle exhaust generate single-point spikes ($4,000 \ \mu\text{g/m}^3$) that can be falsely interpreted as regional sandstorms.

---

## 📐 2. Mathematical Detection Rules & Invariant Tests

```
+---------------------------------------------------------------------------------------------------+
|                            THE 4-STAGE TELEMETRY SANITIZATION PIPELINE                            |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [TEST 1: Physical Plausibility Limits]       0.0 <= PM10 <= 10,000 μg/m³,  0 <= RH <= 100%       |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [TEST 2: Negative Value Clamping]            Negative baseline drift clamped: max(0.0, x)        |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [TEST 3: Zero-Variance Flatline Detector]    Rolling std dev over window: σ_12h < 0.05 μg/m³     |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [TEST 4: Rolling MAD Despiking]              Modified Z-Score M_i > 4.5 WITH Spatial Check       |
+---------------------------------------------------------------------------------------------------+
```

---

### 2.1 Physical Range Constraints
Observations outside physically possible terrestrial atmospheric limits are immediately set to `NaN`:

$$\text{Valid Range}: \quad 0.0 \le \text{PM}_{10} \le 10,000 \ \mu\text{g/m}^3$$
$$\text{Valid Range}: \quad 0.0 \le U_{10} \le 60.0 \ \text{m/s}$$
$$\text{Valid Range}: \quad 0.0\% \le \text{RH} \le 100.0\%$$
$$\text{Valid Range}: \quad 500.0 \le P_{\text{surface}} \le 1080.0 \ \text{hPa}$$

---

### 2.2 Zero-Variance Flatline Detector
A sensor is flagged as mechanically frozen if its rolling standard deviation over a 12-hour window falls below measurement resolution:

$$\sigma_{12\text{h}}(t) = \sqrt{\frac{1}{12} \sum_{k=0}^{11} \left(x_{t-k} - \bar{x}_{12\text{h}}\right)^2}$$
$$\text{Is Flatline}: \quad \sigma_{12\text{h}}(t) < 0.05 \ \mu\text{g/m}^3 \quad \land \quad \text{Consecutive Repetitions} \ge 6$$
*When flagged, the frozen window is converted to `NaN` and routed to Stage 2 for spatial interpolation.*

---

### 2.3 Rolling Median Absolute Deviation (MAD) Despiking
Standard Z-scores ($\frac{x - \mu}{\sigma}$) fail in sandstorm data because extreme storms heavily distort the sample mean $\mu$ and standard deviation $\sigma$. The **Modified Z-Score ($M_i$)** based on the median and Median Absolute Deviation (MAD) is inherently outlier-resistant:

$$\text{MAD}_t = \text{median}\left(\left| x_k - \tilde{x}_t \right|\right), \quad k \in [t - W, \ t + W]$$
$$M_i = \frac{0.6745 \cdot \left| x_i - \tilde{x}_t \right|}{\max(\text{MAD}_t, \ 1.0)}$$

Where $\tilde{x}_t$ is the rolling median over window $W = 12\text{ hours}$.

#### Spatial Corroboration Requirement (Differentiating Noise from Real Storms):
A candidate spike ($M_i > 4.5$) is flagged as **an isolated electronic artifact** ONLY IF:
1. It lasts for $\le 2$ consecutive hours, **AND**
2. No neighboring station within $100\text{ km}$ observes an elevated $\text{PM}_{10} > 300 \ \mu\text{g/m}^3$, **AND**
3. Local wind speed $U_{10} < 5.0\text{ m/s}$ (aerodynamically incapable of local saltation).

*If neighboring stations corroborate the rise or wind speed is severe ($U_{10} > 10\text{ m/s}$), the spike is preserved as a genuine frontal dust storm.*

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `max_pm10_ceiling` | `float` | `10000.0` | `8000 - 15000` | Absolute physical ceiling ($\mu\text{g/m}^3$) for extreme particulate sensor range. |
| `flatline_window_h` | `int` | `12` | `6 - 24` | Rolling window length (hours) for flatline evaluation. |
| `flatline_std_threshold`| `float`| `0.05` | `0.01 - 0.10` | Standard deviation floor indicating frozen sensor output. |
| `mad_window_h` | `int` | `12` | `6 - 24` | Window width for rolling median and MAD calculation. |
| `modified_z_cutoff` | `float` | `4.5` | `3.5 - 6.0` | Modified Z-score threshold for candidate spike detection. |
| `neighbor_radius_km` | `float` | `100.0` | `50 - 150` | Search radius for spatial neighbor corroboration of candidate spikes. |

---

## 💡 4. Automated Python Despiking Implementation

```python
import numpy as np
import pandas as pd

def clean_sensor_telemetry(df: pd.DataFrame, pm10_col: str = "pm10", wind_col: str = "u10") -> pd.DataFrame:
    """
    Cleans raw particulate time-series telemetry.
    """
    df_clean = df.copy()
    pm10 = df_clean[pm10_col].to_numpy(dtype=float)
    wind = df_clean[wind_col].to_numpy(dtype=float) if wind_col in df_clean else np.zeros_like(pm10)

    # 1. Physical range clamping & negative baseline removal
    pm10 = np.where(pm10 > 10000.0, np.nan, pm10)
    pm10 = np.where(pm10 < 0.0, 0.0, pm10)  # Clamp negative calibration drift to 0

    # 2. Detect mechanical zero-variance flatlines (rolling 12 hours)
    s_pm10 = pd.Series(pm10)
    rolling_std = s_pm10.rolling(window=12, min_periods=6).std()
    flatline_mask = (rolling_std < 0.05) & (s_pm10.rolling(window=6).apply(lambda x: len(np.unique(x)) == 1, raw=True) == 1)
    pm10 = np.where(flatline_mask, np.nan, pm10)

    # 3. Rolling MAD Despiking
    rolling_median = s_pm10.rolling(window=13, center=True, min_periods=5).median()
    rolling_mad = s_pm10.rolling(window=13, center=True, min_periods=5).apply(
        lambda x: np.nanmedian(np.abs(x - np.nanmedian(x))), raw=True
    )
    rolling_mad = np.maximum(rolling_mad, 2.0)  # Avoid division by zero

    mod_z = 0.6745 * np.abs(pm10 - rolling_median) / rolling_mad

    # Candidate noise spikes: extreme Z-score occurring during calm wind (< 4 m/s)
    isolated_noise_spike = (mod_z > 4.5) & (wind < 4.0) & (pm10 > 1000.0)
    pm10 = np.where(isolated_noise_spike, np.nan, pm10)

    df_clean[pm10_col] = pm10
    return df_clean
```
