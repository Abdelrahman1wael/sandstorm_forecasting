# 🚀 XGBoost Regressor: Technical Specification & Parameter Guide
### *Extreme Gradient Boosted Decision Trees for Non-Linear Atmospheric Residuals*
**Model Family:** Gradient Boosted Decision Trees (GBDT)  
**Implementation:** `xgboost.XGBRegressor`  
**File Location in Codebase:** [`Ai Pipline/models/machine_learning/`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/machine_learning/)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
XGBoost provides a **high-precision second-order optimization engine** designed to capture complex non-linear meteorological residuals that lower-order algorithms miss. 

In Main Line A, XGBoost is deployed to model:
1. **Severe Frontal Gradient Errors:** During intense cold-air surges from Siberia across the Mongolian Plateau, raw NWP models often misplace the exact frontal boundary by 50–150 km. XGBoost's exact second-order Taylor expansion enables aggressive split finding along steep atmospheric baroclinic gradients.
2. **Multi-Model Stacking Pillar:** Serves as one of the three primary tree estimators in the stacking meta-learner alongside LightGBM and CatBoost, providing orthogonal error diversity.

The operational prediction is formulated as:
$$\Delta \hat{y}_{\text{XGBoost}}(s, t, L) = \sum_{k=1}^K f_k(\mathbf{x}_i)$$
$$\hat{y}_{\text{final}}(s, t+L) = \max\left(0.0, \ y_{\text{NWP}}(s, t+L) + \Delta \hat{y}_{\text{XGBoost}}(s, t, L)\right)$$

---

## 📐 2. Mathematical Objective Function

XGBoost evaluates both the first-order gradient ($g_i$) and second-order Hessian ($h_i$) of the loss function at each step:

$$\mathcal{L}^{(t)} \approx \sum_{i=1}^N \left[ \ell(r_i, \hat{r}_i^{(t-1)}) + g_i f_t(\mathbf{x}_i) + \frac{1}{2} h_i f_t^2(\mathbf{x}_i) \right] + \Omega(f_t)$$

Where:
* First-order gradient: $g_i = \partial_{\hat{r}^{(t-1)}} \ell(r_i, \hat{r}^{(t-1)})$
* Second-order Hessian: $h_i = \partial^2_{\hat{r}^{(t-1)}} \ell(r_i, \hat{r}^{(t-1)})$
* Tree Complexity Penalty:
  $$\Omega(f_t) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2 + \alpha \sum_{j=1}^T |w_j|$$

### Optimal Leaf Weight Solution:
For a given leaf $j$ containing sample set $I_j$, the optimal continuous weight $w_j^*$ is computed in closed form:
$$w_j^* = -\frac{\sum_{i \in I_j} g_i}{\sum_{i \in I_j} h_i + \lambda}$$

### Split Evaluation Criterion (Gain):
A split from node $I$ into left child $I_L$ and right child $I_R$ is accepted if:
$$\text{Gain} = \frac{1}{2} \left[ \frac{\left(\sum_{i \in I_L} g_i\right)^2}{\sum_{i \in I_L} h_i + \lambda} + \frac{\left(\sum_{i \in I_R} g_i\right)^2}{\sum_{i \in I_R} h_i + \lambda} - \frac{\left(\sum_{i \in I} g_i\right)^2}{\sum_{i \in I} h_i + \lambda} \right] - \gamma > 0$$

Where $\gamma$ acts as the minimum gain threshold required to justify splitting a leaf, preventing unnecessary tree partitioning on minor sensor fluctuations.

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning in DustML |
| :--- | :---: | :---: | :---: | :--- |
| `n_estimators` | `int` | `150` | `100 - 400` | Number of sequential gradient trees. |
| `learning_rate` | `float` | `0.05` | `0.01 - 0.10` | Shrinkage factor ($\eta$). Scales each tree's leaf weights after boosting step to control variance. |
| `max_depth` | `int` | `6` | `4 - 8` | Maximum tree depth. Controls maximum interaction order among weather features. |
| `min_child_weight`| `float` | `3.0` | `1.0 - 10.0` | Minimum sum of instance Hessian ($h_i$) required in a child. Higher values stop trees from splitting on rare sensor noise. |
| `gamma` | `float` | `0.10` | `0.0 - 1.0` | Pseudo-regularization threshold ($\gamma$). A node is only split if the loss reduction exceeds $\gamma$. |
| `subsample` | `float` | `0.80` | `0.60 - 0.90` | Subsample ratio of training instances before growing trees. Prevents overfitting to specific synoptic seasons. |
| `colsample_bytree`| `float` | `0.80` | `0.60 - 0.90` | Subsample ratio of columns per tree. Prevents dominant wind variables from masking auxiliary soil moisture features. |
| `colsample_bylevel`| `float`| `0.80` | `0.60 - 1.00` | Subsample ratio of columns for each level/depth split. |
| `reg_alpha` | `float` | `0.10` | `0.0 - 5.0` | $L_1$ Lasso regularization term on leaf weights. Encourages sparsity. |
| `reg_lambda` | `float` | `1.50` | `0.5 - 10.0` | $L_2$ Ridge regularization term on leaf weights. Prevents extreme weight values in leaves with few samples. |
| `tree_method` | `str` | `'hist'` | `'hist'`, `'approx'` | Tree construction algorithm. `'hist'` bins continuous features, drastically accelerating multi-station training. |
| `objective` | `str` | `'reg:squarederror'`| `'reg:squarederror'`, `'reg:pseudohubererror'` | Loss function for residual training. |
| `random_state` | `int` | `42` | Any fixed seed | Fixed seed for reproducibility. |
| `n_jobs` | `int` | `-1` | `-1` | Parallel CPU cores utilized. |

---

## 📥 4. Input Features & Data Types

The XGBoost model processes standardized float32 matrices:
* **Atmospheric Dynamic Grids:** 10m Wind Speed, 850 hPa Wind Velocity, 500 hPa Geopotential Height, Boundary Layer Height, Temperature Lapse Rate.
* **Surface Soil Parameters:** ERA5-Land Soil Moisture (0–7 cm, 7–28 cm), Roughness Length $z_0$, MODIS $\Delta\text{NDVI}$, Snow Cover Fraction.
* **Geographic Topography:** Station elevation, slope, aspect, distance to desert source corridors.
* **Temporal Indicators:** Cyclic day-of-year and hour-of-day harmonic coordinates, lead time $L$.

---

## 📤 5. Output Predictions & Post-Processing

* **Raw Prediction:** $\Delta \hat{y}_{\text{XGBoost}} \in (-\infty, +\infty)$ representing predicted NWP bias.
* **Non-Negativity Clipping:**
  $$\hat{y}_{\text{pred}} = \max\left(0.0, \ y_{\text{NWP}} + \Delta \hat{y}_{\text{XGBoost}}\right)$$

---

## 💡 6. Python Implementation Code

```python
import xgboost as xgb
import numpy as np

class XGBoostBiasCorrector:
    def __init__(self, n_estimators=150, learning_rate=0.05, max_depth=6, seed=42):
        self.model = xgb.XGBRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            min_child_weight=3.0,
            gamma=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.5,
            tree_method='hist',
            objective='reg:squarederror',
            random_state=seed,
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, X_train, y_obs_train, y_nwp_train, X_val=None, y_obs_val=None, y_nwp_val=None):
        target_residual_train = y_obs_train - y_nwp_train
        
        eval_set = None
        if X_val is not None:
            target_residual_val = y_obs_val - y_nwp_val
            eval_set = [(X_val, target_residual_val)]

        self.model.fit(
            X_train, 
            target_residual_train,
            eval_set=eval_set,
            verbose=False
        )
        self.is_fitted = True
        return self

    def predict(self, X, y_nwp):
        pred_residual = self.model.predict(X)
        corrected = y_nwp + pred_residual
        return np.maximum(0.0, corrected)
```
