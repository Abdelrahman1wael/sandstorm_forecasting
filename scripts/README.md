# 🌪️ Riyadh Sand & Dust Storms (SDS) Forecasting — Operational Scripts

All executable pipeline scripts are organized strictly by their **chronological execution order** into structured stages, dedicated **100% to Riyadh Only** (Riyadh Airport SDSC station at $24.926^\circ\text{N}, 46.722^\circ\text{E}$ and its metropolitan grid $24.0^\circ\text{N}\text{--}25.5^\circ\text{N}, 46.0^\circ\text{E}\text{--}47.5^\circ\text{E}$). All external regional domains (such as Arabian Peninsula, Arabian Gulf, and Mesopotamian basins) have been completely removed.

---

## 🏛️ Directory Architecture & Execution Flow

```text
scripts/
├── riyadh_common.py                     # 00. Master common configuration, constants, optics formulas & credentials
│
├── 01_data_acquisition/                # STAGE 1: Multi-Modal Data Ingestion (Riyadh Only)
│   ├── download_cams.py                 # Download CAMS numerical dust forecasts (duaod550, 0-120h)
│   ├── download_era5.py                 # Download ERA5 reanalysis (pressure levels 850/700/500 + surface)
│   ├── download_modis_aod.py            # Download MODIS Deep Blue AOD (550nm) at Riyadh Airport
│   ├── submit_all_cams.py               # Batch parallel submitter for CAMS forecast windows
│   ├── submit_all_era5.py               # Batch parallel submitter for ERA5 reanalysis slices
│   ├── era5_bulk_download.py            # Multi-worker bulk download utility for ERA5
│   ├── era5_big_batch.py                # Large-batch ERA5 archive filler
│   ├── era5_optimized.py                # Optimized connection scheduler for CDS API
│   ├── era5_pl_quarterly.py             # Quarterly pressure level chunk downloader
│   └── era5_supplement.py              # Gap-filling and missing timestamp utility
│
├── 02_data_verification_qaqc/           # STAGE 2: Quality Assurance & Control (QA/QC)
│   ├── qaqc_aeronet.py                  # QA/QC on AERONET ground truth at Riyadh Airport
│   ├── qaqc_cams.py                     # QA/QC on CAMS numerical dust optical depth over Riyadh
│   ├── qaqc_era5.py                     # QA/QC on ERA5 atmospheric levels and surface drivers over Riyadh
│   ├── qaqc_cmip6.py                    # QA/QC on CMIP6 sub-seasonal climate models over Riyadh
│   └── qaqc_report.py                   # Master audit report validating all Riyadh datasets
│
├── 03_collocation_and_features/         # STAGE 3: Spatiotemporal Alignment & Feature Engineering
│   ├── merge_cams.py                    # Merges CAMS forecast windows into unified NetCDF
│   ├── collocate_cams_aeronet.py        # Collocates CAMS forecasts with AERONET at Riyadh (+/-1.5h)
│   ├── three_way_validation.py          # Independent 3-way validation: AERONET vs CAMS vs MODIS
│   └── build_meta_features.py           # Generates multimodal tabular matrix and optical PM proxies
│
├── 04_model_training_and_tuning/        # STAGE 4: Machine Learning & Deep Learning
│   ├── train_meta_model.py              # Trains RF, XGBoost, MLP with SMOTE & cost-sensitive weights
│   └── optimize_threshold.py            # Calibrates optimal F1 precision-recall decision threshold
│
├── 05_literature_rag/                   # STAGE 5: Domain Knowledge & Literature RAG
│   ├── scrape_papers.py                 # Harvester for Riyadh dust storm scientific literature
│   └── query_rag.py                     # Hybrid BM25 + dense embedding literature query agent for Riyadh
│
└── 06_utils/                            # STAGE 6: Operational Utilities
    └── usage_calc.py                    # Storage footprint, DCU hours, and API quota tracker
```

---

## ⚡ Execution Instructions

All scripts automatically import configuration and paths from [`scripts/riyadh_common.py`](riyadh_common.py).

### Run Stage 2 (QA/QC Verification):
```bash
python scripts/02_data_verification_qaqc/qaqc_aeronet.py
python scripts/02_data_verification_qaqc/qaqc_cams.py
python scripts/02_data_verification_qaqc/qaqc_era5.py
python scripts/02_data_verification_qaqc/qaqc_report.py
```

### Run Stage 3 (Collocation & Featurization):
```bash
python scripts/03_collocation_and_features/collocate_cams_aeronet.py
python scripts/03_collocation_and_features/build_meta_features.py
```

### Run Stage 4 (Model Training & Threshold Calibration):
```bash
python scripts/04_model_training_and_tuning/train_meta_model.py
python scripts/04_model_training_and_tuning/optimize_threshold.py
```
