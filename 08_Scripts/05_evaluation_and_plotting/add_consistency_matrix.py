from pathlib import Path
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
MASTER_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v3.docx"


def set_cell_shading(cell, fill_hex: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def set_cell_text(cell, text: str, bold: bool = False, size: int = 9):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    r.bold = bold


def main():
    doc = Document(str(MASTER_PATH))

    # Guard against duplicate insertion
    if any("Research Consistency Matrix" in p.text for p in doc.paragraphs):
        print("Research Consistency Matrix already present; skipping insertion.")
        return

    # 1. Renumber existing Table 1.1 -> Table 1.2 (LOT, body ref, caption)
    for p in doc.paragraphs:
        if "Table 1.1" in p.text and ("research schedule" in p.text.lower() or "seven-phase" in p.text.lower()):
            p.text = p.text.replace("Table 1.1", "Table 1.2")
            for r in p.runs:
                r.font.name = "Times New Roman"
                if p.style and p.style.name == "Normal":
                    r.font.size = Pt(11)

    # 2. Insert Table 1.1 into LIST OF TABLES right before Table 1.2
    lot_12 = next((p for i, p in enumerate(doc.paragraphs[:190]) if p.text.strip().startswith("Table 1.2:")), None)
    if lot_12 is not None:
        new_lot = OxmlElement("w:p")
        lot_12._p.addprevious(new_lot)
        lp = Paragraph(new_lot, lot_12._parent)
        lp.style = lot_12.style
        r = lp.add_run("Table 1.1: Research consistency matrix aligning objectives, data, models, and evaluation metrics\t8")
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    # 3. Insert intro, caption, and Table 1.1 at end of 1.6.1 (after P271, before 1.6.2)
    p_162 = next((p for i, p in enumerate(doc.paragraphs) if i > 190 and p.text.strip().startswith("1.6.2 Research Significance")), None)
    if p_162 is not None:
        intro_el = OxmlElement("w:p")
        p_162._p.addprevious(intro_el)
        intro_p = Paragraph(intro_el, p_162._parent)
        intro_p.style = doc.styles["Normal"]
        r = intro_p.add_run("Table 1.1 summarizes the end-to-end research consistency matrix linking each objective to its causal data modalities, modeling pipelines, evaluation metrics, and thesis chapters.")
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

        cap_el = OxmlElement("w:p")
        p_162._p.addprevious(cap_el)
        cap_p = Paragraph(cap_el, p_162._parent)
        cap_p.style = doc.styles["Caption"] if "Caption" in doc.styles else doc.styles["Normal"]
        rc = cap_p.add_run("Table 1.1: Research consistency matrix aligning objectives, data, models, and evaluation metrics")
        rc.font.name = "Times New Roman"
        rc.font.size = Pt(10)
        rc.bold = True

        tbl = doc.add_table(rows=5, cols=5)
        tbl.style = "Table Grid"
        headers = [
            "Objective / Research Question",
            "Data & Causal Features",
            "Models & Split Protocol",
            "Reliability & Evaluation Metrics",
            "Chapters",
        ]
        rows_data = [
            [
                "O1: Extend forecasting beyond short-term detection to 1–15 days (24–360 h)",
                "86,928 aligned hours (2015–2024); 115 clean causal features across 5 modalities (Ground_METAR, ERA5_Physics, Calendar_Diurnal, Satellite/CAMS Detrended)",
                "Strict 70/15/15 chronological split with 360 h (15-day) purge gaps; train-only de-censoring & Yeo-Johnson",
                "5-fold rolling-origin CV; out-of-sample ROC-AUC, PR-AUC, BSS, Lift@Top10%, RMSE, R²",
                "Ch. 3 (3.2–3.4), Ch. 4 (4.1–4.2)",
            ],
            [
                "O2: Compare calibrated tabular ensembles (Line A) vs. deep sequence/physics models (Line B)",
                "115 tabular predictors (Line A) vs. 24 h lookback sequences & 6-node Riyadh domain (Line B)",
                "Line A: LogReg_Bal_Cal, RF_Cal, ET_Cal, HistGB_Cal, XGB_Cal, Ridge; Line B: LSTM, Transformer, PINN, ST-GNN (3 seeds)",
                "Test ROC-AUC, Platt reliability calibration, Brier Skill Score, continuous PM₁₀ RMSE & R²",
                "Ch. 3 (3.7–3.9), Ch. 4 (4.2–4.3), Ch. 5 (5.2)",
            ],
            [
                "O3: Verify physical realism and multi-horizon drivers without data leakage",
                "168 h target & multi-horizon clean hourly predictors (sin_doy, dust_rate_4320h, soil moisture, VPD, gusts)",
                "Six-module XAI audit (XAI-1 to XAI-6) on out-of-sample test partition",
                "Global/Local SHAP, Permutation ROC drop, 1D/2D PDP-ICE, Surrogate fidelity, LSTM saliency",
                "Ch. 3 (3.9.3), Ch. 4 (4.4), Ch. 5 (5.1)",
            ],
            [
                "O4: Translate calibrated risk into operational early-warning actions",
                "Calibrated dust-event probabilities & Lift@Top10% ranking across KKIA (OERK) and Riyadh",
                "4-tier municipal early-warning matrix & regime-shift limitation audit",
                "Recall@Top10%, Lift@Top10% (3.91× at 24 h), false-alarm mitigation, 2023–2024 regime audit",
                "Ch. 3 (3.10), Ch. 5 (5.3–5.4), Ch. 6",
            ],
        ]

        for c_idx, h in enumerate(headers):
            set_cell_text(tbl.rows[0].cells[c_idx], h, bold=True, size=9)
            set_cell_shading(tbl.rows[0].cells[c_idx], "1F4E78")
            for r in tbl.rows[0].cells[c_idx].paragraphs[0].runs:
                from docx.shared import RGBColor
                r.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx, rdata in enumerate(rows_data, start=1):
            for c_idx, val in enumerate(rdata):
                set_cell_text(tbl.rows[r_idx].cells[c_idx], val, bold=(c_idx == 0), size=8.5)
                if r_idx % 2 == 0:
                    set_cell_shading(tbl.rows[r_idx].cells[c_idx], "F2F5F9")

        # Move table right before 1.6.2
        p_162._p.addprevious(tbl._tbl)

    doc.save(str(MASTER_PATH))
    print("Inserted Table 1.1 (Research Consistency Matrix) and renumbered Table 1.2 successfully.")


if __name__ == "__main__":
    main()
