from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
MASTER_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v3.docx"

ABBREVIATIONS = [
    ("AOD", "Aerosol Optical Depth"),
    ("BLH", "Boundary Layer Height"),
    ("BSS", "Brier Skill Score"),
    ("CAMS", "Copernicus Atmosphere Monitoring Service"),
    ("CV", "Cross-Validation"),
    ("DOY", "Day of Year"),
    ("ECMWF", "European Centre for Medium-Range Weather Forecasts"),
    ("ERA5", "ECMWF Reanalysis v5"),
    ("ET", "ExtraTrees (Extremely Randomized Trees)"),
    ("GRU", "Gated Recurrent Unit"),
    ("HistGB", "Histogram-Based Gradient Boosting"),
    ("ICE", "Individual Conditional Expectation"),
    ("KKIA", "King Khalid International Airport (OERK)"),
    ("LSTM", "Long Short-Term Memory"),
    ("METAR", "Meteorological Aerodrome Report"),
    ("MI", "Mutual Information"),
    ("MLP", "Multi-Layer Perceptron"),
    ("NWP", "Numerical Weather Prediction"),
    ("OERK", "King Khalid International Airport ICAO Station Code"),
    ("OERY", "Riyadh Air Base ICAO Station Code"),
    ("PDP", "Partial Dependence Plot"),
    ("PINN", "Physics-Informed Neural Network"),
    ("PM₁₀", "Particulate Matter with Aerodynamic Diameter ≤ 10 μm"),
    ("PR-AUC", "Area Under the Precision–Recall Curve"),
    ("RF", "Random Forest"),
    ("RMSE", "Root Mean Squared Error"),
    ("ROC-AUC", "Area Under the Receiver Operating Characteristic Curve"),
    ("SDS", "Sand and Dust Storm"),
    ("SHAP", "SHapley Additive exPlanations"),
    ("ST-GNN", "Spatiotemporal Graph Neural Network"),
    ("VPD", "Vapor Pressure Deficit"),
    ("WMO", "World Meteorological Organization"),
    ("XAI", "Explainable Artificial Intelligence"),
    ("XGBoost", "Extreme Gradient Boosting"),
]


def set_cell_shading(cell, fill_hex: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tcPr.append(shd)


def set_cell_text(cell, text: str, bold: bool = False, size: int = 9.5, white: bool = False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(1.5)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    r.bold = bold
    if white:
        r.font.color.rgb = RGBColor(255, 255, 255)


def main():
    doc = Document(str(MASTER_PATH))
    if any("LIST OF ABBREVIATIONS" in p.text.upper() for p in doc.paragraphs[:210]):
        print("LIST OF ABBREVIATIONS already present.")
        return

    ch1 = next(p for i, p in enumerate(doc.paragraphs) if i > 170 and p.style.name == "Heading 1" and p.text.strip().startswith("Chapter 1"))
    lot_hdr = next(p for p in doc.paragraphs[:190] if "LIST OF TABLES" in p.text.upper())

    # Insert Heading paragraph matching LIST OF TABLES formatting
    hdr_el = OxmlElement("w:p")
    ch1._p.addprevious(hdr_el)
    hdr_p = Paragraph(hdr_el, ch1._parent)
    hdr_p.style = lot_hdr.style
    hdr_p.paragraph_format.page_break_before = True
    r = hdr_p.add_run("LIST OF ABBREVIATIONS (缩略词表)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.bold = True

    tbl = doc.add_table(rows=len(ABBREVIATIONS) + 1, cols=2)
    tbl.style = "Table Grid"
    set_cell_text(tbl.rows[0].cells[0], "Abbreviation", bold=True, size=9.5, white=True)
    set_cell_text(tbl.rows[0].cells[1], "Full Term", bold=True, size=9.5, white=True)
    set_cell_shading(tbl.rows[0].cells[0], "1F4E78")
    set_cell_shading(tbl.rows[0].cells[1], "1F4E78")

    for idx, (abbr, full) in enumerate(ABBREVIATIONS, start=1):
        set_cell_text(tbl.rows[idx].cells[0], abbr, bold=True, size=9.5)
        set_cell_text(tbl.rows[idx].cells[1], full, bold=False, size=9.5)
        if idx % 2 == 0:
            set_cell_shading(tbl.rows[idx].cells[0], "F2F5F9")
            set_cell_shading(tbl.rows[idx].cells[1], "F2F5F9")

    ch1._p.addprevious(tbl._tbl)

    # Trailing blank paragraph before Chapter 1
    sp_el = OxmlElement("w:p")
    ch1._p.addprevious(sp_el)

    doc.save(str(MASTER_PATH))
    print(f"Added LIST OF ABBREVIATIONS ({len(ABBREVIATIONS)} entries) before Chapter 1.")


if __name__ == "__main__":
    main()
