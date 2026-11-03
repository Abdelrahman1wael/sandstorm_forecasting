import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def render_sitemap_image():
    fig = plt.figure(figsize=(24, 13), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 2400)
    ax.set_ylim(0, 1300)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    def draw_box(x, y, w, h, bg_color, border_color, title, items, title_color='#FFFFFF', text_color='#1E293B', title_size=10, text_size=8.5, border_w=1.5, arc=15):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0,rounding_size={arc}",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=border_w,
            zorder=3
        )
        ax.add_patch(box)
        
        # Draw Title
        if items:
            ax.text(x + 12, y + h - 18, title, fontsize=title_size, fontweight='bold', color=title_color, va='top', zorder=4, family='sans-serif')
            curr_y = y + h - 34
            for item in items:
                ax.text(x + 12, curr_y, item, fontsize=text_size, color=text_color, va='top', zorder=4, family='sans-serif')
                curr_y -= 14
        else:
            ax.text(x + w/2, y + h/2, title, fontsize=title_size, fontweight='bold', color=title_color, ha='center', va='center', zorder=4, family='sans-serif')

    def draw_edge(x1, y1, x2, y2, color='#64748B', lw=1.8, dashed=False):
        style = '--' if dashed else '-'
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle='-|>',
                color=color,
                lw=lw,
                ls=style,
                shrinkA=0, shrinkB=0,
                mutation_scale=12
            ),
            zorder=2
        )

    # 1. TOP ROOT SITEMAP BANNER
    root_x, root_y, root_w, root_h = 700, 1180, 1000, 80
    root_box = patches.FancyBboxPatch((root_x, root_y), root_w, root_h, boxstyle="round,pad=0,rounding_size=18", facecolor='#0F172A', edgecolor='#38BDF8', linewidth=2.5, zorder=3)
    ax.add_patch(root_box)
    ax.text(1200, 1235, "SAND & DUST STORM (SDS) FORECASTING TAXONOMY SITEMAP", fontsize=15, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4, family='sans-serif')
    ax.text(1200, 1205, "Comparative Hierarchy: Traditional Methods vs. Multi-Scale vs. Machine Learning vs. Deep Learning (LSTM/Transformer/GNN) vs. Tri-Pillar", fontsize=9.5, color='#94A3B8', ha='center', va='center', zorder=4, family='sans-serif')

    # Branch Layout Parameters
    col_w = 430
    col_gap = 35
    start_x = 50
    xs = [start_x + i * (col_w + col_gap) for i in range(5)]
    hdr_y = 1060
    hdr_h = 55

    # 2. LEVEL 1 BRANCH HEADERS
    b_data = [
        ("BRANCH 1: TRADITIONAL METHODS", "Synoptic, Classical Empirical & NWP/CTM", '#6B21A8', '#A855F7', '#FAF5FF', '#D8B4FE', '#3B0764'),
        ("BRANCH 2: MULTI-SCALE DYNAMICS", "Small, Medium & Large Space/Time Scales", '#B45309', '#F59E0B', '#FFFBEB', '#FDE68A', '#78350F'),
        ("BRANCH 3: MACHINE LEARNING (LINE A)", "Statistical AI, GBDT Ensembles & Post-Processing", '#0284C7', '#38BDF8', '#F0F9FF', '#BAE6FD', '#0C4A6E'),
        ("BRANCH 4: DEEP LEARNING (LINE B)", "LSTM, Transformer & GNN Architectures", '#4338CA', '#818CF8', '#EEF2FF', '#C7D2FE', '#1E1B4B'),
        ("BRANCH 5: WHAT SHE USES (TRI-PILLAR)", "AI (LSTM/Transformer/GNN) + GIS + SEM/PADM", '#0F766E', '#2DD4BF', '#F0FDFA', '#99F6E4', '#134E4A')
    ]

    for i in range(5):
        title, sub, hdr_bg, hdr_border, _, _, _ = b_data[i]
        hb = patches.FancyBboxPatch((xs[i], hdr_y), col_w, hdr_h, boxstyle="round,pad=0,rounding_size=12", facecolor=hdr_bg, edgecolor=hdr_border, linewidth=2, zorder=3)
        ax.add_patch(hb)
        ax.text(xs[i] + col_w/2, hdr_y + 35, title, fontsize=11, fontweight='bold', color='#FFFFFF', ha='center', va='center', zorder=4, family='sans-serif')
        ax.text(xs[i] + col_w/2, hdr_y + 16, sub, fontsize=8, color='#E2E8F0', ha='center', va='center', zorder=4, family='sans-serif')
        # Bus connect from Root to Branch
        draw_edge(1200, root_y, xs[i] + col_w/2, hdr_y + hdr_h, color=hdr_border, lw=2)

    # 3. LEAF CARDS PER BRANCH
    card_h = 135
    card_gap = 25
    base_y = 890

    # Branch 1 Cards
    b1_cards = [
        ("1.1 Subjective Synoptic Analysis", ["• Manual surface isobaric chart tracing", "• 500 hPa troughs & 850 hPa wind convergence", "• Delta-P > 4-6 hPa pressure gradient rules", "• Subjective forecaster experience heuristic"], False),
        ("1.2 Classical Empirical Saltation", ["• Persistence & 30-year climatology baseline", "• Linear regressions & ARIMA time-series", "• Bagnold (1941) sand flux: q ~ (rho/g) u_*^3", "• Owen (1964) saltation threshold gate: u_* > u_*t"], False),
        ("1.3 Dynamical NWP & CTM Models", ["• Global NWP: ECMWF IFS, CMA-GFS", "• Atmospheric CTM: WRF-Chem, DREAM8b, CAMS", "• Hydrodynamic Navier-Stokes equations", "• Aerosol continuity: dC/dt + div(uC) = K div^2 C + S - vd C"], False),
        ("1.4 Operational Bottlenecks [CRITICAL]", ["• Chaotic Lyapunov Limit: collapses after Day 3", "• Coarse 9-25km grid misses Wadi Hanifa & escarpments", "• Inability to model convective Haboob downburst walls", "• Extreme supercomputer HPC burden (hours per cycle)"], True)
    ]
    curr_y = base_y
    for title, items, is_alert in b1_cards:
        bg = '#FEF2F2' if is_alert else '#FAF5FF'
        bd = '#EF4444' if is_alert else '#C084FC'
        tc = '#991B1B' if is_alert else '#6B21A8'
        txtc = '#7F1D1D' if is_alert else '#3B0764'
        draw_box(xs[0], curr_y, col_w, card_h, bg, bd, title, items, title_color=tc, text_color=txtc)
        draw_edge(xs[0] + col_w/2, curr_y + card_h + card_gap, xs[0] + col_w/2, curr_y + card_h, color='#A855F7', lw=1.5)
        curr_y -= (card_h + card_gap)

    # Branch 2 Cards (Multi-Scale)
    b2_cards = [
        ("2.1 Small Scale (Microscale & Short-Term)", ["• Spatial: < 2 km (microscale boundary layer shear)", "• Temporal: 0–72 h (nowcasting & acute alerts at KKIA)", "• Hazard: Level 1–2 (Mild haze, PM10 < 150 ug/m3)", "• Friction velocity u_* & local roughness z_0 gating"], '#ECFDF5', '#10B981', '#064E3B'),
        ("2.2 Medium Scale (Mesoscale & Extended)", ["• Spatial: 2–2,000 km (convective Haboob dust walls)", "• Temporal: 3–15 days (Sub-seasonal) — Core Focus!", "• Hazard: Level 3–4 (Blowing sand: 150–2,000 ug/m3)", "• Municipal pre-wetting & flight rerouting window"], '#FFFBEB', '#F59E0B', '#78350F'),
        ("2.3 Large Scale (Synoptic & Seasonal)", ["• Spatial: > 2,000 km (regional Shamal regimes)", "• Temporal: > 15–90+ days (seasonal drought memory)", "• Hazard: Level 5 (Catastrophic blackout Haboob >5,000)", "• Teleconnections: ENSO (ONI/MEI), NAO, AO, IOD"], '#FEF2F2', '#EF4444', '#7F1D1D'),
        ("2.4 5-Tier Hazard Classification", ["• Level 1: Normal air (PM10 < 50 ug/m3, Vis >10km)", "• Level 2: Slight dust (PM10 50-150 ug/m3)", "• Level 3: Moderate blowing sand (PM10 150-500 ug/m3)", "• Level 4-5: Severe Haboob (PM10 >2,000 ug/m3, Vis <200m)"], '#FFFBEB', '#F59E0B', '#78350F')
    ]
    curr_y = base_y
    for title, items, bg, bd, tc in b2_cards:
        draw_box(xs[1], curr_y, col_w, card_h, bg, bd, title, items, title_color=tc, text_color=tc)
        draw_edge(xs[1] + col_w/2, curr_y + card_h + card_gap, xs[1] + col_w/2, curr_y + card_h, color='#F59E0B', lw=1.5)
        curr_y -= (card_h + card_gap)

    # Branch 3 Cards (Machine Learning)
    b3_cards = [
        ("3.1 Classical ML (Literature Cited)", ["• Artificial Neural Networks (ANN / Multi-Layer Perceptrons)", "• Support Vector Machines (SVM) with 500 hPa fields", "• Fuzzy logic (ANFIS) & Radial Basis Functions (RBF)", "• Bayesian Networks + Case-Based Reasoning (CBR)"], False),
        ("3.2 GBDT Tree Ensembles", ["• LightGBM: ultra-fast leaf-wise histogram splits", "• CatBoost: ordered target encoding for station data", "• XGBoost: regularized depth-wise gradient boosting", "• AutoML: AutoGluon & AutoFeat-TPOT pipelines"], False),
        ("3.3 Imbalance & Cost-Sensitive Learning", ["• The <3% rare storm frequency challenge", "• SMOTE minority oversampling for extreme events", "• Asymmetric cost matrix (false negative penalty 10x)", "• Focal Loss down-weighting easy normal weather"], True),
        ("3.4 NWP Bias Correction & Quantiles", ["• Residual learning: y_true = NWP + f_GBDT(X_env)", "• Pinball loss quantiles: P10, P50 (median), P90 (risk)", "• Calibrated non-crossing prediction intervals", "• Tree SHAP game-theoretic feature attribution"], False)
    ]
    curr_y = base_y
    for title, items, is_hl in b3_cards:
        bg = '#F0FDFA' if is_hl else '#F0F9FF'
        bd = '#14B8A6' if is_hl else '#38BDF8'
        tc = '#0F766E' if is_hl else '#0284C7'
        txtc = '#134E4A' if is_hl else '#0C4A6E'
        draw_box(xs[2], curr_y, col_w, card_h, bg, bd, title, items, title_color=tc, text_color=txtc)
        draw_edge(xs[2] + col_w/2, curr_y + card_h + card_gap, xs[2] + col_w/2, curr_y + card_h, color='#0284C7', lw=1.5)
        curr_y -= (card_h + card_gap)

    # Branch 4 Cards (Deep Learning: LSTM, Transformer, GNN)
    b4_cards = [
        ("4.1 Long Short-Term Memory (LSTM)", ["• Recurrent temporal gating for sequential accumulation", "• Bidirectional LSTM/GRU with temporal attention", "• Captures multi-step ahead continuous concentrations", "• Solves long-range vanishing temporal gradients"], '#EEF2FF', '#818CF8', '#3730A3'),
        ("4.2 Transformer & Attention Networks", ["• Multi-head self-attention for sub-seasonal waves", "• Spatiotemporal attention capturing planetary forcing", "• Models non-local teleconnection tele-couplings", "• Maintains robust predictive attention into Day 15"], '#EEF2FF', '#818CF8', '#3730A3'),
        ("4.3 Corridor Graph Networks (ST-GNN)", ["• 14-Node directional transport corridor topology", "• Asymmetric Chebyshev polynomial graph convolutions", "• Captures directional upwind-to-downwind transport", "• Models Ad-Dahna & An-Nafud outflow into Riyadh"], '#FAF5FF', '#C084FC', '#6B21A8'),
        ("4.4 Computer Vision & Foundation AI", ["• 2D/3D CNNs extracting vortex circulations from grids", "• Transfer learning on FengYun FY-4 & MODIS AOD", "• Coupled AI-GAMFS 5km grid (twice-daily cycles)", "• 38%-74% error reduction vs standard ECMWF/NASA"], '#EEF2FF', '#818CF8', '#3730A3')
    ]
    curr_y = base_y
    for title, items, bg, bd, tc in b4_cards:
        draw_box(xs[3], curr_y, col_w, card_h, bg, bd, title, items, title_color=tc, text_color=tc)
        draw_edge(xs[3] + col_w/2, curr_y + card_h + card_gap, xs[3] + col_w/2, curr_y + card_h, color='#6366F1', lw=1.5)
        curr_y -= (card_h + card_gap)

    # Branch 5 Cards (What She Uses - Tri-Pillar)
    b5_cards = [
        ("5.1 Pillar 1: AI (LSTM + Transformer + GNN)", ["• Dual-line: Line A GBDT + Line B LSTM/Transformer/GNN", "• Replaces PINN with pure data-driven deep triad", "• Extended 3-15 days forecast with P10/P50/P90 envelopes", "• Tree SHAP + attention rollouts for XAI diagnostics"]),
        ("5.2 Pillar 2: Spatial Geography & GIS", ["• Ordinary Kriging spatial exposure & vulnerability maps", "• Global Moran's I & LISA local high-high cluster maps", "• Geographically Weighted Regression (GWR) on z_0", "• 90m SRTM DEM topographical escarpment analysis"]),
        ("5.3 Pillar 3: Socioeconomic Behavioral Science", ["• IBM SPSS: Little's MCAR missing test & EFA screening", "• IBM AMOS: Confirmatory Factor Analysis (CFA)", "• Construct Reliability CR >= 0.70 & Convergent AVE >= 0.50", "• Protective Action Decision Model (PADM) SEM compliance"]),
        ("5.4 Municipal Crisis Early Warning Playbook", ["• 4-Tier operational matrix: T-15d -> T-5d -> T-24h -> T-0h", "• Aviation: flight holds & runway diversions at KKIA", "• Urban: high-pressure street misting & cannon deployment", "• Health: preemptive respiratory medication stocking"])
    ]
    curr_y = base_y
    for title, items in b5_cards:
        draw_box(xs[4], curr_y, col_w, card_h, '#F0FDFA', '#14B8A6', title, items, title_color='#0F766E', text_color='#134E4A')
        draw_edge(xs[4] + col_w/2, curr_y + card_h + card_gap, xs[4] + col_w/2, curr_y + card_h, color='#0F766E', lw=1.5)
        curr_y -= (card_h + card_gap)

    # 4. BOTTOM SITEMAP SUMMARY FOOTER
    foot_y = 170
    foot_w = 2300
    foot_box = patches.FancyBboxPatch((50, foot_y), foot_w, 65, boxstyle="round,pad=0,rounding_size=12", facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.5, zorder=3)
    ax.add_patch(foot_box)
    ax.text(1200, foot_y + 40, "METHODOLOGICAL PARADIGM EVOLUTION (SITEMAP SUMMARY)", fontsize=11, fontweight='bold', color='#0F172A', ha='center', va='center', zorder=4, family='sans-serif')
    ax.text(1200, foot_y + 18, "Traditional NWP (Chaotic 72h Lyapunov Barrier)  ➔  Line A GBDT Bias Correction (Quantiles P10/P50/P90)  ➔  Line B Deep AI (LSTM + Transformer + Corridor GNN)  ➔  Tri-Pillar Delivery (GIS Kriging + SPSS/AMOS PADM)", fontsize=9, color='#475569', ha='center', va='center', zorder=4, family='sans-serif')

    # Connect bottoms of branches to footer
    for i in range(5):
        draw_edge(xs[i] + col_w/2, base_y - 3*(card_h + card_gap), xs[i] + col_w/2, foot_y + 65, color='#94A3B8', lw=1.2, dashed=True)

    img_png_path = "c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Supervisor/sandstorm_forecasting_taxonomy.png"
    img_svg_path = "c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Supervisor/sandstorm_forecasting_taxonomy.svg"
    plt.tight_layout()
    plt.savefig(img_png_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.savefig(img_svg_path, format='svg', facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    
    # Also save to root and Digrams
    plt.savefig("c:/Users/hp/Desktop/sandstorm_forecasting/sandstorm_forecasting_taxonomy.png", dpi=300, bbox_inches='tight')
    plt.savefig("c:/Users/hp/Desktop/sandstorm_forecasting/Digrams/sandstorm_forecasting_taxonomy.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved high-res PNG and SVG sitemap images successfully!")

def build_supervisor_document():
    doc = Document()
    
    # Page Setup (Letter, 1 inch margins)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    # Helper function for cell background color
    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    # Helper function for headings
    def add_custom_heading(text, level, color_hex="1E3A8A"):
        h = doc.add_heading(text, level=level)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        for run in h.runs:
            run.font.name = 'Calibri'
            run.font.bold = True
            r, g, b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
            run.font.color.rgb = RGBColor(r, g, b)
        return h

    # Title & Header
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = title_p.add_run("TAXONOMY & SITEMAP OF SAND AND DUST STORM (SDS) FORECASTING METHODOLOGIES")
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(18)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = sub_p.add_run("Technical Synthesis: Traditional Forecasting vs. Multi-Scale Dynamics vs. Proposed Machine Learning & Deep Learning Architecture (LSTM + Transformer + GNN)\nMaster of Engineering • Academic Supervisor Dossier")
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x47, 0x55, 0x69)

    # Executive Summary Callout Box
    tbl_callout = doc.add_table(rows=1, cols=1)
    tbl_callout.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl_callout.cell(0, 0)
    set_cell_background(cell, "F0F9FF")
    cell.paragraphs[0].paragraph_format.space_before = Pt(6)
    cell.paragraphs[0].paragraph_format.space_after = Pt(6)
    r_box_title = cell.paragraphs[0].add_run("EXECUTIVE RESEARCH SUMMARY\n")
    r_box_title.bold = True
    r_box_title.font.color.rgb = RGBColor(0x03, 0x69, 0xA1)
    r_box_txt = cell.paragraphs[0].add_run(
        "This dossier synthesizes the complete taxonomic classification of sand and dust storm forecasting paradigms "
        "identified across global meteorological literature and the research proposal for Riyadh, Saudi Arabia. "
        "It details the scientific limitations of traditional Numerical Weather Prediction (NWP), establishes a tri-dimensional "
        "scale taxonomy (Small, Medium, Large), and outlines the updated research modeling framework: combining Tree Ensembles (Line A) "
        "with a Deep Learning triad—LSTM (temporal sequence memory), Transformer (multi-head self-attention), and Spatio-Temporal GNNs (14-node directional corridor advection)—integrated "
        "with GIS spatial geostatistics and SPSS/AMOS socioeconomic behavioral science."
    )
    r_box_txt.font.size = Pt(10)

    # 1. High-Resolution Visual Sitemap Image
    add_custom_heading("1. Visual Taxonomy & Hierarchy Sitemap", level=1, color_hex="0F172A")
    doc.add_paragraph(
        "The following publication-grade sitemap visually maps the hierarchy from traditional physical paradigms, "
        "through multi-scale environmental dynamics, to the proposed machine learning and deep learning methodologies:"
    )

    png_path = "c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Supervisor/sandstorm_forecasting_taxonomy.png"
    if os.path.exists(png_path):
        doc.add_picture(png_path, width=Inches(6.5))
        caption_p = doc.add_paragraph()
        caption_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption_p.paragraph_format.space_after = Pt(14)
        r_cap = caption_p.add_run("Figure 1: Full-Spectrum Sitemap Taxonomy of Sand & Dust Storm Forecasting Paradigms (Draw.io Export).")
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # 2. Traditional Methods
    add_custom_heading("2. Traditional Forecasting Methods & Their Failure Modes", level=1, color_hex="6B21A8")
    doc.add_paragraph(
        "Historically, sandstorm forecasting has relied on three foundational, non-learning paradigms:\n"
        "• Synoptic Subjective Weather Analysis: Forecasters manually inspect daily surface isobaric charts, upper-air potential fields (500 hPa geopotential troughs, 850 hPa low-level jets), and regional pressure gradient rules (e.g., Delta-P > 4-6 hPa across northern deserts driving Shamal winds).\n"
        "• Classical Empirical Saltation Physics: Physical transport formulas dating from Bagnold (1941) sand transport flux (scaling with the cube of friction velocity q ~ u_*^3) and Owen (1964) saltation threshold gating (u_* > u_*t), with Gillette (1979) damp soil moisture bridging corrections.\n"
        "• Dynamical Numerical Weather Prediction (NWP) & Chemistry-Transport Models (CTMs): Discretized integration of atmospheric Navier-Stokes fluid equations and aerosol advection-diffusion-deposition PDEs (ECMWF IFS, CMA-GFS, WRF-Chem, DREAM8b, Copernicus CAMS)."
    )
    
    warn_p = doc.add_paragraph()
    r_warn = warn_p.add_run("Critical Operational Bottlenecks: ")
    r_warn.bold = True
    r_warn.font.color.rgb = RGBColor(0xB9, 0x1C, 0x1C)
    warn_p.add_run(
        "Traditional NWP models suffer from the chaotic Lyapunov Horizon limit (T_Lyap ~ 72 hours / Day 3), beyond which deterministic error growth diverges exponentially. "
        "Furthermore, coarse grid resolutions (9-25 km) fail to resolve sub-grid orographic channeling through narrow corridors (such as Jabal Tuwaiq and Wadi Hanifa in Riyadh), "
        "cannot simulate rapid convective Haboob downburst walls, and demand massive supercomputer compute cycles that prevent agile real-time emergency cycle updates."
    )

    # 3. Multi-Scale Taxonomy
    add_custom_heading("3. Multi-Scale Taxonomic Classification (Small, Medium, Large)", level=1, color_hex="B45309")
    doc.add_paragraph(
        "Sand and dust storms operate across three intertwined dimensions:\n"
        "• Small Scale (Microscale & Short-Term): Spatial extent < 2 km (boundary layer turbulence, local saltation, urban canyons); temporal horizon 0–72 hours (nowcasting, flight runway holds at KKIA); hazard level 1–2 (mild haze, PM10 < 150 ug/m3).\n"
        "• Medium Scale (Mesoscale & Extended-Range): Spatial extent 2–2,000 km (convective Haboob dust walls, Ad-Dahna / An-Nafud corridor channeling); temporal horizon 3–15 days (sub-seasonal)—the primary scientific innovation frontier of this dissertation; hazard level 3–4 (blowing sand to severe storm, PM10: 150–2,000 ug/m3).\n"
        "• Large Scale (Synoptic-Macro & Seasonal): Spatial extent > 2,000 km (regional Shamal regimes, transboundary Rub' al Khali plumes); temporal horizon > 15–90+ days (seasonal drought memory, planetary teleconnections: ENSO, NAO, AO, IOD); hazard level 5 (catastrophic blackout Haboob, PM10 > 5,000 ug/m3)."
    )

    # 4. Machine Learning (Line A)
    add_custom_heading("4. Machine Learning & GBDT Post-Processing (Main Line A)", level=1, color_hex="0284C7")
    doc.add_paragraph(
        "To correct systematic NWP drifts without incurring supercomputer costs, Main Line A establishes an ensemble post-processing framework:\n"
        "• Gradient Boosting Ensembles: LightGBM (ultra-fast leaf-wise histogram splits), CatBoost (ordered target encoding for categorical station and wind sector features without target leakage), and XGBoost (regularized depth-wise splits).\n"
        "• Rare Class Imbalance Optimization: Because severe dust storms occur on <3% of annual days, standard ML exhibits severe negative bias. This is resolved via SMOTE synthetic oversampling, asymmetric cost matrices (10x penalty on false negatives), and Focal Loss.\n"
        "• Quantile Uncertainty Envelopes: Minimized via Pinball Loss to output calibrated, non-crossing prediction intervals: P10 (optimistic), P50 (median), and P90 (risk-averse threshold).\n"
        "• Explainable AI (Tree SHAP): Game-theoretic feature attribution isolating exact physical trigger thresholds (e.g., 10m wind speed crossing 8.5 m/s combined with topsoil moisture < 0.08 m3/m3)."
    )

    # 5. Deep Learning (Line B: LSTM, Transformer, GNN)
    add_custom_heading("5. Deep Learning Spatiotemporal Architecture (Main Line B)", level=1, color_hex="4338CA")
    doc.add_paragraph(
        "In accordance with updated methodological designs, Main Line B replaces differential PDE loss regularization (PINN) "
        "with an advanced pure data-driven Deep Learning Triad specifically tailored for atmospheric spatiotemporal sequences:\n"
        "• 1. Long Short-Term Memory (LSTM): Recurrent temporal gating (input, forget, and output gates) modeling sequential dust mass accumulation and dispersion across consecutive hourly time-steps.\n"
        "• 2. Spatiotemporal Transformers: Multi-head self-attention mechanisms capturing long-range planetary wave trains and sub-seasonal teleconnections, maintaining high predictive skill across the extended 3–15 day horizon without vanishing gradients.\n"
        "• 3. Spatio-Temporal Graph Neural Networks (ST-GNN): A 14-node directional graph topology linking upstream desert source basins (An-Nafud, Ad-Dahna) with downstream receptor stations in Riyadh. Uses 3-support asymmetric Chebyshev polynomial graph convolutions to simulate physical directional advection driven by prevailing northwest Shamal winds.\n"
        "• 4. Coupled AI-GAMFS Vision Backbone: Ingests 5km gridded multi-channel tensors ([B, 3, 32, 32]: MODIS AOD, 10m U-wind, 10m V-wind) with twice-daily operational updates, matching or exceeding international general circulation models."
    )

    # 6. Tri-Pillar Integration
    add_custom_heading("6. Tri-Pillar Integration & Socioeconomic Delivery", level=1, color_hex="0F766E")
    doc.add_paragraph(
        "To bridge the gap between meteorological engineering and public emergency management, the research couples three pillars:\n"
        "• Pillar 1 (Meteorological AI): Line A GBDT ensembles + Line B deep triad (LSTM, Transformer, ST-GNN).\n"
        "• Pillar 2 (Spatial GIS Geography): Ordinary Kriging spatial exposure interpolation, Global Moran's I spatial autocorrelation, LISA local high-high risk clustering, and Geographically Weighted Regression (GWR) on surface roughness z_0.\n"
        "• Pillar 3 (Socioeconomic Behavioral Science): IBM SPSS data hygiene (Little's MCAR missing test, Mahalanobis D2 multivariate outlier audit, EFA) and IBM AMOS Confirmatory Factor Analysis (CFA; CR >= 0.70, AVE >= 0.50) modeling the Protective Action Decision Model (PADM) structural equation model.\n"
        "• 4-Tier Municipal Playbook: Translating probability envelopes into concrete actions across T-15d (sub-seasonal outlook), T-5d (pre-disaster highway misting & airline rerouting), T-24h (runway holds & hospital alerts), and T-0h (lockdown)."
    )

    # 7. Master Comparison Table
    add_custom_heading("7. Master Methodological Comparison Matrix", level=1, color_hex="0F172A")
    table_data = [
        ["Dimension", "Traditional Methods", "Machine Learning (Line A)", "Deep Learning (Line B - Updated)"],
        ["Core Models", "ECMWF IFS, WRF-Chem, Bagnold flux", "LightGBM, CatBoost, XGBoost", "LSTM, Transformer, ST-GNN, AI-GAMFS"],
        ["Primary Role", "Hydrodynamic baseline simulation", "Statistical NWP bias correction", "End-to-end spatiotemporal corridor prediction"],
        ["Extended Horizon (3-15d)", "Rapid skill collapse after Day 3", "Calibrated quantiles (P10/P50/P90)", "High skill via self-attention & graph advection"],
        ["Spatial Resolution", "Coarse 9–25 km grid", "Station-level local downscaling", "5 km grid + 14-node directional corridor graph"],
        ["Extreme Storm Handling", "Underestimates sudden spikes", "SMOTE + Cost-Sensitive Focal Loss", "Spatiotemporal attention on moving fronts"],
        ["Explainability", "High theoretical physics, low XAI", "Tree SHAP exact feature attribution", "Attention rollouts & graph edge weights"],
        ["Societal Link", "Disconnected from social response", "Probability input to municipal playbooks", "Coupled with GIS Kriging & AMOS SEM (PADM)"]
    ]

    tbl = doc.add_table(rows=len(table_data), cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].paragraph_format.space_before = Pt(4)
            cell.paragraphs[0].paragraph_format.space_after = Pt(4)
            if r_idx == 0:
                set_cell_background(cell, "1E293B")
                p = cell.paragraphs[0]
                for r in p.runs:
                    r.font.bold = True
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                bg_col = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
                set_cell_background(cell, bg_col)
                p = cell.paragraphs[0]
                for r in p.runs:
                    r.font.size = Pt(9)
                    if c_idx == 0:
                        r.font.bold = True

    doc_path = "c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Supervisor/Sandstorm_Forecasting_Taxonomy_and_Methodology.docx"
    doc.save(doc_path)
    
    # Also save copy in root and Documentation
    doc.save("c:/Users/hp/Desktop/sandstorm_forecasting/Sandstorm_Forecasting_Taxonomy_and_Methodology.docx")
    doc.save("c:/Users/hp/Desktop/sandstorm_forecasting/Documentation/Sandstorm_Forecasting_Taxonomy_and_Methodology.docx")
    print("Saved comprehensive Word document at all locations!")

if __name__ == '__main__':
    render_sitemap_image()
    build_supervisor_document()
