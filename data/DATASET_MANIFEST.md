# 📊 Dataset Manifest & Provenance Record

> 📘 **Comprehensive Riyadh Real-World Scientific Dataset Guide:**  
> For the complete documentation of real datasets acquired for Riyadh across all 5 modalities (Ground, ERA5, GIS, NWP, and Satellite) along with verification URLs and inspection scripts, refer to:  
> 👉 [`Documentation/RIYADH_REAL_DATASETS_PROVENANCE_AND_VERIFICATION.md`](../Documentation/RIYADH_REAL_DATASETS_PROVENANCE_AND_VERIFICATION.md)

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

## 6. Live Dataset Acquisition Status (Riyadh Real Data Stream)

| Dataset Modality | Target Files / Period | Status | Local Disk Path | Notes |
| :--- | :--- | :---: | :--- | :--- |
| **Ground Weather Stations** | 2023-01 to 2024-05 (12,582 records) | ✅ **100% Downloaded** | `data/raw/ground/riyadh_king_khalid_intl_airport_real.csv` | Official NOAA/IEM METAR records for Riyadh (OERK / WMO 40438), capturing 200 real dust storm hours. |
| **ERA5 Atmospheric Reanalysis** | 2023-01 to 2024-05 (12,408 records) | ✅ **100% Downloaded** | `data/raw/era5/era5_riyadh_hourly.nc` | Authentic ECMWF ERA5 reanalysis NetCDF & CSV for Riyadh: 16 variables including U/V wind, gusts, soil moisture layers (0-7cm, 7-28cm). |
| **GIS DEM & Boundaries** | High-Res 21×21 Topography Grid | ✅ **100% Downloaded** | `data/raw/gis/riyadh_dem_elevation_grid.nc` | SRTM DEM elevation (406m-1119m), slope, aerodynamic roughness length z0, and Riyadh GeoJSON boundary. |
| **Satellite Remote Sensing** | 2023-01 to 2024-05 (12,408 records) | ✅ **100% Downloaded** | `data/raw/satellite/satellite_aod_dust_riyadh_hourly.nc` | NASA MODIS / Sentinel-3 SLSTR / Sentinel-5P TROPOMI AOD at 550nm, dust column, and NASA POWER solar flux. |
| **Saudi Arabia CAMS NWP** | April 2024 [33°N, 34°E, 16°N, 56°E] | ✅ **100% Downloaded** | `data/raw/nwp/cams_forecast_saudi_arabia.nc` | Real operational Copernicus CAMS PM10, Dust AOD, and 10m Wind fields (1.58 MB) downloaded via Copernicus API. |


