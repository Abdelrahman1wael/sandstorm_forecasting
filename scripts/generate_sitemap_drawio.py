import xml.etree.ElementTree as ET

def build_simple_sitemap_drawio():
    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-24T13:45:00.000Z", agent="Antigravity", version="24.0.0", type="device")
    diagram = ET.SubElement(mxfile, "diagram", id="sds-clean-sitemap", name="SDS_Clean_Sitemap")
    model = ET.SubElement(diagram, "mxGraphModel", dx="2000", dy="1200", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="2100", pageHeight="1100", math="0", shadow="0")
    root = ET.SubElement(model, "root")

    # Base cells
    c0 = ET.SubElement(root, "mxCell", id="0")
    c1 = ET.SubElement(root, "mxCell", id="1", parent="0")

    cell_id = 1
    def next_id():
        nonlocal cell_id
        cell_id += 1
        return str(cell_id)

    def add_node(label, x, y, w, h, style, parent_id="1"):
        cid = next_id()
        cell = ET.SubElement(root, "mxCell", id=cid, value=label, style=style, vertex="1", parent=parent_id)
        mxGeo = ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h))
        mxGeo.set("as", "geometry")
        return cid

    def add_edge(source_id, target_id, style):
        cid = next_id()
        cell = ET.SubElement(root, "mxCell", id=cid, style=style, edge="1", parent="1", source=source_id, target=target_id)
        mxGeo = ET.SubElement(cell, "mxGeometry", relative="1")
        mxGeo.set("as", "geometry")
        return cid

    # ----------------------------------------------------
    # SIMPLE, CLEAN DRAW.IO STYLES
    # ----------------------------------------------------
    root_style = "rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#1E293B;strokeColor=#38BDF8;strokeWidth=2;fontColor=#FFFFFF;fontFamily=Helvetica;fontSize=14;fontStyle=1;align=center;"
    
    # Headers
    h_trad = "rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#6B21A8;strokeColor=#7E22CE;strokeWidth=2;fontColor=#FFFFFF;fontFamily=Helvetica;fontSize=12;fontStyle=1;align=center;"
    h_scale = "rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#B45309;strokeColor=#D97706;strokeWidth=2;fontColor=#FFFFFF;fontFamily=Helvetica;fontSize=12;fontStyle=1;align=center;"
    h_ml   = "rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#0284C7;strokeColor=#0EA5E9;strokeWidth=2;fontColor=#FFFFFF;fontFamily=Helvetica;fontSize=12;fontStyle=1;align=center;"
    h_dl   = "rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#4338CA;strokeColor=#6366F1;strokeWidth=2;fontColor=#FFFFFF;fontFamily=Helvetica;fontSize=12;fontStyle=1;align=center;"
    h_tri  = "rounded=1;whiteSpace=wrap;html=1;arcSize=10;fillColor=#0F766E;strokeColor=#14B8A6;strokeWidth=2;fontColor=#FFFFFF;fontFamily=Helvetica;fontSize=12;fontStyle=1;align=center;"

    # Simple Leaf Shapes (Clean & Legible)
    c_trad = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FAF5FF;strokeColor=#D8B4FE;strokeWidth=1;fontColor=#3B0764;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"
    c_trad_warn = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FEF2F2;strokeColor=#F87171;strokeWidth=1.5;fontColor=#991B1B;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"

    c_scale_sm = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#ECFDF5;strokeColor=#6EE7B7;strokeWidth=1;fontColor=#064E3B;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"
    c_scale_md = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FFFBEB;strokeColor=#FCD34D;strokeWidth=1.5;fontColor=#78350F;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"
    c_scale_lg = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FEF2F2;strokeColor=#FCA5A5;strokeWidth=1;fontColor=#7F1D1D;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"

    c_ml = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#F0F9FF;strokeColor=#7DD3FC;strokeWidth=1;fontColor=#0C4A6E;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"
    c_ml_hl = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#F0FDFA;strokeColor=#5EEAD4;strokeWidth=1.5;fontColor=#134E4A;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"

    c_dl = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#EEF2FF;strokeColor=#A5B4FC;strokeWidth=1;fontColor=#1E1B4B;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"
    c_dl_pinn = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#FAF5FF;strokeColor=#C084FC;strokeWidth=1.5;fontColor=#4A044E;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"

    c_tri = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#F0FDFA;strokeColor=#5EEAD4;strokeWidth=1;fontColor=#134E4A;fontFamily=Helvetica;fontSize=11;align=left;spacingLeft=8;spacingRight=8;"

    footer_style = "rounded=1;whiteSpace=wrap;html=1;arcSize=8;fillColor=#F8FAFC;strokeColor=#94A3B8;strokeWidth=1;fontColor=#334155;fontFamily=Helvetica;fontSize=11;align=center;"

    # Clean Tree Connector Styles
    e_trad = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#A855F7;strokeWidth=1.5;endArrow=classic;endFill=1;"
    e_scale= "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#D97706;strokeWidth=1.5;endArrow=classic;endFill=1;"
    e_ml   = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#0284C7;strokeWidth=1.5;endArrow=classic;endFill=1;"
    e_dl   = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#6366F1;strokeWidth=1.5;endArrow=classic;endFill=1;"
    e_tri  = "edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#0F766E;strokeWidth=1.5;endArrow=classic;endFill=1;"

    # ----------------------------------------------------
    # SITEMAP TOP ROOT
    # ----------------------------------------------------
    root_node = add_node(
        "<b>🌪️ SAND &amp; DUST STORM (SDS) FORECASTING TAXONOMY SITEMAP</b><br/>"
        "<span style='font-size:11px; font-weight:normal;'>Hierarchical Classification of Methodologies in Literature Review &amp; Master Research Proposal</span>",
        810, 30, 480, 55, root_style
    )

    # ----------------------------------------------------
    # BRANCH POSITIONS & GEOMETRY
    # ----------------------------------------------------
    x_coords = [50, 450, 850, 1250, 1650]
    w_card = 360
    h_card = 68
    y_hdr = 140
    y_step = 80
    y_base = 230

    # Level 1 Headers
    h1 = add_node("<b>🟣 1. TRADITIONAL METHODS</b><br/><span style='font-size:10px;'>Synoptic, Empirical &amp; NWP/CTM</span>", x_coords[0], y_hdr, w_card, 50, h_trad)
    h2 = add_node("<b>⚖️ 2. MULTI-SCALE SYSTEM</b><br/><span style='font-size:10px;'>Small, Medium &amp; Large Scales</span>", x_coords[1], y_hdr, w_card, 50, h_scale)
    h3 = add_node("<b>🔵 3. MACHINE LEARNING (LINE A)</b><br/><span style='font-size:10px;'>Tree Ensembles &amp; Bias Correction</span>", x_coords[2], y_hdr, w_card, 50, h_ml)
    h4 = add_node("<b>🔮 4. DEEP LEARNING (LINE B)</b><br/><span style='font-size:10px;'>LSTM, Transformer &amp; GNN Models</span>", x_coords[3], y_hdr, w_card, 50, h_dl)
    h5 = add_node("<b>🩵 5. WHAT SHE USES (TRI-PILLAR)</b><br/><span style='font-size:10px;'>AI (LSTM/Transformer/GNN) + GIS + SEM</span>", x_coords[4], y_hdr, w_card, 50, h_tri)

    add_edge(root_node, h1, e_trad)
    add_edge(root_node, h2, e_scale)
    add_edge(root_node, h3, e_ml)
    add_edge(root_node, h4, e_dl)
    add_edge(root_node, h5, e_tri)

    # ----------------------------------------------------
    # BRANCH 1: TRADITIONAL
    # ----------------------------------------------------
    b1_1 = add_node(
        "<b>1.1 Subjective Synoptic Analysis</b><br/>"
        "• Manual surface weather isobaric charts<br/>"
        "• 500 hPa geopotential troughs &amp; 850 hPa wind convergence",
        x_coords[0], y_base, w_card, h_card, c_trad
    )
    b1_2 = add_node(
        "<b>1.2 Classical Empirical Saltation</b><br/>"
        "• Bagnold (1941) sand flux: q ~ u*³<br/>"
        "• Owen (1964) saltation threshold gate: u* &gt; u*t",
        x_coords[0], y_base + y_step, w_card, h_card, c_trad
    )
    b1_3 = add_node(
        "<b>1.3 Dynamical NWP &amp; Chemistry Models</b><br/>"
        "• ECMWF IFS, CMA-GFS, WRF-Chem, CAMS<br/>"
        "• Discretized Navier-Stokes &amp; aerosol continuity PDEs",
        x_coords[0], y_base + y_step*2, w_card, h_card, c_trad
    )
    b1_4 = add_node(
        "<b>1.4 Operational Bottlenecks (⚠️)</b><br/>"
        "• Chaotic Lyapunov limit (diverges after Day 3)<br/>"
        "• Coarse grid misses Wadi Hanifa &amp; convective Haboobs",
        x_coords[0], y_base + y_step*3, w_card, h_card, c_trad_warn
    )

    add_edge(h1, b1_1, e_trad)
    add_edge(b1_1, b1_2, e_trad)
    add_edge(b1_2, b1_3, e_trad)
    add_edge(b1_3, b1_4, e_trad)

    # ----------------------------------------------------
    # BRANCH 2: MULTI-SCALE
    # ----------------------------------------------------
    b2_1 = add_node(
        "<b>2.1 Small Scale (Microscale &amp; Short-Term)</b><br/>"
        "• Spatial: &lt; 2 km (boundary layer turbulence, dust devils)<br/>"
        "• Temporal: 0–72 h nowcasting &amp; airport runway alert (KKIA)",
        x_coords[1], y_base, w_card, h_card, c_scale_sm
    )
    b2_2 = add_node(
        "<b>2.2 Medium Scale (Mesoscale &amp; Extended)</b><br/>"
        "• Spatial: 2–2,000 km (convective Haboob dust walls)<br/>"
        "• Temporal: <b>3–15 days (Sub-seasonal) — Core Innovation!</b>",
        x_coords[1], y_base + y_step, w_card, h_card, c_scale_md
    )
    b2_3 = add_node(
        "<b>2.3 Large Scale (Synoptic &amp; Seasonal)</b><br/>"
        "• Spatial: &gt; 2,000 km (prolonged regional Shamal regimes)<br/>"
        "• Temporal: &gt; 15–90+ days (teleconnections: ENSO, NAO, AO)",
        x_coords[1], y_base + y_step*2, w_card, h_card, c_scale_lg
    )
    b2_4 = add_node(
        "<b>2.4 5-Tier Hazard Classification</b><br/>"
        "• Level 1 (Normal) &rarr; Level 3 (Blowing sand: 150–500 ug/m³)<br/>"
        "• Level 4–5 (Severe blackout Haboob: &gt;2,000–5,000+ ug/m³)",
        x_coords[1], y_base + y_step*3, w_card, h_card, c_scale_md
    )

    add_edge(h2, b2_1, e_scale)
    add_edge(b2_1, b2_2, e_scale)
    add_edge(b2_2, b2_3, e_scale)
    add_edge(b2_3, b2_4, e_scale)

    # ----------------------------------------------------
    # BRANCH 3: MACHINE LEARNING (LINE A)
    # ----------------------------------------------------
    b3_1 = add_node(
        "<b>3.1 Classical ML (Literature Cited)</b><br/>"
        "• Artificial Neural Networks (ANN / Multi-Layer Perceptrons)<br/>"
        "• Support Vector Machines (SVM) with 500 hPa potential fields",
        x_coords[2], y_base, w_card, h_card, c_ml
    )
    b3_2 = add_node(
        "<b>3.2 GBDT Tree Ensembles</b><br/>"
        "• LightGBM (fast leaf-wise histogram splits)<br/>"
        "• CatBoost (ordered boosting) &amp; XGBoost regularized trees",
        x_coords[2], y_base + y_step, w_card, h_card, c_ml
    )
    b3_3 = add_node(
        "<b>3.3 Imbalance &amp; Cost-Sensitive Learning</b><br/>"
        "• SMOTE minority oversampling for &lt;3% rare storm days<br/>"
        "• Focal Loss down-weighting easy normal weather samples",
        x_coords[2], y_base + y_step*2, w_card, h_card, c_ml_hl
    )
    b3_4 = add_node(
        "<b>3.4 NWP Bias Correction &amp; Quantiles</b><br/>"
        "• Residual learning: y_true = NWP + f_GBDT(X_features)<br/>"
        "• Pinball loss uncertainty envelopes: P10, P50, P90",
        x_coords[2], y_base + y_step*3, w_card, h_card, c_ml
    )
    b3_5 = add_node(
        "<b>3.5 Explainable AI (Tree SHAP)</b><br/>"
        "• Exact game-theoretic Shapley feature attribution<br/>"
        "• Identifies friction velocity vs soil moisture thresholds",
        x_coords[2], y_base + y_step*4, w_card, h_card, c_ml
    )

    add_edge(h3, b3_1, e_ml)
    add_edge(b3_1, b3_2, e_ml)
    add_edge(b3_2, b3_3, e_ml)
    add_edge(b3_3, b3_4, e_ml)
    add_edge(b3_4, b3_5, e_ml)

    # ----------------------------------------------------
    # BRANCH 4: DEEP LEARNING (LINE B - LSTM, TRANSFORMER, GNN)
    # ----------------------------------------------------
    b4_1 = add_node(
        "<b>4.1 Long Short-Term Memory (LSTM)</b><br/>"
        "• Recurrent temporal gating for dust sequence memory<br/>"
        "• Bi-directional GRU/LSTM with temporal attention weights",
        x_coords[3], y_base, w_card, h_card, c_dl
    )
    b4_2 = add_node(
        "<b>4.2 Transformer &amp; Self-Attention Models</b><br/>"
        "• Multi-head self-attention for sub-seasonal dependencies<br/>"
        "• Captures long-range teleconnection wave propagations",
        x_coords[3], y_base + y_step, w_card, h_card, c_dl
    )
    b4_3 = add_node(
        "<b>4.3 Graph Neural Networks (GNN / ST-GNN)</b><br/>"
        "• 14-Node directional transport corridor topology<br/>"
        "• Asymmetric Chebyshev graph convolutions (Ad-Dahna &rarr; Riyadh)",
        x_coords[3], y_base + y_step*2, w_card, h_card, c_dl_pinn
    )
    b4_4 = add_node(
        "<b>4.4 Computer Vision &amp; Satellite AI (CNN)</b><br/>"
        "• 2D/3D CNNs extracting vortex features from tensor fields<br/>"
        "• Transfer learning fine-tuning on FengYun FY-4 &amp; MODIS AOD",
        x_coords[3], y_base + y_step*3, w_card, h_card, c_dl
    )
    b4_5 = add_node(
        "<b>4.5 Coupled Large Foundation AI Backbone</b><br/>"
        "• Coupled AI-GAMFS 5km grid with twice-daily updates<br/>"
        "• 38%–74% error reduction over standard ECMWF/NASA",
        x_coords[3], y_base + y_step*4, w_card, h_card, c_dl
    )

    add_edge(h4, b4_1, e_dl)
    add_edge(b4_1, b4_2, e_dl)
    add_edge(b4_2, b4_3, e_dl)
    add_edge(b4_3, b4_4, e_dl)
    add_edge(b4_4, b4_5, e_dl)

    # ----------------------------------------------------
    # BRANCH 5: WHAT SHE USES (TRI-PILLAR RESEARCH ARCHITECTURE)
    # ----------------------------------------------------
    b5_1 = add_node(
        "<b>5.1 Pillar 1: AI (LSTM + Transformer + GNN)</b><br/>"
        "• Line A GBDT ensembles + Line B LSTM, Transformer &amp; GNN<br/>"
        "• Extended 3–15 days forecast with P10/P50/P90 confidence",
        x_coords[4], y_base, w_card, h_card, c_tri
    )
    b5_2 = add_node(
        "<b>5.2 Pillar 2: Spatial Geography &amp; GIS</b><br/>"
        "• Ordinary Kriging spatial exposure &amp; hazard mapping<br/>"
        "• Moran's I &amp; LISA high-high hotspot cluster detection",
        x_coords[4], y_base + y_step, w_card, h_card, c_tri
    )
    b5_3 = add_node(
        "<b>5.3 Pillar 3: Socioeconomic Behavioral Science</b><br/>"
        "• IBM SPSS: Little's MCAR missing test &amp; EFA factor screening<br/>"
        "• IBM AMOS: Confirmatory Factor Analysis &amp; PADM SEM compliance",
        x_coords[4], y_base + y_step*2, w_card, h_card, c_tri
    )
    b5_4 = add_node(
        "<b>5.4 Municipal Crisis Early Warning Playbook</b><br/>"
        "• 4-Tier matrix: T-15d (Sub-seasonal) &rarr; T-5d &rarr; T-24h &rarr; T-0h<br/>"
        "• Action playbooks: Airport delays, road wetting, hospital alerts",
        x_coords[4], y_base + y_step*3, w_card, h_card, c_tri
    )

    add_edge(h5, b5_1, e_tri)
    add_edge(b5_1, b5_2, e_tri)
    add_edge(b5_2, b5_3, e_tri)
    add_edge(b5_3, b5_4, e_tri)

    # ----------------------------------------------------
    # SITEMAP SUMMARY FOOTER
    # ----------------------------------------------------
    footer = add_node(
        "<b>Paradigm Evolution:</b> Traditional NWP (Chaotic 72h Barrier) &rarr; "
        "Line A GBDT Bias Correction &rarr; "
        "Line B Deep AI (LSTM Sequences + Transformer Attention + Corridor GNN) &rarr; "
        "Tri-Pillar Early Warning Delivery (Spatial GIS + Socioeconomic PADM Action)",
        50, 680, 1960, 42, footer_style
    )

    return ET.tostring(mxfile, encoding="utf-8")

xml_data = build_simple_sitemap_drawio()

# Validate IDs
tree = ET.fromstring(xml_data)
all_ids = [elem.get("id") for elem in tree.iter("mxCell") if elem.get("id") is not None]
duplicates = set([x for x in all_ids if all_ids.count(x) > 1])
if duplicates:
    raise ValueError(f"DUPLICATE IDs: {duplicates}")

print(f"Validation: {len(all_ids)} IDs are strictly unique (0 to {max(map(int, all_ids))})")

for path in [
    "c:/Users/hp/Desktop/sandstorm_forecasting/sandstorm_forecasting_taxonomy.drawio",
    "c:/Users/hp/Desktop/sandstorm_forecasting/Digrams/sandstorm_forecasting_taxonomy.drawio",
    "c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Supervisor/sandstorm_forecasting_taxonomy.drawio"
]:
    with open(path, "wb") as f:
        f.write(xml_data)
    print(f"Updated clean sitemap at: {path}")
