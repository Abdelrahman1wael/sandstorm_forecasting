# 🎓 Chinese University Master's Dissertation Standards & Blueprint
### *Master of Engineering (环境工程硕士专业学位 / 工学硕士学位) • Research Thesis Framework*
**Affiliation:** University of Science and Technology Beijing (北京科技大学 • USTB)  
**School:** School of Energy and Environmental Engineering (能源与环境工程学院)  
**Discipline:** Environmental Engineering (环境工程) • Atmospheric Environment & Environmental Informatics  
**National Standards:** GB/T 7713.1-2006 (学位论文编写规则) & GB/T 7714-2015 (信息与文献 参考文献著录规则)

---

## 🌟 Executive Overview & Degree Requirements

Writing a Master's Degree Dissertation at a premier Chinese national university (Double First-Class / "双一流" / Project 211) requires strict adherence to Ministry of Education (MOE) and University Graduate School regulations. 

A Master of Engineering dissertation must satisfy three mandatory criteria:
1. **Academic Rigor & Theoretical Depth:** Sound mathematical formulations, rigorous literature review, and comprehensive understanding of physical atmospheric dynamics.
2. **Engineering Application & Operational Value:** Developing a working, scalable technological system (DustML) with tangible public safety and municipal emergency value.
3. **Multi-Disciplinary Synthesis:** Uniting engineering mechanics (PINN conservation laws), geospatial analysis (GIS spatial autocorrelation), and socioeconomic behavioral modeling (SPSS/AMOS SEM).

---

## 📂 Master Research Directory Index

```
Planning/Master_Research/
├── 📘 README.md                                         # University Standards, Degree Regulations & Thesis Architecture
├── 📑 CH1_INTRODUCTION.md                              # Chapter 1: 绪论 (Research Background, Problem Statement, Objectives, Innovations)
├── 📚 CH2_LITERATURE_REVIEW.md                         # Chapter 2: 文献综述与理论基础 (NWP Limits, AI in Meteorology, PINNs, Gaps)
├── 📐 CH3_DATA_AND_METHODOLOGY_STANDARDS.md            # Chapters 3 & 4: Data Harmonization, Line A (Tree Ensembles) & Line B (Deep PINN)
├── 🗺️ CH5_SPATIAL_AND_SOCIOECONOMIC_STANDARDS.md       # Chapter 5: GIS Spatial Statistics & SPSS/AMOS Structural Equation Modeling
├── 🌪️ CH6_CASE_STUDIES_AND_VALIDATION_STANDARDS.md     # Chapter 6: Historical Event Hindcasts, XAI (Tree SHAP) & Decision Playbook
└── ⚖️ ACADEMIC_WRITING_AND_DEFENSE_STANDARDS.md         # Formatting Specifications, Blind Review (盲审) Rubric & Defense Protocol
```

---

## 🏛️ Standard 7-Chapter Dissertation Architecture

According to USTB Graduate School guidelines, the dissertation is divided into 7 distinct chapters:

```
+---------------------------------------------------------------------------------------------------+
|                        STANDARD CHINESE UNIVERSITY DISSERTATION STRUCTURE                         |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [PRELIMINARY PAGES]        Chinese Title & Abstract (中文摘要与关键词) • English Abstract (Abstract)  |
|                             Nomenclature & Abbreviations • Table of Contents (目录)               |
|                                                     │                                             |
|                                                     ▼                                             |
|  [CHAPTER 1: 绪论]          Research Background • Problems in NWP • Objectives • Innovations      |
|                             Technical Route Roadmap • Dissertation Organization                   |
|                                                     │                                             |
|                                                     ▼                                             |
|  [CHAPTER 2: 文献综述]      Atmospheric Hydrodynamics & Aerosol Physics • Machine Learning in SDS |
|                             Physics-Informed Deep Learning • Socioeconomic SEM • Research Gaps    |
|                                                     │                                             |
|                                                     ▼                                             |
|  [CHAPTER 3: 数据融合]      Multi-Source Data Ingestion (NWP, Satellites, Stations, DEM)          |
|                             Quality Control & Despiking • 5km Grid Alignment • Feature Store      |
|                                                     │                                             |
|                                                     ▼                                             |
|  [CHAPTER 4: 双线预测模型]  Main Line A (NWP Statistical Bias Correction & Tree Ensembles)        |
|                             Main Line B (Coupled AI-GAMFS + ST-GNN + PINN Conservation PDEs)      |
|                             Uncertainty Head (P10, P50, P90) • Cost-Sensitive 5-Tier Classifier   |
|                                                     │                                             |
|                                                     ▼                                             |
|  [CHAPTER 5: 空间与社会分析] GIS Ordinary Kriging Spatial Exposure • Moran's I & LISA Spatial Clusters|
|                             SPSS Survey Screening • AMOS Confirmatory Factor Analysis & SEM       |
|                                                     │                                             |
|                                                     ▼                                             |
|  [CHAPTER 6: 案例验证与决策] Historical Hindcast: March 2021 Super-Storm & April 2025 Basin Intrusion|
|                             Explainable AI (Tree SHAP & Attention Diagnostics) • Decision Playbook|
|                                                     │                                             |
|                                                     ▼                                             |
|  [CHAPTER 7: 结论与展望]    Summary of Key Scientific Findings • Major Theoretical Innovations    |
|                             Engineering Contributions • Limitations & Future Research Directions  |
|                                                     │                                             |
|                                                     ▼                                             |
|  [BACK MATTER]              References (参考文献 GB/T 7714) • Appendix (附录) • Academic Papers &  |
|                             Patents (攻读学位期间发表的学术论文与研究成果) • Acknowledgements (致谢) |
+---------------------------------------------------------------------------------------------------+
```

---

## 🎯 Master's Degree Evaluation Criteria (USTB Blind Review / 盲审)

To pass the external national blind peer review (教育部抽检 / 匿名盲审), the thesis is scored across five core dimensions:

| Evaluation Dimension | Chinese Criterion | Score Weight | Focus & Quality Standard |
| :--- | :--- | :---: | :--- |
| **1. Topic Selection & Significance** | 选题与综述 | **15%** | Topic aligns with national environmental protection strategies; comprehensive literature review; clear identification of research gaps. |
| **2. Theoretical & Professional Knowledge** | 基础理论与专业知识 | **25%** | Solid grasp of atmospheric fluid dynamics, machine learning algorithms, and environmental remote sensing; rigorous mathematical formulations. |
| **3. Research Capability & Innovation** | 科研能力与创新成果 | **30%** | Clear innovations (e.g., PINN Owen saltation constraints, 14-node ST-GNN corridor diffusion, dual-line adaptive blending); novel methodology. |
| **4. Engineering Application & Value** | 应用价值与工程实践 | **15%** | High practical utility; working REST microservice and interactive web dashboard; concrete municipal disaster reduction playbook. |
| **5. Writing Rigor & Academic Norms** | 写作规范与学风 | **15%** | Flawless formatting (GB/T 7713.1); standardized equations, tables, and figures; strict plagiarism compliance (CNKI TMLC $< 10\%$). |

---

## 📋 Dissertation Writing Checklist for USTB Students

- [x] **Clear Innovation Points:** Formulate at least 3 distinct theoretical and engineering innovations in Chapter 1.
- [x] **Rigorous Mathematical Foundations:** Express all models using standard notation (tensors, PDEs, Lagrangian mechanics, loss functions).
- [x] **No Unsubstantiated Claims:** Every empirical finding must be supported by statistical benchmarks (RMSE, TS/CSI, $R^2$, POD, FAR).
- [x] **Bilingual Academic Nomenclature:** Standardized Chinese terms (e.g., 气溶胶光学厚度, 跃移阈值摩擦风速, 物理信息神经网络) alongside English equivalents.
- [x] **Publication Output Requirement:** At least 1 first-author paper submitted to a recognized peer-reviewed journal (SCI / EI / CSCD) during master's tenure.
