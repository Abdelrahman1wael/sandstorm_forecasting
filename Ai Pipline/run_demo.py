"""
==============================================================================
DustML: Complete Master Demonstration & Pipeline Runner
Applying Machine Learning to Medium- to Long-Term Sand and Dust Storm Forecasting
University of Science and Technology Beijing (北京科技大学)
==============================================================================
"""

import sys
import os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from data.mock_generator import DustMockDataGenerator
from training.train_ml import run_ml_training_pipeline
from training.train_dl import run_dl_training_pipeline
from inference.predictor import DustPredictor
from evaluation.benchmark import run_system_benchmark


def main():
    print("""
=================================================================================
  🌪️  DUST-ML: ADVANCED MACHINE LEARNING & DEEP LEARNING FORECASTING PLATFORM
  University of Science and Technology Beijing (北京科技大学) • Environmental Eng.
  Extended-Range (3-15 Days) Sand and Dust Storm Prediction System
=================================================================================
    """)

    # 1. Generate High-Fidelity Mock Dataset
    print("\n" + "=" * 80)
    print("📦 STEP 1: GENERATING HIGH-FIDELITY SYNTHETIC MOCK DATA")
    print("=" * 80)
    data_dir = os.path.join(current_dir, "data", "cache")
    generator = DustMockDataGenerator(seed=42)
    npz_path, meta_path = generator.save_mock_dataset(data_dir)
    print(f"✅ Mock Tensors saved: {npz_path}")
    print(f"✅ Metadata saved:     {meta_path}")

    # 2. Train Main Line A Machine Learning Pipeline
    print("\n" + "=" * 80)
    print("🌲 STEP 2: TRAINING MAIN LINE A (TREE ENSEMBLE NWP BIAS CORRECTION)")
    print("=" * 80)
    ml_results = run_ml_training_pipeline(
        lead_time_hours=72,
        save_dir=os.path.join(current_dir, "models", "checkpoints", "line_a"),
        verbose=True
    )

    # 3. Train Main Line B Deep Learning Pipeline (PINN + ST-GNN + AI-GAMFS)
    print("\n" + "=" * 80)
    print("🧠 STEP 3: TRAINING MAIN LINE B (PHYSICS-INFORMED DEEP LEARNING)")
    print("=" * 80)
    dl_results = run_dl_training_pipeline(
        epochs=8,
        batch_size=16,
        lr=1e-3,
        save_dir=os.path.join(current_dir, "models", "checkpoints", "line_b"),
        device="cpu",
        verbose=True
    )

    # 4. Run Unified Predictor on Key Stations
    print("\n" + "=" * 80)
    print("🎯 STEP 4: OPERATIONAL INFERENCE ON KEY BENCHMARK STATIONS")
    print("=" * 80)
    predictor = DustPredictor(checkpoints_dir=os.path.join(current_dir, "models", "checkpoints"))

    test_cases = [
        {
            "name": "Minqin Station (民勤, 52681) • Hexi Corridor Bottleneck",
            "code": "52681",
            "u10": 17.2,
            "u_star": 0.88,
            "sm": 0.031,
            "nwp": 1420.0,
            "aod": 2.1
        },
        {
            "name": "Beijing Mega-Station (北京奥体, 54511) • Downstream Receptor",
            "code": "54511",
            "u10": 9.5,
            "u_star": 0.42,
            "sm": 0.082,
            "nwp": 340.0,
            "aod": 1.2
        },
        {
            "name": "Chengdu Station (成都温江, 56187) • 120h Remote Incursion",
            "code": "56187",
            "u10": 4.1,
            "u_star": 0.18,
            "sm": 0.145,
            "nwp": 85.0,
            "aod": 0.65
        }
    ]

    for tc in test_cases:
        pred = predictor.predict_station(
            station_code=tc["code"],
            current_wind_u10=tc["u10"],
            current_u_star=tc["u_star"],
            soil_moisture=tc["sm"],
            nwp_raw_pm10=tc["nwp"],
            aod=tc["aod"]
        )

        p_diag = pred["physics_diagnostics"]
        print(f"\n📍 {tc['name']}")
        print(f"   • Aerodynamic Status:  u* = {p_diag['u_star']} m/s (Threshold u*t = {p_diag['u_star_threshold']} m/s)")
        print(f"   • Active Saltation:    {'🔥 ACTIVE (Severe Local Dust Lift)' if p_diag['saltation_active'] else '❄️ INACTIVE (Advection only)'}")
        print(f"   • PINN Mass Residual:  {p_diag['pinn_mass_residual']}")
        print(f"   • Alert Advisory:      {pred['alert']['level']}")
        print("   • Multi-Lead Forecast Projections:")
        print(f"     {'Lead Time':<15} | {'P10 (Min)':<10} | {'P50 (Median)':<12} | {'P90 (Max)':<10} | {'Threat Score':<12}")
        print("     " + "-" * 65)
        for f in pred["forecasts"]:
            print(f"     {f['lead_label']:<15} | {f['pm10_p10']:<10.1f} | {f['pm10_p50']:<12.1f} | {f['pm10_p90']:<10.1f} | {f['threat_score']:<12.3f}")

    # 5. Run Cross-Model Benchmark vs ECMWF NWP
    print("\n" + "=" * 80)
    print("📈 STEP 5: MODEL BENCHMARKING VS ECMWF IFS NUMERICAL ENSEMBLE")
    print("=" * 80)
    run_system_benchmark(
        output_dir=os.path.join(current_dir, "evaluation", "reports"),
        verbose=True
    )

    print("""
=================================================================================
🎉 COMPLETE PIPELINE EXECUTION SUCCESSFUL!
All Machine Learning, Deep Learning, and PINN components are fully functional.
To launch the REST API server:
  uvicorn api.server:app --reload --port 8000
=================================================================================
    """)


if __name__ == "__main__":
    main()
