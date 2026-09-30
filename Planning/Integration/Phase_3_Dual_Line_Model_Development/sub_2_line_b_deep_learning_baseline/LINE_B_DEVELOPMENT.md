# 🌌 Phase 3 • Subfolder 2: Main Line B Deep Learning Baseline
### *Coupled AI-GAMFS Vision Encoder & Temporal Sequence Baseline Framework*
**Phase Horizon:** May 2026 – August 2026  
**Parent Phase:** Phase 3 (Dual-Line Model Development)

---

## 🎯 1. Operational Goal & Baseline Architectures

Phase 3.2 establishes the deep learning baseline for Main Line B before incorporating full PINN conservation constraints:
1. **Coupled AI-GAMFS Vision Encoder (`aigamfs_backbone.py`):** Trains the dual Conv2D encoders processing NWP fluid dynamics (`[B, 6, 16, 16]`) and satellite AOD rasters (`[B, 3, 32, 32]`) via cross-modal sigmoid gating.
2. **Temporal Sequence Baselines:** Compares standard LSTM, Temporal Convolutional Networks (TCN), and GRU modules over historical station sequences.
3. **Multi-Lead Monotonic Quantile Heads:** Tests softplus delta parametrization ($\hat{y}_{P10} \le \hat{y}_{P50} \le \hat{y}_{P90}$).

---

## 📐 2. Training Baseline Loss

$$\mathcal{L}_{\text{baseline}} = \mathcal{L}_{\text{Huber}}(y, \hat{y}) + \mathcal{L}_{\text{pinball}}(\tau=0.10, 0.50, 0.90)$$

Optimized with AdamW ($\text{lr}=10^{-3}$, weight decay $=10^{-4}$) and Cosine Annealing learning rate schedule over 20 epochs.

---

## 📋 3. Phase 3.2 Deliverables
* Converged checkpoint `models/checkpoints/line_b/baseline_dl.pth`.
* Baseline validation comparison showing deep features outperforming linear autoregressive baselines by $> 20\%$.
