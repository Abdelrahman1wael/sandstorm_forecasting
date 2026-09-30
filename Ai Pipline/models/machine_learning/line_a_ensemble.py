"""
==============================================================================
Main Line A: NWP Statistical Bias Correction & Tree-Ensemble Predictor
Formulation: y_hat = y_NWP + sum_{m=1}^M alpha_m * f_m(x; Theta_m)
==============================================================================
"""

import numpy as np
from typing import Dict, Any, Optional, List
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False


class NWPBiasCorrectionEnsemble:
    """
    Main Line A: Gradient Boosted Decision Forest Ensemble to correct
    systematic operational errors in ECMWF IFS and CMA-GFS NWP models.
    """

    def __init__(self, model_type: str = "lightgbm", n_estimators: int = 150, learning_rate: float = 0.05, seed: int = 42):
        self.model_type = model_type
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.seed = seed
        self.model = None
        self.feature_names = []
        self.is_fitted = False

    def fit(self, X_train: np.ndarray, y_train: np.ndarray, y_nwp_train: np.ndarray,
            feature_names: Optional[List[str]] = None,
            X_val: Optional[np.ndarray] = None, y_val: Optional[np.ndarray] = None, y_nwp_val: Optional[np.ndarray] = None):
        """
        Train the ensemble to learn the residual bias: residual = y_true - y_NWP
        """
        self.feature_names = feature_names or [f"feat_{i}" for i in range(X_train.shape[1])]
        target_residual = y_train - y_nwp_train

        val_set = None
        if X_val is not None and y_val is not None and y_nwp_val is not None:
            val_residual = y_val - y_nwp_val
            val_set = (X_val, val_residual)

        if self.model_type == "lightgbm" and HAS_LIGHTGBM:
            self.model = lgb.LGBMRegressor(
                n_estimators=self.n_estimators,
                learning_rate=self.learning_rate,
                max_depth=6,
                num_leaves=31,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=self.seed,
                verbose=-1
            )
            eval_set = [val_set] if val_set else None
            self.model.fit(X_train, target_residual, eval_set=eval_set)
        else:
            # High-performance scikit-learn fallback
            self.model = HistGradientBoostingRegressor(
                max_iter=self.n_estimators,
                learning_rate=self.learning_rate,
                max_depth=6,
                random_state=self.seed
            )
            self.model.fit(X_train, target_residual)

        self.is_fitted = True
        return self

    def predict(self, X: np.ndarray, y_nwp: np.ndarray) -> np.ndarray:
        """
        Correct NWP forecast by adding the predicted systematic bias:
        y_corrected = y_NWP + predicted_residual
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be trained with .fit() before predicting.")
        pred_residual = self.model.predict(X)
        corrected = y_nwp + pred_residual
        # Dust concentration cannot be negative
        return np.maximum(0.0, corrected)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray, y_nwp_test: np.ndarray) -> Dict[str, float]:
        """
        Benchmark corrected forecasts against raw NWP predictions.
        """
        y_pred = self.predict(X_test, y_nwp_test)

        nwp_rmse = float(root_mean_squared_error(y_test, y_nwp_test))
        nwp_mae = float(mean_absolute_error(y_test, y_nwp_test))
        nwp_r2 = float(r2_score(y_test, y_nwp_test))

        ml_rmse = float(root_mean_squared_error(y_test, y_pred))
        ml_mae = float(mean_absolute_error(y_test, y_pred))
        ml_r2 = float(r2_score(y_test, y_pred))

        rmse_reduction = ((nwp_rmse - ml_rmse) / max(nwp_rmse, 1e-6)) * 100.0
        mae_reduction = ((nwp_mae - ml_mae) / max(nwp_mae, 1e-6)) * 100.0

        return {
            "raw_nwp_rmse": nwp_rmse,
            "raw_nwp_mae": nwp_mae,
            "raw_nwp_r2": nwp_r2,
            "corrected_ml_rmse": ml_rmse,
            "corrected_ml_mae": ml_mae,
            "corrected_ml_r2": ml_r2,
            "rmse_reduction_percent": rmse_reduction,
            "mae_reduction_percent": mae_reduction,
        }

    def get_feature_importances(self) -> List[Dict[str, Any]]:
        """Extract relative feature importance weights."""
        if not self.is_fitted:
            return []

        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
        else:
            # Fallback uniform proxy
            importances = np.ones(len(self.feature_names)) / len(self.feature_names)

        total = np.sum(importances)
        normalized = importances / max(total, 1e-6)

        results = []
        for name, weight in zip(self.feature_names, normalized):
            results.append({
                "feature": name,
                "importance_pct": round(float(weight * 100.0), 2)
            })

        results.sort(key=lambda x: x["importance_pct"], reverse=True)
        return results
