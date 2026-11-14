"""Refactor Section 3.10 (and remove the outdated 3.6.2 / 3.10 leftovers) in
FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver2.docx
to match the exact Line A (NB02) and Line B (NB03) implementations.
"""

from pathlib import Path
import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver2.docx"
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

    # Locate the outdated 3.6.2 / 3.10 block (if present) and Chapter 4 anchor
    ch4_p = next(p for p in doc.paragraphs if p.style.name == "Heading 1" and "Chapter 4" in p.text)
    ch4_el = ch4_p._element

    # Remove any old 3.6.2 (SMOTE/11,688) through old 3.10 / Figure 4 paragraphs before Chapter 4
    old_start = next(
        (p for p in doc.paragraphs if "3.6.2 Statistical Normalization" in p.text or "3.10 Model Architecture" in p.text),
        None,
    )
    if old_start is not None:
        siblings = list(body)
        i_start = siblings.index(old_start._element)
        i_ch4 = siblings.index(ch4_el)
        for el in siblings[i_start:i_ch4]:
            body.remove(el)

    # Add clean, verified Section 3.9 Model Architecture Specifications, Equations, and Hyperparameters
    add_para_before(ch4_el, "3.9 Model Architecture Specifications, Equations, and Hyperparameters", "Heading 2", doc)

    add_para_before(ch4_el, "3.9.1 Main Line A: Tabular Ensembles, Ridge Regression, and Platt Calibration", "Heading 3", doc)
    add_para_before(
        ch4_el,
        "Main Line A (04_Notebooks/02_line_a_tabular_and_meta_models_riyadh.ipynb) processes the 115 train-only Yeo-Johnson scaled hourly features across five horizons H in {24, 72, 168, 216, 360} h and three random seeds {42, 123, 456}:",
        "Normal",
        doc,
    )
    add_para_before(
        ch4_el,
        "Balanced Logistic Regression (LogReg_Bal_Cal): Regularised linear classifier (C = 0.2, class_weight = 'balanced', max_iter = 1000) serving as an interpretable linear baseline.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "Random Forest & ExtraTrees (RandomForest_Cal, ExtraTrees_Cal): 100 randomised trees (n_estimators = 100, max_depth = 8, min_samples_leaf = 8, class_weight = 'balanced') suppressing variance across correlated meteorological predictors; RandomForest_Cal is exported for 24 h, 72 h, and 168 h.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "XGBoost & HistGradientBoosting (XGBoost_Cal, HistGB_Cal): Gradient-boosted tree ensembles using positive-class cost weighting scale_pos_weight = N_neg / N_pos; XGBoost_Cal is exported for 216 h and 360 h.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "Ridge Regression (Ridge_log1p) & Validation Platt Calibration: Continuous PM₁₀ regression fits Ridge(alpha = 50.0) on ln(PM₁₀ + 1) and inverts predictions via exp(y_hat) - 1. For classification, raw validation scores s_va clipped to [-30, 30] are calibrated via LogisticRegression(C = 1.0) into P(y = 1 | s) in [1e-6, 1 - 1e-6] (Figure 9).",
        "List Paragraph",
        doc,
    )
    add_figure_before(
        ch4_el,
        FIG_DIR / "nb02_fig04.png",
        "Figure 9: Main Line A 168 h reliability diagram after validation-set Platt probability calibration (02_line_a_tabular_and_meta_models_riyadh.ipynb).",
        doc,
    )

    add_para_before(ch4_el, "3.9.2 Main Line B: PyTorch Sequence, Transformer, PINN, ST-GNN, and Multi-Modal NPZ Networks", "Heading 3", doc)
    add_para_before(
        ch4_el,
        "Main Line B (04_Notebooks/03_line_b_pytorch_real_layers.ipynb) constructs 24-hour lookback sequences X in R^(N x 24 x 115) with stride = 6 h and 360 h purge gaps, implementing five PyTorch architectures trained across seeds {42, 123, 456} with BCEWithLogitsLoss(pos_weight) + Platt calibration for classification and L1Loss on ln(PM₁₀ + 1) with AdamW(lr = 1.5e-3, weight_decay = 1e-3, batch_size = 128) for regression:",
        "Normal",
        doc,
    )
    add_para_before(
        ch4_el,
        "1. RealLSTMNet: 2-layer LSTM (hidden = 48, num_layers = 2, dropout = 0.2) followed by MLP head Linear(48 -> 24) -> ReLU -> Linear(24 -> 1).",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "2. RealTransformerNet: Linear projection (in_dim -> d_model = 48), learnable positional embedding in R^(1 x 24 x 48), 2-layer TransformerEncoder (nhead = 4, dim_feedforward = 96, dropout = 0.2), and Linear(48 -> 1) head.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "3. RealPINNNet: GRU backbone (hidden = 48) with SiLU MLP head (48 -> 24 -> 1), augmenting BCEWithLogitsLoss with a physics-informed wind-speed monotonicity / saltation residual penalty on era5_wind_speed_10m.",
        "List Paragraph",
        doc,
    )
    add_para_before(
        ch4_el,
        "4. RealSTGNNNet & MultiModalNPZNet: RealSTGNNNet embeds the 6-node regional graph via row-normalised adjacency A_norm = A / deg, 8-d learnable node embeddings, and Linear(in_dim + 8 -> 32) GCN propagation. MultiModalNPZNet fuses Conv2d(6 -> 16) NWP grids (6x16x16), Conv2d(3 -> 16) satellite grids (3x32x32), 24x6x12 sequences, and A_norm on line_b_final_dataset.npz using AdamW(lr = 2e-3) and L1Loss (Figure 10).",
        "List Paragraph",
        doc,
    )
    add_figure_before(
        ch4_el,
        FIG_DIR / "nb03_fig05.png",
        "Figure 10: Direct Line A vs. Line B out-of-sample comparison (best Test ROC-AUC and Test RMSE across 1–15 day horizons; 03_line_b_pytorch_real_layers.ipynb).",
        doc,
    )

    try:
        doc.save(str(DOC_PATH))
        print(f"Refactored Section 3.9 and cleaned old 3.6.2/3.10 in {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver3.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
