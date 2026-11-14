"""Condense Chapter 1 (Introduction) and Chapter 2 (Literature Review) by ~50%
while preserving meaning, bold lead-ins, figures, and tables in
01_Documentation/FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting.docx.
Also updates 1.7 Report Organization.
"""

from pathlib import Path
import re
import docx

DOCX_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting.docx"
)

FILLER_PATTERNS = [
    r"\bIn order to\b",
    r"\bIt is worth noting that\b",
    r"\bIt should be noted that\b",
    r"\bFurthermore,\s*",
    r"\bMoreover,\s*",
    r"\bAdditionally,\s*",
    r"\bIn addition,\s*",
    r"\bAs a result,\s*",
    r"\bConsequently,\s*",
    r"\bSpecifically,\s*",
    r"\bCollectively,\s*",
    r"\bImportantly,\s*",
    r"\bNotably,\s*",
]

KEY_TERMS = re.compile(
    r"(\d+(?:\.\d+)?%?|PM10|PM₂\.₅|AOD|ERA5|CAMS|METAR|KKIA|OERK|SHAP|XAI|"
    r"ROC|AUC|RMSE|XGBoost|Random Forest|SVM|SVR|LSTM|Transformer|TCN|GNN|PINN|"
    r"Riyadh|Saudi|Shamal|NWP|WRF|ECMWF|MODIS|forecast|horizon|gap|dust)",
    re.IGNORECASE,
)


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(\[])", text.strip())
    return [s.strip() for s in parts if s.strip()]


def clean_fillers(s: str) -> str:
    out = s
    for pat in FILLER_PATTERNS:
        out = re.sub(pat, "", out, flags=re.IGNORECASE)
    out = re.sub(r"\s{2,}", " ", out).strip()
    if out and out[0].islower():
        out = out[0].upper() + out[1:]
    return out


def score_sentence(s: str, idx: int, total: int) -> float:
    words = len(s.split())
    if words == 0:
        return -1.0
    hits = len(KEY_TERMS.findall(s))
    nums = len(re.findall(r"\d+(?:\.\d+)?", s))
    cites = len(re.findall(r"\([A-Z][A-Za-z\s,&.-]+\d{4}\)", s))
    density = (hits * 2.0 + nums * 1.5 + cites * 2.0) / max(words, 6)
    pos_bonus = 0.35 if idx == 0 else (0.15 if idx == total - 1 else 0.0)
    return density + pos_bonus


def condense_text(text: str, target_ratio: float = 0.50) -> str:
    lead = ""
    rest = text.strip()
    m = re.match(r"^((?:\d+\.\s*)?[^:.]{3,65}:\s+)(.+)$", rest)
    if m and len(m.group(1).split()) <= 10:
        lead = m.group(1)
        rest = m.group(2)

    sents = split_sentences(rest)
    orig_words = len(text.split())
    target_words = max(10, int(orig_words * target_ratio))

    if len(sents) <= 1:
        cleaned = clean_fillers(rest)
        words = cleaned.split()
        if len(words) > target_words + 6:
            clauses = re.split(r"[;]\s+|,\s+(?:which|while|whereas|because|and|thereby)\s+", cleaned)
            kept = []
            w_cnt = len(lead.split())
            for cl in clauses:
                cw = len(cl.split())
                if w_cnt + cw <= target_words + 6 or not kept:
                    kept.append(cl.rstrip(".,;"))
                    w_cnt += cw
            return (lead + "; ".join(kept)).strip().rstrip(".,;") + "."
        return (lead + cleaned).strip()

    scored = sorted(
        [(score_sentence(s, i, len(sents)), i, clean_fillers(s)) for i, s in enumerate(sents)],
        key=lambda x: x[0],
        reverse=True,
    )
    chosen_idx = set()
    w_sum = len(lead.split())
    for _, i, s in scored:
        sw = len(s.split())
        if not chosen_idx or w_sum + sw <= target_words + 5:
            chosen_idx.add(i)
            w_sum += sw
        if w_sum >= target_words:
            break

    ordered = [clean_fillers(sents[i]) for i in sorted(chosen_idx)]
    result = (lead + " ".join(ordered)).strip()
    if result and result[-1] not in ".!?":
        result += "."
    return result


def main() -> None:
    doc = docx.Document(str(DOCX_PATH))
    in_ch1_ch2 = False
    paras_done = 0
    wb_tot = 0
    wa_tot = 0

    for p in doc.paragraphs:
        t = p.text.strip()
        if p.style.name == "Heading 1" and t.startswith("Chapter 1"):
            in_ch1_ch2 = True
            continue
        if p.style.name == "Heading 1" and t.startswith("Chapter 3"):
            in_ch1_ch2 = False
            break
        if not in_ch1_ch2:
            continue

        if t.startswith("This report is organised into the following chapters."):
            wb_tot += len(t.split())
            new_org = (
                "This thesis is organised into six chapters. Chapter 1 covers Riyadh sandstorm hazards, "
                "motivation, problem statement, ML's role, objectives, and work schedule. Chapter 2 reviews "
                "traditional NWP, ML/DL dust forecasting, forecast error prediction, and research gaps. "
                "Chapter 3 details Riyadh data sources, QC, causal feature engineering, Line A vs. Line B "
                "architectures, balancing, calibration, and verification. Chapter 4 presents 1–15 day "
                "benchmarks and XAI attribution. Chapters 5–6 discuss physical realism, regime-shift "
                "limitations, contributions, and future work."
            )
            p.text = new_org
            wa_tot += len(new_org.split())
            paras_done += 1
            continue

        if p.style.name in ("Normal", "List Paragraph") and len(t.split()) >= 20 and not t.startswith("Figure "):
            wb = len(t.split())
            new_t = condense_text(t, target_ratio=0.50)
            wa = len(new_t.split())
            wb_tot += wb
            wa_tot += wa
            paras_done += 1

            had_bold_lead = bool(p.runs and p.runs[0].bold and ":" in p.runs[0].text)
            p.text = ""
            if had_bold_lead and ":" in new_t:
                idx = new_t.index(":") + 1
                r1 = p.add_run(new_t[:idx])
                r1.bold = True
                p.add_run(new_t[idx:])
            else:
                p.add_run(new_t)

    out_path = DOCX_PATH
    try:
        doc.save(str(out_path))
    except PermissionError:
        out_path = DOCX_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2.docx")
        doc.save(str(out_path))

    pct = (wa_tot / wb_tot * 100) if wb_tot else 0.0
    print(f"Saved: {out_path}")
    print(f"Chapter 1 & 2 paragraphs condensed: {paras_done} | Words: {wb_tot} -> {wa_tot} ({pct:.1f}%)")


if __name__ == "__main__":
    main()
