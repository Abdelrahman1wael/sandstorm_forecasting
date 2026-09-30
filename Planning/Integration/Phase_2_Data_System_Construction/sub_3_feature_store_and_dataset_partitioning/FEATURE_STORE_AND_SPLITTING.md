# 🗄️ Phase 2 • Subfolder 3: Feature Store & Dataset Partitioning
### *4-Tier Physical Feature Engineering, Target Residuals & Walk-Forward Partitioning*
**Phase Horizon:** January 2026 – April 2026  
**Parent Phase:** Phase 2 (Data System Construction)

---

## 🎯 1. Operational Goal & Feature Assembly

Phase 2.3 computes advanced physical indicators from raw fields and partitions datasets into strict chronological training, validation, and testing sets:

```
Raw Calibrated Fields (NWP + Satellite + Surface)
                        │
                        ▼
       [4-Tier Feature Engineering Engine]
       • Tier 1: Dynamics (U10, Gust, Z500, PBLH, Thermal Lapse Rate)
       • Tier 2: Surface/Soil (Volumetric Soil Water, Roughness z0, ΔNDVI)
       • Tier 3: Terrain (Elevation H, Slope, TRI, Source Distance)
       • Tier 4: Temporal & Teleconnection (DOY sin/cos, Hour, AO/NAO)
                        │
                        ▼
       [Target Construction: ε = y_obs - y_nwp across Leads 72h-360h]
                        │
                        ▼
       [Walk-Forward Chronological Dataset Splitting]
```

---

## 📅 2. Walk-Forward Chronological Splitting (No Data Leakage)

To avoid temporal autocorrelation leakage, standard randomized cross-validation is forbidden. Data is split strictly chronologically:

```
Split 1: [Train: 2018 - 2021]  -->  [Test: Spring 2022 SDS Season]
Split 2: [Train: 2018 - 2022]  -->  [Test: Spring 2023 SDS Season]
Split 3: [Train: 2018 - 2023]  -->  [Test: Spring 2024 SDS Season]
Split 4: [Train: 2018 - 2024]  -->  [Test: Spring 2025 SDS Season (Benchmark)]
```

---

## 📋 3. Phase 2.3 Deliverables
* Serialized feature stores in Apache Feather / Parquet format.
* PyTorch DataLoader datasets with precomputed graph adjacency matrices ($\mathbf{A} \in \mathbb{R}^{14 \times 14}$).
