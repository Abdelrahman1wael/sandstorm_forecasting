# 📥 Phase 2 • Subfolder 1: Ingestion & Quality Control Pipeline
### *Automated Bulk Downloader Daemons, Checksum Validation & Telemetry Sanitization*
**Phase Horizon:** January 2026 – April 2026 (Month 5 – Month 8)  
**Parent Phase:** Phase 2 (Data System Construction)

---

## 🎯 1. Operational Goal & Ingestion Daemon Architecture

Phase 2.1 constructs the automated data ingestion engines that collect historical data (2018–2025) and establish scheduled polling daemons for real-time operations:

```
[Copernicus CDS API]    [NASA Earthdata]    [CMA Satellite FTP]    [MEE Sensor Feeds]
         │                     │                    │                      │
         └─────────────────────┼────────────────────┼──────────────────────┘
                               ▼
            [Automated Downloader Worker Pool (Python)]
                               │
                               ▼
                 [SHA-256 Checksum Validation]
                               │
                               ▼
        [Stage 1 Quality Control: Zero-Variance Flatline & Despiking]
                               │
                               ▼
           [Raw Stage Cache: Parquet / NetCDF4 Archives]
```

---

## ⚙️ 2. Core Operational Modules

1. **`cds_downloader.py`:** Fetches 6-hourly ERA5 pressure-level and single-level fields for East Asia ($70^\circ\text{E} - 135^\circ\text{E}, 25^\circ\text{N} - 55^\circ\text{N}$).
2. **`modis_downloader.py`:** Queries NASA CMR search API for daily MOD04_L2 and MYD04_L2 granules over China.
3. **`sensor_qc_sanitizer.py`:** Applies the rolling Median Absolute Deviation (MAD) despiking filter ($M_i > 4.5$) and 12-hour flatline detector ($\sigma_{12\text{h}} < 0.05$) to ground station particulate streams.

---

## 📋 3. Phase 2.1 Deliverables
* Automated cron scripts for daily 00:00 and 12:00 UTC ingestion.
* Clean, decontaminated ground telemetry records stored in partitioned Apache Parquet files.
