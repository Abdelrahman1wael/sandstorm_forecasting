"""Align Section 3.2 Sources of Data and Table 1 with Section 3.1 (2015-2024, 06_Data/data/)
in FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_LATEST_REV33.docx.
"""

from pathlib import Path
import docx

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_LATEST_REV33.docx"
)

S32_BULLETS = [
    "Ground truth observations (OERK and OERY, NOAA / Iowa State Mesonet ASOS): Hourly 2015–2024 METAR observations for King Khalid International Airport (OERK) and Riyadh Air Base (OERY) were consolidated into riyadh_line_a_tabular_features.csv (87,456 hours × 113 columns, 2 January 2015 to 23 December 2024) and the clean master dataset riyadh_hourly_clean_tvt.csv (86,928 hours × 126 columns, 9 January 2015 to 8 December 2024), containing 5,795 confirmed dust-event hours (clean_dust_event = 1), calibrated PM₁₀, visibility, wind speed/gusts, temperature, dew point, and relative humidity.",
    "ECMWF ERA5 hourly reanalysis: 26 harmonised ERA5 columns (19 base physical variables plus 24 h, 72 h, and 168 h rolling wind and gust statistics) are merged at hourly resolution, covering 10 m wind components (u10, v10), 10 m wind speed, direction, and gusts, wind kinetic energy, friction-velocity proxy, 2 m temperature, dew point, relative humidity, apparent temperature, surface pressure, soil temperature (0–7 cm), top-layer (0–7 cm) and deep (7–28 cm) soil moisture, boundary-layer height (era5_blh_m), solar radiation fluxes, and FAO reference evapotranspiration.",
    "Satellite remote sensing (NASA POWER, AERONET, MODIS): Seven harmonised hourly satellite columns are integrated into the master table, including satellite-retrieved PM₂.₅ (sat_retrieved_pm2_5), dust column mass (sat_dust_column_mass), detrended PM₁₀ and AOD₅₅₀ z-scores (sat_retrieved_pm10_detrended_z, sat_aod_550nm_detrended_z), and NASA POWER all-sky, clear-sky, and clearness-index surface solar irradiance.",
    "Multi-modal NWP/satellite tensors and spatial graph (Line B): For deep spatiotemporal architectures, line_b_final_dataset.npz packages 400 multi-modal samples containing NWP spatial grids (6×16×16), satellite spatial grids (3×32×32), 24-hour multi-node sequences (24×6×12), static node features (6×12), and multi-horizon targets (6×6), paired with the 6×6 weighted spatial adjacency matrix (riyadh_graph_adjacency_matrix.npy).",
]

TABLE_1_ROWS = [
    ["Data modality", "Storage path", "Primary file", "Format", "Size", "Records / dimension"],
    [
        "Clean hourly TVT master",
        "06_Data/data/",
        "riyadh_hourly_clean_tvt.csv",
        "CSV",
        "120.32 MB",
        "86,928 hrs × 126 cols (2015-01-09 to 2024-12-08; 5,795 dust hrs; 61,176 / 8,760 / 16,992 split)",
    ],
    [
        "Line A tabular features",
        "06_Data/data/",
        "riyadh_line_a_tabular_features.csv",
        "CSV",
        "94.80 MB",
        "87,456 hrs × 113 cols (2015-01-02 to 2024-12-23; OERK + ERA5 + Satellite)",
    ],
    [
        "Line B multi-modal tensors",
        "06_Data/data/",
        "line_b_final_dataset.npz",
        "NPZ",
        "0.18 MB",
        "400 samples: NWP (6×16×16), Sat (3×32×32), Seq (24×6×12), Nodes (6×12), Targets (6×6)",
    ],
    [
        "Spatial graph adjacency",
        "06_Data/data/",
        "riyadh_graph_adjacency_matrix.npy",
        "NPY",
        "272 B",
        "6×6 weighted regional station adjacency matrix",
    ],
]


def add_para_before(anchor_el, text: str, style: str, doc: docx.Document):
    p = doc.add_paragraph(text, style=style)
    el = p._element
    el.getparent().remove(el)
    anchor_el.addprevious(el)
    return p


def main() -> None:
    doc = docx.Document(str(DOC_PATH))
    body = doc._body._body

    s32_p = next(p for p in doc.paragraphs if p.style.name == "Heading 2" and p.text.strip().startswith("3.2"))
    s33_p = next(p for p in doc.paragraphs if p.style.name == "Heading 2" and p.text.strip().startswith("3.3"))

    s32_el = s32_p._element
    s33_el = s33_p._element

    siblings = list(body)
    i32 = siblings.index(s32_el)
    i33 = siblings.index(s33_el)
    for el in siblings[i32 + 1 : i33]:
        body.remove(el)

    add_para_before(
        s33_el,
        "Operational data pipelines were established for Riyadh through reproducible acquisition and QA/QC scripts (08_Scripts/01_data_acquisition/download_all_real_riyadh_data.py, download_era5.py, download_cams.py, download_modis_aod.py, and 08_Scripts/02_data_verification_qaqc/qaqc_report.py), expanding earlier short-window prototypes into a unified ten-year (2015–2024) empirical multi-modal repository stored in 06_Data/data/:",
        "Normal",
        doc,
    )
    for b in S32_BULLETS:
        add_para_before(s33_el, b, "List Paragraph", doc)

    add_para_before(s33_el, "Table 1 summarises the complete model-ready dataset inventory in 06_Data/data/.", "Normal", doc)
    add_para_before(s33_el, "Table 1: Verified multi-modal dataset inventory in 06_Data/data/ (2015–2024)", "Normal", doc)

    tbl = doc.add_table(rows=len(TABLE_1_ROWS), cols=len(TABLE_1_ROWS[0]))
    tbl.style = "Table Grid"
    for r_i, row in enumerate(TABLE_1_ROWS):
        for c_i, val in enumerate(row):
            tbl.rows[r_i].cells[c_i].text = val
    el_tbl = tbl._element
    el_tbl.getparent().remove(el_tbl)
    s33_el.addprevious(el_tbl)

    try:
        doc.save(str(DOC_PATH))
        print(f"Updated 3.2 and Table 1 in {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name(DOC_PATH.stem + "_SYNCED.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
