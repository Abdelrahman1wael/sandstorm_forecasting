# 🌲 Main Line A: Machine Learning & Uncertainty Quantification Models

This module implements the **Main Line A** machine learning forecasting components, statistical bias correction ensembles, quantile uncertainty estimators, and cost-sensitive hazard classifiers for extended-range sand and dust storm prediction.

---

## 📂 Module Contents

| File | Primary Role & Class Names | Description |
| :--- | :--- | :--- |
| [`line_a_ensemble.py`](file:///c:/Users/hp/Desktop/China_project/Main%20project/models/machine_learning/line_a_ensemble.py) | `NWPBiasCorrectionEnsemble` | Gradient-boosted decision forest ensemble (LightGBM / HistGradientBoosting) learning systematic NWP residual biases ($y_{\text{true}} - y_{\text{NWP}}$). |
| [`uncertainty_head.py`](file:///c:/Users/hp/Desktop/China_project/Main%20project/models/machine_learning/uncertainty_head.py) | `QuantileUncertaintyEstimator`<br>`MLUncertaintyPipeline`<br>`PinballQuantileLoss`<br>`DeepQuantileRegressionHead` | Non-parametric quantile regression ($P_{10}, P_{50}, P_{90}$) and connectors for both Machine Learning and Deep Learning architectures. |
| [`hazard_classifier.py`](file:///c:/Users/hp/Desktop/China_project/Main%20project/models/machine_learning/hazard_classifier.py) | `CostSensitiveHazardClassifier` | 5-class severity classifier with cost-sensitive loss matrix penalizing false negatives for severe dust storms. |
| [`__init__.py`](file:///c:/Users/hp/Desktop/China_project/Main%20project/models/machine_learning/__init__.py) | Module Exports | Unified entry points for models and pipelines. |

---

## 🔗 Connecting Uncertainty Quantification

### 1. Connection to Machine Learning (`MLUncertaintyPipeline`)
Combines any standard point predictor (e.g. `NWPBiasCorrectionEnsemble`, LightGBM, Random Forest) with calibrated quantile prediction intervals.

```python
from sklearn.ensemble import HistGradientBoostingRegressor
from models.machine_learning import MLUncertaintyPipeline

# Initialize base regressor
base_model = HistGradientBoostingRegressor(max_iter=150, random_state=42)

# Wrap inside MLUncertaintyPipeline
pipeline = MLUncertaintyPipeline(
    base_regressor=base_model,
    quantiles=[0.10, 0.50, 0.90]
)

# Fit both models on training data
pipeline.fit(X_train, y_train)

# Inference emitting point forecasts and uncertainty intervals
predictions = pipeline.predict_with_uncertainty(X_test)
# Output keys: 'point_prediction', 'p10_lower_bound', 'p50_median', 'p90_upper_bound', 'interval_width_mpiw', 'uncertainty_category'
```

---

### 2. Connection to Deep Learning

#### Option A: Direct PyTorch Differentiable Head
Use `DeepQuantileRegressionHead` and `PinballQuantileLoss` for end-to-end gradient descent:

```python
import torch
import torch.nn as nn
from models.machine_learning import DeepQuantileRegressionHead, PinballQuantileLoss

class DeepModel(nn.Module):
    def __init__(self, in_features=64):
        super().__init__()
        self.encoder = nn.Linear(in_features, 64)
        # Monotonic output head: P10 <= P50 <= P90
        self.uncertainty_head = DeepQuantileRegressionHead(in_features=64, out_dim=1)

    def forward(self, x):
        h = torch.relu(self.encoder(x))
        return self.uncertainty_head(h)

model = DeepModel()
criterion = PinballQuantileLoss(quantiles=[0.10, 0.50, 0.90])
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# Forward pass
output = model(batch_x)
loss = criterion(output["quantiles_tensor"], batch_y)
loss.backward()
optimizer.step()
```

#### Option B: Post-Hoc Deep Latent Embeddings Bridge
Extract bottleneck features from a trained deep model (e.g. `DustMLUnifiedDeepModel.latent_nodes`) and fit the non-parametric estimator:

```python
from models.machine_learning import connect_dl_embeddings_to_uncertainty

# Pass deep representations into quantile estimator
estimator = connect_dl_embeddings_to_uncertainty(
    latent_embeddings=deep_features_numpy,
    y_true=y_train,
    quantiles=[0.10, 0.50, 0.90]
)

# Generate quantiles on test embeddings
test_quantiles = estimator.predict_quantiles(test_deep_features)
```

---

## 📊 Evaluation Metrics
Uncertainty predictions are evaluated using:
1. **PICP (Prediction Interval Coverage Probability):** Percentage of ground truth observations falling within $[P_{10}, P_{90}]$. Target: $\ge 80\%$.
2. **MPIW (Mean Prediction Interval Width):** Average spread $P_{90} - P_{10}$.
3. **Pinball Loss:** Quantile-specific loss measuring calibration and sharpness.
