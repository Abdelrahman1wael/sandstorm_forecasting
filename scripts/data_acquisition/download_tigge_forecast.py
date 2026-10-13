"""
Script template for TIGGE ECMWF control forecast (Days 6 to 15 / 144h-360h)
from ECMWF Web API (apps.ecmwf.int/datasets/data/tigge).

Variables:
  - 10m wind (10u, 10v)
  - 2m temperature (2t)
  - Surface pressure (sp)
  - Boundary layer height / total precipitation (if available in control run)

Requires:
  - ECMWF account registration at apps.ecmwf.int
  - ecmwfapi client and ~/.ecmwfapirc
"""

import sys
from pathlib import Path

out = Path("data/raw/nwp")
out.mkdir(parents=True, exist_ok=True)

print("TIGGE ECMWF Control Forecast Download Script")
print("Access link: https://apps.ecmwf.int/datasets/data/tigge/")
print("Target: ECMWF operational control forecast out to 360h for March-May 2021.")
