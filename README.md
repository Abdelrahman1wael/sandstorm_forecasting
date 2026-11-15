# Machine Learning for Medium- to Long-Term Sand and Dust Storm Forecasting in Saudi Arabia, with Special Emphasis on Riyadh

**University of Science and Technology Beijing (USTB) — School of Energy and Environmental Engineering**  
**Degree:** Master's Degree in Environmental Engineering | **Author:** 语嫣 (Yuyan, Student ID: `202461024`) | **Supervisor:** Associate Professor Wen Wei (温维)  
**Stage:** Mid-Term Dissertation Prototype & Reproducible Research Repository (`2015–2024` Multi-Modal Hourly Benchmark)

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Study Domain, Dust Sources & Operational Playbook](#2-study-domain-dust-sources--operational-playbook)
3. [Complete Repository & Deliverables Structure](#3-complete-repository--deliverables-structure)
4. [Data Acquisition, QA/QC, Anti-Leakage & Split Protocol](#4-data-acquisition-qaqc-anti-leakage--split-protocol)
5. [115-Feature Causal Engineering Across Physical Modalities](#5-115-feature-causal-engineering-across-physical-modalities)
6. [Dual-Line Modeling Architecture & Hyperparameters](#6-dual-line-modeling-architecture--hyperparameters)
7. [Complete Empirical Results (CV, Classification, Regression)](#7-complete-empirical-results-cv-classification-regression)
8. [Explainable AI Suite (XAI-1 to XAI-6) & Physical Findings](#8-explainable-ai-suite-xai-1-to-xai-6--physical-findings)
9. [Notebook & Figure Catalog (`00` through `04`)](#9-notebook--figure-catalog-00-through-04)
10. [Scripts Index (`08_Scripts/`) & Reproduction Commands](#10-scripts-index-08_scripts--reproduction-commands)
11. [Software Environment & Verified Package Stack](#11-software-environment--verified-package-stack)
12. [Known Mid-Term Prototype Limitations & Stage-Two Roadmap](#12-known-mid-term-prototype-limitations--stage-two-roadmap)

---

## 1. Executive Summary

This repository implements a strictly causal, multi-modal forecasting and Explainable AI (XAI) framework for **1- to 15-day (`24–360 h`)** sand and dust storm (SDS) prediction across **Greater Riyadh, Saudi Arabia**.

- **Master Clean Hourly Dataset:** `86,928` aligned, leak-free hourly records (`06_Data/riyadh_hourly_clean_tvt.csv`, `9 Jan 2015 – 8 Dec 2024`, `115` causal features) derived from `87,456` raw hourly records (`2 Jan 2015 – 23 Dec 2024`), fusing **Ground METAR** surface telemetry (`OERK` / Riyadh), **ECMWF ERA5** boundary-layer & soil-moisture physics, **Detrended Satellite** retrievals, **CAMS NWP** aerosol fields, and **Calendar / Dust-Memory** descriptors.
- **Strict Chronological Split & Purge Gaps:** Partitioned into **70% Train** (`9 Jan 2015 – 18 Dec 2021`), **15% Validation** (`2 Jan 2022 – 14 Jun 2023`), and **15% Test** (`29 Jun 2023 – 8 Dec 2024`) with **`360 h` (15-day) purge gaps** between partitions. Models use **6-hourly samples (`10,142 / 2,114 / 2,114`)** across five horizons $H \in \{24, 72, 168, 216, 360\}\text{ h}$ and three random seeds $\{42, 123, 456\}$.
- **Headline Mid-Term Findings:**
  - **Binary Dust-Event Classification (Line A):** Calibrated tabular ensembles exceed monthly-climatology (`MonthClimo_Cal`) ROC-AUC at every horizon (`0.809 vs. 0.643` at `24 h`; `0.717 vs. 0.641` at `72 h`; `0.703 vs. 0.658` at `168 h`; `0.716 vs. 0.666` at `216 h`; `0.766 vs. 0.665` at `360 h`), achieving `4.28×` `Lift@Top10%` at `24 h` and strictly positive Brier Skill Scores (`BSS = 0.0301–0.3218`). Gains beyond 7 days (`168 h`) are small, consistent with largely seasonal predictability.
  - **PyTorch Sequence & Graph Prototypes (Line B):** `RealLSTMNet`, `RealTransformerNet`, `RealPINNNet`, and `RealSTGNNNet` achieve `0.6817–0.7939` classification ROC-AUC and positive `BSS` (`0.1603–0.2571`).
  - **Continuous $\text{PM}_{10}$ Regression (Honest Finding):** All models obtain **negative test $R^2$**, and the constant training-median baseline (`Trivial_Median`) achieves lower RMSE than the best Line B model at `24–216 h` (e.g., `11.8 vs. 14.5 μg/m³` at `168 h`), with Line B lower only at `360 h` (`14.1 vs. 15.5 μg/m³`). Continuous regression skill is therefore **not demonstrated** in this mid-term prototype.
  - **Explainable AI (`XAI-1` to `XAI-6`):** `Ground_METAR` (`~37.4%`), `Calendar_Diurnal` (`~32.2%`), and `ERA5_Physics` (`~23.5%`) supply over `93%` of total SHAP attribution at `168 h`, led by `sin_doy` (`0.71245`), `dust_rate_4320h` (`0.52050`), `hours_since_dust` (`0.24132`), and `dust_rate_720h` (`0.17698`), while PyTorch LSTM temporal saliency peaks at `Lag 0 h` (`0.0088`).

---

## 2. Study Domain, Dust Sources & Operational Playbook

- **Geographic Domain:** `16°N–33°N`, `34°E–56°E`; Greater Riyadh sits on the Najd plateau (`~614 m` elevation, `~1,913 km²` metropolitan area), centered on **King Khalid International Airport (`OERK`)**.
- **Dust Source Regimes:**
  1. **Local (`Ad Dahna`):** Crescent sand sea wrapping east and north of Riyadh.
  2. **Regional (`Rub' al Khali`):** Primary southern source; southerly winds transport dense mineral dust.
  3. **Remote (`An Nafud` & `Iraq`):** Spring cold fronts and northwesterly **Shamal** outbreaks push dust southward into central Saudi Arabia.
  4. **Micro-Environments:** `Wadi Hanifa` and `Tuwaiq` escarpment topography.
- **6-Node Spatial Graph Topology (Prototype):** Node 0 `KKIA`, Node 1 `Central Riyadh Station`, Node 2 `Riyadh Air Base`, Node 3 `Qassim`, Node 4 `Al Ahsa`, Node 5 `Wadi Ad-Dawasir`.
- **4-Tier Municipal Early-Warning Playbook:**
  - **Level 1 Green ($\text{PM}_{10} < 50\ \mu\text{g/m}^3$):** Routine NCEC ground monitoring.
  - **Level 2 Yellow ($50–150\ \mu\text{g/m}^3$):** Health advisories; PV solar farms schedule dry-brush cleaning.
  - **Level 3 Orange ($150–500\ \mu\text{g/m}^3$):** `72–120 h` advance notice; remote-learning contingency plans, road water sprayers, ER surge staffing.
  - **Level 4 Red ($\ge 500\ \mu\text{g/m}^3$):** GACA/KKIA aviation delay protocols, highway speed limits `< 60 km/h`, construction halt (gated by calibrated probabilities + local SHAP audit).

---

## 3. Complete Repository & Deliverables Structure

```text
sandstorm_forecasting/
├── README.md                                        # Complete project & technical reference (this file)
├── 01_Documentation/                                # USTB Master's Thesis manuscripts
│   └── USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v3.docx
├── 02_Presentation/                                 # Mid-term defense presentation (57 slides + speaker notes)
│   └── Riyadh_Sandstorm_Forecasting_Midterm (1).pptx
├── 03_Supervisor_Planning/                          # Supervisor response, provenance & taxonomy docs
├── 04_Notebooks/                                    # Executed Jupyter notebooks (00 through 04)
│   ├── 00_data_representation_and_distribution_riyadh.ipynb
│   ├── 01_feature_engineering_and_impact.ipynb
│   ├── 02_line_a_tabular_and_meta_models_riyadh.ipynb
│   ├── 03_line_b_pytorch_real_layers.ipynb
│   └── 04_explainable_ai_xai_riyadh.ipynb
├── 05_Models/                                       # Exported preprocessors, Line A & Line B checkpoints
│   ├── line_a/
│   │   ├── clean_hourly_preprocessor.joblib
│   │   ├── line_a_randomforest_cal_24h.joblib
│   │   ├── line_a_randomforest_cal_72h.joblib
│   │   ├── line_a_randomforest_cal_168h.joblib
│   │   ├── line_a_xgboost_cal_216h.joblib
│   │   └── line_a_xgboost_cal_360h.joblib
│   └── line_b/
│       ├── lineb_pinn_24h_cls.pt
│       ├── lineb_transformer_72h_cls.pt
│       ├── lineb_pinn_168h_cls.pt
│       ├── lineb_transformer_216h_cls.pt
│       ├── lineb_transformer_360h_cls.pt
│       ├── lineb_lstm_360h_reg.pt
│       └── multimodal_npz_net.pt
├── 06_Data/                                         # Master datasets & CSV evaluation tables
│   ├── riyadh_hourly_clean_tvt.csv                  # 86,928 hourly records x 115 causal features
│   ├── riyadh_line_a_tabular_features.csv           # 87,456 raw hourly records
│   └── results/
│       ├── nb01_clean_hourly_feature_impact.csv
│       ├── nb02_line_a_5fold_cv_hourly.csv
│       ├── nb02_line_a_classification_hourly.csv
│       ├── nb02_line_a_regression_hourly.csv
│       ├── nb03_line_b_classification_hourly.csv
│       ├── nb03_line_b_regression_hourly.csv
│       └── nb04_xai_clean_hourly_importance.csv
├── 07_Figures/                                      # High-resolution diagnostic, Line A/B & XAI figures
│   ├── nb00_fig01.png .. nb00_fig12.png
│   ├── nb01_fig01.png .. nb01_fig03.png
│   ├── nb02_fig01.png .. nb02_fig08.png
│   ├── nb03_fig01.png .. nb03_fig06.png
│   └── nb04_fig01.png .. nb04_fig07.png, nb04_fig09.png
└── 08_Scripts/                                      # Modular acquisition, QA/QC, training & thesis scripts
    ├── riyadh_common.py
    ├── 01_data_acquisition/                         # CAMS, ERA5, MODIS downloaders
    ├── 02_data_verification_qaqc/                   # QA/QC checks (ERA5, CAMS, AERONET, CMIP6)
    ├── 03_collocation_and_features/                 # Feature engineering, collocation & TVT splitting
    ├── 04_model_training_and_tuning/                # Line A & Line B training and honest audits
    ├── 05_evaluation_and_plotting/                  # Notebook runners, model exporter & docx/pptx builders
    └── tests_and_diagnostics/                       # Unit & pipeline diagnostics
```

---

## 4. Data Acquisition, QA/QC, Anti-Leakage & Split Protocol

### 4.1 Chronological Split & Target Definitions
- **Raw vs. Clean Hourly Window:** `87,456` raw hourly records (`2 Jan 2015 – 23 Dec 2024`) cleaned and aligned to **`86,928` leak-free hourly records** (`9 Jan 2015 – 8 Dec 2024`) in `06_Data/riyadh_hourly_clean_tvt.csv` (mean `pm10_clean_ugm3 = 106.12 μg/m³`, std `254.14 μg/m³`, median `68.00 μg/m³`, max `4,800.0 μg/m³`, skewness `11.79`).
- **Chronological Partitions (`360 h` / 15-day purge gaps between splits):**
  - **Train (70%):** `9 Jan 2015 – 18 Dec 2021` (`10,142` 6-hourly samples; `7.47%` raw hourly dust rate)
  - **Validation (15%):** `2 Jan 2022 – 14 Jun 2023` (`2,114` 6-hourly samples; `8.43%` raw hourly dust rate)
  - **Test (15%):** `29 Jun 2023 – 8 Dec 2024` (`2,114` 6-hourly samples; `0.94%` raw hourly dust rate)
- **Targets Across $H \in \{24, 72, 168, 216, 360\}\text{ h}$:**
  - **Classification Target:** *"Dust (`visibility < 5 km`) occurs at least once in the next $H$ hours"* (`168 h` test positive rate: `35.0%`).
  - **Regression Target:** *"Mean $\text{PM}_{10}$ proxy over the next $H$ hours"* (derived from visibility, with background estimated from ERA5 wind and boundary-layer height).

### 4.2 Four Anti-Leakage & Data-Quality Safeguards (`Notebook 01`)
1. **Missingness & Weather Encoding:** Dropped `100%`-missing `mslp` and encoded METAR present-weather strings into `has_wxcode` and `is_severe_dust_wx` (`SS/DS/SA`).
2. **De-Censoring `53.7 μg/m³` Floor:** Raw PM₁₀ proxy exhibited `79.01%` flat censoring at `53.7 μg/m³`; de-censored into continuous `pm10_clean_ugm3` using wind/BLH background estimation.
3. **Satellite & NWP Drift Removal:** Replaced drifting raw satellite/CAMS columns (`sat_dust_column_mass` Test Z-shift = `5.122`) with causal `4,320 h` (180-day) rolling Z-scores clipped to `[-5, 5]`, and purged all pre-existing `target_*` columns before recomputing clean future horizons.
4. **Train-Only Fitting & Cost-Sensitive Weighting (No SMOTE):** `SimpleImputer` (median) and `PowerTransformer` (Yeo-Johnson) are fitted strictly on the 70% training partition and frozen. Synthetic oversampling (`SMOTE`) is omitted to avoid temporal autocorrelation leakage; class imbalance is handled via `class_weight="balanced"` (Line A) and `pos_weight` inside `BCEWithLogitsLoss` (Line B).

---

## 5. 115-Feature Causal Engineering Across Physical Modalities

| Modality Group | Representative Verified Features | Physical / Operational Role |
| :--- | :--- | :--- |
| **`Ground_METAR`** | `pm10_calibrated_ugm3`, `pm10_clean_ugm3`, `vsby`, `has_wxcode`, `gust`, `hours_since_dust`, `dust_rate_720h`, `dust_rate_4320h`, `pm10_clean_ugm3_roll168h` | Real-time surface particulate/visibility state, gust-driven saltation, and 30–180 day dust-regime memory |
| **`ERA5_Physics`** | `era5_soil_moisture_0_to_7cm`, `era5_soil_moisture_7_to_28cm`, `phys_vpd_kpa_roll168h`, `era5_10m_v_component_of_wind`, `lag_era5_v10_1h` | Capillary soil-moisture cohesion, atmospheric desiccation (VPD), and boundary-layer wind dynamics |
| **`Calendar_Diurnal`** | `sin_doy`, `cos_doy`, diurnal hour harmonics | Spring–early-summer Shamal seasonal phase and afternoon convective mixing cycle |
| **`Satellite_Detrended` & `CAMS_NWP_Detrended`** | `sat_retrieved_pm10_detrended_z`, detrended CAMS aerosol channels | Short-range (`24 h`) optical/NWP anomalies clipped against multi-year sensor drift |

---

## 6. Dual-Line Modeling Architecture & Hyperparameters

### 6.1 Main Line A (`04_Notebooks/02_line_a_tabular_and_meta_models_riyadh.ipynb`)
- **Classifiers:** `LogReg_Bal_Cal` (`C=0.2`, `class_weight="balanced"`), `RandomForest_Cal` (`n_estimators=100`, `class_weight="balanced"`), `ExtraTrees_Cal` (`n_estimators=100`, `class_weight="balanced"`), `HistGB_Cal`, `XGBoost_Cal`, wrapped with validation-set Platt/isotonic probability calibration.
- **Regressors:** `Ridge_log1p` (regularized linear regression on $\ln(\text{PM}_{10}+1)$), `RandomForest`, `ExtraTrees`, `XGBoost`, benchmarked against `Trivial_Median` and `MonthClimo`.
- **Classification Baselines:** `Persistence_Cal` and `MonthClimo_Cal`.

### 6.2 Main Line B (`04_Notebooks/03_line_b_pytorch_real_layers.ipynb`)
All four PyTorch networks ingest 24-hour sequence tensors (`AdamW`, `lr=1.5e-3`, `weight_decay=1e-3`, `batch_size=128`; `BCEWithLogitsLoss(pos_weight)` for classification; `L1Loss` on $\ln(\text{PM}_{10}+1)$ for regression):
1. **`RealLSTMNet`:** Multi-layer LSTM with recurrent gating over the 24-hour lookback window.
2. **`RealTransformerNet`:** Temporal self-attention encoder across the 24-hour sequence.
3. **`RealPINNNet`:** Enforces a physical wind-monotonicity constraint directly in the loss objective:
   $$\mathcal{L}_{\text{PINN}} = \mathcal{L}_{\text{BCE}}(y, \hat{y}; \text{pos\_weight}) + 0.05 \cdot \operatorname{mean}\!\Big(\operatorname{ReLU}\big(f(x) - f(x + 0.5\,e_{\text{wind}})\big)\Big)$$
   where $e_{\text{wind}}$ shifts standardized ERA5 10 m wind speed at $t = 0$ by $+0.5\text{ SD}$, penalizing physically inconsistent drops in predicted dust probability under stronger winds.
4. **`RealSTGNNNet`:** Graph-structured GRU prototype embedding a 6-node graph via row-normalized adjacency $A_{\text{norm}} = A / \deg$, 8-d learnable node embeddings, and `Linear(in_dim + 8 -> 32)` propagation. *Prototype scope:* identical single-station feature vectors are broadcast to all 6 nodes (no inter-station information is used yet; true multi-station inputs are Stage 2 future work).
5. **`MultiModalNPZNet`:** Fuses `Conv2d(6 -> 16)` NWP grids (`6×16×16`), `Conv2d(3 -> 16)` satellite grids (`3×32×32`), `24×6×12` sequences, and $A_{\text{norm}}$ on `line_b_final_dataset.npz` (`AdamW`, `lr=2e-3`, `L1Loss`).

---

## 7. Complete Empirical Results (CV, Classification, Regression)

### 7.1 Main Line A: 5-Fold Rolling-Origin CV ROC-AUC (`nb02_line_a_5fold_cv_hourly.csv`)
| Horizon | Days | `LogReg_Bal` | `RandomForest` | `ExtraTrees` | `HistGB` | `XGBoost` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **24 h** | 1 | 0.8527 | 0.8611 | 0.8598 | 0.8469 | **0.8619** |
| **72 h** | 3 | 0.7875 | 0.8047 | **0.8097** | 0.7832 | 0.8030 |
| **168 h** | 7 | 0.7871 | 0.7822 | **0.7992** | 0.7509 | 0.7630 |
| **216 h** | 9 | 0.7937 | 0.7753 | **0.8043** | 0.7278 | 0.7476 |
| **360 h** | 15 | 0.8052 | 0.8052 | **0.8447** | 0.7615 | 0.7754 |

### 7.2 Main Line A: Calibrated Test Classification (`nb02_line_a_classification_hourly.csv`)
| Horizon | Best Line A Model | Val ROC-AUC | Test ROC-AUC | `MonthClimo_Cal` | `Persistence_Cal` | Test PR-AUC | Test BSS | Lift@Top10% |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **24 h (1 d)** | `RandomForest_Cal` | 0.8368 | **0.8090** | 0.643 | 0.5701 | 0.3143 | 0.3218 | **4.28×** |
| **72 h (3 d)** | `RandomForest_Cal` | 0.7590 | **0.7167** | 0.641 | 0.5451 | 0.3838 | 0.2724 | 2.67× |
| **168 h (7 d)** | `RandomForest_Cal` | 0.6893 | **0.7031** | 0.658 | 0.5436 | 0.5657 | 0.1763 | 2.03× |
| **216 h (9 d)** | `XGBoost_Cal` | 0.6777 | **0.7156** | 0.666 | 0.5410 | 0.6522 | 0.0301 | 1.77× |
| **360 h (15 d)** | `XGBoost_Cal` | 0.7224 | **0.7655** | 0.665 | 0.4721 | 0.8311 | 0.1313 | 1.67× |

### 7.3 Main Line B: PyTorch Classification & Regression (`nb03_line_b_*_hourly.csv`)
| Horizon | Best Line B Cls | Test ROC-AUC | Test PR-AUC | Test BSS | Best Line B Reg | Test RMSE (μg/m³) | Test MAE (μg/m³) |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: |
| **24 h (1 d)** | `LineB_PINN` | 0.7939 | 0.2745 | 0.2159 | `LineB_STGNN` | 21.55 | 6.90 |
| **72 h (3 d)** | `LineB_Transformer` | 0.7158 | 0.3465 | 0.2571 | `LineB_STGNN` | 15.58 | 7.09 |
| **168 h (7 d)** | `LineB_PINN` | 0.6820 | 0.5402 | 0.2395 | `LineB_LSTM` | 14.45 | 8.76 |
| **216 h (9 d)** | `LineB_Transformer` | 0.7065 | 0.6466 | 0.2467 | `LineB_STGNN` | 14.86 | 10.11 |
| **360 h (15 d)** | `LineB_Transformer` | 0.6817 | 0.7739 | 0.1603 | `LineB_LSTM` | 14.13 | 10.43 |

### 7.4 Continuous $\text{PM}_{10}$ Regression Comparison (`nb02_line_a_regression_hourly.csv` vs. Line B)
- **Non-trivial Line A ML RMSE:** `ExtraTrees` `26.34 μg/m³` (`24 h`) and `27.63 μg/m³` (`72 h`); `Ridge_log1p` `29.72` (`168 h`), `27.68` (`216 h`), and `30.25 μg/m³` (`360 h`).
- **Constant Baseline (`Trivial_Median`):** `20.86 μg/m³` (`24 h`), `11.8 μg/m³` (`168 h`), `15.5 μg/m³` (`360 h`).
- **Conclusion:** All models obtain **negative test $R^2$**, and `Trivial_Median` achieves lower RMSE than the best Line B model at `24–216 h` (`11.8 vs. 14.5 μg/m³` at `168 h`), with Line B lower only at `360 h` (`14.1 vs. 15.5 μg/m³`). Continuous regression skill is **not demonstrated** in this prototype.

---

## 8. Explainable AI Suite (XAI-1 to XAI-6) & Physical Findings

Executed in `04_Notebooks/04_explainable_ai_xai_riyadh.ipynb` on the `168 h` clean hourly test set:
- **XAI-1 & XAI-2 (Gain, Permutation & Exact `shap.TreeExplainer`):** Global ranking, directional beeswarm, modality shares (`Ground_METAR ~37.4%`, `Calendar_Diurnal ~32.2%`, `ERA5_Physics ~23.5%`, `Satellite_Detrended ~4.7%`, `CAMS_NWP_Detrended ~1.8%`), and local waterfall on the highest-risk test timestamp (`2024-06-20 04:00:00`: `pm10_calibrated_ugm3 +1.10`, `dust_rate_4320h +0.54`, `sin_doy +0.38`, `cos_doy +0.31`, `has_wxcode +0.27`, `pm10_clean_ugm3 +0.26`, `dust_rate_720h +0.25`, `vsby +0.20`).
- **XAI-3 & XAI-4 (PDP/ICE & 2D Interaction):** 1D PDP/ICE curves for top 4 drivers (`sin_doy` rising monotonically from `~0.45` to `~0.59`) and 2D interaction surface (`sin_doy` × `dust_rate_4320h`, `0.44` to `>0.57`).
- **XAI-5 & XAI-6 (PyTorch LSTM Saliency & Horizon Shift):** Input-gradient temporal saliency across the 24-hour lookback window peaks at `Lag 0 h` (`0.0088`), `Lag -1 h` (`0.0037`), and `Lag -2 h` (`0.0023`); horizon tracking (`24 h -> 168 h -> 360 h`) shows `sin_doy` growing from `~0.19` to `~1.37` while `sat_retrieved_pm10_detrended_z` peaks at `24 h` and decays by `360 h`.

### Top 10 Predictors at `168 h` (`nb04_xai_clean_hourly_importance.csv`)
| Rank | Feature | `XGB_Gain` | `ET_Gini` | `XGB_Perm_ROC` | `ET_Perm_ROC` | `Mean_Abs_SHAP` |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | `sin_doy` | 0.06113 | 0.13477 | 0.16749 | 0.03060 | **0.71245** |
| **2** | `dust_rate_4320h` | 0.01446 | 0.00715 | 0.00563 | 0.00049 | **0.52050** |
| **3** | `hours_since_dust` | 0.01461 | 0.01838 | 0.01524 | -0.00085 | **0.24132** |
| **4** | `dust_rate_720h` | 0.01538 | 0.02220 | -0.00183 | -0.00126 | **0.17698** |
| **5** | `era5_soil_moisture_7_to_28cm` | 0.01607 | 0.02349 | -0.01419 | -0.00803 | **0.12351** |
| **6** | `era5_soil_moisture_0_to_7cm` | 0.03189 | 0.03212 | 0.00299 | -0.00322 | **0.10673** |
| **7** | `cos_doy` | 0.01515 | 0.01505 | -0.00612 | 0.00050 | **0.09449** |
| **8** | `sat_retrieved_pm10_detrended_z` | 0.03097 | 0.03091 | 0.00133 | 0.00031 | **0.08923** |
| **9** | `phys_vpd_kpa_roll168h` | 0.01596 | 0.02346 | 0.00474 | 0.00540 | **0.08831** |
| **10** | `gust` | 0.01465 | 0.00455 | -0.00796 | -0.00035 | **0.07611** |

---

## 9. Notebook & Figure Catalog (`00` through `04`)

| Notebook | Purpose | Key Figures Produced (`07_Figures/`) |
| :--- | :--- | :--- |
| `00_data_representation_and_distribution_riyadh.ipynb` | Exploratory hourly climatology, wind rose, missingness & raw censoring | `nb00_fig01.png` .. `nb00_fig12.png` |
| `01_feature_engineering_and_impact.ipynb` | De-censoring `53.7 μg/m³`, train-only Yeo-Johnson, MI screening & regime shift | `nb01_fig01.png` .. `nb01_fig03.png` |
| `02_line_a_tabular_and_meta_models_riyadh.ipynb` | 5-fold CV, calibrated classification, reliability diagram, RMSE/R², Lift@Top10% | `nb02_fig01.png` .. `nb02_fig08.png` |
| `03_line_b_pytorch_real_layers.ipynb` | PyTorch LSTM, Transformer, PINN, ST-GNN training curves & cross-line comparison | `nb03_fig01.png` .. `nb03_fig06.png` |
| `04_explainable_ai_xai_riyadh.ipynb` | XAI-1 to XAI-6 (SHAP, beeswarm, modalities, waterfall, PDP/ICE, 2D, LSTM saliency, shift) | `nb04_fig01.png` .. `nb04_fig07.png`, `nb04_fig09.png` |

---

## 10. Scripts Index (`08_Scripts/`) & Reproduction Commands

- **`01_data_acquisition/`:** `download_all_real_riyadh_data.py`, `download_cams.py`, `download_era5.py`, `download_modis_aod.py`, `era5_big_batch.py`, `era5_bulk_download.py`, `era5_optimized.py`, `era5_pl_quarterly.py`, `era5_supplement.py`, `submit_all_cams.py`, `submit_all_era5.py`.
- **`02_data_verification_qaqc/`:** `qaqc_aeronet.py`, `qaqc_cams.py`, `qaqc_cmip6.py`, `qaqc_era5.py`, `qaqc_report.py`.
- **`03_collocation_and_features/`:** `build_meta_features.py`, `collocate_cams_aeronet.py`, `data_handling_and_feature_balancing.py`, `merge_cams.py`, `three_way_validation.py`.
- **`04_model_training_and_tuning/`:** `optimize_threshold.py`, `run_line_a_honest_audit.py`, `run_meta_model_honest_cv.py`, `run_unified_honest_pipeline.py`, `train_line_b_pytorch.py`, `train_meta_model.py`.
- **`05_evaluation_and_plotting/`:**
  - `build_and_run_clean_hourly_notebooks.py` — reproducible end-to-end notebook runner.
  - `export_final_hourly_models.py` — exports Line A (`.joblib`) & Line B (`.pt`) artefacts into `05_Models/`.
  - `rebuild_ch4_results_latest.py`, `rebuild_ch5_discussion_latest.py`, `rebuild_ch6_conclusion_latest.py`, `add_appendices_packages_latest.py`, `update_abstract_latest.py`, `apply_5_user_fixes.py` — thesis `.docx` synchronization scripts.
  - `enrich_midterm_pptx.py` — adds callouts, software stack slide, and 57-slide speaker notes to `02_Presentation/Riyadh_Sandstorm_Forecasting_Midterm (1).pptx`.

```powershell
# 1. Execute clean hourly notebooks (00 -> 04)
.venv\Scripts\python.exe 08_Scripts\05_evaluation_and_plotting\build_and_run_clean_hourly_notebooks.py

# 2. Export final Line A & Line B model artefacts
.venv\Scripts\python.exe 08_Scripts\05_evaluation_and_plotting\export_final_hourly_models.py
```

---

## 11. Software Environment & Verified Package Stack

Verified inside `.venv` (**Python `3.12.0`**):

| Package | Version | Category | Role in Pipeline |
| :--- | :--- | :--- | :--- |
| `Python` | `3.12.0` | Core Runtime | Primary interpreter for all scripts & notebooks |
| `numpy` / `pandas` / `scipy` | `2.5.4` / `3.1.1` / `1.18.1` | Core & Tabular | Tensor prep, 86,928-h alignment, 360 h splits, stats |
| `scikit-learn` / `xgboost` | `1.9.1` / `3.4.1` | Line A Tabular ML | `LogReg_Bal`, `RF`, `ExtraTrees`, `HistGB`, `XGBoost`, `Ridge_log1p`, calibration |
| `torch` | `2.15.0+cpu` | Line B Deep Learning | `RealLSTMNet`, `RealTransformerNet`, `RealPINNNet`, `RealSTGNNNet`, saliency |
| `shap` / `matplotlib` | `0.54.1` / `3.11.2` | XAI & Plotting | Exact `TreeSHAP`, PDP/ICE, beeswarm, waterfall & `nb0*` figures |
| `xarray` / `netCDF4` / `cdsapi` | `2026.9.0` / `1.7.5.1.post1` / `0.7.7` | Reanalysis I/O | ECMWF ERA5 & CAMS NetCDF retrieval & decoding |
| `requests` / `joblib` / `ipykernel` | `2.34.2` / `1.6.0` / `7.4.0` | I/O & Execution | HTTP feeds, `.joblib` serialization, Jupyter kernel execution |
| `python-docx` / `python-pptx` | `1.2.0` / `1.0.2` | Documentation | Automated thesis `.docx` & mid-term `.pptx` generation |

---

## 12. Known Mid-Term Prototype Limitations & Stage-Two Roadmap

This mid-term prototype documents known limitations that require modifying the underlying code and data-ingestion pipeline, and are therefore scoped to the **final thesis stage**:
1. **Test-based best-model selection:** Replace post-hoc test selection with strict validation-based selection (`2 Jan 2022 – 14 Jun 2023`) and formal confidence intervals.
2. **Modelled $\text{PM}_{10}$ background:** Replace visibility/ERA5-derived $\text{PM}_{10}$ proxy with measured ground $\text{PM}_{10}$ observations where available.
3. **Single-station graph inputs:** Supply distinct upstream multi-station time series to all 6 nodes of `RealSTGNNNet`.
4. **Shared satellite/CAMS sourcing:** Audit and decouple potential common aerosol retrieval sources.
5. **Seasonal long-range skill & convective haboobs:** Implement rolling recalibration, 15-minute Meteosat SEVIRI dust-RGB imagery, and localized Doppler weather radar integration for `< 6 h` convective haboob nowcasting.
