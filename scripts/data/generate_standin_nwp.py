"""
Generate stand-in NWP NetCDF forecast datasets in data/raw/nwp/.
As specified in thesis guidelines:
"If you cannot get CAMS today, you can build and test the whole data pipeline
using stand-in data. Do not report model results from this stand-in as forecast skill."
"""

from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr

out_dir = Path("data/raw/nwp")
out_dir.mkdir(parents=True, exist_ok=True)

def generate_nwp_month(month="03", days=10):
    target = out_dir / f"cams_forecast_2021_{month}_standin.nc"
    if target.exists():
        print(f"[Stand-in NWP] {target.name} already exists.")
        return

    print(f"[Stand-in NWP] Generating compliant NWP NetCDF for 2021-{month}...")
    lats = np.arange(25.0, 55.5, 0.5)
    lons = np.arange(70.0, 135.5, 0.5)
    dates = pd.date_range(f"2021-{month}-01", periods=days*2, freq="12h")
    leads = np.arange(72, 121, 6) # 72, 78, 84, ..., 120h

    shape = (len(dates), len(leads), len(lats), len(lons))
    np.random.seed(int(month) * 42)

    # Base spatial dust corridor gradient (high over Taklamakan/Gobi ~38-42N, 75-105E)
    lat_grid, lon_grid = np.meshgrid(lats, lons, indexing="ij")
    source_mask = np.exp(-(((lat_grid - 40.0)/4.0)**2 + ((lon_grid - 95.0)/12.0)**2))

    # PM10 (kg/m3) typical values: 20e-9 to 800e-9 kg/m3 (20 to 800 ug/m3)
    pm10 = np.zeros(shape, dtype=np.float32)
    daod = np.zeros(shape, dtype=np.float32)
    u10 = np.random.normal(5.0, 4.0, size=shape).astype(np.float32)
    v10 = np.random.normal(-2.0, 3.0, size=shape).astype(np.float32)

    for t_idx in range(len(dates)):
        synoptic_pulse = 1.0 + 0.8 * np.sin(t_idx / 3.0)
        for l_idx, lead in enumerate(leads):
            # Lead time dispersion
            decay = np.exp(-lead / 200.0)
            pm10_field = (source_mask * synoptic_pulse * decay * 350.0 + 
                          np.random.gamma(2.0, 15.0, size=(len(lats), len(lons)))) * 1e-9
            daod_field = (source_mask * synoptic_pulse * decay * 0.8 + 
                          np.random.exponential(0.05, size=(len(lats), len(lons))))
            pm10[t_idx, l_idx] = np.clip(pm10_field, 5e-9, 2000e-9)
            daod[t_idx, l_idx] = np.clip(daod_field, 0.01, 3.5)

    ds = xr.Dataset(
        data_vars={
            "particulate_matter_10um": (["time", "leadtime_hour", "latitude", "longitude"], pm10,
                                       {"units": "kg m**-3", "long_name": "Particulate matter d < 10 um"}),
            "dust_aerosol_optical_depth_550nm": (["time", "leadtime_hour", "latitude", "longitude"], daod,
                                                {"units": "~", "long_name": "Dust Aerosol Optical Depth 550nm"}),
            "10m_u_component_of_wind": (["time", "leadtime_hour", "latitude", "longitude"], u10,
                                       {"units": "m s**-1", "long_name": "10 metre U wind component"}),
            "10m_v_component_of_wind": (["time", "leadtime_hour", "latitude", "longitude"], v10,
                                       {"units": "m s**-1", "long_name": "10 metre V wind component"}),
        },
        coords={
            "time": dates,
            "leadtime_hour": leads,
            "latitude": lats,
            "longitude": lons,
        },
        attrs={
            "title": "Stand-in CAMS NWP Atmospheric Composition Forecast",
            "conventions": "CF-1.7",
            "note": "Pipeline development stand-in dataset; replace with operational ADS archive."
        }
    )

    ds.to_netcdf(str(target))
    print(f"[Stand-in NWP] Successfully created {target.name} ({target.stat().st_size / 1e6:.2f} MB)")

if __name__ == "__main__":
    for m in ["03", "04", "05"]:
        generate_nwp_month(m, days=15)
