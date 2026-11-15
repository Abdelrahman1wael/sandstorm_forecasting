from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Pt

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
MASTER_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_captions_TOC_fixed_v3.docx"
BLIND_PATH = ROOT / "01_Documentation" / "USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_BLIND_REVIEW.docx"

CHAPTER_BRIDGES = {
    "Chapter 1": (
        "This opening chapter establishes the environmental, health, aviation, and economic urgency of sand and dust storm (SDS) "
        "forecasting across Greater Riyadh, defines the research objectives and multi-horizon scope (24–360 h), and outlines the "
        "seven-phase research schedule."
    ),
    "Chapter 2": (
        "Building on the operational challenges identified in Chapter 1, this chapter reviews numerical weather prediction (NWP), "
        "classical machine learning, and hybrid deep-learning approaches to dust forecasting, synthesizing the methodological gaps "
        "that motivate our strictly causal dual-line framework."
    ),
    "Chapter 3": (
        "To address the data-leakage, multi-horizon, and interpretability gaps identified in Chapter 2, this chapter details the "
        "86,928-hour multi-modal dataset, anti-leakage cleaning and chronological split protocol (10,142 / 2,114 / 2,114 6-hourly "
        "samples), Main Line A and Main Line B model architectures, and the six-module Explainable AI (XAI-1 to XAI-6) pipeline."
    ),
    "Chapter 4": (
        "Following the experimental protocol and model specifications defined in Chapter 3, this chapter presents the empirical "
        "evaluation across 24–360 h horizons: first auditing Main Line A 5-fold cross-validation and out-of-sample test skill, "
        "then benchmarking Main Line B PyTorch prototypes, and finally verifying physical drivers through XAI-1 to XAI-6."
    ),
    "Chapter 5": (
        "While Chapter 4 quantified predictive discrimination, calibration, and regression boundaries, operational adoption requires "
        "interpreting what the models actually learned and where they fall short. This chapter evaluates the physical realism of "
        "the XAI attributions, analyzes Line A versus Line B trade-offs, and transparently documents prototype limitations."
    ),
    "Chapter 6": (
        "Drawing together the empirical evidence of Chapter 4 and the critical limitations analyzed in Chapter 5, this final "
        "chapter synthesizes the scientific and operational contributions of this mid-term prototype, provides actionable "
        "recommendations for Saudi civil defense and aviation planners, and defines the Stage-2 final-thesis roadmap."
    ),
}


def insert_para_after(anchor_p, text, doc):
    new_p = OxmlElement("w:p")
    anchor_p._p.addnext(new_p)
    p = anchor_p.__class__(new_p, doc._body)
    if "Normal" in [s.name for s in doc.styles]:
        p.style = doc.styles["Normal"]
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    return p


def add_flow_bridges(doc_path: Path):
    doc = Document(str(doc_path))

    # 1. Insert chapter-opening bridge paragraphs where Heading 1 is followed immediately by Heading 2
    h1_indices = [i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 1" and "Chapter " in p.text]
    for idx in reversed(h1_indices):
        h1_p = doc.paragraphs[idx]
        next_p = doc.paragraphs[idx + 1] if idx + 1 < len(doc.paragraphs) else None
        if next_p is not None and next_p.style.name == "Heading 2":
            for ch_key, bridge_txt in CHAPTER_BRIDGES.items():
                if h1_p.text.strip().startswith(ch_key):
                    insert_para_after(h1_p, bridge_txt, doc)
                    break

    # 2. Add smooth subsection transitions inside Chapter 4 (before 4.3 and before 4.4)
    h43 = next((i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 2" and p.text.strip().startswith("4.3 ")), None)
    if h43 is not None and "sequence and graph-structured architectures" not in doc.paragraphs[h43 - 1].text:
        new_p = OxmlElement("w:p")
        doc.paragraphs[h43]._p.addprevious(new_p)
        p = doc.paragraphs[h43].__class__(new_p, doc._body)
        if "Normal" in [s.name for s in doc.styles]:
            p.style = doc.styles["Normal"]
        r = p.add_run(
            "Having established the classification skill and regression variance limits of tabular Line A models, we next evaluate "
            "whether sequence and graph-structured architectures in Main Line B improve multi-day discrimination or continuous PM₁₀ estimation."
        )
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    h44 = next((i for i, p in enumerate(doc.paragraphs) if p.style.name == "Heading 2" and p.text.strip().startswith("4.4 ")), None)
    if h44 is not None and "physical mechanisms drive" not in doc.paragraphs[h44 - 1].text:
        new_p = OxmlElement("w:p")
        doc.paragraphs[h44]._p.addprevious(new_p)
        p = doc.paragraphs[h44].__class__(new_p, doc._body)
        if "Normal" in [s.name for s in doc.styles]:
            p.style = doc.styles["Normal"]
        r = p.add_run(
            "Beyond aggregate accuracy metrics, validating operational trustworthiness requires examining which physical mechanisms drive "
            "forecast skill across horizons; Section 4.4 therefore audits the 168 h clean hourly models via XAI-1 through XAI-6."
        )
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    doc.save(str(doc_path))
    print(f"Updated narrative flow in {doc_path.name}")


def main():
    add_flow_bridges(MASTER_PATH)
    add_flow_bridges(BLIND_PATH)


if __name__ == "__main__":
    main()
