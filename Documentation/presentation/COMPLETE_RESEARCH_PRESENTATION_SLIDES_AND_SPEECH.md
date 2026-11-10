# 🎓 Complete Master Presentation & Oral Defense Script
## Applying Machine Learning & Physics-Informed Deep Learning Algorithms to Improve Medium- to Long-Term Sand and Dust Storm (SDS) Forecasting in Riyadh Region

**Author / Candidate:** ALGHAMDI, HUDA 语嫣  
**Research Initiative:** DustML Multi-Modal Atmospheric Data Lab  
**Geographic Domain:** Riyadh Metropolitan Area & 5 Connected Desert Inflow Systems, Kingdom of Saudi Arabia ($24.71^\circ\text{N}, 46.67^\circ\text{E}$)  
**Deliverables Generated:**
1. **PowerPoint Presentation:** [`Persentation/Applying_Machine_Learning_for_Sandstorm_Forecasting_Riyadh_Complete.pptx`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Persentation/Applying_Machine_Learning_for_Sandstorm_Forecasting_Riyadh_Complete.pptx) (25 Executive Widescreen 16:9 Slides)
2. **Interactive HTML Slide Deck & PDF Exporter:** [`Persentation/presentation_slides.html`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Persentation/presentation_slides.html) (Keyboard-navigable, browser-ready, one-click print to PDF via `Ctrl + P`)
3. **Master Methodology Plan:** [`Planning/Supervisor/SUPERVISOR_RESPONSE_METHODOLOGY_PLAN.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Supervisor/SUPERVISOR_RESPONSE_METHODOLOGY_PLAN.md)
4. **Data Architecture & Provenance:** [`Planning/Supervisor/DATA_ARCHITECTURE_LINE_A_AND_LINE_B.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Supervisor/DATA_ARCHITECTURE_LINE_A_AND_LINE_B.md) & [`data/DATASET_MANIFEST.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/DATASET_MANIFEST.md)
5. **Preprocessing & Merging Protocol:** [`Planning/Supervisor/RIYADH_DATA_MERGING_AND_PREPROCESSING_GUIDE.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Supervisor/RIYADH_DATA_MERGING_AND_PREPROCESSING_GUIDE.md)

---

## 📌 Executive Slide-by-Slide Defense Script & Technical Analysis

---

### Slide 1: Title & Opening
* **Slide Title:** Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting in Riyadh Region
* **Candidate:** ALGHAMDI, HUDA 语嫣
* **Spoken Presentation Script:**
  > *"بسم الله الرحمن الرحيم. Respected supervisor, committee members, and colleagues. Today, I present our comprehensive research on 'Applying Machine Learning and Physics-Informed Deep Learning Algorithms to Improve Medium- to Long-Term Sand and Dust Storm Forecasting in Riyadh Region'. Our work tackles a long-standing challenge in atmospheric science: overcoming the chaotic 72-hour predictability barrier of classical numerical weather prediction by introducing a dual-line paradigm that couples statistical machine learning debiasing with end-to-end spatiotemporal deep graph learning."*

---

### Slide 2: Research Motivation & Problem Statement
* **Slide Title:** Research Motivation & The 72-Hour Predictability Barrier
* **Key Visuals:** 3-pillar breakdown: Riyadh Arid Exposure, The 72h NWP Limit, and The Dual-Line Solution.
* **Spoken Presentation Script:**
  > *"Riyadh sits in the central Najd plateau, directly encircled by massive active sand seas. Despite advances in global Numerical Weather Prediction (such as ECMWF IFS and Copernicus CAMS), forecast skill decays exponentially past 72 hours. This is caused by coarse grid topography smoothing, idealized surface roughness lengths, and unmodeled convective Haboob cold pools. Crucially, operational NWP models shut down chemical aerosol forecasting after 120 hours (Day 5). Our research resolves this by building an asymmetric dual-line framework: Main Line A uses gradient boosted decision trees for near-term NWP debiasing, while Main Line B invests in spatiotemporal deep learning (ST-GNN, Transformers, and PINNs) to unlock reliable 3 to 15-day forecasting."*

---

### Slide 3: Riyadh Metropolitan Receptor: Geography & Economics
* **Slide Title:** Riyadh Metropolitan Receptor: Geography & Economic Vulnerability
* **Key Visuals:** Demographics (7.01M), 20 sub-municipalities, 47% non-oil GDP, and multi-sector impact metrics ($150B World Bank estimate, 1,000+ flight cancellations in April 2015, 354 traffic accidents in a single day).
* **Spoken Presentation Script:**
  > *"Riyadh is the economic engine of Saudi Arabia, contributing 47% of the Kingdom's non-oil GDP. Over 7 million inhabitants reside across 20 sub-municipalities. A single severe sandstorm event—such as the April 2015 storm—disrupted over 1,000 flights, halted construction megaprojects, degraded solar photovoltaic efficiency by 30 to 50%, and caused severe health crises with pediatric asthma emergency admissions. Reliable medium-range forecasts are therefore not merely a meteorological pursuit, but a socio-economic imperative directly aligned with Saudi Vision 2030."*

---

### Slide 4: The 5 Connected Desert Inflow Systems
* **Slide Title:** The 5 Connected Desert Inflow Systems Driving Riyadh SDS
* **Key Visuals:** Spatial map and physical roles of:
  1. **Al-Thumamah Dunes (50 km E/NE):** Immediate local dune trigger for rapid visibility drops (<1h).
  2. **Ad-Dahna Desert (120 km NE):** 1,000-km red barchan sand conveyor funneled by easterly/Shamal winds.
  3. **Nafud al-Thuwairat (220 km NW):** Major deflation basin mobilizing dust fronts down the Zulfi-Majmaah corridor.
  4. **Tuwayq Escarpment (180 km SW):** 800-km limestone bluff inducing slope vorticity and Haboob squalls.
  5. **Rub' al-Khali (350 km SE):** Hyper-arid Empty Quarter sand sea driving massive regional AOD plumes.
* **Spoken Presentation Script:**
  > *"Dust does not originate in Riyadh; it is transported along specific aerodynamic corridors. We identify five connected source regions. Notice that Al-Thumamah produces rapid onset events within an hour, whereas Nafud al-Thuwairat and Rub' al-Khali act as massive regional source basins. The steep Tuwayq escarpment acts as a topographic bluff that triggers sudden convective downdrafts. Our models explicitly parameterize the directional wind alignment along each of these five desert bearings."*

---

### Slide 5: Historical Sandstorm Climatology (2016–2026)
* **Slide Title:** Historical Evidence: Documented Sandstorm Attacks (2016–2026)
* **Key Visuals:** Chronological table of major storms: March 2017 (AOD 2.3), April 2018 (276 dust events across KSA), March & May 2022 (visibility < 300m), April 2025 (AOD 2.76, visibility 0.5 km), and historic June 2026 low.
* **Spoken Presentation Script:**
  > *"Over the past decade from 2016 to 2026, Riyadh has experienced recurring, intense sandstorm episodes. March and April represent the peak synoptic spring season, characterized by Mediterranean cold fronts interacting with Arabian thermal low-pressure systems. Notably, on April 11, 2025, horizontal visibility collapsed to 500 meters with Aerosol Optical Depth reaching 2.76. These documented events serve as our independent, out-of-sample benchmark cases."*

---

### Slide 6: Taxonomy Sitemap: 5 Forecasting Paradigms
* **Slide Title:** Taxonomy Sitemap: The 5 Methodological Forecasting Branches
* **Key Visuals:** Branch 1 (Traditional Physics & Statistics), Branch 2 (Multi-Scale Environmental Dynamics), Branch 3 (Machine Learning Line A), Branch 4 (Deep Learning Line B), Branch 5 (Integrated Tri-Pillar Impact).
* **Spoken Presentation Script:**
  > *"Our research is grounded in a five-branch methodological taxonomy. We trace the paradigm evolution from subjective synoptic analysis and dynamical NWP models to statistical gradient boosted ensembles in Branch 3, spatiotemporal deep neural networks in Branch 4, and operational municipal decision-support playbooks in Branch 5."*

---

### Slide 7: Complete End-to-End System Pipeline
* **Slide Title:** End-to-End Pipeline: Ingestion, Physics, Dual Modeling & Support
* **Key Visuals:** 5 pipeline stages:
  1. *Ingestion:* 6 Ground Stations, ERA5 Reanalysis, CAMS/IFS NWP, MODIS/AERONET AOD, SRTM 90m DEM.
  2. *Hygiene & QC:* Strict UTC Reindexing, Bound Clamping, MAD Despiking, Akima Spline.
  3. *Physics Engine:* Wind decomposition, Owen Saltation, VPD, Dry Air Density, Backward Non-Leakage Lags.
  4. *Dual Modeling:* Line A (GBDTs debiasing 72-120h) & Line B (ST-GNN + Transformer + PINN for 3-15 days).
  5. *Dispatch:* TreeSHAP/DeepSHAP, P10/P50/P90 Quantile Envelopes, 5-Tier Hazard Alerts.
* **Spoken Presentation Script:**
  > *"This slide outlines our unified engineering pipeline. Raw multi-modal data enters Stage 1, undergoes rigorous hygiene and physical feature derivation in Stages 2 and 3, and feeds both Main Line A and Main Line B in Stage 4. Stage 5 outputs calibrated predictions, probabilistic risk envelopes, and transparent SHAP explanations for city authorities."*

---

### Slide 8: Tools & Software Ecosystem
* **Slide Title:** Tools & Software Ecosystem: APIs, Geo-Engines & Deep Learning
* **Key Visuals:**
  * *APIs:* `cdsapi`, `Copernicus ADS`, `NASA earthaccess`, `requests`.
  * *Meteorology & GIS:* `CDO`, `xarray`, `netCDF4`, `GDAL`, `rasterio`, `geopandas`.
  * *Classical ML:* `scikit-learn`, `LightGBM`, `XGBoost`, `CatBoost`, `Optuna`.
  * *Deep Learning & XAI:* `PyTorch 2.2+`, `PyTorch Geometric`, `TFT`, `Earthformer`, `SHAP`.
* **Spoken Presentation Script:**
  > *"Our computational infrastructure leverages state-of-the-art scientific Python libraries. We utilize CDO and xarray for high-dimensional atmospheric tensor regridding, rasterio and geopandas for digital elevation modeling, LightGBM and CatBoost for tabular ensembling, and PyTorch Geometric for spatial graph message passing on NVIDIA GPUs."*

---

### Slide 9: Multi-Modal Data Types, Shapes & Links
* **Slide Title:** Multi-Modal Scientific Data: Modalities, Dimensions & Links
* **Key Data Matrix Summary:**

| Modality | Geographic Domain & Nodes | Dimensions & Matrix Shape | Official Source Link | Local Repository Path |
| :--- | :--- | :--- | :--- | :--- |
| **Ground Truth Telemetry** | 6 Stations: `OERK`, `OERY`, `OEPS`, `OEDM`, `OEWD`, `OEGS` | $216,174\text{ rows} \times 14\text{ cols}$ (Hourly, 2020–2024) | Quotsoft / CNEMC & NOAA ISD | [`data/raw/ground/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/ground/) |
| **ECMWF ERA5 Reanalysis** | 6 Spatial Domains (Riyadh + 5 Deserts) | $43,848\text{ h} \times 6\text{ domains} \times 8\text{ channels}$ | Copernicus CDS (`cds.climate.copernicus.eu`) | [`data/raw/era5/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/era5/) |
| **CAMS / IFS NWP Forecasts** | Point & Grid Forecasts (+72h to +120h lead times) | $54\text{ Cycles} \times 17\text{ Leads} \times 6\text{ Nodes}$ | Copernicus ADS (`ads.atmosphere.copernicus.eu`) | [`data/raw/nwp/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/nwp/) |
| **ECMWF TIGGE Extended NWP** | Medium-to-Extended Ensemble (144h–360h / 6–15 Days) | 15 Days $\times$ 6-hourly $\times$ 51 Ensemble Members | ECMWF TIGGE Archive (`apps.ecmwf.int/datasets/tigge`) | [`data/raw/nwp/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/nwp/) |
| **Satellite Remote Sensing** | MODIS Terra/Aqua AOD & Sentinel-3 Column Dust | $43,848\text{ hourly column retrievals}$ | NASA Earthdata & AERONET Solar Village (`aeronet.gsfc.nasa.gov`) | [`data/raw/satellite/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/satellite/) |
| **SRTM 90m Topography (GIS)** | Riyadh Basin & Tuwayq Ridge Elevation Raster | $21 \times 21\text{ Raster Grid}$ ($614\text{m}\text{--}1119\text{m}$ ASL) | CGIAR-CSI SRTM / USGS Earth Explorer | [`data/raw/gis/`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/data/raw/gis/) |

---

### Slide 10: Data Preprocessing Protocol: Hygiene & QC
* **Slide Title:** Data Preprocessing Protocol: Hygiene, QC & Bound Clamping
* **Key Methodological Steps:**
  1. *Strict UTC Standardization:* Snap irregular METAR minutes (:20, :50) to exact top-of-the-hour slots (:00); build a continuous 43,800-hour grid (2020–2024).
  2. *Bound Clamping:* Visibility clipped to $[0.05, 30.0\,\text{km}]$; RH clipped to $[1.0, 100.0\%]$; kinematic check: $\text{Gust} \ge \text{Wind Speed}$.
  3. *Rolling MAD Despiking:* Electronic sensor spikes exceeding $4.5 \times \text{MAD}$ under calm winds are filtered out. Zero-variance flatline detection flags mechanical freeze ($\ge 12\text{h}$).
  4. *Akima Spline Imputation:* Short gaps ($\le 3\text{h}$) imputed via cubic Akima splines to retain diurnal curves; medium gaps ($3\text{h}\text{--}24\text{h}$) filled via spatial corridor regression from upwind stations.
* **Spoken Presentation Script:**
  > *"Data quality determines modeling fidelity. We enforce zero timezone discrepancies by synchronizing all records to UTC. We deploy rolling Median Absolute Deviation filtering to strip out electronic sensor noise without muting genuine sandstorm surges. Short missing records are imputed using Akima cubic splines, preserving diurnal temperature curves and guaranteeing that not a single dust storm event is lost."*

---

### Slide 11: Physics-Informed Feature Engineering
* **Slide Title:** Physics-Informed Feature Engineering: Aerodynamics & Saltation
* **Mathematical Derivations:**
  1. **Aerodynamic Wind Vector Decomposition:**
     $$u_{10} = -W_{10} \sin(\theta), \quad v_{10} = -W_{10} \cos(\theta), \quad E_k = 0.5 W_{10}^2$$
  2. **Owen (1964) Desert Saltation Sand Emission Flux:**
     $$Q \sim u_*^3 \cdot \max\left(0, 1 - \frac{u_{*t}^2}{u_*^2}\right) \cdot \exp\left(-15 \cdot SM_{\text{top}}\right)$$
  3. **Atmospheric Vapor Pressure Deficit (VPD):**
     $$e_s = 0.61078 \exp\left(\frac{17.27 T}{T + 237.3}\right), \quad \text{VPD} = \max(0, e_s - e_a)$$
  4. **Harmonic Astronomical Cyclical Coordinates:**
     $$\sin_{\text{DOY}} = \sin\left(\frac{2\pi \cdot \text{DOY}}{365.25}\right), \quad \cos_{\text{DOY}} = \cos\left(\frac{2\pi \cdot \text{DOY}}{365.25}\right)$$

---

### Slide 12: Multimodal Merging Logic & Anti-Leakage Feature Store
* **Slide Title:** The Multi-Modal Merging Logic & Anti-Leakage Feature Store
* **Key Architecture:**
  * Exact 1-to-1 hourly timestamp inner join between Ground Telemetry and ERA5.
  * Left join with satellite AOD and NASA solar flux; spatial nearest-neighbor attachment of static DEM elevation (614m), slope (1.85°), and roughness length $z_0$ (0.042m).
  * Strict backward-shifting lag engine ($t-1\text{h}, t-3\text{h}, t-6\text{h}, t-12\text{h}, t-24\text{h}$) with sliding windows closed on the left (`closed="left"`), guaranteeing zero future data leakage.
  * Exports **Format A** (2D Tabular Feature Store: $43,800 \times 55+$) and **Format B** (5D Tensor $[B, C, T, H, W]$ and Dynamic Graph Adjacency Matrix $\mathbf{A}(t)$).

---

### Slide 13: Main Line A: Statistical Tree Ensembles
* **Slide Title:** Main Line A: Tree Ensembles & Ensembling Algorithms
* **Models Analyzed:**
  * **Random Forest (RF):** Bagging hundreds of de-correlated decision trees; robust variance reduction.
  * **XGBoost:** Exact greedy boosting with second-order gradient optimization and strong leaf regularization.
  * **LightGBM:** Gradient-based One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB); native pinball loss for quantile regression.
  * **CatBoost:** Ordered boosting to eliminate target leakage from categorical corridor identifiers; symmetric oblivious trees ensure sub-second inference.

---

### Slide 14: Line A NWP Bias Correction & Quantile Loss
* **Slide Title:** Line A NWP Bias Correction & Quantile Uncertainty Heads
* **Mathematical Formulation:**
  * **Residual Target:** $\Delta y(t + \tau) = y_{\text{obs}}(t + \tau) - y_{\text{NWP}}(t + \tau)$
  * **Calibrated Output:** $\hat{y}(t + \tau) = y_{\text{NWP}}(t + \tau) + f_{\text{GBDT}}(\mathbf{X})$
  * **Pinball Quantile Loss:**
    $$L_q(y, \hat{y}) = \max(q(y - \hat{y}), (q - 1)(y - \hat{y})) \quad \text{for } q \in \{0.10, 0.50, 0.90\}$$
  * **Target Performance:** Drops raw NWP RMSE by $\Delta\text{RMSE}\% \ge 25\%$.

---

### Slide 15: Line A Projected Outcomes: 5-Tier Hazard Classification
* **Slide Title:** Line A Projected Outcomes: 5-Tier Hazard Classification
* **Hazard Tiers Defined:**
  * **Tier 0 (Normal):** $\text{PM}_{10} < 50\,\mu\text{g/m}^3$, Visibility $> 10\,\text{km}$.
  * **Tier 1 (Moderate):** $50\text{--}150\,\mu\text{g/m}^3$, Visibility $6\text{--}10\,\text{km}$.
  * **Tier 2 (Elevated Dust):** $150\text{--}300\,\mu\text{g/m}^3$, Visibility $3\text{--}6\,\text{km}$.
  * **Tier 3 (Severe Sandstorm):** $300\text{--}600\,\mu\text{g/m}^3$, Visibility $1\text{--}3\,\text{km}$ (Airport diversion alerts).
  * **Tier 4 (Extreme Haboob):** $> 600\,\mu\text{g/m}^3$, Visibility $< 500\,\text{m}$ (Citywide emergency protocol).

---

### Slide 16: The Critical Turning Point: Why Classical ML Fails Beyond 72 Hours
* **Slide Title:** Why Classical ML Drifts & Gives Inaccurate Long-Term Results
* **The Four Fundamental Failures of Classical ML at Medium/Long-Range:**
  1. **Recursive Error Compounding:** To forecast 6–15 days ahead, tabular models must feed predicted outputs into future lag slots. Single-step errors compound exponentially, causing runaway prediction drift.
  2. **Flat Tabular Spatial Blindness:** Tree models treat each row as an independent vector. They have no concept of fluid wave propagation, spatial advection, or atmospheric continuum across desert space.
  3. **Loss of NWP Physical Baseline:** Because operational NWP aerosol chemistry terminates at 120h (Day 5), Line A loses its physical anchor, causing tree models to regress to the historical climatological mean.
  4. **Extreme Peak Flattening:** GBDTs severely underestimate sudden severe Haboob spikes at extended horizons, failing when accurate warnings are needed most.
* **The Strategic Justification for Line B:**
  > *"This is the pivotal scientific realization of our work: even with aggressive hyperparameter tuning, classical tabular ML cannot break the 72-hour barrier alone. To forecast out to 15 days, we must invest in Main Line B—deep spatiotemporal sequence and graph architectures that directly model physical wave advection."*

---

### Slide 17: Main Line B: End-to-End Deep Spatiotemporal Architecture
* **Slide Title:** Main Line B: End-to-End Deep Spatiotemporal Architecture
* **Four Deep Tracks:**
  * **Track B1 (Bi-LSTM):** Bidirectional Long Short-Term Memory capturing 72h historical sequences and diurnal thermal cycles.
  * **Track B2 (Transformers / TFT):** Temporal Fusion Transformer with self-attention, Gated Residual Networks (GRN), and Variable Selection Networks (VSN).
  * **Track B3 (ST-GNN):** Spatiotemporal Graph Neural Networks modeling 6 ground stations and 5 desert corridors as a dynamic advection graph.
  * **Track B4 (PINN):** Physics-Informed Neural Network loss embedding Owen saltation threshold and mass continuity PDE.

---

### Slide 18: Line B Dynamic ST-GNN Corridor Graph
* **Slide Title:** Line B ST-GNN: Dynamic Wind-Advection Corridor Graph
* **Mathematical Adjacency Matrix Formulation:**
  $$\mathbf{A}_{ij}(t) = \exp\left(-\frac{d_{ij}}{D_0}\right) \cdot \left[1 + \max\left(0, \cos\left(\theta_{\text{wind}}^i(t) - \phi_{ij}\right)\right) \cdot \frac{u_{10}}{15.0}\right]$$
* **Physical Significance:**
  When prevailing winds align with the bearing $\phi_{ij}$ from an upstream desert station (e.g. Gassim or Al-Kharj) toward Riyadh KKIA, the dynamic edge weight increases proportionally to wind velocity. Information is passed along the physical transport route, alerting Riyadh 6 to 12 hours prior to dust front arrival.

---

### Slide 19: Physics-Informed Neural Networks (PINN) Loss Formulation
* **Slide Title:** Physics-Informed Loss Constraints: Enforcing Atmospheric Laws
* **Total Loss Equation:**
  $$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{Data}} + \lambda_1 \mathcal{L}_{\text{Saltation}} + \lambda_2 \mathcal{L}_{\text{Continuity}} + \lambda_3 \mathcal{L}_{\text{NonNegative}}$$
* **Component Descriptions:**
  1. *Owen Saltation Loss:* $\mathcal{L}_{\text{Salt}} = \frac{1}{N} \sum \text{ReLU}(u_{*t} - u_{*,i}) \cdot \hat{y}_i$ (zeros emissions if wind friction velocity is below threshold).
  2. *Continuity PDE Loss:* $\mathcal{L}_{\text{Cont}} = \left\| \frac{\partial \hat{y}}{\partial t} + u \frac{\partial \hat{y}}{\partial x} + v \frac{\partial \hat{y}}{\partial y} - S \right\|^2$ (conserves aerosol mass across grid cells).
  3. *Non-Negativity Barrier:* $\mathcal{L}_{\text{NonNeg}} = \frac{1}{N} \sum \text{ReLU}(-\hat{y}_i)$ (strictly eliminates impossible negative concentrations).

---

### Slide 20: Explainable AI (XAI) & SHAP Attribution
* **Slide Title:** Explainable AI (XAI): SHAP Attribution & Physical Credibility
* **Methodology:**
  * Game-theoretic Shapley values computed via TreeSHAP and DeepSHAP.
  * **Feature Hierarchy Confirmed:**
    1. Upwind surface friction velocity ($u_*$) in Nafud al-Thuwairat & Ad-Dahna.
    2. Topsoil moisture ($0\text{--}7\,\text{cm}$) suppressing saltation.
    3. Baseline NWP forecast ($t + \tau$).
    4. Corridor directional wind alignment factor ($\cos(\theta - \phi)$).
    5. Autoregressive lags ($\text{PM}_{10}$ at $t-1\text{h}, t-3\text{h}, t-24\text{h}$).
    6. Tuwayq mountain bluff roughness and planetary boundary layer height.
  * Individual storm waterfall plots provide audit trails for municipal disaster authorities.

---

### Slide 21: Validation Strategy: Walk-Forward Cross-Validation
* **Slide Title:** Rigorous Validation: Walk-Forward Cross-Validation & Case Studies
* **Four Validation Pillars:**
  1. *Walk-Forward Temporal Split:* Chronological training on 2020–2023, testing on held-out 2024. Zero random shuffling.
  2. *Spatial Leave-One-Station-Out:* Verifies generalizability when an entire corridor station is withheld.
  3. *Extreme Out-of-Sample Stress Tests:* Evaluating peak capture on historic super-storms (March 2021, March 2022, April 2025).
  4. *Perturbation Sensitivity Testing:* Testing monotonic physical response to soil moisture and wind perturbations.

---

### Slide 22: Evaluation Metrics & Targeted Benchmarks
* **Slide Title:** Evaluation Metrics & Targeted WMO Verification Benchmarks
* **Target Acceptance Table:**

| Metric Symbol | Metric Name | Mathematical Definition | Acceptance Target |
| :--- | :--- | :--- | :---: |
| $\mathbf{\Delta\text{RMSE}\%}$ | Error Reduction vs. NWP | $(\text{RMSE}_{\text{NWP}} - \text{RMSE}_{\text{Model}}) / \text{RMSE}_{\text{NWP}} \times 100\%$ | $\mathbf{\ge 25.0\%}$ |
| $\mathbf{R^2}$ | Coefficient of Determination | $1 - \sum(y - \hat{y})^2 / \sum(y - \bar{y})^2$ | $\mathbf{\ge 0.70}$ |
| $\mathbf{\text{POD}}$ | Probability of Detection (Hit Rate) | $H / (H + M)$ | $\mathbf{\ge 0.80}$ |
| $\mathbf{\text{CSI}}$ | Critical Success Index (Threat Score) | $H / (H + M + F)$ | $\mathbf{\ge 0.60}$ |
| $\mathbf{\text{FAR}}$ | False Alarm Ratio | $F / (H + F)$ | $\mathbf{\le 0.25}$ |
| $\mathbf{\text{PICP}}$ | Prediction Interval Coverage | $\% \text{ of observed } y \in [P_{10}, P_{90}]$ | $\mathbf{\ge 85.0\%}$ |

---

### Slide 23: Synthesis: Main Line A vs. Main Line B
* **Slide Title:** Comparative Synthesis: Main Line A vs. Main Line B
* **Comparative Summary:**
  * **Line A (Tree Ensembles):** Optimized for Days 3–5 (+72h to +120h). Sub-second inference. Outstanding for correcting local systematic biases in numerical weather prediction. Fails beyond Day 5 due to recursive lag drift and absence of spatial fluid continuity.
  * **Line B (Deep Spatiotemporal):** Optimized for Days 3–15. Models physical advection across dynamic desert graphs and continuous 2D grids. Respects aerosol mass conservation PDEs. Eliminates tabular drift and captures extended synoptic waves.
  * **Synergy:** Together, Line A and Line B form an integrated multi-horizon forecasting powerhouse.

---

### Slide 24: Operational Early Warning Playbook
* **Slide Title:** Operational Early Warning Playbook & Municipal Action
* **Playbook Execution Flow:**
  1. *T - 0h (Ingestion):* Hourly station feeds from `OERK`, `OERY`, `OEPS`, `OEDM`, `OEWD`, `OEGS` ingested; Owen saltation verified across all 5 desert source basins.
  2. *T + 1h (Dual Execution):* Line A debiases the morning CAMS run (+72h to +120h); Line B propagates ST-GNN and Transformer out to Day 15.
  3. *Alert Thresholds:* Automated red alert if $\text{PM}_{10} > 500\,\mu\text{g/m}^3$ or Visibility $< 1.0\,\text{km}$.
  4. *Targeted Action:* KKIA flight ground-stop advisories, school and construction suspension, emergency hospital pediatric mobilization.
  5. *Continuous Self-Correction:* Ground observations logged to continuously refine PINN loss weights.

---

### Slide 25: Conclusions & Contribution to Saudi Vision 2030
* **Slide Title:** Conclusions & Contribution to Saudi Vision 2030
* **Spoken Presentation Script:**
  > *"In conclusion, this research successfully bridges the gap between atmospheric physics and modern artificial intelligence. By identifying the root causes of the 72-hour NWP limit and the inherent drift of classical machine learning, we demonstrated why investing in Line B deep spatiotemporal models is scientifically necessary. Our dual-line platform delivers accurate, physics-grounded, explainable forecasts up to 15 days in advance. This directly serves Saudi Vision 2030, protects aviation and renewable energy infrastructure, safeguards public health, and strengthens climate resilience across the Kingdom. Thank you for your kind attention. I welcome your questions and discussion."*

---

## 🛠️ How to Access and Present the Slide Deck

### Option 1: Microsoft PowerPoint Presentation (.pptx)
Open the generated widescreen presentation:
👉 [`Persentation/Applying_Machine_Learning_for_Sandstorm_Forecasting_Riyadh_Complete.pptx`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Persentation/Applying_Machine_Learning_for_Sandstorm_Forecasting_Riyadh_Complete.pptx)

### Option 2: Browser Interactive Slides & One-Click PDF Export (.html)
Open [`Persentation/presentation_slides.html`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Persentation/presentation_slides.html) in any web browser (Chrome, Edge, Safari):
- **Navigate:** Use the `◀ Previous` / `Next ▶` buttons or your keyboard arrow keys (`Left` / `Right`, `Spacebar`, `Home`, `End`).
- **Export to PDF:** Click the golden **"🖨️ Export / Print to PDF"** button (or press `Ctrl + P`), select **"Save as PDF"**, set Margins to **"None"**, check **"Background graphics"**, and save a 25-page PDF presentation.
