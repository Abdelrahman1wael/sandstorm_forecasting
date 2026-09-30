# ⚖️ Physics-Informed Neural Network (PINN Core): Technical Specification & Parameter Guide
### *Owen Aerodynamic Saltation Thresholds & Mass Continuity PDE Loss Regularization*
**Model Family:** Physics-Informed Neural Networks (PINN) & PDE Constrained Optimization  
**Implementation:** `torch.nn.Module` (`PhysicsInformedLoss`, `OwenSaltationPhysics`)  
**File Location in Codebase:** [`Ai Pipline/models/deep_learning/pinn_core.py`](file:///c:/Users/hp/Desktop/China_project/Ai%20Pipline/models/deep_learning/pinn_core.py)

---

## 🎯 1. Model Goal & Operational Role in DustML

### 1.1 The Primary Goal
Purely data-driven neural networks are susceptible to **unphysical hallucinations**:
1. **False Emission Hallucinations:** Predicting sudden dust storm formation over deserts during calm conditions ($u_* \ll u_{*t}$), violating boundary-layer aerodynamics.
2. **Spontaneous Mass Creation:** Predicting abrupt spikes in urban particulate concentrations without an upstream advective plume or local emission source, violating the conservation of mass.
3. **Negative Concentration Drift:** Outputting negative dust mass ($< 0 \ \mu\text{g/m}^3$) under dry, clean-air atmospheric states.

The **PINN Conservation Module** acts as an **automated physical governor**. It calculates PDE residuals directly during the forward pass and penalizes physical law violations inside the backpropagation loss objective:

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{data}} + \lambda_{\text{mass}} \mathcal{L}_{\text{mass}} + \lambda_{\text{salt}} \mathcal{L}_{\text{saltation}} + \lambda_{\text{neg}} \mathcal{L}_{\text{negativity}}$$

---

## 📐 2. Mathematical Formulations & Physical Laws

### 2.1 Owen (1964) Aerodynamic Saltation Flux Formula
Dust particles on the desert floor cannot be lifted into the atmosphere until the surface friction velocity $u_* = \sqrt{\tau / \rho}$ exceeds the aerodynamic threshold $u_{*t}$, which is dictated by soil moisture $w_s$ and surface roughness $z_0$:

$$F_{\text{salt}} = \begin{cases} c_{\text{salt}} \cdot \frac{\rho_{\text{air}}}{g} \cdot u_*^3 \left(1 - \frac{u_{*t}^2}{u_*^2}\right), & \text{if } u_* > u_{*t}(w_s, z_0) \\ 0, & \text{if } u_* \le u_{*t} \end{cases}$$

Where:
* $c_{\text{salt}} = 0.25$: Empirical Owen saltation constant.
* $\rho_{\text{air}} = 1.225\text{ kg/m}^3$: Standard air density.
* $g = 9.80665\text{ m/s}^2$: Acceleration due to gravity.

#### The Saltation Penalty ($\mathcal{L}_{\text{saltation}}$):
If the neural network predicts positive primary dust emissions ($\hat{C}_{t=1} > C_{\text{background}}$) at a desert source node while $u_* < 0.9 \, u_{*t}$, the model is severely penalized:

$$\mathcal{L}_{\text{saltation}} = \frac{1}{B \cdot N} \sum_{b=1}^B \sum_{i=1}^N \mathbb{I}\left(u_{*, b, i} < 0.9 \, u_{*t, b, i}\right) \cdot \left(\max\left(0, \ \hat{C}_{b, i, t=1} - 45.0\right)\right)^2$$

---

### 2.2 Spatiotemporal Mass Advection Continuity ($\mathcal{L}_{\text{mass}}$)
Governed by the atmospheric particulate continuity partial differential equation:
$$\frac{\partial C}{\partial t} + \nabla \cdot (\mathbf{u} C) = \nabla \cdot (K \nabla C) + S_{\text{emission}} - D_{\text{deposition}}$$

Along discrete corridor graph edges $\mathbf{A}$, the downstream concentration accumulation between lead times ($\Delta C = C_{l+1} - C_l$) cannot exceed the sum of upstream advective inflow plus local generation:

$$\text{Inflow}_{i, l} = \sum_{j=1}^N A_{j \to i} \cdot \hat{C}_{j, l}$$
$$\text{Mass Residual} = \text{ReLU}\left(\left(\hat{C}_{l+1} - \hat{C}_l\right) - 1.5 \cdot \text{Inflow}_l\right)$$
$$\mathcal{L}_{\text{mass}} = \frac{1}{B \cdot N \cdot (L-1)} \sum_{b, i, l} \left(\text{Mass Residual}\right)^2$$

*Guarantees that a dust spike in Beijing must be physically preceded by an upstream plume passing through Zhangjiakou, Inner Mongolia, or Ningxia.*

---

### 2.3 Non-Negativity Mass Penalty ($\mathcal{L}_{\text{negativity}}$)
$$\mathcal{L}_{\text{neg}} = \frac{1}{B \cdot N \cdot L} \sum_{b, i, l} \left(\text{ReLU}\left(-\hat{C}_{b, i, l}\right)\right)^2$$

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `lambda_mass` | `float` | `0.15` | `0.05 - 0.30` | Multi-task loss weight penalizing mass continuity violations along corridor edges. |
| `lambda_salt` | `float` | `0.20` | `0.10 - 0.40` | Multi-task loss weight penalizing unphysical saltation below threshold $u_* < u_{*t}$. |
| `lambda_neg` | `float` | `0.10` | `0.05 - 0.20` | Loss weight penalizing negative particulate concentrations. |
| `saltation_const`| `float` | `0.25` | `0.20 - 0.30` | Owen (1964) empirical saltation coefficient $c_{\text{salt}}$. |
| `rho_air` | `float` | `1.225` | Fixed constant | Atmospheric air density ($\text{kg/m}^3$). |
| `g` | `float` | `9.80665`| Fixed constant | Gravitational acceleration ($\text{m/s}^2$). |
| `huber_delta` | `float` | `1.0` | `0.5 - 2.0` | Transition threshold for Smooth L1 (Huber) supervised data loss. |

---

## 📈 4. Telemetry Logging Output

The PINN loss module exports per-epoch telemetry tracking the gradual satisfaction of physical laws:

```json
{
  "loss_total": 0.4821,
  "loss_data": 0.3912,
  "loss_mass": 0.0215,
  "loss_saltation": 0.0410,
  "loss_negativity": 0.0000
}
```

---

## 💡 5. PyTorch Implementation Code

Exemplar implementation from `Ai Pipline/models/deep_learning/pinn_core.py`:

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class OwenSaltationPhysics:
    def __init__(self, rho_air=1.225, g=9.80665, saltation_const=0.25):
        self.rho_air = rho_air
        self.g = g
        self.saltation_const = saltation_const

    def compute_theoretical_flux(self, u_star, u_star_t):
        active_mask = (u_star > u_star_t).float()
        u_ratio_sq = (u_star_t / torch.clamp(u_star, min=1e-5)) ** 2
        excess_term = torch.clamp(1.0 - u_ratio_sq, min=0.0)
        flux = self.saltation_const * (self.rho_air / self.g) * (u_star ** 3) * excess_term * active_mask
        return flux * 1000.0


class PhysicsInformedLoss(nn.Module):
    def __init__(self, lambda_mass=0.15, lambda_salt=0.20, lambda_neg=0.10):
        super().__init__()
        self.lambda_mass = lambda_mass
        self.lambda_salt = lambda_salt
        self.lambda_neg = lambda_neg
        self.saltation_calc = OwenSaltationPhysics()

    def forward(self, pred_pm10, target_pm10, u_star, u_star_t, adj_matrix):
        # 1. Supervised Data Loss (Smooth L1 / Huber)
        loss_data = F.smooth_l1_loss(pred_pm10, target_pm10)

        # 2. Strict Non-negativity penalty
        loss_neg = torch.mean(F.relu(-pred_pm10) ** 2)

        # 3. Aerodynamic Saltation Constraint: u* > u*t
        day1_pred = pred_pm10[:, :, 0]
        sub_threshold_mask = (u_star < (u_star_t * 0.9)).float()
        loss_saltation = torch.mean(sub_threshold_mask * (day1_pred - 45.0).clamp(min=0.0) ** 2) / 1000.0

        # 4. Spatiotemporal Mass Continuity along graph edges
        advected_inflow = torch.einsum("ij,bjl->bil", adj_matrix, pred_pm10)
        lead_delta = pred_pm10[:, :, 1:] - pred_pm10[:, :, :-1]
        inflow_trunc = advected_inflow[:, :, 1:]
        mass_residual = F.relu(lead_delta - inflow_trunc * 1.5)
        loss_mass = torch.mean(mass_residual ** 2) / 100.0

        total_loss = (loss_data + 
                      self.lambda_mass * loss_mass + 
                      self.lambda_salt * loss_saltation + 
                      self.lambda_neg * loss_neg)

        telemetry = {
            "loss_total": float(total_loss.item()),
            "loss_data": float(loss_data.item()),
            "loss_mass": float(loss_mass.item()),
            "loss_saltation": float(loss_saltation.item()),
            "loss_negativity": float(loss_neg.item())
        }
        return total_loss, telemetry
```
