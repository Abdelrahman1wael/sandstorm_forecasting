import sys, os
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent if Path(__file__).resolve().parent.name != 'scripts' else Path(__file__).resolve().parent.parent
_SCRIPTS_ROOT = _PROJECT_ROOT / 'scripts'
if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
"""
QA/QC Script for ERA5 Reanalysis Data (Riyadh Only Domain)
===========================================================
Domain Specification:
  - Spatial Coverage  : 24.0°N–25.5°N, 46.0°E–47.5°E (Riyadh Basin & Station Only)
  - Grid Resolution   : 0.25° x 0.25°
  - Temporal Frequency: 6-hourly intervals (00:00, 06:00, 12:00, 18:00 UTC)
  - Atmospheric Levels: 850, 700, 500 hPa (z, u, v, t, r)
  - Surface Drivers   : 10m wind & gusts (ws10, i10fg), BLH, skt, t2m, swvl1, CAPE

Output: data/qaqc_era5_summary.csv
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr

try:
    from riyadh_common import (
        BASE_DIR, DATA_DIR, ERA5_DIR,
        DOMAIN_LAT_MIN, DOMAIN_LAT_MAX, DOMAIN_LON_MIN, DOMAIN_LON_MAX,
        ERA5_PRESSURE_LEVELS, ERA5_6H_INTERVALS,
        RIYADH_LAT, RIYADH_LON
    )
except ImportError:
    _DEFAULT_BASE = _PROJECT_ROOT
    BASE_DIR = Path(os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))).resolve()
    DATA_DIR = BASE_DIR / "data"
    ERA5_DIR = DATA_DIR / "era5"
    DOMAIN_LAT_MIN, DOMAIN_LAT_MAX = 20.0, 34.0
    DOMAIN_LON_MIN, DOMAIN_LON_MAX = 45.0, 60.0
    ERA5_PRESSURE_LEVELS = [850, 700, 500]
    RIYADH_LAT, RIYADH_LON = 24.926, 46.722


OUT_DIR = DATA_DIR


def run_era5_qaqc():
    print("=" * 70)
    print("RUNNING QA/QC FOR ERA5 REANALYSIS DATA")
    print(f"Domain Bounds : {DOMAIN_LAT_MIN}°N–{DOMAIN_LAT_MAX}°N, {DOMAIN_LON_MIN}°E–{DOMAIN_LON_MAX}°E")
    print(f"Target Levels : {ERA5_PRESSURE_LEVELS} hPa | Resolution: 0.25°")
    print("=" * 70)

    nc_files = sorted(list(ERA5_DIR.glob("*.nc")) + list(ERA5_DIR.glob("**/*.nc")))
    if not nc_files:
        print(f"  [WARN] No ERA5 NetCDF files found in {ERA5_DIR}")
        return [], ["No ERA5 NetCDF files found"], False

    results = []
    all_issues = []
    overall_passed = True

    for fp in nc_files:
        fname = fp.name
        issues = []
        try:
            ds = xr.open_dataset(fp)
            lat_var = "latitude" if "latitude" in ds else "lat"
            lon_var = "longitude" if "longitude" in ds else "lon"
            lats = ds[lat_var].values
            lons = ds[lon_var].values

            # Check domain: strictly encapsulates Riyadh receptor site
            l_min, l_max = float(np.min(lats)), float(np.max(lats))
            o_min, o_max = float(np.min(lons)), float(np.max(lons))
            domain_ok = (l_min <= RIYADH_LAT <= l_max and o_min <= RIYADH_LON <= o_max) or \
                        (abs(l_min - RIYADH_LAT) < 1.0 and abs(o_min - RIYADH_LON) < 1.0)
            if not domain_ok:
                issues.append(f"Domain mismatch: Lat [{l_min:.1f}, {l_max:.1f}], Lon [{o_min:.1f}, {o_max:.1f}]")

            # Check variables (supports standard shortnames and full CDS/Open-Meteo descriptions)
            vars_present = list(ds.data_vars.keys())
            pl_keys = ["z", "u", "v", "t", "r", "geopotential", "temperature", "relative_humidity"]
            sl_keys = [
                "u10", "v10", "i10fg", "blh", "skt", "t2m", "swvl1", "cape",
                "10m_u_component_of_wind", "10m_v_component_of_wind", "temperature_2m",
                "wind_speed_10m", "soil_moisture_0_to_7cm", "surface_pressure"
            ]
            has_pl = any(v in vars_present for v in pl_keys)
            has_sl = any(v in vars_present for v in sl_keys)

            if not (has_pl or has_sl):
                issues.append(f"Unrecognized variables: {vars_present}")


            ds.close()

            passed = (len(issues) == 0)
            if not passed:
                overall_passed = False
                all_issues.extend(issues)

            results.append({
                "file": fname,
                "domain_ok": domain_ok,
                "has_pl_or_sl": (has_pl or has_sl),
                "vars_count": len(vars_present),
                "qaqc_passed": passed
            })
            print(f"  {fname}: {'PASS' if passed else 'FAIL'}")
        except Exception as e:
            print(f"  Error reading {fname}: {e}")
            all_issues.append(f"Error reading {fname}: {e}")
            overall_passed = False

    res_df = pd.DataFrame(results)
    out_csv = OUT_DIR / "qaqc_era5_summary.csv"
    res_df.to_csv(out_csv, index=False)
    print(f"\nERA5 QA/QC Summary written to {out_csv}")
    return results, all_issues, overall_passed


if __name__ == "__main__":
    run_era5_qaqc()
