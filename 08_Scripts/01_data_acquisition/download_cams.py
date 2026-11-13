"""
Download CAMS Global Dust AOD Forecasts — 2015 to 2024 (30-Day Batches)
========================================================================
Data Category: Numerical Forecasts (CAMS)
Variables    : Dust Aerosol Optical Depth at 550nm (duaod550)
Domain       : 20.0°N–34.0°N, 45.0°E–60.0°E (centered around Riyadh)
Resolution   : Global 0.4° x 0.4°, 0–120h lead times (3h steps, 41 total steps)
Period       : 2015-01-01 to 2024-12-31
Init time    : 00:00 UTC
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import os
from pathlib import Path
import sys
import time

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = (
    _SCRIPT_DIR.parent.parent
    if _SCRIPT_DIR.name == "scripts"
    else _SCRIPT_DIR.parent
)
_SCRIPTS_ROOT = _PROJECT_ROOT / "scripts"

if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

# --- Paths & Common Configuration ---
_DEFAULT_BASE = _PROJECT_ROOT
BASE_DIR = Path(
    os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))
).resolve()
OUTPUT_DIR = str(BASE_DIR / "data" / "cams")
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

try:
    from riyadh_common import AREA_BOUNDS, CAMS_LEAD_TIMES, get_cds_client
except ImportError:
    AREA_BOUNDS = [34.0, 45.0, 20.0, 60.0]  # North, West, South, East
    CAMS_LEAD_TIMES = list(range(0, 121, 3))

    def get_cds_client(default_url=None, timeout=1800, retry_max=5):
        import cdsapi

        return cdsapi.Client(url=default_url, timeout=timeout, retry_max=retry_max)


DATASET = "cams-global-atmospheric-composition-forecasts"
ADS_URL = "https://ads.atmosphere.copernicus.eu/api"
LEADTIMES_STR = [str(h) for h in CAMS_LEAD_TIMES]


def download_cams_window(start_date, end_date):
    """Download a single 30-day forecast chunk safely with an independent client."""
    client = get_cds_client(default_url=ADS_URL, timeout=1800, retry_max=5)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    label = f"{start_str}_to_{end_str}"
    win_name = f"cams_{label}.nc"
    win_path = os.path.join(TEMP_DIR, win_name)

    # Resume check: Skip if file already exists and is non-empty
    if os.path.exists(win_path) and os.path.getsize(win_path) > 1024:
        print(f"  [SKIP] {label} already downloaded.")
        return True

    date_str = f"{start_str}/{end_str}"
    request = {
        "type": "forecast",
        "variable": ["dust_aerosol_optical_depth_550nm"],
        "date": date_str,
        "time": "00:00",
        "leadtime_hour": LEADTIMES_STR,
        "area": AREA_BOUNDS,
        "data_format": "netcdf",
    }

    print(f"  [FETCH] Requesting CAMS {label} (0-120h leadtimes, 0.4° grid)...", flush=True)
    try:
        client.retrieve(DATASET, request, win_path)
        size_mb = os.path.getsize(win_path) / (1024 * 1024)
        print(f"  [DONE] {label} -> {size_mb:.2f} MB", flush=True)
        return True
    except Exception as e:
        print(f"  [FAIL] {label} error: {e}", flush=True)
        if os.path.exists(win_path):
            try:
                os.remove(win_path)
            except OSError:
                pass
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Parallelized CAMS Dust Forecasts Downloader (2015–2024)"
    )
    parser.add_argument("--start-year", type=int, default=2015, help="Default: 2015")
    parser.add_argument("--end-year", type=int, default=2024, help="Default: 2024")
    parser.add_argument(
        "--max-workers",
        type=int,
        default=5,
        help="Simultaneous requests (keep between 3-5 to prevent CDS API queue rate limits)",
    )
    args = parser.parse_args()

    overall_start = datetime.date(args.start_year, 1, 1)
    overall_end = datetime.date(args.end_year, 12, 31)

    # Build list of 30-day windows
    tasks = []
    current_start = overall_start
    while current_start <= overall_end:
        current_end = min(current_start + datetime.timedelta(days=29), overall_end)
        tasks.append((current_start, current_end))
        current_start = current_end + datetime.timedelta(days=1)

    print("=" * 65)
    print(f"Target Period : {overall_start} to {overall_end}")
    print(f"Total Batches : {len(tasks)} windows (30 days each)")
    print(f"Workers       : {args.max_workers} parallel connections")
    print(f"Output Target : {TEMP_DIR}")
    print("=" * 65)

    failed = []
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = {
            executor.submit(download_cams_window, start, end): (start, end)
            for (start, end) in tasks
        }
        for future in as_completed(futures):
            start, end = futures[future]
            try:
                success = future.result()
                if not success:
                    failed.append((start, end))
                    print(f"⚠️ Warning: Chunk {start} to {end} failed.")
            except Exception as exc:
                failed.append((start, end))
                print(f"❌ Error on task {start} to {end}: {exc}")

    print("\n" + "=" * 65)
    if failed:
        print(f"Completed with {len(failed)} failed tasks.")
        print("Re-run the same command anytime; completed files will automatically skip.")
    else:
        print("All chunks from 2015 to 2024 downloaded successfully.")
    print("=" * 65)


if __name__ == "__main__":
    main()