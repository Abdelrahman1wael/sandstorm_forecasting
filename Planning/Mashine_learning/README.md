# 🌲 Machine Learning Models Suite: Main Line A
### *NWP Statistical Post-Processing, Systematic Bias Correction & Uncertainty Quantification*
**Discipline:** Environmental Engineering (环境工程) • Atmospheric AI  
**Platform:** DustML Forecasting System (北京科技大学 • USTB)

---

## 🌟 Overview of Machine Learning Models

In the DustML architecture, **Main Line A** utilizes gradient boosted decision tree ensembles and statistical learning algorithms to correct systematic spatiotemporal errors in raw Numerical Weather Prediction (NWP) models (ECMWF-IFS and CMA-GFS).

This directory contains standalone, in-depth technical specifications for each individual machine learning model employed in Line A, detailing its mathematical objective, operational goal, comprehensive hyperparameters, and practical implementation.

---

## 📂 Model Directory Index

| Model Document | Model Type | Operational Goal in DustML | Key Strengths & Role |
| :--- | :--- | :--- | :--- |
| **[`LIGHTGBM_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Mashine_learning/LIGHTGBM_MODEL.md)** | Light Gradient Boosting Machine | Primary regressor for predicting NWP residual error: $\Delta y = y_{\text{obs}} - y_{\text{NWP}}$. | Ultra-fast histogram binning, GOSS sampling, low memory footprint, handles large tabular grids. |
| **[`XGBOOST_MODEL.md`](file:///c:/Planning/Mashine_learning/XGBOOST_MODEL.md)** | Extreme Gradient Boosting | High-precision 2nd-order Taylor expansion tree boosting for complex non-linear meteorological residuals. | Exact split finding, column subsampling, high numerical precision. |
| **[`CATBOOST_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Mashine_learning/CATBOOST_MODEL.md)** | Categorical Boosting | Robust spatial station learning preventing target leakage across discrete geographic coordinates. | Oblivious symmetric decision trees, native categorical encoding, compiled microsecond C++ inference. |
| **[`QUANTILE_REGRESSION_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Mashine_learning/QUANTILE_REGRESSION_MODEL.md)** | Pinball Quantile Regressor | Produces non-parametric prediction intervals ($P_{10}, P_{50}, P_{90}$) with guaranteed non-crossing monotonicity. | Directly bounds tail disaster risk; optimizes asymmetric pinball check loss. |
| **[`HAZARD_CLASSIFIER_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Mashine_learning/HAZARD_CLASSIFIER_MODEL.md)** | Cost-Sensitive Hazard Classifier | Predicts official CMA 5-tier sandstorm hazard categories under extreme class imbalance ($< 0.8\%$ storms). | Asymmetric cost matrix ($\text{Cost}_{\text{Miss}} = 50 \times \text{Cost}_{\text{FalseAlarm}}$), Isotonic probability calibration. |
| **[`HIST_GRADIENT_BOOSTING_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Mashine_learning/HIST_GRADIENT_BOOSTING_MODEL.md)** | Histogram Gradient Boosting | High-performance dependency-free fallback (Scikit-Learn native). | Native missing value support, built-in binning, zero external compiled dependencies. |
| **[`STACKING_ENSEMBLE_MODEL.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Mashine_learning/STACKING_ENSEMBLE_MODEL.md)** | Constrained Ridge Stacking Meta-Learner | Blends out-of-fold predictions from LightGBM, CatBoost, and XGBoost. | Non-negative weight constraint ($\sum w_k = 1, w_k \ge 0$), minimizes cross-validation variance. |
