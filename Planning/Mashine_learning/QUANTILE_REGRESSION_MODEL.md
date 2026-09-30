# 🎯 Quantile Regression Uncertainty Head: Technical Specification & Parameter Guide
### *Non-Parametric Prediction Intervals ($P_{10}, P_{50}, P_{90}$) with Guaranteed Monotonicity*
**Model Family:** Quantile Loss Regression & Uncertainty Quantification  
**Implementation:** `HistGradientBoostingRegressor(loss='quantile')` & PyTorch `DeepQuantileRegressionHead`  
**File Location in Codebase:** [`Ai Pipline/models/machine_learning/uncertainty_head.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/machine_learning/uncertainty_head.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
Deterministic single-value forecasts (e.g., *"Tomorrow PM10 will be $420 \ \mu\text{g/m}^3$"*) fail to communicate the chaotic uncertainty inherent in atmospheric systems beyond 72 hours.

The Quantile Regression Uncertainty Head provides **non-parametric prediction intervals** without assuming a Gaussian distribution (since dust concentrations exhibit extreme positive skewness and long Pareto tails):

$$\left[ \hat{y}_{P10}(s, t+L), \quad \hat{y}_{P50}(s, t+L), \quad \hat{y}_{P90}(s, t+L) \right]$$

Where:
* **$\hat{y}_{P10}$ (10th Percentile):** Conservative lower bound ($90\%$ confidence that observed dust will exceed this minimum).
* **$\hat{y}_{P50}$ (50th Percentile / Median):** Most probable deterministic trajectory.
* **$\hat{y}_{P90}$ (90th Percentile):** Severe risk scenario ($10\%$ worst-case tail risk for civil emergency mobilization).

### 1.2 Mathematical Non-Crossing Guarantee
In unconstrained models, independent estimation can cause **quantile crossing** ($\hat{y}_{P10} > \hat{y}_{P50}$ or $\hat{y}_{P50} > \hat{y}_{P90}$), an unphysical contradiction. This module implements:
1. **Algorithmic Post-Hoc Monotonic Sorting:** Enforcing sorting across tabular tree outputs.
2. **Cumulative Softplus Delta Parameterization (Deep Neural Head):** Structurally guaranteeing $0 \le P_{10} \le P_{50} \le P_{90}$ by construction.

---

## 📐 2. Mathematical Objective Function: The Pinball Check Loss

For a specified quantile $\tau \in (0, 1)$, the model minimizes the asymmetric **Pinball (Check) Loss**:

$$\mathcal{L}_\tau(y_i, \hat{y}_{\tau, i}) = \sum_{i=1}^N \rho_\tau\left(y_i - \hat{y}_{\tau, i}\right)$$

Where:
$$\rho_\tau(u) = u \cdot \left(\tau - \mathbb{I}(u < 0)\right) = \begin{cases} \tau \cdot u, & \text{if } u \ge 0 \quad (\text{Underestimation}) \\ (\tau - 1) \cdot u = (1 - \tau) |u|, & \text{if } u < 0 \quad (\text{Overestimation}) \end{cases}$$

### Loss Dynamics across Quantiles:
* For $\tau = 0.90$ ($P_{90}$ Upper Bound):
  * Underestimating a storm ($y_i > \hat{y}$) is penalized with weight **$0.90$**.
  * Overestimating ($y_i < \hat{y}$) is penalized with weight **$0.10$**.
  * *Result: Forces the prediction upward until $90\%$ of observations lie below $\hat{y}_{P90}$.*
* For $\tau = 0.10$ ($P_{10}$ Lower Bound):
  * Underestimating is penalized with weight **$0.10$**.
  * Overestimating is penalized with weight **$0.90$**.
  * *Result: Forces the prediction downward until only $10\%$ of observations fall below $\hat{y}_{P10}$.*

---

## ⚙️ 3. Complete Parameter Dictionary

### 3.1 Tabular Tree Quantile Estimator (`QuantileUncertaintyEstimator`)
| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `quantiles` | `list[float]` | `[0.10, 0.50, 0.90]` | Fixed operational triplet | Target cumulative probability quantiles bounding the $80\%$ confidence envelope. |
| `max_iter` | `int` | `120` | `80 - 250` | Maximum boosting iterations per quantile estimator. |
| `learning_rate` | `float` | `0.05` | `0.02 - 0.10` | Learning rate shrinkage. |
| `max_depth` | `int` | `5` | `4 - 7` | Tree depth constraint. |
| `min_samples_leaf` | `int` | `20` | `15 - 50` | Minimum samples in leaf. Higher values stabilize extreme tail quantile estimates. |
| `l2_regularization`| `float` | `1.0` | `0.1 - 5.0` | $L_2$ leaf weight regularization. |
| `random_state` | `int` | `42` | Any fixed seed | Reproducibility seed. |

### 3.2 Deep Quantile Neural Head (`DeepQuantileRegressionHead`)
| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `in_features` | `int` | `64` | `64 - 256` | Dimensionality of input latent embeddings from ST-GNN or AI-GAMFS backbone. |
| `hidden_dim` | `int` | `64` | `32 - 128` | Width of intermediate dense layers. |
| `n_lead_times` | `int` | `6` | `1 - 15` | Number of forward forecast lead times evaluated simultaneously. |
| `dropout` | `float` | `0.10` | `0.05 - 0.20` | Regularization dropout rate on hidden activations. |

---

## 🔒 4. Monotonic Non-Crossing Architecture (PyTorch)

```python
class DeepQuantileRegressionHead(nn.Module):
    """
    Guarantees: 0 <= P10 <= P50 <= P90 strictly without crossing.
    """
    def __init__(self, in_features=64, hidden_dim=64, n_lead_times=6):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU()
        )
        self.p50_head = nn.Linear(hidden_dim, n_lead_times)
        self.delta_10_head = nn.Linear(hidden_dim, n_lead_times)
        self.delta_90_head = nn.Linear(hidden_dim, n_lead_times)

    def forward(self, x):
        h = self.shared(x)
        
        # Median is strictly positive (dust cannot be negative)
        p50 = F.softplus(self.p50_head(h))
        
        # Positive deltas guaranteed via Softplus
        delta_10 = F.softplus(self.delta_10_head(h))
        delta_90 = F.softplus(self.delta_90_head(h))
        
        # Construct non-crossing quantiles:
        p10 = torch.clamp(p50 - delta_10, min=0.0)
        p90 = p50 + delta_90
        
        return p10, p50, p90
```

---

## 📊 5. Evaluation Metrics for Uncertainty

The quantile model is evaluated using two complementary metrics:

1. **Prediction Interval Coverage Probability (PICP):**
   $$\text{PICP} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}\left(\hat{y}_{P10, i} \le y_i \le \hat{y}_{P90, i}\right) \times 100\%$$
   *Target:* $\text{PICP} \ge 80.0\%$ (calibrated coverage).
2. **Mean Prediction Interval Width (MPIW):**
   $$\text{MPIW} = \frac{1}{N} \sum_{i=1}^N \left(\hat{y}_{P90, i} - \hat{y}_{P10, i}\right)$$
   *Target:* Minimize MPIW while maintaining $\text{PICP} \ge 80\%$ (sharpness).

---

## 💡 6. Python Implementation Code

Exemplar implementation from `Ai Pipline/models/machine_learning/uncertainty_head.py`:

```python
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

class QuantileUncertaintyEstimator:
    def __init__(self, quantiles=[0.10, 0.50, 0.90], max_iter=120, seed=42):
        self.quantiles = quantiles
        self.models = {}
        for q in self.quantiles:
            self.models[q] = HistGradientBoostingRegressor(
                loss="quantile",
                quantile=q,
                max_iter=max_iter,
                random_state=seed
            )

    def fit(self, X_train, y_train):
        for q, model in self.models.items():
            model.fit(X_train, y_train)
        return self

    def predict_quantiles(self, X):
        raw_preds = {q: model.predict(X) for q, model in self.models.items()}
        
        p10 = raw_preds[0.10]
        p50 = raw_preds[0.50]
        p90 = raw_preds[0.90]

        # Enforce non-crossing sorting across columns
        stacked = np.column_stack([p10, p50, p90])
        sorted_stacked = np.sort(stacked, axis=1)

        return {
            "p10": np.maximum(0.0, sorted_stacked[:, 0]),
            "p50": np.maximum(0.0, sorted_stacked[:, 1]),
            "p90": np.maximum(0.0, sorted_stacked[:, 2]),
            "interval_width": sorted_stacked[:, 2] - sorted_stacked[:, 0]
        }
```
