# 📦 Comprehensive Guide to All Data Types, Modalities & Sources
### *Multi-Source Heterogeneous Data Ecosystem for Extended-Range Sand and Dust Storm (SDS) Forecasting & Socioeconomic Analytics*

**Affiliation:** University of Science and Technology Beijing (北京科技大学) • School of Energy and Environmental Engineering  
**Target Horizon:** Extended-Range (3–15 Days) & Sub-seasonal to Seasonal (S2S) Horizons  

---

## 🌟 Executive Overview: The Multi-Modal Data Ecosystem

Predicting sand and dust storms beyond the traditional 72-hour barrier requires breaking data silos. A single data type (such as standalone ground sensors or raw weather simulations) is insufficient:
* **Numerical Weather Prediction (NWP)** provides dynamic atmospheric fluid mechanics, but suffers exponential chaos error beyond 3 days.
* **Satellites** provide massive spatial coverage of dust plumes and soil moisture, but only represent 2D surface reflections without vertical profiles.
* **Ground Stations** provide ground-truth particulate matter concentrations, but are geographically sparse across vast desert source basins.
* **Climate Indices** capture sub-seasonal teleconnections, but cannot resolve local synoptic gale fronts.
* **Socio-Economic Surveys** capture human vulnerability, but require spatial environmental exposure from GIS to establish causality.

To overcome these limitations, the **DustML Platform** harmonizes **7 distinct data modalities** into a unified spatiotemporal tensor ingestion pipeline:

```
+---------------------------------------------------------------------------------------------------+
|                        THE 7 HETEROGENEOUS SCIENTIFIC DATA MODALITIES                             |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [1. NWP Ensemble Forecasts]       [2. Atmospheric Reanalysis]      [3. Satellite Earth Obs.]    |
|   • ECMWF-IFS, CMA-GFS, GEOS-CF     • ERA5 Reanalysis (1979-pres)    • MODIS, FY-4A/B, Sentinel-2 |
|   • Wind u/v, MSLP, T2m, BLH        • Z500, Z700, 40-yr climatology  • AOD, NDVI, FVC, Soil Moist.|
|                     \                            |                           /                    |
|                      \                           |                          /                     |
|                       v                          v                         v                      |
|                     +-------------------------------------------------------+                     |
|                     |        SPATIOTEMPORAL TENSOR HARMONIZATION            |                     |
|                     |  • Regrid to 0.125° Grid   • Temporal UTC Alignment   |                     |
|                     |  • Spatial Kriging Impute  • Z-score Normalization    |                     |
|                     +---------------------------+---------------------------+                     |
|                                                 |                                                 |
|                                                 v                                                 |
|  [4. Ground In-Situ Stations]  ===============> |  [DUSTML PREDICTIVE CORE]                       |
|   • 2,400+ CMA Synoptic Sensors                 |   • Line A: Tree Bias Correction                |
|   • Hourly PM10/PM2.5, Visibility               |   • Line B: AI-GAMFS + PINN + ST-GNN            |
|   • Dust weather codes (WW=06-09)               |   • Uncertainty Quantiles (P10, P50, P90)       |
|                                                 +---------------------------+                     |
|                                                                             |                     |
|  [5. S2S Climate Teleconnections] (AO, NAO, ENSO, Siberian High)            v                     |
|  [6. GIS Vector Geospatial Layers] (DEM, Corridors, Land Cover, Buffers) -> | [SPATIO-TEMPORAL   |
|  [7. Socioeconomic & Public Surveys] (SPSS Hygiene + AMOS Causal SEM)     -> |  DECISION SUPPORT] |
+---------------------------------------------------------------------------------------------------+
```

---

## 🛰️ Detailed Breakdown of the 7 Data Modalities

---

### 1. Numerical Weather Prediction (NWP) Operational Forecasts

NWP models simulate future atmospheric states by integrating Navier-Stokes fluid mechanics and thermodynamic differential equations.

* **Primary Sources & Providers**:
  * **ECMWF-IFS (European Centre for Medium-Range Weather Forecasts)**: HRES (High Resolution 9km) and ENS (51-member ensemble, 18km).
  * **CMA-GFS (China Meteorological Administration Global Forecast System)**: Operational nationwide forecasting system (0.125° / ~12km resolution).
  * **NCEP GFS (National Centers for Environmental Prediction, USA)**: 0.25° global ensemble system.
* **Key Meteorological Variables**:
  | Variable Code | Parameter Name | Physical Unit | Description & Role |
  | :--- | :--- | :--- | :--- |
  | `u10`, `v10` | 10-meter Zonal & Meridional Wind | $\text{m/s}$ | Surface horizontal wind driving particle lifting and saltation. |
  | `MSLP` | Mean Sea Level Pressure | $\text{hPa}$ | Identifies cold front passages and Mongolian Cyclones. |
  | `T2m` | 2-meter Air Temperature | $\text{K} \text{ or } ^\circ\text{C}$ | Surface thermal gradient indicating sensible heat fluxes. |
  | `BLH` / `PBLH`| Planetary Boundary Layer Height | $\text{m}$ | Governs the vertical mixing depth of suspended dust aerosols. |
  | `Z500`, `Z700`| Geopotential Heights at 500 & 700 hPa | $\text{gpm}$ | Mid-tropospheric steering flows and cold air advection troughs. |
  | `shear` | Vertical Wind Shear ($u_{700} - u_{10}$)| $\text{m/s}$ | Quantifies atmospheric dynamic overturning and instability. |
* **Spatiotemporal Structure**:
  * **Horizontal Grid**: $0.125^\circ \times 0.125^\circ$ (regridded).
  * **Lead Time Horizon**: 0 to 360 Hours (Days 1 to 15) at 3-hour or 6-hour forecast intervals.
  * **File Formats**: GRIB2 (`.grib`, `.grb2`), NetCDF4 (`.nc`).
* **Role in AI System**:
  * **Line A (Machine Learning)**: Predictor features for statistical bias correction ($\hat{y}_{\text{res}} = y_{\text{true}} - y_{\text{NWP}}$).
  * **Line B (Deep Learning)**: 6 fluid dynamic channels ingested into the Coupled AI-GAMFS encoder grid ($B \times 6 \times 16 \times 16$).

---

### 2. Atmospheric Climate Reanalysis Datasets

Reanalysis merges historical physical model runs with quality-controlled past observations using 4D-Var data assimilation, creating a physically consistent, continuous multi-decadal historical record.

* **Primary Sources**:
  * **ERA5 (ECMWF 5th Generation Reanalysis)**: 1979–Present (hourly global reanalysis).
  * **MERRA-2 (NASA Modern-Era Retrospective analysis for Research and Applications)**: Specialized aerosol optical reanalysis.
  * **CRA-40 (China 40-Year Global Reanalysis)**: CMA national atmospheric benchmark.
* **Key Variables**:
  * Long-term multi-level atmospheric winds, temperatures, geopotential heights, and vertical velocity ($\omega$).
  * Volumetric soil water across 4 vertical soil layers:
    * Layer 1 ($0 - 7\ \text{cm}$): Immediate surface crust moisture.
    * Layer 2 ($7 - 28\ \text{cm}$): Root-zone moisture reservoir.
  * Surface sensible and latent heat fluxes.
* **Spatiotemporal Structure**:
  * **Resolution**: $0.25^\circ \times 0.25^\circ$ spatial grid, hourly temporal resolution spanning 45+ years.
  * **File Formats**: NetCDF4 (`.nc`), GRIB.
* **Role in AI System**:
  * **Model Pretraining**: Supervised training corpus for neural networks to learn universal fluid dynamics.
  * **Climatological Anomalies**: Subtracting 30-year climatological daily means ($\mu_{\text{clim}}$) to compute standardized anomaly indices:
    $$\Delta X(t) = \frac{X(t) - \mu_{\text{clim}}}{\sigma_{\text{clim}}}$$

---

### 3. Satellite Remote Sensing Earth Observation (EO) Data

Satellites provide continuous, wall-to-wall spatial coverage of surface characteristics, soil conditions, and airborne particulate plumes.

* **Primary Platforms & Sensors**:
  * **NASA Terra & Aqua (MODIS sensor)**: Daily global overpasses.
  * **FengYun FY-4A & FY-4B (AGRI - Advanced Geosynchronous Radiation Imager)**: China's geostationary meteorological satellites positioned at $104.7^\circ\text{E}$ and $105^\circ\text{E}$.
  * **ESA Sentinel-2 & NASA/USGS Landsat-8/9**: High-resolution multispectral imaging.
  * **SMAP (Soil Moisture Active Passive)**: Dedicated L-band microwave radiometer.
* **Key Environmental Variables**:
  | Variable | Full Name | Sensor / Spectral Bands | Role in Dust Storm Physics |
  | :--- | :--- | :--- | :--- |
  | **AOD (550nm)** | Aerosol Optical Depth | MODIS (MCD19A2), FY-4B | Measures column aerosol extinction; tracks real-time plume advection. |
  | **NDVI** | Normalized Difference Vegetation Index | Red & Near-Infrared (NIR) | Quantifies vegetation greenness and surface soil erosion resistance. |
  | **FVC** | Fractional Vegetation Cover | Derived from NDVI | Modulates aerodynamic roughness length ($z_0$). |
  | **SM** | Surface Soil Moisture | SMAP / FY-4 microwave | Critical threshold factor: dry soil drastically lowers saltation threshold $u_{*t}$. |
  | **LST** | Land Surface Temperature | Thermal Infrared (TIR) | Drives sensible heat convection and vertical thermals. |
  | **SCA** | Snow Cover Area | Normalized Difference Snow Index (NDSI) | Snow blanket completely suppresses sand dust emissions. |
  | **LULC / Sand Mask**| Land Use & Desert Boundaries | Landsat / Sentinel-2 | Delineates primary erodible desert source zones. |
* **Spatiotemporal Structure**:
  * **Resolution**: 250m to 1km (polar orbiters); 10-minute update frequency at 2km–4km (geostationary FY-4B).
  * **File Formats**: HDF5 (`.h5`), Cloud-Optimized GeoTIFF (`.tif`), NetCDF4 (`.nc`).
* **Role in AI System**:
  * **Line B Input**: 3 satellite vision channels ($B \times 3 \times 32 \times 32$) fused via cross-attention.
  * **PINN Physics Constraint**: Enforces soil moisture thresholding on aerodynamic friction velocity ($u_{*t}(w) = u_{*t0} \cdot \sqrt{1 + 1.21(w - w')^{0.68}}$).

---

### 4. Surface Ground-Based In-Situ Observations

Ground stations provide point-wise measurements with the highest temporal fidelity and zero atmospheric retrieval bias.

* **Primary Networks**:
  * **CMA National Meteorological Station Network**: 2,400+ national reference and standard surface meteorological stations across China.
  * **Primary Dust Corridor Sub-Network (14 Key Nodes)**: Dunhuang, Minqin, Zhangye, Wuwei, Jiuquan, Lanzhou, Hohhot, Baotou, Yinchuan, Taiyuan, Beijing, Shijiazhuang, Xi'an, Chengdu.
  * **CNEMC (China National Environmental Monitoring Centre)**: 1,800+ national urban ambient air quality monitoring stations.
* **Key Observational Variables**:
  * **Particulate Concentrations**: Hourly $PM_{10}$ and $PM_{2.5}$ mass concentrations ($\mu\text{g/m}^3$) via $\beta$-attenuation or TEOM (Tapered Element Oscillating Microbalance).
  * **Horizontal Visibility**: Atmospheric optical visibility (meters or kilometers) measured via forward-scatter visibility meters.
  * **Surface Wind Speeds**: 2-minute average, 10-minute average, and peak instantaneous gust speed ($u_{\text{gust}}$) at 10m height.
  * **Aerodynamic Friction Velocity ($u_*$)**: Estimated from boundary-layer sonic anemometers or calculated via the logarithmic wind profile:
    $$u_* = \frac{\kappa \cdot u(z)}{\ln(z / z_0)}$$
  * **Present Weather Phenomenon Code (WMO Code Table 4677 / WW Code)**:
    * `WW = 06`: Suspended Dust (浮尘 - fine particles floating in calm air, visibility $< 10\ \text{km}$).
    * `WW = 07`: Blowing Sand (扬沙 - local sand raised by wind, visibility $1 - 10\ \text{km}$).
    * `WW = 08`: Sand and Dust Storm (沙尘暴 - strong wind, visibility $< 1\ \text{km}$).
    * `WW = 09`: Severe Sand and Dust Storm (强沙尘暴 - gale force wind, visibility $< 500\ \text{m}$).
* **Spatiotemporal Structure**:
  * **Temporal Sampling**: Hourly routine reports; 5-minute or 10-minute real-time telemetry during active storm warnings.
  * **File Formats**: Relational Database Tables, CSV, JSON, NetCDF.
* **Role in AI System**:
  * **Ground Truth Target ($y_{\text{true}}$)**: Training labels for regression heads and hazard classification loss.
  * **Benchmark Evaluation**: Truth data for computing RMSE, MAE, Threat Score (TS), POD, FAR, and PICP interval coverage.

---

### 5. Sub-Seasonal to Seasonal (S2S) Climate Teleconnection Indices

Extended-range forecasting (beyond Day 7 up to Day 30) depends heavily on slowly evolving planetary wave patterns, ocean temperatures, and stratospheric polar dynamics.

* **Primary Sources**:
  * **NOAA Climate Prediction Center (CPC)**.
  * **Beijing Climate Center (BCC / CMA)**.
* **Key Teleconnection Climate Indices**:
  | Index Name | Full Parameter | Physical Mechanism in Sand Dust Storms |
  | :--- | :--- | :--- |
  | **AO** | Arctic Oscillation Index | Negative AO phase weakens polar jet, allowing arctic cold surges to plunge southward into desert basins. |
  | **NAO** | North Atlantic Oscillation | Modulates downstream downstream Eurasian teleconnection wavetrains. |
  | **Niño 3.4 (ENSO)**| El Niño-Southern Oscillation SST | Regulates Spring precipitation anomalies and drying trends over Northwest China. |
  | **Siberian High** | Siberian High Intensity Index | Strong central pressure ($> 1040\ \text{hPa}$) directly fuels synoptic cold front winds. |
  | **Polar Vortex** | Circumpolar Vortex Area & Strength | Vortex splitting or displacement drives high-impact sandstorm outbreaks in Northern China. |
* **Spatiotemporal Structure**:
  * **Frequency**: Daily and 5-day running mean index series.
  * **Role in AI System**: Static or low-frequency contextual embeddings appended to the deep learning encoder to modulate extended-range background probabilities.

---

### 6. Geographic Information System (GIS) Vector Geospatial Layers

GIS layers establish the static and dynamic spatial boundary conditions governing how dust particles emit, funnel, deposit, and interact with human settlements.

* **Primary Formats & Sources**:
  * **Digital Elevation Model (DEM)**: NASA SRTM 30m / ASTER GDEM 30m.
  * **Administrative Boundaries**: National Geomatics Center of China (NGCC) official 1:1,000,000 national database (CGCS2000).
  * **Transportation & Infrastructure Vectors**: National railway network (Lan-Xin High-Speed Railway), highway expressways (G6, G7), power grid lines.
  * **Land Cover**: ESA WorldCover 10m / Globeland30.
* **Key Geospatial Parameters Derived in GIS**:
  * **Topographic Slope & Aspect**: Derived from DEM; governs gravitational drainage flows and terrain blockage.
  * **Terrain Roughness ($z_0$)**: Influences surface aerodynamic friction.
  * **Corridor Distance**: Shortest Euclidean / Cost-distance along the Hexi transport funnel from desert source boundaries.
  * **Multi-Ring Proximity Buffers**: 5km, 15km, 30km, and 50km buffers around dust source corridors.
* **Role in Research System**:
  * **Feature Engineering**: Zonal extraction of satellite variables per county polygon.
  * **Spatial Econometrics**: Construction of spatial weights matrix ($W$) for Global Moran’s I and Geographically Weighted Regression (GWR).
  * **Thematic Cartography**: Producing 300+ DPI multi-layer publication figures.

---

### 7. Socio-Economic, Health & Empirical Survey Data

For comprehensive environmental impact and policy evaluation, qualitative and quantitative socioeconomic data are integrated using the SPSS and AMOS methodologies.

* **Primary Sources**:
  * **Field Surveys**: Household questionnaires administered across desert communities and downstream metropolitan districts ($N = 500$ to $10,000$).
  * **Public Health Records**: Municipal Center for Disease Control (CDC) daily hospital emergency admissions for asthma, COPD, and acute cardiovascular distress.
  * **Transportation Logs**: Civil Aviation Administration of China (CAAC) flight cancellation counts; railway delay hours.
  * **Economic Loss Statistics**: Ministry of Emergency Management official agricultural damage assessments (hectares of damaged plastic greenhouses, direct monetary loss in RMB).
* **Key Survey Construct Indicators (5-Point Likert Scales)**:
  * **Risk Perception ($RP_1 - RP_4$)**: Perceived likelihood and severity of dust storm impacts.
  * **Early Warning Trust ($WT_1 - WT_4$)**: Confidence in AI weather warning lead times and mobile push alerts.
  * **Adaptive Capacity ($AC_1 - AC_4$)**: Household financial reserves, air purifier ownership, and emergency food supplies.
  * **Protective Behavior ($PB_1 - PB_4$)**: Sealing windows, wearing N95 masks, cancelling travel.
* **Role in Research System**:
  * **SPSS**: Missing value analysis (Little’s MCAR), normality screening, Cronbach’s alpha reliability, and Exploratory Factor Analysis (EFA).
  * **AMOS**: Confirmatory Factor Analysis (CFA) construct validity (CR, AVE, Fornell-Larcker) and structural equation modeling (SEM) proving the mediation path from forecast lead time to reduced economic loss.

---

## ⚙️ Data Preprocessing & Harmonization Pipeline

Before heterogeneous datasets can be ingested into deep neural networks or statistical software, they pass through a standardized **5-Stage Harmonization Pipeline**:

```
+-----------------------------------------------------------------------------------------+
|                    5-STAGE SPATIOTEMPORAL HARMONIZATION SPECIFICATIONS                  |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  Stage 1: Spatial Harmonization (Regridding & Interpolation)                             |
|  - Continuous NWP & ERA5 grids: Reprojected and regridded to uniform 0.125° x 0.125°    |
|    using Bilinear Interpolation for smooth fields and Conservative Interpolation for    |
|    fluxes (mass conservation).                                                          |
|                                                                                         |
|  Stage 2: Temporal Synchronization                                                      |
|  - All observations converted to standardized Coordinated Universal Time (UTC).         |
|  - Synchronized to 00:00 UTC and 12:00 UTC major meteorological forecast cycles.        |
|                                                                                         |
|  Stage 3: Spatial Imputation of Missing Observations                                    |
|  - Ground sensor gaps (< 3 consecutive hours): Cubic spline interpolation.              |
|  - Sensor spatial gaps: Geostatistical Ordinary Kriging using fitted semivariograms.    |
|                                                                                         |
|  Stage 4: Normalization & Numerical Scaling                                             |
|  - Unbounded atmospheric fields (winds, geopotential heights): Z-score standardized:    |
|      Z = (X - μ) / σ                                                                    |
|  - Non-negative physical concentrations (PM10, AOD): Log-transformed & MinMax scaled:  |
|      X_norm = log(X + 1) / log(X_max + 1)                                               |
|                                                                                         |
|  Stage 5: High-Density Multimodal Tensor Ingestion Packaging                            |
|  - Ingestion Tensors:                                                                   |
|    • NWP Dynamic Tensor:      [Batch, 6 Channels, 16 Lat, 16 Lon]                       |
|    • Satellite Vision Tensor: [Batch, 3 Channels, 32 Lat, 32 Lon]                       |
|    • Corridor Sequence Tensor:[Batch, 24 Hours, 14 Stations, 12 Features]               |
+-----------------------------------------------------------------------------------------+
```

---

## 📊 Master Data Modality Summary Matrix

| Data Modality | Spatial Resolution | Temporal Frequency | Common File Format | Primary Provider | Role in AI & Research Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NWP Model Outputs** | $0.125^\circ - 0.25^\circ$ (9–25 km) | 3h to 6h steps (Days 1–15) | GRIB2, NetCDF4 | ECMWF, CMA, NCEP | Atmospheric background; baseline for Line A bias correction & Line B vision encoder. |
| **Climate Reanalysis** | $0.25^\circ \times 0.25^\circ$ (~31 km) | Hourly (1979–Present) | NetCDF4 (`.nc`) | ECMWF (ERA5), NASA | Model pretraining; 40-year climatological baselines and anomaly index calculation. |
| **Satellite Remote Sensing**| 250m–1km (Polar), 2–4km (Geostationary)| 10-min (FY-4), Daily (MODIS) | HDF5, GeoTIFF | NASA, CMA, ESA | Surface conditions (NDVI, soil moisture) and 2D dust plume advection tracking. |
| **Ground In-Situ Stations** | Point coordinates (2,400+ nodes) | Hourly / 10-minute | Relational DB, CSV | CMA NMIC, CNEMC | Ground truth training targets ($y_{\text{true}}$); verification metrics (RMSE, Threat Score). |
| **S2S Climate Indices** | Global / Hemispheric index series | Daily / 5-day running | CSV, Text Table | NOAA CPC, BCC CMA | Extended-range 10–30 day planetary wave background conditioning. |
| **GIS Geospatial Layers** | Vector polygons & 30m DEM raster | Static / Annual updates | Shapefile, GeoPackage, TIFF| NGCC, USGS, ESA | Spatial feature extraction, buffer zones, spatial weights matrix ($W$), and GWR maps. |
| **Socioeconomic Surveys** | Household / Hospital / County units | Event-based / Annual | `.sav` (SPSS), Excel | Field surveys, CDC, CAAC | SPSS data hygiene, normality checks, and AMOS structural equation causal modeling. |

---

## 💻 Data Acquisition APIs & Download Automation

To automate dataset acquisition, the platform utilizes standard scientific Python interfaces:

### 1. ECMWF Climate Data Store API (`cdsapi`)
```python
import cdsapi

c = cdsapi.Client()
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind',
            '2m_temperature', 'boundary_layer_height',
            'mean_sea_level_pressure', 'volumetric_soil_water_layer_1'
        ],
        'year': '2025',
        'month': ['03', '04', '05'],
        'day': [f"{d:02d}" for d in range(1, 32)],
        'time': [f"{h:02d}:00" for h in range(0, 24, 3)],
        'area': [45, 75, 30, 120], # North China study area [N, W, S, E]
        'format': 'netcdf'
    },
    'era5_dust_spring_2025.nc'
)
```

### 2. NASA Earthdata Search (MODIS AOD & SMAP Soil Moisture)
```python
import earthaccess

auth = earthaccess.login(strategy="environment")
results = earthaccess.search_data(
    short_name="MCD19A2",
    bounding_box=(75.0, 30.0, 120.0, 45.0),
    temporal=("2025-03-01", "2025-05-31")
)
files = earthaccess.download(results, "./data/satellite/modis_aod/")
```

---

*Related Documentation:*
* **Master Technical README:** [`README.md`](file:///c:/Users/hp/Desktop/China_project/README.md)
* **Plain-English README Guide:** [`README_EXPLAINED.md`](file:///c:/Users/hp/Desktop/China_project/README_EXPLAINED.md)
* **Operational Crisis Decision Playbook:** [`Planning/CRISIS_STORY_AND_DECISION_MAKING.md`](file:///c:/Users/hp/Desktop/China_project/Planning/CRISIS_STORY_AND_DECISION_MAKING.md)
* **SPSS Research Roadmap:** [`Planning/SPSS_ROADMAP.md`](file:///c:/Users/hp/Desktop/China_project/Planning/SPSS_ROADMAP.md)
* **AMOS SEM Roadmap:** [`Planning/AMOS_ROADMAP.md`](file:///c:/Users/hp/Desktop/China_project/Planning/AMOS_ROADMAP.md)
* **GIS Spatial Science Roadmap:** [`Planning/GIS_ROADMAP.md`](file:///c:/Users/hp/Desktop/China_project/Planning/GIS_ROADMAP.md)
