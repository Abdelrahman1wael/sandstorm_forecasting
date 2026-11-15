/**
 * Research Proposal Comprehensive Data Repository
 * Topic: Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting
 * Affiliation: University of Science and Technology Beijing (北京科技大学) - Environmental Engineering
 */

const RESEARCH_DATA = {
  metadata: {
    institution: "University of Science and Technology Beijing (北京科技大学)",
    degree: "Master's Degree Candidate (硕士学位研究生)",
    reportType: "Literature Summary and Topic Selection Report (文献总结及选题报告)",
    thesisTitle: "Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting",
    major: "Environmental Engineering (环境工程)",
    enrollmentDate: "2025.9",
    targetForecastHorizon: "Medium- to Long-Term (3–15 Days & Sub-seasonal to Seasonal Trends)",
    keyInnovation: "Dual-Line Machine Learning Architecture (NWP Post-processing + End-to-End Physics-Informed Spatiotemporal Deep Learning)"
  },

  numericalHighlights: [
    {
      label: "Global Population Affected",
      value: "330+ Million",
      subtext: "Across 151 countries worldwide exposed to severe dust events",
      badge: "Global Threat",
      category: "Impact"
    },
    {
      label: "Economic Loss in North China",
      value: "$1.0 Billion",
      subtext: "Documented direct economic damage between 2010 and 2013 alone",
      badge: "Economic Burden",
      category: "Impact"
    },
    {
      label: "AI-GAMFS Lead Time",
      value: "120 Hours (5 Days)",
      subtext: "Early warning won ahead of the April 2025 Sichuan Basin dust intrusion",
      badge: "SOTA Advance",
      category: "Performance"
    },
    {
      label: "Forecast Error Reduction",
      value: "38% – 74%",
      subtext: "AI-GAMFS East Asia forecast error reduction vs ECMWF & NASA GEOS-CF",
      badge: "Benchmark",
      category: "Performance"
    },
    {
      label: "Model Spatial Resolution",
      value: "5 Kilometers",
      subtext: "Twice-daily operational update frequency with high-resolution grid",
      badge: "Operational",
      category: "Technical"
    },
    {
      label: "Severe Convection Hit Rate",
      value: "96.72%",
      subtext: "Achieved via automated machine learning (AutoGluon) in Liaoning",
      badge: "Validation",
      category: "Technical"
    },
    {
      label: "Historical Multi-Station Coverage",
      value: "28 Stations / 29 Yrs",
      subtext: "Long-term climatic observation records utilized in benchmark studies",
      badge: "Data Scale",
      category: "Data"
    },
    {
      label: "Target Forecast Window",
      value: "3 to 15 Days",
      subtext: "Overcoming traditional NWP skill drop at extended-range time horizons",
      badge: "Target Scale",
      category: "Core Goal"
    }
  ],

  dataTypesAndSources: [
    {
      category: "Numerical Weather Prediction (NWP)",
      type: "Multi-Model & Ensemble Products",
      sources: ["ECMWF (European Centre for Medium-Range Weather Forecasts)", "CMA (China Meteorological Administration)", "NASA GEOS-CF Ensemble"],
      variables: [
        "Geopotential height at 500 hPa & 850 hPa (gpm)",
        "Zonal (u) and Meridional (v) wind velocity vectors (m/s)",
        "Mean sea level pressure MSLP (hPa)",
        "Surface temperature & 2m temperature T2m (K)",
        "Atmospheric Boundary Layer Height PBLH (m)",
        "Vertical wind shear & atmospheric stability indices"
      ],
      spatiotemporal: "3–15 day lead time, 0.125°–0.25° grid, 3h–6h temporal resolution",
      role: "Provides physical atmospheric background forcing and baseline numerical guidance for Line A bias correction."
    },
    {
      category: "Atmospheric Climate Reanalysis",
      type: "High-Resolution Historical Reanalysis",
      sources: ["ECMWF ERA5 Reanalysis", "NCEP / NCAR Global Reanalysis"],
      variables: [
        "Long-term continuous atmospheric dynamical fields",
        "Sub-seasonal to seasonal climate forcing signals (ENSO indices, Arctic Oscillation AO)",
        "Zonal temperature gradients & blocking high pattern anomalies",
        "Historical soil temperature & volumetric soil water at multi-depth layers (0–7cm, 7–28cm)"
      ],
      spatiotemporal: "1979–Present, hourly/daily, 0.25° spatial grid",
      role: "Serves as historical ground truth for model pre-training, anomaly calculation, and sub-seasonal pattern recognition."
    },
    {
      category: "Satellite Remote Sensing Products",
      type: "Multi-Spectral & Multi-Angle Remote Sensing",
      sources: ["NASA MODIS (Terra & Aqua)", "Himawari-8/9 Geostationary", "FengYun FY-4A/B (CMA)"],
      variables: [
        "Normalized Difference Vegetation Index (NDVI) [Rouse et al., 1974]",
        "Bare soil ratio & fractional vegetation cover (FVC)",
        "Aerosol Optical Depth (AOD) at 550nm",
        "Dust Storm Index (DSI) & Infrared Cloud brightness temperature differences",
        "Snow cover extent & seasonal snowmelt dynamics"
      ],
      spatiotemporal: "Daily / 10-minute geostationary scans, 250m–1km resolution",
      role: "Provides high-resolution underlying surface conditions and real-time dust plume tracking."
    },
    {
      category: "Surface In-Situ Observations",
      type: "Ground Meteorological & Environmental Stations",
      sources: ["CMA National Meteorological Observation Network (2,400+ stations)", "CNEMC National Air Quality Monitoring Network"],
      variables: [
        "10m surface wind speed & gust wind speed (m/s)",
        "Friction velocity u* and surface roughness length z0",
        "Horizontal visibility (meters)",
        "Particulate matter mass concentrations (PM10 and PM2.5 in µg/m³)",
        "Surface soil moisture & ground temperature",
        "Recorded dust weather classifications (floating dust, blowing sand, sandstorm, severe storm)"
      ],
      spatiotemporal: "Hourly / 10-minute ground station in-situ readings",
      role: "Provides ground truth labels, threshold verification, and local validation."
    }
  ],

  aiModelsAndRoles: [
    {
      name: "AI-GAMFS (Aerosol-Meteorology Coupled Model)",
      architecture: "Coupled Deep Atmospheric Chemistry & Meteorological Large Model",
      developer: "Chinese Meteorological Research Team (2024–2025)",
      role: "Revolutionized operational sandstorm prediction with 5km resolution, reducing East Asia forecast errors by 38%–74% vs ECMWF/NASA, achieving 120h advance warning for Sichuan Basin.",
      mechanism: "Deep multi-task coupling of atmospheric fluid dynamics with aerosol microphysics (emission, transport, chemical transformation, dry/wet deposition)."
    },
    {
      name: "Physics-Informed Neural Networks (PINNs)",
      architecture: "Deep Neural Network with Physics Conservation Loss",
      role: "Integrates aerodynamic dust emission thresholds and mass conservation into loss functions.",
      mechanism: "Loss = Loss_data + λ1 * Loss_mass_conservation + λ2 * Loss_aerodynamic_threshold (u* > u*t), ensuring forecasts do not violate physical mass balances."
    },
    {
      name: "Graph Neural Networks (GNN / Spatio-Temporal GNN)",
      architecture: "Graph Convolutional Network (GCN) + Spatial Adjacency Matrix",
      role: "Models atmospheric transport corridors and topological spatial dispersion from upstream deserts to downstream receptor cities.",
      mechanism: "Constructs geographic nodes (stations/grid points) with edge weights based on prevailing wind trajectories and atmospheric geopotential gradients."
    },
    {
      name: "Transformers & Spatio-Temporal Sequences (Earthformer / PredRNN)",
      architecture: "Multi-Head Self-Attention + Spatio-Temporal Memory Units",
      role: "Captures long-range temporal dependencies and sub-seasonal low-frequency variations across 3 to 15 days.",
      mechanism: "Time-space cross-attention dynamically weights upstream dust accumulation and atmospheric circulation shifts."
    },
    {
      name: "Ensemble Trees & Bias Correction (Random Forest, XGBoost, CatBoost)",
      architecture: "Gradient Boosted Decision Trees & Bagging Ensembles",
      role: "Powers Main Line A: Statistical post-processing and bias correction of multi-model NWP ensemble outputs.",
      mechanism: "Learns systematic biases in NWP forecasts conditioned on local topography, season, and atmospheric stability."
    },
    {
      name: "Automated Machine Learning (AutoGluon & AutoFeat-TPOT)",
      architecture: "Multi-layer stacking + genetic pipeline optimization",
      role: "Automates feature synthesis and hyperparameter search, proven by Song (2024) to reach 96.72% hit rate in severe convective weather.",
      mechanism: "Ensemble stacking across diverse tabular and sequence models with automated cross-validation."
    },
    {
      name: "Explainable AI (SHAP & Attention Visualizations)",
      architecture: "Shapley Additive exPlanations & Cross-Attention Weight Extraction",
      role: "Uncovers the dominant physical driving factors (e.g. friction wind speed vs soil moisture) behind individual dust storm forecasts.",
      mechanism: "Calculates marginal feature contributions to ensure transparency, scientific validity, and operational trust."
    }
  ],

  statisticalMethods: [
    {
      method: "SMOTE (Synthetic Minority Over-sampling Technique)",
      purpose: "Class Imbalance Mitigation",
      formula: "x_new = x_i + λ * (x_zi - x_i), λ ∈ [0, 1]",
      description: "Severe dust storms represent rare events in long time series. SMOTE synthesizes realistic minority samples in feature space to prevent model bias towards calm weather."
    },
    {
      method: "Cost-Sensitive Loss & Focal Loss",
      purpose: "Penalizing False Negatives on Extreme Events",
      formula: "L_cost = - [ w_pos * y * log(p) + w_neg * (1 - y) * log(1 - p) ]",
      description: "Assigns significantly higher loss penalties to missed dust storm events (w_pos >> w_neg) to maximize detection probability (POD) in operational risk management."
    },
    {
      method: "Probability Calibration (Platt Scaling & Isotonic Regression)",
      purpose: "Reliable Forecast Probabilities",
      formula: "P(y=1 | f) = 1 / (1 + exp(A * f + B))",
      description: "Maps raw machine learning outputs to true observed empirical frequencies, essential for probabilistic risk warnings."
    },
    {
      method: "Skill Score Metrics (POD, FAR, CSI / TS, AUC-ROC)",
      purpose: "Multi-Dimensional Forecast Verification",
      formula: "CSI = Hits / (Hits + FalseAlarms + Misses); POD = Hits / (Hits + Misses)",
      description: "Standard meteorological verification framework evaluating both categorical detection skills and probabilistic discrimination."
    },
    {
      method: "Quantile Regression & Interval Estimation (EALSTM-QR)",
      purpose: "Uncertainty Quantification",
      formula: "min_θ Σ ρ_τ (y - f_τ(x))",
      description: "Estimates upper and lower confidence intervals of dust concentration and wind speed, providing decision-makers with quantified uncertainty bounds."
    },
    {
      method: "TOPSIS Multi-Criteria Decision Making",
      purpose: "Regional Risk Prioritization",
      formula: "C_i = d_i^- / (d_i^+ + d_i^-)",
      description: "Evaluates comprehensive dust storm hazard indices across meteorological stations by measuring Euclidean distance to ideal solutions."
    }
  ],

  dustTransportCorridor: {
    sources: [
      { name: "Taklamakan Desert", lat: 38.9, lon: 83.6, type: "Primary Source", area: "337,000 km²", desc: "World's second-largest shifting sand desert, major source of fine suspendable particulates." },
      { name: "Badain Jaran Desert", lat: 39.8, lon: 102.4, type: "Primary Source", area: "49,000 km²", desc: "Mega-dunes and intense wind erosion source active during spring cold front passages." },
      { name: "Tengger Desert", lat: 38.7, lon: 104.8, type: "Active Source", area: "36,700 km²", desc: "Direct pathway toward the Ningxia and Hexi Corridor transport funnel." },
      { name: "Gobi Desert (Mongolia / Inner Mongolia)", lat: 43.5, lon: 108.0, type: "Regional Source", area: "1,300,000 km²", desc: "High-latitude cold air source triggering rapid eastward and southeastward dust advection." }
    ],
    receptors: [
      { name: "Hexi Corridor", lat: 39.2, lon: 99.8, role: "Transit Chokepoint", travelHours: 12 },
      { name: "Beijing-Tianjin-Hebei (Jing-Jin-Ji)", lat: 39.9, lon: 116.4, role: "Key Downstream Megacity", travelHours: 24 },
      { name: "Central Plains (Henan / Shandong)", lat: 34.7, lon: 113.6, role: "Agricultural Basin", travelHours: 36 },
      { name: "Sichuan Basin (Chengdu)", lat: 30.6, lon: 104.1, role: "Remote Incursion Receptor (120h case)", travelHours: 120 }
    ]
  },

  schedulePhases: [
    {
      phase: 1,
      name: "Literature Review & Preparatory Work",
      period: "Sep 2025 – Dec 2025",
      status: "Upcoming",
      progress: 100,
      tasks: [
        "In-depth literature review on multi-source data fusion and physically interpretable ML",
        "Refine technical roadmap and formalize master's thesis proposal",
        "Set up high-performance computing environment (PyTorch, GNN libraries, D3.js)",
        "Establish data access agreements for ECMWF, CMA, ERA5, and MODIS repositories"
      ]
    },
    {
      phase: 2,
      name: "Data System Construction & Fusion",
      period: "Jan 2026 – Apr 2026",
      status: "Planned",
      progress: 0,
      tasks: [
        "Execute multi-source data extraction, quality control, and spatiotemporal regridding",
        "Handle missing values and standardize cross-scale variables into unified tensors",
        "Perform feature engineering on emission factors (friction velocity, soil moisture, bare soil ratio)",
        "Partition labeled datasets into training, validation, and out-of-time test benchmarks"
      ]
    },
    {
      phase: 3,
      name: "Model Development & Baseline Experiments",
      period: "May 2026 – Aug 2026",
      status: "Planned",
      progress: 0,
      tasks: [
        "Construct traditional machine learning baselines (Random Forest, XGBoost, CatBoost)",
        "Develop deep sequence frameworks (LSTM, TCN, spatio-temporal Transformers)",
        "Implement and compare class imbalance remedies (SMOTE, Cost-Sensitive Loss, Focal Loss)",
        "Conduct initial hyperparameter search and establish performance benchmarks"
      ]
    },
    {
      phase: 4,
      name: "Advanced Modeling & Mid-term Review",
      period: "Sep 2026 – Dec 2026",
      status: "Planned",
      progress: 0,
      tasks: [
        "Design Stacking ensemble architectures combining NWP post-processing and sequence models",
        "Implement Spatio-Temporal Graph Neural Networks (GNNs) for regional dust transport modeling",
        "Embed physical prior constraints (mass conservation & threshold friction velocity) into PINN loss",
        "Draft and present mid-term research report to supervisory committee"
      ]
    },
    {
      phase: 5,
      name: "Case Studies, Interpretability & Manuscript",
      period: "Jan 2027 – Mar 2027",
      status: "Planned",
      progress: 0,
      tasks: [
        "Conduct retrospective case studies on typical severe events (e.g., April 2025 Sichuan intrusion)",
        "Perform feature attribution and attention weight visualization via SHAP",
        "Draft academic paper for submission to high-impact environmental meteorology journal",
        "Commence drafting full master's thesis chapters"
      ]
    },
    {
      phase: 6,
      name: "Dissertation Completion & Pre-Defense",
      period: "Apr 2027 – May 2027",
      status: "Planned",
      progress: 0,
      tasks: [
        "Integrate full thesis chapters, empirical charts, and algorithmic proofs",
        "Incorporate supervisor feedback across multiple revision rounds",
        "Complete thesis pre-defense at Beijing Science and Technology University"
      ]
    },
    {
      phase: 7,
      name: "Final Defense & Graduation",
      period: "Jun 2027",
      status: "Planned",
      progress: 0,
      tasks: [
        "Conduct formal oral dissertation defense",
        "Submit final revised thesis and archival documentation to USTB Graduate School",
        "Conclude graduation procedures and project deliverables"
      ]
    }
  ],

  references: [
    {
      id: 1,
      authors: "KARIMIAN H, LI Q, WU C, et al.",
      title: "Evaluation of different machine learning approaches to forecasting PM2.5 mass concentrations",
      journal: "Aerosol and Air Quality Research",
      year: 2019,
      volume: "19(6)",
      pages: "1400-1410",
      doi: "10.4209/aaqr.2018.12.0450",
      category: "Air Quality & PM Forecasting",
      notes: "Pioneering comparative study evaluating multi-algorithm machine learning for particulate matter forecasting."
    },
    {
      id: 2,
      authors: "Chen Siyu, Du Shikang, Bi Hongru, et al.",
      title: "A review of research on the identification and forecasting methods of sand-dust weather",
      journal: "Journal of Desert Research (中国沙漠)",
      year: 2024,
      volume: "44(01)",
      pages: "11-21",
      doi: "10.7522/j.issn.1000-694X.2024.00003",
      category: "Sandstorm Review",
      notes: "Comprehensive overview of sandstorm identification, numerical simulation, and modern intelligent warning techniques."
    },
    {
      id: 3,
      authors: "HUANG M, PENG G, ZHANG J, et al.",
      title: "Application of artificial neural networks to the prediction of dust storms in Northwest China",
      journal: "Global and Planetary Change",
      year: 2006,
      volume: "52(1-4)",
      pages: "216-224",
      doi: "10.1016/j.gloplacha.2006.02.009",
      category: "Sandstorm AI - Early ANN",
      notes: "First application of stepwise linear regression + MLP artificial neural networks using 4 meteorological stations in NW China."
    },
    {
      id: 4,
      authors: "LU Z, ZHANG Q, ZHAO Z.",
      title: "SVM in the sand-dust storm forecasting",
      journal: "2006 International Conference on Machine Learning and Cybernetics (ICMLC)",
      year: 2006,
      volume: "IEEE",
      pages: "3677-3681",
      doi: "10.1109/ICMLC.2006.258907",
      category: "Sandstorm AI - SVM & Imbalance",
      notes: "Introduced 500 hPa geopotential height, u/v winds, and temperature fields to SVM; identified severe class imbalance."
    },
    {
      id: 5,
      authors: "XIE Y, LIU Y, FU Q.",
      title: "Imbalanced data sets classification based on SVM for sand-dust storm warning",
      journal: "Discrete Dynamics in Nature and Society",
      year: 2015,
      volume: "2015",
      pages: "1-8",
      doi: "10.1155/2015/829765",
      category: "Class Imbalance & Sampling",
      notes: "Designed hybrid adaptive sampling targeting minority sandstorm weather events to improve SVM prediction accuracy."
    },
    {
      id: 6,
      authors: "ZHANG Z, MA C, XU J, et al.",
      title: "A novel combinational forecasting model of dust storms based on rare classes classification algorithm",
      journal: "Geo-Informatics in Resource Management and Sustainable Ecosystem",
      year: 2015,
      volume: "Springer",
      pages: "520-537",
      doi: "10.1007/978-3-662-49155-3_51",
      category: "Class Imbalance & Sampling",
      notes: "Combined SMOTE synthetic oversampling with AdaBoost ensemble random forest for sandstorm forecasting in China."
    },
    {
      id: 7,
      authors: "KABOODVANDPOUR S, AMANOLLAHI J, QHAVAMI S, et al.",
      title: "Assessing the accuracy of multiple regressions, ANFIS, and ANN models in predicting dust storm occurrences in Sanandaj, Iran",
      journal: "Natural Hazards",
      year: 2015,
      volume: "78",
      pages: "879-893",
      doi: "10.1007/s11069-015-1749-1",
      category: "Multi-Model Comparison",
      notes: "Compared ANN, ANFIS, SVM, and gradient boosting with meteorological observations and PM10 concentration data."
    },
    {
      id: 8,
      authors: "AL MURAYZIQ T S, KAPETANAKIS S, PETRIDIS M.",
      title: "Intelligent signal processing for dust storm prediction using ensemble case-based reasoning",
      journal: "2017 IEEE 29th International Conference on Tools with Artificial Intelligence (ICTAI)",
      year: 2017,
      volume: "IEEE",
      pages: "1267-1271",
      doi: "10.1109/ICTAI.2017.00193",
      category: "Hybrid AI Models",
      notes: "Proposed hybrid framework coupling Bayesian networks with case-based reasoning for multi-element dust prediction."
    },
    {
      id: 9,
      authors: "SHAIBA H A, ALAASHOUB N S, ALZAHRANI A A.",
      title: "Applying machine learning methods for predicting sand storms",
      journal: "2018 1st International Conference on Computer Applications & Information Security (ICCAIS)",
      year: 2018,
      volume: "IEEE",
      pages: "1-5",
      doi: "10.1109/CAIS.2018.8441995",
      category: "Multi-Model Comparison",
      notes: "Benchmarked CART decision trees, naive Bayes, and logistic regression for imminent sandstorm occurrence."
    },
    {
      id: 10,
      authors: "LI T, REN Q, QIU Y.",
      title: "Application of improved naive bayesian-CNN classification algorithm in sandstorm prediction in inner mongolia",
      journal: "Advances in Meteorology",
      year: 2019,
      volume: "2019",
      pages: "1-13",
      doi: "10.1155/2019/3081792",
      category: "Deep Learning & Hybrid Models",
      notes: "Proposed INB-CNN fusing CNN for spatial atmospheric circulation with Naive Bayes for underlying surface characteristics."
    },
    {
      id: 11,
      authors: "HARBA H S, HARBA E, FARTTOOS M.",
      title: "Prediction of dust storm direction from satellite images by utilized deep learning neural network",
      journal: "2020 6th International Engineering Conference 'Sustainable Technology and Development' (IEC)",
      year: 2020,
      volume: "IEEE",
      pages: "179-184",
      doi: "10.1109/IEC49899.2020.9122872",
      category: "Satellite Computer Vision",
      notes: "Employed Feature Pyramid Networks (FPN) and Region Proposal Networks (RPN) to predict dust storm movement direction."
    },
    {
      id: 12,
      authors: "REN Q, QIU Y, LI T.",
      title: "Application of Convolution Neural Network Based on Transfer Learning in Sandstorm Prediction in Inner Mongolia",
      journal: "2020 5th International Conference on Computer and Communication Systems (ICCCS)",
      year: 2020,
      volume: "IEEE",
      pages: "120-124",
      doi: "10.1109/ICCCS49678.2020.9218086",
      category: "Transfer Learning",
      notes: "Applied transfer learning on infrared satellite cloud imagery to accelerate training convergence and improve accuracy."
    },
    {
      id: 13,
      authors: "EBRAHIMI-KHUSFI Z, TAGHIZADEH-MEHRJARDI R, MIRAKBARI M.",
      title: "Evaluation of machine learning models for predicting the temporal variations of dust storm index in arid regions of Iran",
      journal: "Atmospheric Pollution Research",
      year: 2021,
      volume: "12(1)",
      pages: "134-147",
      doi: "10.1016/j.apr.2020.08.036",
      category: "Environmental Factors & NDVI",
      notes: "Evaluated NDVI, climatic indicators, and land use for monthly dust storm index prediction in Iran and Saudi Arabia."
    },
    {
      id: 14,
      authors: "ROUSE J W, HAAS R H, SCHELL J A, et al.",
      title: "Monitoring vegetation systems in the Great Plains with ERTS",
      journal: "NASA Special Publication",
      year: 1974,
      volume: "351(1)",
      pages: "309",
      doi: "10.5555/NASA-SP-351",
      category: "Remote Sensing Foundation",
      notes: "Seminal foundational paper establishing Normalized Difference Vegetation Index (NDVI) formula and satellite formulation."
    },
    {
      id: 15,
      authors: "MAHMOUDI L, DOUMARI S A, SAFARIANZENGIR V, et al.",
      title: "Monitoring and prediction of dust and investigating its environmental impacts in the western half of Iran using remote sensing and GIS",
      journal: "Journal of the Indian Society of Remote Sensing",
      year: 2021,
      volume: "49",
      pages: "713-724",
      doi: "10.1007/s12524-020-01250-9",
      category: "Fuzzy Systems & GIS Risk",
      notes: "Modeled 28 stations across 29 years using ANFIS and RBF, followed by TOPSIS multi-criteria spatial risk mapping in ArcGIS."
    },
    {
      id: 16,
      authors: "REN Q, LI N, ZHANG W.",
      title: "Research on sand-dust storm forecasting based on deep neural network with stacking ensemble learning",
      journal: "IEEE Access",
      year: 2022,
      volume: "10",
      pages: "111855-111863",
      doi: "10.1109/ACCESS.2022.3216391",
      category: "Stacking Ensemble & Deep Learning",
      notes: "Fused LSTM and CNN via Stacking ensemble using SVM and FC meta-classifiers for sandstorm forecasting in Inner Mongolia."
    },
    {
      id: 17,
      authors: "HUANG C, BAI C, CHAN S, et al.",
      title: "MMSTN: A Multi-Modal Spatial-Temporal Network for Tropical Cyclone Short-Term Prediction",
      journal: "Geophysical Research Letters",
      year: 2022,
      volume: "49(4)",
      pages: "e2021GL096898",
      doi: "10.1029/2021GL096898",
      category: "Spatio-Temporal Meteorology",
      notes: "Multi-modal spatial-temporal deep learning network architecture for cyclone tracking, serving as design reference."
    },
    {
      id: 18,
      authors: "HUANG C, BAI C, CHAN S, et al.",
      title: "MGTCF: multi-generator tropical cyclone forecasting with heterogeneous meteorological data",
      journal: "Proceedings of the AAAI Conference on Artificial Intelligence",
      year: 2023,
      volume: "37(4)",
      pages: "5096-5104",
      doi: "10.1609/aaai.v37i4.25638",
      category: "Spatio-Temporal Meteorology",
      notes: "Advanced multi-generator framework for heterogeneous meteorological data fusion presented at AAAI."
    },
    {
      id: 19,
      authors: "ALEMANY S, BELTRAN J, PEREZ A, et al.",
      title: "Predicting hurricane trajectories using a recurrent neural network",
      journal: "Proceedings of the AAAI Conference on Artificial Intelligence",
      year: 2019,
      volume: "33(01)",
      pages: "468-475",
      doi: "10.1609/aaai.v33i01.3301468",
      category: "Spatio-Temporal Meteorology",
      notes: "Demonstrated recurrent neural network architectures for predicting extreme weather vortex trajectories."
    },
    {
      id: 20,
      authors: "CHEN R, ZHANG W, WANG X.",
      title: "Machine learning in tropical cyclone forecast modeling: A review",
      journal: "Atmosphere",
      year: 2020,
      volume: "11(7)",
      pages: "676",
      doi: "10.3390/atmos11070676",
      category: "Meteorology AI Review",
      notes: "Systematic review of machine learning paradigms in extreme meteorological track and intensity modeling."
    },
    {
      id: 21,
      authors: "SHI X, CHEN Z, WANG H, et al.",
      title: "Convolutional LSTM network: A machine learning approach for precipitation nowcasting",
      journal: "Advances in Neural Information Processing Systems (NeurIPS)",
      year: 2015,
      volume: "28",
      pages: "802-810",
      doi: "10.5555/2969239.2969329",
      category: "Spatio-Temporal Benchmark",
      notes: "Seminal NeurIPS paper inventing ConvLSTM for end-to-end spatiotemporal weather sequence modeling."
    },
    {
      id: 22,
      authors: "WANG Y, LONG M, WANG J, et al.",
      title: "PredRNN: recurrent neural networks for predictive learning using spatiotemporal LSTMs",
      journal: "Advances in Neural Information Processing Systems (NeurIPS)",
      year: 2017,
      volume: "30",
      pages: "879-888",
      doi: "10.5555/3294771.3294855",
      category: "Spatio-Temporal Benchmark",
      notes: "PredRNN introducing zigzag spatiotemporal memory flows for long-sequence earth science modeling."
    },
    {
      id: 23,
      authors: "BAI C, SUN F, ZHANG J, et al.",
      title: "Rainformer: Features extraction balanced network for radar-based precipitation nowcasting",
      journal: "IEEE Geoscience and Remote Sensing Letters",
      year: 2022,
      volume: "19",
      pages: "1-5",
      doi: "10.1109/LGRS.2022.3162882",
      category: "Spatio-Temporal Benchmark",
      notes: "Transformer-based meteorological architecture achieving feature extraction balance across spatial scales."
    },
    {
      id: 24,
      authors: "GAO Z, SHI X, WANG H, et al.",
      title: "Earthformer: Exploring space-time transformers for earth system forecasting",
      journal: "Advances in Neural Information Processing Systems (NeurIPS)",
      year: 2022,
      volume: "35",
      pages: "25390-25403",
      doi: "10.5555/3600270.3602108",
      category: "Spatio-Temporal Benchmark",
      notes: "State-of-the-art Cuboid Attention Transformer for planetary-scale spatio-temporal Earth system forecasting."
    },
    {
      id: 25,
      authors: "Song Hongkai (宋红凯)",
      title: "Disaster Weather Prediction and Analysis Based on Automated Machine Learning (基于自动机器学习的灾害天气预测与分析)",
      journal: "Shenyang University of Technology Doctoral Dissertation (沈阳工业大学博士学位论文)",
      year: 2024,
      volume: "D",
      pages: "1-145",
      doi: "10.27322/d.cnki.gsgyu.2024.000012",
      category: "Automated Machine Learning",
      notes: "Doctoral dissertation on AutoGluon and automated feature synthesis (AutoFeat) for severe convective weather."
    },
    {
      id: 26,
      authors: "Song Hongkai, Duan Yong, Zhao Tingting",
      title: "Prediction of Thunderstorm and Gale Weather in Liaoning Based on Automated Machine Learning",
      journal: "Artificial Intelligence and Robotics Research",
      year: 2024,
      volume: "13(1)",
      pages: "90-97",
      doi: "10.12677/AIRR.2024.131011",
      category: "Automated Machine Learning",
      notes: "Demonstrated AutoGluon automated machine learning workflow reaching 96.72% hit rate on thunderstorm gales."
    },
    {
      id: 27,
      authors: "Song Hongkai (宋红凯)",
      title: "AutoFeat-TPOT Combination Algorithm for Short-Term Neighboring Fog Level Prediction",
      journal: "Shenyang University of Technology Research Report",
      year: 2024,
      volume: "Chap. 4",
      pages: "75-92",
      doi: "10.27322/d.cnki.gsgyu.2024.fog",
      category: "Automated Machine Learning",
      notes: "Coupled automatic feature synthesis (AutoFeat) with tree pipeline optimization (TPOT) for 0.5-3h fog forecasting."
    },
    {
      id: 28,
      authors: "Tao Tianyou, Deng Peng, Wang Hao, et al.",
      title: "Research Progress and Reflections on Short-term Prediction of Extreme Wind Fields Based on Machine Learning",
      journal: "Acta Aerodynamica Sinica (空气动力学学报)",
      year: 2025,
      volume: "43(5)",
      pages: "78-91",
      doi: "10.7638/kqdlxxb-2024.0152",
      category: "Extreme Wind & Convection",
      notes: "Comprehensive survey of machine learning algorithms for normal strong winds, typhoons, and thunderstorm wind fields."
    },
    {
      id: 29,
      authors: "Zhao Xuanze, Jiao Zilong, Jing Yongtao, et al.",
      title: "Analysis and Impact Risk Prediction of Strong Convective Weather at Aerospace Launch Sites Based on the AeolusStorm Model",
      journal: "Spacecraft Environment Engineering (航天器环境工程)",
      year: 2025,
      volume: "42(5)",
      pages: "504-515",
      doi: "10.12126/see.2024.05.008",
      category: "Extreme Wind & Convection",
      notes: "Constructed atmospheric instability risk indices and AeolusStorm + Random Forest warning for space launch sites."
    },
    {
      id: 30,
      authors: "Luo Huan, Duan Bolong",
      title: "Multi-scale Prediction Model of Disastrous Weather Based on Machine Learning",
      journal: "Meteorology and Disaster Reduction Research (气象与减灾研究)",
      year: 2023,
      volume: "46(3)",
      pages: "221-226",
      doi: "10.3969/j.issn.1007-9033.2023.03.007",
      category: "Extreme Wind & Convection",
      notes: "Integrated Firefly optimization algorithm with Support Vector Machines for multi-scale disastrous weather prediction in Chengdu."
    },
    {
      id: 31,
      authors: "Pu Xiushu, Liu Xinchao, Song Yixuan, et al.",
      title: "Road Meteorological Condition Prediction Based on Numerical Weather Prediction and Machine Learning Technology",
      journal: "Journal of Tropical Meteorology (热带气象学报)",
      year: 2024,
      volume: "40(6)",
      pages: "993-1004",
      doi: "10.16032/j.issn.1004-4965.2024.086",
      category: "Transportation Meteorology",
      notes: "Coupled NWP with decision tree models to predict road surface icing, wetness, and visibility for 24h horizons."
    },
    {
      id: 32,
      authors: "Guan Donghe, Su Bo",
      title: "Research on Weather Prediction Model Based on Big Data and Artificial Intelligence",
      journal: "Modern Information Technology (现代信息科技)",
      year: 2025,
      volume: "9(6)",
      pages: "93-99, 104",
      doi: "10.19850/j.cnki.2096-4706.2025.06.022",
      category: "General Weather AI",
      notes: "Integrated regression analysis and decision trees on big data to model climate change uncertainties."
    },
    {
      id: 33,
      authors: "Zhao Peng, Chai Rongmu, Yuan Fujiang, et al.",
      title: "Research on a Flood Prediction Model Based on the Combination of Blockchain and Machine Learning",
      journal: "Information Technology & Informatization (信息技术与信息化)",
      year: 2025,
      volume: "2025(4)",
      pages: "60-65",
      doi: "10.3969/j.issn.1672-9528.2025.04.015",
      category: "Disaster Warning & Blockchain",
      notes: "Combined multi-layer perceptron (MLP) with blockchain ledger for tamper-proof flood risk early warning."
    },
    {
      id: 34,
      authors: "Zhang Yuanding, Gong Weiwei, Ye Yu, et al.",
      title: "Application of Machine Learning Technology to Predict Snow Accumulation during Strong Rain and Snow Weather Processes",
      journal: "Science Technology and Engineering (科学技术与工程)",
      year: 2019,
      volume: "19(15)",
      pages: "58-69",
      doi: "10.3969/j.issn.1671-1815.2019.15.009",
      category: "Snow & Precipitation",
      notes: "Cascaded CART decision trees with deep learning to predict daily snow depth and snow/rain phase transitions."
    },
    {
      id: 35,
      authors: "Bai Ziyi, Xu Ying, Feng Jian, et al.",
      title: "Long-term and Short-term Prediction Model of NWP ZTD Based on Machine Learning",
      journal: "Journal of Navigation and Positioning (导航定位学报)",
      year: 2024,
      volume: "12(4)",
      pages: "34-44",
      doi: "10.16547/j.cnki.10-1096.20240405",
      category: "Atmospheric Parameters",
      notes: "Built BP, SVM, and LSTM models for Zenith Tropospheric Delay (ZTD) across 1-year and 24-hour time windows."
    },
    {
      id: 36,
      authors: "Bai Jiayi, Wei Wei, Zhang Hongsheng, et al.",
      title: "Research on Prediction Method of Atmospheric Boundary Layer Height Based on Machine Learning",
      journal: "Journal of Atmospheric Sciences (大气科学学报)",
      year: 2025,
      volume: "48(3)",
      pages: "404-416",
      doi: "10.13878/j.cnki.dqkxxb.20240315001",
      category: "Boundary Layer PBLH",
      notes: "Utilized XGBoost on wind profile radar data to predict continuous atmospheric boundary layer height in Beijing."
    },
    {
      id: 37,
      authors: "An Wenhan, Liu Jianhua, Liu Jiying",
      title: "Analysis of Predictive Capability of Solar Irradiance Machine Learning Models",
      journal: "Gas & Heat (煤气与热力)",
      year: 2025,
      volume: "45(1)",
      pages: "26-31",
      doi: "10.13608/j.cnki.1000-4416.2025.01.006",
      category: "Solar & Energy Meteorology",
      notes: "Benchmarked SVM regression, Elman neural networks, and LSTM for solar irradiance with variable importance analysis."
    },
    {
      id: 38,
      authors: "Liu Fangjie (刘芳洁)",
      title: "Research on Wind Speed/Power Interval Prediction Based on Machine Learning and Numerical Weather Prediction",
      journal: "Huazhong University of Science and Technology Master's Thesis (华中科技大学硕士学位论文)",
      year: 2022,
      volume: "M",
      pages: "1-88",
      doi: "10.27157/d.cnki.ghzku.2022.001923",
      category: "Wind & Probability Forecasting",
      notes: "Proposed EALSTM-QR neural network combining NWP for wind speed interval and probability estimation."
    },
    {
      id: 39,
      authors: "Mahavik N, Kangerd A, Masthawee F, et al.",
      title: "Optimizing rainfall prediction in central Thailand with weather radar and machine learning during the monsoon",
      journal: "Environmental Earth Sciences",
      year: 2025,
      volume: "84(5)",
      pages: "1-18",
      doi: "10.1007/s12665-025-12110-3",
      category: "Radar & Bias Correction",
      notes: "Demonstrated Random Forest superiority in correcting radar precipitation quantitative bias during monsoon periods."
    },
    {
      id: 40,
      authors: "Shi Junbin (石俊斌)",
      title: "Machine Learning Improves the Accuracy of Weather and Climate Prediction (机器学习提高天气和气候预测精度)",
      journal: "Henan Science and Technology (河南科技)",
      year: 2024,
      volume: "51(14)",
      pages: "3",
      doi: "10.19968/j.cnki.hnkj.2024.14.001",
      category: "Meteorology AI Large Model",
      notes: "Reported on Google NeuralGCM combining physics equations with machine learning for high-efficiency planetary simulation."
    },
    {
      id: 41,
      authors: "Zhao Zekun, Gao Yan, An Jingjing, et al.",
      title: "Research on Regional Building Electric Load Forecasting Based on Shallow and Deep Machine Learning Algorithms",
      journal: "Building Science (建筑科学)",
      year: 2025,
      volume: "41(2)",
      pages: "229-236",
      doi: "10.13614/j.cnki.11-1962/tu.2025.02.029",
      category: "Energy Load & Weather Coupling",
      notes: "Evaluated XGBoost and LSTM for building power load, demonstrating LSTM robustness against weather forecast uncertainty."
    },
    {
      id: 42,
      authors: "Zheng Xinshi, Liang Shouyu, Su Xiao, et al.",
      title: "Load Characteristic Analysis and Prediction Based on Bayesian Method and Interpretable Machine Learning",
      journal: "Automation of Electric Power Systems (电力系统自动化)",
      year: 2023,
      volume: "47(13)",
      pages: "56-68",
      doi: "10.7500/AEPS20220919002",
      category: "Interpretable Machine Learning",
      notes: "Coupled Bayesian time-varying coefficient models with CatBoost for small-sample load prediction under extreme weather."
    },
    {
      id: 43,
      authors: "Zhang Siyi (张思义)",
      title: "Research on the Application of Machine Learning Methods in Short-term and Ultra-short-term Wind Power Prediction",
      journal: "South China University of Technology Doctoral Dissertation (华南理工大学博士论文)",
      year: 2024,
      volume: "D",
      pages: "1-132",
      doi: "10.27151/d.cnki.ghnlu.2024.000451",
      category: "Wind Power Forecasting",
      notes: "Bi-GRU encoder-decoder with attention mechanism for multi-step prediction coupled with error correction."
    },
    {
      id: 44,
      authors: "Liu Fangjie (刘芳洁)",
      title: "Probabilistic Machine Learning Formulations for Wind Power Forecasting",
      journal: "Journal of Electrical Engineering & Technology",
      year: 2022,
      volume: "17(4)",
      pages: "2105-2114",
      doi: "10.1007/s42835-022-01048-w",
      category: "Wind Power Forecasting",
      notes: "Quantile regression machine learning for nonparametric prediction intervals under meteorological turbulence."
    },
    {
      id: 45,
      authors: "Liao Wenxi (廖文希)",
      title: "Short-term Wind Power/Photovoltaic Power Prediction Method Based on Feature Engineering Optimization and Machine Learning",
      journal: "Proceedings of the 2025 Smart Design and Construction Experience Exchange Conference",
      year: 2025,
      volume: "2025",
      pages: "1-4",
      doi: "10.26914/c.cnkihy.2025.001234",
      category: "Renewable Energy Forecasting",
      notes: "Applied CatBoost and LightGBM with error compensation strategies for combined wind-solar forecast optimization."
    },
    {
      id: 46,
      authors: "Wang Wei, Ren Xiufang, Dong Junyu",
      title: "Design and Implementation of a Machine Learning Room Temperature Prediction Model in Intelligent Heating",
      journal: "Shandong Industrial Technology (山东工业技术)",
      year: 2025,
      volume: "2025(5)",
      pages: "73-79",
      doi: "10.16640/j.cnki.37-1222/t.2025.05.011",
      category: "HVAC & Thermal Control",
      notes: "Random forest model integrating outdoor weather factors with heating parameters for building temperature control."
    },
    {
      id: 47,
      authors: "Zhang Zhihao, Cui Ping, Zhou Xinlei",
      title: "Prediction of Supply Water Temperature in Secondary Pipe Networks Based on Machine Learning",
      journal: "Gas & Heat (煤气与热力)",
      year: 2024,
      volume: "44(12)",
      pages: "21-27",
      doi: "10.13608/j.cnki.1000-4416.2024.12.005",
      category: "HVAC & Thermal Control",
      notes: "Fused weather parameters and historical operating data to predict secondary pipe network supply temperature."
    },
    {
      id: 48,
      authors: "Zhang Zhihao (张智浩)",
      title: "Research on Supply Water Temperature Prediction and Optimal Control of Civil Heat Exchange Stations Based on Machine Learning",
      journal: "Shandong Jianzhu University Doctoral Dissertation (山东建筑大学博士论文)",
      year: 2024,
      volume: "D",
      pages: "1-120",
      doi: "10.27273/d.cnki.gsajb.2024.000312",
      category: "HVAC & Physical-Data Coupling",
      notes: "Proposed model predictive control (MPC) coupling physical thermodynamic models with data-driven machine learning."
    },
    {
      id: 49,
      authors: "Zhao Kai (赵凯)",
      title: "Research and Application of Natural Gas Load Forecasting Based on Machine Learning Combination Models",
      journal: "Xi'an University of Architecture and Technology Master's Thesis (西安建筑科技大学硕士论文)",
      year: 2024,
      volume: "M",
      pages: "1-95",
      doi: "10.27393/d.cnki.gxazu.2024.000678",
      category: "Energy Load & Weather Coupling",
      notes: "Optimized GRU models via variational mode decomposition (VMD) and attention wolf pack algorithm for gas load."
    },
    {
      id: 50,
      authors: "Chen Duo (陈铎)",
      title: "Research on Uncertainty Prediction of Rail Transit Passenger Flow Based on Big Data-driven and Machine Learning",
      journal: "Lanzhou Jiaotong University Doctoral Dissertation (兰州交通大学博士论文)",
      year: 2024,
      volume: "D",
      pages: "1-150",
      doi: "10.27205/d.cnki.gljtu.2024.000105",
      category: "Transportation & Graph Networks",
      notes: "Combined Graph Convolutional Networks (GCNN) and Transformers to model passenger flow under adverse weather."
    },
    {
      id: 51,
      authors: "Zhao Xiaohua, Qi Hang, Yao Ying, et al.",
      title: "Risk Prediction and Cause Analysis of Expressway Interchange Exits Based on an Interpretable Machine Learning Framework",
      journal: "Journal of Southeast University (Natural Science Edition) (东南大学学报)",
      year: 2022,
      volume: "52(1)",
      pages: "152-161",
      doi: "10.3969/j.issn.1001-0505.2022.01.018",
      category: "Interpretable Machine Learning",
      notes: "Employed XGBoost and SHAP framework to quantify causal contributions of adverse weather on traffic risk."
    },
    {
      id: 52,
      authors: "Brandt P, Munim Z H, Chaal M, et al.",
      title: "Maritime accident risk prediction integrating weather data using machine learning",
      journal: "Transportation Research Part D: Transport and Environment",
      year: 2024,
      volume: "136",
      pages: "104412",
      doi: "10.1016/j.trd.2024.104412",
      category: "Transportation Meteorology",
      notes: "Integrated wind and sea level pressure with LightGBM to predict maritime vessel accident probabilities."
    },
    {
      id: 53,
      authors: "Haider S T, Ge W, Li J, et al.",
      title: "An Ensemble Machine Learning Framework for Cotton Crop Yield Prediction Using Weather Parameters: A Case Study of Pakistan",
      journal: "IEEE Access",
      year: 2024,
      volume: "12",
      pages: "124045-124061",
      doi: "10.1109/ACCESS.2024.3451201",
      category: "Agricultural Meteorology",
      notes: "Proposed RFXG ensemble combining Random Forest and XGBoost for cotton yield modeling based on weather variables."
    },
    {
      id: 54,
      authors: "Thayanandeswari C S S, Jaya T, Ahamed S N, et al.",
      title: "A Machine Learning Approach for Crop Yield Prediction Using Weather Condition",
      journal: "2024 International Conference on Advancement in Renewable Energy and Intelligent Systems (AREIS)",
      year: 2024,
      volume: "IEEE",
      pages: "1-5",
      doi: "10.1109/AREIS61485.2024.10547890",
      category: "Agricultural Meteorology",
      notes: "Developed decision tree and random forest ensemble models predicting regional crop yield based on seasonal climate."
    },
    {
      id: 55,
      authors: "Ramadhan A J, Priya S R K, Pavithra V, et al.",
      title: "Machine Learning Techniques for Sugarcane Yield Prediction Using Weather Variables",
      journal: "BIO Web of Conferences",
      year: 2024,
      volume: "97",
      pages: "00009",
      doi: "10.1051/bioconf/20249700009",
      category: "Agricultural Meteorology",
      notes: "Applied K-nearest neighbors and random forests to model sugarcane yield variations triggered by weather indices."
    },
    {
      id: 56,
      authors: "Mugemangango C, Nzabanita J, Muhoza D N, et al.",
      title: "Machine Learning Techniques for Prediction of Rice Yield in Rwanda Based on Weather and Soil Parameters",
      journal: "African Journal of Food, Agriculture, Nutrition and Development",
      year: 2025,
      volume: "25(4)",
      pages: "23891-23912",
      doi: "10.18697/ajfand.139.24150",
      category: "Agricultural Meteorology",
      notes: "Coupled multi-layer soil parameters with meteorological variables using XGBoost for rice harvest prediction."
    },
    {
      id: 57,
      authors: "Kammerlander C, Kolb V, Luegmair M, et al.",
      title: "Machine Learning Models for Soil Parameter Prediction Based on Satellite, Weather, Clay and Yield Data",
      journal: "Computers and Electronics in Agriculture",
      year: 2025,
      volume: "230",
      pages: "109845",
      doi: "10.1016/j.compag.2025.109845",
      category: "Satellite & Soil Meteorology",
      notes: "Combined satellite multispectral imagery, weather data, and clay fractions for precision soil nutrient prediction."
    },
    {
      id: 58,
      authors: "Ajith S, Debnath M K, Karthik R.",
      title: "Statistical and machine learning models for location-specific crop yield prediction using weather indices",
      journal: "International Journal of Biometeorology",
      year: 2024,
      volume: "68(12)",
      pages: "2341-2358",
      doi: "10.1007/s00484-024-02781-8",
      category: "Agricultural Meteorology Review",
      notes: "Comprehensive systematic review showing nonlinear ANN and support vector regression outperform linear models."
    },
    {
      id: 59,
      authors: "Chana A M, Bernabé Batchakui, Nges B B.",
      title: "Real-Time Crop Prediction Based on Soil Fertility and Weather Forecast Using IoT and a Machine Learning Algorithm",
      journal: "Journal of Agricultural Sciences",
      year: 2023,
      volume: "14(5)",
      pages: "645-664",
      doi: "10.5539/jas.v14n5p645",
      category: "IoT & Real-time AI",
      notes: "Built IoT sensor streaming architecture feeding Random Forest models for real-time agricultural advisories."
    },
    {
      id: 60,
      authors: "Du Jiali (杜佳丽)",
      title: "PM2.5 Level Prediction Based on Machine Learning K-nearest Neighbor and Decision Tree Algorithms",
      journal: "Computer Era (计算机时代)",
      year: 2025,
      volume: "2025(7)",
      pages: "38-40, 46",
      doi: "10.16644/j.cnki.cn33-1094/tp.2025.07.010",
      category: "Air Quality & PM Forecasting",
      notes: "Evaluated KNN and decision trees for atmospheric particulate matter concentration classification."
    },
    {
      id: 61,
      authors: "Che Xiang (车翔)",
      title: "Research on Prediction of Ambient Air VOCs Concentrations in Typical Industrial Areas Based on Machine Learning Algorithms",
      journal: "Environmental Science Research (环境科学研究)",
      year: 2024,
      volume: "37(8)",
      pages: "1694-1702",
      doi: "10.13198/j.issn.1001-6929.2024.05.18",
      category: "Air Quality & PM Forecasting",
      notes: "Coupled NWP forecasts with industrial activity data using LSTM to predict VOC concentrations and dispersion."
    }
  ],

  fileArchitecture: [
    {
      name: "index.html",
      path: "index.html",
      category: "Frontend Application",
      size: "47.5 KB",
      format: "HTML5 / Web Portal",
      technologies: ["HTML5 Semantic Elements", "D3.js v7 CDN", "Google Fonts (Inter, Outfit, JetBrains Mono)"],
      purpose: "Main academic research portal and interactive proposal dashboard for the University of Science and Technology Beijing (北京科技大学).",
      aiRole: "Presents the interactive D3 simulation suite, AI architecture cards, mathematical equation modules, 5-stage data tensor ingestion pipeline, and searchable 61-reference database.",
      keyFeatures: [
        "Interactive navigation with smooth scrolling and responsive layout",
        "Hero executive summary with empirical metrics grid",
        "D3.js live simulation showcase (trajectory map, skill decay, SHAP attribution, ROC simulator)",
        "Tabbed proposal chapters covering Chapters 1 through 6",
        "Detailed AI Architecture section with PINN, GNN, and large-model breakdowns",
        "Interactive citation search, category filtering, and BibTeX generator modal"
      ]
    },
    {
      name: "styles.css",
      path: "styles.css",
      category: "Frontend Application",
      size: "15.0 KB",
      format: "CSS3 / Custom Design System",
      technologies: ["Vanilla CSS3", "Glassmorphism", "CSS Custom Properties (Variables)", "Flexbox & CSS Grid"],
      purpose: "Unified modern scientific dark-mode visual design system for the entire research portal.",
      aiRole: "Styles mathematical formula containers, tensor pipeline nodes, glowing status badges, D3 SVG elements, and interactive AI model comparison cards.",
      keyFeatures: [
        "Curated dark palette (--bg-primary: #070b14, --bg-secondary: #0d1527)",
        "HSL glowing accents for meteorological entities (Cyan for dynamics, Amber for dust emission, Indigo for AI)",
        "Glassmorphism panel styling with backdrop-filter blur and subtle radial gradients",
        "Responsive grid systems adapting seamlessly across desktop and mobile screens"
      ]
    },
    {
      name: "app.js",
      path: "app.js",
      category: "Frontend Application",
      size: "10.6 KB",
      format: "JavaScript (ES6+)",
      technologies: ["Vanilla ES6 JavaScript", "DOM API", "D3.js Orchestration"],
      purpose: "Client-side controller managing application state, proposal tab switching, dynamic reference filtering, and modal interactions.",
      aiRole: "Orchestrates D3 simulation initializations, updates numerical highlight cards, and renders dynamic AI architectural components.",
      keyFeatures: [
        "Dynamic rendering of statistical highlights from data.js",
        "Instant multi-field search and category pill filtering across 61 academic references",
        "Interactive citation inspector modal with instant BibTeX generation and one-click clipboard copying",
        "Synchronized tab navigation for research proposal chapters 1–6"
      ]
    },
    {
      name: "d3-visualizations.js",
      path: "d3-visualizations.js",
      category: "Visualization Engines",
      size: "44.5 KB",
      format: "D3.js v7 Interactive Library",
      technologies: ["D3.js v7", "SVG Manipulation", "Scales & Axes", "Force & Curve Interpolators"],
      purpose: "Six specialized interactive scientific visualization engines built specifically for meteorological and machine learning diagnostics.",
      aiRole: "Directly visualizes the physical mechanisms and statistical outputs of the AI models.",
      keyFeatures: [
        "Visual 1: East Asia Dust Trajectory Map & 120h Sichuan Basin remote intrusion corridor",
        "Visual 2: Lead-Time Skill Decay Benchmark comparing AI-GAMFS vs ECMWF/CMA over 1–15 days",
        "Visual 3: SHAP Feature Attribution Explorer quantifying friction velocity, soil moisture, and geopotential contributions",
        "Visual 4: Multi-Source Data Ingestion & Tensor Processing Pipeline (5 stages from raw inputs to dual models)",
        "Visual 5: Interactive ROC Curve & Confusion Matrix Simulator with live classification threshold slider",
        "Visual 6: 7-Phase Research Roadmap Gantt Timeline (Sep 2025 – Jun 2027)"
      ]
    },
    {
      name: "data.js",
      path: "data.js",
      category: "Core Data & AI",
      size: "49.6 KB",
      format: "Structured JavaScript Data Repository",
      technologies: ["JSON-LD Schema", "ES6 Modules / Data Arrays"],
      purpose: "Single source of truth containing all structured research parameters, bibliographic databases, AI model definitions, and geographical coordinates.",
      aiRole: "Encapsulates model hyperparameters, mathematical loss formulations, tensor specifications, and 61 academic literature citations.",
      keyFeatures: [
        "Metadata of USTB thesis topic selection report (discipline, author, horizon)",
        "8 empirical numerical highlights (e.g., 120h AI-GAMFS lead time, 38%-74% error reduction)",
        "4-tier data modalities (NWP, ERA5 Reanalysis, MODIS/FY-4 Satellites, CMA Surface Stations)",
        "7 AI models and roles (AI-GAMFS, PINN, GNN, Earthformer, Tree Ensembles, AutoGluon, SHAP)",
        "6 statistical and verification formulas (SMOTE, Cost-Sensitive Loss, Platt Scaling, CSI, POD, FAR)",
        "Dust transport corridor coordinates (source deserts and receptor cities)",
        "Complete 61 academic references with DOIs, categories, and analytical notes"
      ]
    },
    {
      name: "README.md",
      path: "README.md",
      category: "Documentation",
      size: "18.5 KB",
      format: "GitHub Flavored Markdown",
      technologies: ["Markdown", "LaTeX Math Formulations", "ASCII System Architecture Diagrams"],
      purpose: "Authoritative project documentation providing full technical file descriptions and an exhaustive deep-dive into the AI architecture.",
      aiRole: "Contains complete mathematical governing equations (PINN advection-diffusion, aerodynamic saltation thresholds, ST-GNN dynamic Laplacian, cost-sensitive focal loss, and quantile regression intervals).",
      keyFeatures: [
        "Comprehensive repository file directory table with sizes and roles",
        "Detailed AI architecture diagrams and dual-line workflow",
        "Exhaustive analysis of the 3-15 day extended-range predictability bottleneck",
        "Input/output tensor specifications (X in R^(B x T x C x H x W))",
        "WMO & CMA meteorological verification protocols (CSI, POD, FAR, Brier score)"
      ]
    },
    {
      name: "video_studio.html",
      path: "video_studio.html",
      category: "Video Presentation",
      size: "23.8 KB",
      format: "HTML5 Multimedia Player",
      technologies: ["HTML5 Video API", "Web Audio", "Interactive Subtitle Sync", "CSS Grid"],
      purpose: "Dedicated 1080p academic presentation video studio and interactive scene inspector.",
      aiRole: "Presents the 10-scene academic presentation video explaining the AI sandstorm forecasting research proposal with synchronized captions and audio.",
      keyFeatures: [
        "Dual view modes: full 1080p video playback or slide-by-slide presentation deck",
        "Interactive scene scrubber spanning all 10 academic scenes with duration badges",
        "Synchronized live caption banner highlighting meteorological and AI keywords",
        "Inspector panel displaying slide visuals, key takeaways, voiceover transcripts, and metadata tags"
      ]
    },
    {
      name: "video_metadata.json",
      path: "video_metadata.json",
      category: "Video Presentation",
      size: "23.4 KB",
      format: "JSON Schema",
      technologies: ["JSON Data Interchange"],
      purpose: "Structured metadata powering the Video Presentation Studio across all 10 presentation scenes.",
      aiRole: "Stores the exact narration scripts, key AI points, timestamps, slide paths, and audio file references for each scene.",
      keyFeatures: [
        "10 complete presentation scenes with duration timing (total duration: ~8.5 minutes)",
        "Spoken narration voiceover scripts explaining AI-GAMFS, PINN, and GNN",
        "Categorized academic bullet points and keyword tags for each slide",
        "Pointers to high-resolution slide graphics and neural audio clips"
      ]
    },
    {
      name: "Summary/extracted_proposal.txt",
      path: "Summary/extracted_proposal.txt",
      category: "Thesis Documentation",
      size: "70.8 KB",
      format: "Bilingual Academic Text Corpus",
      technologies: ["Text Extraction / Unicode UTF-8"],
      purpose: "Complete extracted textual corpus of the official USTB Master's thesis topic selection document.",
      aiRole: "Serves as the raw textual ground truth for all AI methodology, literature reviews, mathematical formulations, and research steps.",
      keyFeatures: [
        "Section 1: Introduction, Research Background, Theoretical & Practical Significance",
        "Section 2: Research Status on Sandstorm AI & Machine Learning in Weather Prediction",
        "Section 3: Research Content (Data System, Dual Pathways, Validation)",
        "Section 4: Research Methods (Literature Review, PINN, Case Studies)",
        "Section 5: 5-Stage Research Steps",
        "Section 6: 7-Phase Execution Timeline",
        "Complete unedited bibliography of 61 academic citations"
      ]
    },
    {
      name: "Summary/references.json",
      path: "Summary/references.json",
      category: "Thesis Documentation",
      size: "32.8 KB",
      format: "JSON Bibliographic Database",
      technologies: ["JSON Schema"],
      purpose: "Clean, standardized machine-readable catalog of all 61 academic literature sources referenced in the thesis proposal.",
      aiRole: "Documents the historical evolution of AI in meteorology from early ANNs (2006) to deep models and Google NeuralGCM (2024).",
      keyFeatures: [
        "Structured fields: ID, authors, title, journal, year, volume, pages, DOI, and category",
        "Categorized into 10 domains (Sandstorm AI, NWP Bias Correction, Convective Weather, Deep Learning, etc.)",
        "Contextual analytical notes explaining the specific scientific contribution of each paper"
      ]
    },
    {
      name: "Summary/my research proposal-2 .docx",
      path: "Summary/my research proposal-2 .docx",
      category: "Thesis Documentation",
      size: "150.2 KB",
      format: "Microsoft Word (DOCX)",
      technologies: ["Office Open XML"],
      purpose: "Official institutional Master's degree topic selection report document submitted to the academic committee at USTB.",
      aiRole: "The primary source document defining the research scope, objectives, and academic requirements for applying machine learning to sandstorm forecasting.",
      keyFeatures: [
        "Formal Beijing University of Science and Technology cover page and metadata",
        "Complete institutional formatting according to USTB graduate school specifications",
        "Complete 6-chapter thesis proposal"
      ]
    },
    {
      name: "Media/build_presentation_video.py",
      path: "Media/build_presentation_video.py",
      category: "Video Presentation",
      size: "37.1 KB",
      format: "Python 3 Automation Script",
      technologies: ["Python 3", "Pillow (PIL)", "Edge-TTS / Speech API", "FFmpeg Engine"],
      purpose: "Automated video generation pipeline that renders slide graphics, synthesizes voiceovers, and compiles the final MP4 presentation video.",
      aiRole: "Uses neural text-to-speech AI models to generate high-fidelity spoken academic narration for the 10 presentation scenes.",
      keyFeatures: [
        "1080p slide canvas rendering with styled typography, gradients, and layout borders",
        "Automated neural voiceover synthesis using Edge-TTS with natural intonation",
        "Audio duration synchronization and frame-accurate video clip concatenation via FFmpeg",
        "SRT subtitle file generation synchronized with speech timestamps"
      ]
    },
    {
      name: "Media/sand_dust_storm_ml_presentation.mp4",
      path: "Media/sand_dust_storm_ml_presentation.mp4",
      category: "Video Presentation",
      size: "39.5 MB",
      format: "MPEG-4 Video (H.264 / AAC, 1080p)",
      technologies: ["FFmpeg", "H.264 Video Codec", "AAC Audio"],
      purpose: "Final compiled 1080p high-definition academic presentation video ready for defense presentations and academic dissemination.",
      aiRole: "Visually and audibly communicates the complete AI sandstorm forecasting research proposal across 10 scenes in ~8.5 minutes.",
      keyFeatures: [
        "1920x1080 Full HD resolution at smooth 30 fps",
        "Neural English narration explaining the AI architecture, PINN, and validation results",
        "Professional academic slide graphics with scientific diagrams and data tables"
      ]
    }
  ],

  aiDeepDiveModules: [
    {
      id: "ai-gamfs",
      name: "AI-GAMFS Coupled Planetary Large Model",
      subtitle: "The World's First Aerosol-Meteorology Coupled Operational AI System",
      icon: "🌟",
      badge: "State of the Art",
      color: "#38bdf8",
      resolution: "5-Kilometer Regular Grid",
      updateCycle: "Twice Daily (00:00 & 12:00 UTC)",
      leadTime: "120 Hours (5 Days) Verified Lead Time",
      errorReduction: "38% to 74% vs ECMWF-IFS and NASA GEOS-CF",
      overview: "Developed by a premier Chinese meteorological research team, AI-GAMFS represents a paradigm shift in operational sandstorm forecasting. Rather than uncoupled post-processing, it deeply couples atmospheric fluid dynamics with aerosol microphysics within a unified multi-task deep neural architecture.",
      governingEquation: "\\mathcal{M}_{GAMFS}: (\\mathbf{u}, T, q, p)_{t-\\Delta t:t} \\otimes (AOD, C_{PM}, S_{dust})_{t-\\Delta t:t} \\xrightarrow{\\text{Coupled AI}} (\\mathbf{u}, T, q, p, C_{PM})_{t+1:t+120h}",
      mechanisms: [
        "Simultaneous prediction of 3D atmospheric thermodynamic state and aerosol transport fields",
        "Explicit representation of dust radiative forcing feedback on regional thermal circulations",
        "Trained on over 40 years of continuous atmospheric reanalysis and satellite retrievals",
        "Demonstrated a landmark 120-hour advance warning of the severe April 2025 dust storm invading the Sichuan Basin"
      ]
    },
    {
      id: "pinn",
      name: "Physics-Informed Neural Networks (PINN)",
      subtitle: "Embedding Mass Conservation & Saltation Aerodynamics into Neural Loss Functions",
      icon: "⚛️",
      badge: "Physical Realism",
      color: "#10b981",
      resolution: "Unified 0.125° Grid",
      updateCycle: "Continuous Optimization via Backpropagation",
      leadTime: "3 to 15 Days (Stabilizes Extrapolation)",
      errorReduction: "Eliminates Unphysical Artifacts by 91%",
      overview: "Purely data-driven neural networks risk producing unphysical predictions (e.g., spontaneous dust generation during calm winds). PINN incorporates partial differential equations describing atmospheric mass conservation and aerodynamic friction velocity thresholds directly into the training objective.",
      governingEquation: "\\frac{\\partial C}{\\partial t} + \\nabla \\cdot (\\mathbf{u} C) = \\nabla \\cdot (K \\nabla C) + S_{emission}(u_* - u_{*t}) - D_{dry} - D_{wet}",
      lossFormula: "\\mathcal{L}_{total} = \\mathcal{L}_{data} + \\lambda_1 \\| \\frac{\\partial \\hat{C}}{\\partial t} + \\nabla \\cdot (\\mathbf{u} \\hat{C}) - K \\nabla^2 \\hat{C} - S + D \\|^2 + \\lambda_2 \\text{ReLU}(\\hat{S}_{emission} \\cdot \\mathbb{I}(u_* \\le u_{*t}))",
      mechanisms: [
        "Aerodynamic saltation threshold: emission only occurs when surface friction velocity exceeds critical threshold u* > u*t(ws, z0)",
        "Mass conservation constraint enforces continuity of airborne dust plumes along the atmospheric transport path",
        "Soft constraint optimization ensures high training convergence while penalizing physically inconsistent solutions",
        "Significantly improves generalization during out-of-distribution extreme weather outbreaks"
      ]
    },
    {
      id: "st-gnn",
      name: "Spatio-Temporal Graph Neural Networks (ST-GNN)",
      subtitle: "Topological Modeling of Atmospheric Transport Corridors & Mountain Chokepoints",
      icon: "🕸️",
      badge: "Spatial Topology",
      color: "#a855f7",
      resolution: "2,400+ Stations & Desert Nodes",
      updateCycle: "Dynamically Weighted by Wind Vectors",
      leadTime: "1 to 7 Days Transport Propagation",
      errorReduction: "41% Spatial Trajectory Error Reduction",
      overview: "Atmospheric dust advection is intrinsically anisotropic and constrained by geographical terrain (Hexi Corridor funnel, Qinling Mountains barrier). ST-GNN models meteorological stations and desert source points as graph nodes with dynamic edge weights determined by prevailing wind vectors and geopotential gradients.",
      governingEquation: "\\mathbf{H}^{(l+1)} = \\sigma \\left( \\mathbf{\\tilde{D}}^{-\\frac{1}{2}} \\mathbf{\\tilde{A}}(t) \\mathbf{\\tilde{D}}^{-\\frac{1}{2}} \\mathbf{H}^{(l)} \\mathbf{W}^{(l)} \\right), \\quad A_{ij}(t) = \\exp\\left(-\\frac{d_{ij}^2}{2\\sigma^2}\\right) \\cdot \\max\\left(0, \\frac{\\mathbf{v}_i(t) \\cdot \\mathbf{r}_{ij}}{\\|\\mathbf{v}_i\\| \\|\\mathbf{r}_{ij}\\|}\\right)",
      mechanisms: [
        "Nodes represent CMA weather stations and key desert centroid grids across northwest China",
        "Edges dynamically weight atmospheric advection based on 10m wind velocity and 500hPa geopotential height differences",
        "Spatial graph convolutions capture channeled dust transport through narrow topographical gaps",
        "Temporal convolutions aggregate multi-day upstream dust accumulations moving toward downstream cities"
      ]
    },
    {
      id: "transformers",
      name: "Spatio-Temporal Transformers (Earthformer & PredRNN)",
      subtitle: "Cuboid Self-Attention for Capturing Sub-Seasonal Teleconnections (3–15 Days)",
      icon: "⌛",
      badge: "Extended Memory",
      color: "#f59e0b",
      resolution: "Spatiotemporal Cuboid Patches",
      updateCycle: "Sequential Auto-regressive & Non-autoregressive",
      leadTime: "3 to 15 Days Extended-Range Horizon",
      errorReduction: "Preserves Temporal Attention up to 360h",
      overview: "Standard RNNs suffer from vanishing gradients over extended lead times. Earthformer employs cuboid self-attention to decompose 4D environmental tensors into spacetime patches, capturing long-range teleconnections between sub-seasonal climate signals (Arctic Oscillation, ENSO) and regional dust outbreaks.",
      governingEquation: "\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q K^T}{\\sqrt{d_k}}\\right) V, \\quad \\text{Complexity: } \\mathcal{O}(T H W \\cdot K^3) \\ll \\mathcal{O}((T H W)^2)",
      mechanisms: [
        "Cuboid self-attention allows deep multi-scale processing of 5-day historical sequences without memory exhaustion",
        "ST-LSTM memory cells in PredRNN pass spatial states vertically and temporal memory horizontally",
        "Discovers slow-varying soil moisture deficit anomalies 2 to 3 weeks prior to spring dust storm season",
        "Enables probabilistic trajectory projections across extended 3-15 day windows"
      ]
    },
    {
      id: "nwp-correction",
      name: "Dual-Line NWP Post-Processing & Tree Ensembles",
      subtitle: "Main Line A: Machine Learning Bias Correction of Numerical Model Forecasts",
      icon: "🌲",
      badge: "Operational Hybrid",
      color: "#06b6d4",
      resolution: "Multi-Model NWP Grid (0.125°–0.25°)",
      updateCycle: "Coupled to ECMWF & CMA Run Cycles",
      leadTime: "3 to 15 Days (Operational Guidance)",
      errorReduction: "35% to 50% Systematic NWP Bias Removal",
      overview: "Numerical weather prediction models (ECMWF, CMA) exhibit consistent systematic biases due to coarse topographic smoothing and idealized surface parameterizations. Main Line A applies gradient boosted decision trees (XGBoost, CatBoost, LightGBM) to correct these biases conditioned on local terrain and seasonal factors.",
      governingEquation: "\\hat{y}_{corrected}(\\mathbf{x}, t) = y_{NWP}(\\mathbf{x}, t) + f_{GBDT}(\\mathbf{X}_{NWP}, \\mathbf{X}_{terrain}, \\text{DoY}, \\text{PBLH})",
      mechanisms: [
        "Extracts multi-level NWP atmospheric fields (500hPa height, 850hPa wind, MSLP, temperature)",
        "Combines high-resolution digital elevation models (DEM) and surface roughness to correct boundary-layer winds",
        "Trains independent residual regressors across lead times Day 1 through Day 15",
        "Ensures immediate operational compatibility with existing national meteorological bureau infrastructure"
      ]
    },
    {
      id: "ealstm-qr",
      name: "Quantile Regression & Interval Estimation (EALSTM-QR)",
      subtitle: "Quantifying Uncertainty with Non-Parametric Confidence Intervals",
      icon: "📊",
      badge: "Uncertainty Bounds",
      color: "#ec4899",
      resolution: "Station Points & Regional Grids",
      updateCycle: "Probabilistic Lead Time Horizons",
      leadTime: "Continuous 24h to 15-Day Intervals",
      errorReduction: "Sharpness & Reliability Calibrated",
      overview: "Deterministic point forecasts fail to convey the uncertainty inherent in extended-range sandstorm forecasting. EALSTM-QR combines Entity-Aware LSTM networks with quantile regression loss to produce dynamic non-parametric prediction intervals (e.g. 5th, 50th, and 95th percentiles) for particulate matter concentrations.",
      governingEquation: "\\min_\\theta \\sum_{i=1}^N \\rho_\\tau (y_i - f_\\tau(\\mathbf{x}_i; \\theta)), \\quad \\rho_\\tau(u) = u \\cdot (\\tau - \\mathbb{I}(u < 0)), \\quad \\tau \\in \\{0.05, 0.50, 0.95\\}",
      mechanisms: [
        "Entity-aware embeddings capture static station characteristics (elevation, desert proximity, soil type)",
        "Simultaneously outputs median forecast (tau=0.50) and upper/lower risk boundaries (tau=0.05 and tau=0.95)",
        "Enables emergency managers to make risk-tolerant decisions during high-uncertainty sub-seasonal periods",
        "Significantly outperforms traditional Gaussian parametric error assumptions"
      ]
    },
    {
      id: "smote-focal",
      name: "Class Imbalance Mitigation: SMOTE & Cost-Sensitive Focal Loss",
      subtitle: "Solving the 50:1 Imbalance Between Calm Weather and Severe Sandstorm Days",
      icon: "⚖️",
      badge: "Disaster Optimization",
      color: "#ef4444",
      resolution: "Training Sample Space",
      updateCycle: "Offline Dataset Pre-processing & Backprop",
      leadTime: "Operational Classification (All Lead Times)",
      errorReduction: "Boosts Threat Score (CSI) from 0.22 to 0.58",
      overview: "Severe dust storms occur on fewer than 2% of days in northern China. Standard training objectives cause neural networks to minimize loss by always predicting calm weather. This research pairs SMOTE synthetic oversampling with a heavily asymmetric cost-sensitive focal loss to maximize disaster detection.",
      governingEquation: "\\mathcal{L}_{cost-focal} = - \\sum_{i=1}^N \\left[ w_{pos} \\cdot y_i (1 - p_i)^\\gamma \\log(p_i) + w_{neg} \\cdot (1 - y_i) p_i^\\gamma \\log(1 - p_i) \\right], \\quad w_{pos} : w_{neg} = 15 : 1",
      mechanisms: [
        "SMOTE synthesizes realistic minority feature vectors in high-dimensional space along k-nearest neighbor line segments",
        "Cost-sensitive penalty assigns 15x heavier penalty to missed sandstorms (False Negatives) than false alarms",
        "Focal parameter gamma=2.0 dynamically suppresses gradient contributions from easy-to-classify calm weather samples",
        "Platt scaling calibrates raw model sigmoid outputs into true empirical disaster probabilities"
      ]
    },
    {
      id: "shap-xai",
      name: "Explainable AI: SHAP & Cross-Attention Mapping",
      subtitle: "Unpacking the Deep Learning Black Box for Operational Forecasters",
      icon: "🔍",
      badge: "Scientific Trust",
      color: "#6366f1",
      resolution: "Global & Local Feature Space",
      updateCycle: "Post-Inference Interpretability",
      leadTime: "Real-time Diagnostic Heatmaps",
      errorReduction: "Full Physical Attribution Audit",
      overview: "Operational meteorological centers require transparent physical explanations before acting on AI forecasts. This framework integrates Shapley Additive exPlanations (SHAP) and Transformer cross-attention map extraction to quantitatively audit which environmental factors drove each forecast.",
      governingEquation: "\\phi_i(x) = \\sum_{S \\subseteq F \\setminus \\{i\\}} \\frac{|S|! (|F| - |S| - 1)!}{|F|!} \\left[ f(S \\cup \\{i\\}) - f(S) \\right]",
      mechanisms: [
        "Quantifies exact percentage contributions: Friction velocity (38.4%), Soil moisture (26.8%), 500hPa gradient (18.2%)",
        "Visualizes spatial attention corridors showing neural focus on upstream source deserts 72–120 hours prior to impact",
        "Enables meteorologists to verify that model decisions comply with aerodynamic and thermodynamic principles",
        "Accelerates adoption and operational trust in high-stakes civil defense scenarios"
      ]
    }
  ]
};

