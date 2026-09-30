# 🛡️ Multivariate Outlier Screening & Physical Plausibility Auditing
### *Mahalanobis Distance ($D^2$), Isolation Forests & Domain-Specific Physical Invariant Gates*
**Core Methods:** Robust FastMCD Covariance, Isolation Forest, Atmospheric Plausibility Rules  
**Target Indicators:** Multi-Dimensional Feature Vectors $\mathbf{X} \in \mathbb{R}^D$ ($\text{PM}_{10}, \text{PM}_{2.5}, U_{10}, \text{RH}, T, P$)  
**Output Target:** Physically Validated Multidimensional Datasets Free of Instrument Illusions

---

## 🎯 1. Operational Goal & Multivariate Illusions

In complex environmental systems, **univariate screening fails completely**:
* A $\text{PM}_{10}$ concentration of $750 \ \mu\text{g/m}^3$ is completely normal during an intense spring dust storm.
* A relative humidity of $95\%$ is completely normal during a foggy autumn morning.
* A wind speed of $1.5\text{ m/s}$ is completely normal during a nocturnal inversion.

However, **when all three occur simultaneously**, it represents a **physical impossibility**: mineral dust particles cannot initiate or remain suspended at $750 \ \mu\text{g/m}^3$ under near-zero wind in saturated air (where hygroscopic growth and wet scavenging rapidly wash out particulates). The optical particulate sensor was tricked by **condensed water fog droplets**, not sand.

The **Multivariate Plausibility Audit** evaluates observations across their full joint atmospheric correlation structure to eliminate physical illusions before training machine learning models.

---

## 📐 2. Mathematical Detection Formulations

```
+---------------------------------------------------------------------------------------------------+
|                        MULTIVARIATE PLAUSIBILITY AUDITING PIPELINE                                |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [GATE 1: Ratio Consistency Check]             PM2.5 <= PM10 strictly                             |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [GATE 2: Fog vs. Sandstorm Discrimination]    If PM10 > 500 & RH > 85% & Wind < 2.5 m/s -> Flag  |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [GATE 3: Robust Mahalanobis Distance D²]       D² = (x - μ_MCD)^T Σ_MCD^-1 (x - μ_MCD) > χ²_crit |
|                                                                 │                                 |
|                                                                 ▼                                 |
|  [GATE 4: Isolation Forest Anomaly Score]      Anomaly Score s(x, n) > 0.65                       |
+---------------------------------------------------------------------------------------------------+
```

---

### 2.1 The Particulate Physical Ratio Rule ($\text{PM}_{2.5} \le \text{PM}_{10}$)
Particulate matter diameters are defined hierarchically: $\text{PM}_{2.5}$ particles ($\le 2.5\mu\text{m}$) are a physical subset of $\text{PM}_{10}$ particles ($\le 10\mu\text{m}$). Therefore:

$$\text{Physical Invariant}: \quad \text{PM}_{2.5} \le \text{PM}_{10} \quad \forall t$$

Observations where $\text{PM}_{2.5} > \text{PM}_{10} \times 1.05$ (allowing $5\%$ sensor measurement tolerance) indicate separate instrument calibration drift or optical chamber contamination, and are flagged for correction:
$$\text{Corrected } \text{PM}_{2.5} = \min\left(\text{PM}_{2.5}, \ \text{PM}_{10}\right)$$

---

### 2.2 Robust Mahalanobis Distance ($D^2$) via Minimum Covariance Determinant (MCD)
Standard sample covariance $\boldsymbol{\Sigma}$ is easily corrupted by the very outliers it seeks to detect (**masking effect**). The **FastMCD (Minimum Covariance Determinant)** algorithm computes robust location ($\boldsymbol{\mu}_{\text{MCD}}$) and dispersion ($\boldsymbol{\Sigma}_{\text{MCD}}$) using the $75\%$ most concentrated data subset:

$$D^2(\mathbf{x}_i) = \left(\mathbf{x}_i - \boldsymbol{\mu}_{\text{MCD}}\right)^T \boldsymbol{\Sigma}_{\text{MCD}}^{-1} \left(\mathbf{x}_i - \boldsymbol{\mu}_{\text{MCD}}\right)$$

Under the null hypothesis of multivariate normality, $D^2$ follows a chi-square distribution with $p$ degrees of freedom ($p$ = number of features):
$$\text{Is Multivariate Outlier}: \quad D^2(\mathbf{x}_i) > \chi^2_{p, \ 1 - \alpha} \quad (\text{with } \alpha = 0.001)$$

---

### 2.3 Isolation Forest Non-Parametric Anomaly Scoring
Because severe non-linear weather extremes deviate from elliptical Gaussian distributions, an **Isolation Forest** recursively isolates samples using random feature cuts. Outliers require significantly fewer tree splits to isolate:

$$s(\mathbf{x}, N) = 2^{-\frac{\mathbb{E}(h(\mathbf{x}))}{c(N)}}$$

Where $h(\mathbf{x})$ is the path length in the isolation tree, and $c(N)$ is the average path length of unsuccessful searches in a Binary Search Tree of $N$ nodes. Samples with anomaly score $s > 0.65$ are audited for physical consistency.

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `chi2_significance` | `float` | `0.001` | `0.001 - 0.01` | Probability threshold for Mahalanobis $\chi^2$ critical value cutoff. |
| `mcd_support_fraction`| `float` | `0.75` | `0.65 - 0.85` | Fraction of data points included in FastMCD robust covariance estimation. |
| `fog_rh_threshold` | `float` | `85.0` | `80.0 - 90.0` | Relative humidity percentage above which water droplets scatter optical sensors. |
| `fog_wind_max` | `float` | `2.5` | `2.0 - 3.5` | Maximum wind speed ($\text{m/s}$) confirming calm air during fog false alarms. |
| `isolation_forest_trees`|`int` | `150` | `100 - 300` | Number of decision isolation trees in the ensemble. |
| `contamination_rate`| `float` | `0.01` | `0.005 - 0.02`| Expected proportion of true anomalies in raw telemetry datasets. |

---

## 💡 4. Automated Python Multivariate Audit Pipeline

```python
import numpy as np
import pandas as pd
from scipy.stats import chi2
from sklearn.covariance import MinCovDet
from sklearn.ensemble import IsolationForest

def audit_multivariate_plausibility(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies physical invariant gates and statistical multivariate anomaly detection.
    """
    df_audited = df.copy()
    
    # 1. Physical Gate: PM2.5 <= PM10
    if "pm25" in df_audited.columns and "pm10" in df_audited.columns:
        invalid_ratio = df_audited["pm25"] > (df_audited["pm10"] * 1.05)
        df_audited.loc[invalid_ratio, "pm25"] = df_audited.loc[invalid_ratio, "pm10"]

    # 2. Physical Gate: Fog / Condensation False Alarm Filter
    # (High PM10 in calm, humid air is optical condensation scattering, not sand)
    if all(col in df_audited.columns for col in ["pm10", "rh", "u10"]):
        fog_false_alarm = (df_audited["pm10"] > 400.0) & (df_audited["rh"] > 85.0) & (df_audited["u10"] < 2.5)
        df_audited.loc[fog_false_alarm, "pm10"] = np.nan

    # 3. Robust Mahalanobis Distance D² on Clean Continuous Variables
    numeric_cols = ["pm10", "u10", "temp", "pressure"]
    available_cols = [c for c in numeric_cols if c in df_audited.columns]
    
    valid_data = df_audited[available_cols].dropna()
    if len(valid_data) > 100:
        # Fit FastMCD robust covariance
        mcd = MinCovDet(support_fraction=0.75, random_state=42)
        mcd.fit(valid_data.values)
        
        # Calculate robust Mahalanobis distances
        d2 = mcd.mahalanobis(valid_data.values)
        p = len(available_cols)
        crit_val = chi2.ppf(0.999, df=p)
        
        outlier_indices = valid_data.index[d2 > crit_val]
        df_audited["is_multivariate_outlier"] = False
        df_audited.loc[outlier_indices, "is_multivariate_outlier"] = True

    return df_audited
```
