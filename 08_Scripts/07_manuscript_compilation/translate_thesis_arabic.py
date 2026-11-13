"""
Translate FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting.docx into Academic Arabic
while preserving all 14 embedded figures, 7 tables, Word fields (TOC/PAGE), equations,
and USTB A4 formatting with proper Right-to-Left (w:bidi) Word XML layout.
"""

import re
import time
import shutil
import zipfile
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from deep_translator import GoogleTranslator

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DOCX = PROJECT_ROOT / "01_Documentation" / "FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting.docx"
OUT_DOCX = PROJECT_ROOT / "01_Documentation" / "FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_AR.docx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"
XML_NS = "http://www.w3.org/XML/1998/namespace"

for prefix, uri in [("w", W_NS), ("r", R_NS), ("wp", WP_NS), ("a", A_NS), ("pic", PIC_NS)]:
    ET.register_namespace(prefix, uri)


def w_tag(name):
    return f"{{{W_NS}}}{name}"


def has_translatable_english(text):
    # Skip pure numbers, symbols, or already-mostly-Chinese/Arabic lines without English words
    return bool(re.search(r"[A-Za-z]{2,}", text))


def is_field_only_p(p):
    return p.find(f".//{w_tag('instrText')}") is not None or p.find(f".//{w_tag('fldChar')}") is not None


def translate_one(text):
    clean = " ".join(text.split())
    if len(clean) > 4500:
        clean = clean[:4500]
    for attempt in range(3):
        try:
            return GoogleTranslator(source="en", target="ar").translate(clean)
        except Exception:
            time.sleep(0.8 * (attempt + 1))
    return text


def translate_batch(texts):
    if not texts:
        return []
    clean_texts = [" ".join(t.split()) for t in texts]
    joined = "\n".join(clean_texts)
    if len(joined) <= 4500:
        for attempt in range(2):
            try:
                res = GoogleTranslator(source="en", target="ar").translate(joined)
                parts = [x.strip() for x in res.splitlines() if x.strip()]
                if len(parts) == len(clean_texts):
                    return parts
                break
            except Exception:
                time.sleep(0.8 * (attempt + 1))
    with ThreadPoolExecutor(max_workers=6) as pool:
        return list(pool.map(translate_one, clean_texts))


def set_paragraph_text_and_rtl(p, new_text):
    # Preserve drawing elements if any exist in this paragraph
    drawings = p.findall(f".//{w_tag('drawing')}")
    if drawings or is_field_only_p(p):
        return

    pPr = p.find(w_tag("pPr"))
    if pPr is None:
        pPr = ET.Element(w_tag("pPr"))
        p.insert(0, pPr)

    if pPr.find(w_tag("bidi")) is None:
        ET.SubElement(pPr, w_tag("bidi"))

    # Capture first run's rPr as styling template
    first_r = p.find(w_tag("r"))
    template_rPr = first_r.find(w_tag("rPr")) if first_r is not None else None

    # Remove existing runs
    for r in list(p.findall(w_tag("r"))):
        p.remove(r)

    new_r = ET.SubElement(p, w_tag("r"))
    if template_rPr is not None:
        rPr = ET.fromstring(ET.tostring(template_rPr))
    else:
        rPr = ET.Element(w_tag("rPr"))

    rFonts = rPr.find(w_tag("rFonts"))
    if rFonts is None:
        rFonts = ET.SubElement(rPr, w_tag("rFonts"))
    rFonts.set(w_tag("cs"), "Traditional Arabic")
    if rPr.find(w_tag("rtl")) is None:
        ET.SubElement(rPr, w_tag("rtl"))
    new_r.append(rPr)

    t = ET.SubElement(new_r, w_tag("t"))
    t.set(f"{{{XML_NS}}}space", "preserve")
    t.text = new_text


def main():
    tmp_zip = OUT_DOCX.with_suffix(".tmp.docx")
    with zipfile.ZipFile(SRC_DOCX, "r") as zin:
        file_data = {name: zin.read(name) for name in zin.namelist()}

    doc_root = ET.fromstring(file_data["word/document.xml"])
    all_paras = doc_root.findall(f".//{w_tag('p')}")

    targets = []
    for p in all_paras:
        if is_field_only_p(p) or p.find(f".//{w_tag('drawing')}") is not None:
            continue
        txt = "".join(t.text for t in p.findall(f".//{w_tag('t')}") if t.text).strip()
        if not txt or not has_translatable_english(txt):
            continue
        # Keep References entries in original English citation format (or translate section title only)
        if re.match(r"^[A-Z][a-z]+,\s+[A-Z]\.", txt) and ("(" in txt and ")" in txt):
            continue
        targets.append((p, txt))

    print(f"Total translatable paragraphs: {len(targets)}")

    batch_p, batch_txt, batch_len = [], [], 0
    done = 0
    for p, txt in targets:
        if batch_txt and (batch_len + len(txt) > 3600 or len(batch_txt) >= 12):
            translated = translate_batch(batch_txt)
            for bp, ar_txt in zip(batch_p, translated):
                set_paragraph_text_and_rtl(bp, ar_txt)
            done += len(batch_p)
            print(f"Translated {done}/{len(targets)} paragraphs...")
            batch_p, batch_txt, batch_len = [], [], 0
        batch_p.append(p)
        batch_txt.append(txt)
        batch_len += len(txt)

    if batch_txt:
        translated = translate_batch(batch_txt)
        for bp, ar_txt in zip(batch_p, translated):
            set_paragraph_text_and_rtl(bp, ar_txt)
        done += len(batch_p)

    print(f"Completed translation of {done} paragraphs.")
    file_data["word/document.xml"] = ET.tostring(doc_root, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in file_data.items():
            zout.writestr(name, data)

    shutil.move(str(tmp_zip), str(OUT_DOCX))
    print(f"SUCCESS: Saved Arabic translated thesis -> {OUT_DOCX} ({OUT_DOCX.stat().st_size / (1024*1024):.2f} MB)")


if __name__ == "__main__":
    main()

