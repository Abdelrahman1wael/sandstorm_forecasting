# Clean Hourly 5-Notebook Pipeline Report (Train 70% / Val 15% / Test 15% + 5-Fold CV)

> [!NOTE]
> All results below were generated end-to-end with zero new external data added, using [riyadh_line_a_tabular_features.csv](file:///c:/Users/hp/Desktop/sandstorm_forecasting/06_Data/riyadh_line_a_tabular_features.csv) (`87,456` hourly rows) and [line_b_final_dataset.npz](file:///c:/Users/hp/Desktop/sandstorm_forecasting/06_Data/line_b_final_dataset.npz) via [build_and_run_clean_hourly_notebooks.py](file:///c:/Users/hp/Desktop/sandstorm_forecasting/08_Scripts/05_evaluation_and_plotting/build_and_run_clean_hourly_notebooks.py).

---

## 1. The 5 Executed 50-Cell Notebooks

| # | Notebook | Cells | Role | Key Output Artifact |
|---|---|---|---|---|
| 0 | [00_data_representation_and_distribution_riyadh.ipynb](file:///c:/Users/hp/Desktop/sandstorm_forecasting/04_Notebooks/00_data_representation_and_distribution_riyadh.ipynb) | 50 (25 MD + 25 Code) | Hourly 4-modality representation, `line_b_final_dataset.npz` inspection, KAPSARC sensor audit, regime-shift diagnostics | — |
| 1 | [01_feature_engineering_and_impact.ipynb](file:///c:/Users/hp/Desktop/sandstorm_forecasting/04_Notebooks/01_feature_engineering_and_impact.ipynb) | 50 (25 MD + 25 Code) | **All data cleaning & issue fixes**, causal feature engineering, train-only Yeo-Johnson & MI/Ridge impact | [riyadh_hourly_clean_tvt.csv](file:///c:/Users/hp/Desktop/sandstorm_forecasting/06_Data/riyadh_hourly_clean_tvt.csv) |
| 2 | [02_line_a_tabular_and_meta_models_riyadh.ipynb](file:///c:/Users/hp/Desktop/sandstorm_forecasting/04_Notebooks/02_line_a_tabular_and_meta_models_riyadh.ipynb) | 50 (25 MD + 25 Code) | Line A (5-Fold CV + Train/Val/Test) across `24h, 72h, 168h, 216h, 360h` forward averages | [nb02_line_a_classification_hourly.csv](file:///c:/Users/hp/Desktop/sandstorm_forecasting/06_Data/results/nb02_line_a_classification_hourly.csv) |
| 3 | [03_line_b_pytorch_real_layers.ipynb](file:///c:/Users/hp/Desktop/sandstorm_forecasting/04_Notebooks/03_line_b_pytorch_real_layers.ipynb) | 50 (25 MD + 25 Code) | Line B real PyTorch (`LSTM`, `Transformer`, `PINN`, `ST-GNN`) + `MultiModalNPZNet` on `line_b_final_dataset.npz` | [nb03_line_b_classification_hourly.csv](file:///c:/Users/hp/Desktop/sandstorm_forecasting/06_Data/results/nb03_line_b_classification_hourly.csv) |
| 4 | [04_explainable_ai_xai_riyadh.ipynb](file:///c:/Users/hp/Desktop/sandstorm_forecasting/04_Notebooks/04_explainable_ai_xai_riyadh.ipynb) | 50 (25 MD + 25 Code) | Permutation Importance, `shap.TreeExplainer`, PDP/ICE, Surrogate Rules, PyTorch LSTM Saliency, Spatial Graph | [nb04_xai_clean_hourly_importance.csv](file:///c:/Users/hp/Desktop/sandstorm_forecasting/06_Data/results/xai/nb04_xai_clean_hourly_importance.csv) |

---

## 2. Data Issues Identified & Fixed in Notebook 01

1. **`mslp` (`100%` missing) & constant GIS/metadata columns:** Dropped `mslp` and `7` constant columns (`lon`, `lat`, `elevation_m`, `sat_uv_index`, `gis_elevation_m`, `gis_slope_deg`, `gis_roughness_z0_m`), relying on `era5_surface_pressure` (`0%` missing).
2. **`wxcodes` (`92.27%` blank clear-sky):** Encoded into `has_wxcode` and `is_severe_dust_wx`, and combined with physical visibility into an objective target `clean_dust_event = (is_dust_event == 1) | (visibility_km < 5.0)`.
3. **10 km METAR visibility cap / `53.7 µg/m³` floor (`78.1%` capped):** Replaced flat `53.7` values on clear-sky hours (`visibility_km >= 9.9 km`) with a continuous wind/BLH-adjusted physical background (`pm10_clean_ugm3`: `10th=58.7`, `25th=64.91`, `50th=68.0`, `90th=72.7`).
4. **`2023–2024` covariate drift (`sat_retrieved_pm10` jump to `411.5` in `2024`):** Replaced raw `sat_retrieved_pm10`, `nwp_cams_pm10`, and `sat_aod_550nm` with causal 180-day (`4,320h`) rolling z-scores (Test Z-shift reduced to `+0.306`, `+0.306`, `-0.044`).
5. **Final clean hourly dataset:** [riyadh_hourly_clean_tvt.csv](file:///c:/Users/hp/Desktop/sandstorm_forecasting/06_Data/riyadh_hourly_clean_tvt.csv) (`86,928` hourly rows, `115` causal features, `10` forward-average targets).

---

## 3. Split & Evaluation Protocol
- **Train (`70%`):** `2015–2021` (with internal **5-Fold Rolling-Origin Time-Series CV** using `360h` purge gaps).
- **Purge Gap 1:** `360` hours (`15` days).
- **Validation (`15%`):** `2022–2023` (Platt calibration, early stopping, threshold tuning).
- **Purge Gap 2:** `360` hours (`15` days).
- **Held-Out Test (`15%`):** `2023–2024` (3 seeds `[42, 123, 456]`, 6-hour synoptic stride).
- **Horizons:** `24h` (`1d`), `72h` (`3d`), `168h` (`7d`), `216h` (`9d`), `360h` (`15d`) forward averages.

---

## 4. Results Summary

### 4A. Line A — 5-Fold Rolling CV Inside 70% Train (`nb02_line_a_5fold_cv_hourly.csv`)
| Horizon | Best Model | CV ROC-AUC | CV PR-AUC |
|---|---|---|---|
| `24h` (1d) | `XGBoost` | `0.8619` | `0.7028` |
| `72h` (3d) | `ExtraTrees` | `0.8097` | `0.7728` |
| `168h` (7d) | `ExtraTrees` | `0.7992` | `0.8701` |
| `216h` (9d) | `ExtraTrees` | `0.8043` | `0.8956` |
| `360h` (15d) | `ExtraTrees` | `0.8447` | `0.9550` |

### 4B. Held-Out Test Classification (`15%` Test Split — Best Model per Horizon)
| Horizon | Best Line A Model | Val ROC | Test ROC | Test PR | BSS | Lift@10% | Best Line B PyTorch | Line B Test ROC | Line B BSS |
|---|---|---|---|---|---|---|---|---|---|
| `24h` (1d) | `RandomForest_Cal` | `0.8368` | **`0.8090`** | `0.3143` | `+0.3218` | `4.28×` | `LineB_PINN` | `0.7939` | `+0.2159` |
| `72h` (3d) | `RandomForest_Cal` | `0.7590` | **`0.7167`** | `0.3838` | `+0.2724` | `2.67×` | `LineB_Transformer` | `0.7158` | `+0.2571` |
| `168h` (7d) | `RandomForest_Cal` | `0.6893` | **`0.7031`** | `0.5657` | `+0.1763` | `2.03×` | `LineB_PINN` | `0.6820` | `+0.2395` |
| `216h` (9d) | `XGBoost_Cal` | `0.6777` | **`0.7156`** | `0.6522` | `+0.0301` | `1.77×` | `LineB_Transformer` | `0.7065` | `+0.2467` |
| `360h` (15d) | `XGBoost_Cal` | `0.7224` | **`0.7655`** | `0.8311` | `+0.1313` | `1.67×` | `LineB_Transformer` | `0.6817` | `+0.1603` |

### 4C. Held-Out Test Continuous Clean-PM10 Regression (`RMSE` in `µg/m³`)
> [!WARNING]
> Because `2023–2024` Test has much lower mean PM10 than `2015–2021` Train, continuous regression models overpredict the Test mean level (`R² < 0`). **Line B PyTorch** substantially outperforms Line A trees/Ridge on RMSE across all 5 horizons, and `LineB_LSTM` (`14.13`) beats `Trivial_Median` (`15.45`) at `360h`.

| Horizon | `Trivial_Median` RMSE | Best Line A RMSE (Model) | Best Line B PyTorch RMSE (Model) |
|---|---|---|---|
| `24h` (1d) | **`20.86`** | `26.34` (`ExtraTrees`) | `21.55` (`LineB_STGNN`) |
| `72h` (3d) | **`13.46`** | `27.63` (`ExtraTrees`) | `15.58` (`LineB_STGNN`) |
| `168h` (7d) | **`11.80`** | `29.72` (`Ridge_log1p`) | `14.45` (`LineB_LSTM`) |
| `216h` (9d) | **`12.46`** | `27.68` (`Ridge_log1p`) | `14.86` (`LineB_STGNN`) |
| `360h` (15d) | `15.45` | `30.25` (`Ridge_log1p`) | **`14.13`** (`LineB_LSTM`) |

- **`MultiModalNPZNet` on [line_b_final_dataset.npz](file:///c:/Users/hp/Desktop/sandstorm_forecasting/06_Data/line_b_final_dataset.npz) (`70/15/15`):** `Test RMSE = 369.30`, `R² = -0.2688` (small `400`-sample tensor benchmark).

---

## 5. Top XAI Drivers (`168h` / 7-Day Test Set, [nb04_xai_clean_hourly_importance.csv](file:///c:/Users/hp/Desktop/sandstorm_forecasting/06_Data/results/xai/nb04_xai_clean_hourly_importance.csv))
1. `sin_doy` — `Mean |SHAP| = 0.71245`, `XGB_Gain = 0.06113`, `ET_Perm_ROC = 0.03060`
2. `dust_rate_4320h` — `Mean |SHAP| = 0.52050`
3. `hours_since_dust` — `Mean |SHAP| = 0.24132`
4. `dust_rate_720h` — `Mean |SHAP| = 0.17698`
5. `era5_soil_moisture_7_to_28cm` — `Mean |SHAP| = 0.12351`

