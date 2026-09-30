"""
==============================================================================
Training Pipeline: Main Line A Machine Learning Models
Ensemble NWP Bias Correction + Quantile Uncertainty Estimator + Hazard Classifier
==============================================================================
"""

import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
import pickle

def save_artifact(obj, path):
    if HAS_JOBLIB:
        joblib.dump(obj, path)
    else:
        with open(path, "wb") as f:
            pickle.dump(obj, f)
try:
    from ..data.dataset import TabularDustDataset
    from ..models.machine_learning.line_a_ensemble import NWPBiasCorrectionEnsemble
    from ..models.machine_learning.uncertainty_head import QuantileUncertaintyEstimator
    from ..models.machine_learning.hazard_classifier import CostSensitiveHazardClassifier
except (ImportError, ValueError):
    from data.dataset import TabularDustDataset
    from models.machine_learning.line_a_ensemble import NWPBiasCorrectionEnsemble
    from models.machine_learning.uncertainty_head import QuantileUncertaintyEstimator
    from models.machine_learning.hazard_classifier import CostSensitiveHazardClassifier


def run_ml_training_pipeline(
    lead_time_hours: int = 72,
    save_dir: str = "models/checkpoints/line_a",
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Executes end-to-end training and evaluation of Main Line A.
    """
    if verbose:
        print("=" * 75)
        print(f"🚀 [Main Line A] Starting Machine Learning Training for {lead_time_hours}h Forecast...")
        print("=" * 75)

    os.makedirs(save_dir, exist_ok=True)
    dataset = TabularDustDataset()
    data = dataset.get_tabular_data(lead_time_hours=lead_time_hours)

    X_train, y_train = data["X_train"], data["y_train"]
    X_val, y_val = data["X_val"], data["y_val"]
    X_test, y_test = data["X_test"], data["y_test"]
    y_nwp_test = data["y_nwp_test"]
    hazard_train = data["hazard_train"]
    hazard_test = data["hazard_test"]
    feature_names = data["feature_names"]

    # 1. Train NWP Bias Correction Tree Ensemble
    if verbose:
        print("\n🔹 Step 1/3: Training NWP Bias Correction Tree Ensemble...")
    ensemble = NWPBiasCorrectionEnsemble(model_type="lightgbm", n_estimators=150)
    # Using nwp_pm10 from features (index 7 is nwp_pm10 in base features)
    y_nwp_train = X_train[:, 7]
    y_nwp_val = X_val[:, 7]
    ensemble.fit(X_train, y_train, y_nwp_train, feature_names=feature_names, X_val=X_val, y_val=y_val, y_nwp_val=y_nwp_val)

    eval_ensemble = ensemble.evaluate(X_test, y_test, y_nwp_test)
    top_features = ensemble.get_feature_importances()[:5]

    if verbose:
        print(f"   -> Raw NWP Baseline RMSE:       {eval_ensemble['raw_nwp_rmse']:.2f} μg/m³")
        print(f"   -> Corrected DustML ML RMSE:    {eval_ensemble['corrected_ml_rmse']:.2f} μg/m³")
        print(f"   -> Error Reduction:             {eval_ensemble['rmse_reduction_percent']:.2f}%")
        print("   -> Top 3 Governing Features:")
        for feat in top_features[:3]:
            print(f"      • {feat['feature']}: {feat['importance_pct']}%")

    # 2. Train Quantile Uncertainty Estimator
    if verbose:
        print("\n🔹 Step 2/3: Training Quantile Uncertainty Head (P10, P50, P90)...")
    uncertainty = QuantileUncertaintyEstimator(quantiles=[0.10, 0.50, 0.90], max_iter=120)
    uncertainty.fit(X_train, y_train)
    eval_uncertainty = uncertainty.evaluate_uncertainty(X_test, y_test)

    if verbose:
        print(f"   -> Prediction Interval Coverage: {eval_uncertainty['picp_coverage_percent']:.2f}% (Expected ~80%)")
        print(f"   -> Mean Prediction Interval Width: {eval_uncertainty['mpiw_mean_interval_width']:.2f} μg/m³")

    # 3. Train Cost-Sensitive Sandstorm Hazard Classifier
    if verbose:
        print("\n🔹 Step 3/3: Training Cost-Sensitive Hazard Severity Classifier...")
    hazard_clf = CostSensitiveHazardClassifier(n_classes=5, max_iter=120)
    hazard_clf.fit(X_train, hazard_train)
    eval_hazard = hazard_clf.evaluate(X_test, hazard_test)

    if verbose:
        print(f"   -> Sandstorm Threat Score (TS):  {eval_hazard['threat_score_ts']:.4f}")
        print(f"   -> Probability of Detection (POD): {eval_hazard['probability_of_detection_pod']:.4f}")
        print(f"   -> False Alarm Rate (FAR):         {eval_hazard['false_alarm_rate_far']:.4f}")

    # 4. Save Trained Checkpoints
    ensemble_path = os.path.join(save_dir, f"nwp_bias_ensemble_{lead_time_hours}h.joblib")
    uncertainty_path = os.path.join(save_dir, f"quantile_uncertainty_{lead_time_hours}h.joblib")
    hazard_path = os.path.join(save_dir, f"hazard_classifier_{lead_time_hours}h.joblib")

    save_artifact(ensemble, ensemble_path)
    save_artifact(uncertainty, uncertainty_path)
    save_artifact(hazard_clf, hazard_path)

    if verbose:
        print(f"\n💾 Main Line A Checkpoints successfully saved to '{save_dir}'.")

    return {
        "lead_time_hours": lead_time_hours,
        "ensemble_metrics": eval_ensemble,
        "uncertainty_metrics": eval_uncertainty,
        "hazard_metrics": eval_hazard,
        "top_features": top_features,
        "checkpoints": {
            "ensemble": ensemble_path,
            "uncertainty": uncertainty_path,
            "hazard": hazard_path
        }
    }


if __name__ == "__main__":
    run_ml_training_pipeline(lead_time_hours=72)
