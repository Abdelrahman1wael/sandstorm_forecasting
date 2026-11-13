from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import zipfile
import xml.etree.ElementTree as ET

DOCX_PATH = str(PROJECT_ROOT / "Documentation/manuscripts/final/Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2).docx"

with zipfile.ZipFile(DOCX_PATH, 'r') as docx:
    xml_content = docx.read('word/document.xml')

root = ET.fromstring(xml_content)
namespaces = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
}

paragraphs = root.findall('.//w:p', namespaces)
print(f"Total paragraphs: {len(paragraphs)}")

headings = []
for i, p in enumerate(paragraphs):
    text = "".join([t.text for t in p.findall('.//w:t', namespaces) if t.text])
    pStyle = p.find('.//w:pPr/w:pStyle', namespaces)
    style_val = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if pStyle is not None else None
    if style_val or any(text.startswith(h) for h in ["Chapter", "1.", "2.", "3.", "4.", "5.", "6.", "Section"]):
        headings.append((i, style_val, text[:80]))

for idx, style, h_text in headings[-25:]:
    print(f"p[{idx}] ({style}): {h_text}")

