"""
DustML Evaluation Package: Verification metrics, benchmarking against ECMWF IFS NWP, and lead-time decay analysis.
"""
from .metrics import (
    compute_regression_metrics,
    compute_meteorological_contingency,
    compute_quantile_coverage,
    compute_physics_compliance
)
from .benchmark import run_system_benchmark

__all__ = [
    "compute_regression_metrics",
    "compute_meteorological_contingency",
    "compute_quantile_coverage",
    "compute_physics_compliance",
    "run_system_benchmark"
]
