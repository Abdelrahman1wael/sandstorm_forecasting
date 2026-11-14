from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.table import WD_TABLE_ALIGNMENT

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
DOC_PATH = ROOT / "01_Documentation" / "FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver7.docx"

TABLE_8_PACKAGES = [
    ["Package / Library", "Version", "Category", "Role in Project Pipeline"],
    ["Python", "3.12.0", "Core Runtime", "Primary interpreter executing all ingestion, modeling, XAI, and reporting scripts"],
    ["numpy", "2.5.4", "Numerical Computing", "Array operations, tensor construction, lag/rolling calculations, and seed control"],
    ["pandas", "3.1.1", "Tabular Data", "86,928-hour time-series alignment, 360 h purge splitting, and CSV result exports"],
    ["scipy", "1.18.1", "Scientific Computing", "Statistical diagnostics, correlation checks, and distribution analysis"],
    ["scikit-learn", "1.9.1", "Line A Tabular ML", "LogReg_Bal, RandomForest, ExtraTrees, HistGB, Ridge_log1p, calibration, and CV/metrics"],
    ["xgboost", "3.4.1", "Gradient Boosting", "XGBoost binary classifier and regressor across 24–360 h horizons and XAI-1/2"],
    ["torch", "2.15.0+cpu", "Line B Deep Learning", "PyTorch implementations of RealLSTMNet, RealTransformerNet, RealPINNNet, RealSTGNNNet, and LSTM saliency"],
    ["shap", "0.54.1", "Explainable AI (XAI)", "Exact shap.TreeExplainer global, directional, modality, local waterfall, and multi-horizon attributions"],
    ["matplotlib", "3.11.2", "Visualization", "Generation of nb02_fig*, nb03_fig*, and nb04_fig* diagnostic and XAI figures"],
    ["xarray", "2026.9.0", "Gridded Reanalysis", "Multi-dimensional NetCDF handling for ECMWF ERA5 and CAMS atmospheric fields"],
    ["netCDF4", "1.7.5.1.post1", "Gridded I/O", "Backend NetCDF-4/HDF5 file decoding for ERA5 and CAMS reanalysis archives"],
    ["cdsapi", "0.7.7", "Data Ingestion", "Copernicus Climate Data Store API client for ERA5 reanalysis retrieval"],
    ["requests", "2.34.2", "Data Ingestion", "HTTP retrieval of ground METAR, satellite, and auxiliary meteorological feeds"],
    ["joblib", "1.6.0", "Model Serialization", "Exporting and loading trained Line A models in 05_Models/line_a/"],
    ["ipykernel", "7.4.0", "Notebook Execution", "Jupyter kernel execution for reproducible Notebooks 02, 03, and 04"],
    ["python-docx", "1.2.0", "Documentation", "Automated synchronization of thesis tables, figures, and chapters in .docx"],
]

TABLE_9_ARTEFACTS = [
    ["Artefact / Script Path", "Type", "Primary Outputs & Scope"],
    ["06_Data/riyadh_hourly_clean_tvt.csv", "Master Dataset", "86,928 hourly records (2015–2024), 115 features, 70%/15%/15% split with 360 h purge gaps"],
    ["04_Notebooks/02_main_line_a_tabular_ml_riyadh.ipynb", "Notebook (Line A)", "5-fold CV, calibrated classification, regression; outputs nb02_line_a_*_hourly.csv & nb02_fig01..07.png"],
    ["04_Notebooks/03_main_line_b_deep_learning_riyadh.ipynb", "Notebook (Line B)", "RealLSTMNet, RealTransformerNet, RealPINNNet, RealSTGNNNet; outputs nb03_line_b_*_hourly.csv & nb03_fig02..05.png"],
    ["04_Notebooks/04_explainable_ai_xai_riyadh.ipynb", "Notebook (XAI)", "XAI-1 to XAI-6 audit; outputs nb04_xai_clean_hourly_importance.csv & nb04_fig01..09.png"],
    ["08_Scripts/05_evaluation_and_plotting/build_and_run_clean_hourly_notebooks.py", "Orchestrator", "Reproducible end-to-end execution of clean hourly notebooks"],
    ["08_Scripts/05_evaluation_and_plotting/export_final_hourly_models.py", "Model Exporter", "Exports final Line A and Line B artefacts into 05_Models/line_a/ and 05_Models/line_b/"],
]


def add_heading(doc, text, style_name):
    p = doc.add_paragraph(text)
    if style_name in [s.name for s in doc.styles]:
        p.style = doc.styles[style_name]
    return p


def add_normal(doc, text):
    p = doc.add_paragraph()
    if "Normal" in [s.name for s in doc.styles]:
        p.style = doc.styles["Normal"]
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    return p


def add_table(doc, rows, caption):
    cap = add_normal(doc, caption)
    cap.runs[0].bold = True
    cap.runs[0].font.size = Pt(10)
    tbl = doc.add_table(rows=len(rows), cols=len(rows[0]))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = str(val)
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)
                    if r_idx == 0:
                        r.bold = True
    add_normal(doc, "")
    return tbl


def main():
    doc = Document(str(DOC_PATH))

    # Avoid duplicate Appendices if re-run
    app_idx = next((i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Appendices" in p.text), None)
    if app_idx is not None:
        body = doc.element.body
        to_remove = []
        cur = doc.paragraphs[app_idx]._p
        while cur is not None:
            to_remove.append(cur)
            cur = cur.getnext()
        for el in to_remove:
            body.remove(el)

    add_heading(doc, "Appendices", "Heading 1")

    add_heading(doc, "Appendix A: Software Environment, Packages, and Libraries", "Heading 2")
    add_normal(
        doc,
        "All data ingestion, preprocessing, Line A tabular machine learning, Line B PyTorch deep learning, Explainable AI (XAI-1 through XAI-6), and thesis documentation workflows were executed inside a dedicated Python 3.12.0 virtual environment (.venv). Table 8 documents the exact installed package versions and their roles across the forecasting pipeline.",
    )
    add_table(doc, TABLE_8_PACKAGES, "Table 8: Python packages, exact versions, and pipeline roles verified in the project environment")

    add_heading(doc, "Appendix B: Reproducible Notebooks, Scripts, and Exported Artefacts", "Heading 2")
    add_normal(
        doc,
        "To ensure full experimental reproducibility, Table 9 indexes the master clean hourly dataset, Jupyter notebooks, orchestration scripts, and exported model/result directories supporting Chapters 3 through 6.",
    )
    add_table(doc, TABLE_9_ARTEFACTS, "Table 9: Core notebooks, orchestration scripts, and output artefacts")

    try:
        doc.save(str(DOC_PATH))
        print(f"Added Appendices (Tables 8–9) to {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver8.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
