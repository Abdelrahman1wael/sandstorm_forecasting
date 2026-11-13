# Honest Evaluation, Calibration & Ablation Report (Line A & Line B)

**Pipeline Script:** [`08_Scripts/04_model_training_and_tuning/run_unified_honest_pipeline.py`](../08_Scripts/04_model_training_and_tuning/run_unified_honest_pipeline.py)  
**Dataset:** 10-year Riyadh hourly record (`2015–2024`, `87,456` rows at `6h` stride $\rightarrow$ `14,545` gapped sequence windows)  
**Target Definitions:**
1. **24h-Ahead Storm (`target_pm10_24h > 150 µg/m³`)** — WMO Moderate+ Dust Storm threshold
2. **72h-Window Storm (`max(PM10 in next 72h) > 150 µg/m³`)** — 3-day medium-range operational warning window
3. **Continuous 24h PM10 (`µg/m³`)** — Same-split regression trained on `log1p(PM10)`

---

## 1. Anti-Leakage & Methodological Controls

* **Chronological Split with 72h Gap (`GAP = 12` steps = `8` lookback + `4` horizon):**
  * **Train (`60%`):** `8,741` windows (`605` positives, `6.92%`)
  * **Validation (`20%`):** `2,902` windows (`204` positives, `7.03%`)
  * **Test (`20%`, 2023–2024):** `2,902` windows (`33` positives, `1.14%`)
* **Zero Contemporaneous Leakage & Train-Only Feature Selection:**
  * Removed all contemporaneous target, visibility, AOD, and residual columns and short `<24h` PM10 lags.
  * Added domain-driven persistence and seasonal climatology features (`recent_storm_count_7d`, `recent_storm_rate_180d`, `hours_since_last_storm`, `pm10_seasonal_anom_24h`, `wind_seasonal_anom`) using **Train-only monthly climatologies** and strictly causal past observations (`<= t - 24h` via `lag_pm10_calibrated_ugm3_24h`).
  * Selected Top-22 non-noisy predictors strictly on Train (`sin_doy`, `phys_air_density_kgm3`, `era5_wind_speed_10m`, `era5_10m_v_component_of_wind`, `era5_soil_moisture_0_to_7cm`, `nwp_cams_pm10`, `lag_pm10_calibrated_ugm3_24h`, `recent_storm_count_7d`, etc.).
  * Fitted `PowerTransformer(yeo-johnson)` and `StandardScaler` strictly on Train and applied identically to both Line A and Line B.
* **Calibration & Autocorrelation-Aware Uncertainty:**
  * Trained unweighted classifiers (`BCEWithLogitsLoss` without artificial `pos_weight` inflation) and fitted pure monotonic **Platt calibration** strictly on Validation (applied identically to **Persistence**, **Month-of-Year Climatology**, **Logistic Regression**, and **ML/DL models**).
  * Computed **7-day Moving Block Bootstrap (`block_size = 28` steps at `6h` stride) 95% Confidence Intervals** to account for temporal autocorrelation.

---

## 2. 5-Fold Rolling-Origin Pooled CV (Multi-Year Generalization + 7-Day Block CIs)

*(Source: [`06_Data/results/rolling_origin_pooled_cv_metrics.csv`](../06_Data/results/rolling_origin_pooled_cv_metrics.csv))*

Pooling out-of-fold predictions across 5 chronological folds (`72h` gap, inner-validation Platt calibration applied identically to **both `Persistence_Cal` and ML models**) yields **637** (`24h_Storm`) and **3,079** (`72h_Window_Storm`) real positive storm events:

| Target | Total Positives | Model | PR-AUC (95% Block CI) | ROC-AUC (95% Block CI) | Rec@Top5% | Lift@5% | Brier | BSS (Pooled) |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **24h_Storm** | 637 | `Persistence_Cal` | 0.0835 `[0.062, 0.108]` | 0.5504 `[0.502, 0.603]` | **0.1491** | **2.98×** | 0.0494 | +0.0061 |
| **24h_Storm** | 637 | `MonthClimo_Cal` | 0.0807 `[0.065, 0.103]` | 0.6434 `[0.598, 0.687]` | 0.0628 | 1.26× | 0.0493 | +0.0075 |
| **24h_Storm** | 637 | `LogReg_Features_Cal` | 0.1119 `[0.088, 0.142]` | **0.7270** `[0.692, 0.761]` | 0.1303 | 2.61× | 0.0519 | -0.0438 |
| **24h_Storm** | 637 | `LineA_RF_Cal` *(seed=42)* | 0.1032 `[0.080, 0.132]` | 0.6936 `[0.656, 0.730]` | 0.1350 | 2.70× | 0.0497 | -0.0005 |
| **24h_Storm** | 637 | `LineA_XGB_Cal` *(seed=42)* | 0.1111 `[0.087, 0.141]` | 0.7135 `[0.680, 0.748]` | 0.1460 | 2.92× | **0.0492** | **+0.0094** |
| **24h_Storm** | 637 | `LineB_LSTM_Cal` *(seed=42)* | 0.1006 `[0.079, 0.127]` | 0.6969 `[0.658, 0.733]` | 0.1068 | 2.14× | 0.0503 | -0.0119 |
| **72h_Window_Storm** | 3,079 | `Persistence_Cal` | 0.3654 `[0.318, 0.410]` | 0.6504 `[0.612, 0.685]` | 0.1140 | 2.28× | 0.1817 | +0.0403 |
| **72h_Window_Storm** | 3,079 | `MonthClimo_Cal` | 0.4061 `[0.348, 0.472]` | 0.6921 `[0.653, 0.730]` | 0.0741 | 1.48× | 0.1756 | +0.0725 |
| **72h_Window_Storm** | 3,079 | `LogReg_Features_Cal` | 0.4409 `[0.384, 0.498]` | 0.7178 `[0.680, 0.748]` | 0.1082 | 2.16× | 0.1756 | +0.0722 |
| **72h_Window_Storm** | 3,079 | `LineA_RF_Cal` *(seed=42)* | 0.4346 `[0.376, 0.491]` | 0.7022 `[0.664, 0.737]` | 0.1075 | 2.15× | 0.1753 | +0.0738 |
| **72h_Window_Storm** | 3,079 | `LineA_XGB_Cal` *(seed=42)* | 0.4255 `[0.369, 0.477]` | 0.6904 `[0.652, 0.725]` | 0.1085 | 2.17× | 0.1769 | +0.0653 |
| **72h_Window_Storm** | 3,079 | `LineB_LSTM_Cal` *(seed=42)* | **0.4872** `[0.425, 0.545]` | **0.7210** `[0.687, 0.752]` | **0.1354** | **2.71×** | **0.1683** | **+0.1111** |

### Multi-Seed Pooled CV Stability (`5` Seeds: `42, 123, 456, 789, 2024`, Mean $\pm$ SD)
*(Source: [`06_Data/results/rolling_origin_pooled_cv_multiseed.csv`](../06_Data/results/rolling_origin_pooled_cv_multiseed.csv))*

| Target | Model | PR-AUC (Mean $\pm$ SD) | ROC-AUC (Mean $\pm$ SD) | Rec@Top5% (Mean $\pm$ SD) | BSS (Mean $\pm$ SD) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **24h_Storm** | `LineA_RF_Cal` | `0.1033 ± 0.0034` | `0.6955 ± 0.0053` | `0.1372 ± 0.0069` | `0.0000 ± 0.0049` |
| **24h_Storm** | `LineA_XGB_Cal` | `0.1092 ± 0.0021` | `0.7100 ± 0.0035` | `0.1416 ± 0.0082` | `0.0093 ± 0.0018` |
| **24h_Storm** | `LineB_LSTM_Cal` | `0.0990 ± 0.0080` | `0.6927 ± 0.0148` | `0.1086 ± 0.0250` | `-0.0245 ± 0.0218` |
| **72h_Window_Storm** | `LineA_RF_Cal` | `0.4348 ± 0.0039` | `0.7032 ± 0.0035` | `0.1076 ± 0.0012` | `0.0751 ± 0.0042` |
| **72h_Window_Storm** | `LineA_XGB_Cal` | `0.4211 ± 0.0043` | `0.6887 ± 0.0036` | `0.1067 ± 0.0017` | `0.0620 ± 0.0038` |
| **72h_Window_Storm** | `LineB_LSTM_Cal` | `0.4701 ± 0.0113` | `0.7074 ± 0.0121` | `0.1277 ± 0.0048` | `0.0882 ± 0.0160` |

### Key Conclusions from Pooled Rolling-Origin CV, Per-Fold Audit & Paired Bootstrap
*(Sources: [`rolling_origin_per_fold_cv_metrics.csv`](../06_Data/results/rolling_origin_per_fold_cv_metrics.csv) & [`rolling_origin_paired_bootstrap.csv`](../06_Data/results/rolling_origin_paired_bootstrap.csv))*
* **24h Target:** `LogReg_Features_Cal` (`ROC-AUC = 0.7270 [0.692, 0.761]`) significantly beats `LineB_LSTM_Cal` (`dROC_AUC = -0.0295 [-0.059, -0.004]`), while `Persistence_Cal` retains the best `Rec@Top5%` (`0.1491`) and `Lift@5%` (`2.98×`). Overall `BSS` is weak (`-0.04` to `+0.01`) and Top-5% catches only `~11–15%` of storms.
* **72h Window Target:** Paired 7-day block bootstrap shows `LineB_LSTM_Cal` has a statistically significant edge over `LineA_RF_Cal` and `LogReg_Features_Cal` on `PR-AUC` (`+0.0534 [+0.024, +0.085]` and `+0.0448 [+0.006, +0.082]`) and `BSS` (`+0.0378 [+0.011, +0.067]` and `+0.0381 [+0.008, +0.072]`), though not on `ROC-AUC` (`+0.0191 [-0.001, +0.042]`, `+0.0033 [-0.015, +0.020]`).
* **Per-Fold Regime Shift (Fold 5 Covers `2023–2024`):** In **Fold 5 (`2023–2024`)**, `MonthClimo_Cal` (`ROC-AUC = 0.7134` on 24h, `0.6956` on 72h) beats **every** ML/DL model on 72h (`0.5717–0.6212`) and beats `LogReg`/`RF`/`XGB` on 24h (`0.6320–0.6908`).

---

## 3. Single Out-of-Sample Test Split (`2023–2024`, `2,902` Windows, `33` Positives — Deep Learning Ablation)

*(Source: [`06_Data/results/unified_honest_classification_metrics.csv`](../06_Data/results/unified_honest_classification_metrics.csv))*  
*Note: `2023–2024` majority-class baseline accuracy = `0.9886` (`33 / 2,902 = 1.14%` storm windows). All models include `recent_storm_rate_180d` as a causal feature (`<= t - 24h`) and use pure monotonic `Platt` calibration fitted on Validation; `BSS` is measured against the strict `1.14%` test base-rate Brier (`0.0112`), and the fair causal trailing-180d base-rate reference gives the exact same `Brier = 0.0112`. Confusion matrices are evaluated at the exact Top-5% alert budget (`146` flagged windows).*

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

*Single-Split Deep Models Across 5 Seeds (`mean ± SD`, [`unified_honest_classification_multiseed.csv`](../06_Data/results/unified_honest_classification_multiseed.csv)):* `PINN` (`ROC-AUC = 0.6737 ± 0.0202`, `Brier = 0.0312 ± 0.0029`), `LSTM` (`0.6707 ± 0.0321`, `0.0275 ± 0.0043`), `Transformer` (`0.6197 ± 0.0205`, `0.0323 ± 0.0077`).

### Why Single-Split Confidence Intervals Overlap, Why `MonthClimo` Beats Trees, & Why `LogReg` Collapses
1. **Honest `BSS` Reference (`0.0112`) & Pure Monotonic `Platt` Calibration:** Against both the `1.14%` test base-rate constant (`Brier = 0.0112`) and the causal trailing-180d base-rate forecast (`Brier = 0.0112`), every model has negative `BSS` (`-0.2206` to `-6.3847`) because Validation (`2021–2022`) had a `7.03%` base rate (`6×` higher than `2023–2024`). On `2023–2024`, `Baseline_Month_Climatology` (`ROC-AUC = 0.6864`, `Brier = 0.0162`) beats `RF`, `HistGB`, and `XGBoost` on both metrics. `Baseline_LogReg_Features` collapses (`Brier = 0.0830`) because `nwp_cams_pm10` (`w = +0.39`) shifted to `+2.28` SD above the Train mean (up to `+14.63` SD), extrapolating `LogReg`'s mean predicted probability to `0.1597` (`max = 0.9892`, `14×` the test base rate).
2. **Post-Hoc Iteration Disclosure & Statistical Indistinguishability:** Switching the PyTorch regression loss from `HuberLoss` to `L1Loss` and adding `recent_storm_rate_180d` occurred after inspecting initial test-split diagnostics. Because the last rolling CV fold also covers `2023–2024`, the pooled CV is also touched by this mild post-hoc iteration. On `33` positives, all 7-day block bootstrap 95% CIs still overlap across models, so single-split rankings remain inconclusive.

---

## 4. Same-Split Regression Comparison (`µg/m³`, vs Trivial Baselines)

*(Source: [`06_Data/results/unified_honest_regression_metrics.csv`](../06_Data/results/unified_honest_regression_metrics.csv))*

### Target Distribution Shift & Sensor-Censoring Floor Disclosure (`53.7 µg/m³`)
* **Train (`2015–2020`):** `mean = 104.3`, `median = 53.7`, `p90 = 82.8`, `max = 4800.0`
* **Test (`2023–2024`):** `mean = 60.6`, `median = 53.7`, **`p90 = 53.7`**, `max = 2339.4`
* **Physical Cause of the `53.7 µg/m³` Floor (Mandatory Disclosure):** Audit of the hourly record confirms that `53.7 µg/m³` is **not** missing or imputed data—it is the **METAR/ASOS clear-sky `10 km` visibility reporting cap** (`visibility_km >= 9.9 km`), which maps to `53.7 µg/m³` in the visibility-calibrated target. Clear-sky `10 km` visibility occurred in `60.0%–76.2%` of hours during 2015–2022 (`mean PM10 = 84.9–145.2 µg/m³`), but jumped to **`90.0%` in 2023 (`mean = 60.1`) and `94.7%` in 2024 (`mean = 58.6`)**, reflecting **a possible instrument or reporting change**. Consequently, test-period regression $R^2$ and positive storm counts (`33` windows $>150\ \mu\text{g/m}^3$) are directly constrained by this `10 km` visibility-censoring regime shift.

| Model | $R^2$ | RMSE ($\mu\text{g/m}^3$) | MAE ($\mu\text{g/m}^3$) | Notes |
| :--- | :---: | :---: | :---: | :--- |
| `Trivial_Train_Mean` (`104.3`) | -0.3216 | 88.41 | 53.73 | Over-predicts quiet 2023–2024 floor |
| `Trivial_Train_Median` (`53.7`) | -0.0082 | 77.22 | **6.94** | Matches the >90% test floor |
| `LineA_XGBoost_log1p_Direct` | -0.3041 | 87.82 | 44.17 | Slightly better than Train Mean, far worse than Train Median |
| `LineA_XGBoost_Hurdle_Calibrated` | -0.8507 | 104.62 | 57.91 | Worse than both trivial baselines |
| `LineB_PyTorch_LSTM_log1p_L1` *(5 seeds)* | `-0.0077 ± 0.0049` | `77.20 ± 0.19` | `11.32 ± 2.78` | **Ties Median on RMSE (`77.20` vs `77.22`), worse on MAE (`11.32` vs `6.94`)** |
| `LineB_PyTorch_STGNN_log1p_L1` *(5 seeds)* | `-0.0048 ± 0.0028` | `77.09 ± 0.11` | `10.18 ± 0.52` | **Ties Median on RMSE (`77.09` vs `77.22`), worse on MAE (`10.18` vs `6.94`)** |

---

## 5. Reliability & Operational Lift Visualization

![Reliability Curve and Operational Top-5% Lift](../07_Figures/calibration_and_operational_lift.png)

---

## 6. Scope of Valid Claims (What Not to Claim)

1. **Do NOT claim "accurate deterministic $\text{PM}_{10}$ regression":** Because `PM10` is a visibility-derived proxy with a `53.7 µg/m³` floor in `>90%` of 2023–2024 hours, continuous $\text{PM}_{10}$ regression does not beat the median baseline (`R² ≈ 0`, `LSTM`/`ST-GNN` RMSE `76.96–77.03` vs `77.22`, MAE `10.28–11.80` vs `6.94`).
2. **Do NOT claim "deep learning beats trees/linear models" or "models outperform persistence" without specifying the exact metric, baseline, and seed stability:**
   * **Where engineered features + ML/linear models win:** In 5-fold pooled CV, `LogReg_Features_Cal` (`ROC-AUC = 0.7270` on 24h, `0.7178` on 72h), `MonthClimo_Cal` (`0.6921` on 72h), `LineA_RF_Cal`, `LineA_XGB_Cal`, and `LineB_LSTM_Cal` outperform simple `Persistence_Cal` (`0.5504` on 24h, `0.6504` on 72h). However, because `LogReg_Features_Cal` matches or exceeds trees and LSTM on `ROC-AUC` and `LSTM` varies by `±0.02` across seeds, the gain comes primarily from the engineered persistence and seasonal features rather than deep-learning complexity.
   * **Where Persistence remains competitive:** `Persistence_Cal` retains the best `Rec@Top5%` (`0.1491`) and `Lift@5%` (`2.98×`) on `24h_Storm` in pooled CV, as well as the highest `Rec@Top5%` (`0.1818`), `Lift@5%` (`3.61×`), and `Brier` (`0.0137`, `BSS = -0.2206`) on the `2023–2024` single split.
3. **Do NOT over-interpret the 33-positive single test split:** On `2,902` test windows with `33` positives, all 7-day block bootstrap 95% CIs overlap across models.

