"""Generate 01_Documentation/USTB_Midterm_Report_Riyadh_Sandstorm_Forecasting.docx.

Follows the exact USTB Master's Midterm Report template structure while staying
concise, technical, and grounded strictly in 06_Data/results/*.csv and 07_Figures/*.png.
"""

from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import pandas as pd

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
OUT_DOCX = ROOT / "01_Documentation" / "USTB_Midterm_Report_Riyadh_Sandstorm_Forecasting.docx"
RES_DIR = ROOT / "06_Data" / "results"
FIG_DIR = ROOT / "07_Figures"


def add_sup_cite(p, nums: str) -> None:
    r = p.add_run(f"[{nums}]")
    r.font.superscript = True


def add_para(doc: docx.Document, text: str = "", bold_prefix: str = "", style: str = "Normal"):
    p = doc.add_paragraph(style=style)
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.bold = True
    if text:
        p.add_run(text)
    return p


def add_table(doc: docx.Document, headers: list[str], rows: list[list[str]]):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    for j, h in enumerate(headers):
        cell = tbl.rows[0].cells[j]
        cell.text = ""
        r = cell.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            cell = tbl.rows[i].cells[j]
            cell.text = ""
            r = cell.paragraphs[0].add_run(str(val))
            r.font.size = Pt(9)
    return tbl


def add_figure(doc: docx.Document, fig_name: str, caption: str, width_in: float = 5.6):
    p_path = FIG_DIR / fig_name
    if not p_path.exists():
        raise FileNotFoundError(f"Missing figure in 07_Figures: {p_path}")
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(str(p_path), width=Inches(width_in))
    p_cap = doc.add_paragraph(caption)
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p_cap.runs:
        r.italic = True
        r.font.size = Pt(9)


def main() -> None:
    cv_df = pd.read_csv(RES_DIR / "nb02_line_a_5fold_cv_hourly.csv")
    la_cls = pd.read_csv(RES_DIR / "nb02_line_a_classification_hourly.csv")
    la_reg = pd.read_csv(RES_DIR / "nb02_line_a_regression_hourly.csv")
    lb_cls = pd.read_csv(RES_DIR / "nb03_line_b_classification_hourly.csv")
    lb_reg = pd.read_csv(RES_DIR / "nb03_line_b_regression_hourly.csv")
    xai_df = pd.read_csv(RES_DIR / "nb04_xai_clean_hourly_importance.csv")

    doc = docx.Document()
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(10.5)

    # =========================================================================
    # COVER PAGE (USTB Midterm Report Template)
    # =========================================================================
    for line, size, bold in [
        ("北 京 科 技 大 学", 20, True),
        ("硕士学位研究生", 18, True),
        ("中期报告", 22, True),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(line)
        r.bold = bold
        r.font.size = Pt(size)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt = p_title.add_run(
        "论文题目：Applying Machine Learning Algorithms to Improve the Accuracy of "
        "Medium- to Long-Term Sand and Dust Storm Forecasting in Riyadh"
    )
    rt.bold = True
    rt.font.size = Pt(13)

    meta_rows = [
        ["指 导 教 师：", "Prof. Zhang Wei (张伟 教授)"],
        ["单       位：", "School of Economics and Management / 环境科学与工程系"],
        ["学       号：", "202461024"],
        ["作       者：", "Yuyan (语嫣)"],
        ["专 业 名 称：", "Environmental Engineering (环境工程)"],
        ["入 学 时 间：", "September 2024"],
        ["报 告 日 期：", "November 2026"],
    ]
    add_table(doc, ["Field", "Value"], meta_rows)
    doc.add_page_break()

    # =========================================================================
    # FRONT MATTER: Figure/Table List, Abbreviations, Terminology
    # =========================================================================
    doc.add_heading("Figure and Table", level=1)
    add_para(doc, "Figures (all sourced exclusively from 07_Figures/):")
    for item in [
        "Figure 3.1: 10 km METAR visibility cap and 53.7 ug/m3 floor distribution (nb00_fig02.png)",
        "Figure 3.2: Annual dust event rate vs. satellite PM10 drift, 2015–2024 (nb00_fig03.png)",
        "Figure 3.3: Daily visibility proxy vs. KAPSARC 9-station ground sensor (nb00_fig05.png)",
        "Figure 3.4: Clean hourly feature impact — 168 h MI and 5-fold Ridge stability (nb01_fig03.png)",
        "Figure 3.5: Line A Validation vs. Test ROC-AUC across 1–15 day horizons (nb02_fig02.png)",
        "Figure 3.6: Line A vs. Line B PyTorch benchmark across 1–15 days (nb03_fig05.png)",
        "Figure 3.7: XAI SHAP Mean |Impact| vs. Test permutation ROC drop (nb04_fig01.png)",
        "Figure 3.8: XAI SHAP importance shift from 24 h to 360 h horizons (nb04_fig09.png)",
    ]:
        add_para(doc, item, style="List Bullet")

    doc.add_heading("Abbreviation and Symbol", level=1)
    add_table(
        doc,
        ["Abbreviation", "Full Term / Definition"],
        [
            ["AOD / CAMS", "Aerosol Optical Depth (550 nm) / Copernicus Atmosphere Monitoring Service"],
            ["BLH / ERA5", "Boundary-Layer Height (m) / ECMWF Fifth-Generation Reanalysis"],
            ["BSS / PR-AUC", "Brier Skill Score (vs. train climatology) / Precision-Recall Area Under Curve"],
            ["KKIA (OERK)", "King Khalid International Airport, Riyadh (METAR ICAO station OERK)"],
            ["PINN / ST-GNN", "Physics-Informed (Physics-Guided) Neural Network / Spatiotemporal Graph Neural Network"],
            ["ROC-AUC / Lift@10%", "Receiver Operating Characteristic AUC / Event recall enrichment in top-10% alerts"],
            ["SHAP / XAI", "SHapley Additive exPlanations / Explainable Artificial Intelligence"],
        ],
    )

    doc.add_heading("Terminology", level=1)
    add_table(
        doc,
        ["Term", "Operational Definition in This Study"],
        [
            ["Clean Dust Event", "Binary hazard label: clean_dust_event = (is_dust_event == 1) | (visibility_km < 5.0)."],
            ["De-Censored PM10", "Continuous target replacing the 53.7 ug/m3 10 km METAR floor with wind/BLH background."],
            ["360 h Purge Gap", "15-day temporal buffer separating Train/Val/Test and CV folds to block target-window overlap."],
            ["Regime Shift", "2022–2024 drop in Riyadh dust prevalence (7.47% Train -> 0.94% Test) causing mean over-prediction."],
        ],
    )
    doc.add_page_break()

    # =========================================================================
    # 1 INTRODUCTION
    # =========================================================================
    doc.add_heading("1 Introduction", level=1)
    doc.add_heading("1.1 Research Title and Problem Statement", level=2)
    p = add_para(
        doc,
        "Applying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm "
        "Forecasting. Sand and dust storms (SDS) in Riyadh severely degrade aviation safety, solar power output, "
        "and respiratory health. While numerical weather prediction (NWP) captures short-range synoptic transport, "
        "its skill decays rapidly across medium- to long-range horizons (1–15 days, 24 h–360 h)",
        bold_prefix="Research Title: ",
    )
    add_sup_cite(p, "1,2")
    p.add_run(
        ". Simultaneously, Riyadh's observational record suffers from four structural defects: (i) a 10 km METAR "
        "visibility cap that censors 78.1% of hours into a flat 53.7 ug/m3 floor; (ii) a severe 2022–2024 climatic "
        "regime shift (dust prevalence drops from 7.47% in 2015–2021 to 0.94% in 2023–2024); (iii) 100% missingness "
        "in mslp and 92.27% clear-sky sparsity in wxcodes; and (iv) slow drift and redundancy in satellite/CAMS "
        "products. Without causal repair and leakage-safe validation, ML models either memorize regime noise or fail "
        "catastrophically in operational deployment."
    )

    doc.add_heading("1.2 Research Objectives", level=2)
    for bp, txt in [
        ("1. Leakage-Safe Multi-Modal Dataset: ", "Construct an hourly 2015–2024 benchmark (86,928 clean hours, 115 causal features, 10 targets) fusing METAR, ERA5, satellite AOD, and CAMS."),
        ("2. Causal Data Repair: ", "Eliminate the 53.7 ug/m3 visibility floor via physical wind/BLH de-censoring and neutralize satellite/CAMS drift via causal 4,320 h rolling z-scores."),
        ("3. Calibrated 1–15 Day Forecasting: ", "Benchmark classical tabular ensembles (Line A) against real PyTorch sequence, physics-guided, and graph architectures (Line B) under strict 360 h purge gaps."),
        ("4. Class-Imbalance & Bias Correction: ", "Evaluate cost-sensitive weighting, SMOTE vs. class-weighted loss, and validation-set Platt probability calibration."),
        ("5. Physical Explainability (XAI): ", "Triangulate predictions using SHAP, permutation drop, PDP/ICE, and surrogate rules to separate genuine synoptic skill from seasonal climatology."),
    ]:
        add_para(doc, txt, bold_prefix=bp, style="List Bullet")

    # =========================================================================
    # 2 LITERATURE REVIEW
    # =========================================================================
    doc.add_heading("2 Literature Review", level=1)
    doc.add_heading("2.1 Regional Saudi & GCC Dust Forecasting Benchmarks", level=2)
    p = add_para(
        doc,
        "Regional machine learning studies establish strong precedent for tree ensembles, deep sequence models, "
        "and visibility-PM10 coupling across Saudi Arabia, yet expose clear methodological gaps"
    )
    add_sup_cite(p, "3-8")
    p.add_run(":")
    add_table(
        doc,
        ["Regional Study", "Data & Horizon", "Algorithms & Key Finding", "Gap Addressed Here"],
        [
            ["KKIA Riyadh Low-Visibility [3]", "Hourly OERK (2015–2017)", "RF & KNN; PM10 importance ~52%; oversampling", "Extended to 2015–2024 & 1–15 d horizons with 360 h purge gaps."],
            ["Saudi Dust Frequency (2024) [4]", "Riyadh/Jeddah/Dammam monthly", "SVR, GBRT, LSTM, TCN on 62 predictors", "Tested at hourly resolution with strict Line A vs. Line B parity."],
            ["Makkah TabNet + SHAP [5]", "Daily PM10 (Makkah)", "TabNet + SHAP (pressure, humidity, temp)", "Expanded to 6-method XAI + horizon shift (24 h -> 360 h)."],
            ["GCC Visibility ML (2025) [6]", "GCC dust monitoring", "LR, SVM-RBF, ANN; SVM-RBF strongest", "Validates visibility–PM10 proxy link against KAPSARC."],
            ["Saudi Deep PM10 [7]", "KSA air quality", "LSTM sequence modeling", "Benchmarked vs. Transformer, Physics-Guided GRU, ST-GNN."],
            ["Denoising AI PM10 (2024) [8]", "KSA environmental series", "Hybrid denoising + ANN", "Replaced with causal 4,320 h z-scores to prevent future leakage."],
        ],
    )

    doc.add_heading("2.2 Methodological Foundations & Identified Research Gap", level=2)
    p = add_para(
        doc,
        "Standard time-series cross-validation requires temporal purging to prevent autocorrelation leakage"
    )
    add_sup_cite(p, "9,10")
    p.add_run(
        ". On medium-sized tabular Earth-system datasets (~10k–100k samples), regularized tree ensembles "
        "(Random Forest, Extra-Trees, XGBoost)"
    )
    add_sup_cite(p, "11-13")
    p.add_run(" frequently match or outperform deep sequence networks")
    add_sup_cite(p, "14,15")
    p.add_run(
        ". However, prior Saudi dust studies lack: (1) unified 4-modality hourly fusion over 10 years, "
        "(2) explicit de-censoring of the 10 km METAR floor, (3) 360 h purge gaps under regime shift, and "
        "(4) calibrated probabilistic alerts paired with multi-method XAI"
    )
    add_sup_cite(p, "16,17")
    p.add_run(".")

    # =========================================================================
    # 3 RESEARCH MATERIALS AND METHODOLOGY
    # =========================================================================
    doc.add_heading("3 Research Materials and Methodology", level=1)
    add_para(
        doc,
        "The research is engineered as a connected five-phase pipeline (Notebooks 00–04 in 04_Notebooks/, "
        "automated in 08_Scripts/05_evaluation_and_plotting/build_and_run_clean_hourly_notebooks.py), where "
        "every preprocessing and modeling choice in Phase k+1 is directly justified by quantitative diagnostics in Phase k."
    )

    # 3.1 Data Sources & Examination (NB00)
    doc.add_heading("3.1 Phase 1: Riyadh Data Sources, Examination & Diagnosed Defects (NB00)", level=2)
    p = add_para(
        doc,
        "Two primary representations are used: (1) riyadh_line_a_tabular_features.csv (87,456 hourly rows x 114 columns, "
        "2015-01-02 to 2024-12-23) spanning Ground_METAR (12), ERA5_Reanalysis (23)"
    )
    add_sup_cite(p, "18")
    p.add_run(", Satellite_AOD (8), and CAMS_NWP (2)")
    add_sup_cite(p, "19")
    p.add_run(
        "; and (2) line_b_final_dataset.npz (400 multi-modal tensor samples: nwp_grid (400,6,16,16), "
        "satellite_grid (400,3,32,32), seq_features (400,24,6,12), and 6x6 adjacency). Validation against "
        "159 overlapping days of real KAPSARC 9-station ground sensors (2019–2020) confirms the daily visibility "
        "proxy correlates at Pearson r = 0.531 (Spearman rho = 0.566) versus raw CAMS r = 0.240 (rho = 0.322). "
        "Systematic audit exposed four critical defects:"
    )
    add_table(
        doc,
        ["Defect Diagnosed (NB00)", "Quantitative Evidence", "Causal Repair Implemented (NB01)"],
        [
            ["1. Missing / Sparse Fields", "mslp is 100% NaN; wxcodes is 92.27% blank (clear-sky); 7 GIS/meta cols constant.", "Drop mslp & 7 constants; encode has_wxcode & is_severe_dust_wx (SS/DS/SA)."],
            ["2. 10 km Visibility Cap", "78.1% hours >= 9.9 km; 79.1% sit at flat 53.7 ug/m3 floor (P10–P75 = 53.7).", "Replace clear-sky floor with physical wind/BLH background (22–68 ug/m3)."],
            ["3. 2022–2024 Regime Shift", "Dust rate drops 7.47% (Train) -> 8.43% (Val) -> 0.94% (Test); AOD/CAMS drift.", "360 h purge gaps + causal 4,320 h rolling z-scores (AOD Test shift -> -0.044)."],
            ["4. Duplicate Satellite/CAMS", "sat_aod_550nm and nwp_cams_pm10 share identical r=0.1827, rho=0.3128, MI=1.3338.", "Standardize causally and document low satellite/CAMS marginal utility in XAI."],
        ],
    )
    add_figure(doc, "nb00_fig02.png", "Figure 3.1: 10 km METAR visibility cap and resulting 53.7 ug/m3 PM10 floor spike (78.1% capped).")
    add_figure(doc, "nb00_fig03.png", "Figure 3.2: Annual dust event rate (%) vs. satellite PM10 drift across 2015–2024.")
    add_figure(doc, "nb00_fig05.png", "Figure 3.3: Proxy validation against KAPSARC 9-station ground PM10 sensors (r = 0.531, rho = 0.566).")

    # 3.2 Cleaning & Feature Engineering (NB01)
    doc.add_heading("3.2 Phase 2: Data Cleaning & Causal Feature Engineering (NB01)", level=2)
    p = add_para(
        doc,
        "All repairs are strictly causal. First, clear-sky hours (visibility >= 9.9 km) are de-censored via "
        "53.7 * (wind/4)^0.25 * (800/BLH)^0.15 clipped to [22, 68] ug/m3"
    )
    add_sup_cite(p, "20")
    p.add_run(
        ", shifting quantiles from flat 53.7 to [58.7, 64.9, 68.0, 72.7]. Second, 115 causal features are "
        "engineered: cyclic harmonics (sin/cos of doy and hour), 24 h/72 h pressure/temperature/wind tendencies, "
        "24 h/72 h/168 h trailing rolling means (guided by 1–168 h ACF), and 7/30/180-day dust persistence rates "
        "(dust_rate_4320h, hours_since_dust). Third, 10 forward targets (24 h, 72 h, 168 h, 216 h, 360 h avg-PM10 "
        "and any-event) begin strictly at t+1, yielding riyadh_hourly_clean_tvt.csv (86,928 x 133). Train-only "
        "median imputation and Yeo-Johnson power transformation"
    )
    add_sup_cite(p, "21")
    p.add_run(" cut mean absolute feature skew from 2.500 to 0.669.")
    add_figure(doc, "nb01_fig03.png", "Figure 3.4: 168 h Mutual Information and 5-fold Ridge coefficient stability on clean hourly features.")

    # 3.3 Verification, Balancing, SMOTE & Bias Correction
    doc.add_heading("3.3 Phase 3: Verification Plan, Balancing (SMOTE vs. Weighting) & Bias Correction", level=2)
    p = add_para(
        doc,
        "Verification Protocol: Data are split chronologically at 6 h synoptic stride into Train (70%, 10,142 rows) "
        "-> 360 h Purge Gap -> Validation (15%, 2,114 rows) -> 360 h Purge Gap -> Held-Out Test (15%, 2,114 rows), "
        "plus 5-fold expanding-window CV inside Train (with 360 h gaps) and 3 random seeds [42, 123, 456]"
    )
    add_sup_cite(p, "9,10")
    p.add_run(". Statistical significance is tested via 7-day (28-step) block bootstrap (300 resamples)")
    add_sup_cite(p, "22")
    p.add_run(".")
    add_para(
        doc,
        "While SMOTE synthetic oversampling was evaluated in early daily prototypes to counter rare-event "
        "imbalance, interpolating between hourly synoptic neighbors distorts temporal boundaries and inflates "
        "validation optimism. Therefore, the final clean-hourly pipeline replaces SMOTE with exact cost-sensitive "
        "loss weighting: class_weight='balanced' (LogReg, RF, ExtraTrees), scale_pos_weight = N_neg/N_pos (XGBoost), "
        "and BCEWithLogitsLoss(pos_weight) (PyTorch Line B).",
        bold_prefix="Class Balancing (SMOTE vs. Cost-Sensitive Weighting): ",
    )
    p2 = add_para(
        doc,
        "Raw tree/neural logits trained on 7.47% dust prevalence over-predict probabilities on the 0.94% Test "
        "regime. We apply validation-set Platt logistic calibration"
    )
    add_sup_cite(p2, "23")
    p2.add_run(
        " to align probability reliability and apply log1p/expm1 NWP bias correction for continuous PM10. "
        "We note transparently that positive Brier Skill Score (BSS) on weak baselines partly reflects base-rate "
        "recalibration rather than ranking skill, so ROC-AUC, PR-AUC, and Lift@10% are reported alongside BSS."
    )

    # 3.4 Model Architectures, Comparison & Accuracy Explanation (NB02-NB04)
    doc.add_heading("3.4 Phase 4: Model Architectures, Line A vs. Line B Comparison & Accuracy Analysis", level=2)
    add_para(
        doc,
        "Line A (NB02) evaluates shallow, regularized tabular models (RF/ET depth=8, min_leaf=8; XGB depth=4, "
        "lr=0.05, L2=2.0; HistGB depth=5) to prevent overfitting under regime shift. Line B (NB03) trains four "
        "real PyTorch architectures on (N, 24, 115) causal sequences (12 epochs, AdamW, early stopping on Val): "
        "RealLSTMNet (2-layer LSTM, 51,697 params), RealTransformerNet (4-head self-attention, 44,689 params), "
        "RealPINNNet (physics-guided GRU adding a monotonic wind-erosion penalty 0.05*ReLU(logit(x)-logit(x_wind+0.5SD)), "
        "24,961 params), RealSTGNNNet (6-node graph + GRU, 11,441 params), plus MultiModalNPZNet (CNN+ST-GNN, 7,097 params)."
    )

    cls_rows = []
    for h in [24, 72, 168, 216, 360]:
        sa = la_cls[la_cls["Horizon_H"] == h].sort_values("Test_ROC", ascending=False).iloc[0]
        sb = lb_cls[lb_cls["Horizon_H"] == h].sort_values("Test_ROC", ascending=False).iloc[0]
        scv = cv_df[cv_df["Horizon_H"] == h].sort_values("CV_ROC", ascending=False).iloc[0]
        med = la_reg[(la_reg["Horizon_H"] == h) & (la_reg["Model"] == "Trivial_Median")].iloc[0]
        rb = lb_reg[lb_reg["Horizon_H"] == h].sort_values("RMSE").iloc[0]
        cls_rows.append([
            f"{h}h ({h//24}d)",
            f"{scv['Model']} ({scv['CV_ROC']:.4f})",
            f"{sa['Model']} ({sa['Test_ROC']:.4f})",
            f"{sa['Lift10']:.2f}x / {sa['BSS']:+.4f}",
            f"{sb['Model']} ({sb['Test_ROC']:.4f})",
            f"{med['RMSE']:.2f} vs {rb['Model']} ({rb['RMSE']:.2f})",
        ])
    add_table(
        doc,
        ["Horizon", "Train 5-Fold CV", "Best Line A (Test ROC)", "Line A Lift@10% / BSS", "Best Line B PyTorch (ROC)", "RMSE: Median vs. Best Line B"],
        cls_rows,
    )
    add_figure(doc, "nb02_fig02.png", "Figure 3.5: Line A Validation vs. Held-Out Test ROC-AUC decay (regime shift effect).")
    add_figure(doc, "nb03_fig05.png", "Figure 3.6: Line A vs. Line B PyTorch comparison across 1–15 day horizons.")

    add_para(
        doc,
        "1) Classification wins operationally: RandomForest_Cal achieves 0.8090 ROC-AUC at 24 h (Lift@10% = 4.28x, "
        "capturing ~43% of events in the top 10% alerts; 7-day block bootstrap beats persistence by +0.1598, 95% CI "
        "[+0.0683, +0.2440]). 2) Why Line A matches/beats Line B: On 10,142 synoptic rows, shallow trees outperform "
        "deep nets (consistent with Grinsztajn et al. [14]); furthermore, RealSTGNNNet received identical point features "
        "across all 6 nodes, limiting spatial gain, and MultiModalNPZNet only had 400 samples (RMSE 369.30, R2 -0.27). "
        "3) Why continuous regression fails (and when Line B helps): Due to the 7.47% -> 0.94% regime shift, "
        "models over-predict mean PM10 (168 h RF residual = -55.22 ug/m3; 80% quantile interval covers only 21.0%), "
        "yielding negative R2 across horizons. Notably, PyTorch cuts RMSE over trees at all horizons, and LineB_LSTM "
        "(14.13) beats Trivial_Median (15.45) at 360 h. 4) XAI physical mechanism (NB04): TreeExplainer SHAP ranks "
        "sin_doy (0.7125), dust_rate_4320h (0.5205), hours_since_dust (0.2413), dust_rate_720h (0.1770), and "
        "soil_moisture_7_to_28cm (0.1235) highest. A depth-3 surrogate tree matches 96.6% of XGBoost decisions, "
        "while horizon attribution (Figure 3.8) proves forecasts shift from current visibility (24 h) to seasonal "
        "climatology and long dust memory (360 h).",
        bold_prefix="Honest Accuracy Explanation: ",
    )
    add_figure(doc, "nb04_fig01.png", "Figure 3.7: NB04 XAI — Exact TreeExplainer Mean |SHAP| vs. Test Permutation ROC Drop (168 h).")
    add_figure(doc, "nb04_fig09.png", "Figure 3.8: NB04 XAI — Physical horizon shift from current observations (24 h) to seasonality/memory (360 h).")

    # 3.5 Challenges and Solutions
    doc.add_heading("3.5 Identified Challenges and Engineering Solutions", level=2)
    add_table(
        doc,
        ["Challenge", "Empirical Evidence", "Implemented / Planned Solution"],
        [
            ["10 km METAR floor", "78.1% hours capped at 53.7 ug/m3", "Wind/BLH background de-censoring; validated vs. KAPSARC (r=0.531)."],
            ["2022–2024 regime shift", "Test dust 0.94%; 21% interval coverage", "360 h purge gaps, 4,320 h z-scores, Platt calibration; add conformal prediction."],
            ["Satellite/CAMS redundancy", "Identical MI (1.3338) & low SHAP (6.5%)", "Documented openly; future upgrade to gridded spatial ERA5/CAMS fields."],
            ["Regression negative R2", "Over-prediction bias (-55.22 ug/m3)", "Focus operational deployment on calibrated event probabilities & Lift@10%."],
            ["ST-GNN shared node inputs", "400 NPZ samples; identical hourly nodes", "Feed per-station corridor features (OERK/OEGS/OEKK) in next phase."],
        ],
    )

    # =========================================================================
    # 4 TIME SCHEDULE
    # =========================================================================
    doc.add_heading("4 Time Schedule", level=1)
    add_table(
        doc,
        ["Phase", "Timeline", "Deliverables & Status"],
        [
            ["Phase 1: Literature & Data Acquisition", "Sep 2024 – Jun 2025", "Completed — 10-year METAR, ERA5, MODIS AOD, CAMS, KAPSARC collected."],
            ["Phase 2: EDA, Cleaning & Causal Features", "Jul 2025 – Mar 2026", "Completed — Notebooks 00–01; 86,928 clean hourly rows & 115 features."],
            ["Phase 3: Line A, Line B & XAI Benchmarks", "Apr 2026 – Oct 2026", "Completed — Notebooks 02–04; 360 h-gap TVT, 3 seeds, SHAP & figures."],
            ["Phase 4: Midterm Defense & Final Refinements", "Nov 2026 – Jan 2027", "In Progress — Midterm report, conformal intervals, per-node ST-GNN."],
            ["Phase 5: Final Thesis Submission & Defense", "Feb 2027 – May 2027", "Planned — Final USTB dissertation formatting and oral defense."],
        ],
    )

    # =========================================================================
    # REFERENCES (GB/T 7714 / Numbered Bracket Style)
    # =========================================================================
    doc.add_heading("References", level=1)
    refs = [
        "[1] Lorenz EN. The predictability of a flow which possesses many scales of motion. Tellus 1969;21:289–307.",
        "[2] Zhang F, Sun YQ, Magnusson L, Buizza R, Lin SJ, Chen JH, et al. What is the predictability limit of midlatitude weather? J Atmos Sci 2019;76:1077–91.",
        "[3] Alharbi B, et al. Low visibility event prediction using random forest and K-nearest neighbor methods at King Khalid International Airport, Riyadh (2015–2017).",
        "[4] Atmosphere. Monthly dust-storm frequency forecasting for Riyadh, Jeddah, and Dammam using SVR, GBRT, LSTM, and TCN. Atmosphere 2024;15(5):520.",
        "[5] Almaliki AH, Khattak A. Synergizing TabNet and SHAP for PM10 forecasting: Insights from Makkah, Saudi Arabia.",
        "[6] Dronjak L. Visibility prediction and public health risk assessment using machine learning and dust monitoring data. Sustainability 2025;17(14):6581.",
        "[7] Air pollution forecasting using deep learning. Int J Online Biomed Eng (iJOE) 2021;17(14).",
        "[8] Applicability of denoising-based artificial intelligence to forecast environmental externalities. Geosci Front 2024.",
        "[9] Bergmeir C, Hyndman RJ, Koo B. A note on the validity of cross-validation for evaluating autoregressive time series prediction. Comput Stat Data Anal 2018;120:70–83.",
        "[10] Kaufman S, Rosset S, Perlich C, Stitelman O. Leakage in data mining: Formulation, detection, and avoidance. ACM TKDD 2012;6(4):1–21.",
        "[11] Breiman L. Random forests. Mach Learn 2001;45:5–32.",
        "[12] Geurts P, Ernst D, Wehenkel L. Extremely randomized trees. Mach Learn 2006;63:3–42.",
        "[13] Chen T, Guestrin C. XGBoost: A scalable tree boosting system. Proc ACM SIGKDD 2016:785–94.",
        "[14] Grinsztajn L, Oyallon E, Varoquaux G. Why do tree-based models still outperform deep learning on typical tabular data? NeurIPS 2022.",
        "[15] Shwartz-Ziv R, Armon A. Tabular data: Deep learning is not all you need. Inf Fusion 2022;81:84–90.",
        "[16] Lundberg SM, Erion G, Chen H, DeGrave A, Prutkin JM, Nair B, et al. From local explanations to global understanding with explainable AI for trees. Nat Mach Intell 2020;2:56–67.",
        "[17] Molnar C. Interpretable Machine Learning. 2nd ed. 2022.",
        "[18] Hersbach H, Bell B, Berrisford P, Hirahara S, Horányi A, Muñoz-Sabater J, et al. The ERA5 global reanalysis. Q J R Meteorol Soc 2020;146:1999–2049.",
        "[19] Inness A, Ades M, Agustí-Panareda A, Barré J, Benedictow A, Blechschmidt AM, et al. The CAMS reanalysis of atmospheric composition. Atmos Chem Phys 2019;19:3515–56.",
        "[20] Shao Y. Physics and Modelling of Wind Erosion. 2nd ed. Springer; 2008.",
        "[21] Yeo IK, Johnson RA. A new family of power transformations to improve normality or symmetry. Biometrika 2000;87:954–9.",
        "[22] Künsch HR. The jackknife and the bootstrap for general stationary observations. Ann Stat 1989;17:1217–41.",
        "[23] Platt J. Probabilistic outputs for support vector machines. In: Advances in Large Margin Classifiers. MIT Press; 1999.",
    ]
    for r in refs:
        add_para(doc, r)

    doc.save(str(OUT_DOCX))
    print(f"Created {OUT_DOCX} successfully.")


if __name__ == "__main__":
    main()
