# 🛠️ Sandstorm Forecasting Pipeline: Scripts Directory

This directory contains the operational and development scripts for data acquisition, verification, preprocessing, machine learning execution, RAG system, presentation generation, and notebook creation.

```
scripts/
├── data_acquisition/       # Automated retrieval of raw ground, satellite, reanalysis & NWP data
├── data_verification/      # Rigorous QC audits, file integrity, and data validation
├── preprocessing/          # Data harmonization, multi-modal merging & feature engineering
├── pipeline_runners/       # End-to-end ML training, threshold optimization & baseline benchmarking
├── notebook_generators/    # Automated builders for analysis and pipeline Jupyter Notebooks
├── rag/                    # Anthropogenic dust sources literature scraping, indexing & hybrid RAG
├── doc_and_diagrams/       # Automated Word (.docx) document, PowerPoint, Excel, and Draw.io generators
└── utils/                  # Project utility scripts and diagnostic calculators
```

---

## 📂 Subdirectory Inventory

### 1. `data_acquisition/`
Scripts responsible for fetching raw data from official meteorology and atmospheric providers:
* `cams_big_batch.py`: Batch downloader for CAMS dust AOD in 6-month chunks.
* `cams_supplement.py`: Supplementary download pipeline for CAMS forecasts (2020–2024).
* `download_201501_pl.py`: Dedicated download handler for ERA5 pressure-level files.
* `download_cams.py`: CAMS Global Dust AOD forecasts 10-day batch retrieval.
* `download_cmip6.py`: ESGF retrieval for CMIP6 dust optical depth (`od550dust`).
* `download_era5.py`: Monthly batch retrieval of ECMWF ERA5 reanalysis single- and pressure-levels.
* `download_modis_aod.py`: NASA MODIS Deep Blue AOD (550nm) OPeNDAP extraction.
* `era5_big_batch.py`: Bulk gap filler for ERA5 reanalysis datasets.
* `era5_bulk_download.py`: High-throughput multi-field ERA5 bulk downloader.
* `era5_optimized.py`: Combined multi-variable pressure-level ERA5 retrieval.
* `era5_pl_quarterly.py`: Quarterly chunking engine for large ERA5 pressure-level queries.
* `era5_supplement.py`: Supplementary downloader for ERA5 records.
* `submit_all_cams.py`: Concurrent multi-worker job submission for CAMS ADS queues.
* `submit_all_era5.py`: Concurrent multi-worker job submission for ERA5 CDS queues.

### 2. `data_verification/`
Validation scripts ensuring file integrity and scientific rigor:
* `aeronet_temporal_heatmap.py`: Station × month temporal coverage heatmap generator for AERONET Level 1.5 & 2.0.
* `aeronet_tier3_analysis.py`: Detailed temporal and quality tier analysis for Tier 3 stations.
* `qaqc_aeronet.py`: QA/QC validator for AERONET ground truth CSV archives.
* `qaqc_cams.py`: QA/QC integrity and domain boundary checker for CAMS NetCDF forecasts.
* `qaqc_cmip6.py`: QA/QC schema and value bounds validation for CMIP6 climate models.
* `qaqc_era5.py`: Comprehensive QA/QC suite for ERA5 surface and pressure NetCDFs.
* `qaqc_report.py`: Master QA/QC orchestrator producing a unified health and checklist report.
* `three_way_validation.py`: Three-way cross-validation (MODIS vs AERONET vs CAMS) with scatter statistics.

### 3. `preprocessing/`
The core feature engineering, collocation, and multimodal coupling engine:
* `build_meta_features.py`: Phase 2 Step 1 feature engineering coupling CAMS-AERONET error dynamics with ERA5 meteorology.
* `collocate_cams_aeronet.py`: Spatio-temporal collocation aligning AERONET station observations with CAMS forecast timesteps.
* `merge_cams.py`: Merges raw CAMS 10-day forecast windows into unified monthly archives.

### 4. `pipeline_runners/`
End-to-end model training, threshold tuning, and benchmarking:
* `train_meta_model.py`: Phase 2 Step 2 training pipeline for Random Forest, XGBoost, and Neural Network meta-models.
* `benchmark_baselines.py`: Benchmarks meta-models against Climatology and Persistence baselines.
* `optimize_threshold.py`: Precision-recall curve analysis and optimal F1 classification threshold tuning.

### 5. `notebook_generators/`
Generates clean, runnable Jupyter notebooks for presentations and analysis:
* `generate_processing_notebooks.py`: Builds modular data processing notebooks in `notebooks/data_processing/`.
* `create_exploration_notebook.py`: Builds exploratory data analysis notebooks.
* `create_line_a_notebook.py` / `create_notebook_04.py`: Builds Machine Learning Line A model notebooks.
* `create_saudi_notebooks.py`: Builds comprehensive Saudi Arabian domain NWP notebooks.

### 6. `rag/`
Retrieval-Augmented Generation system for anthropogenic and regional dust source literature:
* `scrape_papers.py`: OpenAlex and Unpaywall academic paper harvester.
* `build_rag.py`: PDF text extractor, semantic chunker, and ChromaDB vector store builder.
* `query_rag.py`: Hybrid BM25 + dense vector search with re-ranking and LLM cited synthesis.

### 7. `doc_and_diagrams/`
Automation utilities for presentation and publication deliverables:
* `create_awards_excel.py`: Automated generation of structured research submission and awards tracking sheets.
* `generate_complete_presentation.py`: Builds presentation slide assets.
* `generate_drawio_diagram.py`: Programmatically generates XML architectural and pipeline diagrams.
* `organize_documentation_folder.py`: Automated structure organizer for the `Documentation/` tree.
* `render_sitemap_image_and_doc.py`: Renders diagrams and embeds them into final Word documents.
* `verify_docx.py`: Validates Word document formatting and table layouts.
* `extract_proposal_text.py` / `extracted_proposal.txt`: Extracts and indexes proposal specifications.

### 8. `utils/`
Utility tools and tracking scripts:
* `usage_calc.py`: Token usage, context window, and interaction metrics calculator.
