# 📡 Phase 1 • Subfolder 3: Multi-Source Data Feasibility & API Access
### *Verifying Data Pipelines: ECMWF CDS, NASA Earthdata, CMA Portal & MEE Stations*
**Phase Horizon:** September 2025 – December 2025  
**Parent Phase:** Phase 1 (Preparation and Feasibility)

---

## 🎯 1. Operational Goal & Feasibility Verification

Phase 1.3 verifies that all necessary multi-source environmental datasets can be acquired continuously via programmatic APIs without bandwidth bottlenecks, subscription expirations, or format incompatibilities:

| Data Source | Provider | Access Protocol | Verification Status | Storage Format |
| :--- | :--- | :--- | :---: | :--- |
| **ERA5 / ECMWF IFS** | Copernicus CDS | Python `cdsapi` with API key | Verified ✅ | GRIB2 / NetCDF4 |
| **MODIS Aerosol (MOD04)**| NASA Earthdata | `earthaccess` with Bearer token | Verified ✅ | HDF4 |
| **FY-4A/B AGRI Imagery** | CMA Satellite Center | Fengyun Data Portal FTP / HTTP | Verified ✅ | HDF5 |
| **MEE Ground PM10/PM2.5**| China MEE Network | Hourly REST API / CSV dumps | Verified ✅ | UTF-8 CSV / Parquet |
| **SRTM 90m DEM** | USGS / CGIAR-CSI | GeoTIFF spatial tiles | Verified ✅ | Cloud-Optimized GeoTIFF |

---

## 🔑 2. Automated Credential Configuration

```bash
# ECMWF CDS API Configuration (~/.cdsapirc / C:\Users\<you>\.cdsapirc)
url: https://cds.climate.copernicus.eu/api
key: <your-personal-access-token>

# NASA Earthdata Authentication (~/.netrc)
machine urs.earthdata.nasa.gov login YOUR_USERNAME password YOUR_PASSWORD
```

> [!IMPORTANT]
> **Operational Horizon & Data Availability Constraints:**
> - **ECMWF CAMS Atmospheric Composition:** Aerosol and PM10 chemical transport forecasts are available out to **~120h (5 days)**.
> - **ECMWF IFS / TIGGE:** Purely meteorological forecasts (wind, surface pressure, temperature) extend out to **360h (15 days)**, but do *not* contain dust aerosol/PM10 concentrations.
> - **Line A Two-Tier Strategy:**
>   - *Days 3–5 (72h–120h):* Residual learning on numerical CAMS PM10: $\Delta y = y_{\text{obs}} - y_{\text{CAMS\_PM10}}$.
>   - *Days 6–15 (144h–360h):* Direct ML prediction of PM10 using forecasted meteorological variables (wind, gust, boundary layer height, soil moisture, surface pressure) as dynamical features.

---

## 📋 3. Phase 1.3 Exit Criteria
1. At least 1 complete historical spring season (e.g., March–May 2021) downloaded across all 5 modalities to test integration throughput.
2. Verified automated unzipping, NetCDF header parsing, and spatial bounding box queries.
