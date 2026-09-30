"""
==============================================================================
DustML Operational Forecasting API Microservice
Built with FastAPI, Pydantic, and Asynchronous ML Inference
==============================================================================
"""

import os
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from ..data.mock_generator import CORRIDOR_STATIONS, LEAD_TIMES, LEAD_TIME_LABELS, HAZARD_CLASSES, DustMockDataGenerator
    from ..inference.predictor import DustPredictor
    from ..evaluation.benchmark import run_system_benchmark
except (ImportError, ValueError):
    from data.mock_generator import CORRIDOR_STATIONS, LEAD_TIMES, LEAD_TIME_LABELS, HAZARD_CLASSES, DustMockDataGenerator
    from inference.predictor import DustPredictor
    from evaluation.benchmark import run_system_benchmark

app = FastAPI(
    title="DustML Sand & Dust Storm Operational AI API",
    description="Extended-Range (3-15 Days) Multi-Modal Sand and Dust Storm Forecasting Platform. USTB Environmental Engineering.",
    version="2.4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
predictor = DustPredictor()
generator = DustMockDataGenerator(seed=42)


class StationForecastRequest(BaseModel):
    station_code: str = Field(default="52681", description="WMO Station Code (e.g., 52681 for Minqin)")
    wind_u10: float = Field(default=16.8, description="10m Wind Speed (m/s)")
    u_star: float = Field(default=0.88, description="Surface Friction Velocity (m/s)")
    soil_moisture: float = Field(default=0.031, description="Volumetric Soil Moisture 0-7cm (m3/m3)")
    nwp_raw_pm10: float = Field(default=1250.0, description="Raw NWP Uncorrected PM10 (μg/m³)")
    aod: float = Field(default=1.45, description="Aerosol Optical Depth at 550nm")
    temp_k: float = Field(default=287.35, description="2m Air Temperature (K)")
    blh: float = Field(default=1400.0, description="Boundary Layer Height (m)")
    vis_km: float = Field(default=0.9, description="Horizontal Visibility (km)")


class PhysicsSimulateRequest(BaseModel):
    friction_velocity_u_star: float = Field(default=0.75, description="Friction Velocity u* (m/s)")
    threshold_u_star_t: float = Field(default=0.42, description="Critical Threshold u*t (m/s)")
    air_density_rho: float = Field(default=1.225, description="Air Density (kg/m3)")
    gravitational_accel_g: float = Field(default=9.81, description="Gravity (m/s2)")
    saltation_constant_c: float = Field(default=0.25, description="Owen's Saltation Parameter C")


@app.get("/")
def root():
    return {
        "status": "operational",
        "system": "DustML-NeuroForecast v2.4 (Coupled AI-GAMFS & PINN Core)",
        "institution": "University of Science and Technology Beijing (北京科技大学)",
        "endpoints": [
            "/api/stations",
            "/api/forecast/station",
            "/api/physics/simulate",
            "/api/corridors",
            "/api/benchmark"
        ],
        "lead_times": LEAD_TIME_LABELS
    }


@app.get("/api/stations")
def get_stations():
    """Retrieve metadata and physical threshold parameters for all 14 corridor stations."""
    return {
        "count": len(CORRIDOR_STATIONS),
        "stations": CORRIDOR_STATIONS
    }


@app.post("/api/forecast/station")
def forecast_station(req: StationForecastRequest):
    """
    Run machine learning and deep learning forward inference for a target station.
    Returns P10, P50, P90 quantile intervals, hazard alert, and SHAP attributions.
    """
    try:
        result = predictor.predict_station(
            station_code=req.station_code,
            current_wind_u10=req.wind_u10,
            current_u_star=req.u_star,
            soil_moisture=req.soil_moisture,
            nwp_raw_pm10=req.nwp_raw_pm10,
            aod=req.aod,
            temp_k=req.temp_k,
            blh=req.blh,
            vis_km=req.vis_km
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/physics/simulate")
def simulate_physics(req: PhysicsSimulateRequest):
    """
    Interactive PINN Aerodynamic Saltation Simulator.
    Implements Owen's Horizontal Sand Flux formula:
    F_salt = C * (rho / g) * u_*^3 * (1 - u_*t^2 / u_*^2) * I(u_* > u_*t)
    """
    u = req.friction_velocity_u_star
    ut = req.threshold_u_star_t
    is_active = u > ut

    if is_active:
        ratio = (ut / max(u, 1e-5)) ** 2
        excess = max(0.0, 1.0 - ratio)
        flux_kg = req.saltation_constant_c * (req.air_density_rho / req.gravitational_accel_g) * (u ** 3) * excess
        flux_mg = flux_kg * 1e6
        pinn_loss_penalty = 0.0
    else:
        flux_kg = 0.0
        flux_mg = 0.0
        # Below threshold: penalize any predicted emission as a PINN violation
        pinn_loss_penalty = round(0.5 * (ut - u) ** 2, 5)

    return {
        "inputs": {
            "u_star": u,
            "u_star_threshold": ut,
            "air_density": req.air_density_rho,
            "gravity": req.gravitational_accel_g
        },
        "saltation_active": is_active,
        "horizontal_sand_flux_mg_per_m_s": round(flux_mg, 2),
        "horizontal_sand_flux_kg_per_m_s": round(flux_kg, 6),
        "pinn_boundary_loss_penalty": pinn_loss_penalty,
        "formula": "F_salt = C * (rho / g) * u_*^3 * (1 - u_*t^2 / u_*^2) if u_* > u_*t else 0"
    }


@app.get("/api/corridors")
def get_corridors():
    """Retrieve ST-GNN East Asian dust advection corridor network topology."""
    return {
        "corridor_edges": generator.corridor_edges,
        "adjacency_shape": generator.adj_matrix.shape,
        "total_nodes": len(CORRIDOR_STATIONS)
    }


@app.get("/api/benchmark")
def get_benchmark():
    """Retrieve benchmark verification scores against ECMWF IFS NWP."""
    res = run_system_benchmark(verbose=False)
    return res


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Main project.api.server:app", host="127.0.0.1", port=8000, reload=True)
