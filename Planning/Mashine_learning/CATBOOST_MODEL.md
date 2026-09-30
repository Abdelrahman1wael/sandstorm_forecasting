# 🐱 CatBoost Regressor: Technical Specification & Parameter Guide
### *Categorical Boosting & Oblivious Symmetric Trees for Spatial Heterogeneity*
**Model Family:** Gradient Boosted Decision Trees (GBDT)  
**Implementation:** `catboost.CatBoostRegressor`  
**File Location in Codebase:** [`Ai Pipline/models/machine_learning/`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/machine_learning/)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
CatBoost is specialized to solve the **spatial categorical heterogeneity problem** inherent in regional meteorological sensor networks.

In northern China, ground stations are distributed across heterogeneous geographic biomes (Gobi desert margins, Loess Plateau ravines, agricultural plains, and megacities). When encoding station metadata (e.g., `station_id`, `province_code`, `soil_texture_class`, `land_cover_type`), standard One-Hot Encoding inflates feature dimensions, while Target Encoding causes severe **target leakage and overfitting**.

CatBoost solves this through **Ordered Target Statistics (TS)** and **Oblivious Decision Trees**, delivering:
1. **Target-Leakage-Free Spatial Encoding:** Dynamically encodes discrete station IDs based on random historical permutations without leaking future storm labels.
2. **Microsecond Inference via Symmetric Trees:** Uses oblivious trees where the exact same split condition is applied across an entire depth level. The resulting decision structure compiles into bitwise CPU operations, evaluating thousands of station forecasts in $< 10\text{ ms}$.

---

## 📐 2. Mathematical Objective Function

### 2.1 Ordered Boosting
Conventional gradient boosting uses the entire training dataset to calculate gradients for the next tree, introducing a prediction shift (gradient bias). CatBoost computes gradients using an **ordered principle**:
$$\mathbf{g}_i = \left. \frac{\partial \ell(r_i, \hat{r})}{\partial \hat{r}} \right|_{\hat{r} = \mathcal{M}_{i-1}(\mathbf{x}_i)}$$
Where $\mathcal{M}_{i-1}$ is a model trained strictly on instances appearing **before sample $i$** in a random permutation $\sigma$ of the training dataset.

### 2.2 Ordered Target Statistics for Categorical Features
For a categorical station or soil feature $x_{i, k}$, CatBoost computes continuous target statistics conditioned on the permutation order:
$$\hat{x}_{i, k} = \frac{\sum_{j \in \mathcal{P}_i} \mathbb{I}(x_{j, k} = x_{i, k}) \cdot r_j + a \cdot p}{\sum_{j \in \mathcal{P}_i} \mathbb{I}(x_{j, k} = x_{i, k}) + a}$$
Where:
* $\mathcal{P}_i$: The set of samples preceding sample $i$ in permutation $\sigma$.
* $p$: Prior average residual of the global dataset.
* $a > 0$: Smoothing prior parameter preventing single-observation bias.

### 2.3 Regularized Objective Function
$$\mathcal{L} = \sum_{i=1}^N \left(r_i - \hat{r}_i\right)^2 + \frac{\lambda}{2} \sum_{j=1}^{2^d} w_j^2$$
Where $d$ is tree depth, yielding exactly $2^d$ leaves for a symmetric tree.

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning in DustML |
| :--- | :---: | :---: | :---: | :--- |
| `iterations` | `int` | `200` | `100 - 500` | Number of sequential boosting rounds (equivalent to `n_estimators`). |
| `learning_rate` | `float` | `0.05` | `0.02 - 0.10` | Shrinkage step size ($\eta$) scaling tree weights. |
| `depth` | `int` | `6` | `4 - 8` | Depth of the oblivious symmetric tree ($2^{\text{depth}}$ leaves). |
| `l2_leaf_reg` | `float` | `3.0` | `1.0 - 10.0` | $L_2$ regularization coefficient on leaf values. Prevents extreme weights on rare station splits. |
| `border_count` | `int` | `128` | `64 - 254` | Number of quantization splits for continuous numerical features. |
| `random_strength`| `float` | `1.0` | `0.0 - 5.0` | Amount of randomness used for scoring splits. Helps escape local optima in complex atmospheric manifolds. |
| `bagging_temperature`| `float` | `1.0` | `0.0 - 2.0` | Controls Bayesian bootstrap intensity. `0.0` corresponds to no sampling (all weights 1.0). |
| `cat_features` | `list` | `None` | `['station_id', 'terrain_type']` | Explicit list of column indices or names treated as categorical. |
| `loss_function` | `str` | `'RMSE'` | `'RMSE'`, `'MAE'` | Optimization objective for residual error. |
| `random_seed` | `int` | `42` | Any fixed seed | Fixed seed for reproducible random permutations. |
| `thread_count` | `int` | `-1` | `-1` | Number of parallel threads. |
| `verbose` | `bool` | `False` | `False` | Suppresses iteration printouts during batch cross-validation. |

---

## 📥 4. Input Features & Data Types

* **Continuous Dynamic Meteorological Fields (float32):** Wind velocity, geopotential height, temperature lapse rate, soil moisture, vegetation anomaly.
* **Categorical Geographic Features (string / int):**
  * `station_code`: Identifier of the ground air quality station.
  * `province_code`: Administrative boundary (e.g., Gansu, Xinjiang, Inner Mongolia, Hebei).
  * `terrain_class`: Landform classification (Basin, Plateau, Mountain Pass, Desert Margin, Urban Plain).

---

## 📤 5. Output Predictions & Post-Processing

* **Predicted Residual:** $\Delta \hat{y}_{\text{CatBoost}} \in \mathbb{R}$.
* **Physically Bound Concentration:**
  $$\hat{y}_{\text{corrected}} = \max\left(0.0, \ y_{\text{NWP}} + \Delta \hat{y}_{\text{CatBoost}}\right)$$

---

## 💡 6. Python Implementation Code

```python
from catboost import CatBoostRegressor
import numpy as np

class CatBoostBiasCorrector:
    def __init__(self, iterations=200, learning_rate=0.05, depth=6, seed=42):
        self.model = CatBoostRegressor(
            iterations=iterations,
            learning_rate=learning_rate,
            depth=depth,
            l2_leaf_reg=3.0,
            border_count=128,
            loss_function='RMSE',
            random_seed=seed,
            thread_count=-1,
            verbose=False
        )
        self.is_fitted = False

    def fit(self, X_train, y_obs_train, y_nwp_train, cat_features=None, X_val=None, y_obs_val=None, y_nwp_val=None):
        target_residual_train = y_obs_train - y_nwp_train
        
        eval_set = None
        if X_val is not None:
            target_residual_val = y_obs_val - y_nwp_val
            eval_set = (X_val, target_residual_val)

        self.model.fit(
            X_train,
            target_residual_train,
            cat_features=cat_features,
            eval_set=eval_set,
            early_stopping_rounds=25,
            verbose=False
        )
        self.is_fitted = True
        return self

    def predict(self, X, y_nwp):
        pred_residual = self.model.predict(X)
        corrected = y_nwp + pred_residual
        return np.maximum(0.0, corrected)
```
