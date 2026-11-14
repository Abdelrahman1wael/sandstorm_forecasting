"""Update Section 3.4.2 in MASTER_FINAL-ver1.docx (or save to -ver2.docx if locked)
with verified Yeo-Johnson normalization and cost-sensitive class balancing.
"""

from pathlib import Path
import docx

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver1.docx"
)


def main() -> None:
    doc = docx.Document(str(DOC_PATH))
    h = next(i for i, x in enumerate(doc.paragraphs) if x.style.name == "Heading 3" and "3.4.2" in x.text)
    doc.paragraphs[h].text = "3.4.2 Purge-Gapped Split, Train-Only Yeo-Johnson Normalization, and Cost-Sensitive Balancing"
    doc.paragraphs[h + 1].text = (
        "Atmospheric particulate concentrations and dust predictors in desert environments exhibit extreme positive skewness "
        "(up to 11.79 in pm10_clean_ugm3) and heavy Pareto tails reaching 4,800.0 μg/m³. To prevent high-variance outliers "
        "from destabilising neural gradients and linear/tree objectives without leaking future regime statistics, Notebook 01 "
        "enforces a 360-hour (15-day) purge gap between the 70% training partition (2015–2021; 60,849 h in Notebook 01 / "
        "61,176 h in the calendar TVT split), 15% validation partition (2022), and 15% test partition (2023–2024). Median "
        "imputation (SimpleImputer) and Yeo-Johnson power transformation (PowerTransformer) are fitted strictly via maximum "
        "likelihood on the 70% training split and frozen before transforming validation and test features: "
        "psi(lambda, y) = ((y + 1)^lambda - 1) / lambda [for lambda != 0, y >= 0]; ln(y + 1) [for lambda = 0, y >= 0]; "
        "-((-y + 1)^(2 - lambda) - 1) / (2 - lambda) [for lambda != 2, y < 0]; -ln(-y + 1) [for lambda = 2, y < 0]."
    )

    s343 = next(i for i, x in enumerate(doc.paragraphs) if "3.4.3" in x.text)
    np_p = doc.add_paragraph(
        "Because dust-event prevalence shifts sharply across chronological splits (7.47% in Train 2015–2021, 10.51% in "
        "Validation 2022, and 1.79% in Test 2023–2024), synthetic oversampling (SMOTE) is omitted to avoid temporal "
        "autocorrelation leakage across hourly sequences. Instead, class imbalance is handled through cost-sensitive "
        "learning—balanced class_weight in Line A tabular classifiers and positive-class pos_weight inside "
        "BCEWithLogitsLoss for Line B PyTorch networks—paired with validation-set probability calibration while keeping "
        "the 2023–2024 test partition untouched at its natural prevalence.",
        style="Normal",
    )
    el = np_p._element
    el.getparent().remove(el)
    doc.paragraphs[s343]._element.addprevious(el)

    try:
        doc.save(str(DOC_PATH))
        print(f"Updated {DOC_PATH.name}.")
    except PermissionError:
        alt = DOC_PATH.with_name("FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_MASTER_FINAL-ver2.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved to {alt.name}.")


if __name__ == "__main__":
    main()
