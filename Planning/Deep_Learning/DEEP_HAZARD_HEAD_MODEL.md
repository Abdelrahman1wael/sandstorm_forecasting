# 🚨 Deep Hazard Classification Head: Technical Specification & Parameter Guide
### *Multi-Lead 5-Tier CMA Sandstorm Warning Logits with Class-Weighted Focal Loss*
**Model Family:** Multi-Lead Multi-Class Neural Classifier  
**Implementation:** `torch.nn.Module` (Integrated in `DustMLUnifiedDeepModel`)  
**File Location in Codebase:** [`Ai Pipline/models/deep_learning/unified_model.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/deep_learning/unified_model.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
Municipal civil defense systems require direct probabilistic hazard tier assignments across extended lead times.

The **Deep Hazard Classification Head** simultaneously outputs classification logits across all nodes, lead horizons, and the 5 official CMA severity tiers:

$$\mathbf{Z}_{\text{hazard}} \in \mathbb{R}^{B \times N \times L \times 5}$$

Where:
* Class 0: **Normal Air Quality** ($\text{PM}_{10} < 150 \ \mu\text{g/m}^3$)
* Class 1: **Floating Dust (浮尘)** ($150 \le \text{PM}_{10} < 500$)
* Class 2: **Blowing Sand (扬沙)** ($500 \le \text{PM}_{10} < 1000$)
* Class 3: **Sand and Dust Storm (沙尘暴)** ($1000 \le \text{PM}_{10} < 2000$)
* Class 4: **Severe Sand and Dust Storm (强沙尘暴)** ($\text{PM}_{10} \ge 2000$)

---

## 📐 2. Mathematical Objective Function: Class-Weighted Focal Loss

Because Severe Dust Storms (Class 4) represent $< 0.8\%$ of data instances, standard cross-entropy loss causes the network to ignore rare extreme events. The head is trained using **Multi-Class Focal Loss**:

$$\mathcal{L}_{\text{focal}} = -\frac{1}{B \cdot N \cdot L} \sum_{b, n, l} \sum_{k=0}^4 \alpha_k \left(1 - p_k\right)^\gamma \log(p_k)$$

Where:
* $p_k = \frac{\exp(z_k)}{\sum_{j=0}^4 \exp(z_j)}$ is the Softmax probability for class $k$.
* $\gamma = 2.0$: The **focusing parameter**. Dynamically down-weights easy, well-classified normal days ($p_0 \approx 0.95 \implies (1 - p_0)^2 \approx 0.0025$), directing gradient updates toward misclassified storm days.
* $\alpha_k$: Class-balance weight vector prioritizing extreme hazards:
  $$\boldsymbol{\alpha} = [1.0, \ 3.0, \ 6.0, \ 15.0, \ 35.0]$$

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `in_features` | `int` | `64` | `64 - 128` | Latent node feature dimensionality from fusion MLP. |
| `n_lead_times` | `int` | `6` | `1 - 15` | Forward forecast horizons evaluated simultaneously. |
| `n_classes` | `int` | `5` | Fixed (5) | Number of CMA national warning levels. |
| `focal_gamma` | `float` | `2.0` | `1.5 - 3.0` | Focusing exponent down-weighting easy background air samples. |
| `alpha_severe` | `float` | `35.0` | `20.0 - 50.0` | Amplification weight on Class 4 severe dust storm cross-entropy. |

---

## 📤 4. Output Tensor Dimensions & Probabilities

* **Output Logits:** `hazard_logits` of shape `[B, N, n_lead_times, n_classes]`.
* **Normalized Alert Probabilities:**
  $$P(\text{Class } k \mid \text{Station } n, \text{Lead } l) = \text{Softmax}\left(\text{hazard\_logits}[:, n, l, :]\right)$$

---

## 💡 5. PyTorch Implementation Code

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class DeepHazardClassificationHead(nn.Module):
    def __init__(self, in_features=64, n_lead_times=6, n_classes=5):
        super().__init__()
        self.n_lead_times = n_lead_times
        self.n_classes = n_classes
        self.hazard_head = nn.Linear(in_features, n_lead_times * n_classes)

    def forward(self, latent_nodes):
        """
        latent_nodes: [B, N, in_features]
        Returns: logits of shape [B, N, n_lead_times, n_classes]
        """
        B, N, _ = latent_nodes.shape
        raw_logits = self.hazard_head(latent_nodes) # [B, N, Leads * Classes]
        logits = raw_logits.view(B, N, self.n_lead_times, self.n_classes)
        return logits


class MultiClassFocalLoss(nn.Module):
    def __init__(self, gamma=2.0, alpha_weights=[1.0, 3.0, 6.0, 15.0, 35.0]):
        super().__init__()
        self.gamma = gamma
        self.register_buffer("alpha", torch.tensor(alpha_weights, dtype=torch.float32))

    def forward(self, logits, targets):
        """
        logits: [B, N, Leads, 5]
        targets: [B, N, Leads] with integer labels 0..4
        """
        log_p = F.log_softmax(logits, dim=-1)
        p = torch.exp(log_p)

        target_one_hot = F.one_hot(targets, num_classes=5).float()
        pt = (p * target_one_hot).sum(dim=-1)
        log_pt = (log_p * target_one_hot).sum(dim=-1)
        alpha_t = (self.alpha * target_one_hot).sum(dim=-1)

        focal_loss = -alpha_t * ((1.0 - pt) ** self.gamma) * log_pt
        return focal_loss.mean()
```
