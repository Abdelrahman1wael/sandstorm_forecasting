"""Update the cover page of
FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2_REFS_UPDATED_CLEAN_PERSONAL_EXACT61_REFS.docx
to the USTB Midterm Report (中期报告) cover format with the user's real details.
"""

from pathlib import Path
import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

DOC_PATH = Path(
    r"c:\Users\hp\Desktop\sandstorm_forecasting\01_Documentation\FINAL_USTB_Master_Thesis_Riyadh_Sandstorm_Forecasting_CONDENSED_CH1_CH2_REFS_UPDATED_CLEAN_PERSONAL_EXACT61_REFS.docx"
)


def set_para(p, text: str, size_pt: int | None = None, bold: bool | None = None, align=None) -> None:
    p.text = text
    if align is not None:
        p.alignment = align
    if p.runs:
        r = p.runs[0]
        if size_pt is not None:
            r.font.size = Pt(size_pt)
        if bold is not None:
            r.bold = bold


def main() -> None:
    doc = docx.Document(str(DOC_PATH))

    # Cover page paragraphs 0..13
    set_para(doc.paragraphs[0], "北 京 科 技 大 学", size_pt=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para(doc.paragraphs[1], "硕士学位研究生", size_pt=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para(doc.paragraphs[2], "中期报告", size_pt=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para(doc.paragraphs[3], "", align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para(
        doc.paragraphs[4],
        "论文题目：Machine Learning for Medium- to Long-Term Sand and Dust Storm Forecasting in Saudi Arabia, with Special Emphasis on Riyadh",
        size_pt=14,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )
    set_para(doc.paragraphs[5], "", align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para(doc.paragraphs[6], "", align=WD_ALIGN_PARAGRAPH.LEFT)
    set_para(doc.paragraphs[7], "指 导 教 师：Associate Professor Wen Wei (温维)", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_para(doc.paragraphs[8], "单　   　位：School of Energy and Environmental Engineering, University of Science and Technology Beijing (USTB)", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_para(doc.paragraphs[9], "学　   　号：202461024", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_para(doc.paragraphs[10], "作　   　者：语嫣 yuyan", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_para(doc.paragraphs[11], "专 业 名 称：Master’s Degree in Environmental Engineering", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_para(doc.paragraphs[12], "入 学 时 间：_________________________", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT)
    set_para(doc.paragraphs[13], "20XX年XX月XX日", size_pt=12, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Also update inner title page & rest of document for School / Author / Supervisor consistency
    set_para(doc.paragraphs[20], "Author: 语嫣 yuyan          Supervisor: Associate Professor Wen Wei (温维)")
    set_para(doc.paragraphs[21], "School of Energy and Environmental Engineering, University of Science and Technology Beijing (USTB)")

    reps = [
        ("School of Economics and Management (SEM)", "School of Energy and Environmental Engineering"),
        ("School of Economics and Management", "School of Energy and Environmental Engineering"),
        ("经济管理学院", "能源与环境工程学院"),
    ]
    for p in doc.paragraphs:
        for old, new in reps:
            if old in p.text:
                p.text = p.text.replace(old, new)

    try:
        doc.save(str(DOC_PATH))
        print(f"Successfully updated {DOC_PATH.name}!")
    except PermissionError:
        alt = DOC_PATH.with_name(DOC_PATH.stem + "_MIDTERM_COVER.docx")
        doc.save(str(alt))
        print(f"LOCKED: {DOC_PATH.name} is open in Word; saved updated version to {alt.name}.")


if __name__ == "__main__":
    main()
