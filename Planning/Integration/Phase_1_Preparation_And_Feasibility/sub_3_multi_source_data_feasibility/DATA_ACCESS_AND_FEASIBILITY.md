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
# ECMWF CDS API Configuration (~/.cdsapirc)
url: https://cds.climate.copernicus.eu/api/v2
key: UID:API-KEY-HERE

# NASA Earthdata Authentication (~/.netrc)
machine urs.earthdata.nasa.gov login YOUR_USERNAME password YOUR_PASSWORD
```

---

## 📋 3. Phase 1.3 Exit Criteria
1. At least 1 complete historical spring season (e.g., March–May 2021) downloaded across all 5 modalities to test integration throughput.
2. Verified automated unzipping, NetCDF header parsing, and spatial bounding box queries.
