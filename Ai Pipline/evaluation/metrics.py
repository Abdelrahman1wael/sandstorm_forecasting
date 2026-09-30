"""
==============================================================================
Meteorological & Machine Learning Verification Metrics
Formulas for Threat Score (TS/CSI), POD, FAR, RMSE, and Physics Compliance
==============================================================================
"""

import numpy as np
from typing import Dict, Any


def compute_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate RMSE, MAE, R², and Mean Bias Error."""
    err = y_pred - y_true
    rmse = float(np.sqrt(np.mean(err ** 2)))
    mae = float(np.mean(np.abs(err)))
    mbe = float(np.mean(err))

    ss_res = np.sum(err ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = float(1.0 - (ss_res / max(ss_tot, 1e-6)))

    return {
        "rmse": round(rmse, 2),
        "mae": round(mae, 2),
        "mbe": round(mbe, 2),
        "r2": round(r2, 4)
    }


def compute_meteorological_contingency(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    threshold_ugm3: float = 500.0
) -> Dict[str, float]:
    """
    Standard CMA / WMO 2x2 Contingency Table for Sand and Dust Storms:
      - Hits (NA): Observed YES, Forecast YES
      - False Alarms (NB): Observed NO, Forecast YES
      - Misses (NC): Observed YES, Forecast NO
      - Correct Negatives (ND): Observed NO, Forecast NO
    Metrics:
      - Threat Score (TS / CSI) = NA / (NA + NB + NC)
      - Probability of Detection (POD) = NA / (NA + NC)
      - False Alarm Rate (FAR) = NB / (NA + NB)
      - Bias Score (BIAS) = (NA + NB) / (NA + NC)
    """
    obs_event = (y_true >= threshold_ugm3)
    pred_event = (y_pred >= threshold_ugm3)

    na = int(np.sum(obs_event & pred_event))
    nb = int(np.sum(~obs_event & pred_event))
    nc = int(np.sum(obs_event & ~pred_event))
    nd = int(np.sum(~obs_event & ~pred_event))

    ts = float(na / (na + nb + nc)) if (na + nb + nc) > 0 else 0.0
    pod = float(na / (na + nc)) if (na + nc) > 0 else 0.0
    far = float(nb / (na + nb)) if (na + nb) > 0 else 0.0
    bias = float((na + nb) / (na + nc)) if (na + nc) > 0 else 0.0

    return {
        "threshold_ugm3": threshold_ugm3,
        "threat_score_ts": round(ts, 4),
        "probability_of_detection_pod": round(pod, 4),
        "false_alarm_rate_far": round(far, 4),
        "frequency_bias_score": round(bias, 4),
        "counts": {"hits": na, "false_alarms": nb, "misses": nc, "correct_negatives": nd}
    }


def compute_quantile_coverage(y_true: np.ndarray, p10: np.ndarray, p90: np.ndarray) -> Dict[str, float]:
    """
    Prediction Interval Coverage Probability (PICP)
    and Mean Prediction Interval Width (MPIW).
    """
    covered = (y_true >= p10) & (y_true <= p90)
    picp = float(np.mean(covered) * 100.0)
    mpiw = float(np.mean(p90 - p10))
    return {
        "picp_percent": round(picp, 2),
        "mpiw_ugm3": round(mpiw, 2)
    }


def compute_physics_compliance(
    y_pred: np.ndarray,
    u_star: np.ndarray,
    u_star_t: np.ndarray,
    is_source: np.ndarray
) -> Dict[str, float]:
    """
    Calculates percentage of model predictions that strictly satisfy physical laws:
      1. Non-negativity: concentration >= 0
      2. Aerodynamic threshold: source nodes cannot generate large sandstorms when u* << u*t
    """
    non_negative = np.all(y_pred >= 0)

    # In source areas where u* < u*t * 0.85, severe dust (>1000) is physically disallowed
    unphysical_source_spikes = (is_source[:, None] if is_source.ndim == 1 else is_source) & \
                              (u_star < (u_star_t * 0.85)) & \
                              (y_pred > 1000.0)

    total_pts = y_pred.size
    violation_count = int(np.sum(unphysical_source_spikes))
    compliance_pct = float(100.0 * (1.0 - violation_count / max(total_pts, 1)))

    return {
        "strictly_non_negative": bool(non_negative),
        "aerodynamic_compliance_percent": round(compliance_pct, 2),
        "violation_count": violation_count
    }
