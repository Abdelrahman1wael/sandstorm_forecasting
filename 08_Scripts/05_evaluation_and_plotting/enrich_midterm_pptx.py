from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
PPTX_PATH = ROOT / "02_Presentation" / "Riyadh_Sandstorm_Forecasting_Midterm (1).pptx"

SLIDE_NOTES = {
    1: "Welcome the committee. Introduce the Master's mid-term report on medium- to long-term (24–360 h) sand and dust storm forecasting for Greater Riyadh under the supervision of Assoc. Prof. Wen Wei at USTB.",
    2: "Outline the six chapters: (1) motivation & Riyadh dust sources, (2) literature & gaps, (3) 86,928-h multi-modal data & dual-line Line A / Line B methodology, (4) empirical results & XAI, (5) physical realism & honest prototype limitations, and (6) conclusions & stage-two roadmap.",
    3: "Section 01 divider: transition into why sand and dust storms are a critical hazard for Riyadh.",
    4: "Highlight global scale (330M people across 151 countries) and Riyadh's specific vulnerability (1,913 km² Najd plateau at 614 m) across five sectors: respiratory health, aviation delays at KKIA, PV soiling, infrastructure, and civil-defense lead time.",
    5: "Walk through Riyadh's three source regimes: local Ad Dahna sand sea (east/north), regional Rub' al Khali (southerly winds), and remote An Nafud / Iraq cold fronts, plus Wadi Hanifa / Tuwaiq micro-topography.",
    6: "State the core thesis aim: rigorously compare calibrated tabular ML (Line A) against PyTorch sequence/graph models (Line B) on multi-modal data with physics-informed constraints and XAI.",
    7: "Show progress on the 7-phase plan (Sep 2025 – Jun 2027): Phases 1–3 (literature, data system, baselines) are complete; Phase 4 (GNN, PINN, mid-term review) is current; Phases 5–7 cover stage-two fixes, manuscript, and final defense.",
    8: "Summarize public-health (asthma, COPD, children/outdoor workers) and economic/aviation impacts in Saudi Arabia's capital.",
    9: "Explain WMO visibility-based dust severity classes and why simple historical extrapolation fails: models must separate emission controls (soil moisture, vegetation) from meteorological triggers (wind gusts, cold fronts).",
    10: "Contrast theoretical contributions (multi-source fusion, SHAP importance ranking, horizon-dependent physics) with practical value (proactive civil defense, aviation scheduling, solar-farm cleaning).",
    11: "Section 02 divider: Literature Review.",
    12: "Trace the evolution from NWP (CAMS, WRF-Chem) and classical ML (SVM, RF, XGBoost) to hybrid deep learning (LSTM, Transformer, ST-GNN, PINN) and explain why post-processing + XAI are needed.",
    13: "Note cross-domain lessons from disaster weather, wind/solar forecasting, and environmental engineering: ensemble calibration and multi-scale lag engineering consistently stabilize rare-event prediction.",
    14: "Summarize key prior dust-forecasting benchmarks and why leakage-free chronological splitting is essential when comparing against them.",
    15: "Highlight four research gaps addressed by this thesis: (1) multi-horizon 24–360 h coverage, (2) strict leakage prevention with 360 h purge gaps, (3) physics-informed constraints, and (4) unified multi-method XAI.",
    16: "Section 03 divider: Methodology & Data.",
    17: "Overview of all algorithms evaluated: Line A (LogReg_Bal, RandomForest, ExtraTrees, HistGB, XGBoost, Ridge_log1p + baselines Persistence_Cal, MonthClimo_Cal, Trivial_Median) and Line B (RealLSTMNet, RealTransformerNet, RealPINNNet, RealSTGNNNet).",
    18: "Detail the four data sources: Ground METAR (OERK/Riyadh visibility, weather codes, gusts, visibility-derived PM10 proxy), ECMWF ERA5 (soil moisture 0–7 & 7–28 cm, VPD, wind, BLH), detrended satellite retrievals, and CAMS NWP dust.",
    19: "Summarize the 86,928-hour aligned master table (riyadh_hourly_clean_tvt.csv, 2015–2024, 115 causal features) and how 6-hourly sampling (10,142 / 2,114 / 2,114) is used for model training and evaluation.",
    20: "CRITICAL SLIDE: Explain the exact chronological split: 70% train (9 Jan 2015 – 18 Dec 2021; 10,142 samples), 15% validation (2 Jan 2022 – 14 Jun 2023; 2,114), 15% test (29 Jun 2023 – 8 Dec 2024; 2,114), separated by 360 h (15-day) purge gaps. Hourly dust rate is 7.47% / 8.43% / 0.94%; 168 h event target test positive rate is 35.0%. All scalers/Yeo-Johnson/MI are fitted on train only.",
    21: "Explain the 4 data-quality problems solved: (1) 100%-missing mslp dropped, (2) 79.01% flat censoring at 53.7 ug/m3 de-censored using wind/BLH background, (3) satellite/NWP drift detrended via causal 4,320 h Z-scores clipped to [-5, 5], (4) pre-existing target_* columns purged.",
    22: "Break down the 115 causal features into four groups: Ground METAR & dust memory, ERA5 boundary-layer/soil physics, Calendar/Diurnal harmonics, and Detrended Satellite/CAMS channels.",
    23: "Contrast Line A (tabular ensembles + Platt/isotonic calibration) vs. Line B (24-hour sequence tensors into PyTorch LSTM, Transformer, PINN, and ST-GNN).",
    24: "Walk through the end-to-end pipeline from raw ingestion and causal cleaning (Notebook 01) through Line A (Notebook 02), Line B (Notebook 03), XAI (Notebook 04), and model export.",
    25: "Detail Line A hyperparameters and calibration: LogReg_Bal, RandomForest/ExtraTrees, HistGB, XGBoost with class_weight/pos_weight (no SMOTE), and Ridge_log1p for regression.",
    26: "Explain Line B training setup (AdamW lr=1.5e-3, wd=1e-3, batch 128, BCEWithLogits with pos_weight, L1 on ln(PM10+1)) and the RealPINNNet wind-monotonicity penalty: 0.05 * mean(ReLU(f(x) - f(x + 0.5*e_wind))).",
    27: "Clarify the 6-node graph structure in RealSTGNNNet (row-normalized adjacency A_norm, 8-d node embeddings). Explicitly note that in this mid-term prototype, identical station features are broadcast to all 6 nodes; multi-station inputs are scheduled for Stage 2.",
    28: "Introduce the six-module XAI suite (XAI-1 to XAI-6): Gain/Gini, Permutation ROC-AUC drop, exact TreeSHAP, 1D/2D PDP & ICE, PyTorch LSTM temporal saliency, and 24 h -> 360 h importance shift.",
    29: "Review the experimental protocol: 5 horizons H in {24, 72, 168, 216, 360} h, 3 seeds {42, 123, 456}, event target 'visibility < 5 km at least once in next H hours', regression target 'mean PM10 proxy over next H hours', and metrics (ROC-AUC, PR-AUC, BSS, Lift@Top10%, RMSE, MAE, R2).",
    30: "Walk through the four diagnostic plots (Figures 3.1–3.4): diurnal/monthly Shamal peak, OERK NW wind rose, missingness audit, and the 79.01% raw PM10 censoring spike at 53.7 ug/m3.",
    31: "Walk through Figures 3.6–3.8: before/after de-censoring, train-only Yeo-Johnson skewness reduction, and train-only Mutual Information + 5-fold CV baseline.",
    32: "Present the 5-tier PM10 hazard thresholds and 4-tier municipal action matrix linking forecast probabilities to NCEC, PV, school/ER, and KKIA/GACA actions.",
    33: "Section 04 divider: Results and Validation.",
    34: "Highlight Line A classification performance: Line A beats MonthClimo_Cal at every horizon (0.809 vs 0.643 at 24 h; 0.717 vs 0.641 at 72 h; 0.703 vs 0.658 at 168 h; 0.716 vs 0.666 at 216 h; 0.766 vs 0.665 at 360 h), with 4.28x Lift@Top10% at 24 h and 0.8311 PR-AUC at 360 h.",
    35: "Explain Figure 4.4 (168 h reliability diagram), PR-AUC, and Brier Skill Score (0.0301–0.3218, all > 0). Emphasize that gains beyond 7 days are small, consistent with largely seasonal predictability.",
    36: "Present Line B results: LineB_PINN leads Line B at 24 h (0.7939) and 168 h (0.6820); LineB_Transformer leads at 72 h (0.7158), 216 h (0.7065), and 360 h (0.6817). State honestly that all regression models have negative R2 and Trivial_Median beats Line B at 24–216 h (11.8 vs 14.5 at 168 h), with Line B lower only at 360 h (14.1 vs 15.5).",
    37: "Head-to-head comparison: Line A leads binary classification at all 5 horizons; neither line demonstrates continuous regression skill over Trivial_Median at 24–216 h.",
    38: "Highlight the key XAI finding at 168 h: Ground_METAR (~37.4%), Calendar_Diurnal (~32.2%), and ERA5_Physics (~23.5%) supply >93% of attribution, led by sin_doy (0.71245) and dust_rate_4320h (0.52050), while detrended Satellite (~4.7%) and CAMS (~1.8%) contribute minimally.",
    39: "Walk through directional beeswarm (high sin_doy and gusts push risk positive; winter sin_doy down to -3.0), local waterfall on 2024-06-20 04:00:00 (+1.10 from pm10_calibrated_ugm3), and 24 h -> 360 h shift.",
    40: "Discuss Table 4.1 & Figure 4.1: 5-fold rolling-origin CV inside the 70% training split (XGBoost 0.8619 at 24 h; ExtraTrees 0.7992–0.8447 across 72–360 h).",
    41: "Discuss Figures 4.5, 4.7–4.9: Line A unregularized trees overfit regression under regime shift (RMSE >79–104 at 7–9 d); Line B validation loss rises after early epochs, requiring best-val checkpointing.",
    42: "Discuss Figures 4.2, 4.3, 4.10: validation vs test ROC-AUC, rising PR-AUC with window length, and cross-line comparison showing Trivial_Median's RMSE baseline.",
    43: "Discuss XAI-3 (Figures 4.11, 4.15, 4.16): 1D PDP/ICE shows monotonic positive sin_doy slope (0.45 to 0.59), and 2D PDP shows non-linear interaction between sin_doy and dust_rate_4320h above -1.8.",
    44: "Review Table 4.4 (Top 10 predictors at 168 h by Mean |SHAP|) and Figure 4.17 (24 h -> 360 h shift: sin_doy rises from ~0.19 to ~1.37 while sat_retrieved_pm10_detrended_z decays).",
    45: "Explain Figure 3.12: PyTorch LSTM gradient saliency peaks sharply at Lag 0 h (0.0088), Lag -1 h (0.0037), and Lag -2 h (0.0023), showing the recurrent gate prioritizes immediate pre-event state.",
    46: "Section 05 divider / overview: summarize physical realism (Shamal, soil moisture, VPD, gusts) alongside the four honest limitations.",
    47: "Emphasize why XAI confirms physical realism rather than spurious leakage: capillary soil moisture cohesion (0–7 & 7–28 cm), VPD aridity, gusts, and Shamal seasonality.",
    48: "Summarize operational trade-offs: Line A is the calibrated event-risk classifier (BSS 0.0301–0.3218, Lift 4.28x at 24 h); continuous regression skill is not yet demonstrated and PM10 proxy is visibility/ERA5-modelled.",
    49: "Walk through the four core limitations and safeguards: (1) regime shift & negative R2, (2) DL early validation-loss rise & single-station ST-GNN input, (3) missing optical data, (4) coarse ERA5/CAMS grids for convective haboobs.",
    50: "BE TRANSPARENT WITH THE COMMITTEE: State clearly that best-model selection used test performance, the PM10 background is modelled, ST-GNN lacks multi-station inputs yet, satellite/CAMS may share sources, and long-range skill is mostly seasonal—all scheduled for Stage 2 code fixes.",
    51: "Show how calibrated probabilities + top-decile Lift + local SHAP checks translate into the 4-tier Greater Riyadh operational playbook.",
    52: "Section 06 divider: Conclusion & Future Work.",
    53: "Synthesize the 4 headline takeaways: 0.809 ROC-AUC at 24 h (vs 0.643 climo), 4.28x Lift@Top10%, >93% Ground+Calendar+ERA5 attribution, and honest 'Not yet' status on regression skill (R2 < 0).",
    54: "Present the three actionable recommendations for Saudi Civil Defense, NCEC, and KKIA: dual-line deployment, risk-tiered alerting with SHAP audits, and Najd/Qassim soil-moisture + visibility sensors.",
    55: "Walk through the reproducible codebase table (riyadh_hourly_clean_tvt.csv, Notebooks 01–04, build_and_run_clean_hourly_notebooks.py, export_final_hourly_models.py).",
    56: "Present the verified Python 3.12.0 software stack (Appendix A, Table A.1) powering ingestion, Line A, Line B, XAI, and automated thesis generation.",
    57: "Thank the committee (Assoc. Prof. Wen Wei and USTB defense panel) and invite questions.",
}


def add_callout_box(slide, left, top, width, height, title, lines):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    r0 = p0.add_run()
    r0.text = title
    r0.font.bold = True
    r0.font.size = Pt(14)
    r0.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    for ln in lines:
        p = tf.add_paragraph()
        p.space_before = Pt(4)
        r = p.add_run()
        r.text = f"• {ln}"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)


def main():
    prs = Presentation(str(PPTX_PATH))

    # 1. Enrich Slide 38 (XAI 168h Modality & Top Drivers) if not already enriched
    s38 = prs.slides[37]
    s38_txt = " ".join(sh.text for sh in s38.shapes if sh.has_text_frame)
    if "sin_doy = 0.71245" not in s38_txt:
        add_callout_box(
            s38,
            left=13.4,
            top=1.8,
            width=6.0,
            height=4.8,
            title="Key 168 h Attribution Breakdown",
            lines=[
                "Ground_METAR: ~37.4% | Calendar_Diurnal: ~32.2%",
                "ERA5_Physics: ~23.5% (combined > 93%)",
                "Satellite_Detrended: ~4.7% | CAMS_NWP: ~1.8%",
                "Top 1: sin_doy = 0.71245 (Perm ROC +0.16749)",
                "Top 2: dust_rate_4320h = 0.52050",
                "Top 3: hours_since_dust = 0.24132",
                "Top 4: dust_rate_720h = 0.17698",
                "Soil moisture (0–28 cm) & VPD follow closely",
            ],
        )

    # 2. Enrich Slide 45 (LSTM Temporal Saliency) if not already enriched
    s45 = prs.slides[44]
    s45_txt = " ".join(sh.text for sh in s45.shapes if sh.has_text_frame)
    if "0.0088" not in s45_txt:
        add_callout_box(
            s45,
            left=13.4,
            top=1.8,
            width=6.0,
            height=4.2,
            title="24-Hour Lookback Gradient Magnitudes",
            lines=[
                "Lag 0 h (forecast origin): 0.0088 (peak)",
                "Lag -1 h: 0.0037 (second highest)",
                "Lag -2 h: 0.0023",
                "Lags -23 h to -10 h: near-zero baseline (< 0.0003)",
                "Confirms recurrent gating focuses on immediate surface state",
            ],
        )

    # 3. Add Software Environment & Package Stack slide before Thank You (if not already present)
    has_env_slide = any(
        "Software Environment" in sh.text
        for s in prs.slides
        for sh in s.shapes
        if sh.has_text_frame
    )
    if not has_env_slide:
        blank_layout = prs.slide_layouts[0]
        new_slide = prs.slides.add_slide(blank_layout)
        # Move new_slide right before Thank You (last slide before it)
        xml_slides = prs.slides._sldIdLst
        slides_list = list(xml_slides)
        xml_slides.remove(slides_list[-1])
        xml_slides.insert(len(slides_list) - 2, slides_list[-1])

        # Title
        tb = new_slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(18.4), Inches(0.8))
        p_t = tb.text_frame.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = "Software Environment, Packages and Libraries (Python 3.12.0)"
        r_t.font.bold = True
        r_t.font.size = Pt(28)
        r_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

        # Table of verified .venv packages
        rows = [
            ["Package / Library", "Version", "Category", "Pipeline Role"],
            ["Python / numpy / pandas", "3.12.0 / 2.5.4 / 3.1.1", "Core & Tabular", "Runtime, tensor prep, 86,928 h alignment, 360 h splits"],
            ["scipy / scikit-learn", "1.18.1 / 1.9.1", "Line A Tabular ML", "LogReg_Bal, RF, ExtraTrees, HistGB, Ridge_log1p, calibration"],
            ["xgboost", "3.4.1", "Gradient Boosting", "24–360 h binary classification, regression & XAI-1/2"],
            ["torch", "2.15.0+cpu", "Line B Deep Learning", "RealLSTMNet, RealTransformerNet, RealPINNNet, RealSTGNNNet"],
            ["shap / matplotlib", "0.54.1 / 3.11.2", "XAI & Plotting", "TreeSHAP, PDP/ICE, horizon shift & nb02/03/04 figures"],
            ["xarray / netCDF4 / cdsapi", "2026.9.0 / 1.7.5.1 / 0.7.7", "Reanalysis I/O", "ECMWF ERA5 & CAMS NetCDF retrieval & decoding"],
            ["joblib / ipykernel / python-docx", "1.6.0 / 7.4.0 / 1.2.0", "Export & Docs", "Model serialization, notebook execution & thesis sync"],
        ]
        tbl_shape = new_slide.shapes.add_table(len(rows), 4, Inches(0.8), Inches(1.5), Inches(18.4), Inches(8.6))
        tbl = tbl_shape.table
        col_widths = [Inches(4.2), Inches(3.2), Inches(3.2), Inches(7.8)]
        for ci, w in enumerate(col_widths):
            tbl.columns[ci].width = w
        for ri, row in enumerate(rows):
            for ci, val in enumerate(row):
                cell = tbl.cell(ri, ci)
                cell.text = val
                for p in cell.text_frame.paragraphs:
                    p.alignment = PP_ALIGN.LEFT
                    for r in p.runs:
                        r.font.size = Pt(15 if ri == 0 else 14)
                        r.font.bold = (ri == 0)
                        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if ri == 0 else RGBColor(0x1E, 0x29, 0x3B)
                if ri == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(0x1B, 0x36, 0x5D)
                elif ri % 2 == 1:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(0xF1, 0xF5, 0xF9)

    # 4. Populate rich speaker notes on all slides
    for idx, slide in enumerate(prs.slides, start=1):
        note_txt = SLIDE_NOTES.get(idx)
        if note_txt:
            tf = slide.notes_slide.notes_text_frame
            tf.text = note_txt

    try:
        prs.save(str(PPTX_PATH))
        print(f"Enriched {PPTX_PATH.name}: {len(prs.slides)} slides, all with speaker notes.")
    except PermissionError:
        alt = PPTX_PATH.with_name("Riyadh_Sandstorm_Forecasting_Midterm_detailed.pptx")
        prs.save(str(alt))
        print(f"LOCKED: {PPTX_PATH.name} is open; saved to {alt.name} ({len(prs.slides)} slides).")


if __name__ == "__main__":
    main()
