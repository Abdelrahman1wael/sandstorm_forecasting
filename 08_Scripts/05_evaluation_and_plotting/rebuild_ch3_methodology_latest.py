"""Rebuild Chapter 3 (Methodology) in the latest thesis .docx based strictly on
the actual latest project scripts, notebooks, 06_Data/data/, 06_Data/results/,
and 07_Figures/ charts. Removes all old Chapter 3 charts/tables and embeds
the new clean-hourly figures.
"""

from pathlib import Path
import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2_REFS_UPDATED_CLEAN_PERSONAL_EXACT61_REFS_MIDTERM_COVER.docx"
)
FIG_DIR = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting\07_Figures")

TABLE_1 = [
    ["Data modality", "Storage path", "Primary file", "Format", "Size", "Records / dimension"],
    [
        "Clean hourly TVT master",
        "06_Data/data/",
        "riyadh_hourly_clean_tvt.csv",
        "CSV",
        "120.32 MB",
        "86,928 hrs × 126 cols (2015-01-09 to 2024-12-08; 5,795 dust hrs; 61,176 / 8,760 / 16,992 split)",
    ],
    [
        "Line A tabular features",
        "06_Data/data/",
        "riyadh_line_a_tabular_features.csv",
        "CSV",
        "94.80 MB",
        "87,456 hrs × 113 cols (2015-01-02 to 2024-12-23; OERK + ERA5 + Satellite)",
    ],
    [
        "Line B multi-modal tensors",
        "06_Data/data/",
        "line_b_final_dataset.npz",
        "NPZ",
        "0.18 MB",
        "400 samples: NWP (6×16×16), Sat (3×32×32), Seq (24×6×12), Nodes (6×12), Targets (6×6)",
    ],
    [
        "Spatial graph adjacency",
        "06_Data/data/",
        "riyadh_graph_adjacency_matrix.npy",
        "NPY",
        "272 B",
        "6×6 weighted regional station adjacency matrix",
    ],
]

TABLE_2 = [
    ["Horizon", "Best Line A Classification (Test ROC-AUC)", "Best Line B Classification (Test ROC-AUC)", "Best Line A Regression (Test RMSE)", "Best Line B Regression (Test RMSE)"],
    ["24 h (1 d)", "RandomForest_Cal (0.8090)", "LineB_PINN (0.7939)", "Ridge_log1p (36.99 µg/m³)", "LineB_STGNN (21.55 µg/m³)"],
    ["72 h (3 d)", "RandomForest_Cal (0.7167)", "LineB_Transformer (0.7158)", "ExtraTrees (27.63 µg/m³)", "LineB_STGNN (15.58 µg/m³)"],
    ["168 h (7 d)", "RandomForest_Cal (0.7031)", "LineB_PINN (0.6820)", "Ridge_log1p (29.72 µg/m³)", "LineB_LSTM (14.45 µg/m³)"],
    ["216 h (9 d)", "XGBoost_Cal (0.7156)", "LineB_Transformer (0.7065)", "Ridge_log1p (27.68 µg/m³)", "LineB_STGNN (14.86 µg/m³)"],
    ["360 h (15 d)", "XGBoost_Cal (0.7655)", "LineB_Transformer (0.6817)", "Ridge_log1p (30.25 µg/m³)", "LineB_LSTM (14.13 µg/m³)"],
]

TABLE_3 = [
    ["Level", "PM₁₀ (μg/m³)", "Operational actions"],
    ["Level 1 (Green): Normal Advisory", "< 50", "Normal urban operations; routine ambient air-quality monitoring through NCEC ground sensors; regular street maintenance."],
    ["Level 2 (Yellow): Pre-Alert and Monitoring", "50 – < 150", "Automated alerts sent to health authorities; vulnerable groups advised to carry preventive medication; solar PV farms alerted to optimise dry-brush cleaning."],
    ["Level 3 (Orange): Elevated Dust Warning", "150 – < 500", "Issued 24–168 h in advance; Ministry of Education assesses remote-learning contingencies; municipal water sprayers deployed along arterial corridors."],
    ["Level 4 (Red): Severe Sandstorm / Extreme Haboob", "≥ 500", "Immediate emergency protocols; GACA and KKIA enact flight delay/diversion protocols; Traffic Police enforce highway speed limits (< 60 km/h); outdoor construction halted."],
]


def add_para_before(anchor_el, text: str, style: str, doc: docx.Document, align=None):
    p = doc.add_paragraph(text, style=style)
    if align is not None:
        p.alignment = align
    el = p._element
    el.getparent().remove(el)
    anchor_el.addprevious(el)
    return p


def add_figure_before(anchor_el, img_path: Path, caption: str, doc: docx.Document, width_in: float = 6.0):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(str(img_path), width=Inches(width_in))
    el_img = p_img._element
    el_img.getparent().remove(el_img)
    anchor_el.addprevious(el_img)

    add_para_before(anchor_el, caption, "Normal", doc, align=WD_ALIGN_PARAGRAPH.CENTER)


def add_table_before(anchor_el, rows: list[list[str]], caption: str, doc: docx.Document):
    add_para_before(anchor_el, caption, "Normal", doc)
    tbl = doc.add_table(rows=len(rows), cols=len(rows[0]))
    tbl.style = "Table Grid"
    for r_i, row in enumerate(rows):
        for c_i, val in enumerate(row):
            tbl.rows[r_i].cells[c_i].text = val
    el_tbl = tbl._element
    el_tbl.getparent().remove(el_tbl)
    anchor_el.addprevious(el_tbl)


def main() -> None:
    doc = docx.Document(str(DOC_PATH))
    body = doc._body._body

    ch3_p = next(p for p in doc.paragraphs if p.style.name == "Heading 1" and "Chapter 3" in p.text)
    ch4_p = next(p for p in doc.paragraphs if p.style.name == "Heading 1" and "Chapter 4" in p.text)
    ch3_el = ch3_p._element
    ch4_el = ch4_p._element

    # Remove every XML sibling (paragraphs AND tables) strictly between Chapter 3 and Chapter 4
    siblings = list(body)
    i3 = siblings.index(ch3_el)
    i4 = siblings.index(ch4_el)
    for el in siblings[i3 + 1 : i4]:
        body.remove(el)

    # 3.1 Study Setting
    add_para_before(ch4_el, "3.1 Study Setting", "Heading 2", doc)
    add_para_before(
        ch4_el,
        "The study focuses on Riyadh, the capital of Saudi Arabia, located on the Najd plateau. The primary ground-truth receptor is King Khalid International Airport (KKIA; ICAO OERK, WMO 40438; 24.9252°N, 46.7213°E; elevation 614 m), paired with co-located urban observations from Riyadh Air Base (ICAO OERY; 24.7100°N, 46.7250°E; elevation 635 m) and a six-node regional spatial graph (riyadh_graph_adjacency_matrix.npy) capturing upwind dust corridors. Metropolitan Riyadh covers approximately 1,913 km², with surrounding terrain including the Jabal Tuwaiq escarpment ranging from 406 m to 1,119 m above sea level (mean 649.3 m), while regional numerical and satellite grids span 16°N–33°N and 34°E–56°E.",
        "Normal",
        doc,
    )
    add_para_before(
        ch4_el,
        "In the latest multi-modal project pipeline, the continuous hourly observation window spans nearly ten full years: 87,456 raw hourly records from 2 January 2015 to 23 December 2024 in riyadh_line_a_tabular_features.csv, and 86,928 aligned, leak-free hourly records from 9 January 2015 to 8 December 2024 in riyadh_hourly_clean_tvt.csv (containing 5,795 confirmed dust-event hours). Capturing ten complete spring dust seasons enables a strict chronological split—2015–2021 for training (61,176 hours), 2022 for validation (8,760 hours), and 2023–2024 for out-of-sample testing (16,992 hours)—directly preventing temporal leakage across multi-day forecasting horizons.",
        "Normal",
        doc,
    )

    # 3.2 Sources of Data & Acquisition Scripts
    add_para_before(ch4_el, "3.2 Sources of Data and Acquisition Pipeline", "Heading 2", doc)
    add_para_before(
        ch4_el,
        "All empirical datasets were acquired and audited through reproducible scripts in 08_Scripts/01_data_acquisition/ (led by download_all_real_riyadh_data.py, alongside download_era5.py, download_cams.py, and download_modis_aod.py) and verified with 08_Scripts/02_data_verification_qaqc/qaqc_report.py. Rather than treating each modality in isolation, the acquisition scripts feed directly into downstream collocation and clean-hourly notebook builders (08_Scripts/03_collocation_and_features/collocate_cams_aeronet.py, merge_cams.py, and 08_Scripts/05_evaluation_and_plotting/build_and_run_clean_hourly_notebooks.py):",
        "Normal",
        doc,
    )
    add_para_before(
        ch4_el,
        "Ground METAR observations (NOAA / Iowa State Mesonet ASOS): 2015–2024 hourly surface reports for OERK and OERY (temperature, dew point, wind direction/speed/gusts, visibility, sea-level pressure, and WMO dust weather codes), consolidated with co-located OERY variables (oery_visibility_km, oery_wind_speed_ms, oery_tmpc) into riyadh_hourly_clean_tvt.csv (86,928 × 126) and riyadh_line_a_tabular_features.csv (87,456 × 113).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "ECMWF ERA5 hourly reanalysis: 26 harmonised ERA5 columns (19 base physical fields plus 24 h, 72 h, and 168 h rolling wind/gust statistics), including 10 m wind components (u10, v10), gusts, wind kinetic energy, friction-velocity proxy, 2 m temperature, dew point, relative humidity, surface pressure, soil moisture (0–7 cm and 7–28 cm), boundary-layer height (era5_blh_m), solar radiation, and FAO evapotranspiration.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "Satellite remote sensing and NWP (NASA POWER, AERONET, MODIS, CAMS): Seven harmonised satellite columns (sat_retrieved_pm2_5, sat_dust_column_mass, detrended PM₁₀ and AOD₅₅₀ z-scores, and NASA POWER all-sky/clear-sky irradiance and clearness index) plus multi-modal spatial grids packaged in line_b_final_dataset.npz (400 samples with 6×16×16 NWP grids, 3×32×32 satellite grids, 24×6×12 sequences, 6×12 node features, and 6×6 targets).",
        "List Paragraph",
        doc,
    )
    add_table_before(ch4_el, TABLE_1, "Table 1: Verified dataset inventory in 06_Data/data/ used by the latest notebooks and scripts", doc)

    # 3.3 Merging Problems, Leakage Risks, and Cleaning Solutions
    add_para_before(ch4_el, "3.3 Data Merging Challenges, Regime Shift, and Cleaning", "Heading 2", doc)
    add_para_before(
        ch4_el,
        "Exploratory diagnostics in 04_Notebooks/00_data_representation_and_distribution_riyadh.ipynb and 08_Scripts/03_collocation_and_features/data_handling_and_feature_balancing.py identified three critical data-merging defects that directly shaped the cleaning pipeline in 04_Notebooks/01_feature_engineering_and_impact.ipynb:",
        "Normal",
        doc,
    )
    add_para_before(
        ch4_el,
        "1. Irregular ASOS reporting and missingness: Raw METAR feeds contained string 'M' placeholders, sub-hourly duplicates, and elevated missingness in wind gusts and sea-level pressure (Figure 1). Resampling onto a strict UTC hourly index and forward-aligning ERA5 and satellite streams eliminated timestamp mismatches.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "2. Visibility-floor censoring at 53.7 µg/m³: Calibrating PM₁₀ from METAR visibility produced an artificial flat floor spike at 53.7 µg/m³ whenever visibility reached its 10 km reporting cap. In 01_feature_engineering_and_impact.ipynb, this spike was de-censored into a continuous background target (pm10_clean_ugm3), restoring realistic variance prior to log-transformation and Yeo-Johnson power scaling (Figure 3).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "3. 2015–2024 regime shift and satellite drift: Comparing 2015–2021 against 2023–2024 in nb01_clean_hourly_feature_impact.csv revealed strong non-stationarity—most notably in sat_dust_column_mass (Test Z-shift = 5.122), dust_rate_4320h (2.277), dust_rate_720h (1.266), and nwp_bias_proxy (1.168) (Figure 2). Because random shuffling would leak future regime statistics into training, all Yeo-Johnson lambdas, scalers, mutual-information filters, and correlation matrices were fitted strictly on the 2015–2021 training partition (61,176 hours).",
        "List Paragraph",
        doc,
    )
    add_figure_before(ch4_el, FIG_DIR / "nb00_fig01.png", "Figure 1: Raw hourly METAR missingness audit across OERK/OERY variables prior to UTC alignment (00_data_representation_and_distribution_riyadh.ipynb).", doc)
    add_figure_before(ch4_el, FIG_DIR / "nb00_fig03.png", "Figure 2: 2015–2024 temporal regime shift comparing annual dust-event rate against satellite drift, motivating the strict chronological 2015–2021 / 2022 / 2023–2024 split.", doc)
    add_figure_before(ch4_el, FIG_DIR / "nb01_fig01.png", "Figure 3: De-censoring of the 53.7 µg/m³ visibility-floor spike into continuous pm10_clean_ugm3 and train-only Yeo-Johnson skewness reduction (01_feature_engineering_and_impact.ipynb).", doc)

    # 3.4 Connected Feature Engineering
    add_para_before(ch4_el, "3.4 Connected Feature Engineering and Multi-Horizon Targets", "Heading 2", doc)
    add_para_before(
        ch4_el,
        "Building directly on the de-censored hourly stream, 01_feature_engineering_and_impact.ipynb and 08_Scripts/riyadh_common.py engineer a unified feature set linking surface persistence, boundary-layer thermodynamics, and aeolian dust physics to five future horizons: 24 h (1 d), 72 h (3 d), 168 h (7 d), 216 h (9 d), and 360 h (15 d). Engineered predictors include multi-window rolling means/maxima/standard deviations (6 h, 12 h, 24 h, 72 h, 168 h), short-term lags (1 h–24 h), dust-memory rates (dust_rate_168h, dust_rate_720h, dust_rate_4320h, hours_since_dust), and physical emission terms (phys_air_density_kgm3, phys_vpd_kpa, phys_saltation_emission_proxy, friction_velocity_excess, saltation_active_flag, dryness_wind_interaction, and aod_blh_ratio). Train-only mutual information (Figure 4) governs feature selection before passing identical chronological splits to Line A and Line B.",
        "Normal",
        doc,
    )
    add_figure_before(ch4_el, FIG_DIR / "nb01_fig02.png", "Figure 4: Train-only (2015–2021) mutual-information ranking of engineered physical and lagged predictors for 168 h ahead PM₁₀ forecasting.", doc)

    # 3.5 Dual-Line Architecture & Comparison
    add_para_before(ch4_el, "3.5 Dual-Line Forecasting Architecture (Line A vs. Line B) and Comparison", "Heading 2", doc)
    add_para_before(
        ch4_el,
        "To evaluate tabular ensembles against deep spatiotemporal architectures on the exact same chronological benchmark, the methodology couples two complementary modelling lines executed via build_and_run_clean_hourly_notebooks.py and 08_Scripts/04_model_training_and_tuning/run_unified_honest_pipeline.py:",
        "Normal",
        doc,
    )
    add_para_before(
        ch4_el,
        "Main Line A (Tabular & Calibrated Ensembles; 02_line_a_tabular_and_meta_models_riyadh.ipynb): Trains Persistence_Cal, MonthClimo_Cal, LogReg_Bal_Cal, RandomForest_Cal, ExtraTrees_Cal, HistGB_Cal, and XGBoost_Cal for event classification, alongside Ridge_log1p and tree regressors for continuous PM₁₀, evaluated with 5-fold time-series CV and strict 2023–2024 testing (Figure 5; results in nb02_line_a_classification_hourly.csv and nb02_line_a_regression_hourly.csv).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "Main Line B (PyTorch Spatiotemporal & Physics-Informed Models; 03_line_b_pytorch_real_layers.ipynb and train_line_b_pytorch.py): Maps the same hourly predictors and multi-modal grids (line_b_final_dataset.npz, riyadh_graph_adjacency_matrix.npy) into four deep architectures—LineB_LSTM, LineB_Transformer, LineB_PINN (incorporating physical saltation/conservation residuals), and LineB_STGNN (6-node graph propagation)—evaluated across the identical 24 h–360 h horizons (nb03_line_b_classification_hourly.csv and nb03_line_b_regression_hourly.csv).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "Cross-Line Comparison (Table 2, Figure 6): A direct comparison reveals clear structural complementarity. For binary dust-event classification on the 2023–2024 test set, Line A calibrated tree ensembles achieve the highest ROC-AUC across all horizons—RandomForest_Cal leads at 24 h (0.8090 vs. LineB_PINN 0.7939), 72 h (0.7167 vs. LineB_Transformer 0.7158), and 168 h (0.7031 vs. LineB_PINN 0.6820), while XGBoost_Cal leads at 216 h (0.7156) and 360 h (0.7655). Conversely, for continuous PM₁₀ regression, Line B's spatiotemporal inductive bias substantially outperforms Line A: LineB_STGNN achieves the lowest test RMSE at 24 h (21.55 vs. 36.99 µg/m³), 72 h (15.58 vs. 27.63 µg/m³), and 216 h (14.86 vs. 27.68 µg/m³), while LineB_LSTM leads at 168 h (14.45 µg/m³) and 360 h (14.13 µg/m³).",
        "Normal",
        doc,
    )
    add_table_before(ch4_el, TABLE_2, "Table 2: Direct out-of-sample comparison of Line A vs. Line B on the 2023–2024 test set (nb02 & nb03 hourly results)", doc)
    add_figure_before(ch4_el, FIG_DIR / "nb02_fig02.png", "Figure 5: Main Line A calibrated classification ROC-AUC across validation (2022) and test (2023–2024) partitions from 24 h to 360 h.", doc)
    add_figure_before(ch4_el, FIG_DIR / "nb03_fig05.png", "Figure 6: Direct Line A vs. Line B comparison of best Test ROC-AUC and Test RMSE across 1–15 day horizons (03_line_b_pytorch_real_layers.ipynb).", doc)

    # 3.6 Explainable AI & Operational Early-Warning Matrix
    add_para_before(ch4_el, "3.6 Explainable AI Diagnostics and Municipal Warning Framework", "Heading 2", doc)
    add_para_before(
        ch4_el,
        "To verify physical plausibility and diagnose regime-shift sensitivity across both modelling lines, 04_explainable_ai_xai_riyadh.ipynb computes SHAP values, permutation ROC-AUC drops, 1D/2D partial dependence (PDP/ICE), PyTorch LSTM 24-hour lookback saliency, and 6-node graph weighted degree (Figure 7; nb04_xai_clean_hourly_importance.csv). Finally, calibrated forecast probabilities and PM₁₀ estimates map directly to the four-tier municipal emergency action matrix for Greater Riyadh (Table 3).",
        "Normal",
        doc,
    )
    add_figure_before(ch4_el, FIG_DIR / "nb04_fig01.png", "Figure 7: Explainable AI (SHAP mean |impact| and test permutation ROC-AUC drop) linking forecast decisions to physical dust drivers (04_explainable_ai_xai_riyadh.ipynb).", doc)
    add_table_before(ch4_el, TABLE_3, "Table 3: Four-tier municipal early-warning action matrix for Greater Riyadh", doc)

    try:
        doc.save(str(DOC_PATH))
        print(f"Successfully rebuilt Chapter 3 in {DOC_PATH.name}!")
    except PermissionError:
        alt = DOC_PATH.with_name(DOC_PATH.stem + "_CH3_UPDATED.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
