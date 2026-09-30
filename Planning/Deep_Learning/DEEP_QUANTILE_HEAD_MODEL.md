# 🎯 Deep Quantile Regression Head: Technical Specification & Parameter Guide
### *Multi-Lead Monotonic Uncertainty Envelopes ($P_{10}, P_{50}, P_{90}$) with Guaranteed Non-Crossing*
**Model Family:** Deep Quantile Neural Regression & Non-Parametric Uncertainty Quantification  
**Implementation:** `torch.nn.Module` (Integrated in `DustMLUnifiedDeepModel`)  
**File Location in Codebase:** [`Ai Pipline/models/deep_learning/unified_model.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/deep_learning/unified_model.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
In multi-day extended-range forecasting ($3\text{--}15$ days), single-point predictions rapidly lose credibility as chaotic uncertainty expands. 

The **Deep Quantile Regression Head** directly outputs continuous **non-parametric prediction intervals** for every corridor node across all $L$ lead horizons:

$$\left[ \hat{\mathbf{Y}}_{P10}, \quad \hat{\mathbf{Y}}_{P50}, \quad \hat{\mathbf{Y}}_{P90} \right] \in \mathbb{R}^{B \times N \times L}$$

Where:
* **$\hat{\mathbf{Y}}_{P10}$:** Minimum guaranteed dust level ($90\%$ exceedance probability).
* **$\hat{\mathbf{Y}}_{P50}$:** Median expected trajectory.
* **$\hat{\mathbf{Y}}_{P90}$:** Worst-case severe hazard scenario ($10\%$ tail risk).

### 1.2 Mathematical Proof of Non-Crossing Monotonicity
Conventional unconstrained deep quantile heads frequently suffer from **quantile crossing** ($P_{10} > P_{50}$ or $P_{50} > P_{90}$), which violates probability axioms.

The DustML deep quantile head employs **cumulative softplus delta parametrization**:

$$\hat{y}_{P50} = \text{softplus}\left(\mathbf{W}_{50} \mathbf{h}_{\text{latent}} + \mathbf{b}_{50}\right)$$
$$\Delta_{10} = \text{softplus}\left(\mathbf{W}_{10} \mathbf{h}_{\text{latent}} + \mathbf{b}_{10}\right)$$
$$\Delta_{90} = \text{softplus}\left(\mathbf{W}_{90} \mathbf{h}_{\text{latent}} + \mathbf{b}_{90}\right)$$
$$\hat{y}_{P10} = \max\left(0.0, \ \hat{y}_{P50} - \Delta_{10}\right)$$
$$\hat{y}_{P90} = \hat{y}_{P50} + \Delta_{90}$$

Since $\text{softplus}(z) = \ln(1 + e^z) > 0$ strictly for all $z \in \mathbb{R}$:
$$\Delta_{10} > 0 \implies \hat{y}_{P10} \le \hat{y}_{P50}$$
$$\Delta_{90} > 0 \implies \hat{y}_{P50} \le \hat{y}_{P90}$$
$$\therefore 0 \le \hat{y}_{P10} \le \hat{y}_{P50} \le \hat{y}_{P90} \quad \forall (b, n, l) \quad \text{[Q.E.D.]}$$

---

## ⚙️ 2. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `in_features` | `int` | `64` | `64 - 256` | Input latent node feature dimensionality from fusion MLP. |
| `n_lead_times` | `int` | `6` | `1 - 15` | Number of simultaneous forward forecast lead steps (e.g. 24h, 72h, 120h, 168h, 240h, 360h). |
| `quantiles` | `list` | `[0.10, 0.50, 0.90]` | Fixed triplet | Evaluated cumulative probability levels. |
| `activation` | `str` | `'softplus'` | Fixed | Enforces strictly positive delta offsets and non-negative median concentrations. |

---

## 📐 3. Multi-Lead Pinball Loss Formulation

During training, the multi-lead quantile predictions are optimized against the joint Pinball Loss:

$$\mathcal{L}_{\text{quantile}} = \frac{1}{B \cdot N \cdot L} \sum_{b, n, l} \left[ \rho_{0.10}\left(y - \hat{y}_{P10}\right) + \rho_{0.50}\left(y - \hat{y}_{P50}\right) + \rho_{0.90}\left(y - \hat{y}_{P90}\right) \right]$$

Where:
$$\rho_\tau(u) = u \cdot (\tau - \mathbb{I}(u < 0))$$

---

## 📊 4. Quality & Calibration Telemetry

1. **Prediction Interval Coverage Probability (PICP):**
   $$\text{PICP} = \frac{1}{B \cdot N \cdot L} \sum \mathbb{I}\left(\hat{y}_{P10} \le y \le \hat{y}_{P90}\right) \times 100\% \quad (\text{Target} \ge 80.0\%)$$
2. **Mean Prediction Interval Width (MPIW):**
   $$\text{MPIW} = \frac{1}{B \cdot N \cdot L} \sum \left(\hat{y}_{P90} - \hat{y}_{P10}\right) \quad (\text{Sharpness})$$

---

## 💡 5. PyTorch Implementation Code

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DeepQuantileRegressionHead(nn.Module):
    def __init__(self, in_features=64, n_lead_times=6):
        super().__init__()
        self.p50_head = nn.Linear(in_features, n_lead_times)
        self.p10_offset_head = nn.Linear(in_features, n_lead_times)
        self.p90_offset_head = nn.Linear(in_features, n_lead_times)

    def forward(self, latent_nodes):
        """
        latent_nodes: [B, N, in_features]
        Returns: p10, p50, p90 each of shape [B, N, n_lead_times]
        """
        raw_p50 = F.softplus(self.p50_head(latent_nodes))
        p10_delta = F.softplus(self.p10_offset_head(latent_nodes))
        p90_delta = F.softplus(self.p90_offset_head(latent_nodes))

        p50 = raw_p50
        p10 = torch.clamp(p50 - p10_delta, min=0.0)
        p90 = p50 + p90_delta

        return {
            "p10": p10,
            "p50": p50,
            "p90": p90,
            "interval_width": p90 - p10
        }
```
