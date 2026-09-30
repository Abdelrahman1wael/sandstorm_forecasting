# ⚖️ Phase 4 • Subfolder 1: PINN Conservation Loss Integration
### *Embedding Owen Aerodynamic Saltation & Mass Conservation PDEs into Deep Training*
**Phase Horizon:** September 2026 – December 2026 (Month 13 – Month 16)  
**Parent Phase:** Phase 4 (Advanced Modeling and Mid-Term Review)

---

## 🎯 1. Operational Goal & Physics Integration

Phase 4.1 integrates the Physics-Informed Neural Network (PINN) loss regularizer (`pinn_core.py`) into the forward and backward passes of `DustMLUnifiedDeepModel`:

```
Forward Predictions: pred_pm10 [B, N, Leads]
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
[Owen Saltation Check]       [Mass Continuity Residual]
u* > u*t threshold            ||ΔC - Inflow_upstream||²
       │                               │
       └───────────────┬───────────────┘
                       ▼
         [Curriculum Loss Function]
  Loss = Huber + λ_mass*L_mass + λ_salt*L_salt + λ_neg*L_neg
                       │
                       ▼
          [Gradient Norm Clipping: max_norm = 2.0]
                       │
                       ▼
            [AdamW Optimizer Step]
```

---

## 📅 2. Curriculum Physics Scheduling

To prevent initial PDE gradients from destabilizing untrained weights, a 3-stage curriculum schedule is used:
* **Epochs 1–3 (Warm-Up):** $\lambda_{\text{mass}} = 0.00, \lambda_{\text{salt}} = 0.00$ (Model learns basic data manifold).
* **Epochs 4–8 (Physics Introduction):** Linearly ramp up $\lambda_{\text{mass}} \to 0.15$ and $\lambda_{\text{salt}} \to 0.20$.
* **Epochs 9–20 (Full PINN Enforcement):** Full conservation regularization with Cosine Annealing learning rate.

---

## 📋 3. Phase 4.1 Deliverables
* Zero negative concentration predictions ($\min \hat{y} \ge 0.0$).
* Aerodynamic saltation compliance rate strictly exceeding **$98.0\%$** across desert source nodes.
