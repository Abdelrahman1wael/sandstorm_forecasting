from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
DOC_PATH = ROOT / "01_Documentation" / "FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver4.docx"
FIG_DIR = ROOT / "07_Figures"

TABLE_4_CV = [
    ["Horizon", "Days", "LogReg_Bal", "RandomForest", "ExtraTrees", "HistGB", "XGBoost"],
    ["24 h", "1", "0.8527", "0.8611", "0.8598", "0.8469", "0.8619"],
    ["72 h", "3", "0.7875", "0.8047", "0.8097", "0.7832", "0.8030"],
    ["168 h", "7", "0.7871", "0.7822", "0.7992", "0.7509", "0.7630"],
    ["216 h", "9", "0.7937", "0.7753", "0.8043", "0.7278", "0.7476"],
    ["360 h", "15", "0.8052", "0.8052", "0.8447", "0.7615", "0.7754"],
]

TABLE_5_LINE_A = [
    ["Horizon", "Best Line A Model", "Val ROC-AUC", "Test ROC-AUC", "Test PR-AUC", "Test BSS", "Lift@Top10%", "Persistence ROC"],
    ["24 h (1 d)", "RandomForest_Cal", "0.8368", "0.8090", "0.3143", "0.3218", "4.28×", "0.5701"],
    ["72 h (3 d)", "RandomForest_Cal", "0.7590", "0.7167", "0.3838", "0.2724", "2.67×", "0.5451"],
    ["168 h (7 d)", "RandomForest_Cal", "0.6893", "0.7031", "0.5657", "0.1763", "2.03×", "0.5436"],
    ["216 h (9 d)", "XGBoost_Cal", "0.6777", "0.7156", "0.6522", "0.0301", "1.77×", "0.5410"],
    ["360 h (15 d)", "XGBoost_Cal", "0.7224", "0.7655", "0.8311", "0.1313", "1.67×", "0.4721"],
]

TABLE_6_LINE_B = [
    ["Horizon", "Best Cls Model", "Test ROC-AUC", "Test PR-AUC", "Test BSS", "Best Reg Model", "Test RMSE (μg/m³)", "Test MAE (μg/m³)"],
    ["24 h (1 d)", "LineB_PINN", "0.7939", "0.2745", "0.2159", "LineB_STGNN", "21.55", "6.90"],
    ["72 h (3 d)", "LineB_Transformer", "0.7158", "0.3465", "0.2571", "LineB_STGNN", "15.58", "7.09"],
    ["168 h (7 d)", "LineB_PINN", "0.6820", "0.5402", "0.2395", "LineB_LSTM", "14.45", "8.76"],
    ["216 h (9 d)", "LineB_Transformer", "0.7065", "0.6466", "0.2467", "LineB_STGNN", "14.86", "10.11"],
    ["360 h (15 d)", "LineB_Transformer", "0.6817", "0.7739", "0.1603", "LineB_LSTM", "14.13", "10.43"],
]

TABLE_7_XAI = [
    ["Rank", "Feature", "XGB Gain", "XGB Perm ROC", "Mean |SHAP|"],
    ["1", "sin_doy", "0.06113", "0.16749", "0.71245"],
    ["2", "dust_rate_4320h", "0.01446", "0.00563", "0.52050"],
    ["3", "hours_since_dust", "0.01461", "0.01524", "0.24132"],
    ["4", "dust_rate_720h", "0.01538", "-0.00183", "0.17698"],
    ["5", "era5_soil_moisture_7_to_28cm", "0.01607", "-0.01419", "0.12351"],
    ["6", "era5_soil_moisture_0_to_7cm", "0.03189", "0.00299", "0.10673"],
    ["7", "cos_doy", "0.01515", "-0.00612", "0.09449"],
    ["8", "sat_retrieved_pm10_detrended_z", "0.03097", "0.00133", "0.08923"],
    ["9", "phys_vpd_kpa_roll168h", "0.01596", "0.00474", "0.08831"],
    ["10", "gust", "0.01465", "-0.00796", "0.07611"],
]


def add_para_before(anchor_el, text, style_name, doc):
    new_p = OxmlElement("w:p")
    anchor_el.addprevious(new_p)
    p = doc.paragraphs[0].__class__(new_p, doc._body)
    if style_name in [s.name for s in doc.styles]:
        p.style = doc.styles[style_name]
    run = p.add_run(text)
    if style_name == "Normal":
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
    return p


def add_table_before(anchor_el, rows, caption, doc):
    cap = add_para_before(anchor_el, caption, "Normal", doc)
    cap.runs[0].bold = True
    cap.runs[0].font.size = Pt(10)
    tbl = doc.add_table(rows=len(rows), cols=len(rows[0]))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = str(val)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)
                    if r_idx == 0:
                        r.bold = True
    anchor_el.addprevious(tbl._tbl)
    add_para_before(anchor_el, "", "Normal", doc)


def add_figure_with_desc_before(anchor_el, img_path: Path, caption: str, description: str, doc, width=6.1):
    p_img = add_para_before(anchor_el, "", "Normal", doc)
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(str(img_path), width=Inches(width))
    cap = add_para_before(anchor_el, caption, "Normal", doc)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(10)
    add_para_before(anchor_el, description, "Normal", doc)


def main():
    doc = Document(str(DOC_PATH))
    body = doc.element.body

    # Add description below Figure 11 in Section 3.9.3 if not already added
    fig11_idx = next(
        (i for i, p in enumerate(doc.paragraphs) if p.text.strip().startswith("Figure 11:")),
        None,
    )
    if fig11_idx is not None and fig11_idx + 1 < len(doc.paragraphs):
        next_txt = doc.paragraphs[fig11_idx + 1].text.strip()
        if next_txt.startswith("Chapter 4"):
            add_para_before(
                doc.paragraphs[fig11_idx + 1]._p,
                "As shown in Figure 11, input-gradient temporal saliency across the 24-hour LSTM lookback window increases monotonically toward the forecast origin, rising from near-zero weights at Lag -23 h to -10 h up to 0.0023 at Lag -2 h, 0.0037 at Lag -1 h, and 0.0088 at Lag 0 h. This confirms that the recurrent hidden state prioritizes immediate pre-event meteorological and particulate conditions while retaining weak long-range context.",
                "Normal",
                doc,
            )

    ch4_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Chapter 4" in p.text)
    ch5_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Chapter 5" in p.text)

    ch4_el = doc.paragraphs[ch4_idx]._p
    ch5_el = doc.paragraphs[ch5_idx]._p

    # Remove all body elements strictly between Chapter 4 heading and Chapter 5 heading
    to_remove = []
    cur = ch4_el.getnext()
    while cur is not None and cur is not ch5_el:
        to_remove.append(cur)
        cur = cur.getnext()
    for el in to_remove:
        body.remove(el)

    # 4.1 Experimental Protocol
    add_para_before(ch5_el, "4.1 Experimental Protocol and Chronological Split Verification", "Heading 2", doc)
    add_para_before(
        ch5_el,
        "All evaluations in Notebooks 02, 03, and 04 strictly respect temporal causality on the 86,928-hour clean master dataset (riyadh_hourly_clean_tvt.csv, 2015–2024; 115 features). A 360-hour (15-day) purge gap separates the 70% training partition (2015–2021; 7.47% dust prevalence), the 15% validation partition (2022; 10.51% dust prevalence), and the 15% out-of-sample test partition (2023–2024; 1.79% dust prevalence). Every model is evaluated across five multi-day horizons H in {24, 72, 168, 216, 360} h (1 to 15 days) and three random seeds {42, 123, 456}.",
        "Normal",
        doc,
    )

    # 4.2 Main Line A Evaluation
    add_para_before(ch5_el, "4.2 Main Line A: 5-Fold CV and Independent 2023–2024 Tabular Evaluation", "Heading 2", doc)
    add_para_before(
        ch5_el,
        "Inside the 70% training partition, 5-fold rolling-origin cross-validation (Table 4; Figure 12) confirms consistent skill across all five horizons, led by XGBoost at 24 h (0.8619) and ExtraTrees across 72–360 h (0.8097 at 72 h, 0.7992 at 168 h, 0.8043 at 216 h, and 0.8447 at 360 h).",
        "Normal",
        doc,
    )
    add_table_before(ch5_el, TABLE_4_CV, "Table 4: Main Line A 5-fold rolling-origin CV ROC-AUC on clean hourly training data (nb02_line_a_5fold_cv_hourly.csv)", doc)
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb02_fig01.png",
        "Figure 12: Main Line A 5-fold rolling-origin cross-validation ROC-AUC across 24 h to 360 h.",
        "Figure 12 plots 5-fold rolling-origin cross-validation ROC-AUC over 1, 3, 7, 9, and 15 days for five tabular classifiers. All models cluster tightly at 24 h (0.8469–0.8619), after which ExtraTrees (green) maintains the highest discrimination across 72–360 h (0.7992–0.8447), whereas HistGB and XGBoost dip at 7–9 days before recovering at 15 days as cumulative window prevalence rises.",
        doc,
    )

    add_para_before(
        ch5_el,
        "On the untouched 2023–2024 test partition (Table 5; Figures 13–17), RandomForest_Cal achieves the highest ROC-AUC at 24 h (0.8090, Lift@Top10% = 4.28×), 72 h (0.7167, Lift@Top10% = 2.67×), and 168 h (0.7031, Lift@Top10% = 2.03×), while XGBoost_Cal leads at 216 h (0.7156) and 360 h (0.7655, Test PR-AUC = 0.8311), substantially outperforming Persistence_Cal (0.5701 at 24 h; 0.4721 at 360 h). For continuous PM₁₀ regression (Figure 16), ExtraTrees delivers the lowest Line A ML test RMSE at 24 h (26.34 μg/m³) and 72 h (27.63 μg/m³), while Ridge_log1p leads at 168 h (29.72 μg/m³), 216 h (27.68 μg/m³), and 360 h (30.25 μg/m³).",
        "Normal",
        doc,
    )
    add_table_before(ch5_el, TABLE_5_LINE_A, "Table 5: Main Line A calibrated classification performance on the 2023–2024 test set (nb02_line_a_classification_hourly.csv)", doc)
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb02_fig02.png",
        "Figure 13: Main Line A validation (2022) vs. test (2023–2024) ROC-AUC across 1–15 day horizons.",
        "Figure 13 compares 2022 validation ROC-AUC (left) with 2023–2024 out-of-sample test ROC-AUC (right). Every calibrated ML model substantially outperforms Persistence_Cal (blue) and MonthClimo_Cal (orange) at 1–3 days; on the test set, RandomForest_Cal leads through 7 days (0.8090 to 0.7031) while XGBoost_Cal climbs to 0.7655 at 15 days as Persistence_Cal decays below 0.50.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb02_fig03.png",
        "Figure 14: Main Line A Test PR-AUC and Brier Skill Score (BSS) across 1–15 day horizons.",
        "Figure 14 presents Test PR-AUC (left) and Brier Skill Score (right). PR-AUC rises monotonically with forecast window length (reaching 0.8311 for XGBoost_Cal at 15 days) as multi-day event base rates increase. On the right, all calibrated ML models remain strictly positive above the 0.00 BSS no-skill line, led by ExtraTrees_Cal (~0.35 at 1 day) and LogReg_Bal_Cal (>0.22 out to 15 days).",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb02_fig05.png",
        "Figure 15: Main Line A 168 h (7-day) calibrated probability reliability diagram on the 2023–2024 test set.",
        "Figure 15 evaluates probability calibration at the 168 h horizon against the dashed 1:1 perfect-reliability diagonal. All four calibrated tree ensembles follow the diagonal closely across the 0.25–0.60 probability range, with RandomForest_Cal and ExtraTrees_Cal extending cleanly into the high-confidence regime (0.74–0.86 predicted vs. 0.61–1.00 observed).",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb02_fig06.png",
        "Figure 16: Main Line A continuous PM₁₀ regression Test RMSE and R² across 1–15 day horizons.",
        "Figure 16 shows continuous PM₁₀ regression Test RMSE (left) and R² (right) for Line A. ExtraTrees achieves the lowest non-trivial ML RMSE at 1 day (26.34 μg/m³) and 3 days (27.63 μg/m³), while Ridge_log1p stabilizes around 27.68–30.25 μg/m³ from 3 to 15 days. Unregularized tree models (XGBoost and RandomForest) exhibit inflated RMSE and negative R² at 7–9 days due to variance shift between 2015–2021 and 2023–2024.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb02_fig07.png",
        "Figure 17: Main Line A operational Lift@Top10% across 1–15 day horizons.",
        "Figure 17 quantifies operational alert concentration via Lift@Top10% relative to the 1.0× baseline (dashed line). At 24 h, XGBoost_Cal (~4.45×) and RandomForest_Cal (4.28×) capture more than four times the baseline dust-event rate inside the top decile of predicted risk, sustaining >2.0× lift through 7 days and ~1.67× at 15 days.",
        doc,
    )

    # 4.3 Main Line B & Cross-Line Comparison
    add_para_before(ch5_el, "4.3 Main Line B: PyTorch Spatiotemporal Evaluation and Line A vs. Line B Comparison", "Heading 2", doc)
    add_para_before(
        ch5_el,
        "Main Line B evaluates RealLSTMNet, RealTransformerNet, RealPINNNet, and RealSTGNNNet on 24-hour sequence tensors (Table 6; Figures 18–21). For event classification, LineB_PINN leads Line B at 24 h (Test ROC-AUC = 0.7939, BSS = 0.2159) and 168 h (0.6820, BSS = 0.2395), while LineB_Transformer leads at 72 h (0.7158, BSS = 0.2571), 216 h (0.7065, BSS = 0.2467), and 360 h (0.6817, PR-AUC = 0.7739). Crucially, for continuous PM₁₀ regression, Line B's spatiotemporal architectures dramatically outperform Line A ML models: LineB_STGNN achieves Test RMSE = 21.55 μg/m³ (MAE = 6.90) at 24 h, 15.58 μg/m³ at 72 h, and 14.86 μg/m³ at 216 h, while LineB_LSTM achieves 14.45 μg/m³ at 168 h and 14.13 μg/m³ at 360 h (Figure 20).",
        "Normal",
        doc,
    )
    add_table_before(ch5_el, TABLE_6_LINE_B, "Table 6: Main Line B PyTorch classification and regression performance on the 2023–2024 test set (nb03_line_b_*_hourly.csv)", doc)
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb03_fig02.png",
        "Figure 18: Main Line B 168 h training and validation loss convergence curves across PyTorch architectures.",
        "Figure 18 displays 12-epoch training (blue) and validation (orange) loss curves at 168 h for LineB_LSTM, LineB_Transformer, LineB_PINN, and LineB_STGNN. Training loss decreases smoothly across all four models (from ~0.39 to <0.15), whereas validation loss climbs after the opening epochs, demonstrating why best-validation-checkpoint selection is critical under the 2015–2021 vs. 2022 regime shift.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb03_fig03.png",
        "Figure 19: Main Line B Test ROC-AUC and Brier Skill Score (BSS) across 1–15 day horizons.",
        "Figure 19 summarizes Line B classification skill across 1–15 days. Test ROC-AUC (left) peaks at 24 h (~0.791–0.794 across all four networks, led by LineB_PINN at 0.7939), with LineB_Transformer leading at 3, 9, and 15 days (0.7158, 0.7065, 0.6817). Test BSS (right) remains solidly positive (0.12–0.26) across all horizons, with LineB_PINN sustaining ~0.20–0.25 throughout.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb03_fig04.png",
        "Figure 20: Main Line B continuous PM₁₀ Test RMSE and R² across 1–15 day horizons.",
        "Figure 20 shows Line B continuous PM₁₀ regression Test RMSE (left) and R² (right). LineB_STGNN (red) and LineB_LSTM (blue) achieve substantially lower RMSE (14.13–21.55 μg/m³) and far more stable R² than LineB_Transformer (21.5–25.7 μg/m³), confirming that graph-spatial coupling and recurrent gating suppress extreme concentration drift.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb03_fig05.png",
        "Figure 21: Cross-Line Comparison — Best Test ROC-AUC and Best Test RMSE (1–15 day horizons).",
        "Figure 21 directly compares Main Line A and Main Line B PyTorch across 1–15 days. For event classification (left), Line A retains a slight ROC-AUC advantage (0.8090 vs. 0.7939 at 1 d; 0.7655 vs. 0.6817 at 15 d). For regression (right), Line A's plotted minimum corresponds to the constant Trivial_Median baseline (11.8–20.9 μg/m³), whereas among predictive ML/DL models, Line B (14.13–21.55 μg/m³) decisively outperforms Line A (26.34–30.25 μg/m³).",
        doc,
    )

    # 4.4 Explainable AI Results
    add_para_before(ch5_el, "4.4 Explainable AI (XAI) Multi-Method Attribution & Physical Evidence", "Heading 2", doc)
    add_para_before(
        ch5_el,
        "Notebook 04 (04_explainable_ai_xai_riyadh.ipynb) executes XAI-1 through XAI-6 on the 168 h clean hourly test set (Table 7; Figures 22–28). Across global gain, permutation ROC-AUC drop, and exact shap.TreeExplainer attributions (Figure 22), the top 10 predictors by Mean |SHAP| are sin_doy (0.71245), dust_rate_4320h (0.52050), hours_since_dust (0.24132), dust_rate_720h (0.17698), era5_soil_moisture_7_to_28cm (0.12351), era5_soil_moisture_0_to_7cm (0.10673), cos_doy (0.09449), sat_retrieved_pm10_detrended_z (0.08923), phys_vpd_kpa_roll168h (0.08831), and gust (0.07611).",
        "Normal",
        doc,
    )
    add_table_before(ch5_el, TABLE_7_XAI, "Table 7: Top 10 predictors at 168 h ranked by Mean |SHAP| on the clean hourly test set (nb04_xai_clean_hourly_importance.csv)", doc)
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb04_fig01.png",
        "Figure 22: XAI-1 & XAI-2 — Global SHAP Mean |Impact| vs. ExtraTrees Test Permutation ROC-AUC drop.",
        "Figure 22 contrasts global exact Mean |SHAP| (left, blue) with ExtraTrees out-of-sample permutation ROC-AUC drop (right, green) for the top 12 predictors at 168 h. Seasonal phase (sin_doy) dominates both criteria (Mean |SHAP| = 0.71245; Perm ROC Drop ≈ +0.0306), followed by 180-day and 30-day dust-memory rates (dust_rate_4320h, hours_since_dust, dust_rate_720h), ERA5 soil moisture, and phys_vpd_kpa_roll168h (+0.0054 permutation drop).",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb04_fig02.png",
        "Figure 23: XAI-2 — Directional SHAP beeswarm scatter plot for the top 10 clean hourly features.",
        "Figure 23 maps standardized feature values (blue = low, red = high) against signed SHAP log-odds contributions. High sin_doy (spring–summer shamal season, red) and high wind gust (red) push dust risk strongly positive (+0.5 to +1.5), whereas winter sin_doy (blue) pushes log-odds sharply negative (down to -3.0). High hours_since_dust and low dust_rate_4320h also shift predictions positively, reflecting synoptic-seasonal regime conditioning.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb04_fig03.png",
        "Figure 24: Modality-level SHAP attribution share (%) across ground, calendar, ERA5, satellite, and CAMS groups.",
        "Figure 24 aggregates feature-level Mean |SHAP| into five physical data modalities. Ground_METAR (~37.4%) and Calendar_Diurnal (~32.2%) account for nearly 70% of total model attribution, followed by ERA5_Physics (~23.5%), Satellite_Detrended (~4.7%), and CAMS_NWP_Detrended (~1.8%), confirming that local surface observations and seasonal-diurnal cycles govern predictive skill far more than detrended NWP dust fields.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb04_fig04.png",
        "Figure 25: Local SHAP explanation on the highest-risk 2023–2024 test timestamp (2024-06-20 04:00:00).",
        "Figure 25 decomposes the local prediction at the peak-risk test timestamp (2024-06-20 04:00:00 UTC). Positive risk is driven primarily by pm10_calibrated_ugm3 (+1.10), dust_rate_4320h (+0.54), sin_doy (+0.38), cos_doy (+0.31), has_wxcode (+0.27), pm10_clean_ugm3 (+0.26), dust_rate_720h (+0.25), and reduced visibility vsby (+0.20), demonstrating physically coherent alignment between real-time surface degradation and shamal seasonality.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb04_fig05.png",
        "Figure 26: XAI-3 — 1D Partial Dependence (PDP) and ICE curves for the top four clean hourly drivers.",
        "Figure 26 overlays Individual Conditional Expectation curves (thin lines) with the global Partial Dependence average (dashed line) for the top four drivers. While sin_doy shows a clear monotonic upward slope (from ~0.45 at -1.4 to ~0.59 at +1.4) across all test samples, dust_rate_4320h, hours_since_dust, and dust_rate_720h display nearly flat marginal averages with sample-dependent baseline offsets.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb04_fig06.png",
        "Figure 27: XAI-3 — 2D Partial Dependence interaction surface for sin_doy vs. dust_rate_4320h.",
        "Figure 27 visualizes the joint 2D Partial Dependence surface between sin_doy and dust_rate_4320h. Predicted probability contours rise smoothly from 0.44 (upper-left) to >0.57 (right) as sin_doy increases, while the diagonal bending of contour lines above dust_rate_4320h > -1.8 reveals a non-linear interaction between seasonal phase and 180-day dust-regime memory.",
        doc,
    )
    add_figure_with_desc_before(
        ch5_el,
        FIG_DIR / "nb04_fig09.png",
        "Figure 28: XAI-6 — Multi-horizon SHAP importance shift from 24 h to 168 h to 360 h.",
        "Figure 28 tracks Mean |SHAP| across 24 h (blue), 168 h (orange), and 360 h (green) for the top eight features. Seasonal phase (sin_doy, rising from ~0.19 at 24 h to ~1.37 at 360 h), long-range dust memory (dust_rate_4320h, hours_since_dust), and deep soil moisture (era5_soil_moisture_7_to_28cm) gain importance at longer lead times, whereas short-term satellite anomaly (sat_retrieved_pm10_detrended_z) peaks at 24 h (~0.18) and decays by 360 h.",
        doc,
    )

    try:
        doc.save(str(DOC_PATH))
        print(f"Rebuilt Chapter 4 + XAI descriptions in {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver5.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
