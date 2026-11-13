from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile(str(PROJECT_ROOT / 'Documentation/manuscripts/final/Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2).docx') as docx:
    xml_content = docx.read('word/document.xml')
root = ET.fromstring(xml_content)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paras = root.findall('.//w:p', ns)
for idx in range(349, 383):
    t = ''.join([n.text for n in paras[idx].findall('.//w:t', ns) if n.text])
    print(f'p[{idx}]: {t}')

