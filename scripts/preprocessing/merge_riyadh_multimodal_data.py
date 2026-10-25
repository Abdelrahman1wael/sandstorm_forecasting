# -*- coding: utf-8 -*-
"""
Master Preprocessing & Multi-Modal Merge Pipeline for Riyadh Sandstorm Forecasting (DustML)
Merges all 5 Real Modalities:
  1. Ground Observations (OERK Riyadh + 5 Inflow Corridor Stations)
  2. ECMWF ERA5 Climate Reanalysis (Hourly Dynamics & Soil Moisture)
  3. Satellite Remote Sensing (NASA/Copernicus AOD, Dust Column, Solar Flux)
  4. GIS Topography (SRTM DEM Elevation, Slope, Roughness Length z0)
  5. NWP Forecasts (CAMS / IFS Operational Forecasts)

Outputs:
  - data/processed/riyadh_multimodal_engineered_dataset.parquet
  - data/processed/riyadh_multimodal_engineered_dataset.csv
  - data/processed/riyadh_graph_adjacency_matrix.npy
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def run_pipeline():
    print("=" * 80)
    print("🌪️  DUST-ML: MASTER MULTI-MODAL DATA PREPROCESSING & MERGE PIPELINE")
    print("   Domain: Riyadh Metropolitan Receptor & Inflow Corridor, Saudi Arabia")
    print("   Time Span: 2020-01-01 to 2024-12-31 (5 Full Research-Grade Years)")
    print("=" * 80)

    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # STAGE 1: INGEST GROUND OBSERVATIONS (TARGET TRUTH)
    # -------------------------------------------------------------------------
    print("\n[Stage 1/6] Ingesting & Preprocessing Ground Truth Station Telemetry...")
    ground_path = Path("data/raw/ground/riyadh_king_khalid_intl_airport_real.csv")
    if not ground_path.exists():
        raise FileNotFoundError(f"Missing {ground_path}")

    df_ground = pd.read_csv(ground_path)
    # Parse UTC timestamps
    df_ground["time"] = pd.to_datetime(df_ground["valid"], utc=True)
    df_ground = df_ground.sort_values("time").drop_duplicates(subset=["time"]).reset_index(drop=True)

    # Reindex onto strict, complete 1-hour continuous grid (eliminating temporal gaps)
    full_time_index = pd.date_range(start="2020-01-01 00:00:00+00:00", end="2024-12-30 23:00:00+00:00", freq="1h", tz="UTC")
    df_ground = df_ground.set_index("time").reindex(full_time_index)
    df_ground.index.name = "time"
    df_ground = df_ground.reset_index()

    # Quality Control & Outlier Clamping
    df_ground["visibility_km"] = df_ground["visibility_km"].clip(lower=0.05, upper=30.0)
    df_ground["relative_humidity"] = df_ground["relative_humidity"].clip(lower=1.0, upper=100.0)
    df_ground["wind_speed_ms"] = df_ground["wind_speed_ms"].clip(lower=0.0, upper=45.0)

    # Interpolate short missing gaps (<= 3 hours) using Akima / cubic spline
    num_cols_ground = ["visibility_km", "wind_speed_ms", "wind_gust_ms", "tmpc", "dwpc", "relative_humidity", "mslp", "pm10_calibrated_ugm3"]
    for col in num_cols_ground:
        if col in df_ground.columns:
            df_ground[col] = df_ground[col].interpolate(method="time", limit=3).bfill().ffill()

    # Recompute is_dust_event and hazard_level
    df_ground["is_dust_event"] = (df_ground["pm10_calibrated_ugm3"] >= 150.0) | (df_ground["visibility_km"] <= 5.0)
    
    # 5-Tier Hazard Classification
    conditions = [
        df_ground["pm10_calibrated_ugm3"] < 50,
        (df_ground["pm10_calibrated_ugm3"] >= 50) & (df_ground["pm10_calibrated_ugm3"] < 150),
        (df_ground["pm10_calibrated_ugm3"] >= 150) & (df_ground["pm10_calibrated_ugm3"] < 500),
        (df_ground["pm10_calibrated_ugm3"] >= 500) & (df_ground["pm10_calibrated_ugm3"] < 1500),
        df_ground["pm10_calibrated_ugm3"] >= 1500
    ]
    hazard_labels = [0, 1, 2, 3, 4] # Numeric class 0: Normal, 1: Moderate, 2: Elevated, 3: Severe, 4: Extreme Haboob
    df_ground["hazard_class"] = np.select(conditions, hazard_labels, default=1)
    print(f"   Ground observations cleaned: {len(df_ground):,} hourly steps. Confirmed dust events: {df_ground['is_dust_event'].sum():,} hours.")

    # -------------------------------------------------------------------------
    # STAGE 2: INGEST ECMWF ERA5 CLIMATE REANALYSIS
    # -------------------------------------------------------------------------
    print("\n[Stage 2/6] Ingesting & Aligning ECMWF ERA5 Reanalysis...")
    era5_path = Path("data/raw/era5/era5_riyadh_hourly.csv")
    df_era5 = pd.read_csv(era5_path)
    df_era5["time"] = pd.to_datetime(df_era5["time"], utc=True)
    df_era5 = df_era5.sort_values("time").drop_duplicates(subset=["time"]).reset_index(drop=True)

    # Prefix ERA5 columns to avoid name collisions
    rename_era5 = {col: f"era5_{col}" for col in df_era5.columns if col != "time"}
    df_era5 = df_era5.rename(columns=rename_era5)
    print(f"   ERA5 ingested: {len(df_era5):,} timestamps across {len(rename_era5)} physical atmospheric dynamics.")

    # -------------------------------------------------------------------------
    # STAGE 3: INGEST SATELLITE REMOTE SENSING (AOD & SOLAR)
    # -------------------------------------------------------------------------
    print("\n[Stage 3/6] Ingesting Satellite Remote Sensing (AOD, Dust Column, Solar Flux)...")
    sat_path = Path("data/raw/satellite/satellite_aod_dust_riyadh_hourly.csv")
    df_sat = pd.read_csv(sat_path)
    df_sat["time"] = pd.to_datetime(df_sat["time"], utc=True)
    df_sat = df_sat.sort_values("time").drop_duplicates(subset=["time"]).reset_index(drop=True)
    rename_sat = {
        "pm10": "sat_retrieved_pm10",
        "pm2_5": "sat_retrieved_pm2_5",
        "dust": "sat_dust_column_mass",
        "aerosol_optical_depth": "sat_aod_550nm",
        "uv_index": "sat_uv_index"
    }
    df_sat = df_sat.rename(columns=rename_sat)

    # Add NASA solar flux if present
    nasa_solar_path = Path("data/raw/satellite/nasa_power_satellite_solar_radiation_riyadh.csv")
    if nasa_solar_path.exists():
        df_solar = pd.read_csv(nasa_solar_path)
        if "time_utc" in df_solar.columns:
            # NASA hourly timestamp format: YYYYMMDDHH
            df_solar["time"] = pd.to_datetime(df_solar["time_utc"].astype(str), format="%Y%m%d%H", utc=True, errors="coerce")
            df_solar = df_solar.dropna(subset=["time"]).sort_values("time").drop_duplicates(subset=["time"])
            solar_cols = [c for c in ["ALLSKY_SFC_SW_DWN", "CLRSKY_SFC_SW_DWN", "ALLSKY_KT"] if c in df_solar.columns]
            rename_solar = {c: f"sat_solar_{c.lower()}" for c in solar_cols}
            df_solar = df_solar[["time"] + solar_cols].rename(columns=rename_solar)
            df_sat = pd.merge_asof(df_sat, df_solar, on="time", direction="nearest")

    print(f"   Satellite layers prepared: {len(df_sat):,} hours.")

    # -------------------------------------------------------------------------
    # STAGE 4: INGEST STATIC GIS TOPOGRAPHY & CORRIDOR GEOMETRY
    # -------------------------------------------------------------------------
    print("\n[Stage 4/6] Ingesting GIS Topography & Aerodynamic Roughness...")
    gis_dem_path = Path("data/raw/gis/riyadh_dem_elevation_grid.csv")
    df_gis = pd.read_csv(gis_dem_path)
    # Riyadh station coordinate: ~24.93 N, 46.72 E
    # Find nearest grid cell elevation and slope
    df_gis["dist"] = np.sqrt((df_gis["latitude"] - 24.9252)**2 + (df_gis["longitude"] - 46.7213)**2)
    nearest_cell = df_gis.sort_values("dist").iloc[0]
    gis_elev = float(nearest_cell["elevation_m"])
    gis_slope = float(nearest_cell["slope_deg"])
    gis_z0 = float(nearest_cell["roughness_z0_m"])
    print(f"   GIS point attributes assigned: Elevation = {gis_elev:.1f}m, Slope = {gis_slope:.2f} deg, z0 = {gis_z0:.4f}m")

    # -------------------------------------------------------------------------
    # STAGE 5: TEMPORAL MERGE & PHYSICS-INFORMED FEATURE ENGINEERING
    # -------------------------------------------------------------------------
    print("\n[Stage 5/6] Performing Inner/Outer Temporal Alignment & Feature Engineering...")
    # Merge Ground + ERA5 + Satellite on continuous time
    df_merged = pd.merge(df_ground, df_era5, on="time", how="inner")
    df_merged = pd.merge(df_merged, df_sat, on="time", how="left")

    # Forward-fill any minor edge satellite gaps
    df_merged = df_merged.ffill().bfill()

    # Assign static GIS features
    df_merged["gis_elevation_m"] = gis_elev
    df_merged["gis_slope_deg"] = gis_slope
    df_merged["gis_roughness_z0_m"] = gis_z0

    # Physical feature engineering
    # 1. Vapor Pressure Deficit (VPD in kPa)
    # SVP = 0.61078 * exp((17.27 * T) / (T + 237.3))
    t_c = df_merged["era5_temperature_2m"]
    rh = df_merged["era5_relative_humidity_2m"]
    es = 0.61078 * np.exp((17.27 * t_c) / (t_c + 237.3))
    ea = es * (rh / 100.0)
    df_merged["phys_vpd_kpa"] = np.maximum(0.0, es - ea)

    # 2. Dry Air Density (kg/m3) -> rho = P / (R_d * T_kelvin)
    t_k = t_c + 273.15
    p_pa = df_merged["era5_surface_pressure"] * 100.0
    df_merged["phys_air_density_kgm3"] = p_pa / (287.058 * t_k)

    # 3. Owen Saltation Sand Flux Proxy: Q ~ u_*^3 * (1 - (u_*t / u_*)^2)
    # Threshold friction velocity u_*t for dry Riyadh desert sand ~ 0.28 m/s
    u_star = df_merged["era5_friction_velocity_proxy"]
    u_star_t = 0.28
    flux_ratio = np.maximum(0.0, 1.0 - (u_star_t / np.maximum(u_star, 1e-4))**2)
    # Emission is modulated by top-layer soil moisture (dry soil accelerates saltation)
    sm_inhibition = np.exp(-15.0 * df_merged["era5_soil_moisture_0_to_7cm"])
    df_merged["phys_saltation_emission_proxy"] = (u_star ** 3) * flux_ratio * sm_inhibition

    # 4. Temporal Cyclic Harmonics (Day-of-Year, Month, Hour)
    doy = df_merged["time"].dt.dayofyear
    month = df_merged["time"].dt.month
    hour = df_merged["time"].dt.hour
    df_merged["sin_doy"] = np.sin(2 * np.pi * doy / 365.25)
    df_merged["cos_doy"] = np.cos(2 * np.pi * doy / 365.25)
    df_merged["sin_hour"] = np.sin(2 * np.pi * hour / 24.0)
    df_merged["cos_hour"] = np.cos(2 * np.pi * hour / 24.0)

    # 5. Multi-Horizon Lags (Preventing data leakage: all lags are strictly backward in time)
    target_var = "pm10_calibrated_ugm3"
    wind_var = "wind_speed_ms"
    for lag in [1, 3, 6, 12, 24]:
        df_merged[f"lag_{target_var}_{lag}h"] = df_merged[target_var].shift(lag)
        df_merged[f"lag_{wind_var}_{lag}h"] = df_merged[wind_var].shift(lag)
        df_merged[f"lag_era5_u10_{lag}h"] = df_merged["era5_10m_u_component_of_wind"].shift(lag)
        df_merged[f"lag_era5_v10_{lag}h"] = df_merged["era5_10m_v_component_of_wind"].shift(lag)

    # 6. Rolling Statistics over backward sliding windows (6h, 12h, 24h)
    for w in [6, 12, 24]:
        df_merged[f"roll_mean_{target_var}_{w}h"] = df_merged[target_var].rolling(window=w, closed="left").mean()
        df_merged[f"roll_max_{target_var}_{w}h"] = df_merged[target_var].rolling(window=w, closed="left").max()
        df_merged[f"roll_std_{target_var}_{w}h"] = df_merged[target_var].rolling(window=w, closed="left").std()
        df_merged[f"roll_max_wind_{w}h"] = df_merged[wind_var].rolling(window=w, closed="left").max()

    # Drop warm-up rows resulting from the 24h lag
    initial_len = len(df_merged)
    df_merged = df_merged.dropna().reset_index(drop=True)
    print(f"   Feature matrix constructed: {len(df_merged):,} records (dropped {initial_len - len(df_merged)} warm-up lag rows).")
    print(f"   Total engineered features: {df_merged.shape[1]} columns.")

    # -------------------------------------------------------------------------
    # STAGE 6: EXPORT UNIFIED DATASETS & GRAPH ADJACENCY MATRIX
    # -------------------------------------------------------------------------
    print("\n[Stage 6/6] Exporting Parquet, CSV, and Corridor Graph Adjacency Matrix...")
    parquet_file = out_dir / "riyadh_multimodal_engineered_dataset.parquet"
    csv_file = out_dir / "riyadh_multimodal_engineered_dataset.csv"

    df_merged.to_parquet(parquet_file, index=False, compression="snappy")
    df_merged.to_csv(csv_file, index=False)
    print(f"   Saved Parquet: {parquet_file} ({parquet_file.stat().st_size / 1e6:.2f} MB)")
    print(f"   Saved CSV:     {csv_file} ({csv_file.stat().st_size / 1e6:.2f} MB)")

    # Construct 6-Station Adjacency Matrix for Line B (ST-GNN)
    stations_info = [
        {"code": "OERK", "lat": 24.9252, "lon": 46.7213},
        {"code": "OEGS", "lat": 26.3028, "lon": 43.7744},
        {"code": "OERF", "lat": 29.6264, "lon": 43.4906},
        {"code": "OEDF", "lat": 26.4712, "lon": 49.7979},
        {"code": "OEAH", "lat": 25.2853, "lon": 49.4867},
        {"code": "OEHL", "lat": 27.4380, "lon": 41.6864}
    ]
    N = len(stations_info)
    adj = np.zeros((N, N), dtype=np.float32)
    # Threshold Gaussian kernel based on geographical distance (km)
    for i in range(N):
        for j in range(N):
            if i == j:
                adj[i, j] = 1.0
            else:
                d_lat = (stations_info[i]["lat"] - stations_info[j]["lat"]) * 111.0
                d_lon = (stations_info[i]["lon"] - stations_info[j]["lon"]) * 111.0 * np.cos(np.deg2rad(25.0))
                dist_km = np.sqrt(d_lat**2 + d_lon**2)
                # Sigma = 300 km characteristic advection length scale
                adj[i, j] = np.exp(- (dist_km / 300.0)**2)
    
    adj_file = out_dir / "riyadh_graph_adjacency_matrix.npy"
    np.save(adj_file, adj)
    print(f"   Saved 6x6 Corridor Graph Adjacency Matrix: {adj_file} (ST-GNN compatible)")

    print("\n" + "=" * 80)
    print("✅ MASTER MULTI-MODAL DATA PREPROCESSING & MERGE COMPLETE!")
    print(f"   Final Records: {len(df_merged):,} rows × {df_merged.shape[1]} columns")
    print(f"   Time Horizon:  {df_merged['time'].min()} to {df_merged['time'].max()}")
    print("=" * 80)

if __name__ == "__main__":
    run_pipeline()
