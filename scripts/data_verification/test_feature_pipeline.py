import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr

nc_path = Path("data/raw/nwp/cams_forecast_saudi_arabia.nc")
ds = xr.open_dataset(nc_path)
print("Dataset loaded:", ds.sizes)

df_raw = ds[["pm10", "duaod550", "u10", "v10"]].to_dataframe().reset_index()

df_features = pd.DataFrame()
df_features["ref_time"] = df_raw["forecast_reference_time"]
df_features["valid_time"] = df_raw["valid_time"]
df_features["lead_hours"] = df_raw["forecast_period"].dt.total_seconds() / 3600.0 if np.issubdtype(df_raw["forecast_period"].dtype, np.timedelta64) else df_raw["forecast_period"]
df_features["latitude"] = df_raw["latitude"]
df_features["longitude"] = df_raw["longitude"]
df_features["nwp_pm10_ugm3"] = df_raw["pm10"] * 1e9
df_features["nwp_aod550"] = df_raw["duaod550"]
df_features["u10"] = df_raw["u10"]
df_features["v10"] = df_raw["v10"]

df_features["wind_speed_10m"] = np.sqrt(df_features["u10"]**2 + df_features["v10"]**2)
df_features["wind_power_flux"] = df_features["wind_speed_10m"]**3

VON_KARMAN = 0.40
ROUGHNESS_Z0 = 0.001
U_STAR_THRESH = 0.28
HEIGHT_Z = 10.0

df_features["u_star"] = (VON_KARMAN * df_features["wind_speed_10m"]) / np.log(HEIGHT_Z / ROUGHNESS_Z0)
df_features["is_saltating"] = (df_features["u_star"] > U_STAR_THRESH).astype(int)

out_dir = Path("data/processed")
out_dir.mkdir(parents=True, exist_ok=True)
parquet_path = out_dir / "saudi_nwp_engineered_features.parquet"
df_features.to_parquet(parquet_path, index=False)
print("Pipeline verified! Parquet written:", parquet_path, f"({parquet_path.stat().st_size / 1e6:.2f} MB)")
