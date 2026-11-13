# Scripts Directory Architecture

This directory houses the operational, preprocessing, modeling, evaluation, and manuscript pipeline for the Riyadh Sandstorm Forecasting project:

```
scripts/
├── riyadh_common.py                 # Core shared config (bounding boxes, thresholds, paths, CDS client)
├── 01_data_acquisition/             # Automated downloaders for CAMS, ERA5 (Surface & Pressure Levels), MODIS
├── 02_data_verification_qaqc/       # QA/QC inspection, range validation & completeness reports
├── 03_collocation_and_features/     # 4-modality alignment, anti-leakage lags & feature store generation
├── 04_model_training_and_tuning/    # Meta-Models, Line A (Tabular ML), Line B (Deep Learning & PINN)
├── 05_evaluation_and_plotting/      # Automated execution of all 4 Jupyter notebooks with inline outputs
├── 05_literature_rag/               # Scientific literature retrieval augmented generation (RAG) tools
├── 06_utils/                        # General utilities (usage calculator, telemetry helpers)
├── 07_manuscript_compilation/       # Manuscript builder, figure generation & Word packaging
│   ├── compile_enhanced_manuscript.py
│   ├── generate_manuscript_figures.py
│   ├── copy_to_original.py
│   └── update_full_manuscript.py
└── tests_and_diagnostics/           # Diagnostic inspections, figure validators & XML drawing tests
    ├── inspect_docx.py
    ├── inspect_images.py
    ├── print_drawing_xml.py
    ├── print_full_drawing.py
    ├── print_section3.py
    ├── test_drawing_syntax.py
    ├── test_embed_image.py
    ├── test_xml_helper.py
    └── verify_figures.py
```
