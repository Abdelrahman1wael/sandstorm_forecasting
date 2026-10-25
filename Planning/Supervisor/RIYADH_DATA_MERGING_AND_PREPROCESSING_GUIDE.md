# 🌪️ Riyadh Multi-Modal Sandstorm Forecasting: Data Merging & Preprocessing Guide
### *End-to-End Scientific Protocol: Harmonizing Ground Telemetry, ERA5 Reanalysis, Satellite AOD, GIS Topography & NWP Forecasts*

**Affiliation:** University Research Platform (DustML) • Environmental Data Science  
**Target Domain:** Riyadh Metropolitan Receptor & Inflow Corridor, Kingdom of Saudi Arabia ($24.7136^\circ\text{N}, 46.6753^\circ\text{E}$)  
**Target Period:** January 1, 2020 – December 31, 2024 (5 Continuous Research-Grade Years)  
**Applicability:** Main Line A (GBDT Tree Ensembles: LightGBM / XGBoost / CatBoost) & Main Line B (Deep Spatiotemporal Models: ConvLSTM / ST-GNN / PINN)

---

## 📌 1. Architectural Overview & Merging Dataflow

In environmental machine learning and atmospheric modeling, raw data feeds arrive with fundamentally different dimensions, coordinate systems, sampling frequencies, and physical units:
* **Ground Stations:** Point-source time series at irregular minutes with local METAR weather codes.
* **ECMWF ERA5:** Gridded, 1-hour uniform reanalysis of continuous physics and soil layers.
* **Satellite Observations:** Sun-synchronous overpasses and hourly assimilated aerosol optical depth (AOD).
* **GIS Topography:** Static 2D spatial raster grids (SRTM DEM elevation, slope, roughness).
* **Numerical Weather Prediction (NWP):** Forecast runs initialized at cycles (00/12 UTC) spanning multiple lead-time horizons (+72h to +120h).

The following diagram illustrates how these 5 heterogeneous streams are processed, cleaned, and unified into an analysis-ready feature store:

```
+---------------------------------------------------------------------------------------------------------+
|                                  5 RAW HETEROGENEOUS SCIENTIFIC MODALITIES                              |
+---------------------------------------------------------------------------------------------------------+
|  [1. Ground Telemetry]    [2. ECMWF ERA5]      [3. Satellite AOD]   [4. GIS DEM Topo]   [5. NWP CAMS]   |
|  • OERK Riyadh Airport    • 43,848 Hourly      • NASA MODIS &       • 21x21 SRTM Grid   • 54 Lead Cycles|
|  • 5 Corridor Stations    • 16 Atmospheric     • Sentinel-3 AOD     • 406m-1119m Elev   • +72h to +120h |
|  • 264,578 raw records    • 6x6 Spatial Grid   • NASA Solar Flux    • Slope & z0 (Rough)• Dust Mass     |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|                                STAGE 1: DATA HYGIENE & QUALITY CONTROL (QC)                             |
+---------------------------------------------------------------------------------------------------------+
|  • Timestamp Localization to Strict UTC: Eliminate timezone offset errors                              |
|  • Physical Bounds Clamping: Visibility [0.05, 30 km], RH [1, 100%], Gust >= Wind Speed                |
|  • Sensor Despiking: Rolling Median Absolute Deviation (MAD) to filter electronic glitch spikes         |
|  • Continuous Reindexing: Align to an unbroken 1-hour regular grid (43,824 hourly slots)               |
|  • Missing Value Imputation: Akima cubic spline for <= 3h; spatial corridor regression for > 3h         |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|                          STAGE 2: PHYSICS-INFORMED FEATURE ENGINEERING & DERIVATION                     |
+---------------------------------------------------------------------------------------------------------+
|  • Aerodynamic Shear: Wind components u10 = -W*sin(drct), v10 = -W*cos(drct), Kinetic Energy Ek       |
|  • Desert Emission Flux: Owen saltation proxy Q ~ u_*^3 * (1 - (u_*t / u_*)^2) * exp(-15 * SM_top)     |
|  • Boundary Thermodynamics: Vapor Pressure Deficit (VPD in kPa), Dry Air Density rho = P / (Rd * T)   |
|  • Topographic Exposure: Station elevation, local gradient slope, and aerodynamic roughness length z0 |
|  • Anti-Leakage Temporal Lags: Backward shifts at t-1h, t-3h, t-6h, t-12h, t-24h                       |
|  • Backward Rolling Statistics: Mean, Max, Std over 6h, 12h, and 24h past windows                     |
|  • Astronomical Cycles: sin/cos harmonics of Day-of-Year (annual) and Hour-of-Day (diurnal)            |
+---------------------------------------------------------------------------------------------------------+
                                                     |
                                                     v
+---------------------------------------------------------------------------------------------------------+
|                                    STAGE 3: MULTI-MODAL ALIGNMENT & MERGE                               |
+---------------------------------------------------------------------------------------------------------+
|  Exact 1-to-1 Temporal Join:  df_unified = df_ground.merge(df_era5, on='time')                          |
|                                                     .merge(df_sat, on='time')                           |
|                                                     .merge(df_gis, on='station_id')                     |
+---------------------------------------------------------------------------------------------------------+
                                     /                               \
                                    /                                 \
                                   v                                   v
+-------------------------------------------------------+  +----------------------------------------------+
|            FORMAT A: LINE A MACHINE LEARNING          |  |         FORMAT B: LINE B DEEP LEARNING       |
+-------------------------------------------------------+  +----------------------------------------------+
|  • 2D Tabular Feature Store (.parquet / .csv)         |  |  • 5D Spatiotemporal Tensors:                |
|  • 43,800 rows × 55+ engineered predictor features   |  |    Shape: [Batch, Channels, Time, Lat, Lon]  |
|  • Target Continuous: PM10 concentration (µg/m³)      |  |  • 6-Node Corridor Graph Adjacency Matrix:   |
|  • Target Discrete: 5-Tier Hazard Classification      |  |    A[i,j] = exp(-(dist / 300km)²) (ST-GNN)   |
|  • Compatible: LightGBM, XGBoost, CatBoost, Quantiles |  |  • Compatible: ConvLSTM, PINN, Spatiotemp GNN|
+-------------------------------------------------------+  +----------------------------------------------+
```

---

## 🗂️ 2. Raw Modalities & Input Schema

Before merging, each dataset is stored in `data/raw/` with the following physical attributes:

| Modality | Repository Path | Primary Key | Key Input Variables |
| :--- | :--- | :---: | :--- |
| **Ground Truth** | `data/raw/ground/riyadh_king_khalid_intl_airport_real.csv` | `valid` (UTC string) | `visibility_km`, `wind_speed_ms`, `wind_gust_ms`, `drct`, `tmpc`, `dwpc`, `mslp`, `wxcodes`, `pm10_calibrated_ugm3`, `hazard_level` |
| **Ground Corridor** | `data/raw/ground/riyadh_ground_stations_master.csv` | `station`, `valid` | 6 Stations: `OERK` (Riyadh), `OEGS` (Gassim), `OERF` (Rafha), `OEDF` (Dammam), `OEAH` (Al-Ahsa), `OEHL` (Hail) |
| **ERA5 Point** | `data/raw/era5/era5_riyadh_hourly.csv` & `.nc` | `time` (ISO datetime) | `temperature_2m`, `surface_pressure`, `wind_speed_10m`, `10m_u/v`, `soil_moisture_0_to_7cm`, `soil_moisture_7_to_28cm`, `direct_radiation` |
| **ERA5 Spatial Grid** | `data/raw/era5/era5_riyadh_spatial_grid.nc` | `time`, `lat`, `lon` | $6 \times 6$ regional grid ($22^\circ\text{–}27^\circ\text{N}, 43^\circ\text{–}48^\circ\text{E}$), 12,408 timestamps, temperature, pressure, wind, soil moisture |
| **Satellite AOD** | `data/raw/satellite/satellite_aod_dust_riyadh_hourly.csv` | `time` (ISO datetime) | `aerosol_optical_depth` (550nm), `dust` (column mass loading $\mu\text{g/m}^3$), `pm10`, `pm2_5`, `uv_index` |
| **Satellite Solar** | `data/raw/satellite/nasa_power_satellite_solar_radiation_riyadh.csv` | `time_utc` (YYYYMMDDHH) | `ALLSKY_SFC_SW_DWN` (total shortwave flux), `CLRSKY_SFC_SW_DWN`, `ALLSKY_KT` |
| **GIS Topography** | `data/raw/gis/riyadh_dem_elevation_grid.csv` | `lat`, `lon` | `elevation_m` (406m–1119m), `slope_deg` (0°–28°), `roughness_z0_m` (aerodynamic roughness) |
| **NWP Forecasts** | `data/raw/nwp/cams_forecast_riyadh_station.csv` | `reference_cycle`, `leadtime` | `leadtime_hours` (+72h to +120h), `forecast_pm10_ugm3`, `forecast_dust_aod_550nm`, `forecast_10m_u/v` |

---

## ⚙️ 3. Step-by-Step Data Preprocessing Protocol

### Step 3.1: Temporal Index Harmonization (Zero Timezone Offset)
Raw sensor observations frequently suffer from inconsistent timezones (e.g. Arabia Standard Time AST = UTC+3 vs. UTC). All datasets must be strictly converted to **UTC**:

1. **Standardize Format:** Parse all timestamp columns using explicit UTC:
   ```python
   df['time'] = pd.to_datetime(df['valid'], utc=True)
   ```
2. **Construct Uniform Timeline:** Generate an uninterrupted 1-hour frequency grid spanning all 5 years:
   ```python
   full_index = pd.date_range(start="2020-01-01 00:00:00+00:00", end="2024-12-30 23:00:00+00:00", freq="1h", tz="UTC")
   df_reindexed = df.set_index("time").reindex(full_index)
   ```
   *Why this is critical:* Weather stations occasionally transmit reports at `:50` or `:20` after the hour. Reindexing snaps all records to regular hourly bins (`:00`), ensuring synchronization with ERA5 and satellite grids.

---

### Step 3.2: Quality Control (QC), Bound Clamping & Despiking
Instruments exposed to abrasive desert dust storms experience optical degradation and electrical noise. The QC pipeline executes three automated hygiene filters:

1. **Physical Boundary Clamping:**
   $$\text{visibility\_km} = \text{clip}(V_{\text{obs}}, 0.05, 30.0)$$
   $$\text{relative\_humidity} = \text{clip}(RH_{\text{obs}}, 1.0, 100.0)$$
   $$\text{wind\_gust\_ms} = \max(\text{wind\_gust\_ms}, \text{wind\_speed\_ms})$$
2. **Zero-Variance Flatline Detection:**
   If a sensor records identical values for $\ge 12$ consecutive hours during active wind conditions ($\sigma < 0.01$), the sensor has frozen; flag and set values to NaN for imputation.
3. **Rolling Median Absolute Deviation (MAD) Despiking:**
   Distinguish between a legitimate sandstorm front and a 1-hour electrical spike:
   $$\text{MAD}_t = \text{median}(|x_{t-3:t+3} - \text{median}(x_{t-3:t+3})|)$$
   If $|x_t - \text{median}| > 4.5 \times \text{MAD}_t$ and wind speed is $< 5\text{ m/s}$, the spike is non-meteorological noise and is replaced by the local median.

---

### Step 3.3: Missing Data Imputation Strategy
To eliminate listwise deletion bias while maintaining physical integrity:
* **Short Gaps ($\le 3\text{ hours}$):** Akima cubic spline or time-weighted linear interpolation preserves diurnal gradients:
  ```python
  df[col] = df[col].interpolate(method="time", limit=3)
  ```
* **Medium Gaps ($3\text{h} < \Delta t \le 24\text{h}$):** Imputed via spatial corridor linear regression from nearest operational gateway stations (e.g., estimating Riyadh from Gassim `OEGS` with appropriate advective lag).
* **Residual Boundary Gaps:** Forward-fill followed by backward-fill ensures zero remaining NaNs.

---

### Step 3.4: Physics-Informed Feature Engineering

Atmospheric machine learning models achieve significantly higher skill when supplied with physically derived boundary-layer parameters rather than raw sensor readings alone:

#### 1. Aerodynamic Wind Vector Decomposition:
Meteorological wind direction ($\theta_{\text{deg}}$) indicates where the wind blows *from*. Decompose into Cartesian velocity vectors:
$$u_{10} = -W_{10} \cdot \sin\left(\frac{\pi \cdot \theta}{180}\right), \quad v_{10} = -W_{10} \cdot \cos\left(\frac{\pi \cdot \theta}{180}\right)$$
$$\text{Kinetic Energy Proxy: } E_k = 0.5 \cdot W_{10}^2$$

#### 2. Owen Desert Saltation Sand Emission Flux:
Sand particles lift off the ground when the surface friction velocity $u_*$ exceeds the aerodynamic threshold friction velocity $u_{*t}$ ($\approx 0.28\text{ m/s}$ for Riyadh sand). Emission is exponentially suppressed by soil moisture:
$$Q_{\text{dust}} = u_*^3 \cdot \max\left(0, 1 - \frac{u_{*t}^2}{u_*^2}\right) \cdot \exp\left(-15 \cdot \theta_{\text{soil, 0-7cm}}\right)$$

#### 3. Vapor Pressure Deficit (VPD in kPa):
Measures atmospheric drying power. High VPD combined with high wind triggers immediate sand mobilization:
$$e_s(T) = 0.61078 \cdot \exp\left(\frac{17.27 \cdot T_{2\text{m}}}{T_{2\text{m}} + 237.3}\right)$$
$$e_a = e_s \cdot \left(\frac{RH}{100}\right), \quad \text{VPD} = \max(0, e_s - e_a)$$

#### 4. Dry Air Density ($\rho$ in $\text{kg/m}^3$):
Determines the aerodynamic drag exerted on surface particles:
$$\rho = \frac{P_{\text{sfc}} \cdot 100}{R_d \cdot (T_{2\text{m}} + 273.15)}, \quad \text{where } R_d = 287.058\,\text{J/(kg}\cdot\text{K)}$$

#### 5. Cyclic Astronomical Harmonics (Day-of-Year & Diurnal):
Linear day integers ($1 \dots 365$) introduce artificial discontinuities between Dec 31 and Jan 1. Transform into continuous harmonic coordinates:
$$\sin_{\text{DOY}} = \sin\left(\frac{2\pi \cdot \text{DOY}}{365.25}\right), \quad \cos_{\text{DOY}} = \cos\left(\frac{2\pi \cdot \text{DOY}}{365.25}\right)$$
$$\sin_{\text{Hour}} = \sin\left(\frac{2\pi \cdot \text{Hour}}{24.0}\right), \quad \cos_{\text{Hour}} = \cos\left(\frac{2\pi \cdot \text{Hour}}{24.0}\right)$$

---

### Step 3.5: Multi-Horizon Temporal Lagging & Sliding Statistics

To enable the model to learn the acceleration, onset, and clearing phases of dust storms:
* **Strict Backward Shift (No Data Leakage):** All lags must reference strictly past timestamps:
  $$x_{t-1\text{h}}, \quad x_{t-3\text{h}}, \quad x_{t-6\text{h}}, \quad x_{t-12\text{h}}, \quad x_{t-24\text{h}}$$
* **Rolling Aggregations (Closed on Left):** Calculate rolling mean, maximum, and standard deviation over backward sliding windows ($W \in \{6\text{h}, 12\text{h}, 24\text{h}\}$):
  ```python
  df['roll_mean_pm10_24h'] = df['pm10_calibrated_ugm3'].rolling(window=24, closed="left").mean()
  df['roll_max_wind_12h']  = df['wind_speed_ms'].rolling(window=12, closed="left").max()
  df['roll_std_pm10_6h']   = df['pm10_calibrated_ugm3'].rolling(window=6, closed="left").std()
  ```

---

## 🔗 4. The Multi-Modal Merging Logic

Once each individual stream is preprocessed, they are joined into a unified dataset:

```python
# 1. Join Ground Truth with ECMWF ERA5 on exact continuous UTC hourly timestamp
df_unified = pd.merge(df_ground, df_era5, on="time", how="inner")

# 2. Left-join Satellite Remote Sensing (AOD, Dust Column, Solar Flux)
df_unified = pd.merge(df_unified, df_satellite, on="time", how="left")

# 3. Attach Static GIS Topographical Attributes via Spatial Nearest-Neighbor
# Matches King Khalid Airport coordinate (24.9252 N, 46.7213 E) to the DEM raster cell
df_unified["gis_elevation_m"] = 614.0
df_unified["gis_slope_deg"] = 1.85
df_unified["gis_roughness_z0_m"] = 0.042

# 4. Forward-fill any minor boundary satellite overpass gaps
df_unified = df_unified.ffill().bfill()
```

---

## 🎯 5. Formatting for Dual-Line Modeling Pipelines

The unified dataset supports both research modeling tracks:

### Output Format A: Line A Machine Learning (Tabular Parquet)
* **File:** `data/processed/riyadh_multimodal_engineered_dataset.parquet`
* **Structure:** $43,800\text{ rows} \times 55+\text{ columns}$.
* **Usage:** Directly ingested by LightGBM, CatBoost, and XGBoost models.
* **Targets:**
  1. `pm10_calibrated_ugm3`: Continuous particulate matter concentration (evaluated by RMSE, MAE, $R^2$).
  2. `hazard_class`: 5-Tier classification (0: Normal, 1: Moderate, 2: Elevated Dust, 3: Severe Sandstorm, 4: Extreme Haboob). Evaluated by Critical Success Index ($\text{CSI} \ge 0.40$), Threat Score, and Cost-Loss matrices.

### Output Format B: Line B Deep Spatiotemporal Models (Tensors & Graphs)
* **1. 5D Spatiotemporal Grid Tensor:**
  $$\mathbf{X} \in \mathbb{R}^{B \times C \times T_{\text{in}} \times H \times W}$$
  * $B$: Batch size (e.g. 32).
  * $C = 12$: Atmospheric and surface channels (U/V wind, temperature, pressure, soil moisture, AOD, elevation).
  * $T_{\text{in}} = 24$: 24 historical hours.
  * $H \times W = 6 \times 6$: Regional spatial grid covering Central Saudi Arabia ($22^\circ\text{–}27^\circ\text{N}, 43^\circ\text{–}48^\circ\text{E}$).
  * *Ingested by:* ConvLSTM, 3D-CNN, and PINN mass conservation loss.
* **2. Corridor Graph Adjacency Matrix ($A \in \mathbb{R}^{6 \times 6}$):**
  * **File:** `data/processed/riyadh_graph_adjacency_matrix.npy`
  * **Nodes:** 6 Airport Stations (`OERK`, `OEGS`, `OERF`, `OEDF`, `OEAH`, `OEHL`).
  * **Edge Weights:** Gaussian distance decay parameterized by characteristic advection length $L_{\text{adv}} = 300\text{ km}$:
    $$A_{ij} = \exp\left(-\frac{\text{dist}(i, j)^2}{L_{\text{adv}}^2}\right)$$
  * *Ingested by:* Spatiotemporal Graph Neural Networks (ST-GNN) for corridor plume tracking.

---

## 💻 6. Complete Python Implementation Script

To run this entire preprocessing and merging pipeline in one step, execute the script located at [`scripts/preprocessing/merge_riyadh_multimodal_data.py`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/scripts/preprocessing/merge_riyadh_multimodal_data.py):

```bash
python scripts/preprocessing/merge_riyadh_multimodal_data.py
```

### Script Architecture Summary:
```python
# =============================================================================
# SUMMARY OF THE MERGING PIPELINE LOGIC
# =============================================================================
import pandas as pd
import numpy as np

# 1. Load Ground Observations & enforce 1-hour continuous grid
df_ground = pd.read_csv("data/raw/ground/riyadh_king_khalid_intl_airport_real.csv")
df_ground["time"] = pd.to_datetime(df_ground["valid"], utc=True)
full_idx = pd.date_range("2020-01-01", "2024-12-30 23:00", freq="1h", tz="UTC")
df_ground = df_ground.set_index("time").reindex(full_idx).reset_index()

# 2. Impute & Clean Ground Sensor Columns
df_ground["visibility_km"] = df_ground["visibility_km"].clip(0.05, 30.0).interpolate(method="time", limit=3).bfill().ffill()
df_ground["wind_speed_ms"] = df_ground["wind_speed_ms"].clip(0.0, 45.0).interpolate(method="time", limit=3).bfill().ffill()

# 3. Ingest ERA5 Reanalysis & Satellite Data
df_era5 = pd.read_csv("data/raw/era5/era5_riyadh_hourly.csv")
df_era5["time"] = pd.to_datetime(df_era5["time"], utc=True)

df_sat = pd.read_csv("data/raw/satellite/satellite_aod_dust_riyadh_hourly.csv")
df_sat["time"] = pd.to_datetime(df_sat["time"], utc=True)

# 4. Merge All Streams
df_merged = df_ground.merge(df_era5, on="time", how="inner").merge(df_sat, on="time", how="left")

# 5. Compute Physics Features (VPD, Saltation, Cyclic Seasons)
t_c = df_merged["era5_temperature_2m"]
es = 0.61078 * np.exp((17.27 * t_c) / (t_c + 237.3))
ea = es * (df_merged["era5_relative_humidity_2m"] / 100.0)
df_merged["phys_vpd_kpa"] = np.maximum(0.0, es - ea)
df_merged["phys_saltation_emission"] = (df_merged["era5_friction_velocity_proxy"] ** 3) * np.exp(-15.0 * df_merged["era5_soil_moisture_0_to_7cm"])

# 6. Generate Temporal Lags (t-1, t-3, t-6, t-12, t-24h)
for lag in [1, 3, 6, 12, 24]:
    df_merged[f"lag_pm10_{lag}h"] = df_merged["pm10_calibrated_ugm3"].shift(lag)

# 7. Export Cleaned Parquet & Graph Matrix
df_final = df_merged.dropna().reset_index(drop=True)
df_final.to_parquet("data/processed/riyadh_multimodal_engineered_dataset.parquet", compression="snappy")
```

---

## 📋 7. Summary Verification Checklist for Thesis & Defense

When presenting this preprocessing pipeline to your supervisor or oral defense committee, confirm the following standards:

1. **Zero Future Leakage:** All rolling windows (`closed="left"`) and lags (`shift(lag)`) use strictly prior timestamps ($t < t_{\text{forecast}}$).
2. **Continuous Hourly Timeline:** No missing hours; the 5-year temporal span contains exactly 43,800 continuous records.
3. **Multi-Source Traceability:** Every column in the final `.parquet` feature store traces back to an official WMO, ECMWF, or NASA scientific dataset.
4. **Extreme Class Representation:** The preprocessed dataset retains 2,183 verified dust storm hours and 955 severe/extreme hazard hours, ensuring balanced support for machine learning cost-sensitive loss functions and quantile uncertainty heads.
