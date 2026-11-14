"""Remove mock personal information (Yuyan, 202461024, Prof. Zhang Wei, Gender: Female)
and move Acknowledgements (致谢) before Chapter 1 / Abstract in the thesis .docx.
"""

from pathlib import Path
import docx

TARGET_DOCS = [
    Path(r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting.docx"),
    Path(r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2_REFS_UPDATED.docx"),
]

REPLACEMENTS = [
    ("Yuyan (语嫣)", "_________________________"),
    ("202461024", "_________________________"),
    ("Prof. Zhang Wei (张伟 教授)", "_________________________"),
    ("Gender: Female", "Gender: _____________"),
    ("November 2026", "2027"),
    ("September 2024 – June 2027 (Expected)", "September 2025 – June 2027 (Expected)"),
]


def clean_text_in_para(p) -> None:
    txt = p.text
    changed = False
    for old, new in REPLACEMENTS:
        if old in txt:
            txt = txt.replace(old, new)
            changed = True
    if changed:
        # Preserve style & font of first run if present
        bold = p.runs[0].bold if p.runs else False
        size = p.runs[0].font.size if p.runs else None
        p.text = txt
        if p.runs:
            p.runs[0].bold = bold
            if size:
                p.runs[0].font.size = size


def update_doc(doc_path: Path) -> None:
    if not doc_path.exists():
        return
    doc = docx.Document(str(doc_path))

    # 1. Remove mock personal info across all paragraphs and tables
    for p in doc.paragraphs:
        clean_text_in_para(p)
    for tbl in doc.tables:
        try:
            for row in tbl.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        clean_text_in_para(p)
        except Exception:
            pass

    # 2. Move Acknowledgements before Abstract / Chapter 1 (if currently after References)
    ack_idx = None
    resume_idx = None
    anchor_idx = None
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if p.style.name == "Heading 1" and (t.startswith("Abstract") or t.startswith("Chapter 1")) and anchor_idx is None:
            anchor_idx = i
        if p.style.name == "Heading 1" and t.startswith("Acknowledgements"):
            ack_idx = i
        elif ack_idx is not None and p.style.name == "Heading 1":
            resume_idx = i
            break

    if ack_idx is not None and anchor_idx is not None and ack_idx > anchor_idx:
        end_idx = resume_idx if resume_idx is not None else len(doc.paragraphs)
        ack_elements = [doc.paragraphs[i]._element for i in range(ack_idx, end_idx)]
        anchor_el = doc.paragraphs[anchor_idx]._element
        for el in ack_elements:
            el.getparent().remove(el)
            anchor_el.addprevious(el)
        print(f"{doc_path.name}: Moved Acknowledgements ({len(ack_elements)} paragraphs) before {doc.paragraphs[anchor_idx].text.strip()}.")

    try:
        doc.save(str(doc_path))
        print(f"Saved {doc_path.name} successfully.")
    except PermissionError:
        alt = doc_path.with_name(doc_path.stem + "_CLEAN_PERSONAL.docx")
        doc.save(str(alt))
        print(f"{doc_path.name} locked by Word; saved to {alt.name}.")


def main() -> None:
    for p in TARGET_DOCS:
        update_doc(p)


if __name__ == "__main__":
    main()
