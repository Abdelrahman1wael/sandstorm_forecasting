/**
 * ==============================================================================
 * DUST-ML AI ARCHITECTURE: COMPREHENSIVE SCIENTIFIC MOCK DATA REPOSITORY
 * Applying Machine Learning to Medium- to Long-Term Sand & Dust Storm Forecasting
 * University of Science and Technology Beijing (北京科技大学)
 * ==============================================================================
 */

window.AI_ARCH_MOCK_DATA = (function () {
  'use strict';

  // 1. SYSTEM HARDWARE & HIGH-LEVEL SPECIFICATIONS
  const SYSTEM_SPEC = {
    systemName: "DustML-NeuroForecast v2.4 (Coupled AI-GAMFS & PINN Core)",
    institution: "University of Science and Technology Beijing (北京科技大学)",
    department: "School of Energy and Environmental Engineering (环境工程系)",
    targetLeadTimes: ["24h (Day 1)", "72h (Day 3)", "120h (Day 5)", "168h (Day 7)", "240h (Day 10)", "360h (Day 15)"],
    spatialResolution: "0.05° (~5.0 km) Gridded East Asia Domain [70°E–135°E, 25°N–55°N]",
    temporalStep: "Hourly (0–72h), 3-Hourly (72–168h), 6-Hourly (168–360h)",
    operationalCycles: "Twice daily (00:00 UTC and 12:00 UTC assimilation windows)",
    inferenceHardware: {
      cluster: "4x NVIDIA A100-SXM4 (80GB VRAM) Cluster Node",
      tensorPrecision: "Mixed Precision FP16 / BF16 with TensorRT-LLM Optimizations",
      inferenceLatencySec: 1.42,
      traditionalNWPLatencyHours: 6.5,
      speedupFactor: "16,478x vs ECMWF IFS 50-member Ensemble"
    },
    totalParameters: 348520000, // 348.5M params
    totalTrainingEpochs: 100,
    datasetVolumeTB: 14.8,
    benchmarkAccuracyGain: "38.4% – 74.2% error reduction over ECMWF IFS and NASA GEOS-CF"
  };

  // 2. MULTI-SOURCE HETEROGENEOUS INPUT TENSOR SCHEMAS (MOCK DATA)
  const INPUT_TENSORS = [
    {
      id: "tensor-nwp",
      source: "ECMWF IFS / CMA-GFS Ensemble",
      dimensions: "[Batch=16, LeadTimes=15, Channels=12, Lat=601, Lon=1301]",
      shapeHuman: "16 × 15 × 12 × 601 × 1301",
      variables: [
        { code: "u10", name: "10m Zonal U-Wind", unit: "m/s", typicalRange: "[-25.0, 35.0]", mean: 4.82, std: 3.91 },
        { code: "v10", name: "10m Meridional V-Wind", unit: "m/s", typicalRange: "[-20.0, 30.0]", mean: -1.24, std: 3.42 },
        { code: "t2m", name: "2m Air Temperature", unit: "K", typicalRange: "[250.0, 315.0]", mean: 288.4, std: 12.1 },
        { code: "msl", name: "Mean Sea Level Pressure", unit: "hPa", typicalRange: "[980.0, 1045.0]", mean: 1013.2, std: 9.8 },
        { code: "blh", name: "Boundary Layer Height", unit: "m", typicalRange: "[100.0, 3500.0]", mean: 1120.0, std: 620.0 },
        { code: "gh500", name: "500 hPa Geopotential Height", unit: "dam", typicalRange: "[510.0, 595.0]", mean: 562.1, std: 18.4 }
      ],
      updateFrequency: "6 Hours",
      regridMethod: "Bilinear Conservative Remapping to 0.05°",
      sampleSlice: [
        [10.4, 12.1, 14.8, 16.2, 15.0, 11.8],
        [8.9, 14.5, 18.2, 21.0, 17.6, 12.4],
        [6.2, 11.0, 19.4, 24.5, 20.1, 13.9],
        [5.1, 8.4, 16.3, 22.8, 18.9, 11.2]
      ]
    },
    {
      id: "tensor-era5",
      source: "ERA5 Reanalysis (Historical Climatology)",
      dimensions: "[Batch=16, HistorySteps=72, Channels=8, Lat=601, Lon=1301]",
      shapeHuman: "16 × 72 × 8 × 601 × 1301",
      variables: [
        { code: "swvl1", name: "Volumetric Soil Water Layer 1 (0-7cm)", unit: "m³/m³", typicalRange: "[0.02, 0.45]", mean: 0.08, std: 0.05 },
        { code: "swvl2", name: "Volumetric Soil Water Layer 2 (7-28cm)", unit: "m³/m³", typicalRange: "[0.04, 0.48]", mean: 0.12, std: 0.06 },
        { code: "sd", name: "Snow Depth Water Equivalent", unit: "m", typicalRange: "[0.0, 0.8]", mean: 0.01, std: 0.04 },
        { code: "ustar", name: "Surface Friction Velocity (u*)", unit: "m/s", typicalRange: "[0.05, 1.80]", mean: 0.38, std: 0.29 }
      ],
      updateFrequency: "Hourly Retrospective",
      regridMethod: "High-order Bicubic Spline",
      sampleSlice: [
        [0.042, 0.038, 0.035, 0.031, 0.033, 0.040],
        [0.039, 0.034, 0.029, 0.027, 0.029, 0.036],
        [0.045, 0.036, 0.031, 0.025, 0.028, 0.038],
        [0.050, 0.041, 0.034, 0.030, 0.032, 0.042]
      ]
    },
    {
      id: "tensor-satellite",
      source: "Fengyun-4B (AGRI) & MODIS Terra/Aqua",
      dimensions: "[Batch=16, Channels=6, Lat=1202, Lon=2602]",
      shapeHuman: "16 × 6 × 1202 × 2602",
      variables: [
        { code: "aod550", name: "Aerosol Optical Depth (550nm)", unit: "dimensionless", typicalRange: "[0.05, 5.00]", mean: 0.42, std: 0.68 },
        { code: "dust_rgb", name: "Thermal Dust Enhancement (B12-B14)", unit: "K", typicalRange: "[-15.0, 15.0]", mean: -2.1, std: 4.8 },
        { code: "ndvi", name: "Normalized Difference Vegetation Index", unit: "[-0.2, 0.9]", mean: 0.14, std: 0.12 }
      ],
      updateFrequency: "15 Minutes (FY-4B Rapid Scan)",
      regridMethod: "Cloud-masked Spatio-Temporal Kriging Imputation",
      sampleSlice: [
        [0.18, 0.24, 0.85, 2.14, 3.42, 1.95],
        [0.22, 0.41, 1.62, 3.88, 4.60, 2.78],
        [0.19, 0.58, 2.30, 4.12, 3.90, 2.10],
        [0.15, 0.32, 1.15, 2.80, 2.45, 1.20]
      ]
    },
    {
      id: "tensor-ground",
      source: "CMA National Surface Observation Stations (2,400+ Nodes)",
      dimensions: "[Batch=16, Stations=2418, Features=9, History=24]",
      shapeHuman: "16 × 2418 × 9 × 24",
      variables: [
        { code: "pm10", name: "Particulate Matter PM10 Concentration", unit: "μg/m³", typicalRange: "[10, 8500]", mean: 112.5, std: 345.8 },
        { code: "vis", name: "Horizontal Meteorological Visibility", unit: "m", typicalRange: "[50, 50000]", mean: 14200, std: 8900 },
        { code: "gust", name: "Maximum Instantaneous Wind Gust", unit: "m/s", typicalRange: "[0.5, 42.0]", mean: 9.8, std: 5.6 },
        { code: "code4677", name: "Present Weather Code (06: Dust, 07: Blowing, 08: Storm)", unit: "WMO Code", mean: 2.1, std: 1.8 }
      ],
      updateFrequency: "Real-time 10-Minute Stream",
      regridMethod: "Graph Adjacency Projection onto Hexagonal Geohash",
      sampleSlice: [
        [45.0, 120.0, 680.0, 2450.0, 4800.0, 1850.0],
        [52.0, 180.0, 920.0, 3100.0, 5600.0, 2200.0],
        [38.0, 95.0, 540.0, 1980.0, 3950.0, 1420.0]
      ]
    }
  ];

  // 3. DETAILED NEURAL ARCHITECTURE LAYERS (AI-GAMFS + PINN + ST-GNN + LINE A)
  const ARCHITECTURE_LAYERS = [
    {
      id: "layer-ingest",
      name: "Heterogeneous Multi-Modal Tensor Fusion Layer",
      branch: "Data Ingestion Backbone",
      type: "Adaptive Multi-Scale Embedding & Patch Projection",
      parameters: 18450000,
      inputShape: "Tensors from NWP (12ch), ERA5 (8ch), Satellite (6ch), Stations (9ch)",
      outputShape: "Latent Tensor [B=16, T=72, D=512, H=120, W=260]",
      activation: "GELU (Gaussian Error Linear Unit)",
      formula: "Z_0 = \\text{LayerNorm}\\left(\\sum_{m \\in \\mathcal{M}} \\mathbf{W}_m \\star X_m + \\mathbf{E}_{pos} + \\mathbf{E}_{modal}\\right)",
      description: "Projects high-dimensional multi-rate atmospheric variables into a unified 512-dimensional latent vector space with spatiotemporal positional and modality encodings.",
      hardwareFlops: "3.8 TFLOPs"
    },
    {
      id: "layer-aigamfs-swin",
      name: "AI-GAMFS Dual-Branch 3D Swin-Transformer Encoder",
      branch: "Main Line B: Deep Foundation Model",
      type: "Hierarchical Spatio-Temporal Shifted Window Self-Attention",
      parameters: 142800000,
      inputShape: "[B=16, T=72, D=512, H=120, W=260]",
      outputShape: "[B=16, T=15, D=1024, H=30, W=65]",
      activation: "GELU + DropPath (rate=0.2)",
      formula: "\\text{Attn}(Q, K, V) = \\text{Softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}} + B_{relative}\\right)V",
      description: "World's first aerosol-meteorology coupled neural large model backbone. Dispatches shifted 3D window self-attention across atmospheric fluid dynamics and aerosol advection tensors, scaling computation linearly with grid area.",
      hardwareFlops: "28.4 TFLOPs"
    },
    {
      id: "layer-stgnn-corridor",
      name: "Spatio-Temporal Graph Neural Network (ST-GNN)",
      branch: "Main Line B: Dust Advection Corridors",
      type: "Graph Diffusion Convolution with Adaptive Adjacency",
      parameters: 34200000,
      inputShape: "Graph Nodes N=34 (Key Deserts & Basins), Features D=256",
      outputShape: "Corridor Flux Tensor [B=16, N=34, T=15, F=64]",
      activation: "LeakyReLU (alpha=0.15)",
      formula: "H^{(l+1)} = \\sigma\\left(\\sum_{k=0}^{K} \\mathbf{P}_k \\mathbf{H}^{(l)} \\mathbf{W}_k + \\mathbf{A}_{dyn} \\mathbf{H}^{(l)} \\mathbf{\\Theta}\\right)",
      description: "Explicitly models the non-Euclidean physical advection pathways across the Taklamakan Desert, Badain Jaran, Hexi Corridor, Loess Plateau, and Sichuan Basin breach corridors using dynamic atmospheric geopotential distance matrices.",
      hardwareFlops: "6.2 TFLOPs"
    },
    {
      id: "layer-pinn-constraint",
      name: "Physics-Informed Neural Network (PINN) Constraint Layer",
      branch: "Physical Enforcement Engine",
      type: "Auto-Differentiating PDE Loss Regularizer",
      parameters: 12400000,
      inputShape: "Velocity (u,v,w), Density rho, Dust Concentration C, Friction u*",
      outputShape: "Physics Residual Scalars (L_mass, L_saltation, L_diffusion)",
      activation: "Tanh / Sine Activation for Smooth High-Order Derivatives",
      formula: "\\mathcal{L}_{PINN} = \\lambda_1 \\left\\|\\nabla \\cdot (\\rho \\mathbf{u}) + \\frac{\\partial \\rho}{\\partial t}\\right\\|^2 + \\lambda_2 \\left\\| F_{salt} - C \\frac{\\rho}{g} u_*^3 \\left(1 - \\frac{u_{*t}^2}{u_*^2}\\right) \\cdot \\mathbb{I}(u_* > u_{*t})\\right\\|^2",
      description: "Computes analytic backward gradients using automatic differentiation to penalize non-physical predictions that violate mass conservation or trigger dust saltation below the aerodynamic friction velocity threshold (u* < u*t).",
      hardwareFlops: "4.1 TFLOPs"
    },
    {
      id: "layer-line-a-ensemble",
      name: "Main Line A: Tree-Ensemble NWP Statistical Post-Processor",
      branch: "Main Line A: Statistical ML",
      type: "Gradient Boosted Decision Forest (LightGBM + CatBoost + XGBoost)",
      parameters: 28600000,
      inputShape: "Point-wise Feature Vector (184 engineered features per station)",
      outputShape: "Deterministic Bias-Corrected Residual [B=16, Stations=2418, LeadTimes=15]",
      activation: "Histogram-split Tree Leaves",
      formula: "\\hat{y}_{A} = y_{NWP} + \\sum_{m=1}^{M} \\alpha_m f_m(\\mathbf{x}; \\Theta_m)",
      description: "Corrects systematic operational bias in ECMWF IFS and CMA-GFS numerical ensembles, resolving local terrain sheltering effects, thermal inversions, and surface roughness micro-variations.",
      hardwareFlops: "0.8 TFLOPs"
    },
    {
      id: "layer-ealstm-qr",
      name: "EALSTM-QR Quantile Regression Uncertainty Head",
      branch: "Uncertainty & Decision Layer",
      type: "Entity-Aware LSTM with Pinball Quantile Loss",
      parameters: 22800000,
      inputShape: "Fused Representation Vector [B=16, D=1024]",
      outputShape: "Parametric Quantile Forecasts: 10th (P10), 50th (P50), 90th (P90) Percentiles",
      activation: "ELU / Linear",
      formula: "\\mathcal{L}_{pinball}(\\tau) = \\sum_{i} \\max\\left(\\tau(y_i - \\hat{y}_i^{(\\tau)}), (\\tau - 1)(y_i - \\hat{y}_i^{(\\tau)})\\right)",
      description: "Generates non-parametric prediction intervals rather than single point forecasts, providing probabilistic risk boundaries (10%, 50%, 90% exceedance) vital for emergency municipal mitigation.",
      hardwareFlops: "2.5 TFLOPs"
    },
    {
      id: "layer-focal-hazard",
      name: "Cost-Sensitive 4-Tier Categorical Hazard Classifier",
      branch: "Operational Meteorological Alerting",
      type: "Focal Loss Softmax Classifier with Asymmetric Penalty Matrix",
      parameters: 8900000,
      inputShape: "Multi-scale Spatiotemporal Head [B=16, D=512]",
      outputShape: "4-Class Probability Vector: [Clean, Floating Dust, Blowing Sand, Sandstorm, Severe]",
      activation: "Softmax with Cost Matrix Weighting",
      formula: "\\mathcal{L}_{Focal} = -\\alpha_t (1 - p_t)^\\gamma \\log(p_t) \\times \\mathbf{C}_{cost}[y_{true}, \\hat{y}_{pred}]",
      description: "Resolves the severe class imbalance where severe sandstorms account for <1.5% of total annual hours. Heavy penalties are levied against False Negatives (missed disasters).",
      hardwareFlops: "1.1 TFLOPs"
    }
  ];

  // 4. EIGHT KEY OBSERVATION & FORECAST BENCHMARK STATIONS (REAL COORDINATES & MOCK PREDICTIONS)
  const FORECAST_STATIONS = [
    {
      id: "station-minqin",
      name: "Minqin Station (民勤)",
      code: "52681",
      region: "Gansu • Hexi Corridor Gateway (河西走廊咽喉)",
      type: "Primary Dust Transport Bottleneck",
      coordinates: { lat: 38.63, lon: 103.08, elevationM: 1367 },
      currentObs: {
        timestamp: "2026-04-12 08:00 UTC",
        pm10: 1840,
        pm25: 410,
        visibilityKm: 0.9,
        windSpeed10m: 16.8,
        frictionVelocityUStar: 0.88,
        thresholdUStarT: 0.42,
        saltationActive: true,
        tempC: 14.2,
        relativeHumidity: 12,
        soilMoisture0_7cm: 0.031,
        alertLevel: "Sandstorm (沙尘暴)",
        alertColor: "#f97316"
      },
      leadTimeForecasts: [
        { lead: "24h (Day 1)", pm10_p50: 2150, p10: 1800, p90: 2600, category: "Severe Sandstorm", probDust: 0.98, pinnResidual: 0.0014, threatScore: 0.89 },
        { lead: "72h (Day 3)", pm10_p50: 1620, p10: 1250, p90: 2080, category: "Sandstorm", probDust: 0.93, pinnResidual: 0.0022, threatScore: 0.84 },
        { lead: "120h (Day 5)", pm10_p50: 890, p10: 620, p90: 1240, category: "Blowing Sand", probDust: 0.86, pinnResidual: 0.0038, threatScore: 0.78 },
        { lead: "168h (Day 7)", pm10_p50: 420, p10: 260, p90: 680, category: "Floating Dust", probDust: 0.72, pinnResidual: 0.0051, threatScore: 0.71 },
        { lead: "240h (Day 10)", pm10_p50: 210, p10: 110, p90: 380, category: "Floating Dust", probDust: 0.58, pinnResidual: 0.0079, threatScore: 0.62 },
        { lead: "360h (Day 15)", pm10_p50: 115, p10: 55, p90: 230, category: "Normal / Moderate", probDust: 0.39, pinnResidual: 0.0112, threatScore: 0.53 }
      ],
      shapContributions: [
        { feature: "Surface Friction Velocity (u*)", value: "+462 μg/m³", pct: 36.4, direction: "positive" },
        { feature: "10m Wind Speed (u10)", value: "+340 μg/m³", pct: 26.8, direction: "positive" },
        { feature: "Soil Moisture Deficit (0-7cm)", value: "+210 μg/m³", pct: 16.5, direction: "positive" },
        { feature: "Upstream Badain Jaran AOD", value: "+180 μg/m³", pct: 14.2, direction: "positive" },
        { feature: "Boundary Layer Height (BLH)", value: "-78 μg/m³", pct: 6.1, direction: "negative" }
      ]
    },
    {
      id: "station-hotan",
      name: "Hotan Station (和田)",
      code: "51828",
      region: "Xinjiang • Southern Taklamakan Desert Rim (塔克拉玛干南缘)",
      type: "Major Source Desert Origin",
      coordinates: { lat: 37.13, lon: 79.93, elevationM: 1375 },
      currentObs: {
        timestamp: "2026-04-12 08:00 UTC",
        pm10: 3850,
        pm25: 860,
        visibilityKm: 0.4,
        windSpeed10m: 19.5,
        frictionVelocityUStar: 1.12,
        thresholdUStarT: 0.38,
        saltationActive: true,
        tempC: 18.5,
        relativeHumidity: 9,
        soilMoisture0_7cm: 0.018,
        alertLevel: "Severe Sandstorm (强沙尘暴)",
        alertColor: "#ef4444"
      },
      leadTimeForecasts: [
        { lead: "24h (Day 1)", pm10_p50: 4200, p10: 3400, p90: 5100, category: "Severe Sandstorm", probDust: 0.99, pinnResidual: 0.0009, threatScore: 0.92 },
        { lead: "72h (Day 3)", pm10_p50: 2950, p10: 2200, p90: 3800, category: "Severe Sandstorm", probDust: 0.96, pinnResidual: 0.0018, threatScore: 0.88 },
        { lead: "120h (Day 5)", pm10_p50: 1780, p10: 1200, p90: 2450, category: "Sandstorm", probDust: 0.91, pinnResidual: 0.0031, threatScore: 0.82 },
        { lead: "168h (Day 7)", pm10_p50: 890, p10: 540, p90: 1350, category: "Blowing Sand", probDust: 0.79, pinnResidual: 0.0048, threatScore: 0.75 },
        { lead: "240h (Day 10)", pm10_p50: 480, p10: 250, p90: 820, category: "Floating Dust", probDust: 0.65, pinnResidual: 0.0072, threatScore: 0.66 },
        { lead: "360h (Day 15)", pm10_p50: 290, p10: 130, p90: 540, category: "Floating Dust", probDust: 0.48, pinnResidual: 0.0105, threatScore: 0.58 }
      ],
      shapContributions: [
        { feature: "Aerodynamic Shear Ratio (u*/u*t)", value: "+890 μg/m³", pct: 41.2, direction: "positive" },
        { feature: "Extreme Dry Soil Profile", value: "+510 μg/m³", pct: 23.6, direction: "positive" },
        { feature: "Surface Thermal Convection", value: "+380 μg/m³", pct: 17.6, direction: "positive" },
        { feature: "Low Atmospheric Humidity (9%)", value: "+240 μg/m³", pct: 11.1, direction: "positive" },
        { feature: "Topographic Basin Trapping", value: "+140 μg/m³", pct: 6.5, direction: "positive" }
      ]
    },
    {
      id: "station-beijing",
      name: "Beijing Mega-Station (北京奥体)",
      code: "54511",
      region: "Beijing-Tianjin-Hebei • North China Plain (华北平原受体城市)",
      type: "High-Value Megacity Downstream Receptor",
      coordinates: { lat: 39.98, lon: 116.39, elevationM: 43 },
      currentObs: {
        timestamp: "2026-04-12 08:00 UTC",
        pm10: 145,
        pm25: 48,
        visibilityKm: 12.0,
        windSpeed10m: 3.8,
        frictionVelocityUStar: 0.22,
        thresholdUStarT: 0.55,
        saltationActive: false,
        tempC: 16.8,
        relativeHumidity: 38,
        soilMoisture0_7cm: 0.145,
        alertLevel: "Normal (良好)",
        alertColor: "#10b981"
      },
      leadTimeForecasts: [
        { lead: "24h (Day 1)", pm10_p50: 180, p10: 120, p90: 260, category: "Normal / Moderate", probDust: 0.22, pinnResidual: 0.0011, threatScore: 0.91 },
        { lead: "72h (Day 3)", pm10_p50: 640, p10: 420, p90: 920, category: "Floating Dust", probDust: 0.84, pinnResidual: 0.0028, threatScore: 0.85 },
        { lead: "120h (Day 5)", pm10_p50: 1420, p10: 980, p90: 1980, category: "Sandstorm (Advection Arrival)", probDust: 0.94, pinnResidual: 0.0042, threatScore: 0.81 },
        { lead: "168h (Day 7)", pm10_p50: 510, p10: 310, p90: 780, category: "Floating Dust", probDust: 0.74, pinnResidual: 0.0059, threatScore: 0.73 },
        { lead: "240h (Day 10)", pm10_p50: 195, p10: 95, p90: 340, category: "Normal / Moderate", probDust: 0.42, pinnResidual: 0.0084, threatScore: 0.64 },
        { lead: "360h (Day 15)", pm10_p50: 110, p10: 45, p90: 210, category: "Normal", probDust: 0.28, pinnResidual: 0.0118, threatScore: 0.55 }
      ],
      shapContributions: [
        { feature: "Upstream Gobi/Inner Mongolia Advection Vector", value: "+540 μg/m³", pct: 45.0, direction: "positive" },
        { feature: "850 hPa Northwest Jet Stream", value: "+320 μg/m³", pct: 26.7, direction: "positive" },
        { feature: "Cold Front Baroclinic Forcing", value: "+190 μg/m³", pct: 15.8, direction: "positive" },
        { feature: "Local Urban Dry Deposition", value: "-95 μg/m³", pct: 7.9, direction: "negative" },
        { feature: "Boundary Layer Inversion Trap", value: "+55 μg/m³", pct: 4.6, direction: "positive" }
      ]
    },
    {
      id: "station-chengdu",
      name: "Chengdu Station (成都温江)",
      code: "56187",
      region: "Sichuan Basin • Southwest China (四川盆地 - 120h Landmark Benchmark)",
      type: "Remote Deep Basin Incursion (Qinling Breach)",
      coordinates: { lat: 30.70, lon: 103.83, elevationM: 526 },
      currentObs: {
        timestamp: "2026-04-12 08:00 UTC",
        pm10: 68,
        pm25: 35,
        visibilityKm: 18.0,
        windSpeed10m: 1.8,
        frictionVelocityUStar: 0.12,
        thresholdUStarT: 0.62,
        saltationActive: false,
        tempC: 19.4,
        relativeHumidity: 65,
        soilMoisture0_7cm: 0.242,
        alertLevel: "Normal (良好)",
        alertColor: "#10b981"
      },
      leadTimeForecasts: [
        { lead: "24h (Day 1)", pm10_p50: 72, p10: 50, p90: 105, category: "Normal", probDust: 0.08, pinnResidual: 0.0008, threatScore: 0.94 },
        { lead: "72h (Day 3)", pm10_p50: 95, p10: 65, p90: 140, category: "Normal", probDust: 0.18, pinnResidual: 0.0019, threatScore: 0.89 },
        { lead: "120h (Day 5)", pm10_p50: 680, p10: 440, p90: 960, category: "Floating Dust / Basin Intrusion ★", probDust: 0.91, pinnResidual: 0.0035, threatScore: 0.83 },
        { lead: "168h (Day 7)", pm10_p50: 820, p10: 560, p90: 1150, category: "Severe Trapping in Basin", probDust: 0.95, pinnResidual: 0.0049, threatScore: 0.77 },
        { lead: "240h (Day 10)", pm10_p50: 340, p10: 180, p90: 520, category: "Floating Dust", probDust: 0.64, pinnResidual: 0.0076, threatScore: 0.68 },
        { lead: "360h (Day 15)", pm10_p50: 92, p10: 48, p90: 170, category: "Normal", probDust: 0.25, pinnResidual: 0.0108, threatScore: 0.59 }
      ],
      shapContributions: [
        { feature: "AI-GAMFS 120h Remote Incursion Vector", value: "+380 μg/m³", pct: 48.1, direction: "positive" },
        { feature: "Qinling Mountain Gap Spillover", value: "+210 μg/m³", pct: 26.6, direction: "positive" },
        { feature: "Sichuan Basin Stagnant Inversion Layer", value: "+130 μg/m³", pct: 16.5, direction: "positive" },
        { feature: "High Relative Humidity Wet Scavenging", value: "-48 μg/m³", pct: 6.1, direction: "negative" },
        { feature: "Basin Micro-topography Barrier", value: "-22 μg/m³", pct: 2.7, direction: "negative" }
      ]
    },
    {
      id: "station-erenhot",
      name: "Erenhot Station (二连浩特)",
      code: "53068",
      region: "Inner Mongolia • Sino-Mongolian Border (中蒙边境荒漠化区)",
      type: "Northern Gobi Inflow Corridor",
      coordinates: { lat: 43.65, lon: 111.97, elevationM: 965 },
      currentObs: {
        timestamp: "2026-04-12 08:00 UTC",
        pm10: 2450,
        pm25: 520,
        visibilityKm: 0.6,
        windSpeed10m: 18.2,
        frictionVelocityUStar: 0.96,
        thresholdUStarT: 0.40,
        saltationActive: true,
        tempC: 8.4,
        relativeHumidity: 15,
        soilMoisture0_7cm: 0.024,
        alertLevel: "Severe Sandstorm (强沙尘暴)",
        alertColor: "#ef4444"
      },
      leadTimeForecasts: [
        { lead: "24h (Day 1)", pm10_p50: 2800, p10: 2100, p90: 3600, category: "Severe Sandstorm", probDust: 0.99, pinnResidual: 0.0011, threatScore: 0.91 },
        { lead: "72h (Day 3)", pm10_p50: 1950, p10: 1400, p90: 2600, category: "Sandstorm", probDust: 0.94, pinnResidual: 0.0021, threatScore: 0.86 },
        { lead: "120h (Day 5)", pm10_p50: 920, p10: 590, p90: 1380, category: "Blowing Sand", probDust: 0.85, pinnResidual: 0.0039, threatScore: 0.80 },
        { lead: "168h (Day 7)", pm10_p50: 440, p10: 240, p90: 710, category: "Floating Dust", probDust: 0.70, pinnResidual: 0.0054, threatScore: 0.72 },
        { lead: "240h (Day 10)", pm10_p50: 220, p10: 105, p90: 390, category: "Floating Dust", probDust: 0.54, pinnResidual: 0.0081, threatScore: 0.63 },
        { lead: "360h (Day 15)", pm10_p50: 125, p10: 52, p90: 240, category: "Normal", probDust: 0.35, pinnResidual: 0.0115, threatScore: 0.54 }
      ],
      shapContributions: [
        { feature: "Mongolian Cyclone Central Pressure Gradient", value: "+710 μg/m³", pct: 42.5, direction: "positive" },
        { feature: "Surface Friction Velocity (u*)", value: "+490 μg/m³", pct: 29.3, direction: "positive" },
        { feature: "Spring Thawing Loose Surface Crust", value: "+280 μg/m³", pct: 16.8, direction: "positive" },
        { feature: "Dry Cold Air Advection", value: "+140 μg/m³", pct: 8.4, direction: "positive" },
        { feature: "Grassland Boundary Buffer", value: "-50 μg/m³", pct: 3.0, direction: "negative" }
      ]
    },
    {
      id: "station-lanzhou",
      name: "Lanzhou Station (兰州皋兰)",
      code: "52889",
      region: "Gansu • Loess Plateau & Yellow River Basin (黄土高原核心)",
      type: "Transport Channel Transition Node",
      coordinates: { lat: 36.05, lon: 103.88, elevationM: 1517 },
      currentObs: {
        timestamp: "2026-04-12 08:00 UTC",
        pm10: 890,
        pm25: 195,
        visibilityKm: 2.2,
        windSpeed10m: 11.2,
        frictionVelocityUStar: 0.54,
        thresholdUStarT: 0.46,
        saltationActive: true,
        tempC: 13.5,
        relativeHumidity: 22,
        soilMoisture0_7cm: 0.062,
        alertLevel: "Blowing Sand (扬沙)",
        alertColor: "#eab308"
      },
      leadTimeForecasts: [
        { lead: "24h (Day 1)", pm10_p50: 1120, p10: 820, p90: 1540, category: "Sandstorm", probDust: 0.95, pinnResidual: 0.0016, threatScore: 0.88 },
        { lead: "72h (Day 3)", pm10_p50: 850, p10: 580, p90: 1220, category: "Blowing Sand", probDust: 0.89, pinnResidual: 0.0026, threatScore: 0.83 },
        { lead: "120h (Day 5)", pm10_p50: 460, p10: 290, p90: 710, category: "Floating Dust", probDust: 0.78, pinnResidual: 0.0041, threatScore: 0.76 },
        { lead: "168h (Day 7)", pm10_p50: 280, p10: 150, p90: 450, category: "Floating Dust", probDust: 0.62, pinnResidual: 0.0058, threatScore: 0.69 },
        { lead: "240h (Day 10)", pm10_p50: 160, p10: 80, p90: 280, category: "Normal", probDust: 0.45, pinnResidual: 0.0083, threatScore: 0.61 },
        { lead: "360h (Day 15)", pm10_p50: 95, p10: 42, p90: 190, category: "Normal", probDust: 0.31, pinnResidual: 0.0116, threatScore: 0.52 }
      ],
      shapContributions: [
        { feature: "Hexi Corridor Funneling Advection", value: "+380 μg/m³", pct: 40.0, direction: "positive" },
        { feature: "Loess Fine Particulate Re-entrainment", value: "+260 μg/m³", pct: 27.4, direction: "positive" },
        { feature: "Valley Terrain Wind Acceleration", value: "+170 μg/m³", pct: 17.9, direction: "positive" },
        { feature: "Yellow River Local Vapor Scavenging", value: "-80 μg/m³", pct: 8.4, direction: "negative" },
        { feature: "Mountain Barrier Stagnation", value: "+60 μg/m³", pct: 6.3, direction: "positive" }
      ]
    },
    {
      id: "station-dunhuang",
      name: "Dunhuang Station (敦煌)",
      code: "52418",
      region: "Gansu • Western Gobi & Kumtag Desert (库姆塔格沙漠前哨)",
      type: "Western Desert Oasis Inflow Node",
      coordinates: { lat: 40.15, lon: 94.68, elevationM: 1139 },
      currentObs: {
        timestamp: "2026-04-12 08:00 UTC",
        pm10: 2980,
        pm25: 640,
        visibilityKm: 0.5,
        windSpeed10m: 17.6,
        frictionVelocityUStar: 1.02,
        thresholdUStarT: 0.39,
        saltationActive: true,
        tempC: 15.8,
        relativeHumidity: 11,
        soilMoisture0_7cm: 0.021,
        alertLevel: "Severe Sandstorm (强沙尘暴)",
        alertColor: "#ef4444"
      },
      leadTimeForecasts: [
        { lead: "24h (Day 1)", pm10_p50: 3200, p10: 2500, p90: 4100, category: "Severe Sandstorm", probDust: 0.99, pinnResidual: 0.0010, threatScore: 0.92 },
        { lead: "72h (Day 3)", pm10_p50: 2100, p10: 1550, p90: 2800, category: "Sandstorm", probDust: 0.95, pinnResidual: 0.0020, threatScore: 0.87 },
        { lead: "120h (Day 5)", pm10_p50: 1150, p10: 780, p90: 1620, category: "Sandstorm", probDust: 0.88, pinnResidual: 0.0037, threatScore: 0.81 },
        { lead: "168h (Day 7)", pm10_p50: 520, p10: 310, p90: 840, category: "Floating Dust", probDust: 0.74, pinnResidual: 0.0052, threatScore: 0.73 },
        { lead: "240h (Day 10)", pm10_p50: 260, p10: 130, p90: 460, category: "Floating Dust", probDust: 0.57, pinnResidual: 0.0078, threatScore: 0.65 },
        { lead: "360h (Day 15)", pm10_p50: 140, p10: 60, p90: 270, category: "Normal", probDust: 0.38, pinnResidual: 0.0110, threatScore: 0.56 }
      ],
      shapContributions: [
        { feature: "Kumtag Desert Saltation Flux", value: "+740 μg/m³", pct: 43.5, direction: "positive" },
        { feature: "Surface Friction Velocity (u*)", value: "+460 μg/m³", pct: 27.1, direction: "positive" },
        { feature: "Extreme Aridity & Soil Crusting", value: "+290 μg/m³", pct: 17.1, direction: "positive" },
        { feature: "Surface Albedo Radiation Forcing", value: "+140 μg/m³", pct: 8.2, direction: "positive" },
        { feature: "Oasis Micro-climate Damping", value: "-70 μg/m³", pct: 4.1, direction: "negative" }
      ]
    },
    {
      id: "station-hohhot",
      name: "Hohhot Station (呼和浩特)",
      code: "53463",
      region: "Inner Mongolia • Daqing Mountains Southern Foothill (大青山南麓)",
      type: "Northern Steppe Transition Zone",
      coordinates: { lat: 40.85, lon: 111.75, elevationM: 1063 },
      currentObs: {
        timestamp: "2026-04-12 08:00 UTC",
        pm10: 1150,
        pm25: 280,
        visibilityKm: 1.8,
        windSpeed10m: 14.5,
        frictionVelocityUStar: 0.72,
        thresholdUStarT: 0.48,
        saltationActive: true,
        tempC: 11.2,
        relativeHumidity: 26,
        soilMoisture0_7cm: 0.078,
        alertLevel: "Sandstorm (沙尘暴)",
        alertColor: "#f97316"
      },
      leadTimeForecasts: [
        { lead: "24h (Day 1)", pm10_p50: 1350, p10: 980, p90: 1820, category: "Sandstorm", probDust: 0.96, pinnResidual: 0.0013, threatScore: 0.90 },
        { lead: "72h (Day 3)", pm10_p50: 920, p10: 640, p90: 1310, category: "Blowing Sand", probDust: 0.90, pinnResidual: 0.0024, threatScore: 0.85 },
        { lead: "120h (Day 5)", pm10_p50: 510, p10: 320, p90: 790, category: "Floating Dust", probDust: 0.81, pinnResidual: 0.0039, threatScore: 0.78 },
        { lead: "168h (Day 7)", pm10_p50: 290, p10: 160, p90: 480, category: "Floating Dust", probDust: 0.66, pinnResidual: 0.0055, threatScore: 0.70 },
        { lead: "240h (Day 10)", pm10_p50: 175, p10: 85, p90: 310, category: "Normal", probDust: 0.48, pinnResidual: 0.0080, threatScore: 0.62 },
        { lead: "360h (Day 15)", pm10_p50: 105, p10: 48, p90: 210, category: "Normal", probDust: 0.32, pinnResidual: 0.0114, threatScore: 0.53 }
      ],
      shapContributions: [
        { feature: "Ulan Buh / Hobq Desert Advection", value: "+410 μg/m³", pct: 39.0, direction: "positive" },
        { feature: "Northwesterly Gale Downslope Wind", value: "+310 μg/m³", pct: 29.5, direction: "positive" },
        { feature: "Low Spring Vegetative Cover", value: "+190 μg/m³", pct: 18.1, direction: "positive" },
        { feature: "Daqing Mountain Orographic Wave", value: "+95 μg/m³", pct: 9.0, direction: "positive" },
        { feature: "Urban Artificial Green Belt Mitigation", value: "-45 μg/m³", pct: 4.4, direction: "negative" }
      ]
    }
  ];

  // 5. ST-GNN CORRIDOR ADVECTION GRAPH NODES AND DIRECTED EDGES
  const CORRIDOR_GRAPH_DATA = {
    nodes: [
      { id: "taklamakan", label: "Taklamakan Desert (塔克拉玛干)", role: "Primary Source", x: 120, y: 320, baseFlux: 4200, category: "source" },
      { id: "kumtag", label: "Kumtag Desert (库姆塔格)", role: "Source", x: 230, y: 280, baseFlux: 3100, category: "source" },
      { id: "badain_jaran", label: "Badain Jaran Desert (巴丹吉林)", role: "Primary Source", x: 380, y: 190, baseFlux: 3800, category: "source" },
      { id: "tengger", label: "Tengger Desert (腾格里)", role: "Source", x: 440, y: 250, baseFlux: 2900, category: "source" },
      { id: "gobi_mongolia", label: "Gobi Desert Mongolia (蒙古戈壁)", role: "Transboundary Source", x: 490, y: 110, baseFlux: 3900, category: "source" },
      
      { id: "hexi_corridor", label: "Hexi Corridor Gateway (河西走廊)", role: "Choke Point", x: 340, y: 270, baseFlux: 2400, category: "bottleneck" },
      { id: "hulan_buh", label: "Ulan Buh Desert (乌兰布和)", role: "Transport Steppe", x: 520, y: 220, baseFlux: 2100, category: "corridor" },
      { id: "loess_plateau", label: "Loess Plateau (黄土高原)", role: "Secondary Emission & Transit", x: 500, y: 320, baseFlux: 1650, category: "corridor" },
      { id: "hebei_corridor", label: "Zhangjiakou Gate (张家口风口)", role: "North China Gate", x: 670, y: 190, baseFlux: 1450, category: "bottleneck" },
      { id: "qinling_barrier", label: "Qinling Mountain Breach (秦岭豁口)", role: "Basin Infiltration Point", x: 480, y: 400, baseFlux: 820, category: "bottleneck" },

      { id: "beijing_receptor", label: "Beijing / Bohai Rim (华北城市群)", role: "Downstream Receptor", x: 740, y: 220, baseFlux: 1420, category: "receptor" },
      { id: "sichuan_basin", label: "Sichuan Basin / Chengdu (四川盆地)", role: "120h Deep Receptor", x: 460, y: 490, baseFlux: 780, category: "receptor" },
      { id: "central_china", label: "Central Plains (中原地区)", role: "Downstream Receptor", x: 640, y: 340, baseFlux: 950, category: "receptor" },
      { id: "korean_peninsula", label: "Yellow Sea & Beyond (跨国输送)", role: "Transboundary Inflow", x: 860, y: 260, baseFlux: 480, category: "receptor" }
    ],
    links: [
      { source: "taklamakan", target: "kumtag", weight: 0.88, distanceKm: 580, transitHours: 18 },
      { source: "kumtag", target: "hexi_corridor", weight: 0.94, distanceKm: 420, transitHours: 14 },
      { source: "badain_jaran", target: "hexi_corridor", weight: 0.91, distanceKm: 310, transitHours: 10 },
      { source: "badain_jaran", target: "tengger", weight: 0.85, distanceKm: 260, transitHours: 8 },
      { source: "tengger", target: "loess_plateau", weight: 0.89, distanceKm: 340, transitHours: 12 },
      { source: "gobi_mongolia", target: "hulan_buh", weight: 0.92, distanceKm: 460, transitHours: 16 },
      { source: "gobi_mongolia", target: "hebei_corridor", weight: 0.87, distanceKm: 620, transitHours: 22 },
      { source: "hexi_corridor", target: "loess_plateau", weight: 0.96, distanceKm: 390, transitHours: 15 },
      { source: "loess_plateau", target: "hebei_corridor", weight: 0.82, distanceKm: 510, transitHours: 20 },
      { source: "hebei_corridor", target: "beijing_receptor", weight: 0.98, distanceKm: 180, transitHours: 6 },
      { source: "loess_plateau", target: "qinling_barrier", weight: 0.79, distanceKm: 310, transitHours: 14 },
      { source: "qinling_barrier", target: "sichuan_basin", weight: 0.84, distanceKm: 390, transitHours: 28 }, // 120h benchmark breach
      { source: "loess_plateau", target: "central_china", weight: 0.86, distanceKm: 440, transitHours: 18 },
      { source: "beijing_receptor", target: "korean_peninsula", weight: 0.73, distanceKm: 720, transitHours: 32 }
    ]
  };

  // 6. TRAINING & PHYSICS CONVERGENCE TELEMETRY (100 EPOCHS MOCK LOGS)
  const TRAINING_TELEMETRY = [];
  for (let ep = 1; ep <= 100; ep++) {
    const decay = Math.exp(-ep / 22);
    const dataMse = 0.012 + 0.185 * decay + (Math.sin(ep * 0.4) * 0.001);
    const pinnMassLoss = 0.0008 + 0.045 * Math.exp(-ep / 18) + (Math.cos(ep * 0.3) * 0.0004);
    const pinnSaltationLoss = 0.0015 + 0.068 * Math.exp(-ep / 20) + (Math.sin(ep * 0.5) * 0.0005);
    const totalLoss = dataMse + 0.25 * pinnMassLoss + 0.35 * pinnSaltationLoss;
    const valRmse = 24.2 + 88.5 * decay;
    const threatScore = 0.52 + (1 - decay) * 0.395 - (ep > 80 ? 0.005 * Math.random() : 0);
    const saltationViolations = Math.max(0, Math.floor(840 * Math.exp(-ep / 14) + (100 - ep) * 0.2));

    TRAINING_TELEMETRY.push({
      epoch: ep,
      totalLoss: Number(totalLoss.toFixed(5)),
      dataMse: Number(dataMse.toFixed(5)),
      pinnMassLoss: Number(pinnMassLoss.toFixed(5)),
      pinnSaltationLoss: Number(pinnSaltationLoss.toFixed(5)),
      valRmse: Number(valRmse.toFixed(2)),
      threatScore: Number(threatScore.toFixed(3)),
      saltationViolations: saltationViolations,
      learningRate: Number((0.0005 * Math.pow(0.5, Math.floor(ep / 25))).toFixed(6))
    });
  }

  // 7. COMPREHENSIVE MULTI-MODEL BENCHMARK MATRIX (DAYS 1 TO 15)
  const MODEL_BENCHMARKS = [
    {
      leadTime: "24h (Day 1)",
      models: {
        "AI-GAMFS (Coupled Deep)": { rmse: 28.4, mae: 18.2, threatScore: 0.912, far: 0.082, latencySec: 1.42 },
        "Main Line A (LightGBM/XGB)": { rmse: 35.8, mae: 23.5, threatScore: 0.865, far: 0.124, latencySec: 0.35 },
        "ECMWF IFS (Operational NWP)": { rmse: 52.1, mae: 38.6, threatScore: 0.742, far: 0.235, latencySec: 23400 },
        "CMA-GFS (CMA Physical NWP)": { rmse: 58.4, mae: 42.1, threatScore: 0.718, far: 0.261, latencySec: 21600 },
        "Baseline LSTM / ConvLSTM": { rmse: 44.2, mae: 31.0, threatScore: 0.814, far: 0.178, latencySec: 2.8 }
      }
    },
    {
      leadTime: "72h (Day 3)",
      models: {
        "AI-GAMFS (Coupled Deep)": { rmse: 41.5, mae: 28.4, threatScore: 0.864, far: 0.118, latencySec: 1.42 },
        "Main Line A (LightGBM/XGB)": { rmse: 58.2, mae: 41.0, threatScore: 0.785, far: 0.192, latencySec: 0.35 },
        "ECMWF IFS (Operational NWP)": { rmse: 88.6, mae: 64.2, threatScore: 0.612, far: 0.345, latencySec: 23400 },
        "CMA-GFS (CMA Physical NWP)": { rmse: 96.4, mae: 71.8, threatScore: 0.584, far: 0.380, latencySec: 21600 },
        "Baseline LSTM / ConvLSTM": { rmse: 72.8, mae: 53.2, threatScore: 0.698, far: 0.274, latencySec: 2.8 }
      }
    },
    {
      leadTime: "120h (Day 5 - Benchmark Horizon)",
      models: {
        "AI-GAMFS (Coupled Deep)": { rmse: 59.8, mae: 42.1, threatScore: 0.815, far: 0.154, latencySec: 1.42 },
        "Main Line A (LightGBM/XGB)": { rmse: 84.5, mae: 62.4, threatScore: 0.692, far: 0.278, latencySec: 0.35 },
        "ECMWF IFS (Operational NWP)": { rmse: 142.0, mae: 108.5, threatScore: 0.448, far: 0.485, latencySec: 23400 },
        "CMA-GFS (CMA Physical NWP)": { rmse: 158.2, mae: 121.0, threatScore: 0.412, far: 0.528, latencySec: 21600 },
        "Baseline LSTM / ConvLSTM": { rmse: 112.4, mae: 84.6, threatScore: 0.562, far: 0.385, latencySec: 2.8 }
      }
    },
    {
      leadTime: "168h (Day 7)",
      models: {
        "AI-GAMFS (Coupled Deep)": { rmse: 78.4, mae: 56.2, threatScore: 0.742, far: 0.215, latencySec: 1.42 },
        "Main Line A (LightGBM/XGB)": { rmse: 118.0, mae: 89.4, threatScore: 0.584, far: 0.384, latencySec: 0.35 },
        "ECMWF IFS (Operational NWP)": { rmse: 198.5, mae: 154.2, threatScore: 0.298, far: 0.635, latencySec: 23400 },
        "CMA-GFS (CMA Physical NWP)": { rmse: 224.0, mae: 172.5, threatScore: 0.264, far: 0.672, latencySec: 21600 },
        "Baseline LSTM / ConvLSTM": { rmse: 154.8, mae: 119.2, threatScore: 0.428, far: 0.495, latencySec: 2.8 }
      }
    },
    {
      leadTime: "240h (Day 10)",
      models: {
        "AI-GAMFS (Coupled Deep)": { rmse: 104.2, mae: 76.5, threatScore: 0.648, far: 0.295, latencySec: 1.42 },
        "Main Line A (LightGBM/XGB)": { rmse: 154.2, mae: 118.0, threatScore: 0.462, far: 0.492, latencySec: 0.35 },
        "ECMWF IFS (Operational NWP)": { rmse: 268.4, mae: 210.0, threatScore: 0.165, far: 0.785, latencySec: 23400 },
        "CMA-GFS (CMA Physical NWP)": { rmse: 295.0, mae: 232.0, threatScore: 0.138, far: 0.824, latencySec: 21600 },
        "Baseline LSTM / ConvLSTM": { rmse: 205.0, mae: 162.0, threatScore: 0.310, far: 0.620, latencySec: 2.8 }
      }
    },
    {
      leadTime: "360h (Day 15 - Extended Range)",
      models: {
        "AI-GAMFS (Coupled Deep)": { rmse: 135.0, mae: 98.4, threatScore: 0.545, far: 0.382, latencySec: 1.42 },
        "Main Line A (LightGBM/XGB)": { rmse: 198.5, mae: 152.0, threatScore: 0.342, far: 0.610, latencySec: 0.35 },
        "ECMWF IFS (Operational NWP)": { rmse: 345.0, mae: 275.0, threatScore: 0.082, far: 0.895, latencySec: 23400 },
        "CMA-GFS (CMA Physical NWP)": { rmse: 382.0, mae: 305.0, threatScore: 0.065, far: 0.925, latencySec: 21600 },
        "Baseline LSTM / ConvLSTM": { rmse: 262.0, mae: 208.0, threatScore: 0.215, far: 0.742, latencySec: 2.8 }
      }
    }
  ];

  // 8. GLOBAL SHAP FEATURE IMPORTANCE DISTRIBUTION
  const GLOBAL_SHAP_FEATURES = [
    { rank: 1, name: "Surface Friction Velocity (u*)", category: "Micro-meteorology", meanShap: 0.285, unit: "m/s", importancePct: 24.8, description: "Direct aerodynamic shear driving dust particle saltation lifting" },
    { rank: 2, name: "10m Horizontal Wind Speed (u10, v10)", category: "Dynamic NWP", meanShap: 0.218, unit: "m/s", importancePct: 19.0, description: "Large-scale advection velocity carrying dust plumes downstream" },
    { rank: 3, name: "Volumetric Soil Water Layer 1 (0-7cm)", category: "Land Surface", meanShap: 0.174, unit: "m³/m³", importancePct: 15.2, description: "Capillary moisture cohesion inhibiting particle dislodgement" },
    { rank: 4, name: "Upstream Advection Plume AOD (550nm)", category: "Satellite Sensor", meanShap: 0.142, unit: "AOD", importancePct: 12.4, description: "Optical thickness of incoming dust cloud from western desert sources" },
    { rank: 5, name: "Planetary Boundary Layer Height (BLH)", category: "Thermodynamic", meanShap: 0.108, unit: "m", importancePct: 9.4, description: "Vertical convective mixing volume diluting or capping ground PM10" },
    { rank: 6, name: "500 hPa Geopotential Height Gradient", category: "Synoptic Scale", meanShap: 0.086, unit: "dam/100km", importancePct: 7.5, description: "Upper-tropospheric trough baroclinicity and cold-front propagation" },
    { rank: 7, name: "Surface Air Temperature Deficit (Cold Surge)", category: "Thermodynamic", meanShap: 0.062, unit: "K", importancePct: 5.4, description: "Density current wedge lifting warm desert boundary air" },
    { rank: 8, name: "Vegetation Index (MODIS NDVI)", category: "Land Surface", meanShap: 0.045, unit: "[-0.2, 0.9]", importancePct: 3.9, description: "Surface roughness element density absorbing wind shear energy" },
    { rank: 9, name: "2m Relative Humidity (RH)", category: "Atmospheric State", meanShap: 0.028, unit: "%", importancePct: 2.4, description: "Electrostatic aggregation and hygroscopic particle growth" }
  ];

  // 9. COST-SENSITIVE CONFUSION MATRIX & ASYMMETRIC LOSS WEIGHTS
  const COST_MATRIX = {
    classes: ["Clean", "Floating Dust", "Blowing Sand", "Sandstorm", "Severe Sandstorm"],
    matrixSample: [
      [18420, 312, 45, 8, 0],
      [280, 4820, 210, 32, 2],
      [38, 195, 2140, 115, 12],
      [5, 24, 98, 920, 45],
      [0, 2, 11, 38, 384]
    ],
    misclassificationPenalties: {
      "Severe Missed as Clean": 100.0,
      "Severe Missed as Floating": 50.0,
      "Sandstorm Missed as Clean": 40.0,
      "False Alarm (Clean predicted as Sandstorm)": 2.5
    },
    threatScoreMacro: 0.815,
    criticalSuccessIndex: 0.782,
    detectionRate: 0.941
  };

  // EXPORT COMPLETE API OBJECT
  return {
    SYSTEM_SPEC,
    INPUT_TENSORS,
    ARCHITECTURE_LAYERS,
    FORECAST_STATIONS,
    CORRIDOR_GRAPH_DATA,
    TRAINING_TELEMETRY,
    MODEL_BENCHMARKS,
    GLOBAL_SHAP_FEATURES,
    COST_MATRIX,

    // HELPER FUNCTIONS FOR INTERACTIVE SIMULATIONS
    calculatePhysicsResidual: function (uStar, uStarT, soilMoisture) {
      const density = 1.225; // kg/m3
      const g = 9.81; // m/s2
      const C = 2.61; // empirical saltation constant
      const saltationActive = uStar > uStarT;
      const flux = saltationActive ? (C * (density / g) * Math.pow(uStar, 3) * (1 - (Math.pow(uStarT, 2) / Math.pow(uStar, 2)))) : 0;
      const moistureDamping = Math.exp(-15 * soilMoisture);
      const effectiveFlux = flux * moistureDamping * 1000; // in mg/m2*s
      const shearRatio = uStar / (uStarT || 0.001);
      const massBalanceError = Math.abs(shearRatio > 1 ? (Math.sin(shearRatio * 2) * 0.002) : 0.0003);
      const pinnLoss = (effectiveFlux > 0 ? (0.0012 + massBalanceError * 0.4) : 0.0004);

      return {
        saltationActive,
        shearRatio: Number(shearRatio.toFixed(2)),
        saltationFluxMg: Number(effectiveFlux.toFixed(2)),
        massBalanceError: Number(massBalanceError.toFixed(5)),
        pinnLoss: Number(pinnLoss.toFixed(5)),
        status: saltationActive ? "⚡ Saltation Triggered (u* > u*t)" : "🛡️ Aerodynamic Quiescence (Sub-threshold)"
      };
    },

    getStationById: function (id) {
      return FORECAST_STATIONS.find(s => s.id === id) || FORECAST_STATIONS[0];
    },

    getLayerById: function (id) {
      return ARCHITECTURE_LAYERS.find(l => l.id === id) || ARCHITECTURE_LAYERS[0];
    }
  };
})();
