from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Pt

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
DOC_PATH = ROOT / "01_Documentation" / "FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver5.docx"


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


def main():
    doc = Document(str(DOC_PATH))
    body = doc.element.body

    ch5_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Chapter 5" in p.text)
    ch6_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Chapter 6" in p.text)

    ch5_el = doc.paragraphs[ch5_idx]._p
    ch6_el = doc.paragraphs[ch6_idx]._p

    # Remove all body elements strictly between Chapter 5 heading and Chapter 6 heading
    to_remove = []
    cur = ch5_el.getnext()
    while cur is not None and cur is not ch6_el:
        to_remove.append(cur)
        cur = cur.getnext()
    for el in to_remove:
        body.remove(el)

    # 5.1
    add_para_before(ch6_el, "5.1 Atmospheric Physical Realism of Multi-Method XAI Attributions", "Heading 2", doc)
    add_para_before(
        ch6_el,
        "A central scientific question in AI-assisted meteorology is whether statistical and deep learning models capture genuine Arabian boundary-layer physics or merely memorize spurious dataset artifacts. Multi-method explainability across Notebook 04 (XAI-1 through XAI-6 on the 168 h clean hourly test set) confirms strong physical consistency. The dominant predictors by exact Mean |SHAP| are seasonal solar-calendar phase (sin_doy = 0.71245; cos_doy = 0.09449), multi-scale dust-regime memory (dust_rate_4320h = 0.52050, hours_since_dust = 0.24132, dust_rate_720h = 0.17698), two-layer ERA5 volumetric soil moisture (era5_soil_moisture_7_to_28cm = 0.12351, era5_soil_moisture_0_to_7cm = 0.10673), detrended satellite anomaly (sat_retrieved_pm10_detrended_z = 0.08923), 7-day rolling vapor pressure deficit (phys_vpd_kpa_roll168h = 0.08831), and surface wind gusts (gust = 0.07611).",
        "Normal",
        doc,
    )
    add_para_before(
        ch6_el,
        "These attributions align directly with established desert aeolian dynamics. Seasonal phase (sin_doy/cos_doy) encodes the spring–early-summer Shamal and pre-frontal dust-storm window over the Najd plateau, while surface and root-zone soil moisture (0–7 cm and 7–28 cm) regulate inter-particle capillary cohesion and threshold friction velocity. Combined with atmospheric desiccation (phys_vpd_kpa_roll168h) and gust-driven saltation (gust), the models recover a coherent physical pathway from dry soil preconditioning to surface dust mobilization. Modality aggregation further shows that Ground_METAR (~37.4%), Calendar_Diurnal (~32.2%), and ERA5_Physics (~23.5%) supply over 93% of total explanatory power, whereas Satellite_Detrended (~4.7%) and CAMS_NWP_Detrended (~1.8%) play secondary roles once raw trends and leakage are removed.",
        "Normal",
        doc,
    )
    add_para_before(
        ch6_el,
        "Moreover, multi-horizon attribution tracking (XAI-6) and PyTorch LSTM gradient saliency (Figure 11) demonstrate physically appropriate temporal scaling. At 24 h, short-range surface/satellite anomalies (sat_retrieved_pm10_detrended_z) and immediate pre-event sequence lags (Lag 0 h = 0.0088, Lag -1 h = 0.0037) carry the highest weight; as the horizon extends to 168 h and 360 h, attribution shifts smoothly toward seasonal phase (sin_doy rising from ~0.19 to ~1.37), multi-month dust memory, and deeper soil moisture.",
        "Normal",
        doc,
    )

    # 5.2
    add_para_before(ch6_el, "5.2 Line A vs. Line B Trade-offs and Deep Learning Performance Analysis", "Heading 2", doc)
    add_para_before(
        ch6_el,
        "A key finding of this thesis is the complementary division of strength—and honest performance boundary—between Main Line A (calibrated tabular ensembles) and Main Line B (PyTorch spatiotemporal networks). For binary dust-event classification on the 2023–2024 test set, Line A achieves slightly higher ROC-AUC than Line B across all five horizons (0.8090 vs. 0.7939 at 24 h; 0.7167 vs. 0.7158 at 72 h; 0.7031 vs. 0.6820 at 168 h; 0.7156 vs. 0.7065 at 216 h; and 0.7655 vs. 0.6817 at 360 h). Although deep learning architectures are often expected to dominate tabular baselines, their slightly lower classification discrimination here is physically and statistically understandable: under a low out-of-sample positive rate (1.79% dust prevalence in 2023–2024 vs. 7.47% in training and 10.51% in validation), high-parameter sequence models begin to overfit validation loss after the opening epochs (Figure 18), whereas depth-constrained tree ensembles with post-hoc probability calibration generalize more stably on engineered multi-lag summaries.",
        "Normal",
        doc,
    )
    add_para_before(
        ch6_el,
        "For continuous PM₁₀ regression, however, the pattern reverses decisively among predictive models. Unregularized Line A tree regressors (XGBoost and RandomForest) suffer severe variance amplification under the 2015–2021 to 2023–2024 distribution shift (Test RMSE spiking to 79–104 μg/m³ at 7–9 days), leaving only Ridge_log1p (27.68–30.25 μg/m³ at 168–360 h) and ExtraTrees at short range (26.34 μg/m³ at 24 h; 27.63 μg/m³ at 72 h) competitive. In contrast, Line B's spatiotemporal inductive biases—graph-coupled station topology in LineB_STGNN (21.55 μg/m³ at 24 h, 15.58 μg/m³ at 72 h, 14.86 μg/m³ at 216 h) and recurrent gating in LineB_LSTM (14.45 μg/m³ at 168 h, 14.13 μg/m³ at 360 h)—suppress extreme extrapolation errors and cut continuous prediction RMSE roughly in half relative to non-trivial Line A ML regressors.",
        "Normal",
        doc,
    )

    # 5.3
    add_para_before(ch6_el, "5.3 Operational Early-Warning Deployment and False-Alarm Mitigation", "Heading 2", doc)
    add_para_before(
        ch6_el,
        "In municipal air-quality management and aviation operations at King Khalid International Airport (KKIA), uncalibrated binary alerts under a 1.79% base rate would generate unacceptable false-alarm burdens. Our dual-line framework mitigates this risk through two operational mechanisms verified in Chapter 4. First, post-hoc calibrated Line A probabilities (RandomForest_Cal at 24–168 h; XGBoost_Cal at 216–360 h) maintain strictly positive Brier Skill Scores (0.0301–0.3218) and concentrate dust events into the top risk decile (Lift@Top10% = 4.28× at 24 h, 2.67× at 72 h, and 2.03× at 168 h), enabling tiered alert thresholds rather than brittle binary triggers.",
        "Normal",
        doc,
    )
    add_para_before(
        ch6_el,
        "Second, local SHAP attributions (exemplified by the 2024-06-20 04:00:00 peak-risk case study in Figure 25) give duty meteorologists transparent diagnostic evidence—showing whether an elevated forecast probability is corroborated by real-time surface visibility degradation (vsby), active weather codes (has_wxcode), calibrated PM₁₀, and Shamal seasonality—before escalating to Level 4 public advisories or aviation ground-delay programs.",
        "Normal",
        doc,
    )

    # 5.4
    add_para_before(ch6_el, "5.4 Data Subtlety, Regime Shift, and Operational Limitations", "Heading 2", doc)
    add_para_before(
        ch6_el,
        "A rigorous assessment requires acknowledging four core data and modeling limitations encountered in this study, together with the safeguards implemented to handle them:",
        "Normal",
        doc,
    )
    add_para_before(
        ch6_el,
        "1. Inter-Annual Dust Regime Shift and Negative Test R²: Dust-event prevalence shifts markedly across the chronological split—from 7.47% in 2015–2021 (training) and 10.51% in 2022 (validation) down to 1.79% in 2023–2024 (test). Because 2023–2024 exhibits much lower background PM₁₀ variance than 2015–2021, even well-behaved continuous models (LineB_LSTM RMSE = 14.13 μg/m³; LineB_STGNN RMSE = 15.58 μg/m³) record negative out-of-sample Test R² against the much-narrower test variance, and the constant Trivial_Median baseline achieves low RMSE by predicting near-quiescent levels. Rather than hiding this phenomenon, our evaluation enforces 360-hour purge gaps, reports Trivial_Median, Persistence_Cal, and MonthClimo_Cal benchmarks transparently, and relies on rank/calibration metrics (ROC-AUC, PR-AUC, BSS, Lift@Top10%) alongside RMSE and MAE.",
        "Normal",
        doc,
    )
    add_para_before(
        ch6_el,
        "2. Deep Learning Generalization Ceiling Under Rare-Event Scarcity: As reflected in Figure 18, all four PyTorch architectures exhibit rising validation loss after early training epochs, limiting their classification ROC-AUC (0.6817–0.7939) below calibrated random-forest and boosted-tree ensembles. We mitigated this through early-epoch best-validation checkpointing, physics-informed monotonicity regularization in RealPINNNet, and multi-seed averaging ({42, 123, 456}), while positioning Line B primarily for continuous PM₁₀ trajectory estimation where its recurrent and graph-spatial inductive biases excel.",
        "Normal",
        doc,
    )
    add_para_before(
        ch6_el,
        "3. Subtlety and Missingness in Ground METAR and Satellite Retrievals: Hourly surface visibility, weather codes, and passive optical satellite retrievals contain nocturnal gaps, cloud-contamination dropouts, and sensor quantization noise. Strict causal cleaning, detrending (sat_retrieved_pm10_detrended_z), and multi-modal redundancy across Ground_METAR, ERA5_Physics, and Calendar_Diurnal ensure graceful degradation when individual optical channels are missing.",
        "Normal",
        doc,
    )
    add_para_before(
        ch6_el,
        "4. Spatial Grid Coarseness for Convective Haboobs: ERA5 (~31 km), CAMS (~40 km), and our 6-node regional station graph resolve synoptic Shamal troughs and inter-regional dust advection well over 24–360 h horizons, but cannot directly capture sub-kilometre thunderstorm cold-pool outflows (convective haboobs). Operational nowcasting at < 6 h lead times therefore requires pairing this framework with localized Doppler weather radar and convective-permitting numerical simulations.",
        "Normal",
        doc,
    )

    try:
        doc.save(str(DOC_PATH))
        print(f"Rebuilt Chapter 5 in {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver6.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
