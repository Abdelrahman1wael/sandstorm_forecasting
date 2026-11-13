from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import zipfile
import xml.etree.ElementTree as ET

DOCX_PATH = str(PROJECT_ROOT / "Documentation/manuscripts/final/Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2).docx"

with zipfile.ZipFile(DOCX_PATH, 'r') as docx:
    doc_content = docx.read('word/document.xml')
    rels_content = docx.read('word/_rels/document.xml.rels')

print("RELS:")
print(rels_content.decode('utf-8'))

root = ET.fromstring(doc_content)
# find all elements containing 'blip'
for elem in root.iter():
    if elem.tag.endswith('blip'):
        print("BLIP:", elem.tag, elem.attrib)
        # print ancestor drawing or p

