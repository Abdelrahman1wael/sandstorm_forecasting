# 🧹 Data Cleaning & Quality Control Suite: Master Overview
### *Sensor Telemetry Decontamination, Missing Data Imputation, Temporal Synchronization & Multivariate Auditing*
**Discipline:** Environmental Data Engineering & Empirical Research Hygiene  
**Platform:** DustML Operational Forecasting Platform (北京科技大学 • USTB)  
**Target Domain:** Multi-Source Heterogeneous Ground, Atmospheric, and Socioeconomic Feeds

---

## 🌟 Executive Overview

In environmental engineering and disaster prediction, the adage **"Garbage In, Garbage Out"** is absolute. Raw environmental feeds from sensor networks, numerical models, and public surveys are plagued by real-world corruptions:
* **Mechanical Telemetry Failures:** Sensor pump clogging, optical window dust coating, and electronic freezing producing flatlines.
* **Severe Missing Gaps:** Power outages during violent storms causing data loss exactly when observations are most critical.
* **Timezone Desynchronization:** Mixing UTC numerical model runs with China Standard Time (CST / UTC+8) station logs, causing fatal 8-hour phase lags.
* **Univariate vs. Physical Outliers:** Confusing a genuine extreme sandstorm ($3,500 \ \mu\text{g/m}^3$) with an unphysical sensor spike (e.g., insect obstruction or electrical surge).
* **Survey Careless Responding:** Straight-lining and speeder submissions corrupting psychometric SEM models in SPSS and AMOS.

This directory provides the technical specifications, mathematical equations, parameter dictionaries, and automated Python / SPSS scripts across the **5 Core Stages of Data Cleaning**:

```
+---------------------------------------------------------------------------------------------------+
|                           5-STAGE DATA CLEANING & HYGIENE PIPELINE                                |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [STAGE 1: Sensor QC & Despiking]       Zero-Variance Flatline Detection & Negative Clipping       |
|                                         Rolling MAD Despiking (Physical vs Noise Spikes)          |
|                                         (Detailed in SENSOR_TELEMETRY_QC_AND_DESPIKING.md)        |
|                                                     |                                             |
|                                                     v                                             |
|  [STAGE 2: Missing Data Imputation]     Little's MCAR Test & Missing Mechanism Diagnosis          |
|                                         Akima Spline (<=3h) • Spatial Kriging • MICE (Chained)    |
|                                         (Detailed in MISSING_DATA_IMPUTATION_FRAMEWORK.md)        |
|                                                     |                                             |
|                                                     v                                             |
|  [STAGE 3: Temporal Harmonization]      UTC vs CST Explicit Conversion (Eliminating 8h Shift)     |
|                                         Irregular Rate Resampling -> Uniform Hourly & Synoptic    |
|                                         (Detailed in TEMPORAL_ALIGNMENT_AND_TIMEZONE_HARMONIZATION.md)|
|                                                     |                                             |
|                                                     v                                             |
|  [STAGE 4: Multivariate Plausibility]   Mahalanobis Distance D² & Isolation Forest Screening      |
|                                         Physical Consistency Rules (High Dust Requires High Wind) |
|                                         (Detailed in MULTIVARIATE_OUTLIER_AND_PLAUSIBILITY_AUDIT.md)|
|                                                     |                                             |
|                                                     v                                             |
|  [STAGE 5: Survey Data Hygiene]         Straight-Lining Variance Filter (Var < 0.20)              |
|                                         Speeder Screen (<30% Median Time) & Reverse Coding       |
|                                         (Detailed in SURVEY_DATA_HYGIENE_AND_SCREENING.md)        |
+---------------------------------------------------------------------------------------------------+
```

---

## 📂 Data Cleaning Catalog

| Document | Focus & Core Methodologies | Target Output / Deliverable |
| :--- | :--- | :--- |
| **[`SENSOR_TELEMETRY_QC_AND_DESPIKING.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Data_cleaning/SENSOR_TELEMETRY_QC_AND_DESPIKING.md)** | Zero-variance flatline detection ($\sigma < 0.1$ across 12h), negative calibration drift clipping ($\max(0, x)$), and rolling Median Absolute Deviation (MAD) despiking separating electronic spikes from true dust storm peaks. | Decontaminated ground particulate ($\text{PM}_{10}, \text{PM}_{2.5}$) and surface meteorological time-series. |
| **[`MISSING_DATA_IMPUTATION_FRAMEWORK.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Data_cleaning/MISSING_DATA_IMPUTATION_FRAMEWORK.md)** | Missing mechanism diagnosis (MCAR, MAR, MNAR), Akima shape-preserving splines for short gaps ($\le 3\text{h}$), Spatial Ordinary Kriging for sensor dropouts ($3\text{--}24\text{h}$), and Multiple Imputation by Chained Equations (MICE) for long records. | 100% complete continuous training matrices without listwise deletion bias. |
| **[`TEMPORAL_ALIGNMENT_AND_TIMEZONE_HARMONIZATION.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Data_cleaning/TEMPORAL_ALIGNMENT_AND_TIMEZONE_HARMONIZATION.md)** | Strict timezone localization (`Asia/Shanghai` $\to$ `UTC`), resampling heterogeneous 15-min/1-hour feeds into standardized synoptic reporting intervals (00, 06, 12, 18 UTC), and backward-lag alignment. | Synchronized spatiotemporal timestamps matching NWP initialization cycles. |
| **[`MULTIVARIATE_OUTLIER_AND_PLAUSIBILITY_AUDIT.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Data_cleaning/MULTIVARIATE_OUTLIER_AND_PLAUSIBILITY_AUDIT.md)** | Mahalanobis Distance $D^2$, robust minimum covariance determinants (FastMCD), Isolation Forests, and physical environmental plausibility logic (e.g., rejecting $\text{PM}_{10} > 1000$ if $U_{10} < 2\text{ m/s}$ and relative humidity $> 90\%$). | Clean multidimensional feature matrices certified free of physical contradictions. |
| **[`SURVEY_DATA_HYGIENE_AND_SCREENING.md`](file:///c:/Users/hp/Desktop/China_project/Planning/Data_cleaning/SURVEY_DATA_HYGIENE_AND_SCREENING.md)** | Psychometric survey hygiene: detection of unengaged respondents (straight-lining), speeders submission filtering, reverse item polarity re-coding, and outlier screening ready for SPSS and AMOS SEM modeling. | Verified `.sav` survey datasets guaranteeing convergent and discriminant validity. |
