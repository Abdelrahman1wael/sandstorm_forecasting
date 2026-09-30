"""
==============================================================================
Uncertainty Quantification Head: Non-parametric Quantile Regression (P10, P50, P90)
Pinball Quantile Loss: L_pinball(tau) = sum_i max(tau*(y_i - y_hat), (tau - 1)*(y_i - y_hat))
==============================================================================
"""

import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import HistGradientBoostingRegressor


class QuantileUncertaintyEstimator:
    """
    Quantile Regression Head estimating P10, P50, and P90 uncertainty intervals.
    Enables probabilistic emergency disaster planning rather than single point forecasts.
    """

    def __init__(self, quantiles: List[float] = [0.10, 0.50, 0.90], max_iter: int = 150, seed: int = 42):
        self.quantiles = quantiles
        self.max_iter = max_iter
        self.seed = seed
        self.models = {}

    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        """Fit a dedicated quantile gradient boosting regressor for each percentile."""
        for q in self.quantiles:
            model = HistGradientBoostingRegressor(
                loss="quantile",
                quantile=q,
                max_iter=self.max_iter,
                random_state=self.seed
            )
            model.fit(X_train, y_train)
            self.models[q] = model
        return self

    def predict_quantiles(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        """Generate P10, P50, and P90 predictions for the input instances."""
        preds = {}
        for q in self.quantiles:
            key = f"p{int(q * 100)}"
            preds[key] = np.maximum(0.0, self.models[q].predict(X))

        # Enforce non-crossing monotonicity: P10 <= P50 <= P90
        p10 = preds["p10"]
        p50 = np.maximum(p10, preds["p50"])
        p90 = np.maximum(p50, preds["p90"])

        preds["p10"] = p10
        preds["p50"] = p50
        preds["p90"] = p90
        preds["interval_width"] = p90 - p10

        return preds

    def evaluate_uncertainty(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """
        Evaluate Prediction Interval Coverage Probability (PICP)
        and Mean Prediction Interval Width (MPIW).
        """
        q_preds = self.predict_quantiles(X_test)
        p10 = q_preds["p10"]
        p90 = q_preds["p90"]

        # Interval coverage: percentage of ground truth observations within [P10, P90]
        in_interval = (y_test >= p10) & (y_test <= p90)
        picp = float(np.mean(in_interval) * 100.0)
        mpiw = float(np.mean(p90 - p10))

        # Pinball loss per quantile
        pinball_scores = {}
        for q in self.quantiles:
            key = f"p{int(q * 100)}"
            err = y_test - q_preds[key]
            loss = np.maximum(q * err, (q - 1.0) * err)
            pinball_scores[f"pinball_loss_{key}"] = float(np.mean(loss))

        return {
            "picp_coverage_percent": picp,
            "mpiw_mean_interval_width": mpiw,
            **pinball_scores
        }


# ==============================================================================
# 🌲 1. MACHINE LEARNING CONNECTION: MLUncertaintyPipeline
# Combines any Scikit-Learn/LightGBM point regressor with Quantile Uncertainty
# ==============================================================================

class MLUncertaintyPipeline:
    """
    Connects a Machine Learning point predictor (e.g. LightGBM, Random Forest, 
    or NWPBiasCorrectionEnsemble) with the Quantile Uncertainty Estimator.
    
    Workflow:
      1. Point Predictor: Learns E[y | X] (expected mean / bias-corrected forecast).
      2. Quantile Estimator: Learns P10, P50, P90 bounds via pinball loss.
      3. Unified Inference: Emits point forecast alongside calibrated uncertainty bounds.
    """

    def __init__(self, base_regressor: Any, quantiles: List[float] = [0.10, 0.50, 0.90]):
        self.base_regressor = base_regressor
        self.uncertainty_head = QuantileUncertaintyEstimator(quantiles=quantiles)
        self.is_fitted = False

    def fit(self, X_train: np.ndarray, y_train: np.ndarray, **base_fit_kwargs):
        """Fit both the ML point model and the quantile uncertainty head."""
        # 1. Fit base machine learning point regressor
        self.base_regressor.fit(X_train, y_train, **base_fit_kwargs)

        # 2. Fit quantile uncertainty estimator on training features
        self.uncertainty_head.fit(X_train, y_train)

        self.is_fitted = True
        return self

    def predict_with_uncertainty(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Unified operational output combining point prediction and uncertainty intervals.
        """
        if not self.is_fitted:
            raise RuntimeError("Pipeline must be fitted before calling predict_with_uncertainty.")

        # Point forecast from ML base model
        point_pred = self.base_regressor.predict(X)
        if isinstance(point_pred, list):
            point_pred = np.array(point_pred)

        # Quantile bounds from uncertainty head
        q_preds = self.uncertainty_head.predict_quantiles(X)

        # Categorize confidence/risk level based on relative interval width
        rel_width = q_preds["interval_width"] / np.maximum(q_preds["p50"], 1.0)
        risk_level = np.where(rel_width > 0.8, "HIGH_UNCERTAINTY",
                     np.where(rel_width > 0.4, "MODERATE_UNCERTAINTY", "LOW_UNCERTAINTY"))

        return {
            "point_prediction": point_pred,
            "p10_lower_bound": q_preds["p10"],
            "p50_median": q_preds["p50"],
            "p90_upper_bound": q_preds["p90"],
            "interval_width_mpiw": q_preds["interval_width"],
            "relative_spread": rel_width,
            "uncertainty_category": risk_level
        }


# ==============================================================================
# 🧠 2. DEEP LEARNING CONNECTION: PyTorch Quantile Loss & Neural Head
# End-to-end differentiable uncertainty quantification for Deep Neural Networks
# ==============================================================================

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


if HAS_TORCH:
    class PinballQuantileLoss(nn.Module):
        """
        Differentiable Multi-Quantile Pinball Loss for Deep Learning Models.
        Loss = sum_{tau} max(tau * (y - y_hat), (tau - 1) * (y - y_hat))
        Enables end-to-end backpropagation through CNNs, GNNs, and Transformers.
        """

        def __init__(self, quantiles: List[float] = [0.10, 0.50, 0.90]):
            super().__init__()
            self.quantiles = quantiles

        def forward(self, q_preds: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
            """
            Args:
                q_preds: [Batch, ..., num_quantiles]
                targets: [Batch, ...]
            """
            if targets.dim() < q_preds.dim():
                targets = targets.unsqueeze(-1)  # broadcast to match quantiles dimension

            losses = []
            for i, tau in enumerate(self.quantiles):
                err = targets - q_preds[..., i:i+1]
                loss_tau = torch.max(tau * err, (tau - 1.0) * err)
                losses.append(loss_tau)

            total_loss = torch.mean(torch.cat(losses, dim=-1))
            return total_loss


    class DeepQuantileRegressionHead(nn.Module):
        """
        Deep Learning Head connecting to any neural network latent embedding
        (e.g., DustMLUnifiedDeepModel, ResNet, GNN, or LSTM backbone).
        
        Key Innovation:
          Enforces strictly non-crossing quantiles: P10 <= P50 <= P90
          P50 = Softplus(Linear(h))
          P10 = clamp(P50 - Softplus(Linear_delta10(h)), min=0)
          P90 = P50 + Softplus(Linear_delta90(h))
        """

        def __init__(self, in_features: int, out_dim: int = 1):
            super().__init__()
            self.in_features = in_features
            self.out_dim = out_dim

            # Dedicated projection heads for median and offsets
            self.fc_p50 = nn.Linear(in_features, out_dim)
            self.fc_offset_p10 = nn.Linear(in_features, out_dim)
            self.fc_offset_p90 = nn.Linear(in_features, out_dim)

        def forward(self, latent_features: torch.Tensor) -> Dict[str, torch.Tensor]:
            """
            Args:
                latent_features: [Batch, InFeatures] or [Batch, Nodes, InFeatures]
            Returns:
                Dictionary containing p10, p50, p90 tensors and stacked quantiles.
            """
            # Base median estimation
            p50 = F.softplus(self.fc_p50(latent_features))

            # Non-negative offsets
            delta_10 = F.softplus(self.fc_offset_p10(latent_features))
            delta_90 = F.softplus(self.fc_offset_p90(latent_features))

            p10 = torch.clamp(p50 - delta_10, min=0.0)
            p90 = p50 + delta_90

            # Stacked tensor of shape [..., 3] for computing PinballQuantileLoss
            quantiles_stacked = torch.cat([p10, p50, p90], dim=-1)

            return {
                "p10": p10,
                "p50": p50,
                "p90": p90,
                "interval_width": p90 - p10,
                "quantiles_tensor": quantiles_stacked
            }

else:
    # Fallback placeholders when PyTorch is not yet installed in the current environment
    class PinballQuantileLoss:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required for PinballQuantileLoss. Install via `pip install torch`.")

    class DeepQuantileRegressionHead:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required for DeepQuantileRegressionHead. Install via `pip install torch`.")


# ==============================================================================
# 🌉 3. DEEP EMBEDDINGS BRIDGE FUNCTION
# Connects extracted Deep Learning latent representations to the Quantile Estimator
# ==============================================================================

def connect_dl_embeddings_to_uncertainty(
    latent_embeddings: np.ndarray,
    y_true: np.ndarray,
    quantiles: List[float] = [0.10, 0.50, 0.90]
) -> QuantileUncertaintyEstimator:
    """
    Post-hoc Quantile Uncertainty Estimation on top of Deep Learning Embeddings.
    Extracts bottleneck representations (e.g. latent_nodes from DustMLUnifiedDeepModel)
    and trains a dedicated non-parametric quantile estimator.
    """
    estimator = QuantileUncertaintyEstimator(quantiles=quantiles)
    estimator.fit(latent_embeddings, y_true)
    return estimator

