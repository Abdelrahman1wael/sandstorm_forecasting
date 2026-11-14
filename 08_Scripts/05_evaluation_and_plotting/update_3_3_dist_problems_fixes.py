"""Update ONLY Section 3.3 in FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_LATEST.docx
to cover Data Distribution, Merging Problems, and Cleaning/Fixing Solutions
with exact statistics and figures from 04_Notebooks/00 & 01 and 07_Figures/.
"""

from pathlib import Path
import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_LATEST.docx"
)
FIG_DIR = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting\07_Figures")

TABLE_2 = [
    ["Hazard tier", "PM₁₀ range (μg/m³)", "Municipal action level"],
    ["Normal", "< 50", "Level 1 (Green)"],
    ["Moderate", "50 – 150", "Level 2 (Yellow)"],
    ["Elevated Dust", "150 – 500", "Level 3 (Orange)"],
    ["Severe Sandstorm", "500 – 1,500", "Level 4 (Red)"],
    ["Extreme Haboob", "≥ 1,500", "Level 4 (Red)"],
]


def add_para_before(anchor_el, text: str, style: str, doc: docx.Document, align=None):
    p = doc.add_paragraph(text, style=style)
    if align is not None:
        p.alignment = align
    el = p._element
    el.getparent().remove(el)
    anchor_el.addprevious(el)
    return p


def add_figure_before(anchor_el, img_path: Path, caption: str, doc: docx.Document, width_in: float = 5.8):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(str(img_path), width=Inches(width_in))
    el_img = p_img._element
    el_img.getparent().remove(el_img)
    anchor_el.addprevious(el_img)
    add_para_before(anchor_el, caption, "Normal", doc, align=WD_ALIGN_PARAGRAPH.CENTER)


def main() -> None:
    doc = docx.Document(str(DOC_PATH))
    body = doc._body._body

    s33_p = next(p for p in doc.paragraphs if p.style.name == "Heading 2" and p.text.strip().startswith("3.3"))
    s34_p = next(p for p in doc.paragraphs if p.style.name == "Heading 2" and p.text.strip().startswith("3.4"))

    s33_p.text = "3.3 Data Distribution, Merging Problems, and Cleaning Solutions"
    s33_el = s33_p._element
    s34_el = s34_p._element

    siblings = list(body)
    i33 = siblings.index(s33_el)
    i34 = siblings.index(s34_el)
    for el in siblings[i33 + 1 : i34]:
        body.remove(el)

    # 3.3.1 Data Distribution
    add_para_before(s34_el, "3.3.1 Multi-Modal Data Distribution and Temporal Dynamics", "Heading 3", doc)
    add_para_before(
        s34_el,
        "Across the 86,928 aligned hourly records in riyadh_hourly_clean_tvt.csv (2015–2024), surface particulate concentrations exhibit extreme right skewness (11.69 raw; 11.79 cleaned) with a heavy dust-storm tail reaching 4,800.0 μg/m³ (mean 106.12 μg/m³, std 254.14 μg/m³, median 68.00 μg/m³). Confirmed dust-event prevalence also varies sharply across the chronological partitions: 7.47% in Training (2015–2021; 61,176 h), 10.51% in Validation (2022; 8,760 h), and 1.79% in Testing (2023–2024; 16,992 h). Diurnal and seasonal cycles peak during spring afternoon convective mixing and northwesterly Shamal wind outbreaks (Figures 1–2), while operational severity is categorised into five PM₁₀ hazard tiers (Table 2).",
        "Normal",
        doc,
    )
    add_figure_before(s34_el, FIG_DIR / "nb00_fig07.png", "Figure 1: Hourly diurnal cycle and monthly dust-event distribution over Riyadh (00_data_representation_and_distribution_riyadh.ipynb).", doc)
    add_figure_before(s34_el, FIG_DIR / "nb00_fig09.png", "Figure 2: Hourly surface wind rose at OERK showing prevailing northwesterly Shamal transport corridors.", doc)

    add_para_before(s34_el, "Table 2: Five-tier PM₁₀ hazard classification", "Normal", doc)
    tbl = doc.add_table(rows=len(TABLE_2), cols=len(TABLE_2[0]))
    tbl.style = "Table Grid"
    for r_i, row in enumerate(TABLE_2):
        for c_i, val in enumerate(row):
            tbl.rows[r_i].cells[c_i].text = val
    el_tbl = tbl._element
    el_tbl.getparent().remove(el_tbl)
    s34_el.addprevious(el_tbl)

    # 3.3.2 Merging Problems
    add_para_before(s34_el, "3.3.2 Data Merging Problems Discovered", "Heading 3", doc)
    add_para_before(
        s34_el,
        "Auditing the merged multi-source streams in 00_data_representation_and_distribution_riyadh.ipynb and 08_Scripts/03_collocation_and_features/data_handling_and_feature_balancing.py uncovered four concrete merging and distribution defects:",
        "Normal",
        doc,
    )
    add_para_before(
        s34_el,
        "1. Irregular ASOS/METAR reporting and missingness: Raw METAR downloads contained 'M' missing strings, sub-hourly duplicate timestamps, and high missingness in wind gusts and sea-level pressure (Figure 3).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        s34_el,
        "2. Visibility-cap censoring at 53.7 μg/m³: Because routine METAR visibility is capped at 10 km, visibility-calibrated PM₁₀ (pm10_calibrated_ugm3) pinned 79.01% of all 86,928 hours flat at 53.70 μg/m³ (25th, 50th, and 75th percentiles all equal to 53.70 μg/m³), creating an artificial floor spike (Figure 4).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        s34_el,
        "3. Temporal regime shift and satellite drift (2015–2024): Feature-shift auditing (nb01_clean_hourly_feature_impact.csv) revealed large distributional shifts between 2015–2021 and 2023–2024 in sat_dust_column_mass (Test Z-shift = 5.122), dust_rate_4320h (2.277), dust_rate_720h (1.266), and nwp_bias_proxy (1.168), alongside the dust-rate drop from 10.51% (2022) to 1.79% (2023–2024) (Figure 5).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        s34_el,
        "4. Lookahead and contemporaneous target leakage risk: Merging unlagged visibility/weather codes or fitting scalers on the full 10-year series would leak future storm states and test-regime statistics into training.",
        "List Paragraph",
        doc,
    )
    add_figure_before(s34_el, FIG_DIR / "nb00_fig01.png", "Figure 3: Raw hourly missingness (%) across METAR, ERA5, and satellite columns before UTC alignment.", doc)
    add_figure_before(s34_el, FIG_DIR / "nb00_fig02.png", "Figure 4: Raw hourly PM₁₀ proxy showing the 79.01% flat censoring spike at 53.7 μg/m³.", doc)
    add_figure_before(s34_el, FIG_DIR / "nb00_fig03.png", "Figure 5: 2015–2024 regime shift comparing annual dust-event rate decline against satellite drift.", doc)

    # 3.3.3 How It Was Fixed (Merging & Cleaning)
    add_para_before(s34_el, "3.3.3 Merging and Cleaning Solutions Applied", "Heading 3", doc)
    add_para_before(
        s34_el,
        "Each defect was resolved systematically in 01_feature_engineering_and_impact.ipynb and build_and_run_clean_hourly_notebooks.py before model training:",
        "Normal",
        doc,
    )
    add_para_before(
        s34_el,
        "1. Strict UTC hourly grid alignment and multi-modal merging: Raw OERK and OERY METAR reports were converted from 'M' to NaN, resampled onto a uniform UTC hourly index, and inner-aligned with 26 ERA5 columns and 7 satellite columns to produce riyadh_line_a_tabular_features.csv (87,456 × 113) and riyadh_hourly_clean_tvt.csv (86,928 × 126).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        s34_el,
        "2. De-censoring the 53.7 μg/m³ floor spike and Yeo-Johnson scaling: The flat 53.7 μg/m³ floor was de-censored into continuous background values (pm10_clean_ugm3: min 22.02 μg/m³, 25th percentile 64.92 μg/m³, median 68.00 μg/m³), and train-only Yeo-Johnson power transformations suppressed extreme feature skewness (Figure 6).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        s34_el,
        "3. Zero-leakage chronological splitting and cost-sensitive weighting: Random splitting was replaced with a strict chronological split (2015–2021 Train / 2022 Val / 2023–2024 Test). All Yeo-Johnson lambdas, scalers, and mutual-information rankings were fitted strictly on 2015–2021, and class imbalance was handled via balanced class_weight (Line A) and pos_weight (Line B) rather than synthetic SMOTE oversampling.",
        "List Paragraph",
        doc,
    )
    add_figure_before(s34_el, FIG_DIR / "nb01_fig01.png", "Figure 6: Before vs. after de-censoring the 53.7 μg/m³ floor spike and train-only Yeo-Johnson skewness reduction (01_feature_engineering_and_impact.ipynb).", doc)

    try:
        doc.save(str(DOC_PATH))
        print(f"Updated Section 3.3 in {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name(DOC_PATH.stem + "_REV33.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
