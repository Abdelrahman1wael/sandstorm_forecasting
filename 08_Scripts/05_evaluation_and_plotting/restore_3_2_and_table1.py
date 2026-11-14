"""Restore the exact user-requested Section 3.2 Sources of Data and Table 1
into the latest thesis .docx, while keeping Sections 3.1 and 3.3-3.6 intact.
"""

from pathlib import Path
import docx

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2_REFS_UPDATED_CLEAN_PERSONAL_EXACT61_REFS_MIDTERM_COVER_CH3_UPDATED.docx"
)

S32_BULLETS = [
    "Ground truth observations (KKIA and corridors): Continuous observations from King Khalid International Airport comprise 12,582 hourly records, of which 200 are confirmed dust hours identified by official WMO present-weather codes (BLDU, HZ, DU, SA, SS, DS). The corridor stations Gassim (OEGS) and Rafha (OERF), together with KKIA, provide 37,510 synchronised multi-station observations.",
    "ECMWF ERA5 reanalysis: 12,408 consecutive hourly steps were extracted for the Riyadh station point and for a 4×4 spatial grid (24.0°N–25.5°N, 46.0°E–47.5°E). The 16 core physical variables include the 10 m wind components (u10, v10), 10 m gusts, wind kinetic energy (0.5·W10²), a friction-velocity proxy (u* ≈ 0.04·W10), 2 m temperature, dew point, relative humidity, surface pressure, top-layer soil moisture (0–7 cm), deep soil moisture (7–28 cm), and solar fluxes.",
    "GIS and topographic DEM: The NASA Shuttle Radar Topography Mission (SRTM) 90 m digital elevation model was extracted on a 21×21 grid (441 cells) covering Greater Riyadh and Jabal Tuwaiq. Derived layers include terrain slope vectors, aerodynamic surface roughness z₀, and the municipal boundary (1,913 km²).",
    "Operational NWP forecasts (CAMS and ECMWF IFS): ECMWF CAMS atmospheric-composition forecasts were extracted on a regional 43×56 grid (16°N–33°N, 34°E–56°E) at extended-range lead times of +72 h to +120 h in 6-hour steps (Days 3 to 5). Complementary ECMWF IFS high-resolution forecasts provide 240 consecutive hourly predictions (0 to 10 days).",
    "Satellite remote sensing: Columnar aerosol optical depth at 550 nm (AOD₅₅₀) from NASA MODIS (Terra/Aqua, MAIAC algorithm) and Sentinel-3 SLSTR, the Sentinel-5P TROPOMI UV Aerosol Index, and 12,408 hours of NASA POWER all-sky and clear-sky surface solar irradiance (ALLSKY_SFC_SW_DWN).",
]

TABLE_1_ROWS = [
    ["Data modality", "Storage path", "Primary file", "Format", "Size", "Records / dimension"],
    ["Ground truth (KKIA)", "data/raw/ground/", "riyadh_king_khalid_intl_airport_real.csv", "CSV", "2.58 MB", "12,582 hourly records (200 dust hrs)"],
    ["Ground corridor", "data/raw/ground/", "riyadh_ground_stations_master.csv", "CSV", "7.61 MB", "37,510 records (OERK, OEGS, OERF)"],
    ["ERA5 point time series", "data/raw/era5/", "era5_riyadh_hourly.nc", "NetCDF", "1.71 MB", "12,408 hours × 16 variables"],
    ["ERA5 spatial grid", "data/raw/era5/", "era5_riyadh_spatial_grid.nc", "NetCDF", "398 KB", "16 points (4×4) × 1,464 steps"],
    ["GIS DEM topography", "data/raw/gis/", "riyadh_dem_elevation_grid.nc", "NetCDF", "15 KB", "441 cells (21×21), 406 m–1,119 m"],
    ["GIS spatial boundary", "data/raw/gis/", "riyadh_boundary_and_stations.geojson", "GeoJSON", "3 KB", "City boundary, Tuwaiq, stations"],
    ["CAMS NWP station", "data/raw/nwp/", "cams_forecast_riyadh_station.csv", "CSV", "7 KB", "54 cycles (+72 h to +120 h lead)"],
    ["ECMWF IFS 10-day NWP", "data/raw/nwp/", "ecmwf_ifs_nwp_riyadh_forecast.csv", "CSV", "33 KB", "240 hourly steps (0 to 10 days)"],
    ["Regional CAMS NWP", "data/raw/nwp/", "cams_forecast_saudi_arabia.nc", "NetCDF", "1.58 MB", "43×56 grid, 9 lead times, 6 cycles"],
    ["Satellite AOD and dust", "data/raw/satellite/", "satellite_aod_dust_riyadh_hourly.nc", "NetCDF", "607 KB", "12,408 hours (MODIS/Sentinel-3/5P)"],
    ["Satellite solar flux", "data/raw/satellite/", "nasa_power_satellite_solar_radiation_riyadh.csv", "CSV", "355 KB", "12,408 hours NASA solar irradiance"],
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

    s32_p.text = "3.2 Sources of Data"
    s32_el = s32_p._element
    s33_el = s33_p._element

    siblings = list(body)
    i32 = siblings.index(s32_el)
    i33 = siblings.index(s33_el)
    for el in siblings[i32 + 1 : i33]:
        body.remove(el)

    add_para_before(
        s33_el,
        "Operational data pipelines were established for Riyadh and its inflow corridors, replacing earlier synthetic representations with authentic empirical data. All five data modalities required by the methodology were acquired, audited, and harmonised over the observation window.",
        "Normal",
        doc,
    )
    for b in S32_BULLETS:
        add_para_before(s33_el, b, "List Paragraph", doc)
    add_para_before(s33_el, "Table 1 summarises the complete dataset inventory.", "Normal", doc)
    add_para_before(s33_el, "Table 1: Comprehensive multi-modal dataset inventory for the Riyadh sandstorm forecasting platform", "Normal", doc)

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
        print(f"Updated 3.2 Sources of Data and Table 1 in {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name(DOC_PATH.stem + "_REV32.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
