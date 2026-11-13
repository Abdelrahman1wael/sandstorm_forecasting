from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import zipfile
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace('w', W_NS)

def make_p(text, style_id=None, bold=False, italic=False, space_before=120, space_after=120):
    p = ET.Element(f"{{{W_NS}}}p")
    pPr = ET.SubElement(p, f"{{{W_NS}}}pPr")
    if style_id:
        pStyle = ET.SubElement(pPr, f"{{{W_NS}}}pStyle")
        pStyle.set(f"{{{W_NS}}}val", str(style_id))
    
    spacing = ET.SubElement(pPr, f"{{{W_NS}}}spacing")
    spacing.set(f"{{{W_NS}}}before", str(space_before))
    spacing.set(f"{{{W_NS}}}after", str(space_after))
    
    r = ET.SubElement(p, f"{{{W_NS}}}r")
    rPr = ET.SubElement(r, f"{{{W_NS}}}rPr")
    if bold:
        ET.SubElement(rPr, f"{{{W_NS}}}b")
    if italic:
        ET.SubElement(rPr, f"{{{W_NS}}}i")
    
    t = ET.SubElement(r, f"{{{W_NS}}}t")
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return p

def make_tbl(headers, rows):
    tbl = ET.Element(f"{{{W_NS}}}tbl")
    tblPr = ET.SubElement(tbl, f"{{{W_NS}}}tblPr")
    tblStyle = ET.SubElement(tblPr, f"{{{W_NS}}}tblStyle")
    tblStyle.set(f"{{{W_NS}}}val", "13") # Table Grid
    tblW = ET.SubElement(tblPr, f"{{{W_NS}}}tblW")
    tblW.set(f"{{{W_NS}}}w", "9600")
    tblW.set(f"{{{W_NS}}}type", "dxa")
    
    # Header Row
    tr_h = ET.SubElement(tbl, f"{{{W_NS}}}tr")
    for h in headers:
        tc = ET.SubElement(tr_h, f"{{{W_NS}}}tc")
        tcPr = ET.SubElement(tc, f"{{{W_NS}}}tcPr")
        p = make_p(h, bold=True, space_before=60, space_after=60)
        tc.append(p)
        
    for r in rows:
        tr = ET.SubElement(tbl, f"{{{W_NS}}}tr")
        for val in r:
            tc = ET.SubElement(tr, f"{{{W_NS}}}tc")
            p = make_p(str(val), space_before=40, space_after=40)
            tc.append(p)
            
    return tbl

print("Helper defined successfully.")

