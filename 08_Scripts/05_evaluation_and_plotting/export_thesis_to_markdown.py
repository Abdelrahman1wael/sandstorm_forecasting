from pathlib import Path
import re
from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.table import Table

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
DOC_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v3.docx"
OUT_MD = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_COMPLETE.md"
FIG_OUT_DIR = ROOT / "01_Documentation" / "thesis_figures"


def clean_cell(txt: str) -> str:
    txt = re.sub(r"\s+", " ", txt.strip())
    return txt.replace("|", "\\|")


def table_to_md(tbl: Table) -> str:
    rows = []
    for r in tbl.rows:
        cells = [clean_cell(c.text) for c in r.cells]
        rows.append(cells)
    if not rows:
        return ""
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    lines = [
        "| " + " | ".join(rows[0]) + " |",
        "| " + " | ".join(["---"] * ncols) + " |",
    ]
    for r in rows[1:]:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def main():
    FIG_OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = Document(str(DOC_PATH))
    rels = doc.part.rels
    body = doc.element.body

    md_lines = [
        "---",
        'title: "Machine Learning for Medium- to Long-Term Sand and Dust Storm Forecasting in Saudi Arabia, with Special Emphasis on Riyadh"',
        'author: "Author Name"',
        'date: "2026"',
        "---",
        "",
    ]

    pending_img_path = None
    img_counter = 0

    for child in body:
        tag = child.tag.split("}")[-1]

        if tag == "p":
            p = Paragraph(child, doc)
            style = p.style.name if p.style else "Normal"
            txt = p.text.strip()

            # Skip auto-generated Word TOC / LOF / LOT entries (LaTeX generates these)
            if style.startswith("toc") or style == "table of figures":
                continue
            if txt.startswith(("TABLE OF CONTENTS", "LIST OF FIGURES", "LIST OF TABLES")):
                continue
            if txt.startswith("LIST OF ABBREVIATIONS"):
                md_lines.append("\n# List of Abbreviations\n")
                continue

            # Extract any embedded figure in this paragraph
            blips = child.xpath('.//*[local-name()="blip"]')
            if blips:
                rid = blips[0].get(qn("r:embed"))
                if rid in rels:
                    part = rels[rid].target_part
                    img_counter += 1
                    ext = Path(part.partname).suffix or ".png"
                    # Skip cover-page university logo (first image before ABSTRACT)
                    if img_counter == 1 and len(md_lines) < 20:
                        continue
                    fname = f"fig_{img_counter:02d}{ext}"
                    (FIG_OUT_DIR / fname).write_bytes(part.blob)
                    pending_img_path = f"thesis_figures/{fname}"
                continue

            if not txt:
                continue

            # Headings
            if style == "Heading 1":
                md_lines.append(f"\n# {txt}\n")
            elif style == "Heading 2":
                md_lines.append(f"\n## {txt}\n")
            elif style == "Heading 3":
                md_lines.append(f"\n### {txt}\n")
            elif txt in ("ABSTRACT", "摘  要"):
                md_lines.append(f"\n# {txt}\n")
            elif re.match(r"^Figure\s+\d+\.\d+\s*:", txt):
                if pending_img_path:
                    md_lines.append(f"\n![{txt}]({pending_img_path})\n")
                    pending_img_path = None
                else:
                    md_lines.append(f"\n*{txt}*\n")
            elif re.match(r"^Table\s+[A-Z0-9]+\.\d+\s*:", txt):
                md_lines.append(f"\n**{txt}**\n")
            elif style == "List Paragraph":
                if re.match(r"^\d+[\.\)]\s+", txt):
                    md_lines.append(f"{txt}")
                else:
                    md_lines.append(f"- {txt}")
            else:
                if pending_img_path:
                    md_lines.append(f"\n![]({pending_img_path})\n")
                    pending_img_path = None
                md_lines.append(f"{txt}\n")

        elif tag == "tbl":
            tbl = Table(child, doc)
            md_tbl = table_to_md(tbl)
            if md_tbl:
                md_lines.append(f"\n{md_tbl}\n")

    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")
    word_count = len(OUT_MD.read_text(encoding="utf-8").split())
    print(f"Exported complete thesis Markdown: {OUT_MD.name} ({word_count:,} words, {img_counter - 1} figures in {FIG_OUT_DIR.name}/)")


if __name__ == "__main__":
    main()
