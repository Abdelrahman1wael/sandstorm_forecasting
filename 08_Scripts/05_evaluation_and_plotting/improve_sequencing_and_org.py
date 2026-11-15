from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
MASTER_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v3.docx"


def set_para_text(p, text: str, bold: bool | None = None):
    p.text = text
    for r in p.runs:
        r.font.name = "Times New Roman"
        if p.style and p.style.name == "Normal":
            r.font.size = Pt(11)
        if bold is not None:
            r.bold = bold


def insert_normal_after(p_ref, text: str):
    new_p = OxmlElement("w:p")
    p_ref._p.addnext(new_p)
    # Wrap with python-docx Paragraph via parent
    from docx.text.paragraph import Paragraph
    para = Paragraph(new_p, p_ref._parent)
    para.style = p_ref._parent.styles["Normal"] if hasattr(p_ref._parent, "styles") else "Normal"
    r = para.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    return para


def main():
    doc = Document(str(MASTER_PATH))

    # 1. Fix accidental typo "Characteriztics" -> "Characteristics" (TOC, Heading 2, and body)
    typo_fixes = 0
    for p in doc.paragraphs:
        if "Characteriztics" in p.text or "characteriztics" in p.text:
            new_t = p.text.replace("Characteriztics", "Characteristics").replace("characteriztics", "characteristics")
            set_para_text(p, new_t)
            typo_fixes += 1

    # 2. Align 3.6.3 Model Construction & 3.7.4 Quantile Regression with final dual-pipeline methodology
    for i, p in enumerate(doc.paragraphs):
        if i <= 190:
            continue
        t = p.text.strip()
        if t.startswith("Main Line A, Numerical Forecast Enhancement:"):
            set_para_text(
                p,
                "Main Line A (Calibrated Tabular Ensembles and Ridge Regression): Train regularized linear and tree-ensemble classifiers "
                "(LogReg_Bal_Cal, RandomForest_Cal, ExtraTrees_Cal, HistGB_Cal, XGBoost_Cal) with validation-set Platt probability calibration, "
                "alongside Ridge continuous PM₁₀ regression, over the 115 clean causal hourly features across horizons H ∈ {24, 72, 168, 216, 360} h."
            )
        elif t.startswith("Main Line B, End-to-End Sandstorm Risk and Intensity Forecasting:"):
            set_para_text(
                p,
                "Main Line B (PyTorch Deep Sequence and Physics-Informed Models): Construct 24-hour causal lookback sequences and evaluate "
                "RealLSTMNet, RealTransformerNet, RealPINNNet, and the RealSTGNNNet prototype across three random seeds for multi-horizon classification and continuous PM₁₀ regression."
            )
        elif t.startswith("To quantify predictive uncertainty over the +72 h to +120 h horizon"):
            set_para_text(
                p,
                t.replace("over the +72 h to +120 h horizon", "across multi-day forecast horizons (24–360 h)")
            )

    # 3. Add concise introductory lead-in paragraphs before bare bullet/list sections
    lead_ins = {
        "2.1.2 Bottlenecks and Limitations of Traditional Forecasting":
            "Despite their physical rigor, conventional NWP dust models face three structural bottlenecks when applied to multi-day urban early warning:",
        "2.3.2 Prediction of Key Meteorological Parameters":
            "Beyond extreme-event detection, machine learning has demonstrated strong skill in downscaling and bias-correcting continuous atmospheric variables:",
        "2.3.3 Energy, Power Load, and Thermal Systems":
            "Weather-driven forecasting frameworks have also matured rapidly across renewable energy and grid-load management:",
        "2.3.4 Transportation and Maritime":
            "In transportation and maritime safety, interpretable tree ensembles and spatiotemporal networks are widely used to translate meteorological hazards into operational risk:",
        "3.4.1 Four Causal Feature Groups (115 Predictors)":
            "To capture local emissions, regional transport, and seasonal regimes without future-target leakage, the 115 clean hourly predictors are organized into four causal groups:",
        "3.5 Research Methods":
            "Following the data-preparation pipeline above, this study integrates two complementary methodological pillars:",
        "3.6.2 Feature Engineering and Input Representation":
            "At the feature-engineering stage, predictors are structured around three physical mechanisms:",
        "3.6.3 Model Construction":
            "Model development follows a controlled dual-pipeline design comparing tabular ensembles against deep sequence architectures:",
        "3.6.4 Probability Calibration and Event Optimization":
            "Because rare dust events (~0.94% test prevalence) distort uncalibrated scores, three post-processing and loss-design safeguards are applied:",
        "6.2 Actionable Recommendations for Saudi Civil Defense and Municipal Planners":
            "Based on the out-of-sample validation in Chapter 4 and the operational constraints analyzed in Chapter 5, three concrete deployment actions are recommended:",
    }

    added_leads = 0
    for p in doc.paragraphs:
        t = p.text.strip()
        if t in lead_ins and (p.style and p.style.name in ("Heading 2", "Heading 3")):
            nxt_el = p._p.getnext()
            if nxt_el is not None and nxt_el.tag.endswith("}p"):
                nxt_txt = "".join(nxt_el.itertext()).strip()
                if nxt_txt != lead_ins[t]:
                    insert_normal_after(p, lead_ins[t])
                    added_leads += 1

    # 4. Re-sequence Chapter 3: move 3.8 (Municipal Early-Warning Decision Framework + Table 3.4) to after 3.10.3,
    #    and renumber 3.9 -> 3.8, 3.10 -> 3.9 (3.9.1–3.9.3), moved 3.8 -> 3.10 in both body and TOC.
    body = doc.element.body
    p38 = next((p for i, p in enumerate(doc.paragraphs) if i > 190 and p.text.strip().startswith("3.8 Municipal Early-Warning")), None)
    p39 = next((p for i, p in enumerate(doc.paragraphs) if i > 190 and p.text.strip().startswith("3.9 Multimodal Feature Groups")), None)
    ch4 = next((p for i, p in enumerate(doc.paragraphs) if i > 190 and p.text.strip().startswith("Chapter 4")), None)

    moved_38 = False
    if p38 is not None and p39 is not None and ch4 is not None:
        children = list(body)
        idx_38 = children.index(p38._p)
        idx_39 = children.index(p39._p)
        block_38 = children[idx_38:idx_39]
        for el in block_38:
            body.remove(el)
        # Insert right before Chapter 4
        ch4_el = ch4._p
        for el in block_38:
            ch4_el.addprevious(el)
        moved_38 = True

        # Renumber headings in body and TOC
        renames = [
            ("3.9 Multimodal Feature Groups and 6-Node Domain Overview", "3.8 Multimodal Feature Groups and 6-Node Domain Overview"),
            ("3.10 Model Architecture Specifications, Equations, and Hyperparameters", "3.9 Model Architecture Specifications, Equations, and Hyperparameters"),
            ("3.10.1 Main Line A:", "3.9.1 Main Line A:"),
            ("3.10.2 Main Line B:", "3.9.2 Main Line B:"),
            ("3.10.3 Explainable AI Suite", "3.9.3 Explainable AI Suite"),
            ("3.8 Municipal Early-Warning Decision Framework and Operational Playbook", "3.10 Municipal Early-Warning Decision Framework and Operational Playbook"),
        ]
        for p in doc.paragraphs:
            for old, new in renames:
                if old in p.text:
                    set_para_text(p, p.text.replace(old, new))

        # Also reorder TOC entries for 3.8, 3.9, 3.10 so TOC matches body order
        toc_310 = next((p for i, p in enumerate(doc.paragraphs[:190]) if "3.10 Municipal Early-Warning" in p.text), None)
        toc_38 = next((p for i, p in enumerate(doc.paragraphs[:190]) if "3.8 Multimodal Feature Groups" in p.text), None)
        toc_ch4 = next((p for i, p in enumerate(doc.paragraphs[:190]) if p.text.strip().startswith("Chapter 4")), None)
        if toc_310 is not None and toc_38 is not None and toc_ch4 is not None:
            # Move toc_310 right before toc_ch4
            toc_el = toc_310._p
            body.remove(toc_el)
            toc_ch4._p.addprevious(toc_el)

    doc.save(str(MASTER_PATH))
    print(f"Sequencing & org improvements applied: typo_fixes={typo_fixes}, added_leads={added_leads}, moved_38_to_310={moved_38}")


if __name__ == "__main__":
    main()
