# Complete Metrics Compendium — All Models (Honest Audited Results & Exploratory Appendix)

This document consolidates **every observed evaluation metric** across all models in the repository, compiled directly from [`06_Data/results/`](../06_Data/results). Every main-text table includes its **majority-class or trivial baseline**, states the **exact dataset, split, and positive count**, and uses **leak-free chronological evaluation** (no test-set threshold tuning or calibration). Earlier, non-comparable, or test-tuned runs are separated into **Section 6 (Appendix)**.

---

## 1. Unified Honest Calibrated Pipeline — 5-Fold Rolling-Origin Pooled CV (24h & 72h Storm Targets)
*(Source: [`06_Data/results/rolling_origin_pooled_cv_metrics.csv`](../06_Data/results/rolling_origin_pooled_cv_metrics.csv))*  
*Dataset & Split: 10-year Riyadh hourly record (`2015–2024`, 6h stride, `14,545` windows), 5-fold rolling-origin `TimeSeriesSplit` with `72h` gap (`GAP = 12` steps), Top-22 train-selected physical + persistence features, inner-validation Platt calibration applied identically to both `Persistence_Cal` and ML models, 7-day Moving Block Bootstrap (`block_size = 28`) 95% CIs.*

| Target | Total Positives | Model | PR-AUC (95% Block CI) | ROC-AUC (95% Block CI) | Rec@Top5% | Lift@5% | Brier | BSS (Pooled) |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **24h_Storm** (`>150 µg/m³`) | 637 | `Persistence_Cal` *(Baseline)* | 0.0835 `[0.062, 0.108]` | 0.5504 `[0.502, 0.603]` | **0.1491** | **2.98×** | **0.0494** | **+0.0061** |
| **24h_Storm** (`>150 µg/m³`) | 637 | `LineA_RF_Cal` | **0.1004** `[0.079, 0.127]` | **0.7012** `[0.666, 0.737]` | 0.1287 | 2.57× | 0.0500 | -0.0051 |
| **24h_Storm** (`>150 µg/m³`) | 637 | `LineA_XGB_Cal` | 0.0944 `[0.076, 0.119]` | 0.6867 `[0.653, 0.724]` | 0.1036 | 2.07× | 0.0504 | -0.0133 |
| **72h_Window_Storm** (`>150 µg/m³`) | 3,079 | `Persistence_Cal` *(Baseline)* | 0.3654 `[0.318, 0.410]` | 0.6504 `[0.612, 0.685]` | **0.1140** | **2.28×** | 0.1817 | +0.0403 |
| **72h_Window_Storm** (`>150 µg/m³`) | 3,079 | `LineA_RF_Cal` | **0.4347** `[0.376, 0.489]` | **0.7060** `[0.670, 0.739]` | 0.1072 | 2.14× | **0.1741** | **+0.0805** |
| **72h_Window_Storm** (`>150 µg/m³`) | 3,079 | `LineA_XGB_Cal` | 0.4183 `[0.362, 0.468]` | 0.6829 `[0.646, 0.718]` | 0.1075 | 2.15× | 0.1785 | +0.0569 |

---

## 2. Unified Honest Calibrated Pipeline — Single `2023–2024` Test Split (`2,902` Windows, `33` Positives)
*(Source: [`06_Data/results/unified_honest_classification_metrics.csv`](../06_Data/results/unified_honest_classification_metrics.csv))*  
*Note: `2023–2024` test split has `33 / 2,902 = 1.14%` storm rate (majority-class baseline accuracy = `0.9886`) vs `7.03%` in Validation (`2021–2022`) due to the METAR `10 km` clear-sky visibility floor (`53.7 µg/m³` in `90.0%–94.7%` of hours).*

| Model | Cal | PR-AUC (95% Block CI) | ROC-AUC (95% Block CI) | Prec@Top5% | Rec@Top5% (95% Block CI) | Lift@1% | Lift@5% | Brier | BSS | TP / FP / FN / TN (@5%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Baseline_Persistence_24h` | Isotonic | 0.0218 `[0.009, 0.047]` | 0.5905 `[0.503, 0.658]` | **0.0548** | **0.2424** `[0.050, 0.312]` | **5.86×** | **4.82×** | **0.0134** | **+0.0804** | `8 / 183 / 25 / 2686` |
| `LineA_RandomForest` | Isotonic | 0.0216 `[0.013, 0.037]` | **0.6798** `[0.591, 0.789]` | 0.0137 | 0.0606 `[0.000, 0.191]` | 0.00× | 1.20× | 0.0365 | -1.5017 | `2 / 156 / 31 / 2713` |
| `LineA_HistGB` | Isotonic | 0.0165 `[0.009, 0.028]` | 0.6261 `[0.517, 0.757]` | 0.0068 | 0.0303 `[0.000, 0.179]` | 0.00× | 0.60× | 0.0409 | -1.8014 | `4 / 288 / 29 / 2581` |
| `LineA_XGBoost` | Isotonic | 0.0156 `[0.010, 0.027]` | 0.6118 `[0.514, 0.731]` | 0.0068 | 0.0303 `[0.000, 0.146]` | 0.00× | 0.60× | 0.0435 | -1.9844 | `2 / 192 / 31 / 2677` |
| `LineB_PyTorch_PINN` | Isotonic | 0.0166 `[0.010, 0.031]` | 0.6563 `[0.577, 0.752]` | 0.0137 | 0.0606 `[0.000, 0.200]` | 0.00× | 1.20× | 0.0329 | -1.2570 | `4 / 346 / 29 / 2523` |
| `LineB_Ablation_LSTM` *(Headline LSTM)* | Isotonic | 0.0175 `[0.011, 0.031]` | 0.6583 `[0.573, 0.745]` | 0.0137 | 0.0606 `[0.000, 0.167]` | 0.00× | 1.20× | 0.0191 | -0.3079 | `2 / 144 / 31 / 2725` |
| `LineB_Ablation_Transformer` | Isotonic | **0.0449** `[0.009, 0.113]` | 0.5814 `[0.471, 0.721]` | 0.0068 | 0.0303 `[0.000, 0.200]` | 2.93× | 0.60× | 0.0265 | -0.8141 | `5 / 331 / 28 / 2538` |

---

## 3. Same-Split Continuous $\text{PM}_{10}$ Regression (`2023–2024` Test Split, `2,902` Windows, `µg/m³`)
*(Source: [`06_Data/results/unified_honest_regression_metrics.csv`](../06_Data/results/unified_honest_regression_metrics.csv))*  
*All models trained on `log1p(PM10)` with `HuberLoss` (deep models) or squared error (XGBoost) and evaluated on the exact same `2,902` test windows in `µg/m³`.*

| Model | $R^2$ | RMSE ($\mu\text{g/m}^3$) | MAE ($\mu\text{g/m}^3$) | Notes |
| :--- | :---: | :---: | :---: | :--- |
| `Trivial_Train_Mean` (`104.3`) *(Baseline)* | -0.3216 | 88.41 | 53.73 | Over-predicts quiet 2023–2024 floor |
| `Trivial_Train_Median` (`53.7`) *(Baseline)* | -0.0082 | 77.22 | **6.94** | Matches the >90% test floor (`53.7 µg/m³`) |
| `LineA_XGBoost_log1p_Direct` | -0.2345 | 85.45 | 35.49 | Beats Train Mean, worse than Train Median |
| `LineA_XGBoost_Hurdle_Calibrated` | -1.1165 | 111.88 | 63.91 | *Reported failure:* 7% Val-calibrated $P(\text{storm})$ inflated predictions |
| `LineB_PyTorch_LSTM_log1p_Huber` | **-0.0038** | **77.05** | 9.31 | Matches the trivial median baseline ($R^2 \approx 0$) |
| `LineB_PyTorch_STGNN_log1p_Huber` | -0.0040 | 77.06 | 13.71 | Matches the trivial median baseline ($R^2 \approx 0$) |

---

## 4. Part 1: Multimodal Reliability Meta-Models — Honest 5-Fold Rolling-Origin CV (`12,175` OOF Samples, `350` Positives)
*(Source: [`06_Data/results/meta_model_rolling_cv_metrics.csv`](../06_Data/results/meta_model_rolling_cv_metrics.csv))*  
*Protocol: `meta_features.csv` (`2015–2024`, 6h stride), 5-fold `TimeSeriesSplit(gap=12)` (`72h` gap), inner-validation Platt calibration and F1-threshold tuning strictly before the held-out test fold (NO SMOTE before split, NO test-set tuning), 7-day moving block bootstrap 95% CIs.*

| Model | Accuracy | Balanced Acc | Precision | Recall | F1 | Macro-F1 | ROC-AUC (95% Block CI) | PR-AUC (95% Block CI) | Brier | BSS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Majority_Class_Baseline` *(Always 0)* | **0.9713** | 0.5000 | 0.0000 | 0.0000 | 0.0000 | 0.4927 | 0.5000 `[0.500,0.500]` | 0.0287 `[0.029,0.029]` | 0.0279 | 0.0000 |
| `RandomForest` | 0.9519 | **0.6120** | 0.2136 | 0.2514 | **0.2310** | **0.6031** | **0.8080** `[0.768,0.843]` | **0.1757** `[0.136,0.216]` | **0.0260** | **+0.0676** |
| `XGBoost` | 0.9625 | 0.5828 | 0.2704 | 0.1800 | 0.2161 | 0.5984 | 0.7868 `[0.741,0.828]` | 0.1667 `[0.127,0.210]` | 0.0263 | +0.0577 |
| `HistGradientBoosting` | 0.9624 | 0.5869 | **0.2750** | 0.1886 | 0.2237 | 0.6022 | 0.7785 `[0.732,0.820]` | 0.1654 `[0.128,0.210]` | 0.0262 | +0.0599 |
| `NeuralNetwork` | 0.4323 | 0.5774 | 0.0362 | **0.7314** | 0.0690 | 0.3303 | 0.5711 `[0.530,0.612]` | 0.0323 `[0.025,0.040]` | 0.0288 | -0.0306 |

---

## 5. Line A: Hourly Tabular Audit (`2023–2024` Test Split, `17,352` Hours, `72h` Gap)

### A. Line A1 — NWP Bias Correction vs Raw CAMS Forecast (`190` High-$\text{PM}_{10}$ Hours $\ge 150\ \mu\text{g/m}^3$)
*(Source: [`06_Data/results/line_a1_honest_audit.csv`](../06_Data/results/line_a1_honest_audit.csv))*

| Model | RMSE ($\mu\text{g/m}^3$) | MAE ($\mu\text{g/m}^3$) | True $R^2$ | RMSE Reduction vs Raw CAMS | High-$\text{PM}_{10}$ RMSE | High-$\text{PM}_{10}$ MAE | High-$\text{PM}_{10}$ RMSE Reduction vs Raw CAMS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Raw_CAMS_Baseline` | 407.44 | 207.04 | -49.1389 | 0.00% | 570.20 | 383.21 | 0.00% |
| `LineA1_HistGB_NWP_Bias_Correction` | **312.54** | **95.82** | **-28.5016** | **+23.29% RMSE reduction vs raw CAMS forecast** | **436.41** | **226.24** | **+23.46%** |
| `LineA1_XGBoost_NWP_Bias_Correction` | 321.81 | 99.76 | -30.2781 | +21.02% RMSE reduction vs raw CAMS forecast | 445.42 | 240.83 | +21.88% |

### B. Line A2 — $T+24\text{h}$ Quantile & Point Forecasters vs Trivial Train Median (`53.7 µg/m³`)
*(Source: [`06_Data/results/line_a2_honest_audit.csv`](../06_Data/results/line_a2_honest_audit.csv))*

| Model | RMSE ($\mu\text{g/m}^3$) | MAE ($\mu\text{g/m}^3$) | True $R^2$ | Mean 80% Width | Overall PICP80 | Storm RMSE (`n=190`) | Storm MAE (`n=190`) | Storm 80% Width | Storm PICP80 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Trivial_Train_Median` (`53.7`) *(Baseline)* | **57.78** | **5.61** | **-0.0095** | — | — | 548.04 | 391.81 | — | — |
| `LineA2_HistGB_T+24h_Quantile_P50` | **57.78** | **5.61** | **-0.0095** | 194.36 | 98.0% | 548.04 | 391.81 | 219.03 | 26.3% |
| `LineA2_XGBoost_T+24h_Forecaster` | 195.91 | 129.69 | -10.6051 | — | — | **470.51** | **280.48** | — | — |

*Finding:* `LineA2_HistGB_T+24h_Quantile_P50` matches the trivial train median identically (`RMSE = 57.78`, `MAE = 5.61`, `R² = -0.0095`)—it learned the `53.7 µg/m³` METAR clear-sky floor—and its 80% prediction interval covers only **26.3%** of actual storm hours ($\ge 150\ \mu\text{g/m}^3$).

### C. Line A3 — 5-Tier WMO/CMA Dust Hazard Classifier vs Majority-Class Baseline
*(Source: [`06_Data/results/line_a3_honest_audit.csv`](../06_Data/results/line_a3_honest_audit.csv))*

| Model | Accuracy | Balanced Accuracy | Macro-F1 | Weighted-F1 | Recall Tier 1 (`50–150`, `n=17,162`) | Recall Tier 2 (`150–500`, `n=156`) | Recall Tier 3 (`500–1500`, `n=26`) | Recall Tier 4 (`>=1500`, `n=8`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Majority_Class_Baseline` *(Always Tier 1)* | **0.9891** | 0.2500 | 0.2486 | **0.9836** | **1.0000** | 0.0000 | 0.0000 | 0.0000 |
| `LineA3_HistGB_5Tier_Hazard` | 0.9565 | **0.2896** | **0.2618** | 0.9676 | 0.9662 | **0.0769** | **0.1154** | 0.0000 |
| `LineA3_XGBoost_5Tier_Hazard` | 0.9890 | 0.2500 | 0.2486 | **0.9836** | 0.9999 | 0.0000 | 0.0000 | 0.0000 |

*Finding:* `LineA3_XGBoost_5Tier_Hazard` (`0.9890` accuracy) does **not** beat "always predict Tier 1" (`0.9891` accuracy, `Balanced_Acc = 0.2500`, `0%` recall on all storm tiers). `LineA3_HistGB_5Tier_Hazard` achieves `Balanced_Acc = 0.2896` and `Macro-F1 = 0.2618` with modest recall on Tiers 2–3 (`7.7%` and `11.5%`).

---

## 6. Appendix — Exploratory / Earlier-Split / Leaky Runs (Not Comparable, Superseded)

> [!WARNING]
> The tables in this appendix are preserved strictly for transparency. They are **superseded** by Sections 1–5 above and **must not** be cited as valid headline results.

### A. Part 1 Meta-Model — Leaky / Test-Tuned Threshold Runs *(In-Sample / Test-Tuned, Leaky, Not Valid)*
* [`optimal_thresholds.csv`](../06_Data/results/optimal_thresholds.csv): `RandomForest` (`F1 = 0.8054`), `GradientBoosting` (`F1 = 0.8722`), `NeuralNetwork` (`F1 = 0.8128`) — **invalid** due to leaky/in-sample threshold optimization; superseded by Section 4 (`meta_model_rolling_cv_metrics.csv`, `F1 = 0.2161–0.2310`).
* [`model_comparison.csv`](../06_Data/results/model_comparison.csv): `RandomForest` (`ROC-AUC = 0.6590`, `F1 = 0.0488`), `XGBoost` (`0.6544`, `F1 = 0.0662`), `GradientBoosting` (`0.6189`, `F1 = 0.0620`), `NeuralNetwork` (`0.5825`, `F1 = 0.0465`) — **test-tuned optimal threshold** on the single 2023–2024 split; superseded by Section 4.

### B. Line B — Earlier Split (`23` Positives) & 400-Sample Multi-Node Snapshot *(Exploratory, Not Comparable)*
* [`line_b_pytorch_metrics.csv`](../06_Data/results/line_b_pytorch_metrics.csv) (`2,917` test windows, `23` positives, earlier uncalibrated split with test-tuned F1 threshold): `PyTorch_LSTM_2Layer` (`ROC-AUC = 0.7692`, `PR-AUC = 0.0233`, `Brier = 0.0467`), `PyTorch_Transformer_4Head` (`0.7115`, `0.0171`), `PyTorch_PINN_Autograd` (`0.7529`, `0.0230`), `PyTorch_LSTM_Transformer_Ensemble` (`0.7272`, `0.0185`). Superseded by Section 2 (`LineB_Ablation_LSTM` `ROC-AUC = 0.6583 [0.573, 0.745]`).
* **Exploratory 400-Sample 6-Node ST-GNN (`line_b_final_dataset.npz`, raw unscaled `targets_pm10` up to `4,800 µg/m³`):** `R² = -0.0843`, `RMSE = 628.24`, `MAE = 241.08`. Uses a different 400-sample dataset and raw target scale; superseded by Section 3 (`LineB_PyTorch_STGNN_log1p_Huber`, `RMSE = 77.06`).
* [`line_b_metrics.csv`](../06_Data/results/line_b_metrics.csv): Original `scikit-learn` MLP surrogates (`LineB_LSTM_Sequence_Classifier` `AUC = 0.6881`, `LineB_6Node_ST_GNN_LSTM_Transformer_Regressor` `RMSE = 628.13`). Exploratory surrogates superseded by Sections 2–3.

