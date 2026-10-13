# 📊 Dataset Manifest & Provenance Record

This document records all environmental and meteorological datasets utilized in the extended-range sandstorm forecasting project, their source URLs, access methods, variables, and licensing. This serves as the documentation standard for the thesis data chapter.

---

## 1. Observed Ground Air Quality Stations (Target Truth)
- **Source:** CNEMC (China National Environmental Monitoring Centre) / Quotsoft Archive
- **URL:** `https://quotsoft.net/air/`
- **File Pattern:** `https://quotsoft.net/air/data/china_sites_YYYYMMDD.csv`
- **Target Period:** March 1, 2021 – May 31, 2021 (92 daily files)
- **Timezone:** Beijing Time (UTC+8) -> *Must be shifted to UTC during preprocessing (`UTC = CST - 8h`)*
- **Key Target Variable:** `type == "PM10"` (hourly concentration in $\mu\text{g}/\text{m}^3$)
- **Domain Coverage:** National network (~1,600 stations), filtered for Northern China / Northwest dust corridors.
- **Local Path:** `data/raw/ground/`

---

## 2. Atmospheric & Land Surface Reanalysis (ERA5)
- **Source:** Copernicus Climate Data Store (CDS), ECMWF
- **Dataset:** `reanalysis-era5-single-levels`
- **API URL:** `https://cds.climate.copernicus.eu/api` (updated 2024+ CDS engine)
- **Spatial Domain:** $[55^\circ\text{N}, 70^\circ\text{E}, 25^\circ\text{N}, 135^\circ\text{E}]$ (East Asian Sandstorm Corridor)
- **Temporal Resolution:** 3-hourly intervals, March 1 – May 31, 2021
- **Variables:**
  1. `10m_u_component_of_wind` ($u_{10}$)
  2. `10m_v_component_of_wind` ($v_{10}$)
  3. `10m_wind_gust_since_previous_post_processing` ($u_{\text{gust}}$)
  4. `2m_temperature` ($T_{2\text{m}}$)
  5. `boundary_layer_height` (BLH)
  6. `surface_pressure` ($P_{\text{sfc}}$)
  7. `volumetric_soil_water_layer_1` ($SM_{\text{top}}$)
- **Local Path:** `data/raw/era5/`

---

## 3. Atmospheric Composition Forecasts (Days 3–5 / 72h–120h)
- **Source:** Copernicus Atmosphere Data Store (ADS), CAMS
- **Dataset:** `cams-global-atmospheric-composition-forecasts`
- **Variables:**
  - `particulate_matter_10um` (forecast PM10 concentration)
  - `dust_aerosol_optical_depth_550nm` (Dust AOD at 550nm)
  - 10m wind ($u, v$)
- **Operational Lead Times:** 72h to 120h (3h cadence)
- **Role in Line A:** Residual learning target $\Delta y = y_{\text{obs}} - y_{\text{CAMS\_PM10}}$
- **Local Path:** `data/raw/nwp/`

---

## 4. Extended-Range Meteorological Forecasts (Days 6–15 / 144h–360h)
- **Source:** ECMWF TIGGE Archive (`apps.ecmwf.int/datasets/data/tigge`)
- **Dataset:** ECMWF Operational Control Forecast
- **Variables:**
  - $10\text{m}$ Wind speed and direction
  - $2\text{m}$ Temperature
  - Surface pressure
- **Role in Line A:** Direct non-linear PM10 regression using forecast dynamics and boundary layer stability as predictors (since NWP outputs no chemical dust transport beyond 120h).
- **Local Path:** `data/raw/nwp/`

---

## 5. Digital Elevation Model (DEM) & Static Topography
- **Source:** CGIAR-CSI SRTM 90m / USGS Earth Explorer
- **Domain:** $70^\circ\text{E} - 135^\circ\text{E}$, $25^\circ\text{N} - 55^\circ\text{N}$
- **Variables:** Elevation ($H_{\text{dem}}$), Slope, Aspect, Roughness ($z_0$)
- **Local Path:** `data/raw/gis/`

---

## 6. Live Dataset Acquisition Status (Updated)

| Dataset Modality | Target Files / Period | Status | Local Disk Path | Notes |
| :--- | :--- | :---: | :--- | :--- |
| **Saudi Arabia CAMS NWP (Real)** | April 2024 [33°N, 34°E, 16°N, 56°E] | ✅ **100% Downloaded** (`cams_forecast_saudi_arabia.nc`, 1.58 MB) | `data/raw/nwp/cams_forecast_saudi_arabia.nc` | Real operational CAMS PM10, Dust AOD, and 10m Wind fields for Saudi Arabia (43×56 grid, 9 forecast lead steps, 6 cycles) downloaded via Copernicus API. Detailed authenticity proof: [Documentation/SAUDI_ARABIA_NWP_DATASET_PROVENANCE.md](../Documentation/SAUDI_ARABIA_NWP_DATASET_PROVENANCE.md). |
| **Ground Air Quality Stations** | China Network | ⏹️ **Stopped** (per user request) | `data/raw/ground/` | Halted to focus strictly on Saudi Arabia NWP. |
| **ERA5 Atmospheric Reanalysis** | Arabian Peninsula Domain | ⏳ Pending NWP completion | `data/raw/era5/` | API token configured in `Keys/API_Key/API.txt`. |
| **GIS DEM Elevation** | Topography grid across domain | ⏳ Pending download | `data/raw/gis/` | SRTM 90m domain raster. |


