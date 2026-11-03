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

## 6. Live Dataset Acquisition Status (Riyadh & Connected Deserts)

| Dataset Modality | Target Domain / Period | Status | Local Disk Path | Notes |
| :--- | :--- | :---: | :--- | :--- |
| **Ground Weather Stations** | 2020–2024 (216,174 records across 6 stations) | ✅ **100% Downloaded** | [`data/raw/ground/riyadh_and_connected_deserts_ground_master.csv`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/ground/riyadh_and_connected_deserts_ground_master.csv) | Riyadh KKIA (`OERK`), Riyadh Air Base (`OERY`), Al-Kharj (`OEPS`), Ad-Duwadimi (`OEDM`), Wadi Al-Dawasir (`OEWD`), Gassim (`OEGS`). |
| **ERA5 Atmospheric Reanalysis** | 2020–2024 (43,848 h × 6 domains) | ✅ **100% Downloaded** | [`data/raw/era5/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/era5/) | ECMWF ERA5 reanalysis time-series for Riyadh Metropolitan, Al-Thumamah Dunes, Ad-Dahna Desert, Nafud al-Thuwairat, Tuwayq Escarpment, and Rub' al-Khali. |
| **Satellite & AERONET** | 2020–2024 (AOD, Dust Mass, Solar Flux) | ✅ **100% Downloaded** | [`data/raw/satellite/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/satellite/) | Satellite AOD & dust column across all 5 deserts + NASA AERONET ground-truth optical depth for Solar Village ([`aeronet_solar_village_riyadh_aod.csv`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/satellite/aeronet_solar_village_riyadh_aod.csv)). |
| **GIS DEM & Desert Geometry** | High-Res Topography & Spatial Polygons | ✅ **100% Downloaded** | [`data/raw/gis/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/gis/) | Connected Deserts GeoJSON (`riyadh_connected_deserts_geometry.geojson`), physics metadata, and DEM grid (`connected_deserts_dem_elevation_grid.csv`). |
| **NWP Operational Forecasts** | 5-day CAMS & ECMWF IFS Forecasts | ✅ **100% Downloaded** | [`data/raw/nwp/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/nwp/) | Point forecasts across all 5 desert corridors ([`cams_forecast_connected_deserts_and_riyadh.csv`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/nwp/cams_forecast_connected_deserts_and_riyadh.csv)) + regional CAMS grid. |



