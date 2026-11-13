from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import zipfile
import xml.etree.ElementTree as ET

DOCX_PATH = str(PROJECT_ROOT / "Documentation/manuscripts/final/Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2).docx"

with zipfile.ZipFile(DOCX_PATH, 'r') as docx:
    rels_content = docx.read('word/_rels/document.xml.rels')
    doc_content = docx.read('word/document.xml')

root_rels = ET.fromstring(rels_content)
print("=== Relationships in document.xml.rels ===")
for r in root_rels:
    print(r.attrib)

root_doc = ET.fromstring(doc_content)
namespaces = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
}

drawings = root_doc.findall('.//w:drawing', namespaces)
print(f"Total drawings in document: {len(drawings)}")
for d in drawings:
    blip = d.find('.//a:blip', namespaces)
    if blip is not None:
        print("Drawing blip:", blip.attrib)
        # parent paragraph

