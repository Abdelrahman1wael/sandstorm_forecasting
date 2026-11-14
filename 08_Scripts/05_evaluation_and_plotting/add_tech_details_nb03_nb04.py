"""Add exact technical details from NB03 (PINN monotonicity loss, 12-epoch best-val
checkpointing) and NB04 (XAI-1 to XAI-6 suite) + export_final_hourly_models.py
into Section 3.9 of MASTER_FINAL-ver3.docx.
"""

from pathlib import Path
import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver3.docx"
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
    ch4_el = next(p for p in doc.paragraphs if p.style.name == "Heading 1" and "Chapter 4" in p.text)._element

    # Update RealPINNNet bullet with exact monotonicity loss equation and training protocol
    for p in doc.paragraphs:
        if p.text.startswith("3. RealPINNNet:"):
            p.text = (
                "3. RealPINNNet: GRU backbone (hidden = 48) with SiLU MLP head (48 -> 24 -> 1), "
                "trained for 12 epochs (batch_size = 128, AdamW lr = 1.5e-3, weight_decay = 1e-3, "
                "best-validation-loss checkpointing) using a composite physics-informed monotonicity loss: "
                "L_PINN = L_BCE(y, y_hat; pos_weight) + 0.05 * mean(ReLU(f_theta(x) - f_theta(x + 0.5 * e_wind))), "
                "where e_wind perturbs standardised era5_wind_speed_10m at the current step (t = 0) by +0.5 SD "
                "to penalise non-physical predictions where higher wind reduces dust-storm probability."
            )
            break

    # Add 3.9.3 Explainable AI Suite (XAI-1 to XAI-6) and Reproducible Export Pipeline before Chapter 4
    if not any("3.9.3" in p.text for p in doc.paragraphs):
        add_para_before(ch4_el, "3.9.3 Explainable AI Suite (XAI-1 to XAI-6) and Export Pipeline", "Heading 3", doc)
        add_para_before(
            ch4_el,
            "All trained models and diagnostic artefacts are orchestrated reproducibly by 08_Scripts/05_evaluation_and_plotting/build_and_run_clean_hourly_notebooks.py and exported by export_final_hourly_models.py into 05_Models/line_a/ and 05_Models/line_b/. Notebook 04 (04_Notebooks/04_explainable_ai_xai_riyadh.ipynb) executes a six-module XAI verification suite on the 168 h clean hourly test partition:",
            "Normal",
            doc,
        )
        add_para_before(
            ch4_el,
            "XAI-1 & XAI-2 (Global Gain, Permutation & Exact SHAP): Computes XGBoost/ExtraTrees test permutation ROC-AUC drops (n_jobs = 1), exact game-theoretic shap.TreeExplainer attributions, directional beeswarm plots, modality-level attribution shares, and local high-risk/low-risk waterfall explanations.",
            "List Paragraph",
            doc,
        )
        add_para_before(
            ch4_el,
            "XAI-3 & XAI-4 (PDP/ICE, Surrogate Rules & Counterfactuals): Generates 1D Partial Dependence and Individual Conditional Expectation (ICE) curves for the top four drivers, 2D interaction surfaces, a depth-3 surrogate decision tree, and +1 SD local counterfactual sensitivity tests.",
            "List Paragraph",
            doc,
        )
        add_para_before(
            ch4_el,
            "XAI-5 & XAI-6 (PyTorch LSTM Saliency, 6-Node Graph & Horizon Shift): Computes input-gradient temporal saliency across the 24-hour LSTM lookback window (Lag -23 h to 0 h; Figure 11), compares Line B saliency against XGBoost SHAP, audits 6-node spatial graph weighted degree, tracks SHAP importance shift from 24 h to 168 h to 360 h, and performs a False Positive / False Negative error-case audit.",
            "List Paragraph",
            doc,
        )
        add_figure_before(
            ch4_el,
            FIG_DIR / "nb04_fig07.png",
            "Figure 11: Real PyTorch LSTM 24-hour lookback temporal saliency (Lag -23 h to 0 h) and Line B vs. XGBoost SHAP agreement (04_explainable_ai_xai_riyadh.ipynb).",
            doc,
        )

    try:
        doc.save(str(DOC_PATH))
        print(f"Added technical details from NB03 & NB04 to {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver4.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
