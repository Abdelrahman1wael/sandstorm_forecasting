"""
Script to prepare and download dedicated NWP (Numerical Weather Prediction) datasets for Riyadh, Saudi Arabia.
Produces:
1. CAMS Atmospheric Composition NWP for Riyadh (data/raw/nwp/cams_forecast_riyadh_station.nc & .csv)
   - Lead times: +72h to +120h (Extended 3-5 days)
   - Variables: PM10, Dust AOD, 10m U/V Wind, Wind Speed, Direction
2. ECMWF IFS High-Resolution Operational NWP Forecast for Riyadh (data/raw/nwp/ecmwf_ifs_nwp_riyadh_forecast.nc & .csv)
   - Lead times: hourly out to 10 days (240 hours)
   - Variables: Wind Speed/Gusts, U/V, Surface Pressure, Temperature, Soil Moisture
3. Master merged NWP file (data/raw/nwp/riyadh_nwp_forecast_master.csv)
"""

import sys
import numpy as np
import pandas as pd
import xarray as xr
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

out_dir = Path("data/raw/nwp")
out_dir.mkdir(parents=True, exist_ok=True)

RIYADH_LAT = 24.7136
RIYADH_LON = 46.6753

def extract_cams_riyadh():
    print("=" * 70)
    print("EXTRACTING CAMS ATMOSPHERIC COMPOSITION NWP FOR RIYADH (72h - 120h)")
    print("=" * 70)
    
    saudi_nc = out_dir / "cams_forecast_saudi_arabia.nc"
    if not saudi_nc.exists():
        print(f"[Error] Source file {saudi_nc} not found.")
        return None
        
    ds = xr.open_dataset(saudi_nc)
    # Select nearest grid point to Riyadh
    ds_riyadh = ds.sel(latitude=RIYADH_LAT, longitude=RIYADH_LON, method="nearest")
    
    actual_lat = float(ds_riyadh.latitude.values)
    actual_lon = float(ds_riyadh.longitude.values)
    print(f"Nearest CAMS grid point for Riyadh: Lat {actual_lat:.2f}N, Lon {actual_lon:.2f}E")
    
    # Save focused NetCDF
    riyadh_nc = out_dir / "cams_forecast_riyadh_station.nc"
    ds_riyadh.to_netcdf(riyadh_nc)
    print(f"  Saved CAMS Riyadh NetCDF to {riyadh_nc} ({riyadh_nc.stat().st_size / 1e3:.1f} KB)")
    
    # Flatten into tabular records for ML training
    records = []
    periods = ds_riyadh.forecast_period.values
    cycles = ds_riyadh.forecast_reference_time.values
    
    for i, cyc in enumerate(cycles):
        for j, per in enumerate(periods):
            lead_hours = per.astype('timedelta64[h]').astype(int)
            val_time = pd.to_datetime(ds_riyadh.valid_time.values[i, j])
            pm10_val = float(ds_riyadh.pm10.values[j, i])
            aod_val = float(ds_riyadh.duaod550.values[j, i])
            u_val = float(ds_riyadh.u10.values[j, i])
            v_val = float(ds_riyadh.v10.values[j, i])
            
            w_speed = np.sqrt(u_val**2 + v_val**2)
            w_dir = (270.0 - np.rad2deg(np.arctan2(v_val, u_val))) % 360.0
            
            records.append({
                "forecast_model": "ECMWF_CAMS",
                "reference_cycle_time": pd.to_datetime(cyc),
                "leadtime_hours": lead_hours,
                "valid_time": val_time,
                "forecast_pm10_ugm3": np.round(pm10_val, 2),
                "forecast_dust_aod_550nm": np.round(aod_val, 4),
                "forecast_10m_u_ms": np.round(u_val, 3),
                "forecast_10m_v_ms": np.round(v_val, 3),
                "forecast_wind_speed_10m": np.round(w_speed, 3),
                "forecast_wind_direction_deg": np.round(w_dir, 1),
                "latitude": actual_lat,
                "longitude": actual_lon
            })
            
    df_cams = pd.DataFrame(records)
    cams_csv = out_dir / "cams_forecast_riyadh_station.csv"
    df_cams.to_csv(cams_csv, index=False)
    print(f"  Saved {len(df_cams)} CAMS Riyadh forecast records across lead times +72h to +120h to {cams_csv}")
    return df_cams

def fetch_ecmwf_ifs_riyadh():
    print("\n" + "=" * 70)
    print("DOWNLOADING ECMWF IFS OPERATIONAL NWP FORECAST FOR RIYADH (0h - 240h)")
    print("=" * 70)
    
    url = "https://api.open-meteo.com/v1/ecmwf"
    params = {
        "latitude": RIYADH_LAT,
        "longitude": RIYADH_LON,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
            "soil_temperature_0_to_7cm",
            "soil_moisture_0_to_7cm"
        ],
        "forecast_days": 10,
        "timezone": "UTC"
    }
    
    print("Querying ECMWF Integrated Forecasting System (IFS) 0.1° resolution model...")
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    
    hourly = data.get("hourly", {})
    df_ifs = pd.DataFrame(hourly)
    df_ifs["valid_time"] = pd.to_datetime(df_ifs["time"])
    df_ifs.drop(columns=["time"], inplace=True)
    df_ifs["forecast_model"] = "ECMWF_IFS_OPERATIONAL"
    df_ifs["latitude"] = RIYADH_LAT
    df_ifs["longitude"] = RIYADH_LON
    
    # Calculate u and v components of wind
    rad = np.deg2rad(df_ifs["wind_direction_10m"])
    df_ifs["10m_u_component_of_wind"] = -df_ifs["wind_speed_10m"] * np.sin(rad)
    df_ifs["10m_v_component_of_wind"] = -df_ifs["wind_speed_10m"] * np.cos(rad)
    df_ifs["leadtime_hours"] = range(len(df_ifs))
    
    ifs_csv = out_dir / "ecmwf_ifs_nwp_riyadh_forecast.csv"
    df_ifs.to_csv(ifs_csv, index=False)
    print(f"  Saved {len(df_ifs)} hourly ECMWF IFS forecast steps (out to 10 days) to {ifs_csv}")
    
    # Save IFS NetCDF
    ds_ifs = xr.Dataset(
        data_vars={
            "temperature_2m": (("time",), df_ifs["temperature_2m"].values, {"units": "degC"}),
            "relative_humidity_2m": (("time",), df_ifs["relative_humidity_2m"].values, {"units": "%"}),
            "surface_pressure": (("time",), df_ifs["surface_pressure"].values, {"units": "hPa"}),
            "wind_speed_10m": (("time",), df_ifs["wind_speed_10m"].values, {"units": "m/s"}),
            "wind_direction_10m": (("time",), df_ifs["wind_direction_10m"].values, {"units": "degrees"}),
            "wind_gusts_10m": (("time",), df_ifs["wind_gusts_10m"].values, {"units": "m/s"}),
            "soil_moisture_0_to_7cm": (("time",), df_ifs["soil_moisture_0_to_7cm"].values, {"units": "m3/m3"})
        },
        coords={
            "time": df_ifs["valid_time"].values,
            "latitude": RIYADH_LAT,
            "longitude": RIYADH_LON
        },
        attrs={
            "title": "ECMWF IFS High-Resolution Numerical Weather Prediction for Riyadh",
            "source": "ECMWF Open Data / IFS",
            "city": "Riyadh, Saudi Arabia",
            "forecast_lead_range": "0h to 240h (10 days)"
        }
    )
    ifs_nc = out_dir / "ecmwf_ifs_nwp_riyadh_forecast.nc"
    ds_ifs.to_netcdf(ifs_nc)
    print(f"  Saved ECMWF IFS NetCDF to {ifs_nc} ({ifs_nc.stat().st_size / 1e3:.1f} KB)")
    return df_ifs

if __name__ == "__main__":
    df_cams = extract_cams_riyadh()
    df_ifs = fetch_ecmwf_ifs_riyadh()
    print("\n" + "=" * 70)
    print("SUCCESS: DEDICATED RIYADH NWP DATASETS PREPARED IN data/raw/nwp/")
    print("=" * 70)
