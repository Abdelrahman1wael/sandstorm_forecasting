"""
Script to download observed ground station air quality data (PM10 target)
from quotsoft.net public archive for the target period: March 1 - May 31, 2021.
"""

import time
import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm

out_dir = Path("data/raw/ground")
out_dir.mkdir(parents=True, exist_ok=True)

days = pd.date_range("2021-03-01", "2021-05-31")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print(f"Checking / downloading station files for {len(days)} days (2021-03-01 to 2021-05-31)...")

success_count = 0
skipped_count = 0
failed_count = 0

for d in tqdm(days, desc="Downloading Station CSVs"):
    ds = d.strftime("%Y%m%d")
    target_file = out_dir / f"china_sites_{ds}.csv"
    
    if target_file.exists() and target_file.stat().st_size > 1000:
        skipped_count += 1
        continue
        
    url = f"https://quotsoft.net/air/data/china_sites_{ds}.csv"
    retries = 3
    downloaded = False
    
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=60, headers=headers)
            if r.status_code == 200 and len(r.content) > 1000:
                target_file.write_bytes(r.content)
                success_count += 1
                downloaded = True
                break
            elif r.status_code == 404:
                print(f"[404 Not Found] {ds}")
                break
            else:
                time.sleep(2)
        except Exception as e:
            if attempt == retries - 1:
                print(f"[Error] Failed {ds}: {e}")
            time.sleep(2)
            
    if not downloaded:
        failed_count += 1
        
    time.sleep(0.5)

print("\n--- Download Summary ---")
print(f"Total days: {len(days)}")
print(f"Already present: {skipped_count}")
print(f"Newly downloaded: {success_count}")
print(f"Failed / Missing: {failed_count}")
