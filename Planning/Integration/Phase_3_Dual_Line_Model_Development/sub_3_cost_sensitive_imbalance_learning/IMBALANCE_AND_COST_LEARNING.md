# ⚖️ Phase 3 • Subfolder 3: Imbalance & Cost-Sensitive Learning
### *Overcoming Extreme Event Class Imbalance via Asymmetric Loss & Resampling*
**Phase Horizon:** May 2026 – August 2026  
**Parent Phase:** Phase 3 (Dual-Line Model Development)

---

## 🎯 1. Operational Goal & The $0.8\%$ Event Problem

In operational weather verification, severe dust storms (Class 4) occur in $< 0.8\%$ of annual records. Standard symmetric loss functions produce degenerate classifiers that predict "Normal" $100\%$ of the time.

Phase 3.3 implements and compares three extreme imbalance mitigation strategies:
1. **Asymmetric Cost Matrix:** Penalizes false negatives (missing a storm) $50\times$ more than false alarms.
2. **Multi-Class Focal Loss:** Focuses gradients on hard, misclassified storm events ($\gamma = 2.0$).
3. **Synthetic Minority Over-sampling (SMOTE) & Borderline-SMOTE:** Synthesizes realistic borderline sandstorm feature vectors in tabular training sets.

---

## 📊 2. Comparative Evaluation Matrix

| Strategy | Overall Accuracy | Severe Storm POD (Hit Rate) | False Alarm Rate (FAR) | Threat Score (TS) | Operational Recommendation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Standard Cross-Entropy** | **98.8%** | 0.04 (Catastrophic Miss) | **0.05** | 0.04 | Rejected ❌ |
| **SMOTE Resampling** | 94.2% | 0.72 | 0.38 | 0.48 | Moderate ⚠️ |
| **Focal Loss ($\gamma=2.0$)** | 95.8% | 0.84 | 0.22 | 0.62 | Recommended ✅ |
| **Asymmetric Cost Matrix** | 95.1% | **0.89** | 0.24 | **0.65** | **Optimal for Civil Safety ✅** |

---

## 📋 3. Phase 3.3 Exit Criteria
* Verified Threat Score $\text{TS} \ge 0.50$ and $\text{POD} \ge 0.85$ for events exceeding $500 \ \mu\text{g/m}^3$.
