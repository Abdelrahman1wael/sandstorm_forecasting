import sys, os
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent if Path(__file__).resolve().parent.name != 'scripts' else Path(__file__).resolve().parent.parent
_SCRIPTS_ROOT = _PROJECT_ROOT / 'scripts'
if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
"""
Download MODIS Deep Blue AOD (550 nm) from MOD08_D3 via OPeNDAP
================================================================
Extracts daily 1° grid-cell values at each AERONET station location.
Purpose (architecture §2): third-layer verification of AERONET readings,
independent of CAMS, over the unified domain 20–34°N / 45–60°E.

Product : MOD08_D3 v061 (MODIS/Terra Atmosphere Daily L3 Global 1Deg CMG)
Variables:
  - Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean (works over desert)
  - AOD_550_Dark_Target_Deep_Blue_Combined_Mean (merged DT+DB product)
Grid    : 1° x 1°, 180 rows x 360 cols (cell centres 89.5N..-89.5, -179.5..179.5)
Scale   : 0.001 (raw * 0.001 = AOD)
Fill    : -9999
QC      : non-physical AOD < 0 masked to NaN (architecture §4)

Cell mapping (nearest 1° cell centre):
    row = round(89.5 - lat)      col = round(lon + 179.5)
    Sub-region rows 55..69  -> cell centres 34.5N .. 20.5N  (covers 20-34N)
    Sub-region cols 225..240 -> cell centres 45.5E .. 60.5E (covers 45-60E)

FIXES vs previous version:
  1. Credentials read from environment variables (were hard-coded - security risk).
  2. Robust OPeNDAP ASCII parser: parses floats (old int() parsing silently
     dropped entire rows if the server returned float-formatted values),
     skips the [start_col] header token, guards column count, handles
     scientific notation and NaN tokens.
  3. Retry with exponential backoff on 429/5xx/timeouts (old code wrote NaN
     for the whole day on any transient failure).
  4. Clear error message if the filename cache is missing (old code crashed
     with a bare FileNotFoundError).
  5. QC per architecture §4: scaled AOD < 0 masked to NaN.
  6. Yearly checkpoints written atomically (.tmp -> rename), so an interrupted
     run never leaves a partial year CSV that looks complete on re-run.
  7. Grid-cell centre lat/lon written to output for traceability; station
     indices validated against the sub-region bounds at startup.
  8. Days sorted numerically (string sort broke if doy padding was inconsistent).
"""

import os
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta

# --- Config ---
_DEFAULT_BASE = _PROJECT_ROOT
BASE = os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))
OUTPUT_DIR = os.path.join(BASE, "data", "modis")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Credentials from environment (set before running):
#   set EARTHDATA_USER=your_user
#   set EARTHDATA_PASS=your_password
EARTHDATA_USER = os.environ.get("EARTHDATA_USER", "")
EARTHDATA_PASS = os.environ.get("EARTHDATA_PASS", "")

STATIONS = {
    "Riyadh_Airport_SDSC": {"lat": 24.926, "lon": 46.722},
    "Riyadh_Diriyah": {"lat": 24.729, "lon": 46.573},
    "Riyadh_IMSI": {"lat": 24.713, "lon": 46.625},
    "Solar_Village": {"lat": 24.907, "lon": 46.397},
}



VARIABLES = {
    "db_aod550":   "Deep_Blue_Aerosol_Optical_Depth_550_Land_Mean",
    "dtdb_aod550": "AOD_550_Dark_Target_Deep_Blue_Combined_Mean",
}

SCALE_FACTOR = 0.001
FILL_VALUE = -9999

# Sub-region covering all stations (unified domain, architecture §4):
# rows 55..69  = cell centres 34.5N .. 20.5N ; cols 225..240 = 45.5E .. 60.5E
Y1, Y2 = 55, 69
X1, X2 = 225, 240
NY = Y2 - Y1 + 1
NX = X2 - X1 + 1

START_YEAR = 2015
END_YEAR = 2024

REQUEST_TIMEOUT = 60       # seconds per OPeNDAP request
SLEEP_BETWEEN_DAYS = 0.05  # polite delay


def latlon_to_subgrid(lat, lon):
    """Nearest 1° cell centre -> indices relative to the sub-region."""
    y_global = int(round(89.5 - lat))
    x_global = int(round(lon + 179.5))
    return y_global - Y1, x_global - X1


def cell_center_latlon(y_global, x_global):
    return 89.5 - y_global, x_global - 179.5


def parse_opendap_ascii(text, ny=NY, nx=NX):
    """
    Parse an OPeNDAP .ascii response of the form:
        var[55][225], -9999, 123, 456, ...
        var[56][225], ...
    Returns a (ny, nx) float array with fill values as NaN, scaled by
    SCALE_FACTOR. Tolerates float/scientific-notation values and the
    [start_col] header token.
    """
    arr = np.full((ny, nx), np.nan)
    n_lines = 0
    for line in text.splitlines():
        line = line.strip()
        if "[" not in line or "," not in line:
            continue  # skip Dataset/declaration header lines
        try:
            i0 = line.index("[")
            i1 = line.index("]")
            row = int(line[i0 + 1:i1])
            if not (0 <= row < ny):
                continue
            rest = line[i1 + 1:]
            # rest looks like "[225], v1, v2, ..." -> drop the [start_col] token
            if rest.lstrip().startswith("["):
                rest = rest[rest.index(",") + 1:]
            values = rest.split(",")
            if len(values) != nx:
                # unexpected width; still parse what we can
                pass
            for c, tok in enumerate(values):
                if c >= nx:
                    break
                tok = tok.strip()
                if not tok:
                    continue
                try:
                    raw = float(tok)
                except ValueError:
                    continue
                if not np.isfinite(raw) or raw == FILL_VALUE:
                    continue
                arr[row, c] = raw * SCALE_FACTOR
            n_lines += 1
        except (ValueError, IndexError):
            continue
    if n_lines == 0:
        return None  # response had no data rows
    return arr


def apply_qc(arr):
    """Architecture §4: reject non-physical negative optical values."""
    out = arr.astype(float).copy()
    out[out < 0] = np.nan
    return out


def build_session():
    session = requests.Session()
    session.auth = (EARTHDATA_USER, EARTHDATA_PASS)
    retry = Retry(
        total=4,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def extract_day(session, year, doy, fname):
    """Download both variables for one day; returns dict of QC'd grids.

    A persistent failure after retries returns NaN grids for that day only.
    """
    opendap_base = (
        f"https://ladsweb.modaps.eosdis.nasa.gov/opendap/RemoteResources/laads/"
        f"allData/61/MOD08_D3/{year}/{doy}/{fname}"
    )
    grids = {}
    for short_name, full_name in VARIABLES.items():
        url = f"{opendap_base}.ascii?{full_name}[{Y1}:{Y2}][{X1}:{X2}]"
        arr = None
        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT)
            if resp.status_code == 200:
                arr = parse_opendap_ascii(resp.text)
            elif resp.status_code in (401, 403):
                raise RuntimeError(
                    f"Earthdata auth failed (HTTP {resp.status_code}). "
                    "Check EARTHDATA_USER / EARTHDATA_PASS."
                )
            # 404 (file not at LAADS yet) -> arr stays None -> NaN grid
        except requests.exceptions.RequestException:
            arr = None  # retries exhausted
        if arr is None:
            arr = np.full((NY, NX), np.nan)
        grids[short_name] = apply_qc(arr)
        time.sleep(0.05)  # small pause between the 2 variable requests
    return grids


def main():
    if not EARTHDATA_USER or not EARTHDATA_PASS:
        raise SystemExit(
            "ERROR: set EARTHDATA_USER and EARTHDATA_PASS environment "
            "variables before running."
        )

    session = build_session()

    # --- Load cached filenames ---
    cache_path = os.path.join(OUTPUT_DIR, "mod08d3_filenames.json")
    if not os.path.exists(cache_path):
        raise SystemExit(
            f"ERROR: filename cache not found at:\n  {cache_path}\n"
            "Run the filename-listing step first to build mod08d3_filenames.json."
        )
    with open(cache_path) as f:
        fname_cache = json.load(f)
    print(f"Loaded {len(fname_cache)} cached filenames")

    # --- Pre-compute & validate sub-grid indices ---
    stn_idx = {}
    for name, coords in STATIONS.items():
        sy, sx = latlon_to_subgrid(coords["lat"], coords["lon"])
        if not (0 <= sy < NY and 0 <= sx < NX):
            raise ValueError(f"{name} falls outside the sub-region - check coordinates.")
        glat, glon = cell_center_latlon(sy + Y1, sx + X1)
        stn_idx[name] = (sy, sx, glat, glon)
        print(f"  {name}: ({coords['lat']:.3f}N, {coords['lon']:.3f}E) "
              f"-> cell centre ({glat:.1f}N, {glon:.1f}E) subgrid[{sy},{sx}]")

    all_rows = []

    for year in range(START_YEAR, END_YEAR + 1):
        print(f"\n{'=' * 50}\nYear {year}\n{'=' * 50}")

        # --- Checkpoint (atomic writes mean an existing file is complete) ---
        ckpt = os.path.join(OUTPUT_DIR, f"modis_aod_{year}.csv")
        if os.path.exists(ckpt):
            df_ckpt = pd.read_csv(ckpt)
            all_rows.extend(df_ckpt.to_dict("records"))
            print(f"  Loaded checkpoint: {len(df_ckpt)} rows")
            continue

        # --- Days for this year, sorted numerically ---
        year_files = {d: fn for k, fn in fname_cache.items()
                      for y, d in [k.split("_", 1)] if int(y) == year}
        if not year_files:
            print("  WARNING: no files in cache for this year - skipped.")
            continue

        print(f"  {len(year_files)} days to process")
        year_rows = []

        for i, doy in enumerate(sorted(year_files, key=int)):
            fname = year_files[doy]
            date = datetime(year, 1, 1) + timedelta(days=int(doy) - 1)

            try:
                grids = extract_day(session, year, doy, fname)
            except RuntimeError as e:
                raise SystemExit(str(e))

            for stn_name, (sy, sx, glat, glon) in stn_idx.items():
                year_rows.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "doy": int(doy),
                    "station": stn_name,
                    "grid_lat": glat,
                    "grid_lon": glon,
                    "modis_db_aod550": grids["db_aod550"][sy, sx],
                    "modis_dtdb_aod550": grids["dtdb_aod550"][sy, sx],
                })

            if (i + 1) % 50 == 0:
                last = year_rows[-len(STATIONS) * 50:]
                valid_db = sum(1 for r in last if not np.isnan(r["modis_db_aod550"]))
                print(f"  {date.strftime('%Y-%m-%d')} ({i + 1}/{len(year_files)}) "
                      f"valid DB: {valid_db}/{len(last)}")

            time.sleep(SLEEP_BETWEEN_DAYS)

        # --- Atomic save: tmp file then rename ---
        df_year = pd.DataFrame(year_rows)
        tmp_path = ckpt + ".tmp"
        df_year.to_csv(tmp_path, index=False)
        os.replace(tmp_path, ckpt)
        valid = df_year["modis_db_aod550"].notna().sum()
        print(f"  Saved {len(df_year)} rows "
              f"({valid} valid Deep Blue, {valid / len(df_year) * 100:.0f}%)")
        all_rows.extend(year_rows)

    # --- Combined output ---
    df_all = pd.DataFrame(all_rows)
    if df_all.empty:
        raise SystemExit("No rows collected - nothing to save.")
    out_path = os.path.join(OUTPUT_DIR, "modis_aod_all_stations.csv")
    df_all.to_csv(out_path, index=False)

    print(f"\n{'=' * 50}")
    print(f"DONE: {len(df_all)} total rows")
    print(f"Valid Deep Blue: {df_all['modis_db_aod550'].notna().sum()} "
          f"({df_all['modis_db_aod550'].notna().mean() * 100:.1f}%)")
    print(f"Valid Combined:  {df_all['modis_dtdb_aod550'].notna().sum()} "
          f"({df_all['modis_dtdb_aod550'].notna().mean() * 100:.1f}%)")
    print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()