# 🏆 Phase 7 • Subfolder 1: Defense Materials & Oral Slides
### *Slide Decks, Committee Defense Speeches & Anticipated Q&A Bank*
**Phase Horizon:** June 2027 (Month 22)  
**Parent Phase:** Phase 7 (Final Defense, Graduation & Production)

---

## 🎯 1. Operational Goal & Defense Strategy

Phase 7.1 prepares the official oral defense materials for the Master's Degree Defense Committee:

### Core Defense Assets:
1. **Oral Defense PPT Slide Deck (30 Minutes, ~35 Slides):**
   * Slides 1–5: Research Problem & 3–15 Day Predictability Bottleneck
   * Slides 6–12: Multi-Source Harmonization & Data Cleaning
   * Slides 13–20: Dual-Line Architecture (Line A Trees + Line B PINN)
   * Slides 21–26: Empirical Benchmark vs ECMWF IFS & Skill Curves
   * Slides 27–30: March 2021 Case Study & SHAP Interpretability
   * Slides 31–33: Spatial GIS & Socioeconomic SEM Findings
   * Slides 34–35: Conclusions, Innovations & Academic Contributions
2. **Synchronized Video Presentation:** Master 1080p academic presentation video (`Media/production/sand_dust_storm_ml_presentation.mp4`) as demonstration backup.

---

## ❓ 2. Anticipated Committee Defense Q&A Bank

* **Q1: Why use PINN instead of standard data-driven deep learning?**  
  *Answer:* Standard deep networks hallucinate dust emissions under zero wind conditions because they memorize spurious statistical correlations. PINN explicitly penalizes predictions when friction velocity $u_* < u_{*t}$, ensuring $100\%$ physical compliance.
* **Q2: Why combine Line A and Line B rather than using a single model?**  
  *Answer:* Line A provides superior localized station bias correction at short lead times ($72\text{h}-120\text{h}$), while Line B captures planetary teleconnections and corridor advection at extended ranges ($168\text{h}-360\text{h}$). Adaptive blending yields lower RMSE across the entire 15-day spectrum than either model alone.

---

## 📋 3. Phase 7.1 Deliverables
* Final oral defense slide deck, synchronized presentation script, and high-resolution video demonstrations.
