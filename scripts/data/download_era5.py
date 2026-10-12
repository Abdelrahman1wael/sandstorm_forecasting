"""
Script to download ERA5 reanalysis single levels data (weather and soil features)
for March, April, May 2021 over the East Asian domain [55N, 70E, 25N, 135E].

Prerequisites:
  1. Copernicus account registered at https://cds.climate.copernicus.eu
  2. Accepted the license terms on the dataset page:
     https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
  3. API key configured in Keys/API_Key/API.txt or ~/.cdsapirc
"""

import os
import sys
from pathlib import Path

try:
    import cdsapi
except ImportError:
    print("Error: 'cdsapi' is not installed. Run: pip install cdsapi")
    sys.exit(1)

out = Path("data/raw/era5")
out.mkdir(parents=True, exist_ok=True)

# Auto-discover API token
api_key = None
key_file = Path("Keys/API_Key/API.txt")
if key_file.exists():
    for line in key_file.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("key:"):
            api_key = line.split(":", 1)[1].strip()
        elif len(line.strip()) == 36 and "-" in line.strip():
            api_key = line.strip()

if not api_key:
    home_rc = Path.home() / ".cdsapirc"
    if home_rc.exists():
        for line in home_rc.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("key:"):
                api_key = line.split(":", 1)[1].strip()

# ERA5 meteorological and surface soil moisture variables
variables = [
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
    "10m_wind_gust_since_previous_post_processing",
    "2m_temperature",
    "boundary_layer_height",
    "surface_pressure",
    "volumetric_soil_water_layer_1",
]

cds_url = "https://cds.climate.copernicus.eu/api"
print(f"Initializing CDS API client at: {cds_url}...")
try:
    if api_key:
        c = cdsapi.Client(url=cds_url, key=api_key)
    else:
        c = cdsapi.Client(url=cds_url)
except Exception as e:
    print(f"Failed to initialize cdsapi client: {e}")
    sys.exit(1)

for month in ["03", "04", "05"]:
    target = out / f"era5_2021_{month}.nc"
    if target.exists() and target.stat().st_size > 1024 * 1024:
        print(f"File {target.name} already exists. Skipping.")
        continue

    print(f"\nRequesting ERA5 for 2021-{month} (Area: [55, 70, 25, 135], 3-hourly)...")
    try:
        c.retrieve(
            "reanalysis-era5-single-levels",
            {
                "product_type": ["reanalysis"],
                "variable": variables,
                "year": ["2021"],
                "month": [month],
                "day": [f"{d:02d}" for d in range(1, 32)],
                "time": [f"{h:02d}:00" for h in range(0, 24, 3)],
                "area": [55, 70, 25, 135],   # North, West, South, East
                "data_format": "netcdf",
            },
            str(target),
        )
        print(f"Successfully retrieved {target.name}")
    except Exception as e:
        print(f"Error retrieving 2021-{month}: {e}")
