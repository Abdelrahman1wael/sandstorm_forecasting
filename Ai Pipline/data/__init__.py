"""
DustML Data Module: Mock data generation, station profiles, and PyTorch dataset loaders.
"""
from .mock_generator import DustMockDataGenerator, CORRIDOR_STATIONS, LEAD_TIMES, LEAD_TIME_LABELS, HAZARD_CLASSES

__all__ = [
    "DustMockDataGenerator",
    "CORRIDOR_STATIONS",
    "LEAD_TIMES",
    "LEAD_TIME_LABELS",
    "HAZARD_CLASSES"
]
