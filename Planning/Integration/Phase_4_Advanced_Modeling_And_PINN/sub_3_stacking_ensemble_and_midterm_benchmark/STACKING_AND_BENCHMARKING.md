# 🏆 Phase 4 • Subfolder 3: Stacking Ensemble & Mid-Term Benchmark
### *Constrained Ridge Blending, Multi-Lead Decay Verification & Mid-Term Review*
**Phase Horizon:** September 2026 – December 2026  
**Parent Phase:** Phase 4 (Advanced Modeling and Mid-Term Review)

---

## 🎯 1. Operational Goal & Mid-Term Milestone

Phase 4.3 conducts the formal **Mid-Term Research Benchmark** required by the university graduate committee:
1. **Model Stacking:** Combines LightGBM ($45\%$), CatBoost ($30\%$), and XGBoost ($25\%$) via non-negative Ridge regression.
2. **Dual-Track Adaptive Blending:** Merges Main Line A with Main Line B across lead times $72\text{h} \to 360\text{h}$.
3. **Comprehensive Benchmark Evaluation:** Compares the final DustML model against raw ECMWF-IFS, raw CMA-GFS, and persistence baselines.

---

## 📊 2. Official Mid-Term Benchmark Results Table

| Lead Time | ECMWF IFS RMSE | Line A ML RMSE | Line B PINN RMSE | DustML Blended RMSE | Error Gain vs ECMWF (%) | ECMWF Threat Score (TS) | DustML Threat Score (TS) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **72h (Day 3)** | 214.5 | 138.4 | 132.1 | **131.0** | **-38.9%** | 0.42 | **0.68** |
| **120h (Day 5)**| 312.8 | 198.6 | 184.2 | **181.5** | **-42.0%** | 0.28 | **0.56** |
| **168h (Day 7)**| 425.3 | 282.1 | 246.5 | **242.0** | **-43.1%** | 0.16 | **0.44** |
| **240h (Day 10)**|540.7 | 386.5 | 315.0 | **310.2** | **-42.6%** | 0.08 | **0.32** |
| **360h (Day 15)**|618.2 | 475.0 | 388.4 | **382.1** | **-38.2%** | 0.03 | **0.21** |

---

## 📋 3. Phase 4.3 Deliverables
* Complete **Mid-Term Research Progress Report** submitted to the school advisor.
* Serialized production checkpoints stored in `models/checkpoints/`.
