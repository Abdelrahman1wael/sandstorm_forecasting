"""Update ONLY Section 3.4 (Feature Engineering and Input Representation) in
FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_LATEST_REV33_SYNCED.docx
to match 04_Notebooks/01_feature_engineering_and_impact.ipynb and scripts.
"""

from pathlib import Path
import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_LATEST_REV33_SYNCED.docx"
)
FIG_DIR = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting\07_Figures")


def add_para_before(anchor_el, text: str, style: str, doc: docx.Document, align=None):
    p = doc.add_paragraph(text, style=style)
    if align is not None:
        p.alignment = align
    el = p._element
    el.getparent().remove(el)
    anchor_el.addprevious(el)
    return p


def add_figure_before(anchor_el, img_path: Path, caption: str, doc: docx.Document, width_in: float = 5.8):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(str(img_path), width=Inches(width_in))
    el_img = p_img._element
    el_img.getparent().remove(el_img)
    anchor_el.addprevious(el_img)
    add_para_before(anchor_el, caption, "Normal", doc, align=WD_ALIGN_PARAGRAPH.CENTER)


def main() -> None:
    doc = docx.Document(str(DOC_PATH))
    body = doc._body._body

    s34_p = next(p for p in doc.paragraphs if p.style.name == "Heading 2" and p.text.strip().startswith("3.4"))
    s35_p = next(p for p in doc.paragraphs if p.style.name == "Heading 2" and p.text.strip().startswith("3.5"))

    s34_p.text = "3.4 Feature Engineering and Multimodal Input Representation"
    s34_el = s34_p._element
    s35_el = s35_p._element

    siblings = list(body)
    i34 = siblings.index(s34_el)
    i35 = siblings.index(s35_el)
    for el in siblings[i34 + 1 : i35]:
        body.remove(el)

    add_para_before(
        s35_el,
        "Building directly on the cleaned hourly stream in 04_Notebooks/01_feature_engineering_and_impact.ipynb and 08_Scripts/riyadh_common.py, this study constructs a 115-feature causal parameter space (stored in riyadh_hourly_clean_tvt.csv alongside 10 multi-horizon targets at 24 h, 72 h, 168 h, 216 h, and 360 h). Four anti-leakage and cleaning controls govern the pipeline: (i) dropping 100%-missing mslp and encoding wxcodes into has_wxcode and is_severe_dust_wx (SS/DS/SA); (ii) de-censoring the 53.7 μg/m³ visibility-cap floor into continuous pm10_clean_ugm3; (iii) defining an objective dust-event label clean_dust_event = (is_dust_event == 1) | (visibility_km < 5.0); and (iv) replacing drifting raw NWP/satellite columns with causal 180-day (4,320 h) rolling Z-scores clipped to [-5, 5], while dropping pre-existing target_* columns prior to recomputing clean future horizons.",
        "Normal",
        doc,
    )

    add_para_before(s35_el, "3.4.1 Four Causal Feature Groups (115 Predictors)", "Heading 3", doc)
    add_para_before(
        s35_el,
        "1. Ground & Co-Located Urban Meteorology: Surface observations at OERK (tmpc, dwpc, drct, sknt, gust, vsby, wind_speed_ms, wind_gust_ms, visibility_km, relative_humidity, has_wxcode, is_severe_dust_wx) paired with co-located OERY predictors (oery_visibility_km, oery_wind_speed_ms, oery_tmpc) and short-term lags (1 h, 3 h, 6 h, 12 h, 24 h) of PM₁₀, wind speed, and ERA5 u10.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        s35_el,
        "2. Dust Emission, Boundary-Layer & Synoptic Dynamics (ERA5): 26 ERA5 fields (10 m u10/v10, wind speed/direction/gusts, era5_wind_kinetic_energy, era5_friction_velocity_proxy, era5_blh_m, soil temperature 0–7 cm, topsoil and deep soil moisture 0–7 cm and 7–28 cm, solar radiation, FAO evapotranspiration, and 24 h/72 h/168 h rolling winds), 24 h and 72 h tendencies (sp_diff_24h, sp_diff_72h, t2m_diff_24h, ws_diff_24h), and physical emission proxies (phys_air_density_kgm3, phys_vpd_kpa, phys_saltation_emission_proxy, friction_velocity_excess, saltation_active_flag, dryness_wind_interaction, and aod_blh_ratio).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        s35_el,
        "3. Historical Sandstorm Memory & Multi-Scale Rolling Statistics: Causal 24 h, 72 h, and 168 h rolling means of pm10_clean_ugm3, wind speed/gusts, visibility, and VPD; 6 h/12 h/24 h rolling mean, max, and std of calibrated PM₁₀ and wind; plus long-memory dust persistence rates over 7 d (dust_rate_168h), 30 d (dust_rate_720h), and 180 d (dust_rate_4320h) alongside hours_since_dust.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        s35_el,
        "4. Calendar Harmonics, Satellite & Graph/Tensor Inputs: Cyclic seasonal and diurnal encodings (sin_doy, cos_doy, sin_hour, cos_hour), NASA POWER irradiance (all-sky, clear-sky, clearness index), sat_retrieved_pm2_5, sat_dust_column_mass, and causally detrended sat_retrieved_pm10_detrended_z, nwp_cams_pm10_detrended_z, and sat_aod_550nm_detrended_z. For Line B deep models, line_b_final_dataset.npz and riyadh_graph_adjacency_matrix.npy package 6×16×16 NWP grids, 3×32×32 satellite grids, 24×6×12 sequences, and the 6×6 regional spatial adjacency matrix.",
        "List Paragraph",
        doc,
    )

    add_para_before(s35_el, "3.4.2 Purge-Gapped Chronological Split, Train-Only Scaling, and Feature Impact", "Heading 3", doc)
    add_para_before(
        s35_el,
        "To prevent 15-day (360 h) target overlap across partition boundaries, Notebook 01 enforces a 360-hour purge gap between the 70% training set, 15% validation set, and 15% test set. Median imputation (SimpleImputer) and Yeo-Johnson power transformation (PowerTransformer) are fitted strictly on the 70% training split to suppress extreme feature skewness without distributional leakage (Figure 7). Train-only Mutual Information (24 h and 168 h) and 5-fold rolling-origin RidgeCV stability (Figure 8) verify predictor relevance before passing identical splits to Line A and Line B.",
        "Normal",
        doc,
    )
    add_figure_before(s35_el, FIG_DIR / "nb01_fig02.png", "Figure 7: Hourly feature |skewness| before vs. after train-only (70%) Yeo-Johnson transformation (01_feature_engineering_and_impact.ipynb).", doc)
    add_figure_before(s35_el, FIG_DIR / "nb01_fig03.png", "Figure 8: Train-only Mutual Information (168 h Avg PM₁₀) and 5-fold rolling-origin CV Ridge stability across engineered features.", doc)

    try:
        doc.save(str(DOC_PATH))
        print(f"Updated Section 3.4 in {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name(DOC_PATH.stem + "_REV34.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
