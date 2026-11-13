# ⚠️ Complete Research Troubleshooting Guide: Errors That Can Occur & How to Fix Them
### *SPSS, AMOS, GIS, Machine Learning (Line A), Deep Learning PINN (Line B), Data Ingestion & Production Deployment*
**Discipline:** Environmental Engineering (环境工程) • Atmospheric AI & Quantitative Methodology  
**Platform:** DustML Research System (北京科技大学 • USTB)

---

## 🌟 Executive Overview

In an end-to-end multi-disciplinary research system spanning **social science statistics (SPSS/AMOS)**, **spatial analytics (GIS)**, **meteorological data pipelines**, and **dual-line artificial intelligence (Line A tree ensembles & Line B deep PINNs)**, errors can occur across mathematical, numerical, physical, and software-engineering layers.

This guide provides an exhaustive diagnosis, root cause analysis, prevention protocol, and concrete code/software fix for the most frequent and severe errors encountered in this project.

```
+---------------------------------------------------------------------------------------------------+
|                                  SIX DOMAINS OF POTENTIAL ERRORS                                  |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [1. SPSS Statistics]        Missing Value Bias • Multicollinearity • Factor Cross-Loadings       |
|  [2. IBM SPSS AMOS]          Heywood Cases • Non-Positive Definite Matrix • Mediation Bootstrap   |
|  [3. GIS & Spatial Science]  CRS Reprojection Shifts • Semivariogram Singularity • Isolated Nodes |
|  [4. Main Line A (ML)]       Quantile Crossing • Severe Class Collapse • Temporal Data Leakage    |
|  [5. Main Line B (PINN)]     PDE Gradient Explosion (NaN) • Saltation Division by Zero • GPU OOM  |
|  [6. Operational API & Web]  UTC vs CST Time Shifting • CDS API Deadlocks • CORS & Schema Errors  |
+---------------------------------------------------------------------------------------------------+
```

---

## 📊 1. IBM SPSS Statistics Errors & Fixes

---

### Error 1.1: Singular Covariance Matrix & Extreme Multicollinearity
* **Software Message:**  
  `"The matrix is ill-conditioned or singular. Determinant of correlation matrix is 0.000. Parameter estimates may be unreliable."`
* **Root Cause:** Two or more environmental or survey indicators are virtually identical ($r > 0.90$, $\text{VIF} > 10.0, \text{Tolerance} < 0.10$), such as placing raw 10m wind speed, maximum gust speed, and kinetic energy density simultaneously into an unpenalized OLS regression without regularization.
* **Diagnostic Check:**  
  Run `Analyze > Regression > Linear > Statistics > Collinearity Diagnostics`. Look for $\text{VIF} > 5.0$ and Condition Index $> 30.0$.
* **Step-by-Step Fix:**
  1. Calculate bivariate Pearson correlation matrix: `Analyze > Correlate > Bivariate`.
  2. Drop the redundant indicator or combine them using a composite index or PCA factor score:
     ```sps
     COMPUTE Wind_Compound_Index = MEAN(z_u10, z_gust).
     EXECUTE.
     ```
  3. In machine learning pipelines, replace ordinary least squares with Ridge regression or tree ensembles (Line A) which naturally handle correlated splits.

---

### Error 1.2: Rejection of Little’s MCAR Test (Missing Data Bias)
* **Software Message:**  
  `"EM Estimated Statistics: Little's MCAR test: Chi-Square = 142.85, DF = 42, Sig. = .000 (p < .05)"`
* **Root Cause:** Data is **MAR (Missing at Random)** or **MNAR (Missing Not at Random)** rather than completely random. For instance, elderly survey respondents skipped app-based warning questions, or particulate monitors failed specifically during extreme dust storm spikes due to sensor clogging.
* **Why Listwise Deletion Fails:** Simply clicking *"Exclude cases listwise"* will discard 30–50% of the sample and introduce fatal survivorship bias into regression coefficients.
* **Step-by-Step Fix:**
  1. Do not use mean substitution (which artificially suppresses variance).
  2. Perform **Multiple Imputation (MI)** with 5 to 10 imputed datasets:
     * SPSS menu: `Analyze > Multiple Imputation > Impute Missing Data Values`.
     * Choose `Fully Conditional Specification (MCMC / FCS)` with 20 iterations.
     * Pool regression results across all imputations using Rubin's rules.

---

### Error 1.3: Factor Cross-Loadings in Exploratory Factor Analysis (EFA)
* **Software Message:** An indicator exhibits factor loadings $> 0.40$ on two distinct latent factors simultaneously, or fails to achieve a primary loading $\ge 0.50$.
* **Root Cause:** Double-barreled questionnaire items (e.g., *"I wear a mask because dust irritates my lungs and I trust government warnings"* taps both *Personal Symptom Sensitivity* and *Institutional Trust*).
* **Step-by-Step Fix:**
  1. Switch factor rotation from orthogonal (`Varimax`) to oblique (`Promax` with $\kappa = 4$), because psychological constructs in environmental disasters are naturally correlated.
  2. If the cross-loading persists with a difference $< 0.20$ between factors, eliminate the problematic indicator one by one, rerunning EFA after each removal until a clean simple structure is achieved.

---

## 🏛️ 2. IBM SPSS AMOS (CFA & SEM) Errors & Fixes

---

### Error 2.1: The Notorious "Heywood Case" (Negative Error Variance)
* **Software Message:**  
  `"The following error variance is negative: e4 = -0.082. An inadmissible solution was reached."` or `"Correlation between latent constructs exceeds 1.0."`
* **Root Cause:**
  1. Small sample size ($N < 200$) combined with high indicator collinearity.
  2. Only two indicators measuring a single latent construct without equal-loading constraints (under-identification).
  3. Outliers with extreme leverage distorting sample covariance.
* **Step-by-Step Fix:**
  1. **Examine Mahalanobis $D^2$:** Go to `View > Output Path > Observations farthest from the centroid`. Identify and remove cases with $p_1 < .001$ and $p_2 < .001$.
  2. **Add a Minimal Variance Constraint:** If the negative variance is tiny and statistically indistinguishable from zero, double-click error variable `e4` $\to$ `Parameters` tab $\to$ set variance to a small non-zero boundary:
     ```
     Variance = 0.005 (Fixed)
     ```
  3. **Ensure 3+ Indicators:** Ensure every latent factor has at least three reliable reflective indicators. If only two exist, constrain their unstandardized factor loadings to be equal ($a = b$).

---

### Error 2.2: Covariance Matrix is Not Positive Definite
* **Software Message:**  
  `"The model is probably not identified. In order to achieve identification, it may be necessary to impose additional constraints. The sample covariance matrix is not positive definite."`
* **Root Cause:** One or more eigenvalues of the covariance matrix are zero or negative, usually caused by linear dependency, pair-wise missing data handling, or negative measurement error variance.
* **Step-by-Step Fix:**
  1. Switch raw data missing handling from pairwise deletion to **Full Information Maximum Likelihood (FIML)**:
     * In AMOS, click `View > Analysis Properties > Estimation` tab $\to$ check `Estimate means and intercepts`.
  2. Inspect bivariate correlations for values $|r| \ge 0.95$. Remove redundant duplicate variables.
  3. Verify all latent factors have their scale set by fixing one factor loading to `1.0` (Reference Indicator).

---

### Error 2.3: Poor Global Model Fit (RMSEA > 0.08, CFI < 0.90)
* **Software Message:**  
  `CMIN/DF = 4.82 (Target < 3.0), CFI = 0.842 (Target ≥ 0.90), RMSEA = 0.098 (Target < 0.06).`
* **Root Cause:** Unmodeled shared method variance between items with similar wording, or omitted structural cross-paths.
* **Step-by-Step Fix:**
  1. Check **Modification Indices (MI)**: In AMOS, go to `Analysis Properties > Output` $\to$ check `Modification Indices (Threshold = 4.0)`.
  2. Inspect covariances between error terms: If two indicators belong to the **same latent construct** (e.g., `e1` and `e2` both measure *Institutional Trust*) and $\text{MI} > 15.0$, add a two-headed covariance arrow $\text{e1} \longleftrightarrow \text{e2}$, provided there is strong theoretical justification (e.g., reverse-coded items or identical sentence structure).
  3. **Never correlate errors across different latent constructs**, as this invalidates construct validity.

---

## 🗺️ 3. GIS & Spatial Science (ArcGIS / QGIS / GeoPandas) Errors

---

### Error 3.1: Coordinate Reference System (CRS) Reprojection Shift
* **Symptom:** Ground observation stations appear in the middle of the Indian Ocean or 100 kilometers away from their true desert corridor locations. Distance calculations in GWR return zeros or giant numbers ($10^{12}$).
* **Root Cause:** Mixing **Geographic Coordinate Systems** (WGS84, `EPSG:4326`, measured in angular degrees) with **Projected Coordinate Systems** (Web Mercator `EPSG:3857` or CGCS2000 / 3-degree Gauss-Kruger `EPSG:4490`, measured in metric meters). Euclidean distance functions assume meters, while coordinates are passed as $(116.4^\circ\text{E}, 39.9^\circ\text{N})$.
* **Step-by-Step Fix (GeoPandas & QGIS):**
  ```python
  import geopandas as gpd

  # 1. Load raw stations in WGS84 geographic coordinates
  gdf = gpd.read_file("stations.geojson") # CRS: EPSG:4326
  
  # 2. DO NOT just overwrite .crs! Must use .to_crs() to project coordinates into meters
  # For Northern China: CGCS2000 / 3-degree Gauss-Kruger Zone 39 (EPSG:4527) or UTM Zone 50N (EPSG:32650)
  gdf_projected = gdf.to_crs(epsg=32650)
  
  # 3. Verify units are now in meters:
  print("Units:", gdf_projected.crs.axis_info[0].unit_name) # 'metre'
  ```

---

### Error 3.2: Semivariogram Singularity in Kriging Interpolation
* **Software Message:**  
  `"Unable to fit theoretical semivariogram. Sill is negative or range exceeds bounding box. Matrix inversion failed."`
* **Root Cause:**
  1. Duplicate sensor points with identical $(x, y)$ coordinates having contradictory $\text{PM}_{10}$ readings.
  2. Severe spatial anisotropy or strong linear trend that was not detrended prior to Ordinary Kriging.
* **Step-by-Step Fix:**
  1. Remove co-located points using `Delete Identical` in ArcGIS or `gdf.drop_duplicates(subset=['geometry'])` in Python.
  2. Check for strong regional trend (e.g., dust concentrations naturally decreasing along the northwest-to-southeast transport corridor).
  3. Fit a 1st-order polynomial detrending surface before calculating the semivariogram:
     * In ArcGIS: Select `Universal Kriging` with Linear Drift, or perform `Trend Removal > Order 1`.
  4. Manually constrain the Nugget variance: $\text{Nugget} \ge 0$, $\text{Sill} > \text{Nugget}$, $\text{Range} \le \frac{1}{2} \text{Maximum Bounding Distance}$.

---

### Error 3.3: Spatial Weights Matrix "Island" Disconnection in Moran’s I & GWR
* **Software Message:**  
  `"Neighbor count for feature ID 14 is zero. Spatial weight matrix has disconnected islands. Analysis cannot proceed."`
* **Root Cause:** Using a fixed distance band threshold ($d = 50\text{ km}$) when station density is highly heterogeneous (dense clusters in Beijing/Tianjin, but sparse stations separated by $300\text{ km}$ in western Xinjiang).
* **Step-by-Step Fix:**
  1. Replace fixed distance band weighting with **$K$-Nearest Neighbors ($K$-NN)** or **Adaptive Bisquare Kernel**:
     ```python
     from libpysal.weights import KNN
     # Ensure every station has at least 8 neighbors regardless of isolation
     w = KNN.from_dataframe(gdf_projected, k=8)
     w.transform = 'R' # Row-standardized
     ```
  2. In GWR (ArcGIS Pro / `mgwr` package), select `Adaptive Bandwidth` using AICc minimization rather than `Fixed Bandwidth`.

---

## 🌲 4. Main Line A (Machine Learning & Bias Correction) Errors

---

### Error 4.1: Quantile Crossing Violation ($P_{10} > P_{50}$ or $P_{50} > P_{90}$)
* **Symptom:** The lower uncertainty bound ($P_{10}$) predicts $450 \ \mu\text{g/m}^3$, while the median ($P_{50}$) predicts $320 \ \mu\text{g/m}^3$, creating a mathematically impossible uncertainty envelope.
* **Root Cause:** Fitting separate independent LightGBM or Scikit-Learn models for each quantile without joint constraints. Under sparse extreme validation splits, gradients for $P_{10}$ and $P_{50}$ can cross.
* **Diagnostic Check:** Run `np.any(p10 > p50) or np.any(p50 > p90)`.
* **Step-by-Step Fix:**
  1. **Post-Hoc Sorting:**
     ```python
     quantiles_matrix = np.column_stack([p10_raw, p50_raw, p90_raw])
     quantiles_sorted = np.sort(quantiles_matrix, axis=1)
     p10_clean, p50_clean, p90_clean = quantiles_sorted[:, 0], quantiles_sorted[:, 1], quantiles_sorted[:, 2]
     ```
  2. **Cumulative Softplus Gap Parametrization in Deep Uncertainty Heads (PyTorch):**
     ```python
     p50 = F.softplus(self.head_p50(x))
     p10 = torch.clamp(p50 - F.softplus(self.head_p10_delta(x)), min=0.0)
     p90 = p50 + F.softplus(self.head_p90_delta(x))
     # Monotonicity is mathematically guaranteed: p10 <= p50 <= p90
     ```

---

### Error 4.2: Severe Class Collapse in Sandstorm Hazard Classifiers ($\text{TS} = 0.0$)
* **Symptom:** Model achieves $98.5\%$ classification accuracy, but the Threat Score (TS) for Class 4 (Severe Dust Storm) is $0.000$, and Probability of Detection ($\text{POD}$) is $0.0\%$.
* **Root Cause:** Extreme class imbalance. Severe storms occur $< 0.8\%$ of the year. Standard Cross-Entropy loss minimizes global error by predicting "Normal Air Quality" $100\%$ of the time.
* **Step-by-Step Fix:**
  1. Pass inverse class frequency weights into the classifier:
     ```python
     class_weights = {0: 1.0, 1: 3.0, 2: 6.0, 3: 15.0, 4: 50.0}
     clf = lgb.LGBMClassifier(class_weight=class_weights)
     ```
  2. Implement an **Asymmetric Cost Matrix** during evaluation, penalizing missed storms (False Negatives) $50\times$ more than false alarms (False Positives).
  3. Apply threshold optimization on output probabilities rather than using default $p > 0.50$ argmax cutoffs.

---

### Error 4.3: Temporal Data Leakage in Cross-Validation
* **Symptom:** Model shows stellar test $R^2 = 0.94$ in experiments, but crashes to $R^2 = 0.28$ when evaluated in real-time operational deployment.
* **Root Cause:** Using `sklearn.model_selection.KFold(shuffle=True)`. Random shuffling places March 15 storm records into the training set and March 14 records into the test set. Atmospheric memory and autocorrelation leak future information into the model.
* **Step-by-Step Fix:**
  * **Always use Walk-Forward (TimeSeriesSplit) Validation**:
    ```python
    from sklearn.model_selection import TimeSeriesSplit
    tscv = TimeSeriesSplit(n_splits=5)
    for train_index, test_index in tscv.split(time_ordered_data):
        # train_index always strictly precedes test_index chronologically
        X_train, X_test = X[train_index], X[test_index]
    ```

---

## 🌌 5. Main Line B (Deep Learning & PINN Conservation) Errors

---

### Error 5.1: NaN Gradient Explosion in PINN PDE Mass Conservation Loss
* **Software Message:**  
  `"Loss is NaN at Epoch 3, Step 42. Backpropagation produced inf gradients in loss_mass."`
* **Root Cause:**
  1. In the mass continuity residual $\|\Delta C - \text{Inflow}\|^2$, wind velocity gradients or rapid spatial advection divergence create huge numeric spikes when multiplied by large concentration values ($2,500 \ \mu\text{g/m}^3$).
  2. In Owen's saltation flux formula, $u_*^3$ with $u_* = 25\text{ m/s}$ produces $15,625$, leading to gradient blowups when unnormalized.
* **Step-by-Step Fix:**
  1. **Add Gradient Clipping:**
     ```python
     loss.backward()
     torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
     optimizer.step()
     ```
  2. **Replace MSE with Smooth L1 (Huber Loss) in PDE Residuals:**
     ```python
     # Instead of (residual)**2, use Huber loss:
     mass_residual = F.relu(lead_delta - inflow_trunc * 1.5)
     loss_mass = torch.mean(F.smooth_l1_loss(mass_residual, torch.zeros_like(mass_residual)))
     ```
  3. **Implement Physics Loss Curriculum Warm-Up:**
     Keep $\lambda_{\text{mass}} = 0$ and $\lambda_{\text{salt}} = 0$ during Epochs 1–3, then linearly scale them up to $0.15$ and $0.20$ across Epochs 4–8.

---

### Error 5.2: Division by Zero in Graph Laplacian Normalization (ST-GNN)
* **Software Message:**  
  `"RuntimeError: Function 'DivBackward0' returned nan values in its grad_edge."`
* **Root Cause:** If a corridor node has no outgoing edges ($d_{\text{out}} = 0$) or isolated disconnected vertices, computing $\mathbf{D}_{\text{out}}^{-1} \mathbf{A}$ divides by zero.
* **Step-by-Step Fix:**
  ```python
  # Always add identity self-loops and clamp degree minimums:
  I = torch.eye(N, device=adj.device)
  adj_with_loops = adj + I
  d_out = torch.sum(adj_with_loops, dim=1, keepdim=True).clamp(min=1e-5)
  P_fwd = adj_with_loops / d_out
  ```

---

### Error 5.3: PyTorch CUDA Out of Memory (GPU OOM) on 4D Tensors
* **Software Message:**  
  `"torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 2.40 GiB."`
* **Root Cause:** High-resolution multi-modal batches (`[B=32, T=24, N=14, F=12]` plus Conv2D satellite rasters `[32, 3, 256, 256]`) retain intermediate activation graphs across all 15 lead-time steps.
* **Step-by-Step Fix:**
  1. **Use Gradient Accumulation:** Reduce physical batch size from 32 to 8, accumulating gradients over 4 steps:
     ```python
     loss = loss / 4
     loss.backward()
     if (step + 1) % 4 == 0:
         optimizer.step()
         optimizer.zero_grad()
     ```
  2. **Enable Automatic Mixed Precision (`torch.amp`):**
     ```python
     from torch.amp import autocast, GradScaler
     scaler = GradScaler('cuda')
     with autocast('cuda'):
         outputs = model(nwp_grid, sat_grid, seq_feats, node_feats, adj_matrix)
         loss, _ = pinn_criterion(outputs["p50"], targets_pm10, u_star, u_star_t, adj_matrix)
     scaler.scale(loss).backward()
     scaler.step(optimizer)
     scaler.update()
     ```

---

## 🌐 6. Operational Data, Microservice & Production Errors

---

### Error 6.1: UTC vs CST (China Standard Time) 8-Hour Phase Shift
* **Symptom:** The model consistently predicts maximum dust storm arrival at midnight, but observations show peak storms hitting at 4:00 PM local time.
* **Root Cause:** ECMWF and CMA numerical models report timestamps in **UTC (00:00, 12:00 UTC)**, whereas Ministry of Ecology and Environment (MEE) Chinese station monitors log in **Beijing Time (CST / UTC+8)**. Failing to explicitly harmonize timezones creates a lethal 8-hour diurnal lag.
* **Step-by-Step Fix:**
  ```python
  import pandas as pd

  # Harmonize all observations explicitly to UTC prior to alignment
  df_obs['datetime_utc'] = pd.to_datetime(df_obs['local_time']).dt.tz_localize('Asia/Shanghai').dt.tz_convert('UTC')
  ```

---

### Error 6.2: CDS API Deadlock & Request Timeouts (ERA5 Ingestion)
* **Software Message:**  
  `"cdsapi.exceptions.HTTPError: 504 Gateway Time-out. Request queued for > 12 hours."`
* **Root Cause:** Requesting multi-gigabyte continuous global ERA5 hourly chunks covering all 137 vertical pressure levels in a single `cdsapi` call. The ECMWF queue blocks massive single requests.
* **Step-by-Step Fix:**
  1. Break requests down by **monthly chunks** and **spatial bounding boxes**:
     ```python
     # Restrict to East Asian domain bounding box: North, West, South, East
     'area': [55, 70, 25, 135],
     # Request only necessary vertical levels:
     'pressure_level': ['500', '700', '850', '925', '1000'],
     ```
  2. Add automated exponential retry backoff logic with `tenacity` or `urllib3`.

---

### Error 6.3: FastAPI CORS Blocking & Pydantic Validation Error (HTTP 422)
* **Symptom:** React frontend cannot receive predictions from `http://127.0.0.1:8000`, logging:  
  `"Access to fetch at '...' from origin 'http://localhost:5173' has been blocked by CORS policy"` or `"HTTP 422 Unprocessable Entity"`.
* **Root Cause:**
  1. Missing CORS middleware headers allowing Vite's development origin.
  2. Pydantic request model expects `float` for `u10_wind_speed`, but React sent an unparsed string `"12.4"` from an `<input type="range">`.
* **Step-by-Step Fix:**
  * **In `Ai Pipline/api/server.py`:**
    ```python
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```
  * **In Pydantic schema, use lenient type coercing:**
    ```python
    from pydantic import BaseModel, Field

    class ForecastRequest(BaseModel):
        station_id: str
        lead_time_hours: int = Field(ge=3, le=360)
        u10_wind_speed: float
        soil_moisture: float
    ```

---

## 📋 Comprehensive Emergency Triage Cheatsheet

| Symptom / Error | Immediate Suspect | 60-Second Emergency Remedy |
| :--- | :--- | :--- |
| **AMOS:** Error variance negative (`e < 0`) | Heywood case | Fix variance of error to `0.005` in object properties. |
| **SPSS:** Little's MCAR $p < .05$ | Missing Not at Random | Replace Listwise deletion with Multiple Imputation (FCS). |
| **GIS:** Stations appear in wrong hemisphere | CRS mismatch (WGS84 vs Metric) | Use `gdf.to_crs(epsg=32650)`, never manually assign `.crs`. |
| **Line A:** $P_{10} > P_{50}$ | Quantile crossing | Apply `np.sort()` or softplus cumulative gap parametrization. |
| **Line A:** TS $= 0$ for severe storm class | Extreme class imbalance | Add cost matrix ($\text{Cost}_{\text{Miss}} = 50 \times \text{Cost}_{\text{FalseAlarm}}$). |
| **Line B:** PyTorch loss returns `NaN` | PDE gradient explosion | Add `clip_grad_norm_(max_norm=2.0)` and Huber loss. |
| **Pipeline:** 8-hour peak forecast lag | UTC vs China Beijing Time | Convert ground timestamps: `tz_localize('Asia/Shanghai').tz_convert('UTC')`. |
| **API:** HTTP 422 Unprocessable Entity | String sent instead of float | Parse slider values with `parseFloat()` in React before POST. |
