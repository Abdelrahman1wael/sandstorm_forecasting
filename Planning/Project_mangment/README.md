# 📁 Project Management & Infrastructure Planning Suite
### *DustML Research Initiative • Compute Resources & Dataset Sizing Specifications*

This directory houses the foundational infrastructure, hardware capacity planning, and scientific dataset sizing guides required to train, evaluate, and deploy the **DustML Sandstorm Forecasting Platform**.

---

## 📂 Documentation Catalog

| Document | Primary Focus & Domain | Key Deliverables & Targets |
| :--- | :--- | :--- |
| **[`HARDWARE_RESOURCE_SPECIFICATIONS_GPU_CPU.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Project_mangment/HARDWARE_RESOURCE_SPECIFICATIONS_GPU_CPU.md)** | **Compute & Hardware Infrastructure**<br>CPU, GPU, RAM, VRAM, and Storage Throughput | • Multi-tier hardware matrix (Tier 1 Local, Tier 2 Academic Workstation, Tier 3 HPC/Cloud).<br>• VRAM memory mathematical footprint for Line B (AI-GAMFS + ST-GNN + PINN autograd).<br>• Host RAM sizing for Line A GBDT (15M rows $\times$ 142 features).<br>• High-speed NVMe scratch storage and I/O throughput targets.<br>• Training wall-clock time estimates & production inference serving specs. |
| **[`DATASET_VOLUME_AND_SAMPLE_SIZING_GUIDE.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Project_mangment/DATASET_VOLUME_AND_SAMPLE_SIZING_GUIDE.md)** | **Data Volume & Statistical Sample Sizing**<br>Temporal Span, Spatial Density, Class Imbalance | • Scientific rationale for 10–15 years temporal span (capturing rare extreme spring events and ENSO/AO teleconnections).<br>• Modality-by-modality data volume breakdown (8.0 TB raw $\to$ 1.06 TB harmonized tensors).<br>• Extreme event effective sample size ($N_{\text{eff}} > 2.7\text{M}$ severe observations).<br>• 5D sequence volume for Line B deep learning ($18,500$ sequences).<br>• Psychometric sample size calculation ($N = 1,500$ valid survey cases) for AMOS/SPSS SEM.<br>• Strict chronological walk-forward split (2012–2021 Train, 2022–2023 Val, 2024 Blind Test). |

---

## ⚡ Quick Reference: Target Requirements Snapshot

```
+---------------------------------------------------------------------------------------------------+
|                                 DUSTML INFRASTRUCTURE AT A GLANCE                                 |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [COMPUTE SPECIFICATION (RECOMMENDED)]               [DATASET SCALE (PUBLICATION-GRADE)]          |
|  • GPU: 1× or 2× NVIDIA RTX 4090 (24GB VRAM)        • Historical Span: 10 - 15 Years (2012-2024)  |
|  • CPU: Intel i9-14900K / AMD Ryzen 9 7950X         • Ground Stations: 2,400+ CMA/MEE Sensors     |
|  • System RAM: 64 GB - 128 GB DDR5                  • Total Raw Tabular Records: ~210 Million     |
|  • Storage: 2TB NVMe OS + 4TB NVMe Scratch + 16TB   • Deep Spatiotemporal Sequences: ~18,500      |
|  • Training Time: ~36 Hours for full pipeline       • Public Survey Size: N = 1,500 Valid Cases   |
+---------------------------------------------------------------------------------------------------+
```

---

## 🔗 Related Documentation
* Master Planning Catalog: [`Planning/README.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/README.md)
* Data Modalities & Sources: [`Planning/DATA_TYPES_AND_SOURCES_GUIDE.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/DATA_TYPES_AND_SOURCES_GUIDE.md)
* Machine Learning Methodology: [`Planning/LINE_A_PHASES_AND_METHODOLOGY.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/LINE_A_PHASES_AND_METHODOLOGY.md)
* Deep Learning & PINN Methodology: [`Planning/LINE_B_PHASES_AND_METHODOLOGY.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/LINE_B_PHASES_AND_METHODOLOGY.md)
* Anti-Overfitting Safeguards: [`Planning/Prevent_Overfiting/README.md`](file:///c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Prevent_Overfiting/README.md)
