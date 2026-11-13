from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

DOCX_IN = Path(str(PROJECT_ROOT / "Documentation/manuscripts/final/Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2).docx.bak")
DOCX_TEST = Path(str(PROJECT_ROOT / "Documentation/manuscripts/final/test_image_embed.docx")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

def make_drawing_p(r_id, pic_id, pic_name, cx=5486400, cy=3086100):
    p = ET.Element(f"{{{W_NS}}}p")
    pPr = ET.SubElement(p, f"{{{W_NS}}}pPr")
    jc = ET.SubElement(pPr, f"{{{W_NS}}}jc")
    jc.set(f"{{{W_NS}}}val", "center")
    spacing = ET.SubElement(pPr, f"{{{W_NS}}}spacing")
    spacing.set(f"{{{W_NS}}}before", "240")
    spacing.set(f"{{{W_NS}}}after", "120")
    
    r = ET.SubElement(p, f"{{{W_NS}}}r")
    drawing = ET.SubElement(r, f"{{{W_NS}}}drawing")
    inline = ET.SubElement(drawing, f"{{{WP_NS}}}inline")
    inline.set("distT", "0")
    inline.set("distB", "0")
    inline.set("distL", "0")
    inline.set("distR", "0")
    
    extent = ET.SubElement(inline, f"{{{WP_NS}}}extent")
    extent.set("cx", str(cx))
    extent.set("cy", str(cy))
    
    effectExtent = ET.SubElement(inline, f"{{{WP_NS}}}effectExtent")
    effectExtent.set("l", "0")
    effectExtent.set("t", "0")
    effectExtent.set("r", "0")
    effectExtent.set("b", "0")
    
    docPr = ET.SubElement(inline, f"{{{WP_NS}}}docPr")
    docPr.set("id", str(pic_id))
    docPr.set("name", str(pic_name))
    
    cNvGraphicFramePr = ET.SubElement(inline, f"{{{WP_NS}}}cNvGraphicFramePr")
    graphicFrameLocks = ET.SubElement(cNvGraphicFramePr, f"{{{A_NS}}}graphicFrameLocks")
    graphicFrameLocks.set("noChangeAspect", "1")
    
    graphic = ET.SubElement(inline, f"{{{A_NS}}}graphic")
    graphicData = ET.SubElement(graphic, f"{{{A_NS}}}graphicData")
    graphicData.set("uri", PIC_NS)
    
    pic = ET.SubElement(graphicData, f"{{{PIC_NS}}}pic")
    nvPicPr = ET.SubElement(pic, f"{{{PIC_NS}}}nvPicPr")
    cNvPr = ET.SubElement(nvPicPr, f"{{{PIC_NS}}}cNvPr")
    cNvPr.set("id", str(pic_id))
    cNvPr.set("name", str(pic_name))
    
    cNvPicPr = ET.SubElement(nvPicPr, f"{{{PIC_NS}}}cNvPicPr")
    picLocks = ET.SubElement(cNvPicPr, f"{{{A_NS}}}picLocks")
    picLocks.set("noChangeAspect", "1")
    picLocks.set("noChangeArrowheads", "1")
    
    blipFill = ET.SubElement(pic, f"{{{PIC_NS}}}blipFill")
    blip = ET.SubElement(blipFill, f"{{{A_NS}}}blip")
    blip.set(f"{{{R_NS}}}embed", str(r_id))
    blip.set("cstate", "print")
    stretch = ET.SubElement(blipFill, f"{{{A_NS}}}stretch")
    ET.SubElement(stretch, f"{{{A_NS}}}fillRect")
    
    spPr = ET.SubElement(pic, f"{{{PIC_NS}}}spPr")
    xfrm = ET.SubElement(spPr, f"{{{A_NS}}}xfrm")
    off = ET.SubElement(xfrm, f"{{{A_NS}}}off")
    off.set("x", "0")
    off.set("y", "0")
    ext = ET.SubElement(xfrm, f"{{{A_NS}}}ext")
    ext.set("cx", str(cx))
    ext.set("cy", str(cy))
    
    prstGeom = ET.SubElement(spPr, f"{{{A_NS}}}prstGeom")
    prstGeom.set("prst", "rect")
    ET.SubElement(prstGeom, f"{{{A_NS}}}avLst")
    
    return p

print("Image embedder test helper defined successfully.")

