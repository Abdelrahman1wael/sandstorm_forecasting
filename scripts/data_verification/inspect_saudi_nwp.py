import xarray as xr
from pathlib import Path

target = Path("data/raw/nwp/cams_forecast_saudi_arabia.nc")
if not target.exists():
    print(f"File {target} does not exist!")
    exit(1)

print(f"File exists: {target} ({target.stat().st_size / 1e6:.2f} MB)")
ds = xr.open_dataset(target)
print("=== NetCDF Dataset Summary ===")
print("Dimensions:", dict(ds.dims))
print("Coordinates:", list(ds.coords.keys()))
print("Data Variables:", list(ds.data_vars.keys()))
for var in ds.data_vars:
    da = ds[var]
    print(f"  - {var}: shape={da.shape}, min={float(da.min()):.4e}, max={float(da.max()):.4e}, units={da.attrs.get('units', 'N/A')}")
print("Latitude range:", float(ds.latitude.min()), "to", float(ds.latitude.max()))
print("Longitude range:", float(ds.longitude.min()), "to", float(ds.longitude.max()))
print("Lead times:", ds.leadtime_hour.values if "leadtime_hour" in ds else "N/A")
ds.close()
