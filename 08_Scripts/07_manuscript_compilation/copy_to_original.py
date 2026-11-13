import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
src = PROJECT_ROOT / "Documentation" / "manuscripts" / "final" / "Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2)_latest.docx"
dst_enhanced = PROJECT_ROOT / "Documentation" / "manuscripts" / "final" / "Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2)_enhanced.docx"
dst_orig = PROJECT_ROOT / "Documentation" / "manuscripts" / "final" / "Machine_Learning_for_Medium-_to_Long-Term_Sand_and_Dust_Storm_Forecasting_in_Saudi_Arabia__Riyadh_ (2).docx"

print("Synchronizing latest compiled manuscript...")

for dst in [dst_enhanced, dst_orig]:
    try:
        shutil.copyfile(src, dst)
        print(f"SUCCESS: Synchronized -> {dst.name}")
    except PermissionError:
        print(f"LOCKED: Could not overwrite {dst.name} (currently open in Microsoft Word). Please close Word to update.")
