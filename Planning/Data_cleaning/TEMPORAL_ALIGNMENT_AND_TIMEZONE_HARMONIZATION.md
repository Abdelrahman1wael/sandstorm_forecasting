# ⏱️ Temporal Alignment & Timezone Harmonization
### *Eliminating the 8-Hour Phase Shift, Reconciling Irregular Sampling & Synoptic Aggregation*
**Core Synchronization Standard:** Coordinated Universal Time (UTC / GMT) & ISO 8601  
**Target Feeds:** ECMWF (UTC), CMA-GFS (UTC), MEE Stations (CST / UTC+8), FY-4A (UTC)  
**Output Target:** Spatiotemporally Aligned Hourly & 6-Hour Synoptic Forecasting Records

---

## 🎯 1. The Critical 8-Hour Phase Shift Error

The most frequent yet disastrous silent error in atmospheric artificial intelligence is **mixing timezones between numerical models and local ground sensors**:
* **Numerical Models (ECMWF-IFS, ERA5, GFS):** Explicitly run and archive output fields in **UTC** (cycles at 00:00, 06:00, 12:00, 18:00 UTC).
* **Chinese Environmental Monitoring Stations (MEE):** Record hourly particulate matter concentrations in **China Standard Time (CST / Beijing Time, UTC+8)**.

### The Catastrophic Result of Inaction:
When a researcher blindly merges datasets on date-time strings without explicit localization, the model is trained on a **fatal 8-hour temporal phase shift**:
* Peak diurnal thermal convective winds hitting at **16:00 CST (08:00 UTC)** are matched to numerical predictions for **16:00 UTC (00:00 midnight CST)**.
* The neural network learns that sandstorms strike in the dark during calm midnight inversions, completely inverting diurnal aerodynamic physics.

---

## 📐 2. Timezone Normalization Protocol

All datasets must undergo strict explicit timezone localization and conversion to **UTC** as the project's single source of truth before any spatial or feature merging occurs:

```
[MEE Station Raw Feed (CST / UTC+8)]
                   │
                   ▼
.dt.tz_localize("Asia/Shanghai")        # Attach explicit timezone
                   │
                   ▼
.dt.tz_convert("UTC")                   # Subtract exactly 8 hours to align with NWP
                   │
                   ▼
[Synchronized UTC Ground Baseline Matching ECMWF 00/06/12/18 UTC Forecast Slices]
```

---

## 🔄 3. Reconciling Heterogeneous Sampling Cadences

Different atmospheric measurement platforms operate at drastically different temporal intervals:

```
Platform / Source:               Raw Sampling Interval:      Target Unified Pipeline Step:
------------------------------------------------------------------------------------------
AWS Automatic Weather Stations:  1-minute / 10-minute        1-hour vector mean [t-1h, t]
MEE Ground Particulate Monitors: 1-hour rolling average      1-hour instantaneous stamp (UTC)
FY-4A/B AGRI Geostationary Sat:  15-minute rapid scan        Closest top-of-the-hour snapshot
MODIS Polar Orbiting Satellites: Twice-daily (10:30 & 13:30) Collocated by exact UTC swath time
ECMWF-IFS Numerical Ensemble:    3-hour / 6-hour cycles      3-hour synoptic forecast step
```

### 3.1 Aggregation & Resampling Rules
1. **Flow & Flux Variables ($\text{PM}_{10}, \text{PM}_{2.5}$, Total Precipitation):**  
   Must be aggregated via **backward-window interval integration**:
   $$\text{PM}_{10, \text{hourly}}(t) = \frac{1}{\Delta t} \int_{t - 1\text{h}}^{t} \text{PM}_{10}(\tau) \, d\tau$$
   *Represents the cumulative airborne mass concentration over the preceding hour.*
2. **State & Intensive Variables (Surface Pressure, 2m Temperature, Wind Speed):**  
   Sampled as **instantaneous snapshots** within $\pm 15$ minutes of the exact synoptic hour ($t$).
3. **Wind Direction Vector Averaging:**  
   Standard arithmetic averaging of wind direction degrees produces catastrophic errors (averaging $355^\circ$ and $5^\circ$ yields $180^\circ$ South instead of $0^\circ$ North). Wind vectors must be decomposed into Cartesian components:
   $$\bar{u} = \frac{1}{K} \sum_{k=1}^K -U_k \sin\left(\theta_k\right), \quad \bar{v} = \frac{1}{K} \sum_{k=1}^K -U_k \cos\left(\theta_k\right)$$
   $$\bar{\theta} = \text{atan2}\left(-\bar{u}, \ -\bar{v}\right) \pmod{360^\circ}$$

---

## ⚙️ 4. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Description / Physical Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `project_timezone` | `str` | `'UTC'` | Fixed (`'UTC'`) | Unified baseline timezone for all training tensors. |
| `local_station_tz` | `str` | `'Asia/Shanghai'` | `'Asia/Shanghai'` | Original timezone of Chinese meteorological station logs. |
| `target_resample_freq`| `str` | `'1h'` | `'1h'`, `'3h'`, `'6h'` | Unified resampling frequency string for Pandas / Polars. |
| `max_timestamp_tolerance_min`| `int` | `15` | `10 - 30` | Maximum allowable time delta (minutes) when snapping satellite swaths to hourly steps. |

---

## 💡 5. Automated Python Harmonization Pipeline

```python
import numpy as np
import pandas as pd

def harmonize_station_timestamps(
    df: pd.DataFrame, 
    datetime_col: str = "datetime_str", 
    is_beijing_time: bool = True
) -> pd.DataFrame:
    """
    Parses, localizes, and converts timestamps to UTC, resampling to clean 1-hour bins.
    """
    df_out = df.copy()

    # 1. Parse string to datetime
    dt_series = pd.to_datetime(df_out[datetime_col], errors="coerce")

    # 2. Localize to Beijing Time (CST / UTC+8) and convert to UTC
    if is_beijing_time:
        dt_utc = dt_series.dt.tz_localize("Asia/Shanghai").dt.tz_convert("UTC")
    else:
        dt_utc = dt_series.dt.tz_localize("UTC")

    df_out["datetime_utc"] = dt_utc
    df_out = df_out.dropna(subset=["datetime_utc"]).sort_values("datetime_utc")
    df_out = df_out.set_index("datetime_utc")

    # 3. Vector-aware resampling to exact 1-hour intervals
    resampled_records = {}
    for col in df_out.select_dtypes(include=[np.number]).columns:
        if "wind_dir" in col.lower() or "direction" in col.lower():
            # Circular vector mean
            rads = np.radians(df_out[col].values)
            sin_mean = pd.Series(np.sin(rads), index=df_out.index).resample("1h").mean()
            cos_mean = pd.Series(np.cos(rads), index=df_out.index).resample("1h").mean()
            dir_mean = np.degrees(np.arctan2(sin_mean, cos_mean)) % 360.0
            resampled_records[col] = dir_mean
        else:
            # Standard arithmetic mean for PM10, Temp, Pressure
            resampled_records[col] = df_out[col].resample("1h").mean()

    df_hourly = pd.DataFrame(resampled_records)
    return df_hourly.reset_index()
```
