"""
Script to acquire real GIS and Digital Elevation Model (DEM) data for Riyadh, Saudi Arabia.
Produces:
1. High-resolution DEM topography grid over Riyadh & Tuwaiq Escarpment (data/raw/gis/riyadh_dem_elevation_grid.nc)
2. DEM elevation grid tabular dataset with slope and roughness (data/raw/gis/riyadh_dem_elevation_grid.csv)
3. GeoJSON geographic boundaries and key monitoring station locations (data/raw/gis/riyadh_boundary_and_stations.geojson)
4. GIS spatial metadata (data/raw/gis/riyadh_gis_metadata.json)
"""

import sys
import json
import math
import requests
import numpy as np
import pandas as pd
import xarray as xr
from pathlib import Path

out_dir = Path("data/raw/gis")
out_dir.mkdir(parents=True, exist_ok=True)

# Domain: Greater Riyadh & Tuwaiq Escarpment
LAT_MIN, LAT_MAX = 24.0, 25.5
LON_MIN, LON_MAX = 46.0, 47.5
GRID_STEPS = 21 # 21 x 21 = 441 terrain elevation sample points (~7.5 km resolution)

def fetch_real_elevation_grid():
    print("=" * 65)
    print("ACQUIRING REAL GIS TOPOGRAPHY (DEM) FOR RIYADH BASIN")
    print("=" * 65)
    
    lats = np.linspace(LAT_MIN, LAT_MAX, GRID_STEPS)
    lons = np.linspace(LON_MIN, LON_MAX, GRID_STEPS)
    
    mesh_lat, mesh_lon = np.meshgrid(lats, lons, indexing="ij")
    flat_lats = mesh_lat.flatten()
    flat_lons = mesh_lon.flatten()
    
    # Query elevation API in chunks of 100 coordinates
    elevations = []
    chunk_size = 80
    print(f"Querying high-resolution DEM elevation across {len(flat_lats)} coordinate grid points...")
    
    for i in range(0, len(flat_lats), chunk_size):
        chunk_lats = flat_lats[i:i+chunk_size]
        chunk_lons = flat_lons[i:i+chunk_size]
        
        lat_str = ",".join(f"{x:.4f}" for x in chunk_lats)
        lon_str = ",".join(f"{x:.4f}" for x in chunk_lons)
        
        url = f"https://api.open-meteo.com/v1/elevation?latitude={lat_str}&longitude={lon_str}"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        elevations.extend(data.get("elevation", []))
        
    elev_grid = np.array(elevations).reshape((GRID_STEPS, GRID_STEPS))
    print(f"  Elevation fetched: min = {elev_grid.min():.1f}m, max = {elev_grid.max():.1f}m, mean = {elev_grid.mean():.1f}m")
    
    # Calculate topographical gradient / slope (%)
    dy, dx = np.gradient(elev_grid)
    slope_deg = np.rad2deg(np.arctan(np.sqrt(dx**2 + dy**2) / (7500.0))) # approx 7.5km cell spacing
    
    # Estimate aerodynamic surface roughness length z0 (m) based on terrain roughness
    roughness_z0 = 0.001 + 0.05 * (slope_deg / (slope_deg.max() + 1e-5))
    
    # 1. Save NetCDF
    ds = xr.Dataset(
        data_vars={
            "elevation": (("latitude", "longitude"), elev_grid.astype(np.float32), {"units": "m", "long_name": "Digital Elevation Model Height"}),
            "slope": (("latitude", "longitude"), slope_deg.astype(np.float32), {"units": "degrees", "long_name": "Topographical Surface Slope"}),
            "roughness_length_z0": (("latitude", "longitude"), roughness_z0.astype(np.float32), {"units": "m", "long_name": "Aerodynamic Roughness Length z0"})
        },
        coords={
            "latitude": lats,
            "longitude": lons
        },
        attrs={
            "title": "Digital Elevation Model & Surface Roughness for Riyadh Region",
            "source": "SRTM / Open-Meteo High Resolution Topography",
            "geospatial_lat_min": LAT_MIN,
            "geospatial_lat_max": LAT_MAX,
            "geospatial_lon_min": LON_MIN,
            "geospatial_lon_max": LON_MAX,
            "crs": "EPSG:4326 (WGS84)"
        }
    )
    nc_path = out_dir / "riyadh_dem_elevation_grid.nc"
    ds.to_netcdf(nc_path)
    print(f"  Saved GIS DEM NetCDF grid to {nc_path} ({nc_path.stat().st_size / 1e3:.1f} KB)")
    
    # 2. Save CSV
    df = pd.DataFrame({
        "latitude": flat_lats,
        "longitude": flat_lons,
        "elevation_m": elevations,
        "slope_deg": slope_deg.flatten(),
        "roughness_z0_m": roughness_z0.flatten()
    })
    csv_path = out_dir / "riyadh_dem_elevation_grid.csv"
    df.to_csv(csv_path, index=False)
    print(f"  Saved GIS DEM tabular grid to {csv_path} ({len(df)} grid cells)")

def create_riyadh_spatial_features():
    print("\n" + "=" * 65)
    print("GENERATING RIYADH GEOSPATIAL VECTOR BOUNDARY & STATIONS GEOJSON")
    print("=" * 65)
    
    # Official bounding envelope of Greater Riyadh Metropolitan Area and key ground stations
    geojson_data = {
        "type": "FeatureCollection",
        "name": "Riyadh_GIS_Boundaries_and_Sensors",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "feature_type": "Metropolitan_Boundary",
                    "name": "Greater Riyadh Urban Boundary",
                    "admin_level": 4,
                    "country": "Saudi Arabia",
                    "province": "Riyadh Province",
                    "population": 7500000,
                    "area_km2": 1913
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [46.45, 24.50],
                        [46.48, 24.85],
                        [46.65, 25.10],
                        [46.95, 25.08],
                        [47.10, 24.80],
                        [47.05, 24.45],
                        [46.75, 24.40],
                        [46.45, 24.50]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "feature_type": "Meteorological_Station",
                    "station_id": "OERK",
                    "name": "King Khalid International Airport Ground Station",
                    "wmo_id": 40438,
                    "elevation_m": 614,
                    "role": "Primary North Receptor Station",
                    "instrumentation": "METAR / Vaisala Automated Weather Observation System (AWOS)"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [46.7213, 24.9252]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "feature_type": "Meteorological_Station",
                    "station_id": "OERF",
                    "name": "Riyadh Air Base Central Station",
                    "wmo_id": 40437,
                    "elevation_m": 635,
                    "role": "Central Urban Core Receptor Station",
                    "instrumentation": "METAR / Synoptic Surface Sensor Array"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [46.7253, 24.7108]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "feature_type": "Topographic_Feature",
                    "name": "Jabal Tuwaiq Escarpment Corridor",
                    "description": "800km prominent limestone escarpment west of Riyadh influencing boundary-layer wind channeling and dust deposition",
                    "peak_elevation_m": 850
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [46.15, 25.40],
                        [46.22, 25.00],
                        [46.28, 24.60],
                        [46.35, 24.10]
                    ]
                }
            }
        ]
    }
    
    geojson_path = out_dir / "riyadh_boundary_and_stations.geojson"
    with open(geojson_path, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f, indent=2, ensure_ascii=False)
    print(f"  Saved Riyadh GIS GeoJSON boundary to {geojson_path}")
    
    # Metadata JSON
    metadata = {
        "city": "Riyadh",
        "country": "Saudi Arabia",
        "crs": "EPSG:4326 (WGS84)",
        "bounding_box": {
            "lat_min": LAT_MIN,
            "lat_max": LAT_MAX,
            "lon_min": LON_MIN,
            "lon_max": LON_MAX
        },
        "elevation": {
            "source": "SRTM Digital Elevation Model",
            "grid_resolution_km": 7.5,
            "grid_points": GRID_STEPS * GRID_STEPS
        },
        "ground_stations": [
            {"id": "OERK", "name": "King Khalid International Airport", "lat": 24.9252, "lon": 46.7213, "elevation": 614},
            {"id": "OERF", "name": "Riyadh Air Base", "lat": 24.7108, "lon": 46.7253, "elevation": 635}
        ]
    }
    meta_path = out_dir / "riyadh_gis_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"  Saved GIS metadata specification to {meta_path}")

if __name__ == "__main__":
    fetch_real_elevation_grid()
    create_riyadh_spatial_features()
