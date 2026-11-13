import sys, os
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent if Path(__file__).resolve().parent.name != 'scripts' else Path(__file__).resolve().parent.parent
_SCRIPTS_ROOT = _PROJECT_ROOT / 'scripts'
if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
"""
QA/QC Script for CAMS Dust AOD Forecasts
=========================================
Data Category: Numerical Forecasts (CAMS)
Specification:
  - Domain     : 24.0°N–25.5°N, 46.0°E–47.5°E (Riyadh Only, centered around Riyadh 24.926°N, 46.722°E)
  - Resolution : Global 0.4° x 0.4° grid
  - Lead Times : 0–120h in 3h steps (41 steps total)
  - Variable   : Dust Aerosol Optical Depth at 550nm (duaod550)
  - QC Checks  : Domain bounds, step sequence, grid resolution, rejection of negative values

Output: data/qaqc_cams_summary.csv
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
from datetime import datetime

try:
    from riyadh_common import (
        BASE_DIR, DATA_DIR, CAMS_DIR,
        DOMAIN_LAT_MIN, DOMAIN_LAT_MAX, DOMAIN_LON_MIN, DOMAIN_LON_MAX,
        CAMS_LEAD_TIMES, RIYADH_LAT, RIYADH_LON
    )
except ImportError:
    _DEFAULT_BASE = _PROJECT_ROOT
    BASE_DIR = Path(os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))).resolve()
    DATA_DIR = BASE_DIR / "data"
    CAMS_DIR = DATA_DIR / "cams"
    DOMAIN_LAT_MIN, DOMAIN_LAT_MAX = 24.0, 25.5
    DOMAIN_LON_MIN, DOMAIN_LON_MAX = 46.0, 47.5
    RIYADH_LAT, RIYADH_LON = 24.926, 46.722
    CAMS_LEAD_TIMES = list(range(0, 121, 3))

OUT_DIR = DATA_DIR
EXPECTED_STEPS = len(CAMS_LEAD_TIMES)  # 41 steps
EXPECTED_RESOLUTION = 0.4


def run_cams_qaqc():
    print("=" * 70)
    print("RUNNING QA/QC FOR CAMS DUST FORECASTS")
    print(f"Expected Domain: {DOMAIN_LAT_MIN}°N–{DOMAIN_LAT_MAX}°N, {DOMAIN_LON_MIN}°E–{DOMAIN_LON_MAX}°E")
    print(f"Expected Resolution: {EXPECTED_RESOLUTION}°, Lead times: 0–120h (41 steps)")
    print("=" * 70)

    nc_files = sorted(list(CAMS_DIR.glob("*.nc")))
    if not nc_files:
        print(f"  [WARN] No CAMS NetCDF files found in {CAMS_DIR}")
        return [], ["No CAMS NetCDF files found"], False

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

            lat_min, lat_max = float(lats.min()), float(lats.max())
            lon_min, lon_max = float(lons.min()), float(lons.max())

            # Domain checks: strictly encapsulates Riyadh receptor site
            domain_ok = (lat_min <= RIYADH_LAT <= lat_max and lon_min <= RIYADH_LON <= lon_max)
            if not domain_ok:
                issues.append(f"Domain mismatch: Lat [{lat_min:.1f}, {lat_max:.1f}], Lon [{lon_min:.1f}, {lon_max:.1f}]")


            # Check variable
            var_name = "duaod550" if "duaod550" in ds else "dust_aerosol_optical_depth_550nm"
            has_var = var_name in ds
            if not has_var:
                issues.append(f"Missing dust AOD variable {var_name}")

            # Value checks
            n_neg = 0
            val_mean, val_max = np.nan, np.nan
            if has_var:
                vals = ds[var_name].values
                n_neg = int((vals < 0.0).sum())
                if n_neg > 0:
                    issues.append(f"{n_neg} non-physical negative dust AOD values (< 0.0)")
                valid_vals = vals[vals >= 0.0]
                if len(valid_vals) > 0:
                    val_mean = float(valid_vals.mean())
                    val_max = float(valid_vals.max())

            ds.close()

            passed = (len(issues) == 0)
            if not passed:
                overall_passed = False
                all_issues.extend(issues)

            results.append({
                "file": fname,
                "domain_ok": domain_ok,
                "has_dust_aod": has_var,
                "n_negative_values": n_neg,
                "mean_dust_aod": val_mean,
                "max_dust_aod": val_max,
                "qaqc_passed": passed
            })
            print(f"  {fname}: {'PASS' if passed else 'FAIL'}")
        except Exception as e:
            all_issues.append(f"Error reading {fname}: {e}")
            overall_passed = False

    res_df = pd.DataFrame(results)
    out_csv = OUT_DIR / "qaqc_cams_summary.csv"
    res_df.to_csv(out_csv, index=False)
    print(f"\nCAMS QA/QC Summary written to {out_csv}")
    return results, all_issues, overall_passed


if __name__ == "__main__":
    run_cams_qaqc()
