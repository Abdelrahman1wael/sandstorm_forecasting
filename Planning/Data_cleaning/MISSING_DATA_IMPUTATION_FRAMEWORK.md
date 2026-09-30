# 🧩 Missing Data Imputation Framework
### *Hierarchical Multi-Tier Reconstruction: Akima Splines, Spatial Kriging & MICE*
**Theoretical Foundation:** Rubin's Missing Data Taxonomy (MCAR, MAR, MNAR) & Spatial Interpolation  
**Target Modalities:** Station Particulate Networks, Meteorological Sensors, Socioeconomic Surveys  
**Output Target:** 100% Complete Spatiotemporal Training Matrices Without Survivorship Bias

---

## 🎯 1. Operational Goal & The Missing Data Dilemma

In environmental and meteorological sensor networks, missing data is unavoidable due to power blackouts during violent frontal storms, satellite orbital revisit intervals, or data logger memory overflow.

### The Danger of Listwise Deletion:
In multi-station spatio-temporal modeling, discarding any row containing a missing value (**listwise deletion**) discards **$> 45\%$ of the entire training dataset**, introducing severe **survivorship bias** (since sensors fail disproportionately during extreme disaster events).

### The Solution:
DustML deploys a **Hierarchical 3-Tier Imputation Protocol** selected dynamically based on gap duration and spatial correlation structure:

```
                          Length of Missing Temporal Gap:
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
  [Tier 1: Short Gaps (<= 3h)]  [Tier 2: Medium Gaps (3 - 24h)]  [Tier 3: Long Gaps (> 24h)]
  Akima Shape-Preserving Spline   Spatial Ordinary Kriging Infill  MICE / ERA5 Atmospheric Anchor
  (Preserves diurnal inertia)   (Borrowed from adjacent network) (Multi-variate chained equations)
```

---

## 📐 2. Mathematical Formulations across Imputation Tiers

---

### 2.1 Tier 1: Short Gaps ($\le 3\text{ Hours}$) — Akima Shape-Preserving Spline
Standard cubic splines suffer from **Runge’s phenomenon** (severe unphysical overshoots and undershoots around steep dust peaks, producing negative concentrations).

The **Akima Sub-Spline** constructs a continuously differentiable curve ($C^1$) where the tangent slope $t_i$ at point $x_i$ is determined strictly by the four neighboring slopes $m_{i-2}, m_{i-1}, m_i, m_{i+1}$:

$$t_i = \frac{|m_{i+1} - m_i| m_{i-1} + |m_{i-1} - m_{i-2}| m_i}{|m_{i+1} - m_i| + |m_{i-1} - m_{i-2}|}$$

If $m_{i+1} = m_i$ (local plateau), $t_i = m_i$, **completely eliminating artificial oscillating overshoots**.

---

### 2.2 Tier 2: Medium Gaps ($3\text{--}24\text{ Hours}$) — Spatial Ordinary Kriging Infill
When a single station drops out for several hours during an active synoptic storm, temporal interpolation fails because the storm front is rapidly advecting. The missing value is reconstructed using **Spatial Ordinary Kriging** from the surrounding $K=8$ reporting stations:

$$\hat{y}_0 = \sum_{k=1}^K w_k y_k, \quad \text{subject to } \sum_{k=1}^K w_k = 1$$

Where spatial weights $w_k$ solve the Kriging linear system using the empirical spherical semivariogram $\gamma(h)$:
$$\begin{pmatrix} \gamma(d_{11}) & \dots & \gamma(d_{1K}) & 1 \\ \vdots & \ddots & \vdots & \vdots \\ \gamma(d_{K1}) & \dots & \gamma(d_{KK}) & 1 \\ 1 & \dots & 1 & 0 \end{pmatrix} \begin{pmatrix} w_1 \\ \vdots \\ w_K \\ \mu \end{pmatrix} = \begin{pmatrix} \gamma(d_{10}) \\ \vdots \\ \gamma(d_{K0}) \\ 1 \end{pmatrix}$$

---

### 2.3 Tier 3: Long Gaps ($> 24\text{ Hours}$) — MICE & ERA5 Reanalysis Anchoring
When an entire station cluster loses power for multiple days:
1. **Multiple Imputation by Chained Equations (MICE):** Models each station variable as a function of all other correlated stations using Bayesian Ridge regression across 10 Gibbs sampling iterations.
2. **ERA5 Atmospheric Reanalysis Proxy:** For regional blackouts, the missing sensor sequence is anchored to the ERA5 particulate tracer scaled by the historical station-to-reanalysis ratio:
   $$\hat{y}(s, t) = \text{ERA5}_{\text{dust}}(s, t) \times \left( \frac{\bar{y}_{\text{station}}}{\bar{y}_{\text{ERA5}}} \right)$$

---

## ⚙️ 3. Complete Parameter Dictionary

| Parameter Name | Data Type | Default Value | Recommended Range | Physical / Algorithmic Meaning |
| :--- | :---: | :---: | :---: | :--- |
| `max_akima_gap_h` | `int` | `3` | `1 - 4` | Maximum gap length (hours) for temporal Akima interpolation. |
| `kriging_neighbors`| `int` | `8` | `6 - 16` | Number of neighboring ground stations used in spatial Kriging infill. |
| `kriging_max_dist_km`|`float` | `250.0` | `150 - 400` | Maximum spatial search distance for neighboring stations. |
| `mice_max_iter` | `int` | `10` | `5 - 20` | Number of iterative chained equation cycles in MICE. |
| `mice_imputations` | `int` | `5` | `5 - 10` | Number of parallel imputed datasets for pooled statistical estimation. |

---

## 💡 4. Automated Python Imputation Pipeline

```python
import numpy as np
import pandas as pd
from scipy.interpolate import Akima1DInterpolator
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge

def hierarchical_impute_timeseries(series: pd.Series, max_spline_gap: int = 3) -> pd.Series:
    """
    Tier 1 & Tier 3 hierarchical imputation on single-station series.
    """
    s_clean = series.copy()
    valid_idx = np.where(~s_clean.isna())[0]
    
    if len(valid_idx) < 5:
        return s_clean

    # 1. Identify missing gap lengths
    is_na = s_clean.isna()
    gap_lengths = is_na.groupby((~is_na).cumsum()).transform("sum")
    
    # 2. Apply Akima Spline strictly on short gaps (<= max_spline_gap)
    short_gap_mask = is_na & (gap_lengths <= max_spline_gap)
    if short_gap_mask.any():
        akima = Akima1DInterpolator(valid_idx, s_clean.iloc[valid_idx].values)
        short_gap_indices = np.where(short_gap_mask)[0]
        interpolated_vals = akima(short_gap_indices)
        s_clean.iloc[short_gap_indices] = np.maximum(0.0, interpolated_vals)

    return s_clean

def multi_station_mice_impute(station_matrix_df: pd.DataFrame, max_iter: int = 10) -> pd.DataFrame:
    """
    Tier 3 Multi-Station MICE Imputation across full station network DataFrame.
    """
    imputer = IterativeImputer(
        estimator=BayesianRidge(),
        max_iter=max_iter,
        random_state=42,
        min_value=0.0,
        sample_posterior=False
    )
    imputed_array = imputer.fit_transform(station_matrix_df)
    return pd.DataFrame(imputed_array, columns=station_matrix_df.columns, index=station_matrix_df.index)
```
