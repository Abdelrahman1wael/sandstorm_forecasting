# 🌲 LightGBM Regressor: Technical Specification & Parameter Guide
### *Primary Numerical Weather Prediction (NWP) Residual Bias Correction Engine*
**Model Family:** Gradient Boosted Decision Trees (GBDT)  
**Implementation:** `lightgbm.LGBMRegressor`  
**File Location in Codebase:** [`Ai Pipline/models/machine_learning/line_a_ensemble.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/machine_learning/line_a_ensemble.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
The primary objective of the LightGBM model is to learn and predict the **systematic spatiotemporal residual error ($\Delta y$)** of raw Numerical Weather Prediction models (ECMWF-IFS and CMA-GFS):

$$\Delta y(s, t, L) = y_{\text{obs}}(s, t+L) - y_{\text{NWP}}(s, t+L)$$

Where:
* $y_{\text{obs}}$: True ground particulate concentration ($\text{PM}_{10}$ in $\mu\text{g/m}^3$) measured at station $s$.
* $y_{\text{NWP}}$: Raw uncorrected forecast produced by the numerical hydrodynamic model at lead time $L$.
* $\Delta y$: The systematic bias caused by coarse topography smoothing, unresolved orographic channeling, and idealized dust emission schemes.

The final corrected forecast is reconstructed as:
$$\hat{y}_{\text{corrected}}(s, t+L) = \max\left(0, \ y_{\text{NWP}}(s, t+L) + \Delta \hat{y}_{\text{LightGBM}}(s, t, L)\right)$$

### 1.2 Why LightGBM for Main Line A?
1. **High Computational Efficiency:** In operational weather services, predictions across 1,500+ Chinese ground stations must execute in sub-second time. LightGBM evaluates tens of thousands of station-hours in less than 20 milliseconds.
2. **Gradient-Based One-Side Sampling (GOSS):** Retains instances with large gradients (severe dust storm bias spikes) while randomly downsampling calm background days with small gradients.
3. **Exclusive Feature Bundling (EFB):** Compresses sparse meteorological and land-cover indicators into dense feature bundles without loss of accuracy.
4. **Leaf-Wise Tree Growth:** Expands the leaf with the maximum delta loss reduction, achieving higher precision on non-linear terrain-wind interactions than level-wise architectures.

---

## 📐 2. Mathematical Objective Function

LightGBM minimizes a regularized objective function combining Mean Squared Error (or Huber loss) with $L_1$ and $L_2$ leaf penalties:

$$\mathcal{L}^{(t)} = \sum_{i=1}^N \ell\left(r_i, \ \hat{r}_i^{(t-1)} + f_t(\mathbf{x}_i)\right) + \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2 + \alpha \sum_{j=1}^T |w_j|$$

Where:
* $r_i = y_{\text{true}, i} - y_{\text{NWP}, i}$: True numerical residual target.
* $f_t(\mathbf{x}_i)$: New decision tree added at iteration $t$.
* $T$: Number of terminal leaves in tree $f_t$.
* $w_j$: Continuous weight assigned to leaf $j$.
* $\lambda, \alpha$: $L_2$ (Ridge) and $L_1$ (Lasso) regularization parameters preventing overfitting to anomalous weather cycles.

Using a second-order Taylor expansion approximation:
$$\mathcal{L}^{(t)} \approx \sum_{i=1}^N \left[ g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2$$
Where $g_i = \partial_{\hat{r}} \ell(r_i, \hat{r})$ and $h_i = \partial^2_{\hat{r}} \ell(r_i, \hat{r})$.

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning in DustML |
| :--- | :---: | :---: | :---: | :--- |
| `n_estimators` | `int` | `150` | `100 - 500` | Number of sequential boosting trees. Higher values capture finer seasonal residuals but risk overfitting. |
| `learning_rate` | `float` | `0.05` | `0.01 - 0.10` | Step size shrinkage ($\eta$). Shrinks tree contributions to prevent dominance of isolated extreme storm events. |
| `num_leaves` | `int` | `31` | `15 - 63` | Maximum leaves per tree. Controls model complexity; kept $\le 2^{\text{max\_depth}}$ to avoid deep leaf overfitting. |
| `max_depth` | `int` | `6` | `4 - 8` | Maximum tree depth. Constrains high-order interaction complexity among meteorological predictors. |
| `subsample` | `float` | `0.80` | `0.60 - 0.90` | Row subsampling fraction (bagging). Randomly samples $80\%$ of training days per tree to increase generalization. |
| `subsample_freq`| `int` | `1` | `1 - 5` | Frequency for bagging. Evaluates a new random subsample at every boosting iteration. |
| `colsample_bytree`| `float` | `0.80` | `0.50 - 0.90` | Feature fraction per tree. Prevents surface wind speed ($U_{10}$) from masking subtle soil moisture signals. |
| `min_child_samples`| `int` | `20` | `10 - 50` | Minimum samples required in a terminal leaf. Prevents creating micro-leaves for rare single-station sensor noise. |
| `reg_alpha` | `float` | `0.10` | `0.0 - 5.0` | $L_1$ Lasso regularization on leaf weights. Encourages sparsity in feature split weights. |
| `reg_lambda` | `float` | `1.00` | `0.1 - 10.0` | $L_2$ Ridge regularization on leaf weights. Smooths predictions during extreme synoptic transitions. |
| `objective` | `str` | `'regression'` | `'regression'`, `'huber'` | Loss metric. `'regression'` (MSE) targets expected mean residual; `'huber'` is robust against sensor spikes. |
| `boosting_type`| `str` | `'gbdt'` | `'gbdt'`, `'goss'` | Boosting algorithm. `'gbdt'` uses standard sampling; `'goss'` accelerates training by downsampling small gradients. |
| `random_state` | `int` | `42` | Any fixed seed | Enforces deterministic reproducibility across multi-fold experimental runs. |
| `n_jobs` | `int` | `-1` | `-1` | Number of parallel CPU threads for histogram building. |

---

## 📥 4. Input Features & Data Types

The model ingests a 12-to-24 column tabular feature matrix $\mathbf{X} \in \mathbb{R}^{N \times D}$:

1. **`nwp_pm10` (float32, $\mu\text{g/m}^3$):** Baseline numerical prediction from ECMWF or CMA.
2. **`u10_wind_speed` (float32, $\text{m/s}$):** 10m surface horizontal wind velocity.
3. **`wind_gust` (float32, $\text{m/s}$):** Sub-grid scale turbulent gust.
4. **`z850_geopotential` (float32, $\text{gpm}$):** Lower tropospheric geopotential height tracking frontal boundaries.
5. **`z500_geopotential` (float32, $\text{gpm}$):** Planetary wave trough/ridge indicator (Siberian High tracking).
6. **`pbl_height` (float32, $\text{m}$):** Planetary boundary layer height controlling vertical mixing volume.
7. **`temp_lapse_rate` (float32, $\text{K/km}$):** Atmospheric static stability.
8. **`soil_moisture_l1` (float32, $\text{m}^3/\text{m}^3$):** Surface capillary moisture (0–7 cm).
9. **`ndvi_anomaly` (float32, dimensionless):** Normalized vegetation degradation vs 10-year climatology.
10. **`terrain_roughness` (float32, $\text{m}$):** Local DEM heterogeneity index.
11. **`dist_to_desert` (float32, $\text{km}$):** Distance along dominant wind trajectory to Taklamakan or Gobi margins.
12. **`lead_time_hours` (int32, hours):** Forecast horizon ($72, 120, 168, 240, 360$).
13. **`doy_sin` / `doy_cos` (float32):** Cyclical calendar encoding of spring dust storm seasonality.

---

## 📤 5. Output Predictions & Post-Processing

* **Raw Output:** Predicted residual bias $\Delta \hat{y} \in \mathbb{R}$ (can be positive or negative).
* **Physical Post-Processing:**
  $$\hat{y}_{\text{corrected}} = \max\left(0.0, \ y_{\text{NWP}} + \Delta \hat{y}\right)$$
  *Guarantees particulate matter concentration never drops below absolute physical vacuum ($0.0 \ \mu\text{g/m}^3$).*

---

## 💡 6. Python Implementation Code

Exemplar implementation from `Ai Pipline/models/machine_learning/line_a_ensemble.py`:

```python
import lightgbm as lgb
import numpy as np

class LightGBMBiasCorrector:
    def __init__(self, n_estimators=150, learning_rate=0.05, num_leaves=31, seed=42):
        self.model = lgb.LGBMRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            num_leaves=num_leaves,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=seed,
            n_jobs=-1,
            verbose=-1
        )
        self.is_fitted = False

    def fit(self, X_train, y_obs_train, y_nwp_train, X_val=None, y_obs_val=None, y_nwp_val=None):
        # Learn residual bias: residual = y_obs - y_nwp
        target_residual_train = y_obs_train - y_nwp_train
        
        eval_set = None
        if X_val is not None:
            target_residual_val = y_obs_val - y_nwp_val
            eval_set = [(X_val, target_residual_val)]

        self.model.fit(
            X_train, 
            target_residual_train,
            eval_set=eval_set,
            callbacks=[lgb.early_stopping(stopping_rounds=20, verbose=False)] if eval_set else None
        )
        self.is_fitted = True
        return self

    def predict(self, X, y_nwp):
        pred_residual = self.model.predict(X)
        corrected = y_nwp + pred_residual
        return np.maximum(0.0, corrected)
```
