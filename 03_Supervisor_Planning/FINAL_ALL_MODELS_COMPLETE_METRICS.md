# Complete Metrics Compendium — All Models (Honest Audited Results & Exploratory Appendix)

This document consolidates **every observed evaluation metric** across all models in the repository, compiled directly from [`06_Data/results/`](../06_Data/results). Every main-text table includes its **majority-class or trivial baseline**, states the **exact dataset, split, and positive count**, and uses **leak-free chronological splits**. Earlier, non-comparable, or test-tuned runs are separated into **Section 7 (Appendix)**.

> [!NOTE]
> **Post-Hoc Iteration Disclosure:** Switching the PyTorch regression loss from `HuberLoss` to `L1Loss` (Section 3) and adding the causal trailing-180d persistence feature (`recent_storm_rate_180d`, Section 1–2) were applied after inspecting initial test-split diagnostics. Pure monotonic `Platt` calibration on Validation is used throughout (no test-time prior shift), and `recent_storm_rate_180d` uses strictly past (`<= t - 24h`) data with zero future label leakage. However, because the **last rolling CV fold** also covers the `2023–2024` period whose diagnostics were inspected, the pooled CV is not completely untouched by this mild post-hoc iteration.

---

## Summary Verdict Table

| Component | Verdict |
| :--- | :--- |
| **Methodology and honesty** (`72h` gap, `Platt` calibration, 7-day block & paired bootstrap, multi-seed, leaky runs in appendix) | **Good** |
| **Meta-model reliability flagging** (`ROC-AUC = 0.808`, `PR-AUC = 0.176`, `F1 = 0.231`) | **Average to good** (best result, but F1 is low) |
| **72h storm forecasting, pooled CV** (`ROC-AUC = 0.69–0.72`, `BSS = +0.06 to +0.09`; mostly seasonality & features) | **Average, modest skill** |
| **24h storm forecasting, pooled CV** (`BSS = -0.04 to +0.01`, Top-5% catches `~11–15%` of storms) | **Weak** |
| **Deep learning** (paired 72h `PR-AUC`/`BSS` edge, but `LogReg` matches/beats on 24h & `MonthClimo` beats in 2023–2024) | **No reliable advantage** |
| **Single `2023–2024` test split** (`33` positives, overlapping 95% CIs, negative BSS vs `0.0112` prior/trailing ref) | **Inconclusive** |
| **Continuous $\text{PM}_{10}$ regression** ($R^2 \approx 0$, ties median on RMSE, worse on MAE) | **Bad** (constrained by `53.7 µg/m³` visibility-proxy floor) |
| **NWP post-processing** (`73.98` vs median `57.78` overall; `449–453` vs `548` on storm hours) | **Good only on storm hours, worse than the median overall** |
| **5-tier hazard classifier** (no better than majority class) | **Bad** |

---

## 1. Unified Honest Calibrated Pipeline — 5-Fold Rolling-Origin Pooled CV (24h & 72h Storm Targets)
*(Source: [`06_Data/results/rolling_origin_pooled_cv_metrics.csv`](../06_Data/results/rolling_origin_pooled_cv_metrics.csv))*  
*Dataset & Split: 10-year Riyadh hourly record (`2015–2024`, 6h stride, `14,545` windows), 5-fold rolling-origin `TimeSeriesSplit` with `72h` gap (`GAP = 12` steps), Top-22 train-selected physical + persistence features, inner-validation Platt calibration applied identically to `Persistence_Cal`, `LineA`, and `LineB_LSTM_Cal`, 7-day Moving Block Bootstrap (`block_size = 28`) 95% CIs.*

| Target | Total Positives | Model | PR-AUC (95% Block CI) | ROC-AUC (95% Block CI) | Rec@Top5% | Lift@5% | Brier | BSS (Pooled) |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **24h_Storm** (`>150 µg/m³`) | 637 | `Persistence_Cal` *(Baseline)* | 0.0835 `[0.062, 0.108]` | 0.5504 `[0.502, 0.603]` | **0.1491** | **2.98×** | 0.0494 | +0.0061 |
| **24h_Storm** (`>150 µg/m³`) | 637 | `MonthClimo_Cal` *(Baseline)* | 0.0807 `[0.065, 0.103]` | 0.6434 `[0.598, 0.687]` | 0.0628 | 1.26× | 0.0493 | +0.0075 |
| **24h_Storm** (`>150 µg/m³`) | 637 | `LogReg_Features_Cal` *(Baseline)* | 0.1119 `[0.088, 0.142]` | **0.7270** `[0.692, 0.761]` | 0.1303 | 2.61× | 0.0519 | -0.0438 |
| **24h_Storm** (`>150 µg/m³`) | 637 | `LineA_RF_Cal` *(seed=42)* | 0.1032 `[0.080, 0.132]` | 0.6936 `[0.656, 0.730]` | 0.1350 | 2.70× | 0.0497 | -0.0005 |
| **24h_Storm** (`>150 µg/m³`) | 637 | `LineA_XGB_Cal` *(seed=42)* | 0.1111 `[0.087, 0.141]` | 0.7135 `[0.680, 0.748]` | 0.1460 | 2.92× | **0.0492** | **+0.0094** |
| **24h_Storm** (`>150 µg/m³`) | 637 | `LineB_LSTM_Cal` *(seed=42)* | 0.1006 `[0.079, 0.127]` | 0.6969 `[0.658, 0.733]` | 0.1068 | 2.14× | 0.0503 | -0.0119 |
| **72h_Window_Storm** (`>150 µg/m³`) | 3,079 | `Persistence_Cal` *(Baseline)* | 0.3654 `[0.318, 0.410]` | 0.6504 `[0.612, 0.685]` | 0.1140 | 2.28× | 0.1817 | +0.0403 |
| **72h_Window_Storm** (`>150 µg/m³`) | 3,079 | `MonthClimo_Cal` *(Baseline)* | 0.4061 `[0.348, 0.472]` | 0.6921 `[0.653, 0.730]` | 0.0741 | 1.48× | 0.1756 | +0.0725 |
| **72h_Window_Storm** (`>150 µg/m³`) | 3,079 | `LogReg_Features_Cal` *(Baseline)* | 0.4409 `[0.384, 0.498]` | 0.7178 `[0.680, 0.748]` | 0.1082 | 2.16× | 0.1756 | +0.0722 |
| **72h_Window_Storm** (`>150 µg/m³`) | 3,079 | `LineA_RF_Cal` *(seed=42)* | 0.4346 `[0.376, 0.491]` | 0.7022 `[0.664, 0.737]` | 0.1075 | 2.15× | 0.1753 | +0.0738 |
| **72h_Window_Storm** (`>150 µg/m³`) | 3,079 | `LineA_XGB_Cal` *(seed=42)* | 0.4255 `[0.369, 0.477]` | 0.6904 `[0.652, 0.725]` | 0.1085 | 2.17× | 0.1769 | +0.0653 |
| **72h_Window_Storm** (`>150 µg/m³`) | 3,079 | `LineB_LSTM_Cal` *(seed=42)* | **0.4872** `[0.425, 0.545]` | **0.7210** `[0.687, 0.752]` | **0.1354** | **2.71×** | **0.1683** | **+0.1111** |

### Multi-Seed Stability (`5` Seeds: `42, 123, 456, 789, 2024`, Mean $\pm$ SD)
*(Source: [`06_Data/results/rolling_origin_pooled_cv_multiseed.csv`](../06_Data/results/rolling_origin_pooled_cv_multiseed.csv))*

| Target | Model | PR-AUC (Mean $\pm$ SD) | ROC-AUC (Mean $\pm$ SD) | Rec@Top5% (Mean $\pm$ SD) | BSS (Mean $\pm$ SD) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **24h_Storm** | `LineA_RF_Cal` | `0.1033 ± 0.0034` | `0.6955 ± 0.0053` | `0.1372 ± 0.0069` | `0.0000 ± 0.0049` |
| **24h_Storm** | `LineA_XGB_Cal` | `0.1092 ± 0.0021` | `0.7100 ± 0.0035` | `0.1416 ± 0.0082` | `0.0093 ± 0.0018` |
| **24h_Storm** | `LineB_LSTM_Cal` | `0.0990 ± 0.0080` | `0.6927 ± 0.0148` | `0.1086 ± 0.0250` | `-0.0245 ± 0.0218` |
| **72h_Window_Storm** | `LineA_RF_Cal` | `0.4348 ± 0.0039` | `0.7032 ± 0.0035` | `0.1076 ± 0.0012` | `0.0751 ± 0.0042` |
| **72h_Window_Storm** | `LineA_XGB_Cal` | `0.4211 ± 0.0043` | `0.6887 ± 0.0036` | `0.1067 ± 0.0017` | `0.0620 ± 0.0038` |
| **72h_Window_Storm** | `LineB_LSTM_Cal` | `0.4701 ± 0.0113` | `0.7074 ± 0.0121` | `0.1277 ± 0.0048` | `0.0882 ± 0.0160` |

### Per-Fold Rolling-Origin CV (`ROC-AUC`, Fold 5 Covers `2023–2024`) & Paired 7-Day Block Bootstrap
*(Sources: [`rolling_origin_per_fold_cv_metrics.csv`](../06_Data/results/rolling_origin_per_fold_cv_metrics.csv) & [`rolling_origin_paired_bootstrap.csv`](../06_Data/results/rolling_origin_paired_bootstrap.csv))*

| Target | Fold | Positives | `Persistence_Cal` | `MonthClimo_Cal` | `LogReg_Features_Cal` | `LineA_RF_Cal` | `LineA_XGB_Cal` | `LineB_LSTM_Cal` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **24h_Storm** | 1 | 166 | 0.6088 | 0.6911 | **0.7656** | 0.7142 | 0.7050 | 0.7546 |
| **24h_Storm** | 2 | 157 | 0.4581 | 0.6325 | 0.7332 | 0.7139 | **0.7444** | 0.7029 |
| **24h_Storm** | 3 | 135 | 0.5515 | 0.6650 | **0.7546** | 0.7408 | 0.7418 | 0.7467 |
| **24h_Storm** | 4 | 155 | 0.6453 | 0.7193 | 0.7912 | 0.7967 | 0.7857 | **0.8085** |
| **24h_Storm** | 5 *(2023–24)* | 24 | 0.5739 | **0.7134** | 0.6320 | 0.6677 | 0.6908 | 0.7116 |
| **72h_Window_Storm** | 1 | 790 | 0.6226 | 0.7038 | 0.7957 | 0.7658 | 0.7120 | **0.8047** |
| **72h_Window_Storm** | 2 | 770 | 0.5708 | 0.6759 | 0.7207 | 0.6854 | 0.7100 | **0.7314** |
| **72h_Window_Storm** | 3 | 745 | 0.5512 | 0.6153 | **0.6892** | 0.6657 | 0.6724 | **0.6892** |
| **72h_Window_Storm** | 4 | 570 | 0.6255 | 0.7215 | 0.7450 | 0.7383 | 0.6794 | **0.7521** |
| **72h_Window_Storm** | 5 *(2023–24)* | 204 | 0.5231 | **0.6956** | 0.5874 | 0.6136 | 0.6212 | 0.5717 |

| Target | Paired Comparison (`A - B`) | $\Delta\text{PR-AUC}$ (95% Block CI) | $\Delta\text{ROC-AUC}$ (95% Block CI) | $\Delta\text{BSS}$ (95% Block CI) |
| :--- | :--- | :---: | :---: | :---: |
| **24h_Storm** | `LineB_LSTM_Cal - LineA_RF_Cal` | `-0.0028 [-0.016, +0.010]` | `+0.0033 [-0.025, +0.028]` | `-0.0116 [-0.032, +0.007]` |
| **24h_Storm** | `LineB_LSTM_Cal - LogReg_Features_Cal` | `-0.0114 [-0.030, +0.006]` | **`-0.0295 [-0.059, -0.004]`** | `+0.0302 [-0.010, +0.074]` |
| **24h_Storm** | `LineB_LSTM_Cal - Persistence_Cal` | `+0.0174 [-0.011, +0.043]` | **`+0.1468 [+0.093, +0.201]`** | `-0.0197 [-0.054, +0.009]` |
| **24h_Storm** | `LogReg_Features_Cal - Persistence_Cal` | **`+0.0289 [+0.002, +0.054]`** | **`+0.1763 [+0.118, +0.229]`** | **`-0.0499 [-0.105, -0.004]`** |
| **72h_Window_Storm** | `LineB_LSTM_Cal - LineA_RF_Cal` | **`+0.0534 [+0.024, +0.085]`** | `+0.0191 [-0.001, +0.042]` | **`+0.0378 [+0.011, +0.067]`** |
| **72h_Window_Storm** | `LineB_LSTM_Cal - LogReg_Features_Cal` | **`+0.0448 [+0.006, +0.082]`** | `+0.0033 [-0.015, +0.020]` | **`+0.0381 [+0.008, +0.072]`** |
| **72h_Window_Storm** | `LineB_LSTM_Cal - Persistence_Cal` | **`+0.1221 [+0.068, +0.177]`** | **`+0.0724 [+0.031, +0.113]`** | **`+0.0704 [+0.025, +0.112]`** |
| **72h_Window_Storm** | `LogReg_Features_Cal - Persistence_Cal` | **`+0.0774 [+0.032, +0.119]`** | **`+0.0690 [+0.025, +0.112]`** | `+0.0324 [-0.021, +0.076]` |

*Key Takeaway on Baselines, Paired Tests & Fold 5:* On `72h_Window_Storm`, `LineB_LSTM_Cal` has a statistically significant paired-bootstrap edge over `LineA_RF_Cal` and `LogReg_Features_Cal` on `PR-AUC` (`+0.0534`, `+0.0448`) and `BSS` (`+0.0378`, `+0.0381`), though not on `ROC-AUC`. On `24h_Storm`, `LogReg_Features_Cal` significantly outperforms `LineB_LSTM_Cal` on `ROC-AUC` (`-0.0295 [-0.059, -0.004]`), while in **Fold 5 (`2023–2024`)**, `MonthClimo_Cal` (`0.7134` on 24h, `0.6956` on 72h) beats **every** ML/DL model on 72h and beats `LogReg`/`RF`/`XGB` on 24h.

---

## 2. Unified Honest Pipeline — Single `2023–2024` Test Split (`2,902` Windows, `33` Positives — Inconclusive)
*(Sources: [`unified_honest_classification_metrics.csv`](../06_Data/results/unified_honest_classification_metrics.csv) & [`unified_honest_classification_multiseed.csv`](../06_Data/results/unified_honest_classification_multiseed.csv))*  
*Note: `2023–2024` test split has `33 / 2,902 = 1.14%` storm windows (majority-class baseline accuracy = `0.9886`) vs `7.03%` in Validation (`2021–2022`) due to a possible instrument or reporting change in the `10 km` clear-sky visibility floor (`53.7 µg/m³` in `90.0%–94.7%` of hours vs `60.0%–76.2%` in 2015–2022). All models include `recent_storm_rate_180d` as a causal feature (`<= t - 24h`) and use pure monotonic `Platt` calibration fitted on Validation. `BSS` is measured against the strict `1.14%` test base-rate Brier (`0.0112`), and `BSS_vs_Trailing` is measured against the causal trailing-180d base-rate reference (`0.0112`). Confusion matrices are evaluated at the exact Top-5% alert budget (`146` flagged windows).*

| Model | Cal | PR-AUC (95% Block CI) | ROC-AUC (95% Block CI) | Prec@Top5% | Rec@Top5% (95% Block CI) | Lift@1% | Lift@5% | Brier | BSS (vs `0.0112`) | BSS vs Trailing | TP / FP / FN / TN (@5% = 146) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Baseline_Persistence_24h` | Platt | 0.0246 `[0.009, 0.056]` | 0.6141 `[0.514, 0.694]` | **0.0411** | **0.1818** `[0.040, 0.306]` | 2.93× | **3.61×** | **0.0137** | **-0.2206** | **-0.2201** | `6 / 140 / 27 / 2729` |
| `Baseline_Month_Climatology` | Platt | 0.0221 `[0.011, 0.050]` | 0.6864 `[0.566, 0.796]` | 0.0274 | 0.1212 `[0.000, 0.312]` | 0.00× | 2.41× | 0.0162 | -0.4388 | -0.4382 | `4 / 142 / 29 / 2727` |
| `Baseline_LogReg_Features` | Platt | 0.0158 `[0.009, 0.036]` | 0.5693 `[0.466, 0.725]` | 0.0137 | 0.0606 `[0.000, 0.238]` | 0.00× | 1.20× | 0.0830 | -6.3847 | -6.3819 | `2 / 144 / 31 / 2725` |
| `LineA_RandomForest` | Platt | 0.0204 `[0.012, 0.035]` | 0.6683 `[0.578, 0.785]` | 0.0068 | 0.0303 `[0.000, 0.139]` | 0.00× | 0.60× | 0.0354 | -2.1463 | -2.1452 | `1 / 145 / 32 / 2724` |
| `LineA_HistGB` | Platt | 0.0212 `[0.010, 0.060]` | 0.6081 `[0.501, 0.751]` | 0.0205 | 0.0909 `[0.000, 0.241]` | 2.93× | 1.81× | 0.0329 | -1.9284 | -1.9274 | `3 / 143 / 30 / 2726` |
| `LineA_XGBoost` | Platt | 0.0197 `[0.011, 0.046]` | 0.6289 `[0.516, 0.766]` | 0.0274 | 0.1212 `[0.000, 0.271]` | 2.93× | 2.41× | 0.0306 | -1.7257 | -1.7247 | `4 / 142 / 29 / 2727` |
| `LineB_PyTorch_PINN` *(seed=42)* | Platt | 0.0202 `[0.011, 0.037]` | 0.7013 `[0.605, 0.791]` | 0.0000 | 0.0000 `[0.000, 0.161]` | 0.00× | 0.00× | 0.0282 | -1.5102 | -1.5092 | `0 / 146 / 33 / 2723` |
| `LineB_Ablation_LSTM` *(seed=42)* | Platt | 0.0219 `[0.012, 0.045]` | **0.7177** `[0.625, 0.786]` | 0.0205 | 0.0909 `[0.000, 0.222]` | 2.93× | 1.81× | 0.0219 | -0.9498 | -0.9491 | `3 / 143 / 30 / 2726` |
| `LineB_Ablation_Transformer` *(seed=42)* | Platt | **0.0222** `[0.009, 0.084]` | 0.6065 `[0.500, 0.722]` | 0.0205 | 0.0909 `[0.000, 0.257]` | **5.86×** | 1.81× | 0.0376 | -2.3401 | -2.3389 | `3 / 143 / 30 / 2726` |

*Single-Split Deep Models Across 5 Seeds (`mean ± SD`):* `LineB_PyTorch_PINN` (`ROC-AUC = 0.6737 ± 0.0202`, `PR-AUC = 0.0191 ± 0.0019`, `Brier = 0.0312 ± 0.0029`, `BSS = -1.7743 ± 0.2617`), `LineB_Ablation_LSTM` (`0.6707 ± 0.0321`, `0.0185 ± 0.0021`, `0.0275 ± 0.0043`, `-1.4478 ± 0.3809`), `LineB_Ablation_Transformer` (`0.6197 ± 0.0205`, `0.0284 ± 0.0166`, `0.0323 ± 0.0077`, `-1.8699 ± 0.6859`).  
*Why `Baseline_Month_Climatology` Beats Trees & Why `LogReg` Collapses on `2023–2024`:* On the latest `2023–2024` split, pure seasonality (`Baseline_Month_Climatology`: `ROC-AUC = 0.6864`, `Brier = 0.0162`) outperforms `LineA_RandomForest`, `LineA_HistGB`, and `LineA_XGBoost` on **both** `ROC-AUC` and `Brier`. Meanwhile, `Baseline_LogReg_Features` collapses (`ROC-AUC = 0.5693`, `Brier = 0.0830`) due to linear extrapolation under the `2023–2024` regime shift: `nwp_cams_pm10` (coefficient `w = +0.39`) shifted to `+2.28` SD above the 2015–2020 training mean (reaching `+14.63` SD), inflating `LogReg`'s mean predicted probability on `2023–2024` from `0.0741` (Val) to `0.1597` (`max = 0.9892`, `14×` the `1.14%` test base rate).

---

## 3. Same-Split Continuous $\text{PM}_{10}$ Regression (`2023–2024` Test Split, `2,902` Windows, `µg/m³`)
*(Sources: [`unified_honest_regression_metrics.csv`](../06_Data/results/unified_honest_regression_metrics.csv) & [`unified_honest_regression_multiseed.csv`](../06_Data/results/unified_honest_regression_multiseed.csv))*  
*Deep models trained on `log1p(PM10)` with `L1Loss` (conditional median); XGBoost trained on `log1p(PM10)` with squared error; evaluated on the exact same `2,902` test windows in `µg/m³`.*

| Model | $R^2$ | RMSE ($\mu\text{g/m}^3$) | MAE ($\mu\text{g/m}^3$) | Notes |
| :--- | :---: | :---: | :---: | :--- |
| `Trivial_Train_Mean` (`104.3`) *(Baseline)* | -0.3216 | 88.41 | 53.73 | Over-predicts quiet 2023–2024 floor |
| `Trivial_Train_Median` (`53.7`) *(Baseline)* | -0.0082 | 77.22 | **6.94** | Matches the >90% test floor (`53.7 µg/m³`) |
| `LineA_XGBoost_log1p_Direct` | -0.3041 | 87.82 | 44.17 | Slightly better than Train Mean, far worse than Train Median |
| `LineA_XGBoost_Hurdle_Calibrated` | -0.8507 | 104.62 | 57.91 | Worse than both trivial baselines |
| `LineB_PyTorch_LSTM_log1p_L1` *(5 seeds)* | `-0.0077 ± 0.0049` | `77.20 ± 0.19` | `11.32 ± 2.78` | Ties Median on RMSE (`77.20` vs `77.22`), worse on MAE (`11.32` vs `6.94`) |
| `LineB_PyTorch_STGNN_log1p_L1` *(5 seeds)* | `-0.0048 ± 0.0028` | `77.09 ± 0.11` | `10.18 ± 0.52` | Ties Median on RMSE (`77.09` vs `77.22`), worse on MAE (`10.18` vs `6.94`) |

---

## 4. Part 1: Multimodal Reliability Meta-Models — Honest 5-Fold Rolling-Origin CV (`12,175` OOF Samples, `350` Positives)
*(Source: [`06_Data/results/meta_model_rolling_cv_metrics.csv`](../06_Data/results/meta_model_rolling_cv_metrics.csv))*  
*Protocol: `meta_features.csv` (`2015–2024`, 6h stride), 5-fold `TimeSeriesSplit(gap=12)` (`72h` gap), inner-validation Platt calibration and F1-threshold tuning strictly before the held-out test fold (NO SMOTE before split, NO test-set tuning), 7-day moving block bootstrap 95% CIs.*

| Model | Accuracy | Balanced Acc | Precision | Recall | F1 | Macro-F1 | ROC-AUC (95% Block CI) | PR-AUC (95% Block CI) | Brier | BSS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Training_Prior_Baseline` *(Always 0 class, prior prob = `0.0287`)* | **0.9713** | 0.5000 | 0.0000 | 0.0000 | 0.0000 | 0.4927 | 0.5000 `[0.500,0.500]` | 0.0287 `[0.029,0.029]` | 0.0279 | 0.0000 |
| `RandomForest` | 0.9519 | **0.6120** | 0.2136 | 0.2514 | **0.2310** | **0.6031** | **0.8080** `[0.768,0.843]` | **0.1757** `[0.136,0.216]` | **0.0260** | **+0.0676** |
| `XGBoost` | 0.9625 | 0.5828 | 0.2704 | 0.1800 | 0.2161 | 0.5984 | 0.7868 `[0.741,0.828]` | 0.1667 `[0.127,0.210]` | 0.0263 | +0.0577 |
| `HistGradientBoosting` | 0.9624 | 0.5869 | **0.2750** | 0.1886 | 0.2237 | 0.6022 | 0.7785 `[0.732,0.820]` | 0.1654 `[0.128,0.210]` | 0.0262 | +0.0599 |
| `NeuralNetwork` | 0.4323 | 0.5774 | 0.0362 | **0.7314** | 0.0690 | 0.3303 | 0.5711 `[0.530,0.612]` | 0.0323 `[0.025,0.040]` | 0.0288 | -0.0306 |

---

## 5. Line A: Strictly Non-Leaky Hourly Tabular Audit (`2023–2024` Test Split, `17,352` Hours, `72h` Gap)

### A. Line A1 — NWP Bias Correction vs Raw CAMS Forecast (`190` High-$\text{PM}_{10}$ Hours $\ge 150\ \mu\text{g/m}^3$)
*(Source: [`06_Data/results/line_a1_honest_audit.csv`](../06_Data/results/line_a1_honest_audit.csv))*

> [!WARNING]
> **Overall Benchmark Is the Trivial Median (`57.78 µg/m³`), Not Raw CAMS (`407.44 µg/m³`):** Raw CAMS has `RMSE = 407.44` against a visibility-derived proxy (`std ≈ 58`), so `"+81.84% vs raw CAMS"` alone is a weak strawman. Against the honest overall benchmark (`Trivial_Train_Median = 57.78 µg/m³`, Section 5B), `LineA1_HistGB_log1p_NWP_PostProc` (`73.98 µg/m³`, `R² = -0.6532`) is **still worse overall**. It adds value only on the `190` high-$\text{PM}_{10}$ storm hours (`448.97–452.62` vs `548.04` median and `570.20` raw CAMS), noting that these `190` hours are clustered into **`41` distinct episodes (`≥12h` gap; `47` at `≥6h` gap, `35` at `≥24h` gap)**.

| Model | RMSE ($\mu\text{g/m}^3$) | MAE ($\mu\text{g/m}^3$) | True $R^2$ | RMSE Reduction vs Raw CAMS | High-$\text{PM}_{10}$ RMSE | High-$\text{PM}_{10}$ MAE | High-$\text{PM}_{10}$ RMSE Reduction vs Raw CAMS |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Raw_CAMS_Baseline` | 407.44 | 207.04 | -49.1389 | 0.00% | 570.20 | 383.21 | 0.00% |
| `LineA1_HistGB_NWP_Bias_Correction` *(Additive)* | 419.71 | 209.88 | -52.2040 | -3.01% | 708.47 | 495.84 | -24.25% |
| `LineA1_XGBoost_NWP_Bias_Correction` *(Additive)* | 418.27 | 211.01 | -51.8404 | -2.66% | 725.86 | 508.37 | -27.30% |
| `LineA1_HistGB_log1p_NWP_PostProc` | **73.98** | **33.84** | **-0.6532** | +81.84% *(worse than `57.78` median)* | 452.62 | 289.17 | +20.62% |
| `LineA1_XGBoost_log1p_NWP_PostProc` | 75.45 | 34.42 | -0.7195 | +81.48% *(worse than `57.78` median)* | **448.97** | **286.19** | **+21.26%** |

### B. Line A2 — $T+24\text{h}$ Quantile & Point Forecasters vs Trivial Train Median (`53.7 µg/m³`)
*(Source: [`06_Data/results/line_a2_honest_audit.csv`](../06_Data/results/line_a2_honest_audit.csv))*

| Model | RMSE ($\mu\text{g/m}^3$) | MAE ($\mu\text{g/m}^3$) | True $R^2$ | Mean 80% Width | Overall PICP80 | Storm RMSE (`n=190`) | Storm MAE (`n=190`) | Storm 80% Width | Storm PICP80 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Trivial_Train_Median` (`53.7`) *(Baseline)* | **57.78** | **5.61** | **-0.0095** | — | — | 548.04 | 391.81 | — | — |
| `LineA2_HistGB_T+24h_Quantile_P50` | **57.78** | **5.61** | **-0.0095** | 208.21 | 97.8% | 548.04 | 391.81 | 269.75 | 30.0% |
| `LineA2_XGBoost_T+24h_Forecaster` | 149.98 | 96.26 | -5.8009 | — | — | **481.18** | **300.72** | — | — |

*Finding:* `LineA2_HistGB_T+24h_Quantile_P50` matches the trivial train median identically (`RMSE = 57.78`, `MAE = 5.61`, `R² = -0.0095`)—it learned the `53.7 µg/m³` METAR clear-sky floor. Moreover, its nominal 80% interval is **badly calibrated in both directions**: it over-covers overall (`97.8%`) while severely under-covering actual storm hours (`30.0%`, across `190` hours clustered into `41` episodes at `≥12h` gap).

### C. Line A3 — 5-Tier WMO/CMA Dust Hazard Classifier vs Majority-Class Baseline
*(Source: [`06_Data/results/line_a3_honest_audit.csv`](../06_Data/results/line_a3_honest_audit.csv))*

| Model | Accuracy | Balanced Accuracy | Macro-F1 | Weighted-F1 | Recall Tier 1 (`50–150`, `n=17,162`) | Recall Tier 2 (`150–500`, `n=156`) | Recall Tier 3 (`500–1500`, `n=26`) | Recall Tier 4 (`>=1500`, `n=8`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Majority_Class_Baseline` *(Always Tier 1)* | **0.9891** | **0.2500** | **0.2486** | **0.9836** | **1.0000** | 0.0000 | 0.0000 | 0.0000 |
| `LineA3_HistGB_5Tier_Hazard` | 0.8445 | 0.2373 | 0.2328 | 0.9061 | 0.8530 | **0.0962** | 0.0000 | 0.0000 |
| `LineA3_XGBoost_5Tier_Hazard` | 0.9867 | 0.2494 | 0.2483 | 0.9824 | 0.9976 | 0.0000 | 0.0000 | 0.0000 |

*Finding:* Neither non-leaky 5-tier classifier beats `Majority_Class_Baseline` (`0.9891` accuracy, `0.2500` balanced accuracy, `0.2486` macro-F1).

---

## 6. What You Can Validly Claim (and Key Limitations)
1. **Meta-model reliability flagging:** A clear, statistically supported signal (`ROC-AUC = 0.8080 [0.768, 0.843]`, `F1 = 0.2310`, `BSS = +0.0676` for `RandomForest`) over the training-prior baseline.
2. **72h vs 24h storm forecasting (Pooled CV):**
   * On **`72h_Window_Storm` (`3,079` positives)**, engineered-feature models and seasonality (`MonthClimo_Cal` `ROC-AUC = 0.6921`, `BSS = +0.0725`; `LogReg_Features_Cal` `ROC-AUC = 0.7178`, `BSS = +0.0722`; `LineA_RF_Cal` `0.7032 ± 0.0035`; `LineB_LSTM_Cal` `0.7074 ± 0.0121`, `BSS = +0.0882 ± 0.0160`) beat `Persistence_Cal` (`ROC-AUC = 0.6504`, `BSS = +0.0403`). Paired 7-day block bootstrap shows `LSTM` has a significant edge over `RF` and `LogReg` on `PR-AUC` (`+0.0534`, `+0.0448`) and `BSS` (`+0.0378`, `+0.0381`), though not on `ROC-AUC`, and in **Fold 5 (`2023–2024`)** `MonthClimo_Cal` (`0.6956`) beats every ML/DL model.
   * On **`24h_Storm` (`637` positives)**, `LogReg_Features_Cal` (`ROC-AUC = 0.7270`) significantly beats `LSTM` (`dROC_AUC = -0.0295 [-0.059, -0.004]`) and matches or exceeds trees (`0.696–0.710`), while `Persistence_Cal` retains the best `Rec@Top5%` (`0.1491`) and `Lift@5%` (`2.98×`). Overall `BSS` is weak (`-0.04` to `+0.01`) and Top-5% catches only `~11–15%` of storms.
3. **Single `2023–2024` test split (`33` positives):** Inconclusive. All 95% block CIs overlap, `Baseline_Month_Climatology` (`0.6864`, `Brier = 0.0162`) beats `RF`, `HistGB`, `XGBoost`, and `LogReg` on both `ROC-AUC` and `Brier`, and every model has negative `BSS` against both the `1.14%` test base-rate Brier (`0.0112`) and the causal trailing-180d base-rate Brier (`0.0112`).
4. **Continuous $\text{PM}_{10}$ regression:** Bad (`R² ≈ 0`, 5-seed `LSTM`/`ST-GNN` `RMSE = 77.20 ± 0.19` / `77.09 ± 0.11` ties the median `77.22` and is worse on `MAE` `11.32 ± 2.78` / `10.18 ± 0.52` vs `6.94`), because `PM10` is a visibility-derived proxy with a `53.7 µg/m³` floor in `>90%` of `2023–2024` hours.
5. **NWP post-processing & 5-tier hazard:** `LineA1_HistGB_log1p_NWP_PostProc` (`73.98`) is worse than the trivial median (`57.78`) overall, helping only on the `190` high-$\text{PM}_{10}$ storm hours (`41` episodes at `≥12h` gap). The 5-tier classifier does not beat the majority class.

---

## 7. Appendix — Exploratory / Earlier-Split / Leaky Runs (Not Comparable, Superseded)

> [!WARNING]
> The tables in this appendix are preserved strictly for transparency. They are **superseded** by Sections 1–5 above and **must not** be cited as valid headline results.

### A. Part 1 Meta-Model — Leaky / Test-Tuned Threshold Runs *(In-Sample / Test-Tuned, Leaky, Not Valid)*
* [`optimal_thresholds.csv`](../06_Data/results/optimal_thresholds.csv): `RandomForest` (`F1 = 0.8054`), `GradientBoosting` (`F1 = 0.8722`), `NeuralNetwork` (`F1 = 0.8128`) — **invalid** due to leaky/in-sample threshold optimization; superseded by Section 4 (`meta_model_rolling_cv_metrics.csv`, `F1 = 0.2161–0.2310`).
* [`model_comparison.csv`](../06_Data/results/model_comparison.csv): `RandomForest` (`ROC-AUC = 0.6590`, `F1 = 0.0488`), `XGBoost` (`0.6544`, `F1 = 0.0662`), `GradientBoosting` (`0.6189`, `F1 = 0.0620`), `NeuralNetwork` (`0.5825`, `F1 = 0.0465`) — **test-tuned optimal threshold** on the single 2023–2024 split; superseded by Section 4.

### B. Line B — Earlier Split (`23` Positives) & 400-Sample Multi-Node Snapshot *(Exploratory, Not Comparable)*
* [`line_b_pytorch_metrics.csv`](../06_Data/results/line_b_pytorch_metrics.csv) (`2,917` test windows, `23` positives, earlier uncalibrated split with test-tuned F1 threshold): `PyTorch_LSTM_2Layer` (`ROC-AUC = 0.7692`, `PR-AUC = 0.0233`, `Brier = 0.0467`), `PyTorch_Transformer_4Head` (`0.7115`, `0.0171`), `PyTorch_PINN_Autograd` (`0.7529`, `0.0230`), `PyTorch_LSTM_Transformer_Ensemble` (`0.7272`, `0.0185`). Superseded by Sections 1–2.
* **Exploratory 400-Sample 6-Node ST-GNN (`line_b_final_dataset.npz`, raw unscaled `targets_pm10` up to `4,800 µg/m³`):** `R² = -0.0843`, `RMSE = 628.24`, `MAE = 241.08`. Uses a different 400-sample dataset and raw target scale; superseded by Section 3 (`LineB_PyTorch_STGNN_log1p_L1`, `RMSE = 77.04`).
* [`line_b_metrics.csv`](../06_Data/results/line_b_metrics.csv): Original `scikit-learn` MLP surrogates (`LineB_LSTM_Sequence_Classifier` `AUC = 0.6881`, `LineB_6Node_ST_GNN_LSTM_Transformer_Regressor` `RMSE = 628.13`). Exploratory surrogates superseded by Sections 1–3.

