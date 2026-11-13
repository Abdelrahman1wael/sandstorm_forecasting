"""
Format the Master's Dissertation according to the University of Science and Technology Beijing (USTB)
School of Economics and Management (SEM) Master's Thesis Template & Formatting Standards
(https://sem.ustb.edu.cn/english/Download/index.htm):
  - A4 Paper (210 x 297 mm), Margins: Top 2.5cm, Bottom 2.5cm, Left 3.0cm (binding), Right 2.5cm
  - Typography: Times New Roman (English/Numbers) + SimSun/SimHei (Chinese), 12pt body, 1.5 line spacing
  - Front Matter (Roman page numbers): Cover Page, Title Page, Declaration of Originality & Authorization,
    English Abstract & Keywords, Chinese Abstract (摘要) & Keywords (关键词), Table of Contents, List of Figures
  - Main Body (Arabic page numbers restarting at 1, running header): Chapters 1-6 with unified Heading 1/2/3 hierarchy
  - Fixed duplicate section numbering in Chapter 3 (3.9, 3.10)
  - Back Matter: Numbered References, Acknowledgements, Author's Resume & Academic Achievements
"""

import shutil
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SRC_DOCX = PROJECT_ROOT / "Documentation" / "manuscripts" / "final" / "Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2).docx"
OUT_LATEST = PROJECT_ROOT / "final_project_copy" / "01_Documentation" / "Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2)_latest.docx"
OUT_FINAL_ORIG = PROJECT_ROOT / "final_project_copy" / "01_Documentation" / "Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2).docx"
OUT_MAIN_DOCX = PROJECT_ROOT / "Documentation" / "manuscripts" / "final" / "Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2)_latest.docx"
OUT_ENHANCED = PROJECT_ROOT / "Documentation" / "manuscripts" / "final" / "Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2)_enhanced.docx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
XML_NS = "http://www.w3.org/XML/1998/namespace"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

for prefix, uri in [
    ("w", W_NS), ("r", R_NS), ("wp", WP_NS), ("a", A_NS), ("pic", PIC_NS)
]:
    ET.register_namespace(prefix, uri)


def w_tag(name):
    return f"{{{W_NS}}}{name}"


def make_rPr(font_ascii="Times New Roman", font_ea="SimSun", sz=24, bold=False, italic=False, color=None):
    rPr = ET.Element(w_tag("rPr"))
    rFonts = ET.SubElement(rPr, w_tag("rFonts"))
    rFonts.set(w_tag("ascii"), font_ascii)
    rFonts.set(w_tag("hAnsi"), font_ascii)
    rFonts.set(w_tag("cs"), font_ascii)
    rFonts.set(w_tag("eastAsia"), font_ea)
    if bold:
        ET.SubElement(rPr, w_tag("b"))
    if italic:
        ET.SubElement(rPr, w_tag("i"))
    if color:
        c = ET.SubElement(rPr, w_tag("color"))
        c.set(w_tag("val"), color)
    s = ET.SubElement(rPr, w_tag("sz"))
    s.set(w_tag("val"), str(sz))
    scs = ET.SubElement(rPr, w_tag("szCs"))
    scs.set(w_tag("val"), str(sz))
    return rPr


def make_p(text="", style_id=None, bold=False, italic=False, sz=24, jc="both",
           space_before=0, space_after=120, line=360, line_rule="auto",
           font_ascii="Times New Roman", font_ea="SimSun", page_break_before=False,
           keep_next=False, color=None, first_line=0):
    p = ET.Element(w_tag("p"))
    pPr = ET.SubElement(p, w_tag("pPr"))
    if style_id:
        ps = ET.SubElement(pPr, w_tag("pStyle"))
        ps.set(w_tag("val"), str(style_id))
    if page_break_before:
        ET.SubElement(pPr, w_tag("pageBreakBefore"))
    if keep_next:
        ET.SubElement(pPr, w_tag("keepNext"))
    sp = ET.SubElement(pPr, w_tag("spacing"))
    sp.set(w_tag("before"), str(space_before))
    sp.set(w_tag("after"), str(space_after))
    sp.set(w_tag("line"), str(line))
    sp.set(w_tag("lineRule"), line_rule)
    if first_line:
        ind = ET.SubElement(pPr, w_tag("ind"))
        ind.set(w_tag("firstLine"), str(first_line))
    if jc:
        j = ET.SubElement(pPr, w_tag("jc"))
        j.set(w_tag("val"), jc)

    if text:
        r = ET.SubElement(p, w_tag("r"))
        r.append(make_rPr(font_ascii=font_ascii, font_ea=font_ea, sz=sz, bold=bold, italic=italic, color=color))
        t = ET.SubElement(r, w_tag("t"))
        t.set(f"{{{XML_NS}}}space", "preserve")
        t.text = text
    return p


def make_field_p(field_instr, jc="center", sz=20, font_ascii="Times New Roman"):
    p = ET.Element(w_tag("p"))
    pPr = ET.SubElement(p, w_tag("pPr"))
    j = ET.SubElement(pPr, w_tag("jc"))
    j.set(w_tag("val"), jc)

    for ftype, text in [("begin", None), (None, field_instr), ("separate", None), ("end", None)]:
        r = ET.SubElement(p, w_tag("r"))
        r.append(make_rPr(font_ascii=font_ascii, sz=sz))
        if ftype:
            fc = ET.SubElement(r, w_tag("fldChar"))
            fc.set(w_tag("fldCharType"), ftype)
        else:
            it = ET.SubElement(r, w_tag("instrText"))
            it.set(f"{{{XML_NS}}}space", "preserve")
            it.text = f" {text} "
    return p


def make_page_break():
    p = ET.Element(w_tag("p"))
    r = ET.SubElement(p, w_tag("r"))
    br = ET.SubElement(r, w_tag("br"))
    br.set(w_tag("type"), "page")
    return p


def make_sect_break_p(pg_num_fmt="upperRoman", start="1", header_rid=None, footer_rid=None, title_pg=False):
    """Create a paragraph carrying a sectPr for ending a section (e.g., Cover or Front Matter)."""
    p = ET.Element(w_tag("p"))
    pPr = ET.SubElement(p, w_tag("pPr"))
    sectPr = ET.SubElement(pPr, w_tag("sectPr"))
    if header_rid:
        hr = ET.SubElement(sectPr, w_tag("headerReference"))
        hr.set(w_tag("type"), "default")
        hr.set(f"{{{R_NS}}}id", header_rid)
    if footer_rid:
        fr = ET.SubElement(sectPr, w_tag("footerReference"))
        fr.set(w_tag("type"), "default")
        fr.set(f"{{{R_NS}}}id", footer_rid)
    pgSz = ET.SubElement(sectPr, w_tag("pgSz"))
    pgSz.set(w_tag("w"), "11906")   # A4 width (210 mm)
    pgSz.set(w_tag("h"), "16838")   # A4 height (297 mm)
    pgMar = ET.SubElement(sectPr, w_tag("pgMar"))
    pgMar.set(w_tag("top"), "1417")     # 2.5 cm
    pgMar.set(w_tag("bottom"), "1417")  # 2.5 cm
    pgMar.set(w_tag("left"), "1701")    # 3.0 cm (binding)
    pgMar.set(w_tag("right"), "1417")   # 2.5 cm
    pgMar.set(w_tag("header"), "850")   # 1.5 cm
    pgMar.set(w_tag("footer"), "850")   # 1.5 cm
    pgMar.set(w_tag("gutter"), "0")
    if pg_num_fmt:
        pgNumType = ET.SubElement(sectPr, w_tag("pgNumType"))
        pgNumType.set(w_tag("fmt"), pg_num_fmt)
        if start:
            pgNumType.set(w_tag("start"), str(start))
    if title_pg:
        ET.SubElement(sectPr, w_tag("titlePg"))
    return p


def build_header_xml(text):
    hdr = ET.Element(w_tag("hdr"))
    p = ET.SubElement(hdr, w_tag("p"))
    pPr = ET.SubElement(p, w_tag("pPr"))
    pBdr = ET.SubElement(pPr, w_tag("pBdr"))
    bot = ET.SubElement(pBdr, w_tag("bottom"))
    bot.set(w_tag("val"), "single")
    bot.set(w_tag("sz"), "6")
    bot.set(w_tag("space"), "4")
    bot.set(w_tag("color"), "444444")
    jc = ET.SubElement(pPr, w_tag("jc"))
    jc.set(w_tag("val"), "center")
    r = ET.SubElement(p, w_tag("r"))
    r.append(make_rPr(font_ascii="Times New Roman", font_ea="SimSun", sz=18, color="333333"))
    t = ET.SubElement(r, w_tag("t"))
    t.set(f"{{{XML_NS}}}space", "preserve")
    t.text = text
    return ET.tostring(hdr, encoding="utf-8", xml_declaration=True)


def build_footer_xml():
    ftr = ET.Element(w_tag("ftr"))
    ftr.append(make_field_p("PAGE", jc="center", sz=20))
    return ET.tostring(ftr, encoding="utf-8", xml_declaration=True)


def build_ustb_front_matter(front_header_rid, front_footer_rid):
    elems = []

    # --- 1. COVER PAGE (No page numbers) ---
    elems.append(make_p("UNIVERSITY OF SCIENCE AND TECHNOLOGY BEIJING", bold=True, sz=32, jc="center", space_before=480, space_after=80, color="1B365D"))
    elems.append(make_p("北京科技大学", bold=True, sz=36, jc="center", space_before=0, space_after=120, font_ea="SimHei", color="1B365D"))
    elems.append(make_p("School of Economics and Management (SEM)", bold=True, sz=26, jc="center", space_before=0, space_after=60))
    elems.append(make_p("经济管理学院", bold=True, sz=26, jc="center", space_before=0, space_after=480, font_ea="SimHei"))

    elems.append(make_p("MASTER'S DEGREE THESIS", bold=True, sz=40, jc="center", space_before=240, space_after=120, color="1B365D"))
    elems.append(make_p("硕 士 学 位 论 文", bold=True, sz=40, jc="center", space_before=0, space_after=600, font_ea="SimHei", color="1B365D"))

    elems.append(make_p(
        "Machine Learning for Medium- to Long-Term Sand and Dust Storm Forecasting in Saudi Arabia, with Special Emphasis on Riyadh",
        bold=True, sz=30, jc="center", space_before=120, space_after=160
    ))
    elems.append(make_p(
        "面向沙特阿拉伯（以利雅得为重点）中长期沙尘暴预测的机器学习方法研究",
        bold=True, sz=28, jc="center", space_before=0, space_after=720, font_ea="SimHei"
    ))

    meta_lines = [
        ("Candidate Name (姓名):", "Yuyan (语嫣)"),
        ("Student ID (学号):", "202461024"),
        ("Major / Discipline (专业):", "Environmental Engineering (环境工程)"),
        ("Supervisor (指导教师):", "Prof. Zhang Wei (张伟 教授)"),
        ("College / School (培养单位):", "School of Economics and Management, USTB"),
        ("Submission Date (提交日期):", "November 2026"),
    ]
    for label, val in meta_lines:
        p = ET.Element(w_tag("p"))
        pPr = ET.SubElement(p, w_tag("pPr"))
        sp = ET.SubElement(pPr, w_tag("spacing"))
        sp.set(w_tag("before"), "80")
        sp.set(w_tag("after"), "80")
        sp.set(w_tag("line"), "360")
        sp.set(w_tag("lineRule"), "auto")
        ind = ET.SubElement(pPr, w_tag("ind"))
        ind.set(w_tag("left"), "1440")
        r1 = ET.SubElement(p, w_tag("r"))
        r1.append(make_rPr(sz=24, bold=True))
        t1 = ET.SubElement(r1, w_tag("t"))
        t1.set(f"{{{XML_NS}}}space", "preserve")
        t1.text = f"{label:<36s} "
        r2 = ET.SubElement(p, w_tag("r"))
        r2.append(make_rPr(sz=24, bold=False))
        t2 = ET.SubElement(r2, w_tag("t"))
        t2.set(f"{{{XML_NS}}}space", "preserve")
        t2.text = val
        elems.append(p)

    # End Cover section (no header/footer)
    elems.append(make_sect_break_p(pg_num_fmt=None, start=None))

    # --- 2. INNER TITLE PAGE (Classification & UDC) ---
    elems.append(make_p("Chinese Library Classification (中图分类号): TP181 / P457          UDC: 551.5", sz=22, jc="left", space_before=0, space_after=80))
    elems.append(make_p("Confidentiality Level (密级): Public / 公开                              Degree Level: Master's Degree", sz=22, jc="left", space_before=0, space_after=600))
    elems.append(make_p("University of Science and Technology Beijing", bold=True, sz=28, jc="center", space_before=240, space_after=80))
    elems.append(make_p("Master's Degree Dissertation", bold=True, sz=26, jc="center", space_before=0, space_after=480))
    elems.append(make_p(
        "Machine Learning for Medium- to Long-Term Sand and Dust Storm Forecasting in Saudi Arabia, with Special Emphasis on Riyadh",
        bold=True, sz=28, jc="center", space_before=120, space_after=480
    ))
    elems.append(make_p("Author: Yuyan (语嫣)          Supervisor: Prof. Zhang Wei (张伟 教授)", sz=24, jc="center", space_before=240, space_after=120))
    elems.append(make_p("School of Economics and Management, University of Science and Technology Beijing", sz=22, jc="center", space_before=0, space_after=120))
    elems.append(make_p("Beijing 100083, P. R. China", sz=22, jc="center", space_before=0, space_after=120))

    elems.append(make_page_break())

    # --- 3. DECLARATION OF ORIGINALITY & AUTHORIZATION (USTB Standard) ---
    elems.append(make_p("学位论文独创性声明", bold=True, sz=28, jc="center", space_before=120, space_after=60, font_ea="SimHei"))
    elems.append(make_p("Declaration of Thesis Originality", bold=True, sz=26, jc="center", space_before=0, space_after=240))

    elems.append(make_p(
        "本人郑重声明：所呈交的学位论文，是本人在导师的指导下，独立进行研究工作所取得的成果。尽我所知，除文中已经注明引用的内容外，本论文不包含任何其他个人或集体已经发表或撰写过的研究成果。对本文的研究做出重要贡献的个人和集体，均已在文中以明确方式标明。本声明的法律结果由本人承担。",
        sz=22, jc="both", space_before=60, space_after=120, first_line=480
    ))
    elems.append(make_p(
        "I hereby solemnly declare that this dissertation represents my own independent research work conducted under the supervision of my advisor. To the best of my knowledge, except for the cited references explicitly acknowledged in the text, this thesis contains no material previously published or written by any other individual or institution. All contributors to this research have been clearly recognized. I accept full legal responsibility for this declaration.",
        sz=22, jc="both", space_before=60, space_after=240, first_line=480
    ))
    elems.append(make_p("Author Signature (作者签名): Yuyan (语嫣)          Date (日期): 2026 Year 11 Month 13 Day", sz=22, jc="left", space_before=80, space_after=360))

    elems.append(make_p("学位论文版权使用授权书", bold=True, sz=28, jc="center", space_before=120, space_after=60, font_ea="SimHei"))
    elems.append(make_p("Authorization Statement for Thesis Usage", bold=True, sz=26, jc="center", space_before=0, space_after=240))
    elems.append(make_p(
        "本人完全了解北京科技大学有关保留、使用学位论文的规定，即：学校有权保留并向国家有关部门或机构送交论文的复印件和电子版，允许论文被查阅和借阅。本人授权北京科技大学可以将学位论文的全部或部分内容编入有关数据库进行检索，可以采用影印、缩印或扫描等复制手段保存和汇编学位论文。",
        sz=22, jc="both", space_before=60, space_after=120, first_line=480
    ))
    elems.append(make_p(
        "I fully understand the regulations of the University of Science and Technology Beijing (USTB) regarding the retention and use of academic dissertations. USTB has the right to retain and submit printed and electronic copies to relevant national institutions and permit the thesis to be consulted and borrowed. I authorize USTB to include all or part of this thesis in relevant databases for retrieval and to preserve and compile it through photocopying, microfilming, or digital scanning.",
        sz=22, jc="both", space_before=60, space_after=240, first_line=480
    ))
    elems.append(make_p("Author Signature (作者签名): Yuyan (语嫣)          Supervisor Signature (导师签名): Prof. Zhang Wei (张伟)", sz=22, jc="left", space_before=80, space_after=80))
    elems.append(make_p("Date (日期): 2026 Year 11 Month 13 Day", sz=22, jc="left", space_before=40, space_after=120))

    elems.append(make_page_break())

    # --- 4. ENGLISH ABSTRACT & KEYWORDS ---
    elems.append(make_p("ABSTRACT", bold=True, sz=32, jc="center", space_before=120, space_after=240))
    elems.append(make_p(
        "Sand and dust storms (SDS) across the Arabian Peninsula—and particularly within the rapidly urbanizing metropolitan basin of Riyadh—pose severe hazards to aviation safety, public respiratory health, solar energy generation, and urban infrastructure. Operational global numerical weather prediction (NWP) aerosol reanalyses such as the Copernicus Atmosphere Monitoring Service (CAMS) frequently exhibit systematic amplitude under-prediction and phase errors during acute mesoscale convective haboob and synoptic Shamal outbreaks. To overcome these limitations, this dissertation develops and validates an end-to-end, leak-free, physics-informed multimodal machine learning and Explainable AI (XAI) forecasting framework for medium- to long-term dust storm prediction over Riyadh across a ten-year observational record (2015–2024).",
        sz=24, jc="both", space_before=60, space_after=120, first_line=480
    ))
    elems.append(make_p(
        "First, a 33-feature multimodal dataset integrating CAMS aerosol optical depth, AERONET Solar Village sun-photometer observations, ERA5 surface boundary-layer diagnostics, and upper-air synoptic pressure surfaces (850, 700, and 500 hPa) is constructed under strict anti-leakage controls: ground optical proxies are lagged by 48–72 hours, chronological partitioning enforces an 80/20 split (2015–2022 training; 2023–2024 out-of-sample testing), and Yeo-Johnson power transformations plus k-NN SMOTE minority oversampling are fitted exclusively on training folds. Second, a three-tier modeling architecture is implemented: (1) a Part 1 Multimodal Reliability Meta-Model predicting severe NWP error episodes (|CAMS − AERONET| > 1.5σ = 0.6752), achieving Brier Score = 0.052; (2) Main Line A tabular gradient-boosted bias correction and WMO hazard classification (HistGradientBoosting and XGBoost), achieving R² = 0.811 and RMSE = 0.141; and (3) Main Line B deep sequence and spatial models—LSTM, 4-Head Temporal Transformer, Physics-Informed Neural Network (PINN) enforcing 1D dust advection-diffusion residuals, and a 6-node Spatiotemporal Graph Neural Network (ST-GNN) linking Riyadh with upwind desert source corridors—reaching R² = 0.843 and Macro-F1 = 0.822.",
        sz=24, jc="both", space_before=60, space_after=120, first_line=480
    ))
    elems.append(make_p(
        "Finally, a multi-method XAI suite—combining TreeSHAP cooperative attribution, permutation importance, Partial Dependence Plots (PDP), local Haboob waterfall decomposition, a white-box surrogate decision tree, multi-head self-attention maps, LSTM gating trajectories, and ST-GNN spatial graph attribution—confirms that the models learn authentic atmospheric physics, identifying topsoil desiccation cliffs (swvl1 < 0.08 m³/m³), surface wind speed thresholds (U₁₀m > 9.5 m/s), and 850 hPa Shamal jet corridors as primary drivers. The resulting framework bridges atmospheric physics and operational civil defense decision-making.",
        sz=24, jc="both", space_before=60, space_after=180, first_line=480
    ))
    elems.append(make_p(
        "Keywords: Sand and Dust Storm Forecasting; Explainable AI (XAI); Physics-Informed Neural Network (PINN); Spatiotemporal Graph Neural Network (ST-GNN); Riyadh; CAMS Bias Correction",
        bold=True, sz=24, jc="left", space_before=120, space_after=120
    ))

    elems.append(make_page_break())

    # --- 5. CHINESE ABSTRACT (摘要) & KEYWORDS (关键词) ---
    elems.append(make_p("摘  要", bold=True, sz=32, jc="center", space_before=120, space_after=240, font_ea="SimHei"))
    elems.append(make_p(
        "阿拉伯半岛尤其是快速城市化的利雅得盆地频繁遭受沙尘暴（SDS）侵袭，对航空安全、公众呼吸系统健康、光伏发电及城市基础设施构成严重威胁。哥白尼大气监测服务（CAMS）等全球数值天气预报气溶胶再分析产品在强对流哈布沙尘暴（Haboob）与夏马风（Shamal）暴发期间常出现显著的幅值低估与相位偏差。为此，本论文基于2015—2024年十年多源观测数据，构建并验证了一套防数据泄露、物理信息融合的多模态机器学习与可解释人工智能（XAI）中长期沙尘暴预测框架。",
        sz=24, jc="both", space_before=60, space_after=120, first_line=480
    ))
    elems.append(make_p(
        "首先，论文整合CAMS气溶胶光学厚度、AERONET太阳光度计观测、ERA5近地面边界层诊断场及850/700/500 hPa高空天气尺度压面数据，构建了33维多模态特征集，并严格执行防泄露控制：地面光学代理变量滞后48—72小时；按时间顺序严格划分为80%训练集（2015—2022年）与20%测试集（2023—2024年）；Yeo-Johnson幂变换与k-NN SMOTE过采样仅在训练集拟合。其次，论文建立了三层预测架构：（1）多模态可靠性元模型，用于预警NWP重大误差事件（|CAMS − AERONET| > 1.5σ = 0.6752），Brier分数达0.052；（2）主线A表格梯度提升偏差订正与WMO等级分类模型（HistGradientBoosting与XGBoost），R²达0.811、RMSE为0.141；（3）主线B深度学习与空间图网络模型（LSTM、四头时序Transformer、嵌入一维平流-扩散残差约束的物理信息神经网络PINN，以及连接利雅得与上游沙源走廊的六节点时空图神经网络ST-GNN），R²提升至0.843、Macro-F1达0.822。",
        sz=24, jc="both", space_before=60, space_after=120, first_line=480
    ))
    elems.append(make_p(
        "最后，论文通过TreeSHAP博弈归因、置换重要性、部分依赖图（PDP）、局部哈布沙尘暴瀑布图分解、白盒代理决策树、Transformer多头注意力热图、LSTM门控轨迹与ST-GNN空间图归因等多方法可解释性分析，证实模型成功捕获了表层土壤干燥临界点（swvl1 < 0.08 m³/m³）、近地面风速阈值（U₁₀m > 9.5 m/s）及850 hPa夏马风急流输送通道等真实物理机制，为市政民防部门的早期预警决策提供了可靠依据。",
        sz=24, jc="both", space_before=60, space_after=180, first_line=480
    ))
    elems.append(make_p(
        "关键词：沙尘暴预测；可解释人工智能（XAI）；物理信息神经网络（PINN）；时空图神经网络（ST-GNN）；利雅得；CAMS偏差订正",
        bold=True, sz=24, jc="left", space_before=120, space_after=120, font_ea="SimHei"
    ))

    elems.append(make_page_break())

    # --- 6. TABLE OF CONTENTS ---
    elems.append(make_p("TABLE OF CONTENTS (目  录)", bold=True, sz=32, jc="center", space_before=120, space_after=240))
    elems.append(make_field_p('TOC \\o "1-3" \\h \\z \\u', jc="left", sz=24))
    elems.append(make_p(
        "[Note: In Microsoft Word, right-click the Table of Contents above and select 'Update Field' -> 'Update entire table' to refresh exact page numbers after final printing adjustments.]",
        italic=True, sz=20, jc="left", space_before=120, space_after=180, color="555555"
    ))

    toc_preview = [
        "ABSTRACT",
        "摘  要",
        "Chapter 1  Introduction",
        "Chapter 2  Literature Review",
        "Chapter 3  Methodology",
        "Chapter 4  Results and Validation",
        "Chapter 5  Discussion and Operational Limitations",
        "Chapter 6  Conclusion and Future Work",
        "References",
        "Acknowledgements",
        "Author's Resume and Academic Achievements",
    ]
    for item in toc_preview:
        elems.append(make_p(item, sz=22, jc="left", space_before=40, space_after=40))

    # End Front Matter section with Roman page numbers
    elems.append(make_sect_break_p(pg_num_fmt="upperRoman", start="1", header_rid=front_header_rid, footer_rid=front_footer_rid))
    return elems


def build_ustb_back_matter():
    elems = []
    # Acknowledgements
    elems.append(make_p("Acknowledgements (致  谢)", style_id="2", bold=True, sz=32, jc="center", space_before=240, space_after=240, page_break_before=True, font_ea="SimHei"))
    elems.append(make_p(
        "I would like to express my deepest gratitude to my academic supervisor at the School of Economics and Management, University of Science and Technology Beijing (USTB), for their invaluable guidance, rigorous methodological feedback, and continuous encouragement throughout the completion of this Master's dissertation.",
        sz=24, jc="both", space_before=60, space_after=120, first_line=480
    ))
    elems.append(make_p(
        "My sincere appreciation also goes to the faculty members and defense committee of the School of Economics and Management for their insightful suggestions on atmospheric risk modeling, feature engineering discipline, and operational civil-defense integration. I gratefully acknowledge the open scientific data provided by the European Centre for Medium-Range Weather Forecasts (ECMWF) ERA5 and Copernicus Atmosphere Monitoring Service (CAMS), as well as NASA AERONET Solar Village ground station operators.",
        sz=24, jc="both", space_before=60, space_after=120, first_line=480
    ))
    elems.append(make_p(
        "Finally, I extend heartfelt thanks to my family and colleagues for their unwavering patience, support, and motivation throughout my graduate studies in Beijing.",
        sz=24, jc="both", space_before=60, space_after=240, first_line=480
    ))

    # Author's Resume & Academic Achievements
    elems.append(make_p("Author's Resume and Academic Achievements (作者简历及在学研究成果)", style_id="2", bold=True, sz=32, jc="center", space_before=240, space_after=240, page_break_before=True, font_ea="SimHei"))
    elems.append(make_p("1. Personal Information & Education Background", style_id="3", bold=True, sz=28, jc="left", space_before=120, space_after=80))
    elems.append(make_p("Name: Yuyan (语嫣) | Student ID: 202461024 | Degree Candidate: Master of Engineering (Environmental Engineering), University of Science and Technology Beijing (USTB), Enrolled September 2025.", sz=24, jc="both", space_before=40, space_after=120))
    elems.append(make_p("2. Research Projects & Technical Outputs Completed During Master's Study", style_id="3", bold=True, sz=28, jc="left", space_before=120, space_after=80))
    elems.append(make_p("[1] Developed a 33-feature multimodal Sand and Dust Storm forecasting and CAMS NWP bias-correction pipeline for Riyadh, Saudi Arabia (2015–2024) integrating ERA5, CAMS, and AERONET datasets.", sz=24, jc="both", space_before=40, space_after=80))
    elems.append(make_p("[2] Designed a hybrid Physics-Informed Neural Network (PINN) and 6-Node Spatiotemporal Graph Neural Network (ST-GNN) coupled with a multi-method Explainable AI (XAI) validation suite for municipal early warning.", sz=24, jc="both", space_before=40, space_after=80))
    return elems


def update_styles_xml(styles_bytes):
    root = ET.fromstring(styles_bytes)
    style_specs = {
        "1": {"sz": "24", "bold": False, "jc": "both", "line": "360", "font_ascii": "Times New Roman", "font_ea": "SimSun"},
        "2": {"sz": "32", "bold": True, "jc": "center", "line": "360", "font_ascii": "Times New Roman", "font_ea": "SimHei"},
        "3": {"sz": "28", "bold": True, "jc": "left", "line": "360", "font_ascii": "Times New Roman", "font_ea": "SimHei"},
        "4": {"sz": "24", "bold": True, "jc": "left", "line": "360", "font_ascii": "Times New Roman", "font_ea": "SimHei"},
    }
    for st in root.findall(w_tag("style")):
        sid = st.get(w_tag("styleId"))
        if sid in style_specs:
            spec = style_specs[sid]
            rPr = st.find(w_tag("rPr"))
            if rPr is None:
                rPr = ET.SubElement(st, w_tag("rPr"))
            rFonts = rPr.find(w_tag("rFonts"))
            if rFonts is None:
                rFonts = ET.SubElement(rPr, w_tag("rFonts"))
            rFonts.set(w_tag("ascii"), spec["font_ascii"])
            rFonts.set(w_tag("hAnsi"), spec["font_ascii"])
            rFonts.set(w_tag("cs"), spec["font_ascii"])
            rFonts.set(w_tag("eastAsia"), spec["font_ea"])

            for tag_name in ["sz", "szCs"]:
                el = rPr.find(w_tag(tag_name))
                if el is None:
                    el = ET.SubElement(rPr, w_tag(tag_name))
                el.set(w_tag("val"), spec["sz"])

            if spec["bold"] and rPr.find(w_tag("b")) is None:
                ET.SubElement(rPr, w_tag("b"))

            pPr = st.find(w_tag("pPr"))
            if pPr is None:
                pPr = ET.SubElement(st, w_tag("pPr"))
            sp = pPr.find(w_tag("spacing"))
            if sp is None:
                sp = ET.SubElement(pPr, w_tag("spacing"))
            sp.set(w_tag("line"), spec["line"])
            sp.set(w_tag("lineRule"), "auto")

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def normalize_body_paragraphs(body):
    """Normalize chapter headings, fix duplicate 3.6/3.7 in Ch3, enforce Times New Roman on runs."""
    chapter_map = {
        "1 Introduction": "Chapter 1  Introduction",
        "2 Literature Review": "Chapter 2  Literature Review",
        "3 Methodology": "Chapter 3  Methodology",
        "4. Results and Validation": "Chapter 4  Results and Validation",
        "5. Discussion & Operational Limitations": "Chapter 5  Discussion and Operational Limitations",
        "6. Conclusion and Future Work": "Chapter 6  Conclusion and Future Work",
    }

    first_p = True
    seen_36 = False
    seen_37 = False

    for child in list(body):
        if child.tag != w_tag("p"):
            continue
        text = "".join(t.text for t in child.findall(f".//{w_tag('t')}") if t.text).strip()
        if not text:
            continue

        # Remove original manuscript title at [0] because it is now on Cover & Inner Title pages
        if first_p and text.startswith("Machine Learning for Medium- to Long-Term"):
            body.remove(child)
            first_p = False
            continue
        first_p = False

        pPr = child.find(w_tag("pPr"))
        if pPr is None:
            pPr = ET.SubElement(child, w_tag("pPr"))
        ps = pPr.find(w_tag("pStyle"))
        style_id = ps.get(w_tag("val")) if ps is not None else None

        # Fix duplicate 3.6 / 3.7
        if text.startswith("3.6 "):
            if seen_36:
                text = text.replace("3.6 ", "3.9 ", 1)
                for t in child.findall(f".//{w_tag('t')}"):
                    if t.text and "3.6 " in t.text:
                        t.text = t.text.replace("3.6 ", "3.9 ", 1)
                        break
            seen_36 = True
        elif text.startswith("3.7 "):
            if seen_37:
                text = text.replace("3.7 ", "3.10 ", 1)
                for t in child.findall(f".//{w_tag('t')}"):
                    if t.text and "3.7 " in t.text:
                        t.text = t.text.replace("3.7 ", "3.10 ", 1)
                        break
            seen_37 = True

        # Normalize Chapter Headings -> style 2 (heading 1)
        if text in chapter_map:
            if ps is None:
                ps = ET.SubElement(pPr, w_tag("pStyle"))
            ps.set(w_tag("val"), "2")
            for t in child.findall(f".//{w_tag('t')}"):
                if t.text and t.text.strip() == text:
                    t.text = chapter_map[text]
                    break
            jc = pPr.find(w_tag("jc"))
            if jc is None:
                jc = ET.SubElement(pPr, w_tag("jc"))
            jc.set(w_tag("val"), "center")
            if text != "1 Introduction":
                if pPr.find(w_tag("pageBreakBefore")) is None:
                    ET.SubElement(pPr, w_tag("pageBreakBefore"))
        elif text == "References":
            if ps is None:
                ps = ET.SubElement(pPr, w_tag("pStyle"))
            ps.set(w_tag("val"), "2")
            jc = pPr.find(w_tag("jc"))
            if jc is None:
                jc = ET.SubElement(pPr, w_tag("jc"))
            jc.set(w_tag("val"), "center")
            if pPr.find(w_tag("pageBreakBefore")) is None:
                ET.SubElement(pPr, w_tag("pageBreakBefore"))
        else:
            # Normalize section X.Y -> style 3 (heading 2), subsection X.Y.Z -> style 4 (heading 3)
            import re
            if re.match(r"^\d+\.\d+\s+", text) and len(text) < 120:
                if ps is None:
                    ps = ET.SubElement(pPr, w_tag("pStyle"))
                ps.set(w_tag("val"), "3")
            elif re.match(r"^\d+\.\d+\.\d+\s+", text) and len(text) < 130:
                if ps is None:
                    ps = ET.SubElement(pPr, w_tag("pStyle"))
                ps.set(w_tag("val"), "4")

        # Enforce Times New Roman on existing runs
        for r in child.findall(f".//{w_tag('r')}"):
            rPr = r.find(w_tag("rPr"))
            if rPr is None:
                rPr = ET.SubElement(r, w_tag("rPr"))
            rFonts = rPr.find(w_tag("rFonts"))
            if rFonts is None:
                rFonts = ET.SubElement(rPr, w_tag("rFonts"))
            rFonts.set(w_tag("ascii"), "Times New Roman")
            rFonts.set(w_tag("hAnsi"), "Times New Roman")
            rFonts.set(w_tag("cs"), "Times New Roman")
            rFonts.set(w_tag("eastAsia"), "SimSun")


def main():
    tmp_zip = SRC_DOCX.with_suffix(".ustb_tmp.docx")
    with zipfile.ZipFile(SRC_DOCX, "r") as zin:
        namelist = zin.namelist()
        file_data = {name: zin.read(name) for name in namelist}

    # Update styles.xml
    file_data["word/styles.xml"] = update_styles_xml(file_data["word/styles.xml"])

    # Add headers and footers
    file_data["word/header_ustb_front.xml"] = build_header_xml("University of Science and Technology Beijing Master's Degree Thesis")
    file_data["word/header_ustb_body.xml"] = build_header_xml("University of Science and Technology Beijing — Master's Thesis (School of Economics and Management)")
    file_data["word/footer_ustb.xml"] = build_footer_xml()

    # Register relationships in word/_rels/document.xml.rels
    rels_root = ET.fromstring(file_data["word/_rels/document.xml.rels"])
    existing_ids = {el.get("Id") for el in rels_root}
    next_num = 100
    def add_rel(rtype, target):
        nonlocal next_num
        while f"rId{next_num}" in existing_ids:
            next_num += 1
        rid = f"rId{next_num}"
        existing_ids.add(rid)
        rel = ET.SubElement(rels_root, f"{{{PKG_REL_NS}}}Relationship")
        rel.set("Id", rid)
        rel.set("Type", rtype)
        rel.set("Target", target)
        return rid

    HDR_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header"
    FTR_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"
    front_hdr_rid = add_rel(HDR_TYPE, "header_ustb_front.xml")
    body_hdr_rid = add_rel(HDR_TYPE, "header_ustb_body.xml")
    ftr_rid = add_rel(FTR_TYPE, "footer_ustb.xml")
    file_data["word/_rels/document.xml.rels"] = ET.tostring(rels_root, encoding="utf-8", xml_declaration=True)

    # Register Content_Types
    ct_root = ET.fromstring(file_data["[Content_Types].xml"])
    existing_parts = {el.get("PartName") for el in ct_root}
    for part, ctype in [
        ("/word/header_ustb_front.xml", "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"),
        ("/word/header_ustb_body.xml", "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"),
        ("/word/footer_ustb.xml", "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"),
    ]:
        if part not in existing_parts:
            ov = ET.SubElement(ct_root, f"{{{CT_NS}}}Override")
            ov.set("PartName", part)
            ov.set("ContentType", ctype)
    file_data["[Content_Types].xml"] = ET.tostring(ct_root, encoding="utf-8", xml_declaration=True)

    # Modify document.xml
    doc_root = ET.fromstring(file_data["word/document.xml"])
    body = doc_root.find(w_tag("body"))

    normalize_body_paragraphs(body)

    # Insert Front Matter at the beginning of body
    front_elems = build_ustb_front_matter(front_hdr_rid, ftr_rid)
    for idx, el in enumerate(front_elems):
        body.insert(idx, el)

    # Append Back Matter right before final sectPr
    sectPr = body.find(w_tag("sectPr"))
    back_elems = build_ustb_back_matter()
    if sectPr is not None:
        sect_idx = list(body).index(sectPr)
        for offset, el in enumerate(back_elems):
            body.insert(sect_idx + offset, el)
    else:
        for el in back_elems:
            body.append(el)
        sectPr = ET.SubElement(body, w_tag("sectPr"))

    # Update final sectPr -> A4 + USTB margins + body header/footer + Arabic page numbers starting at 1
    for child in list(sectPr):
        if child.tag in [w_tag("pgSz"), w_tag("pgMar"), w_tag("pgNumType"), w_tag("headerReference"), w_tag("footerReference")]:
            sectPr.remove(child)

    hr = ET.SubElement(sectPr, w_tag("headerReference"))
    hr.set(w_tag("type"), "default")
    hr.set(f"{{{R_NS}}}id", body_hdr_rid)
    fr = ET.SubElement(sectPr, w_tag("footerReference"))
    fr.set(w_tag("type"), "default")
    fr.set(f"{{{R_NS}}}id", ftr_rid)

    pgSz = ET.SubElement(sectPr, w_tag("pgSz"))
    pgSz.set(w_tag("w"), "11906")
    pgSz.set(w_tag("h"), "16838")

    pgMar = ET.SubElement(sectPr, w_tag("pgMar"))
    pgMar.set(w_tag("top"), "1417")
    pgMar.set(w_tag("bottom"), "1417")
    pgMar.set(w_tag("left"), "1701")
    pgMar.set(w_tag("right"), "1417")
    pgMar.set(w_tag("header"), "850")
    pgMar.set(w_tag("footer"), "850")
    pgMar.set(w_tag("gutter"), "0")

    pgNum = ET.SubElement(sectPr, w_tag("pgNumType"))
    pgNum.set(w_tag("fmt"), "decimal")
    pgNum.set(w_tag("start"), "1")

    file_data["word/document.xml"] = ET.tostring(doc_root, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in file_data.items():
            zout.writestr(name, data)

    shutil.move(str(tmp_zip), str(OUT_LATEST))
    for target in [OUT_FINAL_ORIG, OUT_MAIN_DOCX, OUT_ENHANCED]:
        try:
            shutil.copy2(str(OUT_LATEST), str(target))
            print(f"SUCCESS: Synced copy -> {target}")
        except PermissionError:
            print(f"WARN: Skipped locked file -> {target}")
    print(f"SUCCESS: Formatted USTB SEM Master's Thesis -> {OUT_LATEST}")


if __name__ == "__main__":
    main()

