"""Import all 61 references from 'my research proposal-2 .docx' into the thesis
References section and insert their corresponding [number] citations ONLY inside
Chapter 2 (Literature Review).
"""

from pathlib import Path
import re
import docx

PROPOSAL_PATH = Path(r"c:\Users\hp\Downloads\my research proposal-2 .docx")
TARGET_DOCS = [
    Path(r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting.docx"),
    Path(r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2.docx"),
]

# Exact regex -> [number] rules for Chapter 2 (Literature Review) only
CITE_RULES = [
    (r"(multi-source data[^.]{0,80}?exploratory[^.]*\.)", r"\1 [1, 2]"),
    (r"(Huang et al\.)(?!\s*\[)", r"\1 [3]"),
    (r"(Lu et al\.|500 hPa geopotential height field[^.]*\.)", r"\1 [4]"),
    (r"(Xie et al\.|Hybrid adaptive sampling[^.]*\.)", r"\1 [5]"),
    (r"(AdaBoost ensemble learning framework[^.]*\.)", r"\1 [6]"),
    (r"(Stochastic gradient boosting[^.]*\.)", r"\1 [7]"),
    (r"(CART decision trees, naive Bayes[^.]*\.)", r"\1 [9]"),
    (r"(ANFIS[^.]*\.)", r"\1 [7]"),
    (r"(Al Murayziq et al\.)(?!\s*\[)", r"\1 [8]"),
    (r"(INB-CNN)(?!\s*\[)", r"\1 [10]"),
    (r"(predict the movement direction of sandstorms[^.]*\.)", r"\1 [11]"),
    (r"(infrared satellite cloud-image datasets[^.]*\.)", r"\1 [12]"),
    (r"(stacking ensemble of LSTM and CNN[^.]*\.)", r"\1 [16]"),
    (r"(Multi-dimensional factors \(climate, soil characteristics, NDVI[^.]*\.)", r"\1 [13, 14]"),
    (r"(Thunderstorm and gale prediction:[^.]*\.)", r"\1 [47]"),
    (r"(AeolusStorm)(?!\s*\[)", r"\1 [31]"),
    (r"(Floods:[^.]*\.)", r"\1 [44]"),
    (r"(Snow:[^.]*\.)", r"\1 [52]"),
    (r"(Tropospheric delay[^.]*\.)", r"\1 [32]"),
    (r"(Atmospheric boundary layer height in Beijing[^.]*\.)", r"\1 [34]"),
    (r"(Random forest performed best among linear regression[^.]*\.)", r"\1 [56]"),
    (r"(Regional building power load prediction[^.]*\.)", r"\1 [39]"),
    (r"(Bayesian time-varying coefficient model[^.]*\.)", r"\1 [39]"),
    (r"(Bi-GRU)(?!\s*\[)", r"\1 [48]"),
    (r"(CatBoost and LightGBM)(?!\s*\[)", r"\1 [36]"),
    (r"(Zhang Zhihao)(?!\s*\[)", r"\1 [45, 49]"),
    (r"(variational mode decomposition[^.]*\.)", r"\1 [51]"),
    (r"(Solar irradiance prediction:[^.]*\.)", r"\1 [35]"),
    (r"(EALSTM-QR)(?!\s*\[)", r"\1 [33]"),
    (r"(rail transit[^.]*|decomposition-ensemble, graph convolutional neural networks[^.]*\.)", r"\1 [50]"),
    (r"(expressway interchange exits[^.]{0,120}?SHAP[^.]*\.)", r"\1 [46]"),
    (r"(Maritime accident risk:[^.]*\.)", r"\1 [61]"),
    (r"(RFXG)(?!\s*\[)", r"\1 [53]"),
    (r"(Mugemangango et al\.)(?!\s*\[)", r"\1 [58]"),
    (r"(Internet-of-Things sensors with a random forest[^.]*\.)", r"\1 [60]"),
    (r"(PM₂\.₅ concentration level prediction[^.]*\.)", r"\1 [1, 41]"),
    (r"(VOC concentration[^.]*\.)", r"\1 [42]"),
    (r"(NeuralGCM)(?!\s*\[)", r"\1 [38]"),
]


def load_proposal_refs() -> list[str]:
    pdoc = docx.Document(str(PROPOSAL_PATH))
    refs = []
    for p in pdoc.paragraphs[131:192]:
        t = p.text.strip()
        if t:
            refs.append(t)
    return refs


def process_doc(doc_path: Path, prop_refs: list[str]) -> None:
    if not doc_path.exists():
        return
    doc = docx.Document(str(doc_path))

    # 1. Insert [number] citations ONLY in Chapter 2 (Literature Review)
    in_ch2 = False
    cited_paras = 0
    for p in doc.paragraphs:
        t = p.text.strip()
        if p.style.name == "Heading 1" and t.startswith("Chapter 2"):
            in_ch2 = True
            continue
        if p.style.name == "Heading 1" and t.startswith("Chapter 3"):
            in_ch2 = False
            break
        if not in_ch2 or not t or p.style.name.startswith("Heading"):
            continue

        orig = p.text
        updated = orig
        for pat, repl in CITE_RULES:
            updated = re.sub(pat, repl, updated, count=1)
        if updated != orig:
            p.text = updated
            cited_paras += 1

    # 2. Replace/append numbered References [1]..[61] + existing unique refs
    ref_h_idx = None
    ack_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.style.name == "Heading 1" and p.text.strip().startswith("References"):
            ref_h_idx = i
        elif ref_h_idx is not None and p.style.name == "Heading 1":
            ack_idx = i
            break

    if ref_h_idx is not None and ack_idx is not None:
        existing = [doc.paragraphs[i].text.strip() for i in range(ref_h_idx + 1, ack_idx) if doc.paragraphs[i].text.strip()]
        # Remove old reference paragraphs
        for i in range(ack_idx - 1, ref_h_idx, -1):
            el = doc.paragraphs[i]._element
            if el.getparent() is not None:
                el.getparent().remove(el)

        ack_para = doc.paragraphs[ref_h_idx + 1]
        combined = []
        for idx, ref in enumerate(prop_refs, start=1):
            combined.append(f"[{idx}] {ref}")

        # Append any existing thesis references not already covered
        prop_blob = "\n".join(prop_refs).lower()
        next_num = len(combined) + 1
        for ex in existing:
            clean_ex = re.sub(r"^\[\d+\]\s*", "", ex).strip()
            author_key = clean_ex.split(",")[0].split("(")[0].strip().lower()
            if author_key and author_key not in prop_blob:
                combined.append(f"[{next_num}] {clean_ex}")
                next_num += 1

        for ref_line in combined:
            ack_para.insert_paragraph_before(ref_line, style="List Paragraph")

    try:
        doc.save(str(doc_path))
        print(f"Updated {doc_path.name}: {cited_paras} Lit-Review paragraphs cited, {len(prop_refs)} proposal refs added.")
    except PermissionError:
        out_alt = doc_path.with_name(doc_path.stem + "_REFS_UPDATED.docx")
        doc.save(str(out_alt))
        print(f"{doc_path.name} locked by Word; saved to {out_alt.name} ({cited_paras} Lit-Review paras cited, {len(prop_refs)} proposal refs added).")


def main() -> None:
    prop_refs = load_proposal_refs()
    for p in TARGET_DOCS:
        process_doc(p, prop_refs)


if __name__ == "__main__":
    main()
