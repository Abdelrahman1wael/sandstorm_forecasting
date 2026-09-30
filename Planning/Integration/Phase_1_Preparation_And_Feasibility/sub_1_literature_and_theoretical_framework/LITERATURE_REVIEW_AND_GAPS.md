# 📚 Phase 1 • Subfolder 1: Literature Review & Theoretical Framework
### *Extended-Range Predictability Gaps, Navier-Stokes Decay & AI Integration*
**Phase Horizon:** September 2025 – December 2025 (Month 1 – Month 4)  
**Parent Phase:** Phase 1 (Preparation and Feasibility)

---

## 🎯 1. Operational Goal & Research Questions

Phase 1 establishes the scientific rationale for replacing or augmenting traditional Numerical Weather Prediction (NWP) with artificial intelligence for sand and dust storm forecasting in East Asia:

### 1.1 Core Research Questions:
1. **The Predictability Barrier:** Why do numerical hydrodynamic models (ECMWF, CMA-GFS) experience rapid skill loss for dust aerosol transport between Day 3 (72h) and Day 15 (360h)?
2. **Empirical Parameterization Flaws:** Why do standard dust emission schemes (e.g., Ginoux, Kok, Shao) fail over dynamic spring thaw surfaces?
3. **The Physics-Data Synergy:** How can physics-informed constraints (Owen's saltation threshold and mass conservation PDEs) eliminate the unphysical hallucinations of pure deep learning?

---

## 🔬 2. Critical Literature Synthesis

| Research Theme | Key Literature & Authors | Major Scientific Findings | Research Gap Addressed by DustML |
| :--- | :--- | :--- | :--- |
| **Numerical Dust Modeling** | Chen et al. (2024), Benedetti et al. (2018) | Global NWP captures synoptic pressure troughs but underpredicts extreme dust concentrations by $40\text{--}65\%$ due to coarse topographic smoothing. | **Line A:** Applies gradient boosted decision trees to learn systematic orographic bias residuals. |
| **Machine Learning for PM & Dust** | Karimian et al. (2019), Huang et al. (2006) | Standard Random Forest and XGBoost achieve high $R^2$ at 24h lead time, but degrade without spatial correlation beyond 72h. | **Line B:** Introduces 14-node corridor ST-GNN to propagate spatial momentum across multi-day horizons. |
| **Physics-Informed Deep Learning** | Raissi et al. (2019), Owen (1964), Gillette (1979) | Pure neural networks predict impossible dust generation in zero wind. PINN loss constrains models to physical manifolds. | **PINN Core:** Enforces $u_* > u_{*t}$ aerodynamic saltation threshold and mass continuity PDEs. |
| **Socioeconomic Vulnerability** | Hayes (2018), Fornell & Larcker (1981) | Physical alerts are useless without public trust and behavioral compliance. | **Pillar 3:** Uses SPSS and AMOS SEM to model willingness-to-pay and compliance with municipal emergency alerts. |

---

## 📋 3. Phase 1.1 Checklist & Deliverables

- [x] Comprehensive review of 60+ peer-reviewed journal papers (cataloged in BibTeX format).
- [x] Formal mathematical definition of the 3-to-15 day predictability barrier.
- [x] Written Chapter 1 (Introduction) and Chapter 2 (Literature Review) for the master's research proposal.
- [x] Formal supervisor approval from the USTB Environmental Engineering graduate committee.
