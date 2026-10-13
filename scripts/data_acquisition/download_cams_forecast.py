"""
Production script for downloading CAMS global atmospheric composition forecasts
(PM10, Dust AOD, 10m Wind) from Copernicus ADS into data/raw/nwp/.

Supports automatic key discovery:
  1. Keys/API_Key/API.txt
  2. ~/.cdsapirc (C:\\Users\\<you>\\.cdsapirc)
  3. ADS_API_KEY environment variable
  4. Command line --key argument
"""

import os
import sys
import argparse
from pathlib import Path

out_dir = Path("data/raw/nwp")
out_dir.mkdir(parents=True, exist_ok=True)

def find_api_credentials():
    # 1. Environment variable
    env_key = os.environ.get("ADS_API_KEY") or os.environ.get("CDS_API_KEY")
    if env_key:
        return "https://ads.atmosphere.copernicus.eu/api", env_key.strip()

    # 2. Project Keys directory
    local_key_file = Path("Keys/API_Key/API.txt")
    if local_key_file.exists():
        content = local_key_file.read_text(encoding="utf-8").strip()
        if content:
            # Check if key is formatted as url / key or just the token
            lines = [l.strip() for l in content.splitlines() if l.strip()]
            for line in lines:
                if line.startswith("key:"):
                    return "https://ads.atmosphere.copernicus.eu/api", line.replace("key:", "").strip()
            if len(lines) == 1 and not lines[0].startswith("http"):
                return "https://ads.atmosphere.copernicus.eu/api", lines[0]

    # 3. User home ~/.cdsapirc
    home_rc = Path.home() / ".cdsapirc"
    if home_rc.exists():
        url, key = None, None
        for line in home_rc.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("url:"):
                url = line.split(":", 1)[1].strip()
            elif line.startswith("key:"):
                key = line.split(":", 1)[1].strip()
        if key:
            # Force ADS endpoint for CAMS
            return "https://ads.atmosphere.copernicus.eu/api", key

    return None, None

def download_cams_forecast(key=None, months=("03", "04", "05"), test_run=False):
    try:
        import cdsapi
    except ImportError:
        print("[Error] cdsapi is not installed. Run: pip install cdsapi")
        return False

    url, api_key = None, key
    if not api_key:
        url, api_key = find_api_credentials()

    if not api_key:
        print("\n" + "=" * 65)
        print("[!] Missing Copernicus API Key for NWP (CAMS) downloads!")
        print("To download real NWP forecasts into data/raw/nwp/, please either:")
        print("  1. Paste your key into: Keys/API_Key/API.txt")
        print("  2. Or create C:\\Users\\hp\\.cdsapirc with:")
        print("       url: https://ads.atmosphere.copernicus.eu/api")
        print("       key: <your-personal-access-token>")
        print("  3. Register & get your key at: https://ads.atmosphere.copernicus.eu/")
        print("     Remember to accept the dataset license on the CAMS page.")
        print("=" * 65 + "\n")
        return False

    url = url or "https://ads.atmosphere.copernicus.eu/api"
    print(f"[CAMS] Initializing client with endpoint: {url}")
    client = cdsapi.Client(url=url, key=api_key)

    variables = [
        "particulate_matter_10um",
        "dust_aerosol_optical_depth_550nm",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind"
    ]

    for month in months:
        target_file = out_dir / f"cams_forecast_2021_{month}.nc"
        if target_file.exists() and target_file.stat().st_size > 1024 * 1024:
            print(f"[CAMS] {target_file.name} already exists. Skipping.")
            continue

        date_range = f"2021-{month}-01/2021-{month}-05" if test_run else f"2021-{month}-01/2021-{month}-31"
        lead_hours = [str(h) for h in range(72, 121, 6)]  # 72h to 120h at 6h steps

        print(f"[CAMS] Requesting {date_range} (Leads: 72h-120h) -> {target_file.name}...")
        try:
            client.retrieve(
                "cams-global-atmospheric-composition-forecasts",
                {
                    "variable": variables,
                    "date": date_range,
                    "time": ["00:00", "12:00"],
                    "leadtime_hour": lead_hours,
                    "type": ["forecast"],
                    "area": [55, 70, 25, 135], # N, W, S, E
                    "data_format": "netcdf",
                },
                str(target_file)
            )
            print(f"[CAMS] Saved: {target_file}")
        except Exception as e:
            print(f"[CAMS Error] Failed to retrieve month {month}: {e}")
            if "licence" in str(e).lower():
                print(">> LICENCE ERROR: Please go to the CAMS dataset page and click 'Accept Licence'.")
            return False

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download CAMS atmospheric forecast into data/raw/nwp/")
    parser.add_argument("--key", type=str, default=None, help="Copernicus personal access token")
    parser.add_argument("--test", action="store_true", help="Download short 5-day test chunk")
    parser.add_argument("--month", type=str, default="03", help="Specific month (03, 04, 05)")
    args = parser.parse_args()

    months = [args.month] if args.month else ["03", "04", "05"]
    download_cams_forecast(key=args.key, months=months, test_run=args.test)
