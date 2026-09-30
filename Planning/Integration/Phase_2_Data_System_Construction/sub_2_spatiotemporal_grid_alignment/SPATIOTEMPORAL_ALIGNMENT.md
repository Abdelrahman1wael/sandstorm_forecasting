# 🌐 Phase 2 • Subfolder 2: Spatiotemporal Grid Alignment
### *Standardizing to 5km WGS84 Mesh, Conservative Remapping & UTC Synchronization*
**Phase Horizon:** January 2026 – April 2026  
**Parent Phase:** Phase 2 (Data System Construction)

---

## 🎯 1. Operational Goal & Alignment Specifications

Phase 2.2 maps multi-source datasets with conflicting coordinate reference systems, cell sizes, and time zones onto a single **Unified Spatiotemporal Reference Grid**:

```
Dataset:                  Original CRS:     Original Resolution:  Target Harmonized Grid:
-----------------------------------------------------------------------------------------
ECMWF IFS Forecasts:      Reduced Gaussian  0.1° (~9 km)          0.1° / 5km Regular WGS84
ERA5 Reanalysis:          Regular Lat/Lon   0.25° (~25 km)        0.1° / 5km Bilinear Remap
MODIS Deep Blue AOD:      Orbital Swath     10 km sinusoidal      0.1° / 5km Nearest/Bilinear
MEE Ground Stations:      Point Vector      Discrete Lat/Lon      Nearest Node & k-d tree
Elevation (SRTM DEM):     Geographic        90 meters             Aggregated Mean & TRI
Time Baseline:            Mixed (CST & UTC) Irregular intervals   Strict UTC Hourly & 6-Hourly
```

---

## 📐 2. Bilinear & Conservative Remapping Formulas

For continuous variables ($Z_{500}, T_{850}, U_{10}$), values on the target grid $(x_t, y_t)$ are calculated using 4-point bilinear interpolation:
$$f(x_t, y_t) = \frac{1}{(x_2 - x_1)(y_2 - y_1)} \begin{pmatrix} x_2 - x_t & x_t - x_1 \end{pmatrix} \begin{pmatrix} f(Q_{11}) & f(Q_{12}) \\ f(Q_{21}) & f(Q_{22}) \end{pmatrix} \begin{pmatrix} y_2 - y_t \\ y_t - y_1 \end{pmatrix}$$

For particulate flux and total precipitation, 1st-order conservative remapping is used to guarantee that integrated aerosol mass is strictly preserved across grid cells:
$$\int_{\mathcal{A}_{\text{target}}} \phi \, dA = \sum_{k} \int_{\mathcal{A}_k \cap \mathcal{A}_{\text{target}}} \phi \, dA$$

---

## 📋 3. Phase 2.2 Deliverables
* Fully reprojected multi-channel NetCDF4 cubes over East Asia ($70^\circ\text{E} - 135^\circ\text{E}, 25^\circ\text{N} - 55^\circ\text{N}$).
* Certified zero-phase-lag timestamp alignment verified against solar noon.
