from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Pt

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
DOC_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed.docx"


def set_para(p, text, size=11):
    p.text = ""
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)


def add_para_before(anchor_el, text, doc, size=11):
    new_p = OxmlElement("w:p")
    anchor_el.addprevious(new_p)
    p = doc.paragraphs[0].__class__(new_p, doc._body)
    if "Normal" in [s.name for s in doc.styles]:
        p.style = doc.styles["Normal"]
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    return p


def main():
    doc = Document(str(DOC_PATH))
    p = doc.paragraphs

    # Abstract (EN + ZH)
    set_para(
        p[44],
        "A dual-pipeline architecture is evaluated across five horizons H ∈ {24, 72, 168, 216, 360} h and three random seeds "
        "using 6-hourly samples (10,142 / 2,114 / 2,114 across train/validation/test). In Main Line A, calibrated tabular ensembles "
        "exceed monthly-climatology ROC-AUC at every horizon (0.809 vs. 0.643 at 24 h; 0.717 vs. 0.641 at 72 h; 0.703 vs. 0.658 at 168 h; "
        "0.716 vs. 0.666 at 216 h; 0.766 vs. 0.665 at 360 h), outperforming Persistence_Cal (0.5701 at 24 h; 0.4721 at 360 h). "
        "In Main Line B, PyTorch sequence and graph-structured GRU prototypes achieve 0.6817–0.7939 classification ROC-AUC; however, "
        "for continuous PM₁₀ regression, all models yield negative test R², and a constant training-median baseline achieves lower RMSE "
        "than Line B at 24–216 h (e.g., 11.8 vs. 14.5 μg/m³ at 168 h), with Line B lower only at 360 h (14.1 vs. 15.5 μg/m³).",
    )
    set_para(
        p[50],
        "双通道架构在五个预报时效 H ∈ {24, 72, 168, 216, 360} h 与三个随机种子下基于6小时样本（训练/验证/测试分别为10,142 / 2,114 / 2,114）进行评估。"
        "在主线A中，校准表格集成模型在所有时效上均优于月气候态基线（24 h为0.809对比0.643；72 h为0.717对比0.641；168 h为0.703对比0.658；"
        "216 h为0.716对比0.666；360 h为0.766对比0.665），并显著超过Persistence_Cal（0.5701与0.4721）。"
        "在主线B中，PyTorch时序与图结构GRU原型取得0.6817—0.7939的分类ROC-AUC；但在连续PM₁₀回归任务中，所有模型测试集R²均为负值，"
        "且常数训练中位数基线在24—216 h的RMSE低于主线B（如168 h为11.8对比14.5 μg/m³），主线B仅在360 h更低（14.1对比15.5 μg/m³），"
        "因此本原型尚未验证连续回归技能。",
    )

    # Chapter 3 split & ST-GNN updates
    set_para(
        p[384],
        "Across the 86,928 aligned hourly records in riyadh_hourly_clean_tvt.csv (2015–2024), surface particulate concentrations "
        "exhibit extreme right skewness (11.69 raw; 11.79 cleaned) with a heavy dust-storm tail reaching 4,800.0 μg/m³ (mean 106.12 μg/m³, "
        "std 254.14 μg/m³, median 68.00 μg/m³). Data were split chronologically into 70% train (9 Jan 2015 – 18 Dec 2021), 15% validation "
        "(2 Jan 2022 – 14 Jun 2023), and 15% test (29 Jun 2023 – 8 Dec 2024) with a 360-hour gap between partitions; models use 6-hourly "
        "samples (10,142 / 2,114 / 2,114). The hourly dust rate is 7.47%, 8.43%, and 0.94% in the three partitions (computed on the raw table "
        "with the same split rule). For horizon H, the event target is 'dust (visibility < 5 km) occurs at least once in the next H hours' "
        "(168 h test positive rate: 35.0%), and the regression target is the mean PM₁₀ proxy over the next H hours.",
    )
    set_para(
        p[394],
        "3. Temporal regime shift and satellite drift (2015–2024): Feature-shift auditing (nb01_clean_hourly_feature_impact.csv) revealed "
        "large distributional shifts between training and testing in sat_dust_column_mass (Test Z-shift = 5.122), dust_rate_4320h (2.277), "
        "dust_rate_720h (1.266), and nwp_bias_proxy (1.168), alongside the hourly dust-rate decline from 7.47% (train) and 8.43% (validation) "
        "to 0.94% (test) (Figure 3.5).",
    )
    set_para(
        p[419],
        "Atmospheric particulate concentrations and dust predictors in desert environments exhibit extreme positive skewness (up to 11.79 in "
        "pm10_clean_ugm3) and heavy Pareto tails reaching 4,800.0 μg/m³. To prevent high-variance outliers from destabilising neural gradients "
        "and linear/tree objectives without leaking future regime statistics, Notebook 01 enforces a 360-hour (15-day) gap between the 70% "
        "training partition (9 Jan 2015 – 18 Dec 2021), 15% validation partition (2 Jan 2022 – 14 Jun 2023), and 15% test partition "
        "(29 Jun 2023 – 8 Dec 2024). Median imputation (SimpleImputer) and Yeo-Johnson power transformation (PowerTransformer) are fitted "
        "strictly via maximum likelihood on the 70% training split and frozen before transforming validation and test features.",
    )
    set_para(
        p[424],
        "Because hourly dust prevalence shifts across chronological splits (7.47% in Train, 8.43% in Validation, and 0.94% in Test, while the "
        "168 h multi-day event target reaches 35.0% positive rate on the test partition), synthetic oversampling (SMOTE) is omitted to avoid "
        "temporal autocorrelation leakage. Instead, class imbalance is handled through cost-sensitive learning (balanced class_weight in Line A "
        "and positive-class pos_weight in Line B) paired with validation-set probability calibration.",
    )
    set_para(
        p[495],
        "4. RealSTGNNNet & MultiModalNPZNet: RealSTGNNNet is a graph-structured GRU prototype that embeds a 6-node graph via row-normalised "
        "adjacency A_norm = A / deg, 8-d learnable node embeddings, and Linear(in_dim + 8 -> 32) propagation. In this prototype, the same "
        "station feature vector is supplied to all six nodes, so no inter-station information is used yet; true multi-station inputs are "
        "planned as future work. MultiModalNPZNet fuses Conv2d(6 -> 16) NWP grids (6x16x16), Conv2d(3 -> 16) satellite grids (3x32x32), "
        "24x6x12 sequences, and A_norm on line_b_final_dataset.npz using AdamW(lr = 2e-3) and L1Loss (Figure 3.11).",
    )

    # Chapter 4 (4.1, 4.2, 4.3)
    set_para(
        p[508],
        "All evaluations strictly respect temporal causality on the clean hourly master dataset (riyadh_hourly_clean_tvt.csv, 2015–2024; 115 "
        "features). Data were split chronologically into 70% train (9 Jan 2015 – 18 Dec 2021), 15% validation (2 Jan 2022 – 14 Jun 2023), and "
        "15% test (29 Jun 2023 – 8 Dec 2024), with a 360-hour gap between partitions. Models use 6-hourly samples (10,142 / 2,114 / 2,114). The "
        "hourly dust rate is 7.47%, 8.43%, and 0.94% in the three partitions (computed on the raw table with the same split rule). For horizon H "
        "in {24, 72, 168, 216, 360} h across three random seeds {42, 123, 456}, the event target is 'dust (visibility < 5 km) occurs at least "
        "once in the next H hours' (168 h test positive rate: 35.0%), and the regression target is the mean PM₁₀ proxy over the next H hours.",
    )
    set_para(
        p[515],
        "On the untouched test partition (Table 4.2; Figures 4.2–4.6), Line A exceeds monthly-climatology (MonthClimo_Cal) ROC-AUC at all "
        "horizons: 0.809 vs. 0.643 at 24 h, 0.717 vs. 0.641 at 72 h, 0.703 vs. 0.658 at 168 h, 0.716 vs. 0.666 at 216 h, and 0.766 vs. 0.665 "
        "at 360 h, while substantially outperforming Persistence_Cal (0.5701 at 24 h; 0.4721 at 360 h). Gains beyond 7 days (168 h) are small, "
        "consistent with predictability that is largely seasonal. For continuous PM₁₀ regression (Figure 4.5), all models obtain negative test R²; "
        "among non-constant Line A models, ExtraTrees gives 26.34 μg/m³ at 24 h and 27.63 μg/m³ at 72 h while Ridge_log1p gives 29.72, 27.68, "
        "and 30.25 μg/m³ at 168–360 h, though none beat the constant training-median baseline (Trivial_Median).",
    )
    set_para(
        p[521],
        "Figure 4.2 compares validation ROC-AUC (left) with out-of-sample test ROC-AUC (right). Line A exceeds MonthClimo_Cal across every "
        "horizon (0.809 vs. 0.643 at 24 h; 0.717 vs. 0.641 at 72 h; 0.703 vs. 0.658 at 168 h; 0.716 vs. 0.666 at 216 h; 0.766 vs. 0.665 at 360 h), "
        "while gains beyond 7 days remain modest and largely seasonal as Persistence_Cal decays below 0.50.",
    )
    set_para(
        p[535],
        "Main Line B evaluates RealLSTMNet, RealTransformerNet, RealPINNNet, and RealSTGNNNet (a graph-structured GRU prototype using identical "
        "station features across all six nodes) on 24-hour sequence tensors (Table 4.3; Figures 4.7–4.10). For event classification, LineB_PINN "
        "leads Line B at 24 h (Test ROC-AUC = 0.7939, BSS = 0.2159) and 168 h (0.6820, BSS = 0.2395), while LineB_Transformer leads at 72 h "
        "(0.7158, BSS = 0.2571), 216 h (0.7065, BSS = 0.2467), and 360 h (0.6817, PR-AUC = 0.7739). For continuous PM₁₀ regression (Figure 4.9), "
        "all models obtain negative test R²: LineB_STGNN yields Test RMSE = 21.55, 15.58, and 14.86 μg/m³ at 24, 72, and 216 h and LineB_LSTM "
        "yields 14.45 and 14.13 μg/m³ at 168 and 360 h. However, the constant training-median predictor (Trivial_Median) has lower RMSE than the "
        "best Line B model at 24–216 h (e.g., 11.8 vs. 14.5 μg/m³ at 168 h), and Line B is lower only at 360 h (14.1 vs. 15.5 μg/m³). Regression "
        "skill is therefore not demonstrated in this prototype.",
    )
    set_para(
        p[546],
        "Figure 4.9 shows Line B continuous PM₁₀ regression Test RMSE (left) and Test R² (right). LineB_STGNN (red) and LineB_LSTM (blue) yield "
        "lower RMSE (14.13–21.55 μg/m³) than LineB_Transformer (21.5–25.7 μg/m³), though all models record negative Test R² and remain above "
        "Trivial_Median at 24–216 h (11.8 vs. 14.5 μg/m³ at 168 h), outperforming Trivial_Median only at 360 h (14.1 vs. 15.5 μg/m³).",
    )
    set_para(
        p[549],
        "Figure 4.10 compares Main Line A and Main Line B PyTorch across 1–15 days. For event classification (left), Line A retains higher "
        "ROC-AUC across all horizons (0.809 vs. 0.794 at 1 d; 0.766 vs. 0.682 at 15 d). For continuous regression (right), Line A's minimum "
        "curve corresponds to the constant Trivial_Median baseline (11.8–20.9 μg/m³), which achieves lower RMSE than Line B at 24–216 h and is "
        "beaten by Line B only at 360 h (14.1 vs. 15.5 μg/m³), confirming that regression skill is not yet demonstrated.",
    )

    # Chapter 5 (5.2, 5.3, 5.4 + final Limitations paragraph)
    set_para(
        p[581],
        "A key finding of this thesis is the complementary division of strength—and honest performance boundary—between Main Line A (calibrated "
        "tabular ensembles) and Main Line B (PyTorch sequence and graph-structured GRU prototypes). For binary dust-event classification on the "
        "test set, Line A achieves higher ROC-AUC than Line B across all five horizons (0.809 vs. 0.794 at 24 h; 0.717 vs. 0.716 at 72 h; "
        "0.703 vs. 0.682 at 168 h; 0.716 vs. 0.707 at 216 h; and 0.766 vs. 0.682 at 360 h), exceeding MonthClimo_Cal at every horizon though "
        "with small gains beyond 7 days consistent with largely seasonal predictability. Meanwhile, high-parameter PyTorch sequence models begin "
        "to overfit validation loss after the opening epochs (Figure 4.7), whereas depth-constrained tree ensembles with post-hoc probability "
        "calibration generalize more stably on engineered multi-lag summaries.",
    )
    set_para(
        p[582],
        "For continuous PM₁₀ regression, all models obtain negative test R². Although LineB_STGNN (a graph-structured GRU prototype receiving the "
        "same station feature vector across all six nodes without inter-station inputs) and LineB_LSTM produce lower RMSE (14.13–21.55 μg/m³) than "
        "non-constant Line A ML regressors (26.34–30.25 μg/m³), the constant training-median predictor (Trivial_Median) has lower RMSE than the "
        "best Line B model at 24–216 h (e.g., 11.8 vs. 14.5 μg/m³ at 168 h), and Line B is lower only at 360 h (14.1 vs. 15.5 μg/m³). Regression "
        "skill is therefore not demonstrated in this prototype. Furthermore, the PM₁₀ proxy is derived from visibility and its background value "
        "is estimated from ERA5 wind and boundary-layer height, which limits physical interpretation.",
    )
    set_para(
        p[584],
        "In municipal air-quality management and aviation operations at King Khalid International Airport (KKIA), uncalibrated binary alerts "
        "risk excessive false alarms. Our dual-line framework addresses this through two operational mechanisms verified in Chapter 4. First, "
        "post-hoc calibrated Line A probabilities (RandomForest_Cal at 24–168 h; XGBoost_Cal at 216–360 h) maintain strictly positive Brier Skill "
        "Scores (0.0301–0.3218) and concentrate dust events into the top risk decile (Lift@Top10% = 4.28× at 24 h, 2.67× at 72 h, and 2.03× at "
        "168 h), enabling tiered alert thresholds rather than brittle binary triggers.",
    )
    set_para(
        p[588],
        "1. Inter-Annual Dust Regime Shift and Lack of Regression Skill: Hourly dust prevalence shifts across the chronological split—7.47% in "
        "Train (9 Jan 2015 – 18 Dec 2021), 8.43% in Validation (2 Jan 2022 – 14 Jun 2023), and 0.94% in Test (29 Jun 2023 – 8 Dec 2024), while "
        "the 168 h multi-day event target has a 35.0% test positive rate. All models obtain negative test R² for PM₁₀ regression, and the constant "
        "training-median predictor beats the best Line B model at 24–216 h (e.g., 11.8 vs. 14.5 μg/m³ at 168 h; Line B is lower only at 360 h: "
        "14.1 vs. 15.5 μg/m³). Because the PM₁₀ proxy is derived from visibility and its background value is estimated from ERA5 wind and "
        "boundary-layer height, regression skill is not demonstrated in this prototype.",
    )
    set_para(
        p[589],
        "2. Deep Learning Generalization Ceiling and ST-GNN Input Scope: As reflected in Figure 4.7, all four PyTorch architectures exhibit rising "
        "validation loss after early training epochs, keeping classification ROC-AUC (0.6817–0.7939) below calibrated tabular ensembles. Moreover, "
        "RealSTGNNNet is a graph-structured GRU prototype in which the same station feature vector is supplied to all six nodes, so no "
        "inter-station information is used yet; true multi-station inputs remain future work.",
    )
    set_para(
        p[591],
        "4. Spatial Grid Coarseness for Convective Haboobs: Coarse ERA5 (~31 km) and CAMS (~40 km) grids resolve synoptic Shamal troughs over "
        "24–360 h horizons but cannot capture sub-kilometre thunderstorm cold-pool outflows (convective haboobs). Operational nowcasting at < 6 h "
        "lead times requires pairing this framework with localized Doppler weather radar and convective-permitting numerical simulations.",
    )

    # Add explicit Limitations paragraph at the end of Chapter 5 (before Chapter 6 heading)
    ch6_idx = next(i for i, para in enumerate(doc.paragraphs) if para.style.name == "Heading 1" and "Chapter 6" in para.text)
    lim_txt = (
        "This prototype has known limitations that the next stage will address: best models were selected on test performance rather than "
        "validation; the PM₁₀ background is a modelled quantity; the graph model has no real multi-station input; satellite and CAMS channels "
        "may share a common source; and long-range skill is mostly seasonal. Rolling recalibration, validation-based selection and confidence "
        "intervals are planned."
    )
    if "best models were selected on test performance" not in doc.paragraphs[ch6_idx - 1].text:
        add_para_before(doc.paragraphs[ch6_idx]._p, lim_txt, doc)

    # Chapter 6 (6.1, 6.3)
    set_para(
        p[595],
        "Empirical evaluation across Main Line A (Notebook 02), Main Line B (Notebook 03), and the six-module Explainable AI suite (Notebook 04) "
        "using 6-hourly samples (10,142 / 2,114 / 2,114) established clear event-classification skill alongside important prototype boundaries. "
        "Line A exceeds monthly-climatology ROC-AUC at every horizon (0.809 vs. 0.643 at 24 h; 0.717 vs. 0.641 at 72 h; 0.703 vs. 0.658 at 168 h; "
        "0.716 vs. 0.666 at 216 h; 0.766 vs. 0.665 at 360 h), substantially outperforming Persistence_Cal (0.5701 at 24 h; 0.4721 at 360 h), "
        "with modest gains beyond 7 days consistent with largely seasonal predictability. Line B PyTorch sequence and graph-structured GRU "
        "prototypes (using identical station features across all six nodes) achieved 0.6817–0.7939 classification ROC-AUC; for continuous PM₁₀ "
        "regression, however, all models obtained negative test R² and Trivial_Median beat Line B at 24–216 h (11.8 vs. 14.5 μg/m³ at 168 h; "
        "Line B lower only at 360 h: 14.1 vs. 15.5 μg/m³), so regression skill is not demonstrated. Finally, XAI-1 through XAI-6 confirmed "
        "physically realistic drivers—Ground_METAR (~37.4%), Calendar_Diurnal (~32.2%), and ERA5_Physics (~23.5%), led by sin_doy (0.71245), "
        "dust_rate_4320h (0.52050), hours_since_dust (0.24132), soil moisture, VPD, and wind gusts—with LSTM saliency peaking at Lag 0 h (0.0088).",
    )
    set_para(
        p[601],
        "Future research will advance four priorities directly motivated by the prototype limitations identified in Chapter 5: (1) replacing "
        "test-set model selection with strict validation-based selection, rolling recalibration, and formal confidence intervals; (2) supplying "
        "true multi-station upstream inputs to the 6-node RealSTGNNNet graph rather than replicating single-station features; (3) integrating "
        "15-minute Meteosat SEVIRI dust-RGB imagery and Doppler radar for < 6 h convective haboob nowcasting; and (4) auditing independent "
        "satellite vs. CAMS aerosol sources under multi-year regime shifts (7.47% / 8.43% / 0.94% hourly dust rates).",
    )

    try:
        doc.save(str(DOC_PATH))
        print(f"Applied all 5 updates and saved {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name("USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v2.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
