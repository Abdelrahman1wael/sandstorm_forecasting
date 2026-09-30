# 🗺️ GIS (ArcGIS Pro / QGIS): Complete Spatial Science & Analytics Roadmap
### *From Vector Geoprocessing and Kriging Interpolation to Spatial Autocorrelation and GWR*

---

## 🌟 Executive Overview & Role in Empirical Research

**Geographic Information Systems (GIS)** provide the essential **spatial foundation** that transforms tabular statistics into geographical intelligence. In environmental disasters, air quality, urban planning, and socio-ecological research, GIS fulfills three decisive roles:
1. **Spatial Feature Engineering**: Extracting environmental exposure variables (satellite AOD, vegetation indices, elevation, distance to desert emission corridors) to feed into machine learning models and SPSS datasets.
2. **Spatial Pattern & Autocorrelation Analysis**: Proving whether disaster exposure, disease incidence, or social vulnerability are clustered in geographic space (violating standard OLS independence assumptions).
3. **Local Spatial Econometrics & Cartography**: Fitting Geographically Weighted Regression (GWR) to demonstrate how causal relationships vary across regions, and producing publication-grade thematic maps for top-tier journals.

```
+-----------------------------------------------------------------------------------+
|                           GIS SPATIAL WORKFLOW PIPELINE                           |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Multi-Source Spatial Ingestion]                                                 |
|   • Remote Sensing Grids: MODIS/FY-4 AOD, Sentinel NDVI, SRTM DEM, ERA5 Reanalysis|
|   • Vector Features: Sampling Coordinates, Dust Corridors, County Boundaries      |
|                                |                                                  |
|                                v                                                  |
|  [Stage 1: Geoprocessing]      CRS Reprojection (WGS84 -> UTM/CGCS2000)           |
|                                Multi-Ring Buffer Zones • Spatial Joins            |
|                                |                                                  |
|                                v                                                  |
|  [Stage 2: Surface Analysis]   Zonal Statistics (Mean Exposure per County)        |
|                                Geostatistical Ordinary Kriging (Semivariogram)    |
|                                |                                                  |
|                                v                                                  |
|  [Stage 3: Spatial Statistics] Spatial Weights Matrix (W: Queen / k-NN)           |
|                                Global Moran's I (Spatial Clustering Test)         |
|                                Local LISA & Getis-Ord Gi* Hot Spot Mapping        |
|                                |                                                  |
|                                v                                                  |
|  [Stage 4: Spatial Econometrics] Spatial Lag / Error Models (GeoDa)               |
|                                Geographically Weighted Regression (GWR / MGWR)    |
|                                |                                                  |
|                                v                                                  |
|  [Stage 5: Cartography]        Publication-Ready Multi-Layer Thematic Maps (300DPI|
+-----------------------------------------------------------------------------------+
```

---

## 🧭 Phase 1: Spatial Data Architecture, CRS & Georeferencing

### 1.1 Data Models in Environmental Science
* **Vector Data Models**:
  * **Points**: Monitoring stations, survey respondent households, industrial emission stacks.
  * **Lines**: Desert transport corridor centerlines, fault lines, railway arteries, river networks.
  * **Polygons**: Administrative jurisdictions (counties, prefectures, provinces), desert basins, urban ecological redlines.
* **Raster Data Models**:
  * Continuous grids storing physical values per pixel: Digital Elevation Models (DEM), MODIS/FY-4 Aerosol Optical Depth (AOD), Landsat/Sentinel-2 NDVI, ERA5 atmospheric reanalysis grids ($0.125^\circ \times 0.125^\circ$).

### 1.2 Coordinate Reference Systems (CRS) & The "Buffer Distortion Trap"
* **Geographic CRS (GCS)**:
  * E.g., **WGS84 (EPSG:4326)** or **CGCS2000 (EPSG:4490)**.
  * Measures coordinates in **angular degrees** (latitude/longitude).
  * **The Fatal Trap**: Creating a "10km buffer" in WGS84 treats $10$ as $10^\circ$, covering thousands of kilometers!
* **Projected Coordinate Systems (PCS)**:
  * Projects spherical earth onto a 2D Cartesian plane in **linear meters**.
  * Universal Transverse Mercator (**UTM Zones**, e.g., UTM Zone 48N–50N for China).
  * Equal Area projections (e.g., **Albers Equal Area Conic** for nationwide spatial area calculations).
  * **Golden Rule**: Always project all vector and raster layers into the same local Projected Coordinate System before executing proximity, distance, or area calculations.

### 1.3 Geocoding & Spatial Joins
* **Address Geocoding**: Converting addresses or latitude/longitude tables (CSV/Excel) into geospatial Shapefiles (`.shp`) or GeoPackages (`.gpkg`).
* **Spatial Join (`Target: Polygons`, `Join: Points`)**:
  * Summarizes points within each administrative boundary (e.g., calculating average survey risk perception score or count of industrial plants per county).

---

## ⚡ Phase 2: Geoprocessing, Zonal Extraction & Kriging Interpolation

### 2.1 Vector Proximity Operations
* **Buffer Analysis**:
  * Creating defined geographic zones around dust emission corridors or highways (e.g., 5 km, 15 km, 30 km bands).
* **Overlay & Geometric Operations**:
  * **Clip**: Slicing raster or vector datasets to exact study area boundaries.
  * **Intersect**: Identifying overlapping geographical areas between high vulnerability zones and dust plumes.
  * **Dissolve**: Aggregating sub-district polygons into unified regional administrative units.

### 2.2 Surface Analysis & Spatial Interpolation
Continuous environmental phenomena (dust particulate PM10 concentration, surface temperature) are measured at discrete monitoring stations and must be interpolated continuously across geography.

* **Inverse Distance Weighting (IDW)**:
  * Deterministic technique based on Tobler’s First Law: closer points have greater influence.
  * Fast, but does not quantify prediction uncertainty and suffers from "bullseye" artifacts around sensor nodes.
* **Geostatistical Interpolation: Ordinary Kriging**:
  * Calculates optimal linear unbiased predictions based on the **Spatial Semivariogram**:
    $$\gamma(h) = \frac{1}{2N(h)} \sum_{i=1}^{N(h)} (Z(s_i) - Z(s_i + h))^2$$
  * Semivariogram Parameters:
    * **Nugget ($C_0$)**: Measurement error or micro-scale variation at zero distance.
    * **Sill ($C_0 + C$)**: Total plateau variance where spatial correlation ceases.
    * **Range ($a$)**: Distance threshold beyond which observations are spatially independent.
  * Fit theoretical models (Spherical, Exponential, Gaussian) and evaluate Cross-Validation RMSE.

### 2.3 Zonal Statistics (The Bridge to Tabular Statistics)
* **Tool**: `Spatial Analyst > Zonal > Zonal Statistics as Table`.
* Ingests continuous raster layers (e.g., 5-year mean satellite AOD, terrain slope, NDVI) and aggregates them into administrative vector polygons:
  * Computes `MEAN`, `SUM`, `STD`, `MAX` values per county.
* **Export**: Output table exported as CSV/Excel, ready to merge directly into the SPSS master dataset!

---

## 🌐 Phase 3: Spatial Autocorrelation & Cluster Detection

Traditional statistics (OLS regression, ANOVA) assume that observations are Independent and Identically Distributed (i.i.d.). Spatial phenomena violate this assumption because nearby locations influence one another (**Tobler’s First Law of Geography**).

### 3.1 Spatial Weights Matrix ($W$)
Quantifies the neighborhood spatial connectivity structure among $n$ spatial units:
* **Contiguity-Based**:
  * **Rook**: Sharing a common linear boundary edge.
  * **Queen**: Sharing a common boundary edge or corner vertex.
* **Distance-Based**:
  * **$k$-Nearest Neighbors ($k$-NN)**: Ensures every unit has exactly $k$ neighbors (prevents island isolates in remote desert basins).
  * **Inverse Distance Band**: Weights decay continuously with Euclidean distance ($w_{ij} = 1/d_{ij}^\alpha$).
* **Standardization**: Row-standardization ($\sum_j w_{ij} = 1$) so that $W \cdot y$ represents the local spatial lag (neighborhood weighted average).

### 3.2 Global Spatial Autocorrelation (Global Moran's I)
Evaluates whether an environmental or socioeconomic variable is clustered, dispersed, or random across the entire study area:
$$I = \frac{n}{\sum_{i=1}^n \sum_{j=1}^n w_{ij}} \cdot \frac{\sum_{i=1}^n \sum_{j=1}^n w_{ij}(x_i - \bar{x})(x_j - \bar{x})}{\sum_{i=1}^n (x_i - \bar{x})^2}$$

* **Statistical Inference**:
  * Standardized $Z$-Score:
    $$Z_I = \frac{I - E[I]}{\sqrt{\text{Var}(I)}}, \quad \text{where } E[I] = -\frac{1}{n - 1}$$
* **Decision Rules**:
  * $Z_I > +1.96$ ($p < 0.05$): Statistically significant **Spatial Clustering** (similar values cluster together).
  * $Z_I < -1.96$ ($p < 0.05$): Statistically significant **Spatial Dispersion** (checkerboard pattern).
  * $-1.96 \le Z_I \le +1.96$: Random geographic distribution.

### 3.3 Local Indicators of Spatial Association (LISA)
Local Moran’s $I_i$ decomposes the global index into localized spatial clusters:
1. **High-High (Hot Spots)**: High values surrounded by high values (e.g., severe dust exposure and high economic loss).
2. **Low-Low (Cold Spots)**: Low values surrounded by low values.
3. **High-Low (Spatial Outliers)**: High value surrounded by low values.
4. **Low-High (Spatial Outliers)**: Low value surrounded by high values.

### 3.4 Getis-Ord Gi\* Hot Spot Analysis
Identifies statistically significant spatial concentrations of high values (Hot Spots) and low values (Cold Spots):
$$G_i^* = \frac{\sum_{j=1}^n w_{ij} x_j - \bar{X} \sum_{j=1}^n w_{ij}}{S \sqrt{\frac{n \sum_{j=1}^n w_{ij}^2 - (\sum_{j=1}^n w_{ij})^2}{n - 1}}}$$
* Render maps displaying **90%, 95%, and 99% Confidence Hot Spots** (crimson red) and **Cold Spots** (deep blue).

---

## 📈 Phase 4: Spatial Econometrics & Geographically Weighted Regression (GWR)

When spatial autocorrelation exists in regression residuals, ordinary OLS regression in SPSS is invalid because $p$-values are falsely inflated. Spatial modeling resolves this.

```
+---------------------------------------------------------------------------------+
|                       SPATIAL ECONOMETRIC MODEL SELECTION                       |
+---------------------------------------------------------------------------------+
|  1. Fit Baseline OLS Regression:                                                |
|     Y = Xβ + ε                                                                  |
|                                                                                 |
|  2. Check Moran's I of OLS Residuals:                                           |
|     • If Residuals Moran's I is NOT significant (p > 0.05): Standard OLS holds! |
|     • If Residuals Moran's I is SIGNIFICANT (p < 0.05): Spatial Model Required! |
|                                                                                 |
|  3. Run Anselin Lagrange Multiplier (LM) Diagnostics in GeoDa / R:              |
|     • LM-Lag significant -> Spatial Lag Model (SAR):                            |
|       Y = ρ W Y + Xβ + ε   (Spatial spillover effect)                           |
|     • LM-Error significant -> Spatial Error Model (SEM-spatial):                |
|       Y = Xβ + u, where u = λ W u + ε   (Omitted spatially clustered variables) |
|                                                                                 |
|  4. If Spatial Heterogeneity Exists across Geography:                           |
|     • Fit Geographically Weighted Regression (GWR / MGWR):                      |
|       Y_i = β_0(u_i, v_i) + ∑_k β_k(u_i, v_i) X_ik + ε_i                        |
+---------------------------------------------------------------------------------+
```

### 4.1 Geographically Weighted Regression (GWR) Mechanics
Instead of estimating a single global regression coefficient ($\beta_k$) that applies uniformly across China, GWR estimates **local, spatially varying parameters** ($\beta_k(u_i, v_i)$) at every geographic coordinate:
$$\hat{\beta}(u_i, v_i) = \left(X^T W(u_i, v_i) X\right)^{-1} X^T W(u_i, v_i) Y$$

* **Spatial Kernel Function**:
  * **Adaptive Bisquare / Gaussian Kernel**: Adjusts kernel bandwidth dynamically based on sample density (wider in sparsely populated desert basins, narrower in dense downstream cities).
  * **Bandwidth Optimization**: Selected via corrected Akaike Information Criterion (**AICc**) or Cross-Validation (CV).
* **Key Deliverables from GWR**:
  * **Local $R_i^2$ Maps**: Shows where the model explains $80\%$ of variance vs where unexplained gaps remain.
  * **Local $\beta(u_i, v_i)$ Coefficient Maps**: Visualizes how the impact of early warning lead time or vegetation cover changes in strength from the Gansu desert gateway to the North China plain.

---

## 🎨 Phase 5: Publication-Grade Scientific Cartography

Cartographic design standards for publication in *Nature*, *Science of the Total Environment*, or *Atmospheric Environment*:

1. **Hierarchy & Composition**:
   * Clear focal subject with national/provincial inset map showing regional context.
   * Coordinate grid (Graticule) with subtle tick marks (e.g., $100^\circ\text{E}, 35^\circ\text{N}$).
2. **Color Schemes (ColorBrewer Standards)**:
   * **Sequential (Single/Multi-hue)**: Continuous variables (PM10 concentration, AOD) from light yellow to deep orange/red.
   * **Diverging**: Hot spot $Z$-scores or standardized residuals (Blue $\rightarrow$ Neutral White $\rightarrow$ Red). Never use green-red combinations for accessibility (color-blind friendly).
   * **Categorical**: Discrete land cover or hazard zones.
3. **Essential Map Elements**:
   * Subdued, non-distracting North Arrow.
   * Linear Scale Bar formatted in rounded metric units (e.g., $0, 200, 400\ \text{km}$).
   * Complete CRS citation: `Projection: Albers Equal Area Conic, Datum: CGCS2000`.
4. **Resolution Export**:
   * Minimum **300 DPI** (ideally 600 DPI) in TIFF or vector PDF format.

---

## ⚠️ Common GIS Pitfalls & Solutions

| Pitfall | Consequence | Professional Remedy |
| :--- | :--- | :--- |
| **Mixing Projected and Geographic CRS** | Distorted area calculations and failed buffer radii. | Reproject all shapefiles and rasters to the same local Projected CRS (e.g., UTM or Albers). |
| **Running GWR with Global Multicollinearity** | Local coefficient instability and inflated local standard errors. | Screen VIF in SPSS first ($\text{VIF} < 3.0$ for GWR); check condition number in GWR output. |
| **Using Fixed Bandwidth in Heterogeneous Regions** | Desert basins have too few points while cities have too many. | Use an **Adaptive Bisquare Kernel** based on a fixed number of neighbors. |
| **Treating Missing Raster Pixels as Value 0** | Severely drags down county averages in Zonal Statistics. | Set missing pixels explicitly to `NoData` before running zonal extraction. |

---

## 📚 Recommended Software & Reference Literature

* **Software Toolkit**:
  * **ArcGIS Pro** (v3.x) or **QGIS** (v3.34+ LTR) with GRASS / SAGA integration.
  * **GeoDa** (v1.22+) for Exploratory Spatial Data Analysis (ESDA) and spatial lag/error modeling.
  * **MGWR Software** (v2.2+) from Arizona State University for Multiscale GWR.
* **Key Literature**:
  1. Anselin, L. (1988). *Spatial Econometrics: Methods and Models*. Kluwer Academic Publishers.
  2. Fotheringham, A. S., Brunsdon, C., & Charlton, M. (2002). *Geographically Weighted Regression: The Analysis of Spatially Varying Relationships*. John Wiley & Sons.
  3. Goodchild, M. F., et al. (2020). *Geographic Information Science and Systems* (5th Edition). Wiley.
