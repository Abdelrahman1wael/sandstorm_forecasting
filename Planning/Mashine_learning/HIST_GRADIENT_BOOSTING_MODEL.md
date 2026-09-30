# 📊 HistGradientBoosting Regressor: Technical Specification & Parameter Guide
### *High-Performance Native Scikit-Learn Fallback with Automatic Missing Value Handling*
**Model Family:** Histogram-Based Gradient Boosted Decision Trees  
**Implementation:** `sklearn.ensemble.HistGradientBoostingRegressor`  
**File Location in Codebase:** [`Ai Pipline/models/machine_learning/line_a_ensemble.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/machine_learning/line_a_ensemble.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
While LightGBM and CatBoost are powerful specialized libraries, they require external compiled C++ binaries that can fail to build on restricted server environments or embedded meteorological field loggers.

The `HistGradientBoostingRegressor` serves as the **high-performance, dependency-free core engine** in Main Line A:
1. **Zero External Dependencies:** Built natively into standard Scikit-Learn.
2. **Native Missing Value Support:** In real-time atmospheric sensor feeds, ground monitors frequently experience intermittent data dropouts (sensor icing, battery failure, telemetry disconnects). HistGradientBoosting bins missing values (`NaN`) into dedicated separate bins during training and inference, **eliminating the need for fragile runtime imputation**.
3. **Optimized for Hundreds of Thousands of Samples:** Pre-bins continuous features into 256 integer bins, reducing split evaluations from $O(N)$ to $O(\text{n\_bins})$, matching LightGBM's speed while maintaining pure Python compatibility.

---

## 📐 2. Mathematical Objective Function

HistGradientBoosting builds an ensemble of $M$ regression trees minimizing squared error or Huber loss:

$$\mathcal{L} = \sum_{i=1}^N \frac{1}{2}\left(r_i - \hat{r}_i\right)^2 + \frac{\lambda}{2} \sum_{j=1}^T w_j^2$$

Where:
* At each split, candidate thresholds are restricted to the 256 precomputed histogram bin edges.
* Missing values ($x_{i, j} = \text{NaN}$) are assigned to whichever branch (left or right) minimizes the split variance criterion during tree training.

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `max_iter` | `int` | `150` | `100 - 300` | Number of sequential gradient boosting iterations. |
| `learning_rate` | `float` | `0.05` | `0.02 - 0.10` | Learning rate shrinkage ($\eta$). |
| `max_leaf_nodes` | `int` | `31` | `15 - 63` | Maximum leaves per tree. Controls model expressiveness. |
| `max_depth` | `int` | `6` | `4 - 8` | Maximum tree depth. `None` allows expansion up to `max_leaf_nodes`. |
| `min_samples_leaf` | `int` | `20` | `10 - 50` | Minimum samples required in terminal leaves. Prevents overfitting to sensor anomalies. |
| `l2_regularization`| `float` | `1.0` | `0.1 - 5.0` | $L_2$ shrinkage parameter on terminal leaf values. |
| `max_bins` | `int` | `255` | `128 - 255` | Maximum number of histogram bins. 255 allows 8-bit integer indexing (`uint8`). |
| `loss` | `str` | `'squared_error'` | `'squared_error'`, `'absolute_error'`, `'poisson'` | Loss function for residual training. |
| `early_stopping` | `bool / str` | `'auto'` | `'auto'`, `True` | Monitors validation score and halts training when loss plateaus for 10 iterations. |
| `random_state` | `int` | `42` | Any fixed seed | Reproducibility seed. |

---

## 📥 4. Input Features & Data Types

Processes 2D float32 or float64 NumPy matrices:
* Compatible directly with arrays containing `np.nan` values without throwing exceptions.
* Handles numerical wind speeds, geopotential heights, pressure, soil water, and satellite indices.

---

## 📤 5. Output Predictions & Post-Processing

* **Raw Residual:** $\Delta \hat{y} = f(\mathbf{x})$.
* **Corrected Non-Negative Concentration:**
  $$\hat{y}_{\text{corrected}} = \max\left(0.0, \ y_{\text{NWP}} + \Delta \hat{y}\right)$$

---

## 💡 6. Python Implementation Code

```python
from sklearn.ensemble import HistGradientBoostingRegressor
import numpy as np

class NativeHistBiasCorrector:
    def __init__(self, max_iter=150, learning_rate=0.05, max_depth=6, seed=42):
        self.model = HistGradientBoostingRegressor(
            max_iter=max_iter,
            learning_rate=learning_rate,
            max_depth=max_depth,
            min_samples_leaf=20,
            l2_regularization=1.0,
            random_state=seed,
            early_stopping=True
        )
        self.is_fitted = False

    def fit(self, X_train, y_obs_train, y_nwp_train):
        target_residual = y_obs_train - y_nwp_train
        self.model.fit(X_train, target_residual)
        self.is_fitted = True
        return self

    def predict(self, X, y_nwp):
        pred_residual = self.model.predict(X)
        corrected = y_nwp + pred_residual
        return np.maximum(0.0, corrected)
```
