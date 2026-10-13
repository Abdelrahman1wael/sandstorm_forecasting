"""
Script to download CAMS NWP atmospheric composition forecasts
specifically for the Kingdom of Saudi Arabia & Arabian Peninsula domain.

Domain Bounding Box: [33°N, 34°E, 16°N, 56°E] (North: 33, West: 34, South: 16, East: 56)
Target Variables:
  - particulate_matter_10um (PM10)
  - dust_aerosol_optical_depth_550nm (Dust AOD)
  - 10m_u_component_of_wind
  - 10m_v_component_of_wind
Lead Times: 72h to 120h (extended-range 3-5 days)
"""

import os
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

out_dir = Path("data/raw/nwp")
out_dir.mkdir(parents=True, exist_ok=True)

def find_api_credentials():
    key_file = Path("Keys/API_Key/API.txt")
    api_key = None
    url = "https://ads.atmosphere.copernicus.eu/api"
    if key_file.exists():
        for line in key_file.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("key:"):
                api_key = line.split(":", 1)[1].strip()
            elif line.strip().startswith("url:"):
                url = line.split(":", 1)[1].strip()
            elif len(line.strip()) == 36 and "-" in line.strip():
                api_key = line.strip()
    return url, api_key

def download_saudi_nwp(date_range="2024-04-01/2024-04-03", output_filename="cams_forecast_saudi_arabia.nc"):
    try:
        import cdsapi
    except ImportError:
        print("[Error] cdsapi is not installed.")
        return False

    url, api_key = find_api_credentials()
    if not api_key:
        print("[Error] No Copernicus API key found in Keys/API_Key/API.txt")
        return False

    print("=" * 70)
    print("[CAMS] DOWNLOADING REAL NWP FORECAST FOR SAUDI ARABIA")
    print("=" * 70)
    print(f"Domain Area (N/W/S/E): [33N, 34E, 16N, 56E]")
    print(f"Target Dates:          {date_range}")
    print(f"Destination:           {out_dir / output_filename}")
    print(f"Connecting to:         {url}")
    print("=" * 70)

    client = cdsapi.Client(url=url, key=api_key)

    variables = [
        "particulate_matter_10um",
        "dust_aerosol_optical_depth_550nm",
        "10m_u_component_of_wind",
        "10m_v_component_of_wind"
    ]
    lead_hours = [str(h) for h in range(72, 121, 6)] # 72h to 120h (Extended Range 3-5 Days)
    target_path = out_dir / output_filename

    request_params = {
        "variable": variables,
        "date": date_range,
        "time": ["00:00", "12:00"],
        "leadtime_hour": lead_hours,
        "type": ["forecast"],
        "area": [33, 34, 16, 56],  # Saudi Arabia: North, West, South, East
        "data_format": "netcdf",
    }

    try:
        print("[CAMS] Submitting request to Copernicus queue...")
        client.retrieve("cams-global-atmospheric-composition-forecasts", request_params, str(target_path))
        print(f"✅ Successfully downloaded Saudi Arabia NWP dataset: {target_path} ({target_path.stat().st_size / 1e6:.2f} MB)")
        return True
    except Exception as e:
        print(f"[CAMS Error] {e}")
        if "licence" in str(e).lower():
            print(">> License action required: Go to https://ads.atmosphere.copernicus.eu and click 'Accept terms'.")
        return False

if __name__ == "__main__":
    download_saudi_nwp()
