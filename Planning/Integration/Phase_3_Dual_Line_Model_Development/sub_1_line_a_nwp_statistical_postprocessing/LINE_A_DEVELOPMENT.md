# 🌲 Phase 3 • Subfolder 1: Main Line A Model Development
### *NWP Statistical Post-Processing, Tree Ensemble Optimization & Quantile Calibration*
**Phase Horizon:** May 2026 – August 2026 (Month 9 – Month 12)  
**Parent Phase:** Phase 3 (Dual-Line Model Development)

---

## 🎯 1. Operational Goal & Model Suite

Phase 3.1 develops, tunes, and evaluates the Machine Learning Tree Ensemble models in Main Line A:
1. **LightGBM Regressor (`LGBMRegressor`):** Fast histogram-based bias correction on 72h–168h forecasts.
2. **CatBoost Regressor (`CatBoostRegressor`):** Evaluates station categorical embeddings across heterogeneous terrain.
3. **XGBoost Regressor (`XGBRegressor`):** Captures high-order non-linear frontal boundary shifts.
4. **Quantile Uncertainty Head:** Fits pinball loss across $\tau \in [0.10, 0.50, 0.90]$ with post-hoc sorting to prevent quantile crossing.

---

## ⚙️ 2. Hyperparameter Optimization Protocol

Using Bayesian Optimization via Optuna over 100 trials:
* `learning_rate`: Log-uniform $[0.01, 0.15]$
* `num_leaves`: Integer $[15, 63]$
* `subsample`: Uniform $[0.60, 0.95]$
* `colsample_bytree`: Uniform $[0.50, 0.90]$
* `reg_alpha` & `reg_lambda`: Log-uniform $[10^{-2}, 10.0]$

---

## 📋 3. Phase 3.1 Exit Criteria
* Line A reduces raw ECMWF Day 3 (72h) RMSE by **$\ge 30\%$** and Day 5 (120h) RMSE by **$\ge 25\%$**.
* Quantile Prediction Interval Coverage Probability (PICP) strictly achieves $\ge 80.0\%$.
