"""
Script to download real ECMWF ERA5 Reanalysis data for Riyadh, Saudi Arabia.
Downloads both:
1. Hourly multi-variable time series for Riyadh Station (24.7136°N, 46.6753°E)
2. Spatial grid over the Greater Riyadh Receptor Domain (24.0°N - 25.5°N, 46.0°E - 47.5°E)

Saves data in:
- data/raw/era5/era5_riyadh_hourly.nc (NetCDF-4)
- data/raw/era5/era5_riyadh_hourly.csv
- data/raw/era5/era5_riyadh_spatial_grid.nc
"""

import sys
import os
import requests
import pandas as pd
import numpy as np
import xarray as xr
from pathlib import Path

out_dir = Path("data/raw/era5")
out_dir.mkdir(parents=True, exist_ok=True)

# Riyadh Central Coordinates
RIYADH_LAT = 24.7136
RIYADH_LON = 46.6753

# Target period: 2023-01-01 to 2024-05-31 (aligning with ground station records)
START_DATE = "2023-01-01"
END_DATE = "2024-05-31"

def download_riyadh_era5_point():
    print("=" * 65)
    print("DOWNLOADING REAL ECMWF ERA5 REANALYSIS FOR RIYADH (POINT TIME-SERIES)")
    print("=" * 65)
    
    url = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        "latitude": RIYADH_LAT,
        "longitude": RIYADH_LON,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "dew_point_2m",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
            "soil_temperature_0_to_7cm",
            "soil_moisture_0_to_7cm",
            "soil_moisture_7_to_28cm",
            "direct_radiation",
            "diffuse_radiation"
        ],
        "timezone": "UTC"
    }
    
    print(f"Requesting ERA5 reanalysis from {START_DATE} to {END_DATE}...")
    resp = requests.get(url, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    
    hourly = data.get("hourly", {})
    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    
    # Calculate u10 and v10 from wind speed and direction
    # Meteorological convention: wind from direction dir_deg
    rad = np.deg2rad(df["wind_direction_10m"])
    df["10m_u_component_of_wind"] = -df["wind_speed_10m"] * np.sin(rad)
    df["10m_v_component_of_wind"] = -df["wind_speed_10m"] * np.cos(rad)
    
    # Calculate kinetic energy and friction velocity proxy
    df["wind_kinetic_energy"] = 0.5 * (df["wind_speed_10m"] ** 2)
    df["friction_velocity_proxy"] = 0.04 * df["wind_speed_10m"] # Rough surface log-law proxy
    
    # Save CSV
    csv_file = out_dir / "era5_riyadh_hourly.csv"
    df.to_csv(csv_file, index=False)
    print(f"  Saved {len(df)} ERA5 hourly records to {csv_file}")
    
    # Convert to xarray Dataset and save NetCDF
    ds = xr.Dataset(
        data_vars={
            col: (("time",), df[col].values)
            for col in df.columns if col != "time"
        },
        coords={
            "time": df["time"].values,
            "latitude": RIYADH_LAT,
            "longitude": RIYADH_LON
        },
        attrs={
            "title": "ECMWF ERA5 Atmospheric & Soil Reanalysis for Riyadh",
            "source": "ECMWF ERA5 Reanalysis Archive",
            "city": "Riyadh, Saudi Arabia",
            "latitude": RIYADH_LAT,
            "longitude": RIYADH_LON,
            "elevation_m": data.get("elevation", 612),
            "period": f"{START_DATE} to {END_DATE}"
        }
    )
    
    nc_file = out_dir / "era5_riyadh_hourly.nc"
    ds.to_netcdf(nc_file)
    print(f"  Saved ERA5 NetCDF-4 dataset to {nc_file} ({nc_file.stat().st_size / 1e6:.2f} MB)")
    return df

def download_riyadh_era5_spatial_grid():
    print("\n" + "=" * 65)
    print("DOWNLOADING REAL ECMWF ERA5 SPATIAL GRID FOR GREATER RIYADH DOMAIN")
    print("=" * 65)
    
    # Define a 4x4 spatial grid covering Greater Riyadh Metropolitan & Outskirts
    # Lat: 24.0, 24.5, 25.0, 25.5; Lon: 46.0, 46.5, 47.0, 47.5
    lats = [24.0, 24.5, 25.0, 25.5]
    lons = [46.0, 46.5, 47.0, 47.5]
    
    grid_lats = []
    grid_lons = []
    for la in lats:
        for lo in lons:
            grid_lats.append(la)
            grid_lons.append(lo)
            
    # For spatial grid, sample spring 2024 active dust season (March 1 to April 30, 2024)
    grid_start = "2024-03-01"
    grid_end = "2024-04-30"
    
    url = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        "latitude": ",".join(str(x) for x in grid_lats),
        "longitude": ",".join(str(x) for x in grid_lons),
        "start_date": grid_start,
        "end_date": grid_end,
        "hourly": [
            "temperature_2m",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "soil_moisture_0_to_7cm"
        ],
        "timezone": "UTC"
    }
    
    print(f"Requesting 16-point spatial grid over Riyadh for {grid_start} to {grid_end}...")
    resp = requests.get(url, params=params, timeout=90)
    resp.raise_for_status()
    results = resp.json()
    
    if isinstance(results, list):
        times = pd.to_datetime(results[0]["hourly"]["time"])
        n_times = len(times)
        
        # Build 3D array [time, lat, lon]
        arr_t2m = np.zeros((n_times, len(lats), len(lons)), dtype=np.float32)
        arr_sp = np.zeros((n_times, len(lats), len(lons)), dtype=np.float32)
        arr_w10 = np.zeros((n_times, len(lats), len(lons)), dtype=np.float32)
        arr_sm = np.zeros((n_times, len(lats), len(lons)), dtype=np.float32)
        
        idx = 0
        for i, la in enumerate(lats):
            for j, lo in enumerate(lons):
                h = results[idx]["hourly"]
                arr_t2m[:, i, j] = h["temperature_2m"]
                arr_sp[:, i, j] = h["surface_pressure"]
                arr_w10[:, i, j] = h["wind_speed_10m"]
                arr_sm[:, i, j] = h["soil_moisture_0_to_7cm"]
                idx += 1
                
        grid_ds = xr.Dataset(
            data_vars={
                "temperature_2m": (("time", "latitude", "longitude"), arr_t2m),
                "surface_pressure": (("time", "latitude", "longitude"), arr_sp),
                "wind_speed_10m": (("time", "latitude", "longitude"), arr_w10),
                "soil_moisture_0_to_7cm": (("time", "latitude", "longitude"), arr_sm),
            },
            coords={
                "time": times,
                "latitude": lats,
                "longitude": lons
            },
            attrs={
                "title": "ECMWF ERA5 Spatial Reanalysis Grid for Greater Riyadh Basin",
                "domain": "Riyadh Metropolitan & Najd Escarpment (24.0N-25.5N, 46.0E-47.5E)",
                "resolution": "0.5 degree",
                "period": f"{grid_start} to {grid_end}"
            }
        )
        
        grid_nc = out_dir / "era5_riyadh_spatial_grid.nc"
        grid_ds.to_netcdf(grid_nc)
        print(f"  Saved ERA5 spatial grid NetCDF to {grid_nc} ({grid_nc.stat().st_size / 1e6:.2f} MB)")

if __name__ == "__main__":
    download_riyadh_era5_point()
    download_riyadh_era5_spatial_grid()
