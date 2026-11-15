import re
from pathlib import Path
from docx import Document
from docx.shared import Pt

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
FILES = [
    ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v3.docx",
    ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_BLIND_REVIEW.docx",
]

SPELLING_MAP = [
    (r"\bmodelling\b", "modeling"),
    (r"\bModelling\b", "Modeling"),
    (r"\boptimis", "optimiz"),
    (r"\bOptimis", "Optimiz"),
    (r"\bnormalis", "normaliz"),
    (r"\bNormalis", "Normaliz"),
    (r"\bcharacteris", "characteriz"),
    (r"\bCharacteris", "Characteriz"),
    (r"\bcategoris", "categoriz"),
    (r"\bCategoris", "Categoriz"),
    (r"\bregularis", "regulariz"),
    (r"\bRegularis", "Regulariz"),
    (r"\bvisualis", "visualiz"),
    (r"\bVisualis", "Visualiz"),
    (r"\borganis", "organiz"),
    (r"\bOrganis", "Organiz"),
    (r"\bcolour\b", "color"),
    (r"\bColour\b", "Color"),
    (r"\bneighbour", "neighbor"),
    (r"\bNeighbour", "Neighbor"),
    (r"\bartefact", "artifact"),
    (r"\bArtefact", "Artifact"),
    (r"\bkilometre", "kilometer"),
    (r"\bKilometre", "Kilometer"),
]


def unify_doc(path: Path):
    doc = Document(str(path))
    ref_idx = next((i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "References" in p.text), len(doc.paragraphs))
    app_idx = next((i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Appendices" in p.text), len(doc.paragraphs))

    changes = 0
    for i, p in enumerate(doc.paragraphs):
        # Preserve verbatim bibliographic titles inside References
        if ref_idx <= i < app_idx:
            continue
        orig = p.text
        new = orig
        if "3.9 Detailed Feature Engineering and Multimodal Input Representation" in new:
            new = new.replace(
                "3.9 Detailed Feature Engineering and Multimodal Input Representation",
                "3.9 Multimodal Feature Groups and 6-Node Domain Overview",
            )
        for pat, rep in SPELLING_MAP:
            new = re.sub(pat, rep, new)
        if new != orig:
            p.text = new
            for r in p.runs:
                r.font.name = "Times New Roman"
                if p.style.name == "Normal":
                    r.font.size = Pt(11)
            changes += 1

    # Also unify in tables
    for tbl in doc.tables:
        for row in tbl.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    orig = p.text
                    new = orig
                    for pat, rep in SPELLING_MAP:
                        new = re.sub(pat, rep, new)
                    if new != orig:
                        p.text = new
                        for r in p.runs:
                            r.font.name = "Times New Roman"
                            r.font.size = Pt(9.5)
                        changes += 1

    doc.save(str(path))
    print(f"Unified US English & section clarity in {path.name}: {changes} edits")


def main():
    for f in FILES:
        unify_doc(f)


if __name__ == "__main__":
    main()
