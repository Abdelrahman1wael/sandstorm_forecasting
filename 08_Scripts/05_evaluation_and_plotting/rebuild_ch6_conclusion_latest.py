from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Pt

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
DOC_PATH = ROOT / "01_Documentation" / "FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver6.docx"


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

    ch6_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Chapter 6" in p.text)
    ref_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "References" in p.text)

    ch6_el = doc.paragraphs[ch6_idx]._p
    ref_el = doc.paragraphs[ref_idx]._p

    # Remove all body elements strictly between Chapter 6 heading and References heading
    to_remove = []
    cur = ch6_el.getnext()
    while cur is not None and cur is not ref_el:
        to_remove.append(cur)
        cur = cur.getnext()
    for el in to_remove:
        body.remove(el)

    # 6.1
    add_para_before(ref_el, "6.1 Scientific and Operational Synthesis", "Heading 2", doc)
    add_para_before(
        ref_el,
        "This thesis developed, audited, and validated a strictly causal, multi-modal forecasting framework for Greater Riyadh across an 86,928-hour clean master dataset (riyadh_hourly_clean_tvt.csv, 2015–2024; 115 features) integrating ground METAR surface telemetry, ERA5 boundary-layer physics, detrended satellite retrievals, CAMS NWP fields, and seasonal/dust-memory descriptors. Temporal integrity was enforced across all experiments using a 70%/15%/15% chronological split (2015–2021 train, 2022 validation, 2023–2024 untouched test), 360-hour (15-day) purge gaps, five multi-day horizons H in {24, 72, 168, 216, 360} h, and three random seeds {42, 123, 456}.",
        "Normal",
        doc,
    )
    add_para_before(
        ref_el,
        "Empirical evaluation across Main Line A (Notebooks 02), Main Line B (Notebook 03), and the six-module Explainable AI suite (Notebook 04) established a clear operational complementarity. For binary dust-event discrimination on the 2023–2024 test set, calibrated Line A ensembles led all horizons—RandomForest_Cal achieved Test ROC-AUC = 0.8090 (Lift@Top10% = 4.28×, BSS = 0.3218) at 24 h, 0.7167 at 72 h, and 0.7031 at 168 h, while XGBoost_Cal reached 0.7156 at 216 h and 0.7655 (Test PR-AUC = 0.8311) at 360 h, substantially outperforming Persistence_Cal (0.5701 at 24 h; 0.4721 at 360 h). Main Line B PyTorch sequence and graph architectures achieved competitive calibrated classification (LineB_PINN = 0.7939 at 24 h; LineB_Transformer = 0.7158 at 72 h, 0.7065 at 216 h, and 0.6817 at 360 h; Test BSS = 0.1603–0.2571) and decisively outperformed non-trivial Line A ML models on continuous PM₁₀ regression (LineB_STGNN RMSE = 21.55, 15.58, and 14.86 μg/m³ at 24, 72, and 216 h; LineB_LSTM RMSE = 14.45 and 14.13 μg/m³ at 168 and 360 h vs. Line A's 26.34–30.25 μg/m³). Finally, XAI-1 through XAI-6 verified that model skill is anchored in physically realistic drivers—Ground_METAR (~37.4%), Calendar_Diurnal (~32.2%), and ERA5_Physics (~23.5%), led by sin_doy (0.71245), dust_rate_4320h (0.52050), hours_since_dust (0.24132), soil moisture, VPD, and wind gusts—with PyTorch LSTM saliency peaking at Lag 0 h (0.0088).",
        "Normal",
        doc,
    )

    # 6.2
    add_para_before(ref_el, "6.2 Actionable Recommendations for Saudi Civil Defense and Municipal Planners", "Heading 2", doc)
    add_para_before(
        ref_el,
        "1. Dual-Line Operational Deployment for KKIA and Civil Aviation: Pair Line A's calibrated event-risk classifiers (RandomForest_Cal for 24–168 h; XGBoost_Cal for 216–360 h) with Line B's continuous spatiotemporal regressors (LineB_STGNN and LineB_LSTM) to supply King Khalid International Airport (KKIA) and regional aviation controllers with both 1–15 day dust-event probabilities and smooth PM₁₀ trajectory guidance.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ref_el,
        "2. Risk-Tiered Alerting Backed by Lift@Top10% and Local SHAP Audits: Replace uncalibrated binary triggers with top-decile risk tiers (Lift@Top10% = 4.28× at 24 h, 2.67× at 72 h, and 2.03× at 168 h) and require automated local SHAP verification (confirming concurrent elevation in pm10_calibrated_ugm3, visibility reduction vsby, has_wxcode, and seasonal phase) before issuing high-cost Level 4 municipal advisories under low dust-prevalence regimes.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ref_el,
        "3. Targeted Soil-Moisture and Upwind Corridor Instrumentation: Expand automated surface and root-zone soil moisture sensors (0–7 cm and 7–28 cm) alongside visibility/particulate stations along the Najd and Qassim upwind corridors to strengthen real-time monitoring of the primary physical drivers identified by SHAP and permutation audits.",
        "List Paragraph",
        doc,
    )

    # 6.3
    add_para_before(ref_el, "6.3 Future Directions", "Heading 2", doc)
    add_para_before(
        ref_el,
        "Future research will advance three priorities directly motivated by the operational limitations identified in Chapter 5: (1) integrating 15-minute geostationary Meteosat SEVIRI dust-RGB imagery and localized Doppler weather radar to resolve sub-6-hour convective haboob cold-pool outflows that coarse ~31 km ERA5 and ~40 km CAMS grids miss; (2) developing rolling, regime-adaptive probability recalibration and continual learning pipelines to track multi-year dust-prevalence shifts (7.47% to 10.51% to 1.79%) and land-surface changes under Vision 2030 afforestation initiatives (e.g., the Saudi Green Initiative); and (3) scaling the 6-node regional graph to a denser pan-Arabian station topology with cross-regional transfer learning to improve deep-learning sample efficiency under rare severe-storm regimes.",
        "Normal",
        doc,
    )

    try:
        doc.save(str(DOC_PATH))
        print(f"Rebuilt Chapter 6 in {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver7.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
