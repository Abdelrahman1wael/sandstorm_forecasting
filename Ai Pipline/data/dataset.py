"""
==============================================================================
DustML Dataset Loaders: Tabular & Spatiotemporal Multi-Modal Tensors
==============================================================================
"""

import os
from typing import Tuple, Dict, Any, Optional
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from .mock_generator import DustMockDataGenerator, LEAD_TIMES, HAZARD_CLASSES


class TabularDustDataset:
    """
    Dataset builder for Main Line A (Tree Ensembles & NWP Bias Correction).
    Flattens spatial stations and time steps into tabular feature vectors,
    engineered with physical meteorological indicators.
    """

    def __init__(self, data_cache_dir: Optional[str] = None):
        self.generator = DustMockDataGenerator(seed=42)
        self.raw_data = self.generator.generate_station_timeseries(n_samples=3000)
        self.feature_names = self._create_engineered_feature_names()

    def _create_engineered_feature_names(self):
        base = [
            "wind_u10", "u_star", "u_star_t", "soil_moisture",
            "temp_k", "blh", "aod", "nwp_pm10", "visibility_km",
            "elevation_m", "lat", "lon"
        ]
        engineered = [
            "friction_velocity_excess",  # u* - u*t
            "saltation_active_flag",     # 1 if u* > u*t else 0
            "dryness_wind_interaction",  # wind_u10 / (soil_moisture + 1e-4)
            "nwp_bias_proxy",            # nwp_pm10 / (visibility_km + 1.0)
            "aod_blh_ratio"              # aod / (blh + 10.0)
        ]
        return base + engineered

    def get_tabular_data(self, lead_time_hours: int = 72, test_ratio: float = 0.2, val_ratio: float = 0.1):
        """
        Returns (X_train, y_train, X_val, y_val, X_test, y_test, y_nwp_test, hazard_test)
        """
        feats = self.raw_data["features"]             # [14, N, 12]
        n_stations, n_samples, n_base_feats = feats.shape

        lead_idx = LEAD_TIMES.index(lead_time_hours) if lead_time_hours in LEAD_TIMES else 1
        y_leads = self.raw_data["lead_targets"][lead_time_hours] # [14, N]
        nwp_pm10 = self.raw_data["nwp_pm10"]                    # [14, N]

        X_rows = []
        y_rows = []
        nwp_rows = []

        for s in range(n_stations):
            f = feats[s]  # [N, 12]
            u10 = f[:, 0]
            u_star = f[:, 1]
            u_star_t = f[:, 2]
            sm = f[:, 3]
            blh = f[:, 5]
            aod = f[:, 6]
            vis = f[:, 8]
            nwp = nwp_pm10[s]

            # Engineered features
            u_excess = np.maximum(0.0, u_star - u_star_t)
            is_salt = (u_star > u_star_t).astype(np.float32)
            dry_wind = u10 / (sm + 1e-4)
            nwp_proxy = nwp / (vis + 1.0)
            aod_blh = aod / (blh + 10.0)

            eng = np.column_stack([u_excess, is_salt, dry_wind, nwp_proxy, aod_blh])
            all_feats = np.hstack([f, eng])

            X_rows.append(all_feats)
            y_rows.append(y_leads[s])
            nwp_rows.append(nwp)

        X = np.vstack(X_rows)       # [14 * N, 17]
        y = np.concatenate(y_rows)  # [14 * N]
        y_nwp = np.concatenate(nwp_rows)

        # Categorical hazard label (0 to 4)
        hazard = np.zeros(len(y), dtype=np.int64)
        for c in reversed(HAZARD_CLASSES):
            mask = y >= c["pm10_range"][0]
            hazard[mask] = c["id"]

        # Temporal split (avoid data leakage across future events)
        n_total = len(X)
        n_test = int(n_total * test_ratio)
        n_val = int(n_total * val_ratio)
        n_train = n_total - n_test - n_val

        X_train, y_train = X[:n_train], y[:n_train]
        X_val, y_val = X[n_train:n_train + n_val], y[n_train:n_train + n_val]
        X_test, y_test = X[n_train + n_val:], y[n_train + n_val:]
        y_nwp_test = y_nwp[n_train + n_val:]
        hazard_test = hazard[n_train + n_val:]
        hazard_train = hazard[:n_train]

        return {
            "X_train": X_train, "y_train": y_train, "hazard_train": hazard_train,
            "X_val": X_val, "y_val": y_val,
            "X_test": X_test, "y_test": y_test,
            "y_nwp_test": y_nwp_test,
            "hazard_test": hazard_test,
            "feature_names": self.feature_names
        }


class SpatiotemporalDustDataset(Dataset):
    """
    PyTorch Dataset for Main Line B (AI-GAMFS 3D Swin + ST-GNN + PINN).
    Yields synchronized multi-modal spatial tensors and graph topologies.
    """

    def __init__(self, n_batches: int = 120, seq_len: int = 24, seed: int = 42):
        self.generator = DustMockDataGenerator(seed=seed)
        tensors = self.generator.generate_multimodal_dl_tensors(n_batches=n_batches, seq_len=seq_len)

        self.nwp_grid = torch.tensor(tensors["nwp_grid"], dtype=torch.float32)         # [B, 6, 16, 16]
        self.satellite_grid = torch.tensor(tensors["satellite_grid"], dtype=torch.float32) # [B, 3, 32, 32]
        self.node_features = torch.tensor(tensors["node_features"], dtype=torch.float32)   # [B, 14, 12]
        self.seq_features = torch.tensor(tensors["seq_features"], dtype=torch.float32)     # [B, 24, 14, 12]
        self.targets_pm10 = torch.tensor(tensors["targets_pm10"], dtype=torch.float32)     # [B, 14, 6]
        self.hazard_classes = torch.tensor(tensors["hazard_classes"], dtype=torch.long)    # [B, 14, 6]
        self.adj_matrix = torch.tensor(tensors["adjacency_matrix"], dtype=torch.float32)   # [14, 14]

    def __len__(self):
        return len(self.nwp_grid)

    def __getitem__(self, idx):
        return {
            "nwp_grid": self.nwp_grid[idx],
            "satellite_grid": self.satellite_grid[idx],
            "node_features": self.node_features[idx],
            "seq_features": self.seq_features[idx],
            "targets_pm10": self.targets_pm10[idx],
            "hazard_classes": self.hazard_classes[idx]
        }

    def get_adjacency_matrix(self) -> torch.Tensor:
        return self.adj_matrix


def get_dl_dataloaders(batch_size: int = 16, val_split: float = 0.2):
    """Construct Train and Validation PyTorch DataLoaders."""
    full_ds = SpatiotemporalDustDataset(n_batches=160, seq_len=24, seed=42)
    total_len = len(full_ds)
    val_len = int(total_len * val_split)
    train_len = total_len - val_len

    train_ds, val_ds = torch.utils.data.random_split(full_ds, [train_len, val_len])
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, full_ds.get_adjacency_matrix()
