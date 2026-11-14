"""Generate a publication-grade Gantt chart (07_Figures/research_timeline_gantt.png)
and insert the 7-phase Work Plan table + Gantt diagram into the Introduction (end of Chapter 1)
of the thesis .docx.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
GANTT_PATH = ROOT / "07_Figures" / "research_timeline_gantt.png"
DOC_PRIMARY = ROOT / "01_Documentation" / "FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting.docx"
DOC_LINKS = ROOT / "01_Documentation" / "FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_WITH_LINKS.docx"

PHASES = [
    (
        "1. Literature review and preparation",
        "Sep 2025 – Dec 2025",
        datetime(2025, 9, 1),
        datetime(2025, 12, 31),
        "#1B365D",
        "In-depth literature review, refining the proposal and technical roadmap, setting up the software and hardware environment, and confirming access to ECMWF/CMA forecasts, MODIS and ERA5 data.",
    ),
    (
        "2. Data system construction",
        "Jan 2026 – Apr 2026",
        datetime(2026, 1, 1),
        datetime(2026, 4, 30),
        "#2B5B84",
        "Data collection, quality control, spatiotemporal alignment, missing-value handling and standardization. Feature engineering for dust emission and transport, then the train/validation/test split.",
    ),
    (
        "3. Model development and preliminary experiments",
        "May 2026 – Aug 2026",
        datetime(2026, 5, 1),
        datetime(2026, 8, 31),
        "#3A7CA5",
        "Random Forest and XGBoost baselines, first LSTM and Transformer models, class-imbalance strategies (SMOTE, cost-sensitive learning), hyperparameter tuning and a first benchmark.",
    ),
    (
        "4. Advanced modeling and mid-term review",
        "Sep 2026 – Dec 2026",
        datetime(2026, 9, 1),
        datetime(2026, 12, 31),
        "#D97706",
        "Stacking ensembles, Graph Neural Networks, physics-informed constraints, large-scale model comparison and the mid-term report.",
    ),
    (
        "5. Case studies, interpretability and manuscript",
        "Jan 2027 – Mar 2027",
        datetime(2027, 1, 1),
        datetime(2027, 3, 31),
        "#2E7D32",
        "Retrospective case studies of dust storm events, SHAP and attention-weight analysis, a journal manuscript, and the start of the dissertation draft.",
    ),
    (
        "6. Dissertation completion and pre-defense",
        "Apr 2027 – May 2027",
        datetime(2027, 4, 1),
        datetime(2027, 5, 31),
        "#6B4C9A",
        "Full dissertation draft, revisions after supervisor feedback, and pre-defense preparation.",
    ),
    (
        "7. Final defense and graduation",
        "Jun 2027",
        datetime(2027, 6, 1),
        datetime(2027, 6, 30),
        "#B91C1C",
        "Oral defense, final amendments and submission of graduation materials.",
    ),
]


def make_gantt() -> None:
    fig, ax = plt.subplots(figsize=(11.5, 4.8), dpi=220)
    y_pos = list(range(len(PHASES) - 1, -1, -1))

    for y, (name, period, start, end, color, _) in zip(y_pos, PHASES):
        s_num = mdates.date2num(start)
        e_num = mdates.date2num(end)
        dur = max(e_num - s_num, 20)
        ax.barh(y, dur, left=s_num, height=0.58, color=color, edgecolor="white", linewidth=1.2, alpha=0.92)
        ax.text(s_num + dur / 2, y, period, va="center", ha="center", color="white", fontsize=8.5, fontweight="bold")

    # Midterm milestone line (Nov 2026)
    mid_num = mdates.date2num(datetime(2026, 11, 14))
    ax.axvline(mid_num, color="#B91C1C", linestyle="--", linewidth=1.3)
    ax.text(mid_num + 4, len(PHASES) - 0.35, "Midterm Review (Nov 2026)", color="#B91C1C", fontsize=8.5, fontweight="bold")

    ax.set_yticks(y_pos)
    ax.set_yticklabels([p[0] for p in PHASES], fontsize=9.5, fontweight="bold")
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=30, ha="right", fontsize=8.5)
    ax.set_xlim(mdates.date2num(datetime(2025, 8, 15)), mdates.date2num(datetime(2027, 7, 15)))
    ax.grid(axis="x", linestyle=":", alpha=0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Research Work Plan & Gantt Schedule (Sep 2025 – Jun 2027)", fontsize=12, fontweight="bold", pad=12, color="#1B365D")
    plt.tight_layout()
    fig.savefig(GANTT_PATH, dpi=220)
    plt.close(fig)
    print(f"Saved Gantt chart: {GANTT_PATH}")


def insert_into_doc(doc_path: Path) -> bool:
    doc = docx.Document(str(doc_path))
    if any("Research Schedule and Work Plan" in p.text for p in doc.paragraphs):
        print(f"Work plan already present in {doc_path.name}")
        return True

    ch2 = None
    for p in doc.paragraphs:
        if p.text.strip().startswith("Chapter 2"):
            ch2 = p
            break
    if ch2 is None:
        raise ValueError(f"Chapter 2 anchor not found in {doc_path}")

    ch2.insert_paragraph_before("1.7 Research Schedule and Work Plan", style="Heading 2")
    ch2.insert_paragraph_before(
        "Table 1.1 and the accompanying Gantt diagram summarize the seven-phase research schedule from "
        "initial literature preparation (September 2025) through final dissertation defense (June 2027).",
        style="Normal",
    )

    tbl = doc.add_table(rows=1 + len(PHASES), cols=3)
    tbl.style = "Table Grid"
    headers = ["Phase", "Period", "Main work"]
    for j, h in enumerate(headers):
        c = tbl.rows[0].cells[j]
        c.text = ""
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9)
    for i, (name, period, _, _, _, work) in enumerate(PHASES, start=1):
        for j, val in enumerate([name, period, work]):
            c = tbl.rows[i].cells[j]
            c.text = ""
            r = c.paragraphs[0].add_run(val)
            r.font.size = Pt(9)
    ch2._p.addprevious(tbl._tbl)

    p_img = ch2.insert_paragraph_before("", style="Normal")
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.add_run().add_picture(str(GANTT_PATH), width=Inches(6.0))
    p_cap = ch2.insert_paragraph_before(
        "Figure 1.3: Research Gantt schedule spanning Phases 1–7 (September 2025 – June 2027).",
        style="Normal",
    )
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p_cap.runs:
        r.italic = True
        r.font.size = Pt(9)

    try:
        doc.save(str(doc_path))
        print(f"Updated {doc_path} successfully.")
        return True
    except PermissionError:
        print(f"Skipped {doc_path.name} (locked by another process).")
        return False


def main() -> None:
    make_gantt()
    if DOC_LINKS.exists():
        insert_into_doc(DOC_LINKS)
    if DOC_PRIMARY.exists():
        insert_into_doc(DOC_PRIMARY)


if __name__ == "__main__":
    main()
