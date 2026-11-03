import xml.etree.ElementTree as ET
import html

def build_drawio_xml():
    # Root drawio mxfile
    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-24T13:30:00.000Z", agent="Antigravity", version="24.0.0", type="device")
    diagram = ET.SubElement(mxfile, "diagram", id="sandstorm-forecasting-taxonomy", name="SDS_Forecasting_Taxonomy")
    model = ET.SubElement(diagram, "mxGraphModel", dx="2400", dy="1600", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="2800", pageHeight="2100", math="1", shadow="1")
    root = ET.SubElement(model, "root")

    # Base cells required by Draw.io / mxGraph
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

    def add_edge(source_id, target_id, style, label="", points=None):
        cid = next_id()
        cell = ET.SubElement(root, "mxCell", id=cid, value=label, style=style, edge="1", parent="1", source=source_id, target=target_id)
        mxGeo = ET.SubElement(cell, "mxGeometry", relative="1")
        mxGeo.set("as", "geometry")
        if points:
            arr = ET.SubElement(mxGeo, "Array")
            arr.set("as", "points")
            for px, py in points:
                pt = ET.SubElement(arr, "mxPoint", x=str(px), y=str(py))
        return cid

    # ----------------------------------------------------
    # STYLES DEFINITION
    # ----------------------------------------------------
    # Banner
    header_style = "html=1;whiteSpace=wrap;fillColor=#0F172A;strokeColor=#334155;strokeWidth=2;fontColor=#FFFFFF;rounded=1;shadow=1;"
    legend_badge_trad = "html=1;whiteSpace=wrap;fillColor=#6B21A8;strokeColor=#9333EA;fontColor=#FFFFFF;fontStyle=1;rounded=1;arcSize=20;fontSize=12;"
    legend_badge_ml = "html=1;whiteSpace=wrap;fillColor=#0284C7;strokeColor=#38BDF8;fontColor=#FFFFFF;fontStyle=1;rounded=1;arcSize=20;fontSize=12;"
    legend_badge_dl = "html=1;whiteSpace=wrap;fillColor=#4F46E5;strokeColor=#818CF8;fontColor=#FFFFFF;fontStyle=1;rounded=1;arcSize=20;fontSize=12;"
    legend_badge_tri = "html=1;whiteSpace=wrap;fillColor=#0F766E;strokeColor=#2DD4BF;fontColor=#FFFFFF;fontStyle=1;rounded=1;arcSize=20;fontSize=12;"

    # Column Containers (Swimlanes / Parent cards)
    col_trad_bg = "html=1;whiteSpace=wrap;fillColor=#FAF5FF;strokeColor=#A855F7;strokeWidth=3;fontColor=#581C87;rounded=1;shadow=1;verticalAlign=top;fontStyle=1;fontSize=16;"
    col_ml_bg   = "html=1;whiteSpace=wrap;fillColor=#F0F9FF;strokeColor=#0284C7;strokeWidth=3;fontColor=#0369A1;rounded=1;shadow=1;verticalAlign=top;fontStyle=1;fontSize=16;"
    col_dl_bg   = "html=1;whiteSpace=wrap;fillColor=#EEF2FF;strokeColor=#6366F1;strokeWidth=3;fontColor=#3730A3;rounded=1;shadow=1;verticalAlign=top;fontStyle=1;fontSize=16;"
    bottom_bg   = "html=1;whiteSpace=wrap;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=2.5;fontColor=#0F172A;rounded=1;shadow=1;verticalAlign=top;fontStyle=1;fontSize=15;"

    # Content Cards inside Columns
    card_trad = "html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#C084FC;strokeWidth=1.5;fontColor=#3B0764;rounded=1;arcSize=10;shadow=1;align=left;spacingLeft=12;spacingRight=12;spacingTop=8;spacingBottom=8;fontSize=12;"
    card_trad_warn = "html=1;whiteSpace=wrap;fillColor=#FEF2F2;strokeColor=#EF4444;strokeWidth=2;fontColor=#991B1B;rounded=1;arcSize=10;shadow=1;align=left;spacingLeft=12;spacingRight=12;spacingTop=8;spacingBottom=8;fontSize=12;"
    
    card_ml   = "html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#38BDF8;strokeWidth=1.5;fontColor=#0C4A6E;rounded=1;arcSize=10;shadow=1;align=left;spacingLeft=12;spacingRight=12;spacingTop=8;spacingBottom=8;fontSize=12;"
    card_ml_hl= "html=1;whiteSpace=wrap;fillColor=#F0FDFA;strokeColor=#14B8A6;strokeWidth=2;fontColor=#134E4A;rounded=1;arcSize=10;shadow=1;align=left;spacingLeft=12;spacingRight=12;spacingTop=8;spacingBottom=8;fontSize=12;"

    card_dl   = "html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor=#818CF8;strokeWidth=1.5;fontColor=#1E1B4B;rounded=1;arcSize=10;shadow=1;align=left;spacingLeft=12;spacingRight=12;spacingTop=8;spacingBottom=8;fontSize=12;"
    card_dl_pinn = "html=1;whiteSpace=wrap;fillColor=#FAF5FF;strokeColor=#9333EA;strokeWidth=2.5;fontColor=#3B0764;rounded=1;arcSize=10;shadow=1;align=left;spacingLeft=12;spacingRight=12;spacingTop=8;spacingBottom=8;fontSize=12;"

    # Multi-Scale Badges
    scale_small_style = "html=1;whiteSpace=wrap;fillColor=#ECFDF5;strokeColor=#10B981;strokeWidth=1.5;fontColor=#064E3B;rounded=1;shadow=1;fontSize=11;align=left;spacingLeft=8;"
    scale_med_style   = "html=1;whiteSpace=wrap;fillColor=#FFFBEB;strokeColor=#F59E0B;strokeWidth=1.5;fontColor=#78350F;rounded=1;shadow=1;fontSize=11;align=left;spacingLeft=8;"
    scale_large_style = "html=1;whiteSpace=wrap;fillColor=#FEF2F2;strokeColor=#EF4444;strokeWidth=1.5;fontColor=#7F1D1D;rounded=1;shadow=1;fontSize=11;align=left;spacingLeft=8;"

    # Connectors
    edge_evol_style = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#6366F1;strokeWidth=3;endArrow=classic;endFill=1;dashed=1;"
    edge_accent_style = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0284C7;strokeWidth=2.5;endArrow=classic;endFill=1;"

    # ----------------------------------------------------
    # 1. HEADER BANNER & LEGEND
    # ----------------------------------------------------
    title_html = (
        "&lt;div align='center'&gt;"
        "&lt;span style='font-size:24px; font-weight:800; letter-spacing:1px; color:#F8FAFC;'&gt;"
        "🌪️ TAXONOMY OF SAND &amp; DUST STORM (SDS) FORECASTING METHODOLOGIES&lt;/span&gt;&lt;br/&gt;"
        "&lt;span style='font-size:14px; color:#94A3B8; font-weight:500;'&gt;"
        "Comprehensive Hierarchy of All Forecasting Paradigms Mentioned in Research Proposal &amp; Literature Review&lt;/span&gt;&lt;br/&gt;"
        "&lt;span style='font-size:12px; color:#38BDF8; font-weight:600;'&gt;"
        "Focus: Medium- to Long-Term Forecasting in Saudi Arabia (Riyadh) • USTB Environmental Engineering Suite&lt;/span&gt;"
        "&lt;/div&gt;"
    )
    add_node(title_html, 60, 40, 2680, 90, header_style)

    # Badges row
    add_node("&lt;b&gt;🟣 TRADITIONAL METHODS&lt;/b&gt;&lt;br/&gt;Synoptic, Empirical &amp;amp; NWP", 160, 145, 380, 40, legend_badge_trad)
    add_node("&lt;b&gt;🔵 MACHINE LEARNING&lt;/b&gt;&lt;br/&gt;GBDT Ensembles &amp;amp; Bias Correction", 740, 145, 420, 40, legend_badge_ml)
    add_node("&lt;b&gt;🔮 DEEP LEARNING &amp;amp; PINN&lt;/b&gt;&lt;br/&gt;AI-GAMFS, ST-GNN &amp;amp; Physical PDEs", 1360, 145, 440, 40, legend_badge_dl)
    add_node("&lt;b&gt;🩵 TRI-PILLAR INTEGRATION&lt;/b&gt;&lt;br/&gt;GIS Kriging + SPSS/AMOS PADM SEM", 2000, 145, 440, 40, legend_badge_tri)

    # ----------------------------------------------------
    # 2. COLUMN 1: TRADITIONAL FORECASTING METHODS
    # ----------------------------------------------------
    col1_title = "&lt;b style='font-size:18px; color:#581C87;'&gt;🟣 1. TRADITIONAL FORECASTING METHODS&lt;/b&gt;&lt;br/&gt;&lt;span style='font-size:12px; color:#7E22CE; font-weight:normal;'&gt;Physical Mechanics, Numerical Weather Prediction &amp;amp; Synoptic Analysis&lt;/span&gt;"
    col1_id = add_node(col1_title, 60, 210, 840, 1260, col_trad_bg)

    c1_1_text = (
        "&lt;b style='font-size:14px; color:#6B21A8;'&gt;1.1 Subjective Synoptic Meteorology&lt;/b&gt;&lt;hr style='border:0.5px solid #C084FC; margin:4px 0;'&gt;"
        "• &lt;b&gt;Manual Surface Weather Maps:&lt;/b&gt; Manual tracing of isobaric surface contours and thermal front boundaries.&lt;br/&gt;"
        "• &lt;b&gt;Upper-Air Potential Fields:&lt;/b&gt; 500 hPa geopotential height troughs, 700 hPa steering currents, and 850 hPa wind convergence.&lt;br/&gt;"
        "• &lt;b&gt;Pressure Gradient Rules:&lt;/b&gt; Surface pressure differences across northern deserts driving Shamal winds (&amp;Delta;P &amp;gt; 4–6 hPa).&lt;br/&gt;"
        "• &lt;b&gt;Forecaster Heuristics:&lt;/b&gt; Subjective qualitative judgment relying on individual meteorologist experience."
    )
    add_node(c1_1_text, 85, 270, 790, 150, card_trad)

    c1_2_text = (
        "&lt;b style='font-size:14px; color:#6B21A8;'&gt;1.2 Classical Empirical &amp;amp; Statistical Formulations&lt;/b&gt;&lt;hr style='border:0.5px solid #C084FC; margin:4px 0;'&gt;"
        "• &lt;b&gt;Persistence &amp;amp; Climatology:&lt;/b&gt; Baseline assuming tomorrow's dust equals today or 30-year seasonal averages.&lt;br/&gt;"
        "• &lt;b&gt;Linear Time Series:&lt;/b&gt; Autoregressive Integrated Moving Average (ARIMA) &amp;amp; Multiple Linear Regression (MLR).&lt;br/&gt;"
        "• &lt;b&gt;Bagnold (1941) Sand Transport Law:&lt;/b&gt; Sand transport flux scaling with friction velocity: &lt;i&gt;q = C &amp;middot; (&amp;rho;/g) &amp;middot; u_*&lt;sup&gt;3&lt;/sup&gt;&lt;/i&gt;&lt;br/&gt;"
        "• &lt;b&gt;Owen (1964) Saltation Threshold:&lt;/b&gt; Aerodynamic gate: &lt;i&gt;F&lt;sub&gt;salt&lt;/sub&gt; &amp;prop; u_*&lt;sup&gt;3&lt;/sup&gt; (1 - u_*t&lt;sup&gt;2&lt;/sup&gt;/u_*&lt;sup&gt;2&lt;/sup&gt;) &amp;middot; &amp;Iopf;(u_* &amp;gt; u_*t)&lt;/i&gt;&lt;br/&gt;"
        "• &lt;b&gt;Gillette (1979) Formulation:&lt;/b&gt; Critical threshold &lt;i&gt;u_*t&lt;/i&gt; modulated by damp soil moisture bridging &lt;i&gt;f(w&lt;sub&gt;s&lt;/sub&gt;)&lt;/i&gt; and surface roughness &lt;i&gt;z&lt;sub&gt;0&lt;/sub&gt;&lt;/i&gt;."
    )
    add_node(c1_2_text, 85, 440, 790, 200, card_trad)

    c1_3_text = (
        "&lt;b style='font-size:14px; color:#6B21A8;'&gt;1.3 Dynamical NWP &amp;amp; Chemistry-Transport Models (CTMs)&lt;/b&gt;&lt;hr style='border:0.5px solid #C084FC; margin:4px 0;'&gt;"
        "• &lt;b&gt;Global Meteorological Models:&lt;/b&gt; ECMWF IFS (Integrated Forecast System), CMA-GFS, GFS/NCEP.&lt;br/&gt;"
        "• &lt;b&gt;Atmospheric Chemistry-Transport Models:&lt;/b&gt; WRF-Chem, DREAM8b, NASA GEOS-Chem, Copernicus CAMS.&lt;br/&gt;"
        "• &lt;b&gt;Navier-Stokes Hydrodynamic PDEs:&lt;/b&gt; Solves momentum, continuity, and thermodynamic fluid equations on grid cells.&lt;br/&gt;"
        "• &lt;b&gt;Aerosol Advection-Diffusion PDE:&lt;/b&gt;&lt;br/&gt;"
        "&amp;nbsp;&amp;nbsp;&lt;i&gt;&amp;part;C/&amp;part;t + &amp;nabla;&amp;middot;(uC) = &amp;nabla;&amp;middot;(K&amp;nabla;C) + S&lt;sub&gt;emission&lt;/sub&gt; - v&lt;sub&gt;d&lt;/sub&gt;C - &amp;Lambda;&lt;sub&gt;scav&lt;/sub&gt;P&lt;sub&gt;rain&lt;/sub&gt;C&lt;/i&gt;&lt;br/&gt;"
        "• &lt;b&gt;Dust Scheme Parameterization:&lt;/b&gt; Empirical sub-grid assumptions for erodible fraction and particle size distribution."
    )
    add_node(c1_3_text, 85, 660, 790, 220, card_trad)

    c1_4_text = (
        "&lt;b style='font-size:14px; color:#B91C1C;'&gt;⚠️ Traditional Operational Bottlenecks &amp;amp; Failure Modes&lt;/b&gt;&lt;hr style='border:0.5px solid #EF4444; margin:4px 0;'&gt;"
        "• &lt;b&gt;The Chaotic Lyapunov Horizon (T&lt;sub&gt;Lyap&lt;/sub&gt; &amp;asymp; 72 h):&lt;/b&gt; Lorenzian error growth diverges exponentially beyond Day 3, causing extended 3–15d predictions to collapse.&lt;br/&gt;"
        "• &lt;b&gt;Sub-Grid Orographic Smoothing:&lt;/b&gt; Coarse grids (9–25 km) fail to resolve narrow canyon channeling, Wadi Hanifa, or Jabal Tuwaiq escarpments.&lt;br/&gt;"
        "• &lt;b&gt;Failure on Convective Haboobs:&lt;/b&gt; Inability to simulate violent cold-pool thunderstorm downdraft walls.&lt;br/&gt;"
        "• &lt;b&gt;Prohibitive HPC Computational Cost:&lt;/b&gt; High-resolution global CTM runs take hours on supercomputers, preventing rapid real-time emergency cycles."
    )
    add_node(c1_4_text, 85, 900, 790, 200, card_trad_warn)

    c1_5_text = (
        "&lt;b style='font-size:13px; color:#581C87;'&gt;📌 Summary of Traditional Operational Usage:&lt;/b&gt;&lt;br/&gt;"
        "Provides foundational physical understanding, but operates as a rigid, computationally heavy silo. Generates high false-alarm rates for sudden convective spikes and exhibits large extended-range systematic biases (&amp;plusmn;85 &amp;mu;g/m&amp;sup3;)."
    )
    add_node(c1_5_text, 85, 1120, 790, 90, card_trad)

    # ----------------------------------------------------
    # 3. COLUMN 2: MACHINE LEARNING FORECASTING METHODS
    # ----------------------------------------------------
    col2_title = "&lt;b style='font-size:18px; color:#0369A1;'&gt;🔵 2. MACHINE LEARNING FORECASTING METHODS&lt;/b&gt;&lt;br/&gt;&lt;span style='font-size:12px; color:#0284C7; font-weight:normal;'&gt;Statistical AI, Tree Ensembles, Post-Processing &amp;amp; Uncertainty Quantification&lt;/span&gt;"
    col2_id = add_node(col2_title, 930, 210, 880, 1260, col_ml_bg)

    c2_1_text = (
        "&lt;b style='font-size:14px; color:#0369A1;'&gt;2.1 Early &amp;amp; Foundational Machine Learning (Literature Cited)&lt;/b&gt;&lt;hr style='border:0.5px solid #38BDF8; margin:4px 0;'&gt;"
        "• &lt;b&gt;Artificial Neural Networks (ANN):&lt;/b&gt; Multi-layer perceptrons with stepwise linear regression feature screening (Huang et al., 2000).&lt;br/&gt;"
        "• &lt;b&gt;Support Vector Machines (SVM / SVR):&lt;/b&gt; Incorporating 500 hPa potential fields &amp;amp; wind vectors (Lu et al., 2010; Luo &amp;amp; Duan, 2023).&lt;br/&gt;"
        "• &lt;b&gt;Fuzzy &amp;amp; Radial Basis Models:&lt;/b&gt; ANFIS and RBF neural networks for regional dust activity trends (Mahmoudi et al., 2021).&lt;br/&gt;"
        "• &lt;b&gt;Hybrid Expert Systems:&lt;/b&gt; Bayesian networks combined with Case-Based Reasoning (CBR) (Al Murayziq et al., 2022)."
    )
    add_node(c2_1_text, 955, 270, 830, 150, card_ml)

    c2_2_text = (
        "&lt;b style='font-size:14px; color:#0369A1;'&gt;2.2 Gradient Boosting Decision Tree (GBDT) Ensembles&lt;/b&gt;&lt;hr style='border:0.5px solid #38BDF8; margin:4px 0;'&gt;"
        "• &lt;b&gt;Random Forests (RF / Balanced RF):&lt;/b&gt; Ensemble bagging for non-linear meteorological interaction &amp;amp; radar precipitation bias correction (Mahavik, 2025).&lt;br/&gt;"
        "• &lt;b&gt;Extreme Gradient Boosting (XGBoost):&lt;/b&gt; Depth-wise regularized trees for planetary boundary layer height &amp;amp; extreme wind (Bai Jiayi, 2025).&lt;br/&gt;"
        "• &lt;b&gt;LightGBM:&lt;/b&gt; Leaf-wise histogram-based fast split, handling large-scale continuous atmospheric grids (Liao Wenxi, 2025; Brandt, 2024).&lt;br/&gt;"
        "• &lt;b&gt;CatBoost:&lt;/b&gt; Ordered target statistics natively encoding categorical station locations, soil types, and wind sectors without data leakage.&lt;br/&gt;"
        "• &lt;b&gt;Automated ML Frameworks:&lt;/b&gt; AutoGluon &amp;amp; AutoFeat-TPOT automated feature synthesis pipelines (Song Hongkai, 2024)."
    )
    add_node(c2_2_text, 955, 440, 830, 190, card_ml)

    c2_3_text = (
        "&lt;b style='font-size:14px; color:#0F766E;'&gt;2.3 Class Imbalance &amp;amp; Rare Event Optimization (Key Thesis Innovation)&lt;/b&gt;&lt;hr style='border:0.5px solid #2DD4BF; margin:4px 0;'&gt;"
        "• &lt;b&gt;The Challenge:&lt;/b&gt; Severe sandstorms represent &amp;lt;3% of annual observations, causing standard ML models to suffer from negative class bias.&lt;br/&gt;"
        "• &lt;b&gt;SMOTE &amp;amp; Hybrid Sampling:&lt;/b&gt; Synthetic minority over-sampling and adaptive targeted sampling (Xie, 2011; Zhang et al., 2015).&lt;br/&gt;"
        "• &lt;b&gt;Cost-Sensitive Loss Formulation:&lt;/b&gt; Heavy penalty matrix for false negatives (missed alarms cost 10&amp;times; false alarms).&lt;br/&gt;"
        "• &lt;b&gt;Focal Loss:&lt;/b&gt; Dynamically down-weights easy normal weather examples: &lt;i&gt;L&lt;sub&gt;focal&lt;/sub&gt; = -&amp;alpha;&lt;sub&gt;t&lt;/sub&gt; (1 - p&lt;sub&gt;t&lt;/sub&gt;)&lt;sup&gt;&amp;gamma;&lt;/sup&gt; log(p&lt;sub&gt;t&lt;/sub&gt;)&lt;/i&gt;."
    )
    add_node(c2_3_text, 955, 650, 830, 170, card_ml_hl)

    c2_4_text = (
        "&lt;b style='font-size:14px; color:#0369A1;'&gt;2.4 NWP Post-Processing &amp;amp; Quantile Uncertainty (Main Line A)&lt;/b&gt;&lt;hr style='border:0.5px solid #38BDF8; margin:4px 0;'&gt;"
        "• &lt;b&gt;Statistical Bias Correction:&lt;/b&gt; Correcting systematic ECMWF/CAMS drift via residual learning: &lt;i&gt;y&lt;sub&gt;true&lt;/sub&gt; = NWP + f&lt;sub&gt;ML&lt;/sub&gt;(X&lt;sub&gt;env&lt;/sub&gt;)&lt;/i&gt;.&lt;br/&gt;"
        "• &lt;b&gt;Quantile Regression (Pinball Loss):&lt;/b&gt;&lt;br/&gt;"
        "&amp;nbsp;&amp;nbsp;&lt;i&gt;&amp;Lscr;&lt;sub&gt;&amp;tau;&lt;/sub&gt;(y, &amp;ycirc;) = max(&amp;tau;(y - &amp;ycirc;), (&amp;tau; - 1)(y - &amp;ycirc;))&lt;/i&gt;&lt;br/&gt;"
        "• &lt;b&gt;Calibrated Prediction Envelopes:&lt;/b&gt; P10 (optimistic lower bound), P50 (deterministic median), P90 (upper risk-averse threshold).&lt;br/&gt;"
        "• &lt;b&gt;EALSTM-QR Intervals:&lt;/b&gt; Extended prediction intervals guaranteeing non-crossing monotonicity (Liu Fangjie, 2022)."
    )
    add_node(c2_4_text, 955, 840, 830, 180, card_ml)

    c2_5_text = (
        "&lt;b style='font-size:14px; color:#0369A1;'&gt;2.5 Explainable AI (XAI) &amp;amp; Tree SHAP Diagnostics&lt;/b&gt;&lt;hr style='border:0.5px solid #38BDF8; margin:4px 0;'&gt;"
        "• &lt;b&gt;Tree SHAP (SHapley Additive exPlanations):&lt;/b&gt; Game-theoretic feature attribution identifying why a storm was predicted.&lt;br/&gt;"
        "• &lt;b&gt;Physical Attribution:&lt;/b&gt; Quantifying the transition where 10m wind velocity crosses 8.5 m/s, coupled with soil moisture &amp;lt;0.08 m&amp;sup3;/m&amp;sup3;."
    )
    add_node(c2_5_text, 955, 1040, 830, 120, card_ml)

    c2_6_text = (
        "&lt;b style='font-size:13px; color:#0369A1;'&gt;📌 Summary of What She Uses in Line A:&lt;/b&gt;&lt;br/&gt;"
        "LightGBM + CatBoost + XGBoost Ensemble &amp;rarr; Calibrated Quantiles (P10/P50/P90) &amp;rarr; 5-Tier Hazard Classifier &amp;rarr; Tree SHAP."
    )
    add_node(c2_6_text, 955, 1180, 830, 70, card_ml)

    # ----------------------------------------------------
    # 4. COLUMN 3: DEEP LEARNING & PHYSICS-INFORMED AI
    # ----------------------------------------------------
    col3_title = "&lt;b style='font-size:18px; color:#3730A3;'&gt;🔮 3. DEEP LEARNING &amp;amp; PHYSICS-INFORMED AI&lt;/b&gt;&lt;br/&gt;&lt;span style='font-size:12px; color:#4F46E5; font-weight:normal;'&gt;Spatiotemporal Foundation Models, Corridor Graphs &amp;amp; Governing PDEs&lt;/span&gt;"
    col3_id = add_node(col3_title, 1840, 210, 900, 1260, col_dl_bg)

    c3_1_text = (
        "&lt;b style='font-size:14px; color:#3730A3;'&gt;3.1 Deep Spatiotemporal Sequence Models&lt;/b&gt;&lt;hr style='border:0.5px solid #818CF8; margin:4px 0;'&gt;"
        "• &lt;b&gt;Recurrent Architectures:&lt;/b&gt; Long Short-Term Memory (LSTM), Bi-directional GRU with temporal attention mechanisms.&lt;br/&gt;"
        "• &lt;b&gt;PredRNN (Wang et al., 2017):&lt;/b&gt; Spatiotemporal LSTM memory decoupling zigzag memories for non-stationary dust plume fronts.&lt;br/&gt;"
        "• &lt;b&gt;Spatiotemporal Transformers:&lt;/b&gt; Multi-head self-attention models (Earthformer) capturing sub-seasonal teleconnection waves."
    )
    add_node(c3_1_text, 1865, 270, 850, 140, card_dl)

    c3_2_text = (
        "&lt;b style='font-size:14px; color:#3730A3;'&gt;3.2 Computer Vision &amp;amp; Satellite Remote Sensing AI&lt;/b&gt;&lt;hr style='border:0.5px solid #818CF8; margin:4px 0;'&gt;"
        "• &lt;b&gt;Convolutional Neural Networks (CNN):&lt;/b&gt; Extracting 2D/3D spatial vortex representations from gridded atmospheric tensors.&lt;br/&gt;"
        "• &lt;b&gt;Feature Pyramid Networks (FPN):&lt;/b&gt; Multi-scale segmentation isolating dust plume minimum bounding rectangles (Harba et al., 2021).&lt;br/&gt;"
        "• &lt;b&gt;Transfer Learning &amp;amp; Foundation Tuning:&lt;/b&gt; Pre-trained weights fine-tuned on FengYun FY-4A/B &amp;amp; MODIS Deep Blue AOD (Ren et al., 2022)."
    )
    add_node(c3_2_text, 1865, 430, 850, 140, card_dl)

    c3_3_text = (
        "&lt;b style='font-size:14px; color:#3730A3;'&gt;3.3 Hybrid Deep Architectures &amp;amp; Stacking&lt;/b&gt;&lt;hr style='border:0.5px solid #818CF8; margin:4px 0;'&gt;"
        "• &lt;b&gt;CNN-LSTM &amp;amp; ConvLSTM:&lt;/b&gt; Fuses spatial image feature representation with sequential temporal propagation.&lt;br/&gt;"
        "• &lt;b&gt;Stacking Meta-Ensembles:&lt;/b&gt; Stacking LSTM-CNN outputs into SVM/MLP meta-classifiers (Ren et al., 2024).&lt;br/&gt;"
        "• &lt;b&gt;INB-CNN Model:&lt;/b&gt; Integrated Naive Bayes (surface cover) + CNN (atmospheric circulation) (Li et al., 2020)."
    )
    add_node(c3_3_text, 1865, 590, 850, 130, card_dl)

    c3_4_text = (
        "&lt;b style='font-size:14px; color:#4F46E5;'&gt;3.4 Spatio-Temporal Graph Neural Networks (ST-GNN - Main Line B)&lt;/b&gt;&lt;hr style='border:0.5px solid #818CF8; margin:4px 0;'&gt;"
        "• &lt;b&gt;14-Node Corridor Transport Topology:&lt;/b&gt; Non-Euclidean graph modeling upwind-to-downwind advection corridors into Riyadh.&lt;br/&gt;"
        "• &lt;b&gt;3-Support Asymmetric Chebyshev Convolutions:&lt;/b&gt;&lt;br/&gt;"
        "&amp;nbsp;&amp;nbsp;&lt;i&gt;Z = &amp;sum; (T&lt;sub&gt;k&lt;/sub&gt;(&amp;Atilde;&lt;sub&gt;fwd&lt;/sub&gt;) X W&lt;sub&gt;k,1&lt;/sub&gt; + T&lt;sub&gt;k&lt;/sub&gt;(&amp;Atilde;&lt;sub&gt;rev&lt;/sub&gt;) X W&lt;sub&gt;k,2&lt;/sub&gt;)&lt;/i&gt;&lt;br/&gt;"
        "• &lt;b&gt;Physical Directionality:&lt;/b&gt; Upstream source nodes (An-Nafud, Ad-Dahna) dynamically transfer dust mass to downstream Riyadh nodes."
    )
    add_node(c3_4_text, 1865, 740, 850, 160, card_dl)

    c3_5_text = (
        "&lt;b style='font-size:14px; color:#7E22CE;'&gt;3.5 Large Meteorological Foundation Models (Global Frontiers)&lt;/b&gt;&lt;hr style='border:0.5px solid #C084FC; margin:4px 0;'&gt;"
        "• &lt;b&gt;Coupled AI-GAMFS Backbone:&lt;/b&gt; World's first aerosol-meteorology coupled AI large model (5km grid, twice-daily cycles, 38%–74% error reduction vs ECMWF/NASA; successfully predicted Sichuan 120h dust invasion).&lt;br/&gt;"
        "• &lt;b&gt;Google NeuralGCM (2024):&lt;/b&gt; Differentiable circulation solver blended with neural parameterized physics."
    )
    add_node(c3_5_text, 1865, 920, 850, 140, card_dl)

    c3_6_text = (
        "&lt;b style='font-size:14px; color:#6B21A8;'&gt;3.6 Physics-Informed Neural Networks (PINN - Core Innovation)&lt;/b&gt;&lt;hr style='border:0.5px solid #A855F7; margin:4px 0;'&gt;"
        "• &lt;b&gt;Eliminating AI Hallucinations:&lt;/b&gt; Pure deep learning generates unphysical sandstorms in calm air; PINN embeds physical differential operators into loss functions:&lt;br/&gt;"
        "&amp;nbsp;&amp;nbsp;&lt;b&gt;&amp;Lscr;&lt;sub&gt;PINN&lt;/sub&gt; = &amp;Lscr;&lt;sub&gt;data&lt;/sub&gt; + &amp;lambda;&lt;sub&gt;mass&lt;/sub&gt; &amp;Lscr;&lt;sub&gt;continuity&lt;/sub&gt; + &amp;lambda;&lt;sub&gt;salt&lt;/sub&gt; &amp;Lscr;&lt;sub&gt;Owen&lt;/sub&gt;&lt;/b&gt;&lt;br/&gt;"
        "• &lt;b&gt;Mass Conservation PDE Continuity:&lt;/b&gt; &lt;i&gt;&amp;part;C/&amp;part;t + &amp;nabla;&amp;middot;(uC) - K&amp;nabla;&amp;sup2;C + v&lt;sub&gt;d&lt;/sub&gt;C - S = 0&lt;/i&gt;&lt;br/&gt;"
        "• &lt;b&gt;Owen Saltation Gate:&lt;/b&gt; Emission strictly constrained to zero unless friction velocity exceeds critical threshold: &lt;i&gt;u_* &amp;gt; u_*t&lt;/i&gt;."
    )
    add_node(c3_6_text, 1865, 1080, 850, 170, card_dl_pinn)

    # ----------------------------------------------------
    # 5. BOTTOM SECTION: THE PARADIGM SHIFT & MULTI-SCALE
    # ----------------------------------------------------
    bot_title = "&lt;b style='font-size:16px; color:#0F172A;'&gt;⚖️ 4. THE PROPOSED PARADIGM SHIFT &amp;amp; MULTI-SCALE SYNTHESIS (WHAT SHE USES)&lt;/b&gt;"
    add_node(bot_title, 60, 1500, 2680, 520, bottom_bg)

    # Multi-Scale 3 Cards
    small_box = (
        "&lt;b style='font-size:13px; color:#064E3B;'&gt;🟢 SMALL SCALE (Microscale &amp;amp; Short-Term)&lt;/b&gt;&lt;hr style='border:0.5px solid #10B981; margin:3px 0;'&gt;"
        "• &lt;b&gt;Spatial:&lt;/b&gt; &amp;lt;2 km (Boundary layer shear, local Wadi Hanifa micro-canyons, local roughness z&lt;sub&gt;0&lt;/sub&gt;).&lt;br/&gt;"
        "• &lt;b&gt;Temporal:&lt;/b&gt; 0–72 h (Nowcasting &amp;amp; airport runway alert at KKIA).&lt;br/&gt;"
        "• &lt;b&gt;In Her Model:&lt;/b&gt; In-situ station telemetry downscaling, high-resolution SRTM 90m DEM elevation, and local soil moisture gating."
    )
    add_node(small_box, 90, 1550, 820, 130, scale_small_style)

    med_box = (
        "&lt;b style='font-size:13px; color:#78350F;'&gt;🟡 MEDIUM SCALE (Mesoscale &amp;amp; Extended 3–15d)&lt;/b&gt;&lt;hr style='border:0.5px solid #F59E0B; margin:3px 0;'&gt;"
        "• &lt;b&gt;Spatial:&lt;/b&gt; 2–2,000 km (Convective Haboob dust walls, Ad-Dahna / An-Nafud transport corridors).&lt;br/&gt;"
        "• &lt;b&gt;Temporal:&lt;/b&gt; 3–15 days (Sub-seasonal range — &lt;b&gt;The Primary Innovation Frontier!&lt;/b&gt;).&lt;br/&gt;"
        "• &lt;b&gt;In Her Model:&lt;/b&gt; Coupled AI-GAMFS 5km grid vision backbone + 14-Node Corridor ST-GNN + Municipal yellow advisory window."
    )
    add_node(med_box, 990, 1550, 820, 130, scale_med_style)

    large_box = (
        "&lt;b style='font-size:13px; color:#7F1D1D;'&gt;🔴 LARGE SCALE (Synoptic-Macro &amp;amp; Seasonal)&lt;/b&gt;&lt;hr style='border:0.5px solid #EF4444; margin:3px 0;'&gt;"
        "• &lt;b&gt;Spatial:&lt;/b&gt; &amp;gt;2,000 km (Regional Shamal winds, Siberian/Arabian anticyclones, transboundary Rub' al Khali plumes).&lt;br/&gt;"
        "• &lt;b&gt;Temporal:&lt;/b&gt; &amp;gt;15–90+ days (Seasonal drought memory, planetary teleconnections).&lt;br/&gt;"
        "• &lt;b&gt;In Her Model:&lt;/b&gt; Large-scale climate teleconnections (ENSO, NAO, AO, IOD) driving extended-range background conditions."
    )
    add_node(large_box, 1890, 1550, 820, 130, scale_large_style)

    # Tri-Pillar Box
    tri_pillar_box = (
        "&lt;div align='center'&gt;&lt;b style='font-size:14px; color:#0F766E;'&gt;🩵 DUSTML TRI-PILLAR RESEARCH ARCHITECTURE (THE COMPLETE THESIS INTEGRATION)&lt;/b&gt;&lt;/div&gt;&lt;hr style='border:0.5px solid #14B8A6; margin:4px 0;'&gt;"
        "&lt;table width='100%' style='font-size:11px;'&gt;"
        "&lt;tr&gt;"
        "&lt;td width='33%' valign='top'&gt;&lt;b style='color:#0284C7;'&gt;[PILLAR 1: METEOROLOGICAL AI &amp;amp; PINN]&lt;/b&gt;&lt;br/&gt;• Line A: GBDT (LightGBM/CatBoost/XGBoost) bias correction.&lt;br/&gt;• Line B: AI-GAMFS + ST-GNN + PINN Mass Continuity.&lt;br/&gt;• Quantile Envelopes (P10, P50, P90) &amp;amp; Tree SHAP XAI.&lt;/td&gt;"
        "&lt;td width='33%' valign='top'&gt;&lt;b style='color:#0F766E;'&gt;[PILLAR 2: SPATIAL RISK GEOGRAPHY (GIS)]&lt;/b&gt;&lt;br/&gt;• Ordinary Kriging spatial exposure &amp;amp; vulnerability mapping.&lt;br/&gt;• Global Moran's I &amp;amp; LISA local high-high risk clustering.&lt;br/&gt;• Geographically Weighted Regression (GWR) for terrain roughness.&lt;/td&gt;"
        "&lt;td width='34%' valign='top'&gt;&lt;b style='color:#7E22CE;'&gt;[PILLAR 3: SOCIOECONOMIC BEHAVIORAL SCIENCE]&lt;/b&gt;&lt;br/&gt;• SPSS: Little's MCAR, Mahalanobis D&amp;sup2; &amp;amp; Exploratory Factor Analysis.&lt;br/&gt;• AMOS: Confirmatory Factor Analysis (CR&amp;ge;0.70, AVE&amp;ge;0.50).&lt;br/&gt;• Protective Action Decision Model (PADM) SEM &amp;amp; 4-Tier Playbook.&lt;/td&gt;"
        "&lt;/tr&gt;"
        "&lt;/table&gt;"
    )
    add_node(tri_pillar_box, 90, 1710, 2620, 130, card_ml_hl)

    # Operational Evolution Flow (Connecting arrows)
    flow_step1 = add_node("&lt;b&gt;Traditional NWP (ECMWF / CAMS)&lt;/b&gt;&lt;br/&gt;Lyapunov Limit at Day 3", 160, 1870, 320, 60, legend_badge_trad)
    flow_step2 = add_node("&lt;b&gt;Line A: GBDT Bias Correction&lt;/b&gt;&lt;br/&gt;LightGBM/CatBoost + Quantiles", 780, 1870, 360, 60, legend_badge_ml)
    flow_step3 = add_node("&lt;b&gt;Line B: ST-GNN + PINN AI&lt;/b&gt;&lt;br/&gt;Advection Corridors &amp;amp; Mass PDE", 1440, 1870, 380, 60, legend_badge_dl)
    flow_step4 = add_node("&lt;b&gt;Tri-Pillar Early Warning Action&lt;/b&gt;&lt;br/&gt;GIS Exposure &amp;amp; Municipal PADM", 2120, 1870, 400, 60, legend_badge_tri)

    add_edge(flow_step1, flow_step2, edge_accent_style, "Post-Processing Bias Correction")
    add_edge(flow_step2, flow_step3, edge_evol_style, "Coupled Physics-AI Fusion")
    add_edge(flow_step3, flow_step4, edge_accent_style, "Decision Playbook Delivery")

    # Connect Columns at top to evolutionary flow
    add_edge(col1_id, flow_step1, edge_evol_style)
    add_edge(col2_id, flow_step2, edge_evol_style)
    add_edge(col3_id, flow_step3, edge_evol_style)

    # Format XML nicely
    xml_str = ET.tostring(mxfile, encoding="utf-8")
    return xml_str

xml_data = build_drawio_xml()
target_path = "c:/Users/hp/Desktop/sandstorm_forecasting/Digrams/sandstorm_forecasting_taxonomy.drawio"
with open(target_path, "wb") as f:
    f.write(xml_data)

target_path2 = "c:/Users/hp/Desktop/sandstorm_forecasting/sandstorm_forecasting_taxonomy.drawio"
with open(target_path2, "wb") as f:
    f.write(xml_data)

target_path3 = "c:/Users/hp/Desktop/sandstorm_forecasting/Planning/Supervisor/sandstorm_forecasting_taxonomy.drawio"
with open(target_path3, "wb") as f:
    f.write(xml_data)

# Validate all IDs are unique
tree = ET.fromstring(xml_data)
all_ids = [elem.get("id") for elem in tree.iter("mxCell") if elem.get("id") is not None]
duplicates = set([x for x in all_ids if all_ids.count(x) > 1])
if duplicates:
    raise ValueError(f"DUPLICATE IDs FOUND: {duplicates}")
print(f"Validation Passed: All {len(all_ids)} IDs are strictly unique! (IDs range from {min(map(int, all_ids))} to {max(map(int, all_ids))})")
