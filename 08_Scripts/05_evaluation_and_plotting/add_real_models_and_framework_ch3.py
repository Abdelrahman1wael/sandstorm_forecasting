"""Add the verified, real-project sections for Model Construction, Cost-Sensitive
Optimization, Evaluation, Candidate Algorithms, and Municipal Early-Warning
Framework into Chapter 3 of the latest thesis .docx.
"""

from pathlib import Path
import docx

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2_REFS_UPDATED_CLEAN_PERSONAL_EXACT61_REFS_MIDTERM_COVER_CH3_UPDATED_REV32.docx"
)


def add_para_before(anchor_el, text: str, style: str, doc: docx.Document):
    p = doc.add_paragraph(text, style=style)
    el = p._element
    el.getparent().remove(el)
    anchor_el.addprevious(el)
    return p


def main() -> None:
    doc = docx.Document(str(DOC_PATH))
    ch4_p = next(p for p in doc.paragraphs if p.style.name == "Heading 1" and "Chapter 4" in p.text)
    ch4_el = ch4_p._element

    # Avoid duplicate insertion if run twice
    if any(p.style.name == "Heading 2" and p.text.strip().startswith("3.7") for p in doc.paragraphs):
        print("Sections 3.7+ already present; skipping.")
        return

    # 3.7 Model Construction, Cost-Sensitive Optimization, and Evaluation
    add_para_before(ch4_el, "3.7 Model Construction, Cost-Sensitive Optimization, and Evaluation", "Heading 2", doc)
    add_para_before(
        ch4_el,
        "All production models in the latest clean-hourly pipeline are trained via build_and_run_clean_hourly_notebooks.py and exported by export_final_hourly_models.py into 05_Models/line_a/ and 05_Models/line_b/:",
        "Normal",
        doc,
    )
    add_para_before(
        ch4_el,
        "Model Construction and Exported Artifacts: Main Line A exports clean_hourly_preprocessor.joblib alongside horizon-optimal classifiers (line_a_randomforest_cal_24h.joblib, line_a_randomforest_cal_72h.joblib, line_a_randomforest_cal_168h.joblib, line_a_xgboost_cal_216h.joblib, and line_a_xgboost_cal_360h.joblib), benchmarked against ExtraTrees_Cal, HistGB_Cal, LogReg_Bal_Cal, Ridge_log1p, Persistence_Cal, and MonthClimo_Cal. Main Line B exports PyTorch checkpoints (lineb_pinn_24h_cls.pt, lineb_pinn_168h_cls.pt, lineb_transformer_72h_cls.pt, lineb_transformer_216h_cls.pt, lineb_transformer_360h_cls.pt, lineb_lstm_360h_reg.pt, and multimodal_npz_net.pt), evaluated alongside LineB_STGNN.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "Cost-Sensitive Optimization and Probability Calibration: Rather than synthetic oversampling (which risks temporal leakage across hourly autocorrelations), rare-event imbalance is handled via balanced class weights (class_weight) in Line A and positive-class weighting (pos_weight inside BCEWithLogitsLoss) in Line B, paired with validation-set probability calibration (nb02_fig04.png reliability diagrams) and quantile regression intervals.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "Multi-Indicator Evaluation and Mechanistic Interpretation: Models are evaluated on the untouched 2023–2024 test partition using ROC-AUC, PR-AUC, Brier Score, Brier Skill Score (BSS), Recall@Top10%, Lift@Top10%, RMSE, MAE, and R², followed by SHAP attribution, permutation ROC-AUC drop, 1D/2D PDP and ICE curves, LSTM 24-hour lookback saliency, and 6-node spatial graph weighted degree analysis in 04_explainable_ai_xai_riyadh.ipynb.",
        "List Paragraph",
        doc,
    )

    # 3.8 Candidate Machine Learning Algorithms
    add_para_before(ch4_el, "3.8 Candidate Machine Learning Algorithms", "Heading 2", doc)
    add_para_before(
        ch4_el,
        "Random Forests & ExtraTrees (Bagging Ensembles): Train randomised decision trees on bootstrap/subsampled splits with balanced class weights to reduce variance across correlated meteorological predictors.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "XGBoost & Histogram Gradient Boosting (HistGB): Sequentially fit additive trees to second-order gradient residuals with regularisation, excelling at medium-to-long-range (216 h–360 h) tabular classification.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "Ridge Regression (log1p) & Quantile Regression: Regularised linear regression on ln(PM₁₀ + 1) provides drift-resilient continuous baselines under the 2015–2024 regime shift, while quantile regression estimates non-parametric uncertainty bounds.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "LSTM & Transformer Sequence Networks: Capture multi-day temporal dependencies via gated recurrent memory cells (LSTM) and multi-head self-attention over 24-hour lookback windows (Transformer).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "Physics-Informed Neural Networks (PINN) & Spatiotemporal Graph Neural Networks (ST-GNN): LineB_PINN embeds aeolian saltation and mass-conservation constraints into the neural loss, while LineB_STGNN propagates upstream dust dynamics across the 6×6 weighted regional adjacency graph (riyadh_graph_adjacency_matrix.npy).",
        "List Paragraph",
        doc,
    )

    try:
        doc.save(str(DOC_PATH))
        print(f"Successfully added Sections 3.7 and 3.8 to {DOC_PATH.name}!")
    except PermissionError:
        alt = DOC_PATH.with_name(DOC_PATH.stem + "_FINAL_CH3.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
