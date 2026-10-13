# 🛠️ Operations & Utility Scripts Directory
### Sand & Dust Storm Forecasting Platform (DustML)

This directory contains modular utility scripts for operational data retrieval, quality inspection, automated notebook generation, and machine learning pipeline execution.

---

## 📂 Directory Layout

```text
scripts/
├── README.md                          # Documentation index of all operational utilities
│
├── data_acquisition/                 # 1. API downloaders & synthetic stand-in generators
│   ├── download_nwp_saudi_arabia.py  # Primary Copernicus ADS downloader for Saudi Arabia CAMS NWP
│   ├── download_cams_forecast.py     # Global CAMS atmospheric composition downloader
│   ├── download_tigge_forecast.py    # ECMWF TIGGE extended-range downloader
│   ├── generate_standin_nwp.py       # General testing synthetic NetCDF generator
│   └── generate_standin_nwp_saudi.py # Domain-calibrated Saudi Arabia testing generator
│
├── data_verification/                # 2. Quality inspection & data integrity checkers
│   ├── inspect_saudi_nwp.py          # NetCDF-4 metadata & GRIB parameter validator
│   ├── check_downloaded_data.py      # Multi-source dataset integrity & completeness checker
│   └── test_feature_pipeline.py      # Feature engineering calculation & Parquet export test
│
├── pipeline_runners/                  # 3. Operational Machine Learning execution
│   └── run_saudi_line_a_pipeline.py  # Master runner: Line A models (Logistic, RF, XGB) across H3, H7, H15
│
└── notebook_generators/              # 4. Automated reproducible Jupyter notebook builders
    ├── create_saudi_notebooks.py     # Builds Notebooks 01 (EDA) & 02 (Feature Engineering)
    ├── create_line_a_notebook.py     # Builds Notebook 03 (HistGradientBoosting & Pinball Loss)
    ├── create_notebook_04.py         # Builds Notebook 04 (Full 3-algorithm benchmark suite)
    └── create_exploration_notebook.py# Builds general exploratory analysis notebook
```

---

## 🚀 Execution Guide & CLI Examples

Always execute scripts using your Anaconda Python environment from the repository root:

### 1. Data Acquisition
Download real operational CAMS atmospheric composition forecasts for the Kingdom of Saudi Arabia:
```bash
python scripts/data_acquisition/download_nwp_saudi_arabia.py
```
*Destination:* `data/raw/nwp/cams_forecast_saudi_arabia.nc`

### 2. Data Verification
Inspect and validate the NetCDF internal headers, GRIB parameters, and physical value ranges:
```bash
python scripts/data_verification/inspect_saudi_nwp.py
```

Verify the feature engineering pipeline and test Parquet generation:
```bash
python scripts/data_verification/test_feature_pipeline.py
```

### 3. Pipeline Runners
Execute the complete Line A multi-algorithm machine learning benchmark:
```bash
python scripts/pipeline_runners/run_saudi_line_a_pipeline.py
```

### 4. Notebook Generators
Rebuild reproducible Jupyter notebooks:
```bash
# Generate Notebooks 01 and 02
python scripts/notebook_generators/create_saudi_notebooks.py

# Generate Notebook 03 (Line A Tree Ensemble & Quantiles)
python scripts/notebook_generators/create_line_a_notebook.py

# Generate Notebook 04 (Full 3-algorithm benchmark)
python scripts/notebook_generators/create_notebook_04.py
```
