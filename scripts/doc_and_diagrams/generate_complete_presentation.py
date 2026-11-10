import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette: Executive Modern Deep Navy & Sand Desert Theme
    BG_DARK = RGBColor(11, 19, 43)        # #0B132B
    BG_CARD = RGBColor(23, 37, 84)        # #172554
    BG_CARD_LIGHT = RGBColor(30, 41, 59)  # #1E293B
    TEXT_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
    ACCENT_GOLD = RGBColor(245, 158, 11)  # #F59E0B (Sand/Gold)
    ACCENT_CYAN = RGBColor(56, 189, 248)  # #38BDF8 (Sky/Atmosphere)
    ACCENT_EMERALD = RGBColor(16, 185, 129) # #10B981 (Success/Verification)
    ACCENT_ROSE = RGBColor(244, 63, 94)   # #F43F5E (Alert/Hazard)
    BORDER_COLOR = RGBColor(51, 65, 85)   # #334155

    def add_bg(slide, dark=True):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK if dark else RGBColor(248, 250, 252)
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="DUSTML RESEARCH PLATFORM • RIYADH, SAUDI ARABIA"):
        # Category / Pill
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_GOLD
        p_cat.font.name = "Arial"

        # Main Slide Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(0.8))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT
        p_title.font.name = "Arial"

        # Accent Rule Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.03))
        line.fill.solid()
        line.fill.fore_color.rgb = ACCENT_CYAN
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg_rgb=BG_CARD_LIGHT, border_rgb=BORDER_COLOR):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_rgb
        card.line.color.rgb = border_rgb
        card.line.width = Pt(1.2)
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    # Decorative accent banner
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.0), Inches(0.15), Inches(5.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_GOLD
    bar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(11.0), Inches(5.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    p0.font.size = Pt(24)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_GOLD
    p0.alignment = PP_ALIGN.LEFT

    p1 = tf.add_paragraph()
    p1.text = "Applying Machine Learning & Physics-Informed Deep Spatiotemporal Models"
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.text = "To Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm (SDS) Forecasting in Riyadh Region"
    p2.font.size = Pt(18)
    p2.font.color.rgb = ACCENT_CYAN

    p3 = tf.add_paragraph()
    p3.text = "\nCandidate: ALGHAMDI, HUDA 语嫣"
    p3.font.size = Pt(15)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_LIGHT

    p4 = tf.add_paragraph()
    p4.text = "Research Platform: DustML Multi-Modal Atmospheric Data Lab  |  Target Domain: Riyadh & Connected Deserts, KSA"
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEXT_MUTED

    p5 = tf.add_paragraph()
    p5.text = "Core Dual-Line Paradigm: Main Line A (Statistical ML / Tree Ensembles NWP Debiasing) & Main Line B (ST-GNN + Transformer + PINN)"
    p5.font.size = Pt(12)
    p5.font.bold = True
    p5.font.color.rgb = ACCENT_EMERALD

    # ==========================================
    # SLIDE 2: RESEARCH MOTIVATION & PROBLEM STATEMENT
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Research Motivation: The Medium- to Long-Term Forecasting Challenge", "CHAPTER 1: INTRODUCTION & CONTEXT")

    c1 = add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0))
    tb1 = s2.shapes.add_textbox(Inches(0.9), Inches(1.9), Inches(3.4), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "🌪️ Atmospheric Vulnerability"
    tf1.paragraphs[0].font.size = Pt(16)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_GOLD
    pts1 = [
        "• Riyadh is located in the hyper-arid Najd plateau (600m ASL), encircled by major desert dune complexes.",
        "• Recurrent Sand and Dust Storms (SDS) collapse horizontal visibility below 500m.",
        "• Sudden Haboobs driven by convective downdrafts trigger dangerous acute respiratory episodes and traffic crises.",
        "• Major events (e.g. 2015, 2021, 2022, 2025) demonstrate regional systemic exposure."
    ]
    for pt in pts1:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT

    c2 = add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0))
    tb2 = s2.shapes.add_textbox(Inches(4.9), Inches(1.9), Inches(3.4), Inches(4.8))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.paragraphs[0].text = "⚠️ The 72-Hour NWP Barrier"
    tf2.paragraphs[0].font.size = Pt(16)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = ACCENT_ROSE
    pts2 = [
        "• Numerical Weather Prediction (CAMS, ECMWF IFS) degrades exponentially beyond 72 hours (+72h to +120h).",
        "• Coarse grid resolution (~12km) smooths out the 800m Tuwayq mountain ridge.",
        "• Idealized roughness lengths (z0) fail to model shifting barchan dunes.",
        "• Chemical aerosol transport ceases beyond day 5, leaving 6-15 day horizons without reliable dust guidance."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT

    c3 = add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0))
    tb3 = s2.shapes.add_textbox(Inches(8.9), Inches(1.9), Inches(3.5), Inches(4.8))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.paragraphs[0].text = "🚀 The Dual-Line Solution"
    tf3.paragraphs[0].font.size = Pt(16)
    tf3.paragraphs[0].font.bold = True
    tf3.paragraphs[0].font.color.rgb = ACCENT_EMERALD
    pts3 = [
        "• Main Line A: Statistical Tree Ensembles (LightGBM, XGBoost, CatBoost, RF) for NWP residual debiasing up to 120h.",
        "• The ML Drift Bottleneck: Why classical ML degrades at medium-to-long ranges due to recursive feature drift.",
        "• Main Line B: End-to-End Deep Spatiotemporal Models (ST-GNN + Transformer + Bi-LSTM + PINN) for 3-15 days.",
        "• Explainable AI (SHAP) & Rigorous WMO Categorical Validation (CSI ≥ 0.60)."
    ]
    for pt in pts3:
        p = tf3.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 3: RIYADH GEOGRAPHY & CLIMATOLOGY
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Geographic Setting: Riyadh Metropolitan & Atmospheric Exposure", "CHAPTER 1: INTRODUCTION & CONTEXT")

    c1 = add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb1 = s3.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "Metropolitan Receptor Characteristics"
    tf1.paragraphs[0].font.size = Pt(16)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_CYAN
    pts1 = [
        "• Geographic Coordinates: 24.71° N, 46.67° E | Altitude: ~600 m above sea level.",
        "• Total Administrative Area: 380,000 km² across Riyadh Province.",
        "• Demographics: 7.01+ Million inhabitants (2022 Census), 20 sub-municipalities across 6 sectors.",
        "• Economic Significance: Contributes 47% of the Kingdom's non-oil, non-governmental GDP.",
        "• Critical Transport Hub: King Khalid International Airport (KKIA - OERK) and King Salman Park megaproject.",
        "• Climate Regime: Hyper-arid continental desert, extreme summer temperatures (>48°C), low rainfall (<100mm/yr)."
    ]
    for pt in pts1:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT

    c2 = add_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb2 = s3.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.paragraphs[0].text = "Socioeconomic & Public Health Impact"
    tf2.paragraphs[0].font.size = Pt(16)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = ACCENT_GOLD
    pts2 = [
        "• Aviation Disruption: The April 2015 storm forced diversion/cancellation of over 1,000 flights in Saudi Arabia over 3 days.",
        "• Highway Safety: Dense particulate clouds trigger multi-vehicle pileups (e.g., 354 accidents in a single documented day).",
        "• Renewable Energy Losses: Fine desert dust coats solar PV installations, dropping power yield by 30-50% in hours.",
        "• Healthcare Burden: Massive spikes in ER pediatric admissions for asthma, bronchitis, and cardiovascular stress.",
        "• Regional Welfare Cost: World Bank estimates regional annual costs of SDS exceed US$150 Billion.",
        "• Vision 2030 Mandate: Early warning systems are crucial for the Saudi Green Initiative and Quality of Life Program."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 4: CONNECTED DESERTS & SOURCE CORRIDORS
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "The 5 Connected Desert Inflow Corridors Driving Riyadh Dust", "CHAPTER 1: INTRODUCTION & CONTEXT")

    corridors = [
        ("1. Al-Thumamah Dunes", "50 km (E/NE)", "Immediate active red sand dunes; responds rapidly to wind gusts >= 7 m/s, causing sudden local visibility collapse in < 1h."),
        ("2. Ad-Dahna Desert", "120 km (NE)", "1,000-km sand sea conveyor connecting Nafud to Rub' al-Khali; funnels iron-rich barchan dust under easterly/Shamal wind vectors."),
        ("3. Nafud al-Thuwairat", "220 km (NW)", "Major deflation basin down the Zulfi-Majmaah corridor; northwesterly Shamal winds mobilize massive fronts straight into Riyadh."),
        ("4. Tuwayq Escarpment", "180 km (SW)", "800-km steep limestone ridge; aerodynamic bluff causing slope vorticity, thermal channeling, and downdraft Haboobs."),
        ("5. Rub' al-Khali (Empty Qtr)", "350 km (SE)", "Hyper-arid regional sand sea; deep thermal lows propel massive regional AOD plumes across southern corridors into Riyadh.")
    ]

    for idx, (name, dist, desc) in enumerate(corridors):
        top_pos = Inches(1.8 + idx * 1.0)
        card = add_card(s4, Inches(0.8), top_pos, Inches(11.733), Inches(0.85))
        tb = s4.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.05), Inches(11.3), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = f"{name}  |  Distance: {dist}"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_GOLD
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(11)
        p1.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 5: HISTORICAL SANDSTORM CLIMATOLOGY (2016-2026)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Decadal History of Major Sandstorm Events in Riyadh (2016–2026)", "CHAPTER 1: CLIMATOLOGY & HISTORICAL EVIDENCE")

    events = [
        ("2016 - 2017", "20 March 2017", "Major regional dust outbreak; Aerosol Optical Depth (AOD) reached ~2.3 over Riyadh.", "Severe Alert"),
        ("2018", "23-24 April 2018", "Spring outbreak affecting Riyadh & Eastern Province; 276 dust events recorded across KSA.", "High Impact"),
        ("2021", "15 April 2021", "Regional synoptic front across Central and Southwestern Saudi Arabia; widespread ground closure.", "Corridor Event"),
        ("2022", "4 March & 17 May 2022", "Massive orange dust blanket engulfed Riyadh skyline; visibility plummeted to < 300 meters.", "Extreme Haboob"),
        ("2023 - 2024", "Spring 2023 / 2024", "44-47 distinct dust episodes monitored across provincial receptor network.", "Observational"),
        ("2025 - 2026", "6 Feb & 11 Apr 2025", "Extreme storm with AOD reaching 2.76, visibility ~0.5 km; followed by historic June low in 2026.", "Validation Target")
    ]

    for idx, (yr, dt, detail, tag) in enumerate(events):
        top_pos = Inches(1.8 + idx * 0.85)
        c = add_card(s5, Inches(0.8), top_pos, Inches(11.733), Inches(0.72))
        tb = s5.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.04), Inches(11.3), Inches(0.65))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = f"[{yr}]  {dt}  —  {tag}"
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN if "Extreme" not in tag else ACCENT_ROSE
        p1 = tf.add_paragraph()
        p1.text = detail
        p1.font.size = Pt(11)
        p1.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 6: TAXONOMY & SITEMAP OF FORECASTING PARADIGMS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Methodological Taxonomy Sitemap: 5 Research Branches", "CHAPTER 2: SITEMAP & THEORETICAL FOUNDATION")

    tax_branches = [
        ("Branch 1: Traditional Methods", "Physics & Statistics", [
            "• Subjective synoptic chart analysis",
            "• Classical AR / ARIMA time-series",
            "• Dynamical NWP (GFS, WRF, CAMS)",
            "• Operational early warnings"
        ], ACCENT_GOLD),
        ("Branch 2: Multi-Scale Dynamics", "Spatiotemporal Physics", [
            "• Microscale Haboob downdrafts",
            "• Mesoscale Shamal wind fronts",
            "• Synoptic cold pool advection",
            "• Topographic barrier channeling"
        ], ACCENT_CYAN),
        ("Branch 3: Machine Learning", "Linear & Statistical ML", [
            "• Linear & Ridge / Lasso regression",
            "• Tree Ensembles (RF, XGBoost, GBDT)",
            "• NWP Bias Correction (Line A)",
            "• Quantile Regression Envelopes"
        ], ACCENT_EMERALD),
        ("Branch 4: Deep Learning", "Nonlinear Spatiotemporal", [
            "• Bi-LSTM sequence foundations",
            "• Spatial-Temporal Transformers (TFT)",
            "• ST-GNN Corridor Graph Networks",
            "• Physics-Informed PINN Losses"
        ], RGBColor(168, 85, 247)),
        ("Branch 5: Integrated Impact", "Tri-Pillar Applications", [
            "• Ground-satellite multimodal fusion",
            "• GIS hazard risk mapping",
            "• Hospital ER & Aviation alerts",
            "• Saudi Vision 2030 early warning"
        ], ACCENT_ROSE)
    ]

    for idx, (b_title, b_sub, b_items, b_color) in enumerate(tax_branches):
        left_pos = Inches(0.8 + idx * 2.4)
        c = add_card(s6, left_pos, Inches(1.8), Inches(2.25), Inches(5.0), BG_CARD_LIGHT, b_color)
        tb = s6.shapes.add_textbox(left_pos + Inches(0.1), Inches(1.9), Inches(2.05), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = b_title
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = b_color
        p1 = tf.add_paragraph()
        p1.text = b_sub
        p1.font.size = Pt(10)
        p1.font.color.rgb = TEXT_MUTED
        for itm in b_items:
            p = tf.add_paragraph()
            p.text = itm
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 7: END-TO-END PIPELINE ARCHITECTURE
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Complete End-to-End System Architecture: The Dual-Line Paradigm", "CHAPTER 3: SYSTEM ARCHITECTURE")

    pipeline_stages = [
        ("STAGE 1: INGESTION", "5 Raw Modalities", [
            "• Ground In-Situ (6 Stations)",
            "• ECMWF ERA5 Reanalysis",
            "• CAMS/IFS Operational NWP",
            "• NASA MODIS/AERONET AOD",
            "• SRTM 90m GIS Topography"
        ]),
        ("STAGE 2: PREPROCESSING", "Data Hygiene & QC", [
            "• Strict UTC Reindexing (1h)",
            "• Sensor Despiking (MAD)",
            "• Bounds Clamping [0.05, 30km]",
            "• Akima Spline Imputation",
            "• Multimodal 1-to-1 Time Join"
        ]),
        ("STAGE 3: PHYSICS ENGINE", "Engineered Predictors", [
            "• Wind Vector (u10, v10, Ek)",
            "• Owen Saltation Flux (Q)",
            "• Vapor Pressure Deficit (VPD)",
            "• Dry Air Density (rho)",
            "• Backward Non-Leakage Lags"
        ]),
        ("STAGE 4: DUAL MODELING", "Line A & Line B", [
            "• Line A: Tree Ensembles (RF, XGBoost, LightGBM) for NWP Debiasing (72-120h)",
            "• Line B: Deep ST-GNN + TFT + Bi-LSTM + PINN for 3-15 Days"
        ]),
        ("STAGE 5: DECISION SUPPORT", "XAI & Warnings", [
            "• TreeSHAP & DeepSHAP XAI",
            "• P10/P50/P90 Uncertainty",
            "• 5-Tier Hazard Tiers",
            "• Real-time Aviation & City Alert"
        ])
    ]

    for idx, (st_title, st_sub, st_bullets) in enumerate(pipeline_stages):
        left_pos = Inches(0.8 + idx * 2.4)
        c = add_card(s7, left_pos, Inches(1.8), Inches(2.25), Inches(5.0))
        tb = s7.shapes.add_textbox(left_pos + Inches(0.1), Inches(1.9), Inches(2.05), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = st_title
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_GOLD
        p1 = tf.add_paragraph()
        p1.text = st_sub
        p1.font.size = Pt(10)
        p1.font.color.rgb = ACCENT_CYAN
        for b in st_bullets:
            p = tf.add_paragraph()
            p.text = b
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 8: TOOLS & SOFTWARE ECOSYSTEM
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Tools & Software Ecosystem: Data Engineering to Deep Learning", "CHAPTER 3: TOOLS & COMPUTATIONAL STACK")

    tool_boxes = [
        ("Data Extraction & APIs", ACCENT_GOLD, [
            "• cdsapi: ECMWF Copernicus Climate Data Store API",
            "• Copernicus ADS API: CAMS atmospheric forecasts",
            "• NASA earthaccess: MODIS AOD & SMAP soil data",
            "• requests & urllib3: Quotsoft / NOAA automated feeds",
            "• Keys/API_Key: Secured credential management"
        ]),
        ("Meteorology & GIS Processing", ACCENT_CYAN, [
            "• CDO (Climate Data Operators): NetCDF/GRIB manipulation",
            "• xarray & netCDF4: High-dimensional climate arrays",
            "• GDAL & rasterio: SRTM 90m DEM terrain & slope",
            "• geopandas & shapely: GeoJSON desert polygons",
            "• pandas & numpy: Vectorized tabular transformations"
        ]),
        ("Classical ML (Line A)", ACCENT_EMERALD, [
            "• LightGBM: Gradient boosting with GOSS & EFB",
            "• XGBoost: Extreme gradient boosting tree ensembles",
            "• CatBoost: Categorical corridor handling without leakage",
            "• scikit-learn: Random Forest, Ridge, pipelines & metrics",
            "• Optuna: Bayesian hyperparameter tuning"
        ]),
        ("Deep Learning & XAI (Line B)", RGBColor(168, 85, 247), [
            "• PyTorch 2.2+: GPU CUDA-accelerated deep tensor learning",
            "• PyTorch Geometric: Dynamic Spatiotemporal Graph (ST-GNN)",
            "• TFT (Temporal Fusion Transformer): Self-attention & VSN",
            "• Earthformer / ConvLSTM: 2D spatiotemporal plume vision",
            "• SHAP: TreeSHAP & DeepSHAP physical interpretability"
        ])
    ]

    for idx, (title, color, items) in enumerate(tool_boxes):
        col = idx % 2
        row = idx // 2
        left_pos = Inches(0.8 + col * 6.0)
        top_pos = Inches(1.8 + row * 2.6)
        c = add_card(s8, left_pos, top_pos, Inches(5.7), Inches(2.4), BG_CARD_LIGHT, color)
        tb = s8.shapes.add_textbox(left_pos + Inches(0.15), top_pos + Inches(0.1), Inches(5.4), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = color
        for itm in items:
            p = tf.add_paragraph()
            p.text = itm
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 9: DATA TYPES, SHAPES & PROVENANCE
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Multi-Modal Scientific Data: Dimensions, Shapes & Provenance Links", "CHAPTER 4: DATA ARCHITECTURE")

    data_rows = [
        ("1. Ground In-Situ Truth", "6 Stations (OERK, OERY, OEPS, OEDM, OEWD, OEGS)", "216,174 rows x 14 cols [2020-2024]", "Quotsoft / CNEMC & NOAA ISD", "data/raw/ground/"),
        ("2. ECMWF ERA5 Reanalysis", "6 Spatial Domains (Riyadh + 5 Deserts)", "43,848 hrs x 6 x 8 channels (3D/2D)", "Copernicus CDS (cds.climate.copernicus.eu)", "data/raw/era5/"),
        ("3. CAMS / IFS NWP", "Point & Grid Forecasts (+72h to +120h)", "54 Cycles x 17 Leadtimes x 6 Nodes", "Copernicus ADS (ads.atmosphere.copernicus.eu)", "data/raw/nwp/"),
        ("4. ECMWF TIGGE Forecasts", "Medium-to-Extended Ensemble (144h - 360h)", "15 Days x 6-hourly x 51 Members", "ECMWF TIGGE (apps.ecmwf.int/datasets/tigge)", "data/raw/nwp/"),
        ("5. Satellite Remote Sensing", "MODIS Terra/Aqua AOD & Sentinel-3", "43,848 Hourly column retrievals", "NASA Earthdata & AERONET Solar Village", "data/raw/satellite/"),
        ("6. SRTM DEM Topography", "Elevation, Slope, Aerodynamic Roughness", "21 x 21 Raster Grid (614m - 1119m)", "CGIAR-CSI SRTM / USGS Earth Explorer", "data/raw/gis/")
    ]

    for idx, (mod, cov, shp, src, loc) in enumerate(data_rows):
        top_pos = Inches(1.8 + idx * 0.85)
        c = add_card(s9, Inches(0.8), top_pos, Inches(11.733), Inches(0.75))
        tb = s9.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.05), Inches(11.3), Inches(0.68))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = f"{mod}  |  Shape: {shp}"
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_GOLD
        p1 = tf.add_paragraph()
        p1.text = f"Coverage: {cov}  •  Source Link: {src}  •  Path: {loc}"
        p1.font.size = Pt(10)
        p1.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 10: PREPROCESSING PROTOCOL
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Data Preprocessing Protocol: Hygiene, QC & Zero Leakage", "CHAPTER 5: DATA PREPROCESSING & MERGING")

    steps = [
        ("Step 1: Strict UTC Alignment", [
            "• Eliminate AST (UTC+3) offset errors.",
            "• Snap irregular METAR (:20, :50) to exact hourly timestamps.",
            "• Construct unbroken 43,800-hour datetime index (2020-2024)."
        ]),
        ("Step 2: QC & Bound Clamping", [
            "• Visibility clamped: clip(V, 0.05, 30.0 km).",
            "• Relative Humidity clamped: clip(RH, 1.0, 100.0 %).",
            "• Physical consistency: Wind Gust >= Wind Speed."
        ]),
        ("Step 3: Despiking & Flatline Detection", [
            "• Rolling Median Absolute Deviation (MAD): Cutoff at 4.5 x MAD.",
            "• Discard electronic sensor glitches while preserving real storm surges.",
            "• Zero-variance filter flags mechanical sensor freeze (>= 12h)."
        ]),
        ("Step 4: Missing Data Imputation", [
            "• Short gaps (<= 3h): Akima cubic spline preserves diurnal curves.",
            "• Medium gaps (3h - 24h): Spatial corridor regression from upwind station.",
            "• Zero listwise deletion: complete feature matrix maintained."
        ])
    ]

    for idx, (st_name, st_pts) in enumerate(steps):
        col = idx % 2
        row = idx // 2
        left_pos = Inches(0.8 + col * 6.0)
        top_pos = Inches(1.8 + row * 2.6)
        c = add_card(s10, left_pos, top_pos, Inches(5.7), Inches(2.4))
        tb = s10.shapes.add_textbox(left_pos + Inches(0.15), top_pos + Inches(0.1), Inches(5.4), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = st_name
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN
        for pt in st_pts:
            p = tf.add_paragraph()
            p.text = pt
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 11: PHYSICS-INFORMED FEATURE DERIVATION
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Physics-Informed Feature Engineering: Deriving Boundary Physics", "CHAPTER 5: DATA PREPROCESSING & MERGING")

    formulas = [
        ("1. Aerodynamic Wind Decomposition & Kinetic Energy",
         "u10 = -W10 * sin(drct),   v10 = -W10 * cos(drct),   Ek = 0.5 * W10^2",
         "Eliminates circular angular discontinuity (360°/0°) and captures kinetic energy available for sand deflation."),
        ("2. Owen (1964) Desert Saltation Sand Emission Flux",
         "Q ~ u_*^3 * max(0, 1 - (u_*t / u_*)^2) * exp(-15 * SM_top)",
         "Sand particles lift only when friction velocity u_* exceeds threshold u_*t (~0.28 m/s); exponentially suppressed by topsoil moisture."),
        ("3. Atmospheric Vapor Pressure Deficit (VPD)",
         "es = 0.61078 * exp(17.27 * T / (T + 237.3)),   ea = es * (RH/100),   VPD = max(0, es - ea)",
         "Measures atmospheric drying suction. High VPD combined with desert wind triggers instantaneous surface soil crumbling."),
        ("4. Harmonic Astronomical Coordinates (Cyclic Time)",
         "sin_DOY = sin(2*pi*DOY / 365.25),   cos_DOY = cos(2*pi*DOY / 365.25),   sin_Hour = sin(2*pi*H / 24)",
         "Transforms calendar dates into smooth cyclical waves, preventing false artificial jumps between Dec 31 and Jan 1.")
    ]

    for idx, (title, math_expr, desc) in enumerate(formulas):
        top_pos = Inches(1.8 + idx * 1.25)
        c = add_card(s11, Inches(0.8), top_pos, Inches(11.733), Inches(1.15))
        tb = s11.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.05), Inches(11.3), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_GOLD
        p1 = tf.add_paragraph()
        p1.text = f"Formula: {math_expr}"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = ACCENT_CYAN
        p2 = tf.add_paragraph()
        p2.text = f"Physical Role: {desc}"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 12: MULTIMODAL MERGING & LAG ENGINE
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "Multi-Modal Merging Logic & Anti-Leakage Feature Store", "CHAPTER 5: DATA PREPROCESSING & MERGING")

    c1 = add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb1 = s12.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "🔗 1-to-1 Multi-Stream Temporal Join"
    tf1.paragraphs[0].font.size = Pt(15)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_EMERALD
    pts1 = [
        "• Inner Join: Ground telemetry (OERK + corridors) and ECMWF ERA5 synced on UTC hourly key.",
        "• Left Join: Satellite AOD, column dust mass, and NASA solar radiation.",
        "• Spatial Nearest-Neighbor: Attach SRTM DEM elevation (614m), slope (1.85°), and roughness z0 (0.042m) to receptor.",
        "• Forward/Backward Fill: Handle boundary gaps without breaking chronological order.",
        "• Master Output: data/processed/riyadh_multimodal_engineered_dataset.parquet (43,800 rows x 55+ features)."
    ]
    for pt in pts1:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    c2 = add_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb2 = s12.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.paragraphs[0].text = "🛡️ Strict Anti-Leakage Lag Engine"
    tf2.paragraphs[0].font.size = Pt(15)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = ACCENT_GOLD
    pts2 = [
        "• Multi-Horizon Backward Lags: t-1h, t-3h, t-6h, t-12h, t-24h for PM10, wind speed, gusts, and visibility.",
        "• Rolling Aggregations: Closed on left ('closed=left') to guarantee zero future data leaks into model predictors.",
        "• Upwind Corridor Projections: Wind alignment factors computed for each of the 5 connected desert directions.",
        "• Dual Export Formatting:",
        "  - Format A (Line A): 2D Tabular Feature Matrix for GBDT Tree Ensembles.",
        "  - Format B (Line B): 5D Spatiotemporal Tensors [B, C, T, H, W] and Dynamic Graph Adjacency Matrix A(t)."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 13: LINE A - STATISTICAL ML & TREE ENSEMBLES
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13)
    add_header(s13, "Main Line A: Statistical Tree Ensembles & Ensembling Algorithms", "CHAPTER 6: MAIN LINE A MODELING")

    models = [
        ("Random Forest (RF)", "Bagging Ensemble", [
            "• Aggregates hundreds of de-correlated decision trees.",
            "• High stability, prevents extreme outlier over-fitting.",
            "• Baseline non-linear feature importance benchmark."
        ], ACCENT_GOLD),
        ("XGBoost", "Exact Greedy Boosting", [
            "• Second-order Taylor expansion loss optimization.",
            "• Strong L1/L2 regularization on leaf weights to avoid overfitting.",
            "• Highly sensitive to sudden wind gust spikes."
        ], ACCENT_CYAN),
        ("LightGBM", "Histogram & GOSS", [
            "• Gradient-based One-Side Sampling (GOSS) speeds up large datasets.",
            "• Exclusive Feature Bundling (EFB) compresses sparse indicators.",
            "• Native support for Quantile Loss (P10, P50, P90)."
        ], ACCENT_EMERALD),
        ("CatBoost", "Ordered Boosting", [
            "• Solves target leakage in categorical corridor features.",
            "• Symmetric oblivious trees ensure rapid inference execution.",
            "• Robust against noisy desert weather station measurements."
        ], RGBColor(168, 85, 247))
    ]

    for idx, (m_name, m_type, m_desc, m_color) in enumerate(models):
        left_pos = Inches(0.8 + idx * 2.95)
        c = add_card(s13, left_pos, Inches(1.8), Inches(2.8), Inches(5.0), BG_CARD_LIGHT, m_color)
        tb = s13.shapes.add_textbox(left_pos + Inches(0.1), Inches(1.9), Inches(2.6), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = m_name
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = m_color
        p1 = tf.add_paragraph()
        p1.text = m_type
        p1.font.size = Pt(11)
        p1.font.color.rgb = TEXT_MUTED
        for d in m_desc:
            p = tf.add_paragraph()
            p.text = d
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 14: LINE A - NWP BIAS CORRECTION & 72H ERROR
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_bg(s14)
    add_header(s14, "Line A NWP Bias Correction & The 72-120h Error Origin", "CHAPTER 6: MAIN LINE A MODELING")

    c1 = add_card(s14, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb1 = s14.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "Why Basic NWP Produces Severe Errors (~72h)"
    tf1.paragraphs[0].font.size = Pt(15)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_ROSE
    pts1 = [
        "1. Coarse Spatial Grid (~12-25 km): NWP models smooth steep topography, completely missing the 800m Tuwayq ridge slope acceleration.",
        "2. Static Aerodynamic Roughness: Idealized z0 fails across shifting barchan dunes (Ad-Dahna and Nafud).",
        "3. Missed Haboob Downdrafts: Convective thunderstorm cold pools and microscale Haboobs fall below numerical grid cell resolution.",
        "4. Chaotic Butterfly Effect: Atmospheric non-linearities compound exponentially beyond 72 hours (+72h to +120h).",
        "5. Chemical Aerosol Cutoff: Operational NWP models output no chemical dust transport beyond 120 hours (Day 5)."
    ]
    for pt in pts1:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    c2 = add_card(s14, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb2 = s14.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.paragraphs[0].text = "Line A Residual Formulation & Projected Outcomes"
    tf2.paragraphs[0].font.size = Pt(15)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = ACCENT_EMERALD
    pts2 = [
        "• Residual Target Formulation:",
        "  Δy(t + τ) = y_obs(t + τ) - y_NWP(t + τ)",
        "• Calibrated Prediction:",
        "  y_hat(t + τ) = y_NWP(t + τ) + f_GBDT(X_ground, X_ERA5, X_desert, X_GIS)",
        "• Quantile Loss Optimization: Pinball loss at α in {0.10, 0.50, 0.90} outputs probabilistic hazard bounds [P10, P90].",
        "• 5-Tier Hazard Classification: Normal (<50), Moderate (50-150), Elevated (150-300), Severe Sandstorm (300-600), Extreme Haboob (>600 µg/m³).",
        "• Target Accuracy: Drops raw NWP RMSE by ΔRMSE >= 25%."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 15: LIMITATIONS OF CLASSICAL ML AT MEDIUM/LONG RANGES
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_bg(s15)
    add_header(s15, "Why Classical ML Drifts & Gives Inaccurate Long-Term Results", "CHAPTER 6: THE CRITICAL TURNING POINT")

    c1 = add_card(s15, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb1 = s15.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "⚠️ The ML Drift & Error Accumulation Barrier"
    tf1.paragraphs[0].font.size = Pt(15)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_ROSE
    pts1 = [
        "• Autoregressive Error Compounding: When forecasting beyond 72-120h, tabular models must feed predicted outputs back into future lags. Errors explode recursively.",
        "• Flat Tabular Blindness: Tree ensembles treat each row as independent feature vectors, unable to preserve continuous fluid wave continuity.",
        "• Loss of NWP Physical Anchor: Since NWP stops providing dust chemistry beyond Day 5, Line A loses its baseline reference, causing tree models to regress toward the training mean.",
        "• Extreme Peak Flattening: Even with hyperparameter fine-tuning, GBDTs severely underestimate the magnitude of sudden severe Haboobs at long lead times."
    ]
    for pt in pts1:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    c2 = add_card(s15, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb2 = s15.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.paragraphs[0].text = "💡 The Imperative to Invest in Main Line B"
    tf2.paragraphs[0].font.size = Pt(15)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = ACCENT_GOLD
    pts2 = [
        "• We MUST move beyond flat tabular models to handle continuous spatiotemporal physical propagation.",
        "• Line B leverages rich multi-station networks and 2D satellite/reanalysis image grids.",
        "• Instead of treating stations independently, Line B models dust advection along geographic corridor graphs.",
        "• Deep architectures (LSTM, Transformers, ST-GNN) retain multi-day memory without autoregressive breakdown.",
        "• Physics-Informed constraints (PINN) ensure predictions strictly obey mass conservation and aerodynamic laws."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 16: LINE B - DEEP SPATIOTEMPORAL ARCHITECTURE
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    add_bg(s16)
    add_header(s16, "Main Line B: End-to-End Deep Spatiotemporal Architecture", "CHAPTER 7: MAIN LINE B DEEP LEARNING")

    line_b_tracks = [
        ("Track B1: Temporal Foundation", "Bi-LSTM & Diurnal Dynamics", [
            "• Bidirectional LSTM captures past 72h historical sequences.",
            "• Encodes diurnal solar heating cycles & night-time boundary layer collapse.",
            "• Retains long-term temporal dependencies without exponential degradation."
        ], ACCENT_GOLD),
        ("Track B2: Spatial-Temporal Transformers", "TFT & Earthformer", [
            "• Temporal Fusion Transformer (TFT) with self-attention.",
            "• Gated Residual Networks (GRN) filter calm non-dust noise.",
            "• Variable Selection Networks (VSN) identify which desert corridor governs current outbreak."
        ], ACCENT_CYAN),
        ("Track B3: Corridor Graph Networks", "Dynamic ST-GNN", [
            "• Models 6 ground stations + 5 deserts as a directed spatial graph G = (V, E, A(t)).",
            "• Chebyshev spectral graph convolutions track advection along active wind directions.",
            "• Captures real-time transport from Gassim/Dahna into Riyadh."
        ], ACCENT_EMERALD),
        ("Track B4: Physics-Informed PINN", "Governing Atmospheric Laws", [
            "• Enforces Owen friction threshold: zero dust if u_* < u_*t.",
            "• PDE Advection continuity constraint enforces aerosol mass conservation.",
            "• Strictly guarantees non-negative particulate concentrations."
        ], RGBColor(168, 85, 247))
    ]

    for idx, (t_name, t_sub, t_items, t_color) in enumerate(line_b_tracks):
        left_pos = Inches(0.8 + idx * 2.95)
        c = add_card(s16, left_pos, Inches(1.8), Inches(2.8), Inches(5.0), BG_CARD_LIGHT, t_color)
        tb = s16.shapes.add_textbox(left_pos + Inches(0.1), Inches(1.9), Inches(2.6), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = t_name
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = t_color
        p1 = tf.add_paragraph()
        p1.text = t_sub
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = TEXT_MUTED
        for itm in t_items:
            p = tf.add_paragraph()
            p.text = itm
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 17: LINE B - DYNAMIC ST-GNN CORRIDOR GRAPH
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    add_bg(s17)
    add_header(s17, "Line B ST-GNN: Dynamic Wind-Advection Corridor Graph", "CHAPTER 7: MAIN LINE B DEEP LEARNING")

    c1 = add_card(s17, Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.0))
    tb1 = s17.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.6), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "Dynamic Spatial Adjacency Matrix Formulation"
    tf1.paragraphs[0].font.size = Pt(15)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_CYAN
    pts1 = [
        "• Network Nodes (V = 6 Stations): OERK (Riyadh Airport), OERY (Air Base), OEPS (Al-Kharj), OEDM (Ad-Duwadimi), OEWD (Wadi Al-Dawasir), OEGS (Gassim).",
        "• Dynamic Edge Weight Formula:",
        "  A_ij(t) = exp(-d_ij / D0) * [1 + max(0, cos(theta_wind^i(t) - phi_ij)) * (u_10 / 15.0)]",
        "• Physical Meaning: When prevailing wind aligns with the geographical bearing phi_ij from Gassim to Riyadh, the edge weight surges dynamically, transferring upstream dust plume representations.",
        "• Laplacian Normalization: D^(-1/2) * A * D^(-1/2) ensures numerical gradient stability during backpropagation."
    ]
    for pt in pts1:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    c2 = add_card(s17, Inches(7.2), Inches(1.8), Inches(5.3), Inches(5.0))
    tb2 = s17.shapes.add_textbox(Inches(7.4), Inches(2.0), Inches(4.9), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.paragraphs[0].text = "Corridor Message-Passing Advantages"
    tf2.paragraphs[0].font.size = Pt(15)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = ACCENT_EMERALD
    pts2 = [
        "1. Direct Physics Replication: Mimics real atmospheric dust advection across hundreds of kilometers.",
        "2. Upstream Warning Lead-Time: Detects deflation surges in Gassim or Nafud 6 to 12 hours before dust hits Riyadh KKIA.",
        "3. Topographic Attenuation: Incorporates Tuwayq escarpment barrier impedance along western edges.",
        "4. Extended Horizon Resilience: ST-GNN does not suffer from tabular recursive drift, enabling robust 3-15 day trajectories."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 18: PINN - PHYSICS-INFORMED LOSS CONSTRAINTS
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    add_bg(s18)
    add_header(s18, "Physics-Informed Neural Networks (PINN): Enforcing Atmospheric Laws", "CHAPTER 7: MAIN LINE B DEEP LEARNING")

    c1 = add_card(s18, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.5))
    tb1 = s18.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.3), Inches(1.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "Unified Physics-Informed Loss Function"
    tf1.paragraphs[0].font.size = Pt(15)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_GOLD
    p_eq = tf1.add_paragraph()
    p_eq.text = "L_total = L_Data (Huber/Quantile) + λ1 * L_Saltation + λ2 * L_Continuity + λ3 * L_NonNegative"
    p_eq.font.size = Pt(14)
    p_eq.font.bold = True
    p_eq.font.color.rgb = ACCENT_CYAN

    pinn_components = [
        ("Owen Aerodynamic Threshold Loss (L_Saltation)", [
            "• Formula: (1/N) * sum( ReLU(u_*t - u_*,i) * y_hat_i )",
            "• Physical Law: Wind cannot lift sand if surface friction velocity u_* is below threshold u_*t (~0.28 m/s).",
            "• Penalizes unphysical hallucinated dust emissions during calm conditions."
        ]),
        ("Mass Advection Continuity PDE Loss (L_Continuity)", [
            "• Formula: || d(y_hat)/dt + u * d(y_hat)/dx + v * d(y_hat)/dy - S ||^2",
            "• Physical Law: Governed by Navier-Stokes aerosol transport PDE.",
            "• Enforces mass conservation across grid cells and corridor graph edges."
        ]),
        ("Non-Negativity Barrier (L_NonNegative)", [
            "• Formula: (1/N) * sum( ReLU(-y_hat_i) )",
            "• Physical Law: Negative particulate concentrations are physically impossible.",
            "• Eliminates unphysical numerical undershoots common in standard neural nets."
        ])
    ]

    for idx, (title, items) in enumerate(pinn_components):
        left_pos = Inches(0.8 + idx * 3.95)
        c = add_card(s18, left_pos, Inches(3.5), Inches(3.8), Inches(3.3))
        tb = s18.shapes.add_textbox(left_pos + Inches(0.1), Inches(3.6), Inches(3.6), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(12.5)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_EMERALD
        for itm in items:
            p = tf.add_paragraph()
            p.text = itm
            p.font.size = Pt(10.5)
            p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 19: EXPLAINABLE AI (XAI) & SHAP
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    add_bg(s19)
    add_header(s19, "Explainable AI (XAI): SHAP Attribution & Physical Consistency", "CHAPTER 8: INTERPRETABILITY & VALIDATION")

    c1 = add_card(s19, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb1 = s19.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "TreeSHAP & DeepSHAP Formulations"
    tf1.paragraphs[0].font.size = Pt(15)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_CYAN
    pts1 = [
        "• Game-Theoretic Attribution: Computes exact Shapley values phi_i representing the marginal contribution of each atmospheric feature to predicted PM10.",
        "• Global Feature Importance Ranking:",
        "  1. Upwind Friction Velocity (u_* in Nafud & Dahna)",
        "  2. Desert Soil Moisture 0-7cm (SM_top suppression)",
        "  3. NWP Baseline CAMS Forecast (t + tau)",
        "  4. Wind Inflow Alignment Factor along Corridor Bearing",
        "  5. Autoregressive Lags (PM10 at t-1h, t-3h, t-24h)",
        "  6. Tuwayq Slope Roughness & Planetary Boundary Layer Height (BLH)."
    ]
    for pt in pts1:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    c2 = add_card(s19, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb2 = s19.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.paragraphs[0].text = "Local Storm Event Attribution & Trust"
    tf2.paragraphs[0].font.size = Pt(15)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = ACCENT_GOLD
    pts2 = [
        "• Case Attribution (e.g. March 2022 & April 2025 Events):",
        "  SHAP waterfall plots explain exactly why the AI triggered an extreme Haboob warning 4 days in advance.",
        "• Verification of Physical Plausibility: Confirms the model relies on legitimate atmospheric dynamics rather than spurious statistical artifacts.",
        "• Stakeholder Trust: Civil defense authorities and airport air traffic controllers can inspect the physical drivers behind automated alert escalations."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 20: VALIDATION STRATEGY & TESTING
    # ==========================================
    s20 = prs.slides.add_slide(blank_layout)
    add_bg(s20)
    add_header(s20, "Rigorous Validation Framework: Walk-Forward Cross-Validation", "CHAPTER 8: INTERPRETABILITY & VALIDATION")

    val_pillars = [
        ("1. Temporal Walk-Forward Split", [
            "• Strict chronological training: Train on past (2020-2023), evaluate on future (2024).",
            "• Zero random shuffling: Completely eliminates future-to-past temporal leakage.",
            "• Simulates realistic operational deployment conditions."
        ]),
        ("2. Spatial Leave-One-Station-Out", [
            "• Excludes one entire corridor station (e.g., Gassim or Al-Kharj) from training.",
            "• Tests model generalizability across unmonitored desert regions.",
            "• Verifies spatial transferability of the ST-GNN graph network."
        ]),
        ("3. Out-of-Sample Extreme Stress Cases", [
            "• Stress-testing on historic super-storms (e.g. March 15-16, 2021 super-storm, April 2025 event).",
            "• Evaluates peak concentration capture under extreme meteorological stress.",
            "• Assesses safety margins and false alarm rates."
        ]),
        ("4. Perturbation Sensitivity Testing", [
            "• Injects controlled perturbations into soil moisture and wind gust inputs.",
            "• Confirms output response strictly follows Owen saltation physics.",
            "• Validates robustness against sensor calibration drift."
        ])
    ]

    for idx, (title, items) in enumerate(val_pillars):
        col = idx % 2
        row = idx // 2
        left_pos = Inches(0.8 + col * 6.0)
        top_pos = Inches(1.8 + row * 2.6)
        c = add_card(s20, left_pos, top_pos, Inches(5.7), Inches(2.4))
        tb = s20.shapes.add_textbox(left_pos + Inches(0.15), top_pos + Inches(0.1), Inches(5.4), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_EMERALD
        for itm in items:
            p = tf.add_paragraph()
            p.text = itm
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 21: EVALUATION METRICS & ACCEPTANCE THRESHOLDS
    # ==========================================
    s21 = prs.slides.add_slide(blank_layout)
    add_bg(s21)
    add_header(s21, "Evaluation Metrics & WMO Verification Benchmarks", "CHAPTER 8: INTERPRETABILITY & VALIDATION")

    metrics_table = [
        ("Error Reduction Ratio (ΔRMSE%)", "Drop in RMSE compared to raw NWP baseline", ">= 25.0%", ACCENT_EMERALD),
        ("Continuous Determination (R²)", "Variance explained in PM10 concentrations", ">= 0.70", ACCENT_CYAN),
        ("Probability of Detection (POD / Hit Rate)", "H / (H + M) for verified sandstorm events", ">= 0.80", ACCENT_GOLD),
        ("Critical Success Index (CSI / Threat Score)", "H / (H + M + F) — WMO standard metric", ">= 0.60", ACCENT_EMERALD),
        ("False Alarm Ratio (FAR)", "F / (H + F) — minimizing unjustified city shutdowns", "<= 0.25", ACCENT_ROSE),
        ("Probabilistic Coverage (PICP)", "Observed values within [P10, P90] interval", ">= 85.0%", ACCENT_CYAN)
    ]

    for idx, (m_name, m_role, m_target, m_col) in enumerate(metrics_table):
        top_pos = Inches(1.8 + idx * 0.85)
        c = add_card(s21, Inches(0.8), top_pos, Inches(11.733), Inches(0.75))
        tb = s21.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.04), Inches(11.3), Inches(0.68))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = f"{m_name}   |   Target Benchmark: {m_target}"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = m_col
        p1 = tf.add_paragraph()
        p1.text = f"Role: {m_role}"
        p1.font.size = Pt(11)
        p1.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 22: LINE A VS LINE B COMPARATIVE MATRIX
    # ==========================================
    s22 = prs.slides.add_slide(blank_layout)
    add_bg(s22)
    add_header(s22, "Comparative Synthesis: Main Line A vs. Main Line B", "CHAPTER 9: SYNTHESIS & DISCUSSION")

    c1 = add_card(s22, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb1 = s22.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "Main Line A: Statistical Tree Ensembles"
    tf1.paragraphs[0].font.size = Pt(15)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_GOLD
    pts1 = [
        "• Core Purpose: Post-processing & bias-correcting operational NWP (CAMS & IFS).",
        "• Algorithms: LightGBM, CatBoost, XGBoost, Random Forest.",
        "• Input Representation: 2D Tabular Feature Matrix (43,800 x 55+).",
        "• Optimal Lead Times: Days 3–5 (+72h to +120h).",
        "• Strengths: Rapid inference (< 5 seconds), robust to tabular non-linearities, low computational overhead.",
        "• Failure Mode: Severe drift beyond Day 5; cannot model spatial wave propagation; dependent on NWP dust chemistry."
    ]
    for pt in pts1:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    c2 = add_card(s22, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb2 = s22.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.paragraphs[0].text = "Main Line B: Deep Spatiotemporal Models"
    tf2.paragraphs[0].font.size = Pt(15)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = ACCENT_EMERALD
    pts2 = [
        "• Core Purpose: Extended-range spatiotemporal forecasting bypassing NWP limits.",
        "• Algorithms: ST-GNN + Bi-LSTM + Transformer (TFT / Earthformer) + PINN.",
        "• Input Representation: Dynamic Graph A(t) + 5D Tensors [B, C, T, H, W].",
        "• Optimal Lead Times: Days 3–15 (Medium to S2S Horizons).",
        "• Strengths: Learns true advection physics, respects mass conservation, zero recursive tabular drift.",
        "• Implementation: GPU-accelerated PyTorch pipeline with Optuna hyperparameter optimization."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 23: OPERATIONAL EARLY WARNING PLAYBOOK
    # ==========================================
    s23 = prs.slides.add_slide(blank_layout)
    add_bg(s23)
    add_header(s23, "Operational Deployment: Municipal Early Warning Playbook", "CHAPTER 10: IMPACT & TRANSLATION")

    playbook_steps = [
        ("Continuous Ingestion (T - 0h)", "Hourly telemetry from 6 stations synced with latest ERA5 and satellite overpasses; Owen saltation trigger evaluated across 5 deserts."),
        ("Dual-Line Execution (T + 1h)", "Line A debiases daily CAMS cycle (+72h to +120h); Line B propagates ST-GNN and Transformer out to 15 days."),
        ("Automated Threshold Alerting", "If either line forecasts PM10 > 500 µg/m³ or Visibility < 1 km, automated red alert is transmitted to Civil Defense."),
        ("Targeted Action Protocols", "Aviation ground stops at KKIA, school and construction suspension, hospital emergency pediatric capacity expansion."),
        ("Model Retraining & Self-Correction", "Continuous learning loop ingests new storm observations, updating PINN loss weights and fine-tuning tree models.")
    ]

    for idx, (title, desc) in enumerate(playbook_steps):
        top_pos = Inches(1.8 + idx * 1.0)
        c = add_card(s23, Inches(0.8), top_pos, Inches(11.733), Inches(0.85))
        tb = s23.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.05), Inches(11.3), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_GOLD
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(11)
        p1.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 24: CONCLUSION & THESIS CONTRIBUTION
    # ==========================================
    s24 = prs.slides.add_slide(blank_layout)
    add_bg(s24)
    add_header(s24, "Conclusions, Contributions & Alignment with Saudi Vision 2030", "CHAPTER 11: CONCLUSIONS & CLOSING")

    c1 = add_card(s24, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb1 = s24.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.paragraphs[0].text = "🎓 Core Academic Contributions"
    tf1.paragraphs[0].font.size = Pt(15)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = ACCENT_GOLD
    pts1 = [
        "1. Overcomes 72h NWP Limit: Demonstrates that coupling statistical tree ensembles (Line A) with deep spatiotemporal graph learning (Line B) breaks the classical chaos barrier.",
        "2. Physics-Informed Rigor: First comprehensive SDS architecture for Riyadh integrating Owen saltation thresholds and mass continuity PDE loss directly into neural training.",
        "3. Connected Corridor Dynamics: Establishes a dynamic wind-advection graph linking 5 major desert source basins to the Riyadh urban receptor.",
        "4. Full Explainability: Validates feature attribution with SHAP, ensuring physical credibility for scientific publication."
    ]
    for pt in pts1:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    c2 = add_card(s24, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb2 = s24.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.paragraphs[0].text = "🇸🇦 National Strategic Alignment"
    tf2.paragraphs[0].font.size = Pt(15)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = ACCENT_CYAN
    pts2 = [
        "• Saudi Vision 2030: Directly supports environmental sustainability, smart city disaster management, and health protection.",
        "• Saudi Green Initiative (SGI): Provides high-resolution aerosol tracking to protect regional afforestation corridors from extreme sand encroachment.",
        "• Economic Safeguard: Mitigates billions in flight diversion costs, solar panel degradation, and traffic disruption across Riyadh.",
        "• Global Research Impact: Positions Saudi Arabia at the forefront of AI-driven environmental data science and climate resilience."
    ]
    for pt in pts2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 25: THANK YOU / Q&A
    # ==========================================
    s25 = prs.slides.add_slide(blank_layout)
    add_bg(s25)

    tb = s25.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "شُكْرًا لِحُسْنِ اسْتِمَاعِكُمْ"
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_GOLD
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = "Thank You for Your Attention  •  Q & A Session"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "\nApplying Machine Learning Algorithms to Improve the Accuracy of Medium- to Long-Term Sand and Dust Storm Forecasting"
    p2.font.size = Pt(18)
    p2.font.color.rgb = ACCENT_CYAN
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "\nALGHAMDI, HUDA 语嫣  |  DustML Research Platform  |  Riyadh, Saudi Arabia"
    p3.font.size = Pt(15)
    p3.font.color.rgb = TEXT_MUTED
    p3.alignment = PP_ALIGN.CENTER

    # Save presentation
    out_dir = r"c:\Users\hp\Desktop\sandstorm_forecasting\Persentation"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Applying_Machine_Learning_for_Sandstorm_Forecasting_Riyadh_Complete.pptx")
    prs.save(out_path)
    print(f"Successfully generated PowerPoint presentation at: {out_path}")

if __name__ == "__main__":
    build_presentation()
