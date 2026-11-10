import zipfile
import xml.etree.ElementTree as ET

def extract_paragraphs(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        xml_content = z.read('word/document.xml')
    tree = ET.fromstring(xml_content)
    paragraphs = []
    for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        text = ''.join(node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text).strip()
        if text:
            paragraphs.append(text)
    return paragraphs

paras = extract_paragraphs('Documentation/my research proposal.docx')
print(f"Total paragraphs: {len(paras)}")
with open('scripts/extracted_proposal.txt', 'w', encoding='utf-8') as out:
    for i, p in enumerate(paras):
        plower = p.lower()
        if any(k in plower for k in ['traditional', 'short-term', 'medium-term', 'long-term', 'small', 'spatial', 'temporal', 'methodology', 'framework', 'scale', 'model']):
            if len(p) > 30:
                out.write(f"[{i}] {p}\n\n")
print("Done writing to scripts/extracted_proposal.txt")
