"""Revise ONLY Section 3.1 Study Setting, Section 3.2 Sources of Data, and Table 1
in the thesis .docx to match the latest 10-year hourly project dataset in 06_Data/data/.
"""

from pathlib import Path
import docx

TARGET_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2_REFS_UPDATED_CLEAN_PERSONAL_EXACT61_REFS_MIDTERM_COVER.docx"
)

S31_PARAS = [
    (
        "Normal",
        "The study focuses on Riyadh, the capital of Saudi Arabia, located on the Najd plateau. The primary ground-truth station is King Khalid International Airport (KKIA; ICAO OERK, WMO 40438; 24.9252°N, 46.7213°E; elevation 614 m), supplemented by co-located urban meteorological observations from Riyadh Air Base (ICAO OERY) and a six-node regional spatial graph representing upstream and surrounding dust-transport corridors. Metropolitan Riyadh covers approximately 1,913 km², and the surrounding terrain, including the Jabal Tuwaiq escarpment, ranges from 406 m to 1,119 m above sea level (mean 649.3 m).",
    ),
    (
        "Normal",
        "In the latest multi-modal pipeline, the continuous hourly observation window spans nearly ten full years, from January 2015 to December 2024 (87,456 raw hourly records from 2 January 2015 to 23 December 2024, and 86,928 aligned, leak-free hourly records from 9 January 2015 to 8 December 2024). Capturing ten complete spring dust seasons enables a strict chronological train/validation/test split: 2015–2021 for training (61,176 hours), 2022 for validation (8,760 hours), and 2023–2024 for out-of-sample testing (16,992 hours). Regional numerical weather prediction (NWP) and satellite grids cover 16°N–33°N and 34°E–56°E to represent northern and northwestern dust-source regions affecting Riyadh.",
    ),
]

S32_INTRO = (
    "Normal",
    "Operational data pipelines were established for Riyadh, replacing earlier short-window prototypes with a unified ten-year (2015–2024) empirical multi-modal repository stored in 06_Data/data/. All core modalities were quality-controlled, temporally aligned at hourly resolution, and split chronologically without data leakage:",
)

S32_BULLETS = [
    (
        "List Paragraph",
        "Ground truth observations (KKIA OERK and OERY): The clean master hourly dataset (riyadh_hourly_clean_tvt.csv) comprises 86,928 aligned hourly records (9 January 2015 to 8 December 2024) across 126 columns, including 5,795 confirmed dust-event hours (clean_dust_event = 1), calibrated PM₁₀ concentrations (pm10_calibrated_ugm3), visibility, wind speed/gusts, temperature, dew point, and relative humidity at OERK alongside co-located OERY observations (visibility, wind speed, and temperature). The companion Line A tabular feature file (riyadh_line_a_tabular_features.csv) contains 87,456 hourly records (2 January 2015 to 23 December 2024) across 113 features.",
    ),
    (
        "List Paragraph",
        "ECMWF ERA5 hourly reanalysis: 26 harmonised ERA5 columns (19 base physical fields plus 24 h, 72 h, and 168 h rolling wind and gust statistics) are integrated at hourly resolution, covering 10 m wind components (u10, v10), 10 m wind speed, direction, and gusts, wind kinetic energy, friction-velocity proxy, 2 m temperature, dew point, relative humidity, apparent temperature, surface pressure, soil temperature (0–7 cm), top-layer (0–7 cm) and deep (7–28 cm) soil moisture, boundary-layer height (era5_blh_m), direct/diffuse/shortwave radiation, and FAO reference evapotranspiration.",
    ),
    (
        "List Paragraph",
        "Satellite remote sensing: Seven harmonised hourly satellite columns are integrated into the master dataset, comprising satellite-retrieved PM₂.₅ (sat_retrieved_pm2_5), atmospheric dust column mass (sat_dust_column_mass), detrended PM₁₀ and AOD₅₅₀ z-scores (sat_retrieved_pm10_detrended_z, sat_aod_550nm_detrended_z), and NASA POWER all-sky, clear-sky, and clearness-index surface solar irradiance (sat_solar_allsky_sfc_sw_dwn, sat_solar_clrsky_sfc_sw_dwn, sat_solar_allsky_kt).",
    ),
    (
        "List Paragraph",
        "Multi-modal NWP/satellite tensors and spatial graph (Line B): For deep spatiotemporal architectures, line_b_final_dataset.npz packages 400 multi-modal samples containing NWP spatial grids (6×16×16), satellite spatial grids (3×32×32), 24-hour multi-node sequences (24×6×12), static node features (6×12), and multi-horizon PM₁₀ and hazard-class targets (6×6), coupled with the 6×6 weighted spatial graph adjacency matrix (riyadh_graph_adjacency_matrix.npy).",
    ),
]

TABLE_1_ROWS = [
    ["Data modality", "Storage path", "Primary file", "Format", "Size", "Records / dimension"],
    [
        "Clean hourly TVT master",
        "06_Data/data/",
        "riyadh_hourly_clean_tvt.csv",
        "CSV",
        "120.32 MB",
        "86,928 hrs × 126 cols (2015–2024; 5,795 dust hrs; 61,176 / 8,760 / 16,992 split)",
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
        "400 samples: NWP (6×16×16), Sat (3×32×32), Seq (24×6×12), Targets (6×6)",
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


def insert_para_before(anchor_el, text: str, style_name: str, doc: docx.Document) -> None:
    p = doc.add_paragraph(text, style=style_name)
    el = p._element
    el.getparent().remove(el)
    anchor_el.addprevious(el)


def main() -> None:
    doc = docx.Document(str(TARGET_PATH))

    s31_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 2" and "3.1" in p.text)
    s32_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 2" and "3.2" in p.text)
    s33_idx = next(i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 2" and "3.3" in p.text)

    s32_el = doc.paragraphs[s32_idx]._element
    t1_caption_idx = next(i for i in range(s32_idx + 1, s33_idx) if doc.paragraphs[i].text.strip().startswith("Table 1:"))
    t1_caption_el = doc.paragraphs[t1_caption_idx]._element

    to_remove_31 = [doc.paragraphs[i]._element for i in range(s31_idx + 1, s32_idx)]
    to_remove_32 = [doc.paragraphs[i]._element for i in range(s32_idx + 1, t1_caption_idx)]

    for el in to_remove_31:
        el.getparent().remove(el)
    for el in to_remove_32:
        el.getparent().remove(el)

    for style_name, text in S31_PARAS:
        insert_para_before(s32_el, text, style_name, doc)

    insert_para_before(t1_caption_el, S32_INTRO[1], S32_INTRO[0], doc)
    for style_name, text in S32_BULLETS:
        insert_para_before(t1_caption_el, text, style_name, doc)
    insert_para_before(t1_caption_el, "Table 1 summarises the complete latest dataset inventory.", "Normal", doc)

    # Update Table 1 (doc.tables[1])
    tbl = doc.tables[1]
    # Keep header row + 4 data rows (remove extra rows if tbl has more than 5 rows)
    while len(tbl.rows) > len(TABLE_1_ROWS):
        tr = tbl.rows[-1]._tr
        tr.getparent().remove(tr)
    while len(tbl.rows) < len(TABLE_1_ROWS):
        tbl.add_row()
    for r_idx, row_vals in enumerate(TABLE_1_ROWS):
        for c_idx, val in enumerate(row_vals):
            tbl.rows[r_idx].cells[c_idx].text = val

    try:
        doc.save(str(TARGET_PATH))
        print(f"Updated 3.1, 3.2, and Table 1 in {TARGET_PATH.name}.")
    except PermissionError:
        alt = TARGET_PATH.with_name(TARGET_PATH.stem + "_REV31_32.docx")
        doc.save(str(alt))
        print(f"LOCKED: {TARGET_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
