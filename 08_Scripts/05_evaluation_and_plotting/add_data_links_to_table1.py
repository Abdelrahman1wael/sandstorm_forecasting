"""Add clickable real-data source URLs to Table 1 (doc.tables[0]) in
01_Documentation/FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting.docx
without altering any other part of the document.
"""

from pathlib import Path
import docx
from docx.shared import Pt, RGBColor, Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOCX_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting.docx"
)

ROW_URLS = {
    1: ("IEM ASOS/METAR", "https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py"),
    2: ("IEM ASOS / KAPSARC", "https://datasource.kapsarc.org/api/explore/v2.1/catalog/datasets/air-quality/records"),
    3: ("Copernicus CDS (ERA5)", "https://cds.climate.copernicus.eu/api"),
    4: ("Open-Meteo ERA5 Archive", "https://archive-api.open-meteo.com/v1/archive"),
    5: ("NASA SRTM / Earthdata", "https://www.earthdata.nasa.gov/"),
    6: ("OpenAQ v3 Riyadh", "https://api.openaq.org/v3/locations/3185012/sensors"),
    7: ("Copernicus ADS (CAMS)", "https://ads.atmosphere.copernicus.eu/api"),
    8: ("Open-Meteo CAMS/IFS", "https://air-quality-api.open-meteo.com/v1/air-quality"),
    9: ("Copernicus ADS (CAMS)", "https://ads.atmosphere.copernicus.eu/api"),
    10: ("Open-Meteo CAMS AOD", "https://air-quality-api.open-meteo.com/v1/air-quality"),
    11: ("NASA POWER API", "https://power.larc.nasa.gov/api/temporal/hourly/point"),
}


def add_hyperlink(paragraph, url: str, text: str) -> None:
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    rPr.append(color)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "16")  # 8 pt
    rPr.append(sz)
    new_run.append(rPr)

    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def main() -> None:
    doc = docx.Document(str(DOCX_PATH))
    tbl = doc.tables[0]

    # Check if Source URL column already exists
    headers = [c.text.strip() for c in tbl.rows[0].cells]
    if "Source URL" in headers:
        col_idx = headers.index("Source URL")
    else:
        col = tbl.add_column(Inches(1.8))
        col_idx = len(tbl.rows[0].cells) - 1
        hdr_cell = tbl.rows[0].cells[col_idx]
        hdr_cell.text = ""
        r = hdr_cell.paragraphs[0].add_run("Source URL")
        r.bold = True
        r.font.size = Pt(9)

    for row_idx, (label, url) in ROW_URLS.items():
        if row_idx < len(tbl.rows):
            cell = tbl.rows[row_idx].cells[col_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            add_hyperlink(p, url, url)

    try:
        doc.save(str(DOCX_PATH))
        out = DOCX_PATH
    except PermissionError:
        out = DOCX_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_WITH_LINKS.docx")
        doc.save(str(out))
    print(f"Added {len(ROW_URLS)} clickable real-data URLs to Table 1 in {out}")


if __name__ == "__main__":
    main()
