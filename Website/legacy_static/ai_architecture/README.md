# AI Architecture & Neural Laboratory (DustML)
## Medium- to Long-Term Sand and Dust Storm Forecasting Platform
**Affiliation:** University of Science and Technology Beijing (北京科技大学) • School of Energy and Environmental Engineering  
**Discipline:** Environmental Engineering (环境工程) • Master's Candidate (2025.9 Enrollment)  

---

## 📌 Overview

The `ai_architecture/` folder provides a dedicated, interactive scientific dashboard, neural laboratory, and comprehensive synthetic mock data engine for the **DustML** extended-range (3–15 days) sand and dust storm forecasting system.

It translates the theoretical principles of the master's research proposal into an interactive web application that demonstrates:
1. **Coupled Large Planetary Foundation Models (AI-GAMFS):** 5km spatial resolution, 120-hour (5-day) advance forecast capability, 38.4%–74.2% error reduction over ECMWF IFS and NASA GEOS-CF.
2. **Physics-Informed Neural Networks (PINN):** Real-time enforcement of mass conservation ($\|\nabla \cdot (\rho \mathbf{u}) + \frac{\partial \rho}{\partial t}\|^2$) and aerodynamic saltation friction velocity thresholds ($u_* > u_{*t}$).
3. **Spatio-Temporal Graph Neural Networks (ST-GNN):** 14-node directed dust transport network covering Taklamakan, Badain Jaran, Tengger, Hexi Corridor, Loess Plateau, Beijing, and the Sichuan Basin.
4. **Dual-Line Forecasting Pipeline:**
   - **Main Line A:** Tree-Ensemble statistical post-processing (LightGBM, XGBoost, CatBoost) to correct systematic NWP biases.
   - **Main Line B:** End-to-end deep spatiotemporal models (AI-GAMFS 3D Swin-Transformer + ST-GNN + Earthformer).
5. **Non-parametric Uncertainty Quantification:** EALSTM-QR quantile regression yielding 10th (P10), 50th (P50), and 90th (P90) prediction intervals.
6. **Explainability & Verification:** Local and global SHAP attributions, cost-sensitive classification matrices, and 100-epoch training convergence telemetry.

---

## 📂 File Structure

| File | Type | Description |
| :--- | :--- | :--- |
| [`index.html`](file:///c:/Users/hp/Desktop/China_project/ai_architecture/index.html) | Standalone Web Application | Interactive AI Architecture Lab & dashboard containing 6 interactive scientific sections. |
| [`mock_data.js`](file:///c:/Users/hp/Desktop/China_project/ai_architecture/mock_data.js) | Scientific Data Repository | Rich synthetic mock data structures: tensor schemas, neural layer weights, 8 Chinese forecasting stations, training logs, and corridor graph links. |
| [`ai_architecture.js`](file:///c:/Users/hp/Desktop/China_project/ai_architecture/ai_architecture.js) | Controller & Reactive Logic | Handles user interactions, slider events, simulated neural inference runs, dynamic SVG network rendering, and tab switching. |
| [`styles.css`](file:///c:/Users/hp/Desktop/China_project/ai_architecture/styles.css) | Custom Design System | Dark-mode scientific aesthetic (`#050811`, `#070c18`), glassmorphism, responsive grid layouts, glowing telemetry indicators, and typography (`Outfit`, `Inter`, `JetBrains Mono`). |
| [`README.md`](file:///c:/Users/hp/Desktop/China_project/ai_architecture/README.md) | Module Documentation | Detailed architectural specification, tensor dimensions, and scientific references. |

---

## 🧪 Mock Data Engine (`mock_data.js`)

The mock data is fully self-contained and exposed globally under `window.AI_ARCH_MOCK_DATA`. It provides:

### 1. `SYSTEM_SPEC`
- Model Name: `DustML-NeuroForecast v2.4 (Coupled AI-GAMFS & PINN Core)`
- Parameters: 348.5 Million
- Hardware: 4x NVIDIA A100-SXM4 (80GB VRAM)
- Inference Latency: 1.42 seconds (compared to 6.5 hours for ECMWF 50-member physical ensemble, a 16,478x speedup)
- Domain: 0.05° (~5.0 km) Gridded East Asia Domain [70°E–135°E, 25°N–55°N]

### 2. `INPUT_TENSORS`
Synthetic high-dimensional tensors mirroring the 4 ingestion modalities:
- **`tensor-nwp`**: ECMWF IFS / CMA-GFS `[Batch=16, LeadTimes=15, Channels=12, Lat=601, Lon=1301]`
- **`tensor-era5`**: ERA5 Reanalysis `[Batch=16, HistorySteps=72, Channels=8, Lat=601, Lon=1301]`
- **`tensor-satellite`**: Fengyun-4B & MODIS `[Batch=16, Channels=6, Lat=1202, Lon=2602]`
- **`tensor-ground`**: 2,418 CMA Surface Stations `[Batch=16, Stations=2418, Features=9, History=24]`

### 3. `FORECAST_STATIONS`
8 real-world meteorological monitoring and forecast stations across key corridors:
1. **Minqin Station (民勤, 52681):** Hexi Corridor Gateway bottleneck
2. **Hotan Station (和田, 51828):** Southern Taklamakan Desert source
3. **Beijing Mega-Station (北京奥体, 54511):** High-density urban receptor
4. **Chengdu Station (成都温江, 56187):** 120-hour benchmark remote incursion (Qinling breach)
5. **Erenhot Station (二连浩特, 53068):** Sino-Mongolian border Gobi inflow
6. **Lanzhou Station (兰州皋兰, 52889):** Loess Plateau transit node
7. **Dunhuang Station (敦煌, 52418):** Kumtag Desert oasis inflow
8. **Hohhot Station (呼和浩特, 53463):** Northern steppe transition zone

### 4. `TRAINING_TELEMETRY`
100-epoch training convergence records tracking Total Loss, Data MSE, PINN Mass Loss, PINN Saltation Loss, Validation RMSE, and Threat Score (TS).

### 5. `CORRIDOR_GRAPH_DATA`
14 nodes and directed links detailing distance (km) and transit time (hours) across the East Asian dust transport corridors.

---

## 🚀 How to Run Locally

1. Open `ai_architecture/index.html` in any modern web browser directly, or serve the root directory using any local web server:
   ```bash
   # From c:/Users/hp/Desktop/China_project:
   python -m http.server 8000
   ```
2. Navigate to: `http://localhost:8000/ai_architecture/index.html`
3. Click through the interactive modules:
   - Select layers to view layer shapes and mathematical formulas.
   - Adjust station and lead time sliders in the **Live Inference Sandbox** to simulate forward passes.
   - Play with friction velocity and threshold sliders in the **PINN Physics Engine** to observe saltation thresholds.
   - View transport corridors and travel hours on the **ST-GNN Network Graph**.
   - Switch tabs under **Model Verification** to inspect benchmark tables, training curves, and the cost-sensitive matrix.
   - Use the **Mock Data Explorer** to inspect and copy raw synthetic JSON payloads.
