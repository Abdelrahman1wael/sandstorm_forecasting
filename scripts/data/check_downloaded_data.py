"""
Verification script for downloaded datasets:
  - Station PM10 ground CSVs (quotsoft.net)
  - ERA5 NetCDF reanalysis files (CDS)
  - DEM terrain files (data/raw/gis)
  - NWP forecasts (CAMS / TIGGE in data/raw/nwp)
"""

import glob
from pathlib import Path

print("=" * 60)
print("SANDSTORM FORECASTING DATASET VERIFICATION")
print("=" * 60)

# 1. Ground station files
ground_files = sorted(glob.glob("data/raw/ground/china_sites_*.csv"))
print(f"\n[1] Ground Station CSVs:")
print(f"    Found: {len(ground_files)} files (Expected 92 for 2021-03-01 to 2021-05-31)")
if ground_files:
    try:
        import pandas as pd
        df0 = pd.read_csv(ground_files[0])
        print(f"    Sample file: {Path(ground_files[0]).name}")
        print(f"    Columns (first 6): {df0.columns[:6].tolist()}")
        print(f"    Available pollutant types: {df0['type'].unique().tolist()}")
        pm10_rows = df0[df0["type"] == "PM10"]
        print(f"    PM10 records in sample: {len(pm10_rows)} hours across {len(df0.columns)-3} stations")
    except Exception as e:
        print(f"    Could not read sample file: {e}")
else:
    print("    No ground station files found yet.")

# 2. ERA5 NetCDF files
era5_files = sorted(glob.glob("data/raw/era5/era5_2021_*.nc"))
print(f"\n[2] ERA5 Reanalysis Files:")
print(f"    Found: {len(era5_files)} files (Expected 3: 03, 04, 05)")
if era5_files:
    try:
        import xarray as xr
        ds = xr.open_mfdataset("data/raw/era5/era5_2021_*.nc")
        print(f"    Time range: {ds.time.values[0]} to {ds.time.values[-1]}")
        print(f"    Latitude bounds:  {float(ds.latitude.min()):.2f} to {float(ds.latitude.max()):.2f}")
        print(f"    Longitude bounds: {float(ds.longitude.min()):.2f} to {float(ds.longitude.max()):.2f}")
        print(f"    Variables: {list(ds.data_vars.keys())}")
    except Exception as e:
        print(f"    Could not read ERA5 dataset: {e}")
else:
    print("    No ERA5 NetCDF files found yet.")

# 3. GIS / DEM files
gis_files = list(Path("data/raw/gis").glob("*.*"))
print(f"\n[3] GIS / DEM Elevation Files:")
print(f"    Found: {len(gis_files)} files in data/raw/gis/")

# 4. Forecast files (CAMS / TIGGE)
nwp_files = list(Path("data/raw/nwp").glob("*.*"))
print(f"\n[4] Forecast Data (CAMS / TIGGE):")
print(f"    Found: {len(nwp_files)} files in data/raw/nwp/")

print("\n" + "=" * 60)
