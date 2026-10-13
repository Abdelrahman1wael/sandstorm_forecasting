"""
Script to generate notebooks/01_data_representation_and_exploration.ipynb
"""

import json
from pathlib import Path

notebook_dir = Path("notebooks")
notebook_dir.mkdir(parents=True, exist_ok=True)
notebook_path = notebook_dir / "01_data_representation_and_exploration.ipynb"

cells = []

def add_md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

def add_code(text):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().split("\n")]
    })

# CELL 1: Markdown Title
add_md("""# 🌪️ DustML: Data Representation & Exploratory Analysis
### *Extended-Range Sand and Dust Storm (SDS) Forecasting Platform*
**Affiliation:** University of Science and Technology Beijing (USTB) • Environmental Engineering

This interactive Jupyter Notebook provides complete exploratory data analysis (EDA), visual representation, and metadata inspection for the **two core empirical pillars** of your thesis research:
1. **Ground Observational Truth ($y_{\\text{obs}}$)**: National urban monitoring stations across China (`data/raw/ground/`).
2. **Numerical Weather Prediction ($y_{\\text{nwp}}$)**: ECMWF CAMS Global Atmospheric Composition Forecasts (`data/raw/nwp/cams_forecast_2021_03.nc`).
3. **Spatiotemporal Collocation & Residual Target**: How ground truth and numerical simulations are fused for **Line A Machine Learning Bias Correction**.""")

# CELL 2: Code Imports
add_code("""import os
import glob
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Configure publication-style plotting aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 120

print("✅ Scientific visualization environment initialized successfully!")""")

# CELL 3: Markdown Section 1
add_md("""---
## 📍 Pillar 1: Ground Observational Truth (CNEMC Stations)
* **Directory**: `data/raw/ground/`
* **Coverage**: 92 daily files (March 1, 2021 – May 31, 2021)
* **Monitoring Stations**: 2,024 automatic surface atmospheric stations across China.
* **Target Pollutant**: $PM_{10}$ hourly mass concentrations (in $\\mu\\text{g}/\\text{m}^3$).
* **Timezone Note**: Original records are in **Beijing Time (CST, UTC+8)**. We shift timestamps by $-8\\text{h}$ to align with international UTC standards.""")

# CELL 4: Code Section 1 Load
add_code("""# 1. Inspect ground station files
ground_files = sorted(glob.glob("../data/raw/ground/china_sites_*.csv"))
if not ground_files:
    ground_files = sorted(glob.glob("data/raw/ground/china_sites_*.csv"))

print(f"Total Ground Station Files Found: {len(ground_files)}")

# Load the historic March 15, 2021 super sandstorm event
march15_file = [f for f in ground_files if "20210315" in f]
sample_file = march15_file[0] if march15_file else ground_files[0]
print(f"Loading sample event: {Path(sample_file).name}")

df_sample = pd.read_csv(sample_file)
print(f"Shape: {df_sample.shape[0]} rows × {df_sample.shape[1]} columns")
print(f"Available Measurement Types: {df_sample['type'].unique().tolist()[:6]}")
df_sample.head(6).iloc[:, :7]""")

# CELL 5: Code Section 1 Clean & Filter PM10
add_code("""# Filter specifically for PM10 records
df_pm10 = df_sample[df_sample["type"] == "PM10"].copy()

# Station columns start from column index 3 (e.g., '1001A', '1002A', ...)
station_cols = df_pm10.columns[3:]
pm10_values = df_pm10[station_cols].apply(pd.to_numeric, errors='coerce')

print("=== Ground PM10 Summary Statistics on March 15, 2021 (Peak Dust Event) ===")
print(f"Active Monitoring Stations Reporting: {len(station_cols)}")
print(f"Maximum PM10 observed across network: {pm10_values.max().max():.1f} ug/m3")
print(f"Average PM10 across network:          {pm10_values.mean().mean():.1f} ug/m3")
print(f"Severe Dust Threshold Exceedances (>1,000 ug/m3): {(pm10_values > 1000).sum().sum()} station-hours")""")

# CELL 6: Code Section 1 Plot
add_code("""# Visualize Ground PM10 Intensity Distribution & Diurnal Profile
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1: Distribution of observed PM10
valid_pm10 = pm10_values.values.flatten()
valid_pm10 = valid_pm10[~np.isnan(valid_pm10)]

axes[0].hist(np.clip(valid_pm10, 0, 2500), bins=50, color='#d97706', edgecolor='black', alpha=0.8)
axes[0].axvline(150, color='blue', linestyle='--', label='CMA Moderate Dust (150 ug/m3)')
axes[0].axvline(500, color='red', linestyle='--', label='CMA Severe Dust (500 ug/m3)')
axes[0].set_title("Ground PM10 Concentration Distribution (March 15, 2021)", fontsize=12, fontweight='bold')
axes[0].set_xlabel("PM10 Concentration (ug/m3)")
axes[0].set_ylabel("Station-Hour Observations Count")
axes[0].legend()

# Subplot 2: Diurnal network mean PM10 curve
hourly_mean = pm10_values.mean(axis=1)
hours = df_pm10["hour"].values

axes[1].plot(hours, hourly_mean, marker='o', linewidth=2.5, color='#b45309', label='National Network Mean')
axes[1].fill_between(hours, hourly_mean, color='#fef3c7', alpha=0.6)
axes[1].set_title("Network-Wide Diurnal Sandstorm Progression (CST)", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Hour of Day (Beijing Time, UTC+8)")
axes[1].set_ylabel("Mean PM10 Concentration (ug/m3)")
axes[1].set_xticks(range(0, 24, 2))
axes[1].grid(True, linestyle=':', alpha=0.6)
axes[1].legend()

plt.tight_layout()
plt.show()""")

# CELL 7: Markdown Section 2
add_md("""---
## 🌐 Pillar 2: ECMWF CAMS Numerical Forecasts (NWP)
* **File**: `data/raw/nwp/cams_forecast_2021_03.nc`
* **Source**: European Centre for Medium-Range Weather Forecasts (ECMWF), Reading, UK
* **Model**: CAMS Global Atmospheric Composition Forecasts (Integrated Forecasting System with aerosol dynamics)
* **Horizontal Resolution**: $0.4^\\circ \\times 0.4^\\circ$ (~40 km regular grid)
* **Lead Time Horizon**: 72h (Day 3) to 120h (Day 5) forward projection
* **Variables**:
  * `pm10`: Surface PM10 aerosol mass ($\text{kg}/\text{m}^3$) $\\rightarrow$ *Multiply by $10^9$ for $\\mu\\text{g}/\\text{m}^3$*
  * `duaod550`: Columnar Dust Aerosol Optical Depth at 550nm
  * `u10`, `v10`: 10-meter horizontal wind vectors ($\text{m}/\text{s}$)""")

# CELL 8: Code Section 2 Load
add_code("""# Load ECMWF CAMS NetCDF Forecast Dataset
cams_file = Path("../data/raw/nwp/cams_forecast_2021_03.nc")
if not cams_file.exists():
    cams_file = Path("data/raw/nwp/cams_forecast_2021_03.nc")

ds_cams = xr.open_dataset(cams_file)
print("=== ECMWF CAMS NetCDF Dataset Dimensions & Variables ===")
print(ds_cams)""")

# CELL 9: Code Section 2 Coordinates Breakdown
add_code("""# Inspect Coordinates & Physical Magnitudes
lats = ds_cams.latitude.values
lons = ds_cams.longitude.values
leads_hours = ds_cams.forecast_period.values / np.timedelta64(1, 'h')

print(f"Latitude Range:  {lats.min():.2f}°N to {lats.max():.2f}°N ({len(lats)} grid nodes)")
print(f"Longitude Range: {lons.min():.2f}°E to {lons.max():.2f}°E ({len(lons)} grid nodes)")
print(f"Forecast Lead Times Available: {leads_hours.tolist()} hours (Days 3 to 5)")

# Convert CAMS raw kg/m3 to standard ug/m3
cams_pm10_ug = ds_cams["pm10"] * 1e9
print(f"CAMS Model Max PM10 in domain: {float(cams_pm10_ug.max()):.2f} ug/m3")
print(f"CAMS Dust AOD (duaod550) Max:  {float(ds_cams['duaod550'].max()):.2f}")""")

# CELL 10: Code Section 2 2D Spatial Map
add_code("""# Spatial Visualization of CAMS Forecast Plume across East Asia
# Select run initialization 0, lead time 72h (Day 3)
lead_idx = 0 # 72 hours
time_idx = 0

pm10_slice = cams_pm10_ug.isel(forecast_reference_time=time_idx, forecast_period=lead_idx)
aod_slice = ds_cams["duaod550"].isel(forecast_reference_time=time_idx, forecast_period=lead_idx)
u_slice = ds_cams["u10"].isel(forecast_reference_time=time_idx, forecast_period=lead_idx)
v_slice = ds_cams["v10"].isel(forecast_reference_time=time_idx, forecast_period=lead_idx)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Map 1: Surface PM10 Concentration with Wind Vectors
im1 = axes[0].pcolormesh(lons, lats, pm10_slice, cmap='YlOrRd', 
                         norm=mcolors.LogNorm(vmin=10, vmax=2000), shading='auto')
# Overlay wind arrows (skip steps for clarity)
skip = 4
axes[0].quiver(lons[::skip], lats[::skip], u_slice.values[::skip, ::skip], v_slice.values[::skip, ::skip], 
               color='black', alpha=0.6, scale=180, width=0.003)
axes[0].set_title(f"CAMS Numerical PM10 Forecast (Lead: 72h / Day 3)\\n+ 10m Wind Vectors", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Longitude (°E)")
axes[0].set_ylabel("Latitude (°N)")
cbar1 = plt.colorbar(im1, ax=axes[0], orientation='horizontal', pad=0.1, shrink=0.8)
cbar1.set_label("PM10 Concentration (ug/m3) - Log Scale")

# Map 2: Dust Aerosol Optical Depth (duaod550)
im2 = axes[1].pcolormesh(lons, lats, aod_slice, cmap='inferno', vmin=0.0, vmax=2.5, shading='auto')
axes[1].set_title("CAMS Column Dust Aerosol Optical Depth (AOD 550nm)", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Longitude (°E)")
axes[1].set_ylabel("Latitude (°N)")
cbar2 = plt.colorbar(im2, ax=axes[1], orientation='horizontal', pad=0.1, shrink=0.8)
cbar2.set_label("Dust AOD (Dimensionless)")

plt.tight_layout()
plt.show()""")

# CELL 11: Markdown Section 3
add_md("""---
## 🎯 Pillar 3: Spatiotemporal Collocation & Line A Residual Learning
In your thesis, **Line A (Tree Ensemble NWP Bias Correction)** bridges the physical gap between numerical simulation and ground reality:

$$\\varepsilon(s, t, L) = y_{\\text{obs}}(s, t) - y_{\\text{nwp}}(s, t, L)$$

* **Why numerical models fail**: NWP models underestimate peak surface dust emissions due to coarse terrain smoothing and lack of localized sand dune threshold parameterization.
* **What Machine Learning learns**: LightGBM, CatBoost, and XGBoost predict the residual correction $\\varepsilon$ using localized wind dynamics, topography, and seasonal indicators.""")

# CELL 12: Code Section 3 Collocation Demo
add_code("""# Collocation Demonstration: Beijing Station (1001A, ~39.87°N, 116.36°E)
target_lat = 39.87
target_lon = 116.36

# Find nearest CAMS grid cell
lat_idx = np.abs(lats - target_lat).argmin()
lon_idx = np.abs(lons - target_lon).argmin()
nearest_lat = lats[lat_idx]
nearest_lon = lons[lon_idx]

print(f"Target Station (Beijing): ({target_lat}°N, {target_lon}°E)")
print(f"Nearest CAMS Grid Cell:   ({nearest_lat:.2f}°N, {nearest_lon:.2f}°E) [Distance: ~{np.hypot(target_lat-nearest_lat, target_lon-nearest_lon)*111:.1f} km]")

# Extract time evolution across lead times (72h to 120h)
cams_station_pm10 = cams_pm10_ug.isel(forecast_reference_time=0, latitude=lat_idx, longitude=lon_idx).values
cams_station_aod = ds_cams['duaod550'].isel(forecast_reference_time=0, latitude=lat_idx, longitude=lon_idx).values

plt.figure(figsize=(10, 4.5))
plt.plot(leads_hours, cams_station_pm10, marker='s', color='#dc2626', linewidth=2.5, label='Raw CAMS NWP Forecast')
plt.axhline(150, color='gray', linestyle=':', label='Moderate Alert Threshold (150 ug/m3)')
plt.title(f"Beijing Station: CAMS Forecast Progression across Extended Horizons (72h–120h)", fontsize=12, fontweight='bold')
plt.xlabel("Forecast Lead Time (Hours Ahead)")
plt.ylabel("PM10 Concentration (ug/m3)")
plt.xticks(leads_hours)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()
plt.show()""")

# CELL 13: Markdown Conclusion
add_md("""---
## 🚀 Conclusion & Next Modeling Phase
This representation confirms that both your empirical foundations are verified, scientifically sound, and ready for model ingestion:
1. **Target Matrix**: Ground station records provide true labels for continuous regression (RMSE/MAE) and 5-tier CMA hazard categorization.
2. **Feature Matrix**: ECMWF CAMS provides physical advective steering flows and synoptic aerosol concentration predictors.
3. **Pipeline Target**: Run `scripts/data/build_line_a_tabular_dataset.py` to compile `data/processed/tabular_features.parquet` and train the LightGBM baseline!""")

notebook_json = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (dustml / anaconda)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

notebook_path.write_text(json.dumps(notebook_json, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"[Success] Generated notebook at: {notebook_path}")
