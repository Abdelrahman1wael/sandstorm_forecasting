import shutil
import os
from pathlib import Path

DOCS = Path("Documentation").resolve()

lit_dir = DOCS / "literature_and_refs"
pres_dir = DOCS / "presentation"
man_final = DOCS / "manuscripts" / "final"
man_drafts = DOCS / "manuscripts" / "drafts"
reports_dir = DOCS / "dataset_reports"

for d in [lit_dir, pres_dir, man_final, man_drafts, reports_dir]:
    d.mkdir(parents=True, exist_ok=True)

# 1. Final Manuscripts
final_files = [
    "final for Saudi Arabia and especially in Riyadh city.docx",
    "Dust_Storm_Forecasting_Riyadh_rewritten.docx"
]
for f in final_files:
    p = DOCS / f
    if p.exists():
        shutil.move(str(p), str(man_final / f))
        print(f"Moved to final: {f}")

# Move files from old 'final' directory if it exists
old_final = DOCS / "final"
if old_final.exists():
    for f in old_final.glob("*.docx"):
        shutil.move(str(f), str(man_final / f.name))
        print(f"Moved old final to final: {f.name}")
    try:
        old_final.rmdir()
    except Exception as e:
        print(f"Could not remove old final: {e}")

# 2. Drafts and proposals
draft_files = [
    "final for Saudi Arabia and especially in Riyadh city_BACKUP.docx",
    "final_for_Saudi_Arabia_and_especially_in_Riyadh_city_no_duplicates.docx",
    "final.docx",
    "my research proposal.docx",
    "Research.docx"
]
for f in draft_files:
    p = DOCS / f
    if p.exists():
        shutil.move(str(p), str(man_drafts / f))
        print(f"Moved to drafts: {f}")

# 3. Presentation
pres_files = [
    "Review_points_highlighted.docx",
    "COMPLETE_RESEARCH_PRESENTATION_SLIDES_AND_SPEECH.md"
]
for f in pres_files:
    p = DOCS / f
    if p.exists():
        shutil.move(str(p), str(pres_dir / f))
        print(f"Moved to presentation: {f}")

# 4. Literature and references
lit_files = [
    "Environ-13-01-006.pdf",
    "s44407-025-00048-z.pdf",
    "sand_dust_storm_forecasting_taxonomy.pdf",
    "references.docx",
    "weather_ml_literature.csv"
]
for f in lit_files:
    p = DOCS / f
    if p.exists():
        shutil.move(str(p), str(lit_dir / f))
        print(f"Moved to lit: {f}")

json_ref = DOCS / "json_files" / "references.json"
if json_ref.exists():
    shutil.move(str(json_ref), str(lit_dir / "references.json"))
if (DOCS / "json_files").exists():
    try:
        shutil.rmtree(str(DOCS / "json_files"))
    except Exception:
        pass

print("Documentation organization complete!")

