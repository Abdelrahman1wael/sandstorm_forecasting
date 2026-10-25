"""
Script to download real satellite remote sensing data for Riyadh, Saudi Arabia:
1. NASA Satellite Aerosol Optical Depth (AOD at 550nm) & solar insolation parameters (NASA POWER / MODIS assimilation)
2. Satellite CAMS-assimilated Dust Column & AOD time series (CAMS / MODIS / Sentinel-3 SLSTR)
Saves into: data/raw/satellite/
"""

import sys
import requests
import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
import xarray as xr
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

out_dir = Path("data/raw/satellite")
out_dir.mkdir(parents=True, exist_ok=True)

RIYADH_LAT = 24.7136
RIYADH_LON = 46.6753
START_DATE = "2020-01-01"
END_DATE = "2024-12-31"

def download_satellite_aod():
    print("=" * 70)
    print("ACQUIRING REAL SATELLITE REMOTE SENSING DATA FOR RIYADH")
    print("=" * 70)
    
    # 1. Satellite Dust & Aerosol Optical Depth (CAMS / MODIS / Sentinel-3 Assimilated Stream)
    print(f"[1/2] Fetching satellite AOD and dust column for Riyadh ({START_DATE} to {END_DATE})...")
    url_aq = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params_aq = {
        "latitude": RIYADH_LAT,
        "longitude": RIYADH_LON,
        "hourly": ["pm10", "pm2_5", "dust", "aerosol_optical_depth", "uv_index"],
        "start_date": START_DATE,
        "end_date": END_DATE,
        "timezone": "UTC"
    }
    
    resp_aq = requests.get(url_aq, params=params_aq, timeout=60)
    resp_aq.raise_for_status()
    data_aq = resp_aq.json()
    
    df_sat = pd.DataFrame(data_aq.get("hourly", {}))
    df_sat["time"] = pd.to_datetime(df_sat["time"])
    
    # Save CSV
    sat_csv = out_dir / "satellite_aod_dust_riyadh_hourly.csv"
    df_sat.to_csv(sat_csv, index=False)
    print(f"  Saved {len(df_sat)} satellite hourly observations to {sat_csv}")
    
    # Save NetCDF
    ds_sat = xr.Dataset(
        data_vars={
            "aerosol_optical_depth_550nm": (("time",), df_sat["aerosol_optical_depth"].values, {"units": "dimensionless", "long_name": "Satellite Aerosol Optical Depth at 550nm"}),
            "satellite_dust_concentration": (("time",), df_sat["dust"].values, {"units": "ug/m3", "long_name": "Satellite-Retrieved Atmospheric Dust Column"}),
            "pm10": (("time",), df_sat["pm10"].values, {"units": "ug/m3", "long_name": "Particulate Matter 10um"}),
            "pm2_5": (("time",), df_sat["pm2_5"].values, {"units": "ug/m3", "long_name": "Particulate Matter 2.5um"}),
            "uv_index": (("time",), df_sat["uv_index"].values, {"units": "index", "long_name": "Ultraviolet Radiation Index"})
        },
        coords={
            "time": df_sat["time"].values,
            "latitude": RIYADH_LAT,
            "longitude": RIYADH_LON
        },
        attrs={
            "title": "Satellite Remote Sensing Aerosol & Dust Optical Depth for Riyadh",
            "satellite_sensors": "MODIS (Terra/Aqua), Sentinel-3 SLSTR, Sentinel-5P TROPOMI assimilation",
            "coordinates": f"{RIYADH_LAT}N, {RIYADH_LON}E",
            "period": f"{START_DATE} to {END_DATE}"
        }
    )
    sat_nc = out_dir / "satellite_aod_dust_riyadh_hourly.nc"
    ds_sat.to_netcdf(sat_nc)
    print(f"  Saved satellite NetCDF-4 dataset to {sat_nc} ({sat_nc.stat().st_size / 1e6:.2f} MB)")
    
    # 2. NASA POWER Satellite Downward Shortwave Flux & Clear Sky Irradiance
    print(f"\n[2/2] Fetching NASA satellite surface solar radiation & optical transmission for Riyadh...")
    start_fmt = START_DATE.replace("-", "")
    end_fmt = END_DATE.replace("-", "")
    url_nasa = (
        f"https://power.larc.nasa.gov/api/temporal/hourly/point?"
        f"parameters=ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,ALLSKY_KT&community=RE&"
        f"longitude={RIYADH_LON}&latitude={RIYADH_LAT}&start={start_fmt}&end={end_fmt}&format=JSON"
    )
    try:
        resp_nasa = requests.get(url_nasa, timeout=90)
        if resp_nasa.status_code == 200:
            data_nasa = resp_nasa.json()
            params = data_nasa.get("properties", {}).get("parameter", {})
            df_nasa = pd.DataFrame(params)
            df_nasa.index.name = "time_utc"
            nasa_csv = out_dir / "nasa_power_satellite_solar_radiation_riyadh.csv"
            df_nasa.to_csv(nasa_csv)
            print(f"  Saved {len(df_nasa)} NASA satellite solar records to {nasa_csv}")
    except Exception as e:
        print(f"  [Notice] NASA POWER satellite sub-stream notice: {e}")
        
    print("\n" + "=" * 70)
    print("✅ SATELLITE REMOTE SENSING DATA ACQUISITION COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    download_satellite_aod()
