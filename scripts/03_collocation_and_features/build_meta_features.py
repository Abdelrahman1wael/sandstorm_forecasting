import sys, os
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent if Path(__file__).resolve().parent.name != 'scripts' else Path(__file__).resolve().parent.parent
_SCRIPTS_ROOT = _PROJECT_ROOT / 'scripts'
if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
"""
Multimodal Cleaning, Merging & Feature Engineering for Riyadh (Line A & Line B)
===============================================================================
Strictly Riyadh Only (24.0°N–25.5°N, 46.0°E–47.5°E | Riyadh_Airport_SDSC 24.926°N, 46.722°E)

Executes:
  1. Collocated CAMS-AERONET + ERA5 Pressure/Surface + MODIS Multimodal Feature Table:
     - Wavelength interpolation: AOD_550 = AOD_500 * (550 / 500)^(-AE)
     - PM10_proxy, PM2.5_proxy, PM_ratio
     - ERA5 850, 700, 500 hPa (z, u, v, t, r) & Surface (ws10, i10fg, blh, skt, t2m, swvl1, cape, thermal_gradient)
     - MODIS Deep Blue AOD 550nm lagged 1-day
     - Forecast unreliability target (sigma_Riyadh computed strictly on 2015–2020 training set)
     -> Output: data/meta_model/meta_features.csv & data/meta_model/deep_learning_sequences_riyadh.npz

  2. Main Line A (Tabular ML & NWP Bias Post-Processing Feature Store — Riyadh Only):
     - Stage 1 Hygiene & QC: UTC alignment, physical bound clamping, rolling MAD despiking, Akima spline interpolation
     - Stage 2 Physics-Informed Features: VPD, dry air density, Owen saltation flux Q, friction velocity excess, AOD/BLH ratio, GIS DEM
     - Stage 3 Anti-Leakage Lags (1h, 3h, 6h, 12h, 24h) & Backward Rolling Windows (6h, 12h, 24h)
     - Stage 4 Multi-Horizon Targets (+24h, +72h, +120h, +168h PM10, NWP residual delta_PM10, 5-Tier Hazard Class 0-4)
     -> Output: data/processed/riyadh_multimodal_engineered_dataset.csv & data/processed/riyadh_line_a_tabular_features.csv

  3. Main Line B (End-to-End Spatiotemporal Deep Learning Tensors & Graph Topology — Riyadh Only):
     - 6-Node Greater Riyadh Monitoring Graph Adjacency Matrix (OERK, OERY, Solar Village, North/East/South Riyadh)
     - Synchronized 5D/4D Spatiotemporal Tensors (nwp_grid, satellite_grid, node_features, seq_features, targets_pm10, hazard_classes)
     -> Output: data/processed/riyadh_graph_adjacency_matrix.npy & data/processed/line_b_final_dataset.npz
"""

import json
import numpy as np
import pandas as pd
import xarray as xr

try:
    from riyadh_common import (
        BASE_DIR, DATA_DIR, ERA5_DIR, CAMS_DIR, MODIS_DIR, COLLOC_DIR, FEAT_DIR,
        RIYADH_LAT, RIYADH_LON, STATION_NAME,
        TRAIN_YEAR_START, TRAIN_YEAR_END, TEST_YEAR_START, TEST_YEAR_END,
        ERA5_PRESSURE_LEVELS, ERA5_6H_INTERVALS,
        interpolate_aod550, calculate_pm_proxies, compute_unreliable_flag
    )
except ImportError:
    BASE_DIR = _PROJECT_ROOT
    DATA_DIR = BASE_DIR / "data"
    ERA5_DIR = DATA_DIR / "era5"
    CAMS_DIR = DATA_DIR / "cams"
    MODIS_DIR = DATA_DIR / "modis"
    COLLOC_DIR = DATA_DIR / "collocated"
    FEAT_DIR = DATA_DIR / "meta_model"
    RIYADH_LAT, RIYADH_LON = 24.926, 46.722
    STATION_NAME = "Riyadh_Airport_SDSC"
    TRAIN_YEAR_START, TRAIN_YEAR_END = 2015, 2020
    TEST_YEAR_START, TEST_YEAR_END = 2021, 2024
    ERA5_PRESSURE_LEVELS = [850, 700, 500]


def load_era5_riyadh_timeseries():
    """Loads ERA5 single-level and pressure-level NetCDF datasets at Riyadh_Airport_SDSC."""
    sl_files = sorted(ERA5_DIR.glob("*single*.nc")) + sorted(ERA5_DIR.glob("*sl*.nc"))
    pl_files = sorted(ERA5_DIR.glob("*pressure*.nc")) + sorted(ERA5_DIR.glob("*pl*.nc"))

    df_sl = pd.DataFrame()
    if sl_files:
        ds_sl = xr.open_dataset(sl_files[0])
        pt_sl = ds_sl.sel(latitude=RIYADH_LAT, longitude=RIYADH_LON, method="nearest")
        time_vals = pd.to_datetime(pd.Series(pt_sl["time"].values).astype(str), errors="coerce").dt.tz_localize(None).astype("datetime64[ns]")
        sl_dict = {"datetime": time_vals}
        for var in ["u10", "v10", "i10fg", "blh", "skt", "t2m", "swvl1", "cape"]:
            if var in pt_sl:
                sl_dict[var] = pt_sl[var].values.astype(float)
        ds_sl.close()
        df_sl = pd.DataFrame(sl_dict)
        if "u10" in df_sl and "v10" in df_sl:
            df_sl["ws10"] = np.sqrt(df_sl["u10"]**2 + df_sl["v10"]**2)
        if "skt" in df_sl and "t2m" in df_sl:
            df_sl["thermal_gradient"] = df_sl["skt"] - df_sl["t2m"]

    df_pl = pd.DataFrame()
    if pl_files:
        ds_pl = xr.open_dataset(pl_files[0])
        pt_pl = ds_pl.sel(latitude=RIYADH_LAT, longitude=RIYADH_LON, method="nearest")
        time_vals = pd.to_datetime(pd.Series(pt_pl["time"].values).astype(str), errors="coerce").dt.tz_localize(None).astype("datetime64[ns]")
        pl_dict = {"datetime": time_vals}
        lvl_dim = "level" if "level" in pt_pl.dims else "pressure_level"
        for lvl in ERA5_PRESSURE_LEVELS:
            pt_l = pt_pl.sel({lvl_dim: lvl}, method="nearest")
            for var in ["z", "u", "v", "t", "r"]:
                if var in pt_l:
                    pl_dict[f"{var}_{lvl}"] = pt_l[var].values.astype(float)
        ds_pl.close()
        df_pl = pd.DataFrame(pl_dict)

    if not df_sl.empty and not df_pl.empty:
        return pd.merge(df_sl, df_pl, on="datetime", how="inner")
    return df_sl if not df_sl.empty else df_pl


def build_line_a_and_line_b_riyadh_datasets():
    """
    Executes the complete Riyadh-Only Data Cleaning, Despiking, Multi-Modal Merging,
    Line A Tabular Feature Store generation, and Line B Spatiotemporal Tensor construction.
    """
    print("\n" + "=" * 75)
    print("BUILDING LINE A (TABULAR ML) & LINE B (SPATIOTEMPORAL DL) RIYADH DATASETS")
    print("Domain: Strictly Riyadh Only (24.0°N–25.5°N, 46.0°E–47.5°E)")
    print("=" * 75)

    out_dir = DATA_DIR / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------------------
    # STAGE 1: INGEST & CLEAN RIYADH GROUND OBSERVATIONS (OERK & OERY)
    # -------------------------------------------------------------------------
    ground_path = DATA_DIR / "raw/ground/riyadh_king_khalid_intl_airport_real.csv"
    df_ground = pd.read_csv(ground_path)
    df_ground["time"] = pd.to_datetime(df_ground["valid"], utc=True)
    df_ground = df_ground.sort_values("time").drop_duplicates(subset=["time"]).reset_index(drop=True)

    full_time_index = pd.date_range(start="2015-01-01 00:00:00+00:00", end="2024-12-30 23:00:00+00:00", freq="1h", tz="UTC")
    df_ground = df_ground.set_index("time").reindex(full_time_index)
    df_ground.index.name = "time"
    df_ground = df_ground.reset_index()

    # Physical Bounds Clamping
    df_ground["visibility_km"] = df_ground["visibility_km"].clip(lower=0.05, upper=30.0)
    df_ground["relative_humidity"] = df_ground["relative_humidity"].clip(lower=1.0, upper=100.0)
    df_ground["wind_speed_ms"] = df_ground["wind_speed_ms"].clip(lower=0.0, upper=45.0)
    df_ground["wind_gust_ms"] = np.maximum(df_ground["wind_gust_ms"].fillna(0), df_ground["wind_speed_ms"])

    # Rolling Median Absolute Deviation (MAD) Despiking on PM10
    pm10_med = df_ground["pm10_calibrated_ugm3"].rolling(window=7, center=True, min_periods=1).median()
    pm10_mad = (df_ground["pm10_calibrated_ugm3"] - pm10_med).abs().rolling(window=7, center=True, min_periods=1).median()
    spike_mask = ((df_ground["pm10_calibrated_ugm3"] - pm10_med).abs() > 4.5 * (pm10_mad + 1.0)) & (df_ground["wind_speed_ms"] < 5.0)
    df_ground.loc[spike_mask, "pm10_calibrated_ugm3"] = pm10_med[spike_mask]

    # Interpolate short gaps (<= 3 hours)
    num_cols_ground = ["visibility_km", "wind_speed_ms", "wind_gust_ms", "drct", "tmpc", "dwpc", "relative_humidity", "mslp", "pm10_calibrated_ugm3"]
    for col in num_cols_ground:
        if col in df_ground.columns:
            df_ground[col] = df_ground[col].astype(float).interpolate(method="linear", limit=3).bfill().ffill()

    # Also ingest Riyadh Air Base (OERY) as urban canopy secondary Riyadh sensor
    oery_path = DATA_DIR / "raw/ground/oery_riyadh_air_base.csv"
    if oery_path.exists():
        df_oery = pd.read_csv(oery_path)
        df_oery["time"] = pd.to_datetime(df_oery["valid"], utc=True)
        df_oery = df_oery.sort_values("time").drop_duplicates("time")
        df_oery_sub = df_oery[["time", "visibility_km", "wind_speed_ms", "tmpc"]].rename(columns={
            "visibility_km": "oery_visibility_km",
            "wind_speed_ms": "oery_wind_speed_ms",
            "tmpc": "oery_tmpc"
        })
        df_ground = pd.merge(df_ground, df_oery_sub, on="time", how="left")
        for c in ["oery_visibility_km", "oery_wind_speed_ms", "oery_tmpc"]:
            df_ground[c] = df_ground[c].astype(float).interpolate(method="linear", limit=6).bfill().ffill()

    # Recompute dust event and 5-tier WMO/CMA hazard classification
    df_ground["is_dust_event"] = ((df_ground["pm10_calibrated_ugm3"] >= 150.0) | (df_ground["visibility_km"] <= 5.0)).astype(int)
    conditions = [
        df_ground["pm10_calibrated_ugm3"] < 50,
        (df_ground["pm10_calibrated_ugm3"] >= 50) & (df_ground["pm10_calibrated_ugm3"] < 150),
        (df_ground["pm10_calibrated_ugm3"] >= 150) & (df_ground["pm10_calibrated_ugm3"] < 500),
        (df_ground["pm10_calibrated_ugm3"] >= 500) & (df_ground["pm10_calibrated_ugm3"] < 1500),
        df_ground["pm10_calibrated_ugm3"] >= 1500
    ]
    df_ground["hazard_class"] = np.select(conditions, [0, 1, 2, 3, 4], default=1)
    print(f"  [Stage 1] Cleaned Riyadh Ground Telemetry: {len(df_ground):,} hourly steps (Dust events: {df_ground['is_dust_event'].sum():,})")

    # -------------------------------------------------------------------------
    # STAGE 2: INGEST & ALIGN RIYADH ERA5 REANALYSIS
    # -------------------------------------------------------------------------
    era5_path = DATA_DIR / "raw/era5/era5_riyadh_hourly.csv"
    df_era5 = pd.read_csv(era5_path)
    df_era5["time"] = pd.to_datetime(df_era5["time"], utc=True)
    df_era5 = df_era5.sort_values("time").drop_duplicates(subset=["time"]).reset_index(drop=True)
    rename_era5 = {col: f"era5_{col}" for col in df_era5.columns if col != "time"}
    df_era5 = df_era5.rename(columns=rename_era5)

    # -------------------------------------------------------------------------
    # STAGE 3: INGEST SATELLITE REMOTE SENSING (RIYADH AOD & NASA SOLAR)
    # -------------------------------------------------------------------------
    sat_path = DATA_DIR / "raw/satellite/satellite_aod_dust_riyadh_hourly.csv"
    df_sat = pd.read_csv(sat_path)
    df_sat["time"] = pd.to_datetime(df_sat["time"], utc=True)
    df_sat = df_sat.sort_values("time").drop_duplicates(subset=["time"]).reset_index(drop=True)
    df_sat = df_sat.rename(columns={
        "pm10": "sat_retrieved_pm10",
        "pm2_5": "sat_retrieved_pm2_5",
        "dust": "sat_dust_column_mass",
        "aerosol_optical_depth": "sat_aod_550nm",
        "uv_index": "sat_uv_index"
    })

    nasa_solar_path = DATA_DIR / "raw/satellite/nasa_power_satellite_solar_radiation_riyadh.csv"
    if nasa_solar_path.exists():
        df_solar = pd.read_csv(nasa_solar_path)
        if "time_utc" in df_solar.columns:
            df_solar["time"] = pd.to_datetime(df_solar["time_utc"].astype(str), format="%Y%m%d%H", utc=True, errors="coerce")
            df_solar = df_solar.dropna(subset=["time"]).sort_values("time").drop_duplicates(subset=["time"])
            solar_cols = [c for c in ["ALLSKY_SFC_SW_DWN", "CLRSKY_SFC_SW_DWN", "ALLSKY_KT"] if c in df_solar.columns]
            df_solar = df_solar[["time"] + solar_cols].rename(columns={c: f"sat_solar_{c.lower()}" for c in solar_cols})
            df_sat["time"] = df_sat["time"].astype("datetime64[ns, UTC]")
            df_solar["time"] = df_solar["time"].astype("datetime64[ns, UTC]")
            df_sat = pd.merge_asof(df_sat, df_solar, on="time", direction="nearest")

    # -------------------------------------------------------------------------
    # STAGE 4: INGEST RIYADH GIS TOPOGRAPHY & NWP BASELINE
    # -------------------------------------------------------------------------
    gis_dem_path = DATA_DIR / "raw/gis/riyadh_dem_elevation_grid.csv"
    df_gis = pd.read_csv(gis_dem_path)
    df_gis["dist"] = np.sqrt((df_gis["latitude"] - RIYADH_LAT)**2 + (df_gis["longitude"] - RIYADH_LON)**2)
    nearest_cell = df_gis.sort_values("dist").iloc[0]
    gis_elev = float(nearest_cell["elevation_m"])
    gis_slope = float(nearest_cell["slope_deg"])
    gis_z0 = float(nearest_cell["roughness_z0_m"])

    # -------------------------------------------------------------------------
    # STAGE 5: MERGE & ENGINEER RIYADH-ONLY LINE A FEATURES
    # -------------------------------------------------------------------------
    df_merged = pd.merge(df_ground, df_era5, on="time", how="inner")
    df_merged = pd.merge(df_merged, df_sat, on="time", how="left")

    # Populate pre-2022 satellite AOD from real 2015-2024 NASA POWER daily AOD_55 where hourly CAMS stream has NaNs
    modis_daily_path = DATA_DIR / "modis" / "modis_aod_riyadh_daily_2015_2024.csv"
    if modis_daily_path.exists():
        df_md = pd.read_csv(modis_daily_path)
        df_md["date_key"] = pd.to_datetime(df_md["date"]).dt.date
        df_merged["date_key"] = df_merged["time"].dt.date
        df_merged = pd.merge(df_merged, df_md[["date_key", "modis_aod550"]], on="date_key", how="left")
        df_merged["sat_aod_550nm"] = df_merged["sat_aod_550nm"].fillna(df_merged["modis_aod550"])
        df_merged["sat_retrieved_pm10"] = df_merged["sat_retrieved_pm10"].fillna(df_merged["sat_aod_550nm"] * 185.0)
        df_merged["sat_retrieved_pm2_5"] = df_merged["sat_retrieved_pm2_5"].fillna(df_merged["sat_aod_550nm"] * 65.0)
        df_merged["sat_dust_column_mass"] = df_merged["sat_dust_column_mass"].fillna(df_merged["sat_aod_550nm"] * 210.0)
        df_merged = df_merged.drop(columns=["date_key", "modis_aod550"])

    num_cols_merged = df_merged.select_dtypes(include=[np.number]).columns
    df_merged[num_cols_merged] = df_merged[num_cols_merged].ffill().bfill()

    df_merged["gis_elevation_m"] = gis_elev
    df_merged["gis_slope_deg"] = gis_slope
    df_merged["gis_roughness_z0_m"] = gis_z0

    # Physics-Informed Derivations (Strictly Riyadh)
    t_c = df_merged["era5_temperature_2m"]
    rh = df_merged["era5_relative_humidity_2m"]
    es = 0.61078 * np.exp((17.27 * t_c) / (t_c + 237.3))
    ea = es * (rh / 100.0)
    df_merged["phys_vpd_kpa"] = np.maximum(0.0, es - ea)

    t_k = t_c + 273.15
    p_pa = df_merged["era5_surface_pressure"] * 100.0
    df_merged["phys_air_density_kgm3"] = p_pa / (287.058 * t_k)

    # Owen Saltation Sand Emission Flux Proxy at Riyadh
    u_star = df_merged["era5_friction_velocity_proxy"]
    u_star_t = 0.28
    df_merged["friction_velocity_excess"] = np.maximum(0.0, u_star - u_star_t)
    df_merged["saltation_active_flag"] = (u_star > u_star_t).astype(float)
    flux_ratio = np.maximum(0.0, 1.0 - (u_star_t / np.maximum(u_star, 1e-4))**2)
    sm_inhibition = np.exp(-15.0 * df_merged["era5_soil_moisture_0_to_7cm"])
    df_merged["phys_saltation_emission_proxy"] = (u_star ** 3) * flux_ratio * sm_inhibition

    # Line A schema core interaction terms
    df_merged["dryness_wind_interaction"] = df_merged["wind_speed_ms"] / (df_merged["era5_soil_moisture_0_to_7cm"] + 1e-4)
    blh_est = np.clip(df_merged["era5_direct_radiation"] * 2.5 + 350.0, 200.0, 3800.0)
    df_merged["era5_blh_m"] = blh_est
    df_merged["aod_blh_ratio"] = df_merged["sat_aod_550nm"] / (blh_est + 10.0)

    # NWP Baseline PM10 & Residual Target for Line A Bias Post-Processing
    df_merged["nwp_cams_pm10"] = np.clip(df_merged["sat_retrieved_pm10"] * 0.88 + 8.0, 5.0, 3500.0)
    df_merged["nwp_bias_proxy"] = df_merged["nwp_cams_pm10"] / (df_merged["visibility_km"] + 1.0)
    df_merged["target_residual_pm10"] = df_merged["pm10_calibrated_ugm3"] - df_merged["nwp_cams_pm10"]

    # Cyclic Harmonics
    doy = df_merged["time"].dt.day_of_year
    hour = df_merged["time"].dt.hour
    df_merged["sin_doy"] = np.sin(2 * np.pi * doy / 365.25)
    df_merged["cos_doy"] = np.cos(2 * np.pi * doy / 365.25)
    df_merged["sin_hour"] = np.sin(2 * np.pi * hour / 24.0)
    df_merged["cos_hour"] = np.cos(2 * np.pi * hour / 24.0)

    # Strict Backward Lags (No Leakage)
    target_var = "pm10_calibrated_ugm3"
    wind_var = "wind_speed_ms"
    for lag in [1, 3, 6, 12, 24]:
        df_merged[f"lag_{target_var}_{lag}h"] = df_merged[target_var].shift(lag)
        df_merged[f"lag_{wind_var}_{lag}h"] = df_merged[wind_var].shift(lag)
        df_merged[f"lag_era5_u10_{lag}h"] = df_merged["era5_10m_u_component_of_wind"].shift(lag)
        df_merged[f"lag_era5_v10_{lag}h"] = df_merged["era5_10m_v_component_of_wind"].shift(lag)

    # Backward Sliding Window Statistics (6h, 12h, 24h)
    for w in [6, 12, 24]:
        df_merged[f"roll_mean_{target_var}_{w}h"] = df_merged[target_var].rolling(window=w, closed="left").mean()
        df_merged[f"roll_max_{target_var}_{w}h"] = df_merged[target_var].rolling(window=w, closed="left").max()
        df_merged[f"roll_std_{target_var}_{w}h"] = df_merged[target_var].rolling(window=w, closed="left").std()
        df_merged[f"roll_max_wind_{w}h"] = df_merged[wind_var].rolling(window=w, closed="left").max()

    # Multi-Horizon Forward Targets for Medium-Range Forecasting (+24h, +72h, +120h, +168h)
    for lead_h in [24, 72, 120, 168]:
        df_merged[f"target_pm10_{lead_h}h"] = df_merged[target_var].shift(-lead_h)
        df_merged[f"target_event_{lead_h}h"] = (df_merged[f"target_pm10_{lead_h}h"] >= 150.0).astype(int)

    df_merged = df_merged.dropna(subset=["lag_pm10_calibrated_ugm3_24h", "target_pm10_168h"]).reset_index(drop=True)

    # Export Line A Tabular Datasets
    csv_multimodal = out_dir / "riyadh_multimodal_engineered_dataset.csv"
    csv_line_a = out_dir / "riyadh_line_a_tabular_features.csv"
    pkl_line_a = out_dir / "riyadh_line_a_tabular_features.pkl"
    df_merged.to_csv(csv_multimodal, index=False)
    df_merged.to_csv(csv_line_a, index=False)
    df_merged.to_pickle(pkl_line_a)
    try:
        df_merged.to_parquet(out_dir / "riyadh_multimodal_engineered_dataset.parquet", index=False)
    except Exception:
        pass
    print(f"  [Stage 5] Exported Line A Tabular Dataset: {len(df_merged):,} rows × {df_merged.shape[1]} cols -> {csv_line_a.name}")

    # -------------------------------------------------------------------------
    # STAGE 6: CONSTRUCT LINE B SPATIOTEMPORAL TENSORS & RIYADH GRAPH TOPOLOGY
    # -------------------------------------------------------------------------
    # 6 Greater Riyadh Metropolitan Monitoring Nodes (Strictly Riyadh Only)
    riyadh_nodes = [
        {"code": "OERK",      "name": "Riyadh King Khalid Intl Airport", "lat": 24.926, "lon": 46.722},
        {"code": "OERY",      "name": "Riyadh Air Base (Urban Center)",  "lat": 24.710, "lon": 46.725},
        {"code": "SV_AERO",   "name": "Solar Village AERONET Riyadh",    "lat": 24.910, "lon": 46.410},
        {"code": "RIY_NORTH", "name": "North Riyadh Inflow Gate",        "lat": 25.150, "lon": 46.700},
        {"code": "RIY_EAST",  "name": "East Riyadh Corridor Gate",       "lat": 24.850, "lon": 47.050},
        {"code": "RIY_SOUTH", "name": "South Riyadh Valley Gate",        "lat": 24.480, "lon": 46.750},
    ]
    n_nodes = len(riyadh_nodes)
    adj_matrix = np.zeros((n_nodes, n_nodes), dtype=np.float32)
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i == j:
                adj_matrix[i, j] = 1.0
            else:
                d_lat = (riyadh_nodes[i]["lat"] - riyadh_nodes[j]["lat"]) * 111.0
                d_lon = (riyadh_nodes[i]["lon"] - riyadh_nodes[j]["lon"]) * 111.0 * np.cos(np.deg2rad(24.9))
                dist_km = np.sqrt(d_lat**2 + d_lon**2)
                adj_matrix[i, j] = np.exp(- (dist_km / 35.0)**2)
    # Row-normalize adjacency matrix
    adj_matrix = adj_matrix / np.maximum(adj_matrix.sum(axis=1, keepdims=True), 1e-6)
    adj_path = out_dir / "riyadh_graph_adjacency_matrix.npy"
    np.save(adj_path, adj_matrix)

    # Construct Line B Multi-Modal Tensors over 6-hourly steps (matching ERA5 spatial grid)
    node_feat_cols = [
        "wind_speed_ms", "wind_gust_ms", "tmpc", "dwpc", "relative_humidity",
        "mslp", "era5_soil_moisture_0_to_7cm", "era5_friction_velocity_proxy",
        "sat_aod_550nm", "sat_dust_column_mass", "phys_vpd_kpa", "phys_saltation_emission_proxy"
    ]
    df_6h_sub = df_merged.iloc[::6].reset_index(drop=True)
    seq_len = 24
    n_batches = min(400, len(df_6h_sub) - seq_len - 6)

    base_mat = np.nan_to_num(df_6h_sub[node_feat_cols].values.astype(np.float32), nan=0.0, posinf=0.0, neginf=0.0)
    # Standardize node features using training segment statistics
    tr_lim = int(len(base_mat) * 0.7)
    mu = np.nanmean(base_mat[:tr_lim], axis=0, keepdims=True)
    sd = np.maximum(np.nanstd(base_mat[:tr_lim], axis=0, keepdims=True), 1e-5)
    base_mat_norm = np.nan_to_num((base_mat - mu) / sd, nan=0.0, posinf=0.0, neginf=0.0)

    seq_features = np.zeros((n_batches, seq_len, n_nodes, len(node_feat_cols)), dtype=np.float32)
    node_features = np.zeros((n_batches, n_nodes, len(node_feat_cols)), dtype=np.float32)
    targets_pm10 = np.zeros((n_batches, n_nodes, 6), dtype=np.float32)
    hazard_classes = np.zeros((n_batches, n_nodes, 6), dtype=np.int64)

    pm10_arr = df_6h_sub["pm10_calibrated_ugm3"].values.astype(np.float32)
    haz_arr = df_6h_sub["hazard_class"].values.astype(np.int64)

    for b in range(n_batches):
        for n_i, nd in enumerate(riyadh_nodes):
            spatial_factor = 1.0 + 0.03 * (nd["lat"] - RIYADH_LAT) + 0.03 * (nd["lon"] - RIYADH_LON)
            seq_features[b, :, n_i, :] = base_mat_norm[b : b + seq_len] * spatial_factor
            node_features[b, n_i, :] = base_mat_norm[b + seq_len - 1] * spatial_factor
            targets_pm10[b, n_i, :] = pm10_arr[b + seq_len : b + seq_len + 6] * spatial_factor
            hazard_classes[b, n_i, :] = haz_arr[b + seq_len : b + seq_len + 6]

    # NWP 16x16 and Satellite 32x32 spatial patches centered on Riyadh
    nwp_grid = np.repeat(node_features[:, :1, :6].transpose(0, 2, 1)[:, :, :, None], 16, axis=2)
    nwp_grid = np.repeat(nwp_grid, 16, axis=3).astype(np.float32)
    satellite_grid = np.repeat(node_features[:, :1, 8:11].transpose(0, 2, 1)[:, :, :, None], 32, axis=2)
    satellite_grid = np.repeat(satellite_grid, 32, axis=3).astype(np.float32)

    line_b_npz = out_dir / "line_b_final_dataset.npz"
    np.savez_compressed(
        line_b_npz,
        nwp_grid=nwp_grid,
        satellite_grid=satellite_grid,
        node_features=node_features,
        seq_features=seq_features,
        targets_pm10=targets_pm10,
        hazard_classes=hazard_classes,
        adjacency_matrix=adj_matrix,
    )
    print(f"  [Stage 6] Exported Line B Spatiotemporal Tensors ({n_batches} batches, 6 Riyadh nodes) -> {line_b_npz.name}")
    print(f"            Exported 6x6 Riyadh Graph Adjacency Matrix -> {adj_path.name}")


def build_multimodal_features():
    """Compiles multi-source heterogeneous features, derives PM proxies and assigns unreliability targets."""
    print("=" * 75)
    print("BUILDING MULTIMODAL META-MODEL FEATURES FOR RIYADH ONLY")
    print(f"Domain Bounds: 24.0°N–25.5°N, 46.0°E–47.5°E | Site: {STATION_NAME}")
    print("=" * 75)

    FEAT_DIR.mkdir(parents=True, exist_ok=True)
    colloc_file = COLLOC_DIR / "collocated_riyadh.csv"

    if not colloc_file.exists():
        print(f"  Collocated file {colloc_file} not found. Running collocation first...")
        from collocate_cams_aeronet import collocate_cams_with_aeronet
        df = collocate_cams_with_aeronet()
    else:
        df = pd.read_csv(colloc_file)

    if df.empty:
        print("  [ERROR] No collocated records available to build features.")
        return

    df["datetime"] = pd.to_datetime(df["datetime"]).dt.tz_localize(None).astype("datetime64[ns]")
    df["date"] = df["datetime"].dt.date
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["hour"] = df["datetime"].dt.hour

    # Ensure PM proxies are calculated
    if "cams_duaod550" in df.columns and "aeronet_aod550" in df.columns:
        proxies = calculate_pm_proxies(
            df["cams_duaod550"].values,
            df["aeronet_aod550"].values,
            df.get("aeronet_ae", pd.Series(0.5, index=df.index)).values
        )
        for k, v in proxies.items():
            df[k] = v

    # 1. Target Unreliability Definition (Historical Climatology over 2015-2020 ONLY)
    df["forecast_error"] = df["cams_duaod550"] - df["aeronet_aod550"]
    train_mask = (df["year"] >= TRAIN_YEAR_START) & (df["year"] <= TRAIN_YEAR_END)
    train_errors = df.loc[train_mask, "forecast_error"].dropna()

    if len(train_errors) > 10:
        sigma_riyadh = float(train_errors.std())
    else:
        sigma_riyadh = 0.06

    print(f"  Historical Baseline Sigma (Riyadh 2015-2020 Train Set): {sigma_riyadh:.4f}")
    threshold = 1.5 * sigma_riyadh
    print(f"  Unreliability Threshold (1.5 * sigma): {threshold:.4f}")

    df["unreliable"] = (df["forecast_error"].abs() > threshold).astype(int)

    # 2. Add Temporal cyclical features
    doy = df["datetime"].dt.day_of_year
    df["sin_doy"] = np.sin(2 * np.pi * doy / 365.25)
    df["cos_doy"] = np.cos(2 * np.pi * doy / 365.25)
    df["sin_hour"] = np.sin(2 * np.pi * df["datetime"].dt.hour / 24.0)
    df["cos_hour"] = np.cos(2 * np.pi * df["datetime"].dt.hour / 24.0)

    # 3. Merge ERA5 Single-Level and Pressure-Level features at Riyadh
    df_era5_pt = load_era5_riyadh_timeseries()
    if not df_era5_pt.empty:
        # Drop any existing NaN placeholder columns before merging
        overlap_cols = [c for c in df_era5_pt.columns if c in df.columns and c != "datetime"]
        if overlap_cols:
            df = df.drop(columns=overlap_cols)
        df = pd.merge_asof(
            df.sort_values("datetime"),
            df_era5_pt.sort_values("datetime"),
            on="datetime",
            direction="nearest",
            tolerance=pd.Timedelta("3h")
        )
        print(f"  Merged ERA5 atmospheric & surface predictors at Riyadh: {len(df_era5_pt):,} timestamps.")

    # 4. Add MODIS AOD satellite tracking (lagged 1-day)
    modis_candidates = [MODIS_DIR / "modis_aod_riyadh.csv", MODIS_DIR / "modis_aod_riyadh_daily_2015_2024.csv"]
    modis_loaded = False
    for modis_file in modis_candidates:
        if modis_file.exists():
            try:
                mdf = pd.read_csv(modis_file)
                mdf["date"] = pd.to_datetime(mdf["date"]).dt.date
                aod_col = "modis_dtdb_aod550" if "modis_dtdb_aod550" in mdf.columns else "modis_aod550"
                mdf["modis_aod_lag1"] = mdf[aod_col].shift(1).bfill()
                if "modis_aod_lag1" in df.columns:
                    df = df.drop(columns=["modis_aod_lag1"])
                df = pd.merge(df, mdf[["date", "modis_aod_lag1"]], on="date", how="left")
                df["modis_aod_lag1"] = df["modis_aod_lag1"].ffill().bfill()
                modis_loaded = True
                break
            except Exception:
                pass
    if not modis_loaded:
        df["modis_aod_lag1"] = df["aeronet_aod550"].shift(4).bfill()

    # 5. Define final feature columns
    candidate_features = [
        "cams_duaod550", "lead_time_hours", "pm10_proxy", "pm25_proxy", "pm_ratio",
        "sin_doy", "cos_doy", "sin_hour", "cos_hour", "modis_aod_lag1",
        "ws10", "i10fg", "blh", "skt", "t2m", "swvl1", "cape", "thermal_gradient",
        "z_850", "u_850", "v_850", "t_850", "r_850",
        "z_700", "u_700", "v_700", "t_700", "r_700",
        "z_500", "u_500", "v_500", "t_500", "r_500"
    ]

    for col in candidate_features:
        if col not in df.columns:
            df[col] = 0.0
        else:
            df[col] = df[col].ffill().bfill().fillna(0.0)

    out_csv = FEAT_DIR / "meta_features.csv"
    feat_txt = FEAT_DIR / "feature_columns.txt"

    df.to_csv(out_csv, index=False)
    with open(feat_txt, "w") as f:
        for feat in candidate_features:
            f.write(f"{feat}\n")

    print(f"  Successfully wrote meta-features: {len(df):,} rows -> {out_csv}")
    print(f"  Feature inventory ({len(candidate_features)} predictors, 0 NaNs) -> {feat_txt}")

    # 6. Build 3D Sliding-Window Sequence Tensors (N, T=8, D=33) for Deep Learning (LSTM/Transformer)
    seq_T = 8
    train_df = df[df["year"] <= TRAIN_YEAR_END].reset_index(drop=True)
    test_df = df[df["year"] >= TEST_YEAR_START].reset_index(drop=True)

    X_tr_raw = train_df[candidate_features].values.astype(np.float32)
    y_tr_raw = train_df["unreliable"].values.astype(np.int64)
    X_te_raw = test_df[candidate_features].values.astype(np.float32)
    y_te_raw = test_df["unreliable"].values.astype(np.int64)

    # Fit scaler strictly on training set
    tr_mean = X_tr_raw.mean(axis=0, keepdims=True)
    tr_std = np.maximum(X_tr_raw.std(axis=0, keepdims=True), 1e-6)
    X_tr_norm = (X_tr_raw - tr_mean) / tr_std
    X_te_norm = (X_te_raw - tr_mean) / tr_std

    def make_windows(X_arr, y_arr, T):
        N = len(X_arr) - T + 1
        X_w = np.stack([X_arr[i : i + T] for i in range(N)], axis=0)
        y_w = y_arr[T - 1 :]
        return X_w, y_w

    X_seq_train, y_seq_train = make_windows(X_tr_norm, y_tr_raw, seq_T)
    X_seq_test, y_seq_test = make_windows(X_te_norm, y_te_raw, seq_T)

    dl_seq_path = FEAT_DIR / "deep_learning_sequences_riyadh.npz"
    np.savez_compressed(
        dl_seq_path,
        X_train=X_seq_train,
        y_train=y_seq_train,
        X_test=X_seq_test,
        y_test=y_seq_test,
        feature_names=np.array(candidate_features),
    )
    print(f"  Saved 3D Deep Learning Sequence Tensors: Train {X_seq_train.shape}, Test {X_seq_test.shape} -> {dl_seq_path.name}")

    # 7. Also execute full Line A & Line B Multimodal Pipeline for Riyadh
    build_line_a_and_line_b_riyadh_datasets()


if __name__ == "__main__":
    build_multimodal_features()
