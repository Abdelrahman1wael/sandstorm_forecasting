# Final Project Submission: Sand and Dust Storm Forecasting in Saudi Arabia (Riyadh)

This folder contains the consolidated, production-ready, authentic deliverables for the Master's research project:
**"Machine Learning for Medium- to Long-Term Sand and Dust Storm Forecasting in Saudi Arabia (Riyadh)"**.

---

## Directory Overview

```
final_project_copy/
├── README.md                           # Master deliverables catalog (this file)
├── 01_Documentation/                   # Final Word manuscripts & thesis chapters
│   ├── Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2)_latest.docx
│   ├── Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2)_enhanced.docx
│   ├── Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2).docx
│   └── Dust_Storm_Forecasting_Riyadh_rewritten.docx
├── 02_Presentation/                    # Midterm deck & Explainable AI presentations
│   ├── merged_presentation_choladeck.pptx
│   └── Explainable AI for Sand and Dust Storm Forecasting – Riyadh.pdf
├── 03_Supervisor_Planning/             # Supervisor feedback, research roadmap, and taxonomy
│   ├── SUPERVISOR_RESPONSE_METHODOLOGY_PLAN.md
│   ├── Sandstorm_Forecasting_Taxonomy_and_Methodology.docx
│   ├── sandstorm_forecasting_taxonomy.png
│   ├── sandstorm_forecasting_taxonomy.svg
│   ├── DATA_ARCHITECTURE_LINE_A_AND_LINE_B.md
│   ├── RIYADH_REAL_DATASETS_PROVENANCE_AND_VERIFICATION.md
│   ├── SAUDI_ARABIA_NWP_DATASET_PROVENANCE.md
│   └── CITY_SELECTION_AND_VISUALIZATION_EXPLANATION.md
├── 04_Notebooks/                       # All 4 complete executed Jupyter Notebooks with inline plots
│   ├── 00_data_representation_and_distribution_riyadh.ipynb
│   ├── 01_line_a_tabular_and_meta_models_riyadh.ipynb
│   ├── 02_line_b_lstm_transformer_stgnn_riyadh.ipynb
│   ├── 03_explainable_ai_xai_riyadh.ipynb
│   └── riyadh_sandstorm_explainable_ai_xai.ipynb
├── 05_Models/                          # All trained models, checkpoints, scalers, and metadata
│   ├── meta_model/                     # RandomForest, XGBoost, GradientBoosting, NeuralNetwork, PowerTransformer
│   ├── line_a/                         # Line A1, A2, A3 HistGB and XGBoost models + LabelEncoder
│   └── line_b/                         # LSTM, 4-Head Transformer, PINN, Hybrid Ensemble, ST-GNN
├── 06_Data/                            # Authentic real-world feature stores, 3D tensors, and test results
│   ├── meta_features.csv               # 14,612 timestamps x 33 balanced predictors (2015-2024)
│   ├── feature_columns.txt             # Inventory of active features across the 4 modalities
│   ├── deep_learning_sequences_riyadh.npz # 3D Sequence tensors (N, 8 steps, 33 features)
│   ├── riyadh_line_a_tabular_features.csv # 87,456 hourly records x 114 columns
│   ├── line_b_final_dataset.npz        # Multi-node spatiotemporal graph dataset
│   ├── riyadh_graph_adjacency_matrix.npy # 6x6 spatial graph adjacency matrix
│   └── results/                        # All evaluation metrics, optimal thresholds, and XAI CSVs
├── 07_Figures/                         # High-resolution thesis and Explainable AI figures
│   ├── fig1_data_architecture_and_spatial_domain.png
│   ├── fig2_yeo_johnson_distribution_balancing.png
│   ├── fig3_line_a_nwp_bias_correction.png
│   ├── fig4_line_b_models_and_pinn_loss.png
│   └── xai/                            # Figures 6-14 (SHAP, PDP, ICE, Surrogates, Attention, ST-GNN)
└── 08_Scripts/                         # Production pipeline, feature balancer & manuscript compilers
    ├── riyadh_common.py                # Core configuration module
    ├── 01_data_acquisition/            # Real-world data downloaders (CAMS, ERA5, MODIS)
    ├── 02_data_verification_qaqc/      # QA/QC inspection & validation
    ├── 03_collocation_and_features/    # Collocation & data_handling_and_feature_balancing.py
    ├── 04_model_training_and_tuning/   # Model training & optimization
    ├── 05_evaluation_and_plotting/     # build_and_run_all_notebooks.py
    ├── 07_manuscript_compilation/      # compile_enhanced_manuscript.py
    └── tests_and_diagnostics/          # Validation and verification scripts
```

---

## Key Highlights & Scientific Contributions

1. **Zero Synthetic Data / 100% Real-World Telemetry:**
   - Observational target based on authentic CAMS vs. AERONET forecast error ($|CAMS - AERONET| > 1.5\sigma_{Riyadh}$).
   - Real ECMWF ERA5 850, 700, and 500 hPa upper-air fields without artificial multi-scale formulas.
2. **Anti-Leakage Safeguards:**
   - 48-72h lag on ground optical proxies eliminates lookahead autocorrelation.
   - Strict 80/20 chronological partition ($2015\text{--}2022$ train / $2023\text{--}2024$ out-of-sample test).
   - Yeo-Johnson power transformations fitted strictly on training data.
3. **Physics-Informed Deep Learning (PINN):**
   - Direct neural loss penalization of Owen (1964) aeolian saltation flux, 3D dust mass conservation PDE residuals, and baroclinic thermal-wind shear balance.
4. **Explainable AI (XAI) Suite:**
   - 6 complementary XAI methodologies confirming balanced physical attributions across surface soil moisture, wind gusts, upper-level Shamal channels, and ground optical proxies.
