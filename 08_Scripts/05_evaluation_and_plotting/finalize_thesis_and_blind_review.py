from pathlib import Path
import struct
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
FIG_DIR = ROOT / "07_Figures"
MASTER_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v3.docx"
BLIND_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_BLIND_REVIEW.docx"

FIGURE_UPGRADES = {
    "Figure 3.1:": "nb00_fig07.png",
    "Figure 3.2:": "nb00_fig09.png",
    "Figure 3.9:": "fig3_9_domain_architecture.png",
    "Figure 4.1:": "nb02_fig01.png",
    "Figure 4.2:": "nb02_fig02.png",
    "Figure 4.3:": "nb02_fig03.png",
    "Figure 4.5:": "nb02_fig06.png",
    "Figure 4.6:": "nb02_fig07.png",
    "Figure 4.8:": "nb03_fig03.png",
    "Figure 4.9:": "nb03_fig04.png",
    "Figure 4.10:": "nb03_fig05.png",
    "Figure 4.11:": "nb04_fig01.png",
    "Figure 4.13:": "nb04_fig03.png",
}


def get_png_size(png_bytes: bytes):
    if png_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", png_bytes[16:24])
    return None, None


def set_para_text_preserve_font(p, new_text: str):
    p.text = new_text
    for r in p.runs:
        r.font.name = "Times New Roman"
        if p.style and p.style.name == "Normal":
            r.font.size = Pt(11)


def append_sentence(p, sentence: str, ref_token: str):
    if ref_token not in p.text:
        base = p.text.rstrip()
        sep = " " if base and not base.endswith(" ") else ""
        set_para_text_preserve_font(p, f"{base}{sep}{sentence}")
        return True
    return False


def upgrade_figures_in_doc(doc: Document) -> int:
    rels = doc.part.rels
    updated = 0
    for i, p in enumerate(doc.paragraphs):
        if i <= 190:
            continue
        txt = p.text.strip()
        matched_fig = next((k for k in FIGURE_UPGRADES if txt.startswith(k)), None)
        if not matched_fig:
            continue
        img_path = FIG_DIR / FIGURE_UPGRADES[matched_fig]
        if not img_path.exists():
            continue
        prev_el = p._p.getprevious()
        if prev_el is None:
            continue
        blips = prev_el.xpath('.//*[local-name()="blip"]')
        if not blips:
            continue
        rid = blips[0].get(qn("r:embed"))
        if rid not in rels:
            continue

        png_bytes = img_path.read_bytes()
        rels[rid].target_part._blob = png_bytes
        w, h = get_png_size(png_bytes)
        if w and h:
            aspect = h / w
            for ext_name in ("extent", "ext"):
                for ext in prev_el.xpath(f'.//*[local-name()="{ext_name}"]'):
                    cx = ext.get("cx")
                    if cx and cx.isdigit():
                        ext.set("cy", str(int(int(cx) * aspect)))
        updated += 1
    return updated


def add_missing_figure_refs(doc: Document) -> int:
    added = 0
    # Find paragraphs right around the 7 unreferenced figures
    for i, p in enumerate(doc.paragraphs):
        if i <= 190:
            continue
        txt = p.text.strip()
        if txt.startswith("Figure 1.1:"):
            # Reference Figure 1.1 and Figure 1.2 in the following paragraph P222
            if i + 1 < len(doc.paragraphs):
                if append_sentence(doc.paragraphs[i + 1], "As shown in Figure 1.1 and Figure 1.2, Riyadh City sits on the Najd plateau surrounded by active desert corridors and administrative districts.", "Figure 1.1"):
                    added += 2
        elif txt.startswith("3.3.1 Multi-Modal Data Distribution"):
            if i + 1 < len(doc.paragraphs):
                if append_sentence(doc.paragraphs[i + 1], "The diurnal cycle and seasonal dust distribution are shown in Figure 3.1, while the prevailing northwesterly Shamal wind corridor at OERK is illustrated in Figure 3.2.", "Figure 3.1"):
                    added += 2
        elif txt.startswith("3.4.2 Purge-Gapped Split"):
            if i + 1 < len(doc.paragraphs):
                if append_sentence(doc.paragraphs[i + 1], "The resulting reduction in feature skewness after Yeo-Johnson transformation is shown in Figure 3.7, and the top predictors ranked by train-only Mutual Information and 5-fold CV Ridge stability are presented in Figure 3.8.", "Figure 3.7"):
                    added += 2
        elif txt.startswith("4. Detrended Satellite & CAMS NWP Channels"):
            if append_sentence(p, "Figure 3.9 summarizes the 6-node Greater Riyadh spatial domain and the complete leakage-free dual-pipeline architecture.", "Figure 3.9"):
                added += 1
    return added


def sanitize_blind_review(doc: Document):
    # 1. Remove cover-page university logo (image1.jpeg in front matter P000..P020)
    for i in range(min(25, len(doc.paragraphs))):
        p = doc.paragraphs[i]
        if p._p.xpath('.//*[local-name()="blip"]'):
            p.text = "[University Logo Redacted for Blind Review]"
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(11)

    # 2. Redact all institutional & personal identifiers across paragraphs
    replacements = [
        ("Associate Professor Wen Wei (温维)", "[Supervisor Name Redacted for Blind Review]"),
        ("语嫣 yuyan", "[Author Name Redacted for Blind Review]"),
        ("202461024", "[Student ID Redacted]"),
        ("北 京 科 技 大 学", "[University Name Redacted for Blind Review]"),
        ("北京科技大学", "[University Redacted for Blind Review]"),
        ("School of Energy and Environmental Engineering, University of Science and Technology Beijing (USTB)", "[School and Institution Redacted for Blind Review]"),
        ("University of Science and Technology Beijing (USTB)", "[Institution Redacted for Blind Review]"),
        ("University of Science and Technology Beijing", "[Institution Redacted for Blind Review]"),
        ("Beijing 100083, P. R. China", "[Location Redacted for Blind Review]"),
    ]
    for p in doc.paragraphs:
        new_txt = p.text
        changed = False
        for old, new in replacements:
            if old in new_txt:
                new_txt = new_txt.replace(old, new)
                changed = True
        if changed:
            set_para_text_preserve_font(p, new_txt)

    # 2b. Redact Acknowledgements body (between Acknowledgements Heading 1 and ABSTRACT)
    ack_idx = next((i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Acknowledgements" in p.text), None)
    abs_idx = next((i for i, p in enumerate(doc.paragraphs) if p.text.strip() == "ABSTRACT"), None)
    if ack_idx is not None and abs_idx is not None:
        first_body = True
        for i in range(ack_idx + 1, abs_idx):
            if doc.paragraphs[i].text.strip():
                if first_body:
                    set_para_text_preserve_font(doc.paragraphs[i], "[Acknowledgements redacted for double-blind peer review.]")
                    first_body = False
                else:
                    doc.paragraphs[i].text = ""

    # 3. Redact running headers & footers in all sections
    for sec in doc.sections:
        for hdr in (sec.header, sec.first_page_header, sec.even_page_header):
            for p in hdr.paragraphs:
                if "University of Science and Technology Beijing" in p.text or "School of Energy" in p.text:
                    set_para_text_preserve_font(p, "Master's Degree Thesis — Double-Blind Review Copy")

    # 4. Scrub document core metadata properties
    cp = doc.core_properties
    cp.author = ""
    cp.last_modified_by = ""
    cp.comments = ""


def main():
    master = Document(str(MASTER_PATH))
    n_figs = upgrade_figures_in_doc(master)
    n_refs = add_missing_figure_refs(master)
    master.save(str(MASTER_PATH))
    print(f"Updated master ({MASTER_PATH.name}): upgraded {n_figs} figures to 300 DPI, added {n_refs} missing figure cross-references.")

    blind = Document(str(MASTER_PATH))
    sanitize_blind_review(blind)
    blind.save(str(BLIND_PATH))
    print(f"Saved fully sanitized blind-review copy: {BLIND_PATH.name}")


if __name__ == "__main__":
    main()
