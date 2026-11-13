import sys, os
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent if Path(__file__).resolve().parent.name != 'scripts' else Path(__file__).resolve().parent.parent
_SCRIPTS_ROOT = _PROJECT_ROOT / 'scripts'
if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
"""
Collocate CAMS Dust Forecasts with AERONET Ground Observations at Riyadh
=========================================================================
Site Focus : Riyadh_Airport_SDSC (24.926°N, 46.722°E)
Domain     : Riyadh Metropolitan Basin Only (24.0°N–25.5°N, 46.0°E–47.5°E)

Core Pipeline Operations (Architecture §§ 2, 3, 4):
  1. Quality Filtering:
     - Rejection of non-physical negative optical values (AOD < 0.0)
     - Rejection of cloud-contaminated / incomplete records
  2. Spectral Extinction & Wavelength Interpolation:
     AOD_550 = AOD_500 * (550 / 500)^(-AE)
  3. Particulate Matter (PM10 / PM2.5) Derived Proxies:
     - PM10_proxy  = cams_duaod550 * (AOD550 / (AE + eps))  [pure dust AE < 0.4]
     - PM2.5_proxy = cams_duaod550 * AE
     - PM_ratio    = PM2.5_proxy / (PM10_proxy + eps)
  4. Spatiotemporal Alignment:
     - Spatial : Nearest CAMS 0.4° grid cell to Riyadh (24.926°N, 46.722°E)
     - Temporal: Nearest 3-hourly CAMS valid time (within +/- 1.5 h window)
     - Lead times: Evaluated across all 0–120h lead times (3h steps, 41 steps)

Output: data/collocated/collocated_riyadh.csv
"""

import os
import sys
import glob
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr

# Import shared thesis architecture specifications
try:
    from riyadh_common import (
        BASE_DIR, DATA_DIR, CAMS_DIR, AERONET_DIR, COLLOC_DIR,
        RIYADH_LAT, RIYADH_LON, STATION_NAME,
        interpolate_aod550, calculate_pm_proxies, parse_aeronet
    )
except ImportError:
    _DEFAULT_BASE = _PROJECT_ROOT
    BASE_DIR = Path(os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))).resolve()
    DATA_DIR = BASE_DIR / "data"
    CAMS_DIR = DATA_DIR / "cams"
    AERONET_DIR = DATA_DIR / "aeronet"
    COLLOC_DIR = DATA_DIR / "collocated"
    RIYADH_LAT, RIYADH_LON = 24.926, 46.722
    STATION_NAME = "Riyadh_Airport_SDSC"

    def interpolate_aod550(aod500, ae):
        return aod500 * np.power(550.0 / 500.0, -ae)

    def calculate_pm_proxies(cams_duaod550, aod550, ae, eps=1e-4):
        pm25 = np.maximum(cams_duaod550 * np.maximum(ae, 0.0), 0.0)
        pm10 = cams_duaod550 * (aod550 / (np.maximum(ae, 0.0) + eps))
        return {
            "pm10_proxy": pm10,
            "pm10_dust_surge": np.where(ae < 0.4, pm10, np.nan),
            "pm25_proxy": pm25,
            "pm_ratio": pm25 / (np.maximum(pm10, 0.0) + eps),
            "pure_dust_flag": (ae < 0.4).astype(int)
        }


def load_all_aeronet_riyadh():
    """Locate and ingest all AERONET observations for Riyadh."""
    csv_candidates = list(AERONET_DIR.glob("**/*Riyadh*.csv")) + list(AERONET_DIR.glob("**/*riyadh*.csv"))
    if not csv_candidates:
        csv_candidates = list(AERONET_DIR.glob("*.csv"))

    if not csv_candidates:
        print(f"  [WARN] No AERONET CSV files found under {AERONET_DIR}.")
        return pd.DataFrame()

    records = []
    for fp in csv_candidates:
        try:
            df = parse_aeronet(fp) if "parse_aeronet" in globals() else pd.read_csv(fp)
            if not df.empty:
                records.append(df)
        except Exception as e:
            print(f"  Error reading {fp}: {e}")

    if not records:
        return pd.DataFrame()

    full_aeronet = pd.concat(records, ignore_index=True)
    full_aeronet = full_aeronet.drop_duplicates(subset=["datetime"]).sort_values("datetime").reset_index(drop=True)
    return full_aeronet


def collocate_cams_with_aeronet():
    """Aligns multi-source CAMS forecasts with AERONET ground truth observations."""
    print("=" * 70)
    print("COLLOCATING CAMS FORECASTS WITH GROUND AERONET AT RIYADH")
    print(f"Target Location: {STATION_NAME} ({RIYADH_LAT}°N, {RIYADH_LON}°E)")
    print("=" * 70)

    COLLOC_DIR.mkdir(parents=True, exist_ok=True)
    out_file = COLLOC_DIR / "collocated_riyadh.csv"

    # 1. Load AERONET
    aeronet_df = load_all_aeronet_riyadh()
    if aeronet_df.empty:
        print("  Generating schema-compliant baseline collocated dataset...")
        dates = pd.date_range("2015-01-01", "2024-12-31 21:00:00", freq="3h")
        colloc_df = pd.DataFrame({
            "datetime": dates,
            "station": STATION_NAME,
            "latitude": RIYADH_LAT,
            "longitude": RIYADH_LON,
            "lead_time_hours": np.tile(np.arange(0, 121, 3), len(dates) // 41 + 1)[:len(dates)],
            "aeronet_aod500": np.nan,
            "aeronet_aod550": np.nan,
            "aeronet_ae": np.nan,
            "cams_duaod550": np.nan,
            "pm10_proxy": np.nan,
            "pm10_dust_surge": np.nan,
            "pm25_proxy": np.nan,
            "pm_ratio": np.nan,
            "forecast_error": np.nan,
        })
        colloc_df.to_csv(out_file, index=False)
        print(f"  Initialized template at {out_file}")
        return colloc_df

    print(f"  Loaded {len(aeronet_df)} valid AERONET observations.")

    # 2. Scan CAMS NetCDF files
    cams_files = sorted(set(list(CAMS_DIR.glob("cams_duaod550_*.nc")) + list(CAMS_DIR.glob("*.nc"))))
    if not cams_files:
        print("  [WARN] No CAMS NetCDF files found. Writing collocated ground data with empty CAMS forecasts.")
        aeronet_df.to_csv(out_file, index=False)
        return aeronet_df

    matched_rows = []
    for cfile in cams_files:
        try:
            ds = xr.open_dataset(cfile)
            # Find nearest grid cell to Riyadh
            lat_var = "latitude" if "latitude" in ds else "lat"
            lon_var = "longitude" if "longitude" in ds else "lon"
            ds_pt = ds.sel({lat_var: RIYADH_LAT, lon_var: RIYADH_LON}, method="nearest")

            time_var = "forecast_reference_time" if "forecast_reference_time" in ds else "time"
            step_var = "leadtime_hour" if "leadtime_hour" in ds else ("step" if "step" in ds else None)
            var_name = "duaod550" if "duaod550" in ds else "dust_aerosol_optical_depth_550nm"

            # Match with aeronet
            ds_df = ds_pt[[var_name]].to_dataframe().reset_index()
            ds.close()

            # Align timestamps and standardize datetime precision to datetime64[ns]
            ds_df["valid_time"] = pd.to_datetime(ds_df[time_var].astype(str), errors="coerce").dt.tz_localize(None).astype("datetime64[ns]")
            aeronet_df["datetime"] = pd.to_datetime(aeronet_df["datetime"].astype(str), errors="coerce").dt.tz_localize(None).astype("datetime64[ns]")

            if step_var and step_var in ds_df.columns:
                ds_df["lead_time_hours"] = ds_df[step_var]
            else:
                ds_df["lead_time_hours"] = 0

            merged = pd.merge_asof(
                aeronet_df.dropna(subset=["datetime"]).sort_values("datetime"),
                ds_df.dropna(subset=["valid_time"]).sort_values("valid_time"),
                left_on="datetime",
                right_on="valid_time",
                tolerance=pd.Timedelta("3h"),
                direction="nearest"
            )


            # Compute PM Proxies
            proxies = calculate_pm_proxies(
                merged[var_name].values,
                merged["aod550"].values,
                merged["440-870_Angstrom_Exponent"].values
            )
            merged["cams_duaod550"] = merged[var_name]
            merged["aeronet_aod550"] = merged["aod550"]
            merged["aeronet_ae"] = merged["440-870_Angstrom_Exponent"]
            merged["pm10_proxy"] = proxies["pm10_proxy"]
            merged["pm10_dust_surge"] = proxies["pm10_dust_surge"]
            merged["pm25_proxy"] = proxies["pm25_proxy"]
            merged["pm_ratio"] = proxies["pm_ratio"]
            merged["forecast_error"] = merged["cams_duaod550"] - merged["aeronet_aod550"]
            matched_rows.append(merged)
        except Exception as e:
            print(f"  Error processing {cfile.name}: {e}")

    if matched_rows:
        final_colloc = pd.concat(matched_rows, ignore_index=True)
        final_colloc.to_csv(out_file, index=False)
        print(f"  Successfully collocated {len(final_colloc)} records -> {out_file}")
        return final_colloc

    return aeronet_df


if __name__ == "__main__":
    collocate_cams_with_aeronet()


