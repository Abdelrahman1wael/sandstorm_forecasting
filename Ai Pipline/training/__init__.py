"""
DustML Training Module: Automated training pipelines for Machine Learning (Line A) and Deep Learning (Line B).
"""
from .train_ml import run_ml_training_pipeline
from .train_dl import run_dl_training_pipeline

__all__ = [
    "run_ml_training_pipeline",
    "run_dl_training_pipeline"
]
