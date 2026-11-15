from pathlib import Path
from docx import Document
from docx.shared import Pt

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
SRC_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v3.docx"
BLIND_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_BLIND_REVIEW.docx"


def replace_in_para(p, old, new):
    if old in p.text:
        p.text = p.text.replace(old, new)
        for r in p.runs:
            r.font.name = "Times New Roman"
            if p.style.name == "Normal":
                r.font.size = Pt(11)


def main():
    doc = Document(str(SRC_PATH))
    body = doc.element.body

    # 1. Remove duplicate Figure 3.11 (nb03_fig05.png) from Chapter 3 so it appears ONLY in Chapter 4 (Figure 4.10)
    fig311_idx = next(
        (i for i, p in enumerate(doc.paragraphs) if i > 200 and p.text.strip().startswith("Figure 3.11:")),
        None,
    )
    if fig311_idx is not None:
        cap_el = doc.paragraphs[fig311_idx]._p
        img_el = cap_el.getprevious()
        # Verify img_el contains a drawing/picture before removing
        if img_el is not None and len(img_el.xpath(".//*[local-name()='blip']")) > 0:
            body.remove(img_el)
        body.remove(cap_el)

    # Also remove Figure 3.11 entry from LIST OF FIGURES (index < 186)
    lof311_idx = next(
        (i for i, p in enumerate(doc.paragraphs[:186]) if p.text.strip().startswith("Figure 3.11:")),
        None,
    )
    if lof311_idx is not None:
        body.remove(doc.paragraphs[lof311_idx]._p)

    # Renumber Figure 3.12 -> Figure 3.11 everywhere (LOF, Ch 3, Ch 5)
    for p in doc.paragraphs:
        if "Figure 3.12" in p.text:
            replace_in_para(p, "Figure 3.12", "Figure 3.11")

    # 2. Harmonize remaining date labels across TOC, LOF, LOT, Ch 3, Ch 4, Ch 6
    date_replacements = [
        ("Independent 2023–2024 Tabular Evaluation", "Independent Out-of-Sample Tabular Evaluation"),
        ("validation (2022) vs. test (2023–2024)", "validation (2 Jan 2022 – 14 Jun 2023) vs. test (29 Jun 2023 – 8 Dec 2024)"),
        ("on the 2023–2024 test set", "on the out-of-sample test set"),
        ("untouched 2023–2024 test partition", "untouched out-of-sample test partition"),
        ("highest-risk 2023–2024 test timestamp", "highest-risk out-of-sample test timestamp"),
        ("between 2015–2021 and 2023–2024", "between the training and test partitions"),
        ("2015–2021 train, 2022 validation, 2023–2024 untouched test", "9 Jan 2015 – 18 Dec 2021 train, 2 Jan 2022 – 14 Jun 2023 validation, 29 Jun 2023 – 8 Dec 2024 test"),
    ]
    for p in doc.paragraphs:
        for old, new in date_replacements:
            if old in p.text:
                replace_in_para(p, old, new)

    # Save polished master copy
    out_master = SRC_PATH
    try:
        doc.save(str(out_master))
        print(f"Saved polished master: {out_master.name}")
    except PermissionError:
        out_master = SRC_PATH.with_name("USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v4.docx")
        doc.save(str(out_master))
        print(f"LOCKED {SRC_PATH.name}; saved polished master to {out_master.name}")

    # 3. Create anonymized Blind Review copy
    blind_doc = Document(str(out_master))
    pii_replacements = [
        ("Associate Professor Wen Wei (温维)", "[Supervisor Name Redacted for Blind Review]"),
        ("语嫣 yuyan", "[Author Name Redacted for Blind Review]"),
        ("202461024", "[Student ID Redacted]"),
    ]
    for p in blind_doc.paragraphs:
        for old, new in pii_replacements:
            if old in p.text:
                replace_in_para(p, old, new)

    # Redact Acknowledgements body (paragraphs between Acknowledgements Heading 1 and ABSTRACT)
    ack_idx = next((i for i, p in enumerate(blind_doc.paragraphs) if p.style.name == "Heading 1" and "Acknowledgements" in p.text), None)
    abs_idx = next((i for i, p in enumerate(blind_doc.paragraphs) if p.text.strip() == "ABSTRACT"), None)
    if ack_idx is not None and abs_idx is not None:
        first_body = True
        for i in range(ack_idx + 1, abs_idx):
            txt = blind_doc.paragraphs[i].text.strip()
            if txt:
                if first_body:
                    blind_doc.paragraphs[i].text = ""
                    r = blind_doc.paragraphs[i].add_run("[Acknowledgements redacted for double-blind peer review.]")
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)
                    first_body = False
                else:
                    blind_doc.paragraphs[i].text = ""

    blind_doc.save(str(BLIND_PATH))
    print(f"Saved blind-review copy: {BLIND_PATH.name}")


if __name__ == "__main__":
    main()
