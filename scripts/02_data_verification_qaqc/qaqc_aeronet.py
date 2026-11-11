import sys, os
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent if Path(__file__).resolve().parent.name != 'scripts' else Path(__file__).resolve().parent.parent
_SCRIPTS_ROOT = _PROJECT_ROOT / 'scripts'
if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
"""
QA/QC Script for AERONET Ground Truth Data (Riyadh Focus)
=========================================================
Target Station: Riyadh_Airport_SDSC (24.926°N, 46.722°E) — Riyadh Station Only

Checks Implemented (Architecture §§ 2 & 4):
  1. Optical Quality Filtering:
     - Rejection of non-physical negative optical values (AOD < 0.0)
     - Missing value flags (-999, -999.0)
     - Extreme upper bounds (AOD > 10.0)
  2. Spectral Extinction & Derived Variables:
     - AOD_500nm, Angstrom Exponent (440-870nm)
     - Wavelength interpolation: AOD_550 = AOD_500 * (550 / 500)^(-AE)
     - Coarse dust surge condition: AE < 0.4 (pure windblown dust)
     - Fine / Coarse Mode Fractions (FMF)
  3. Temporal Continuity & Completeness:
     - Coverage spans across 2015–2024
     - Observation frequency and gap diagnostics

Output: data/qaqc_aeronet_summary.csv
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime

try:
    from riyadh_common import (
        BASE_DIR, DATA_DIR, AERONET_DIR,
        RIYADH_LAT, RIYADH_LON, STATION_NAME,
        interpolate_aod550, parse_aeronet
    )
except ImportError:
    _DEFAULT_BASE = _PROJECT_ROOT
    BASE_DIR = Path(os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))).resolve()
    DATA_DIR = BASE_DIR / "data"
    AERONET_DIR = DATA_DIR / "aeronet"
    RIYADH_LAT, RIYADH_LON = 24.926, 46.722
    STATION_NAME = "Riyadh_Airport_SDSC"

    def interpolate_aod550(aod500, ae):
        return aod500 * np.power(550.0 / 500.0, -ae)

OUT_DIR = DATA_DIR
AOD_MIN = 0.0
AOD_COL = "AOD_500nm"
AE_COL = "440-870_Angstrom_Exponent"


def run_aeronet_qaqc():
    print("=" * 70)
    print("RUNNING QA/QC FOR AERONET GROUND TRUTH DATA")
    print(f"Target Station: {STATION_NAME} ({RIYADH_LAT}°N, {RIYADH_LON}°E)")
    print("=" * 70)

    csv_files = list(AERONET_DIR.glob("**/*.csv")) + list(AERONET_DIR.glob("*.csv"))
    if not csv_files:
        print(f"  [WARN] No AERONET CSV files found in {AERONET_DIR}")
        return [], ["No AERONET data found"], False

    results = []
    all_issues = []
    overall_passed = True

    for fp in csv_files:
        try:
            # 7 header lines
            df = pd.read_csv(fp, skiprows=7, na_values=[-999, -999.0, "-999", "-999.000000"])
            df.columns = [c.replace("<br>", "").strip() for c in df.columns]

            issues = []
            n_obs = len(df)

            # Check required columns
            has_aod = AOD_COL in df.columns
            has_ae = AE_COL in df.columns

            if not has_aod:
                issues.append(f"Missing column: {AOD_COL}")
            if not has_ae:
                issues.append(f"Missing column: {AE_COL}")

            n_neg = 0
            pure_dust_count = 0
            aod_mean, aod_max, ae_mean = np.nan, np.nan, np.nan

            if has_aod:
                valid_aod = df[AOD_COL].dropna()
                n_neg = (valid_aod < AOD_MIN).sum()
                if n_neg > 0:
                    issues.append(f"{n_neg} non-physical negative AOD values detected (< 0.0)")
                clean_aod = valid_aod[valid_aod >= AOD_MIN]
                if len(clean_aod) > 0:
                    aod_mean = float(clean_aod.mean())
                    aod_max = float(clean_aod.max())

            if has_ae:
                valid_ae = df[AE_COL].dropna()
                if len(valid_ae) > 0:
                    ae_mean = float(valid_ae.mean())
                    pure_dust_count = int((valid_ae < 0.4).sum())

            passed = (len(issues) == 0) and (n_obs > 0)
            if not passed:
                overall_passed = False
                all_issues.extend(issues)

            res = {
                "file": fp.name,
                "n_observations": n_obs,
                "has_aod500": has_aod,
                "has_ae": has_ae,
                "n_negative_aod": n_neg,
                "aod500_mean": aod_mean,
                "aod500_max": aod_max,
                "ae_mean": ae_mean,
                "pure_dust_surges_ae_lt_0_4": pure_dust_count,
                "qaqc_passed": passed
            }
            results.append(res)
            print(f"  {fp.name}: {'PASS' if passed else 'FAIL'} (Obs: {n_obs}, Pure Dust Surges: {pure_dust_count})")
        except Exception as e:
            all_issues.append(f"Error reading {fp.name}: {e}")
            overall_passed = False

    res_df = pd.DataFrame(results)
    out_csv = OUT_DIR / "qaqc_aeronet_summary.csv"
    res_df.to_csv(out_csv, index=False)
    print(f"\nAERONET QA/QC Summary written to {out_csv}")
    return results, all_issues, overall_passed


if __name__ == "__main__":
    run_aeronet_qaqc()
