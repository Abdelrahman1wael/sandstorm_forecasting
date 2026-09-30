"""
==============================================================================
DustML: High-Fidelity Synthetic Mock Data Generator
Translating USTB Master's Research Proposal Specifications into Scientific Mock Data
==============================================================================
"""

import json
import os
from typing import Dict, List, Tuple, Any
import numpy as np

# 14 Primary Nodes across East Asian Dust Corridors (from Planning / ST-GNN specs)
CORRIDOR_STATIONS = [
    {
        "id": "station-minqin",
        "code": "52681",
        "name": "Minqin Station (民勤)",
        "region": "Gansu • Hexi Corridor Gateway (河西走廊咽喉)",
        "type": "Primary Dust Transport Bottleneck",
        "lat": 38.63,
        "lon": 103.08,
        "elevation_m": 1367,
        "is_source": False,
        "u_star_t": 0.42,  # Aerodynamic friction velocity threshold (m/s)
        "roughness_z0": 0.0012,
    },
    {
        "id": "station-hotan",
        "code": "51828",
        "name": "Hotan Station (和田)",
        "region": "Xinjiang • Southern Taklamakan Desert Rim (塔克拉玛干南缘)",
        "type": "Major Source Desert Origin",
        "lat": 37.13,
        "lon": 79.93,
        "elevation_m": 1375,
        "is_source": True,
        "u_star_t": 0.32,
        "roughness_z0": 0.0005,
    },
    {
        "id": "station-beijing",
        "code": "54511",
        "name": "Beijing Mega-Station (北京奥体)",
        "region": "Beijing-Tianjin-Hebei High-Density Urban Zone (京津冀核心受体)",
        "type": "Dense Receptor Urban Node",
        "lat": 39.98,
        "lon": 116.38,
        "elevation_m": 43,
        "is_source": False,
        "u_star_t": 0.65,
        "roughness_z0": 0.85,
    },
    {
        "id": "station-chengdu",
        "code": "56187",
        "name": "Chengdu Station (成都温江)",
        "region": "Sichuan Basin • Complex Topography Receptor (四川盆地受体)",
        "type": "120h Remote Incursion Terminal",
        "lat": 30.70,
        "lon": 103.83,
        "elevation_m": 547,
        "is_source": False,
        "u_star_t": 0.70,
        "roughness_z0": 0.60,
    },
    {
        "id": "station-erenhot",
        "code": "53068",
        "name": "Erenhot Station (二连浩特)",
        "region": "Inner Mongolia • Sino-Mongolian Border (中蒙边境戈壁通道)",
        "type": "Northern Inflow Corridor Gateway",
        "lat": 43.65,
        "lon": 111.97,
        "elevation_m": 965,
        "is_source": True,
        "u_star_t": 0.38,
        "roughness_z0": 0.002,
    },
    {
        "id": "station-lanzhou",
        "code": "52889",
        "name": "Lanzhou Station (兰州皋兰)",
        "region": "Gansu • Western Loess Plateau Valley (黄土高原西缘)",
        "type": "Loess Plateau Advection Transit",
        "lat": 36.05,
        "lon": 103.88,
        "elevation_m": 1517,
        "is_source": False,
        "u_star_t": 0.50,
        "roughness_z0": 0.05,
    },
    {
        "id": "station-dunhuang",
        "code": "52418",
        "name": "Dunhuang Station (敦煌)",
        "region": "Gansu • Kumtag Desert Confluence (库姆塔格沙漠汇流区)",
        "type": "Hexi Western Portal",
        "lat": 40.15,
        "lon": 94.68,
        "elevation_m": 1139,
        "is_source": True,
        "u_star_t": 0.35,
        "roughness_z0": 0.001,
    },
    {
        "id": "station-hohhot",
        "code": "53463",
        "name": "Hohhot Station (呼和浩特)",
        "region": "Inner Mongolia • Daqing Mountains Southern Foothills (大青山南麓)",
        "type": "Northern Grassland Incursion Node",
        "lat": 40.82,
        "lon": 111.68,
        "elevation_m": 1063,
        "is_source": False,
        "u_star_t": 0.48,
        "roughness_z0": 0.02,
    },
    # 6 Additional Corridor Backbone Nodes
    {
        "id": "station-badain",
        "code": "52576",
        "name": "Badain Jaran Desert Core (巴丹吉林沙漠中心)",
        "region": "Alxa League • Mega-dune Dust Source",
        "type": "Active Megadune Source",
        "lat": 39.75,
        "lon": 102.35,
        "elevation_m": 1210,
        "is_source": True,
        "u_star_t": 0.30,
        "roughness_z0": 0.0003,
    },
    {
        "id": "station-tengger",
        "code": "53512",
        "name": "Tengger Desert Rim (腾格里沙漠边缘)",
        "region": "Ningxia/Inner Mongolia • Shapotou",
        "type": "Active Sandfield Source",
        "lat": 37.50,
        "lon": 105.10,
        "elevation_m": 1240,
        "is_source": True,
        "u_star_t": 0.33,
        "roughness_z0": 0.0006,
    },
    {
        "id": "station-zhangye",
        "code": "52652",
        "name": "Zhangye Station (张掖)",
        "region": "Gansu • Middle Hexi Oasis",
        "type": "Hexi Corridor Middle Station",
        "lat": 38.93,
        "lon": 100.45,
        "elevation_m": 1482,
        "is_source": False,
        "u_star_t": 0.45,
        "roughness_z0": 0.015,
    },
    {
        "id": "station-yinchuan",
        "code": "53614",
        "name": "Yinchuan Station (银川)",
        "region": "Ningxia • Helan Mountains Gap",
        "type": "Yellow River Plain Transit",
        "lat": 38.47,
        "lon": 106.27,
        "elevation_m": 1111,
        "is_source": False,
        "u_star_t": 0.48,
        "roughness_z0": 0.03,
    },
    {
        "id": "station-xian",
        "code": "57036",
        "name": "Xi'an Station (西安)",
        "region": "Shaanxi • Guanzhong Plain (关中平原)",
        "type": "Northern Flank of Qinling Mountains",
        "lat": 34.30,
        "lon": 108.93,
        "elevation_m": 397,
        "is_source": False,
        "u_star_t": 0.60,
        "roughness_z0": 0.45,
    },
    {
        "id": "station-taiyuan",
        "code": "53772",
        "name": "Taiyuan Station (太原)",
        "region": "Shanxi • Fenhe Valley Basin",
        "type": "Loess Plateau Eastern Passage",
        "lat": 37.78,
        "lon": 112.55,
        "elevation_m": 778,
        "is_source": False,
        "u_star_t": 0.55,
        "roughness_z0": 0.20,
    }
]

# Forecast Lead Times in hours (1 to 15 days)
LEAD_TIMES = [24, 72, 120, 168, 240, 360]
LEAD_TIME_LABELS = ["24h (Day 1)", "72h (Day 3)", "120h (Day 5)", "168h (Day 7)", "240h (Day 10)", "360h (Day 15)"]

# Hazard Classification Categories (CMA Standard)
HAZARD_CLASSES = [
    {"id": 0, "name": "Clean / Normal", "pm10_range": [0, 150], "weight": 1.0},
    {"id": 1, "name": "Floating Dust (浮尘)", "pm10_range": [150, 500], "weight": 2.5},
    {"id": 2, "name": "Blowing Sand (扬沙)", "pm10_range": [500, 1000], "weight": 5.0},
    {"id": 3, "name": "Sandstorm (沙尘暴)", "pm10_range": [1000, 2000], "weight": 10.0},
    {"id": 4, "name": "Severe Sandstorm (强沙尘暴)", "pm10_range": [2000, 99999], "weight": 25.0},
]


class DustMockDataGenerator:
    """
    Scientific Mock Data Generator for Sand and Dust Storm Forecasting.
    Implements physical aerodynamic principles:
      - Saltation horizontal flux: F_salt = C * (rho/g) * u_*^3 * (1 - u_*t^2 / u_*^2) if u_* > u_*t else 0
      - Advection-diffusion transport across directed corridor network
      - Systematic NWP bias with terrain-dependent errors
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        np.random.seed(seed)
        self.stations = CORRIDOR_STATIONS
        self.n_stations = len(self.stations)
        self.adj_matrix, self.corridor_edges = self._build_corridor_graph()

    def _build_corridor_graph(self) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """Build directed graph adjacency matrix representing East Asian dust pathways."""
        N = self.n_stations
        code_to_idx = {s["code"]: i for i, s in enumerate(self.stations)}
        adj = np.zeros((N, N), dtype=np.float32)

        # Primary physical dust corridors (Source -> Gateway -> Pathway -> Receptor)
        corridors = [
            ("51828", "52418", 1200, 18, 0.90), # Hotan -> Dunhuang
            ("52418", "52652", 600, 10, 0.85),  # Dunhuang -> Zhangye
            ("52576", "52681", 320, 6, 0.95),   # Badain Jaran -> Minqin
            ("52652", "52681", 280, 5, 0.88),   # Zhangye -> Minqin
            ("53512", "53614", 180, 4, 0.85),   # Tengger -> Yinchuan
            ("52681", "52889", 310, 7, 0.82),   # Minqin -> Lanzhou
            ("53068", "53463", 380, 8, 0.88),   # Erenhot -> Hohhot
            ("53463", "54511", 420, 9, 0.85),   # Hohhot -> Beijing
            ("53614", "53772", 560, 12, 0.78),  # Yinchuan -> Taiyuan
            ("53772", "54511", 450, 10, 0.80),  # Taiyuan -> Beijing
            ("52889", "57036", 520, 12, 0.75),  # Lanzhou -> Xi'an
            ("57036", "56187", 650, 24, 0.65),  # Xi'an -> Chengdu (Qinling breach, 120h delayed)
        ]

        edge_list = []
        for src_code, tgt_code, dist_km, transit_h, coupling in corridors:
            if src_code in code_to_idx and tgt_code in code_to_idx:
                u, v = code_to_idx[src_code], code_to_idx[tgt_code]
                # Normalized weight inversely proportional to transit time
                weight = float(coupling * np.exp(-transit_h / 24.0))
                adj[u, v] = weight
                edge_list.append({
                    "src_code": src_code,
                    "tgt_code": tgt_code,
                    "src_idx": u,
                    "tgt_idx": v,
                    "distance_km": dist_km,
                    "transit_hours": transit_h,
                    "coupling_strength": coupling,
                    "weight": weight
                })

        # Add self-loops with physical decay
        for i in range(N):
            adj[i, i] = 0.5

        # Row-normalize adjacency
        deg = np.sum(adj, axis=1, keepdims=True)
        deg[deg == 0] = 1.0
        adj_normalized = adj / deg

        return adj_normalized, edge_list

    def generate_station_timeseries(self, n_samples: int = 3000) -> Dict[str, np.ndarray]:
        """
        Generate synthetic time series for all stations with realistic diurnal,
        spring peak seasonality, and synoptic frontal storm events.
        """
        rng = np.random.default_rng(self.seed)
        t = np.arange(n_samples)

        # Seasonal spring cycle (March-May high probability)
        spring_seasonality = 0.5 + 0.5 * np.sin(2 * np.pi * t / (365 * 24) - np.pi / 2)
        # Diurnal thermal turbulence cycle (peak at 14:00 local time)
        diurnal = 0.3 * np.sin(2 * np.pi * t / 24.0)

        # Synoptic front occurrences (Poisson point process for cold surges)
        synoptic_events = (rng.uniform(0, 1, size=n_samples) > 0.96).astype(np.float32)
        # Exponential decay convolution for dust cloud persistence
        decay_kernel = np.exp(-np.arange(48) / 12.0)
        storm_signal = np.convolve(synoptic_events, decay_kernel, mode='same')

        # Features per station
        all_features = []
        all_nwp_pm10 = []
        all_observed_pm10 = []
        all_lead_pm10 = {lead: [] for lead in LEAD_TIMES}

        for s_idx, station in enumerate(self.stations):
            is_source = station["is_source"]
            u_star_t = station["u_star_t"]

            # 10m Wind Speed (m/s)
            base_wind = 4.0 if not is_source else 6.5
            wind_u10 = base_wind + 7.0 * storm_signal + 2.0 * diurnal + rng.normal(0, 1.2, size=n_samples)
            wind_u10 = np.clip(wind_u10, 0.2, 35.0)

            # Friction velocity u* = kappa * wind / ln(z / z0)
            u_star = 0.04 * wind_u10 + rng.normal(0, 0.02, size=n_samples)
            u_star = np.clip(u_star, 0.05, 2.2)

            # Volumetric soil moisture (0-7cm) [m3/m3]
            base_sm = 0.03 if is_source else 0.12
            soil_moisture = base_sm - 0.02 * storm_signal + rng.normal(0, 0.008, size=n_samples)
            soil_moisture = np.clip(soil_moisture, 0.01, 0.35)

            # 2m Temperature (K)
            temp_k = 285.0 + 8.0 * np.sin(2 * np.pi * t / 24.0) + rng.normal(0, 2.5, size=n_samples)

            # Boundary Layer Height (BLH in meters)
            blh = 800.0 + 1200.0 * np.maximum(0, diurnal) + rng.normal(0, 150, size=n_samples)
            blh = np.clip(blh, 100.0, 3500.0)

            # Satellite AOD (dimensionless)
            aod = 0.15 + 0.8 * storm_signal * spring_seasonality + rng.normal(0, 0.05, size=n_samples)
            aod = np.clip(aod, 0.02, 4.8)

            # Physical Owen's Saltation Emission:
            # F_salt = C * (rho/g) * u_*^3 * (1 - u_*t^2 / u_*^2) if u_* > u_*t
            active_saltation = u_star > u_star_t
            excess_ratio = np.maximum(0.0, 1.0 - (u_star_t ** 2) / np.maximum(u_star ** 2, 1e-6))
            saltation_flux = 1200.0 * (u_star ** 3) * excess_ratio * active_saltation.astype(np.float32)

            # True Observed PM10 (μg/m³)
            background_pm10 = 45.0 + 20.0 * rng.uniform(0, 1, size=n_samples)
            true_pm10 = background_pm10 + saltation_flux + 450.0 * storm_signal * spring_seasonality
            if not is_source:
                # Downstream advected dust
                true_pm10 = true_pm10 * 0.4 + 300.0 * storm_signal * (1.0 - soil_moisture * 2.0)
            true_pm10 = np.clip(true_pm10, 15.0, 8500.0)

            # Simulated Traditional NWP forecast (ECMWF IFS / CMA-GFS)
            # Physical models suffer from smooth diffusion, underestimating extreme peaks and delaying onset
            nwp_pm10 = true_pm10 * rng.uniform(0.65, 0.85, size=n_samples) + rng.normal(0, 45, size=n_samples)
            nwp_pm10 = np.maximum(10.0, nwp_pm10)

            # Visibility (Koschmieder equation: Vis = 3.912 / Extinction ~ Const / PM10)
            visibility_km = 45.0 / (1.0 + 0.015 * true_pm10) + rng.normal(0, 1.5, size=n_samples)
            visibility_km = np.clip(visibility_km, 0.1, 50.0)

            # Build feature array for this station
            # [u10, u_star, u_star_t, soil_moisture, temp_k, blh, aod, nwp_pm10, vis, elev, lat, lon]
            station_features = np.column_stack([
                wind_u10,
                u_star,
                np.full(n_samples, u_star_t),
                soil_moisture,
                temp_k,
                blh,
                aod,
                nwp_pm10,
                visibility_km,
                np.full(n_samples, station["elevation_m"]),
                np.full(n_samples, station["lat"]),
                np.full(n_samples, station["lon"]),
            ])

            all_features.append(station_features)
            all_nwp_pm10.append(nwp_pm10)
            all_observed_pm10.append(true_pm10)

            # Generate multi-lead future targets (lead hours decay predictability)
            for lead in LEAD_TIMES:
                lead_step = max(1, lead // 6)
                shifted_true = np.roll(true_pm10, -lead_step)
                # Add lead-dependent noise (uncertainty grows with lead time)
                noise_scale = 0.05 * (lead / 24.0) * true_pm10
                lead_target = shifted_true + rng.normal(0, noise_scale, size=n_samples)
                all_lead_pm10[lead].append(np.clip(lead_target, 10.0, 9000.0))

        # Array shapes: [N_stations, N_samples, N_features]
        features = np.array(all_features, dtype=np.float32)
        nwp_pm10_arr = np.array(all_nwp_pm10, dtype=np.float32)
        obs_pm10_arr = np.array(all_observed_pm10, dtype=np.float32)
        leads_dict = {lead: np.array(all_lead_pm10[lead], dtype=np.float32) for lead in LEAD_TIMES}

        return {
            "features": features,                     # [14, samples, 12]
            "feature_names": [
                "wind_u10", "u_star", "u_star_t", "soil_moisture",
                "temp_k", "blh", "aod", "nwp_pm10", "visibility_km",
                "elevation_m", "lat", "lon"
            ],
            "nwp_pm10": nwp_pm10_arr,                 # [14, samples]
            "observed_pm10": obs_pm10_arr,            # [14, samples]
            "lead_targets": leads_dict,               # dict of [14, samples]
            "adjacency_matrix": self.adj_matrix,      # [14, 14]
            "corridor_edges": self.corridor_edges,
            "stations": self.stations
        }

    def generate_multimodal_dl_tensors(self, n_batches: int = 128, seq_len: int = 24) -> Dict[str, np.ndarray]:
        """
        Generate multi-modal spatiotemporal tensors mirroring operational ingestion schemas:
          - NWP Ensembles: [Batch, Channels=6, Height=16, Width=16]
          - Satellite (AOD, RGB Dust, NDVI): [Batch, Channels=3, Height=32, Width=32]
          - Station Graph Nodes: [Batch, Nodes=14, Features=12]
          - Temporal Sequence: [Batch, SeqLen=24, Nodes=14, Features=12]
          - Multi-lead targets: [Batch, Nodes=14, Leads=6]
        """
        rng = np.random.default_rng(self.seed + 1)
        N = self.n_stations
        L = len(LEAD_TIMES)

        # 1. Gridded NWP atmospheric dynamic fields (u10, v10, t2m, msl, blh, gh500)
        nwp_grid = rng.normal(0, 1, size=(n_batches, 6, 16, 16)).astype(np.float32)

        # 2. Satellite imagery (FY-4B & MODIS: AOD, dust index, NDVI)
        satellite_grid = np.abs(rng.normal(0.4, 0.3, size=(n_batches, 3, 32, 32))).astype(np.float32)

        # 3. Graph node features (current instant)
        node_features = rng.normal(0, 1, size=(n_batches, N, 12)).astype(np.float32)

        # 4. Spatiotemporal sequence of node states (past 24 hours)
        seq_features = rng.normal(0, 1, size=(n_batches, seq_len, N, 12)).astype(np.float32)

        # 5. Future multi-lead PM10 concentrations across all 14 stations
        # Physical structure: higher values in source deserts, smooth propagation downstream
        targets_pm10 = np.zeros((n_batches, N, L), dtype=np.float32)
        for b in range(n_batches):
            base_event = rng.choice([50.0, 250.0, 900.0, 2200.0], p=[0.55, 0.25, 0.15, 0.05])
            for i, st in enumerate(self.stations):
                source_factor = 1.8 if st["is_source"] else 0.8
                for l_idx, lead in enumerate(LEAD_TIMES):
                    decay = np.exp(-lead / 200.0)
                    targets_pm10[b, i, l_idx] = base_event * source_factor * decay + rng.uniform(20.0, 80.0)

        # Categorical hazard classes [Batch, Nodes, Leads]
        hazard_classes = np.zeros((n_batches, N, L), dtype=np.int64)
        for class_info in reversed(HAZARD_CLASSES):
            mask = targets_pm10 >= class_info["pm10_range"][0]
            hazard_classes[mask] = class_info["id"]

        return {
            "nwp_grid": nwp_grid,
            "satellite_grid": satellite_grid,
            "node_features": node_features,
            "seq_features": seq_features,
            "targets_pm10": targets_pm10,
            "hazard_classes": hazard_classes,
            "adjacency_matrix": self.adj_matrix
        }

    def save_mock_dataset(self, output_dir: str):
        """Save synthetic datasets to disk in compressed NPZ and JSON format."""
        os.makedirs(output_dir, exist_ok=True)
        ts_data = self.generate_station_timeseries(n_samples=2500)
        dl_data = self.generate_multimodal_dl_tensors(n_batches=160, seq_len=24)

        # Save timeseries and tabular mock data
        npz_path = os.path.join(output_dir, "dust_mock_dataset.npz")
        np.savez_compressed(
            npz_path,
            features=ts_data["features"],
            nwp_pm10=ts_data["nwp_pm10"],
            observed_pm10=ts_data["observed_pm10"],
            adjacency_matrix=ts_data["adjacency_matrix"],
            dl_nwp_grid=dl_data["nwp_grid"],
            dl_satellite=dl_data["satellite_grid"],
            dl_seq_features=dl_data["seq_features"],
            dl_targets=dl_data["targets_pm10"],
            dl_hazards=dl_data["hazard_classes"]
        )

        # Save metadata and stations
        meta_path = os.path.join(output_dir, "dust_stations.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({
                "stations": self.stations,
                "lead_times": LEAD_TIMES,
                "lead_time_labels": LEAD_TIME_LABELS,
                "hazard_classes": HAZARD_CLASSES,
                "corridor_edges": self.corridor_edges,
                "feature_names": ts_data["feature_names"]
            }, f, indent=2, ensure_ascii=False)

        print(f"[MockDataGenerator] Successfully generated and saved mock datasets to {output_dir}")
        return npz_path, meta_path


if __name__ == "__main__":
    generator = DustMockDataGenerator(seed=42)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generator.save_mock_dataset(os.path.join(current_dir, "cache"))
