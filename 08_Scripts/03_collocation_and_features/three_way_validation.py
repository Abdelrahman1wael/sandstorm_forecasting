import sys, os
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent if Path(__file__).resolve().parent.name != 'scripts' else Path(__file__).resolve().parent.parent
_SCRIPTS_ROOT = _PROJECT_ROOT / 'scripts'
if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
"""
Three-Way Validation: MODIS vs AERONET vs CAMS
================================================
For each station, computes pairwise validation stats and generates scatter plots.

Comparisons:
1. MODIS (Combined DT+DB AOD 550nm) vs AERONET (AOD 550nm, daily avg)
2. CAMS (DOD 550nm, T+0 daily avg) vs AERONET (AOD 550nm, daily avg)
3. MODIS vs CAMS

Outputs:
- three_way_stats.csv          — stats table
- three_way_scatter_{station}.png — per-station scatter (3 panels)
- three_way_summary.png        — all stations combined figure
"""

import pandas as pd
import numpy as np
try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    plt = None
    HAS_MPL = False
import os
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
_DEFAULT_BASE = _PROJECT_ROOT
BASE_DIR = Path(os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))).resolve()
DATA_DIR = BASE_DIR / "data"
OUT_DIR = DATA_DIR / "validation"
OUT_DIR.mkdir(exist_ok=True)

# ─── Load MODIS ───
print("Loading MODIS...")
modis_path = DATA_DIR / "modis" / "modis_aod_riyadh.csv"
if not modis_path.exists():
    modis_path = DATA_DIR / "modis" / "modis_aod_riyadh_daily_2015_2024.csv"

if modis_path.exists():
    modis = pd.read_csv(modis_path)
    modis['date'] = pd.to_datetime(modis['date'])
    if 'station' not in modis.columns:
        modis['station'] = "Riyadh_Airport_SDSC"
    if 'modis_dtdb_aod550' not in modis.columns and 'modis_aod550' in modis.columns:
        modis['modis_dtdb_aod550'] = modis['modis_aod550']
    modis = modis[['date', 'station', 'modis_dtdb_aod550']].dropna(subset=['modis_dtdb_aod550'])
else:
    modis = pd.DataFrame(columns=['date', 'station', 'modis_dtdb_aod550'])
print(f"  MODIS rows (non-null): {len(modis)}")

# ─── Load Collocated (AERONET + CAMS) ───
print("Loading collocated AERONET-CAMS data...")
colloc_path = DATA_DIR / "collocated" / "collocated_riyadh.csv"
if not colloc_path.exists():
    colloc_path = DATA_DIR / "collocated" / "collocated_all_stations.csv"

if colloc_path.exists():
    colloc = pd.read_csv(colloc_path)
else:
    colloc = pd.DataFrame(columns=['datetime', 'station', 'lead_time_hours', 'aeronet_aod550', 'aeronet_ae', 'cams_duaod550'])
if 'station' not in colloc.columns:
    colloc['station'] = "Riyadh_Airport_SDSC"
if 'lead_time_hours' not in colloc.columns:
    colloc['lead_time_hours'] = 0.0
else:
    colloc['lead_time_hours'] = colloc['lead_time_hours'].fillna(0.0)
colloc['datetime'] = pd.to_datetime(colloc['datetime'])
colloc['date'] = colloc['datetime'].dt.date

# Daily average AERONET AOD 550nm
print("  Computing daily AERONET averages...")
aeronet_daily = (colloc.groupby(['station', 'date'])
                 .agg(aeronet_aod550=('aeronet_aod550', 'mean'),
                      aeronet_ae=('aeronet_ae', 'mean'),
                      n_aeronet_obs=('aeronet_aod550', 'count'))
                 .reset_index())
aeronet_daily['date'] = pd.to_datetime(aeronet_daily['date'])
print(f"  AERONET daily records: {len(aeronet_daily)}")

# Daily average CAMS DOD 550nm (T+0 only for fairest comparison)
print("  Computing daily CAMS T+0 averages...")
cams_t0 = colloc[colloc['lead_time_hours'] == 0].copy()
if len(cams_t0) == 0:
    # If no exact T+0, use shortest lead time per day
    print("  No exact T+0 found, using shortest lead time per day...")
    colloc['date_tmp'] = colloc['datetime'].dt.date
    idx = colloc.groupby(['station', 'date_tmp'])['lead_time_hours'].idxmin()
    cams_t0 = colloc.loc[idx].copy()

cams_daily = (cams_t0.groupby(['station', colloc.loc[cams_t0.index, 'datetime'].dt.date.rename('date')])
              if len(cams_t0) > 0 else None)

# Simpler approach: daily average CAMS from all lead times <= 12h
cams_short = colloc[colloc['lead_time_hours'] <= 12].copy()
cams_daily = (cams_short.groupby(['station', cams_short['datetime'].dt.date.rename('date')])
              .agg(cams_duaod550=('cams_duaod550', 'mean'),
                   n_cams_obs=('cams_duaod550', 'count'))
              .reset_index())
cams_daily['date'] = pd.to_datetime(cams_daily['date'])
print(f"  CAMS daily records: {len(cams_daily)}")

# ─── Merge all three ───
print("\nMerging datasets...")
# AERONET + CAMS (daily)
ac = pd.merge(aeronet_daily, cams_daily, on=['station', 'date'], how='inner')
# + MODIS
three = pd.merge(ac, modis, on=['station', 'date'], how='inner')
print(f"  Three-way matched records: {len(three)}")
print(f"  Stations: {three['station'].nunique()}")
print(f"  Per station:")
for st in sorted(three['station'].unique()):
    n = len(three[three['station'] == st])
    yr_min = three[three['station'] == st]['date'].dt.year.min()
    yr_max = three[three['station'] == st]['date'].dt.year.max()
    print(f"    {st}: {n} days ({yr_min}-{yr_max})")

# ─── Validation functions ───
def compute_stats(x, y, name_x, name_y):
    """Compute validation statistics between two arrays."""
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    n = len(x)
    if n < 10:
        return {'N': n, 'R': np.nan, 'bias': np.nan, 'RMSE': np.nan,
                'slope': np.nan, 'intercept': np.nan, 'EE_pct': np.nan}

    r, p = stats.pearsonr(x, y)
    bias = np.mean(y - x)
    rmse = np.sqrt(np.mean((y - x)**2))
    slope, intercept, _, _, _ = stats.linregress(x, y)

    # Expected Error envelope (MODIS): ±(0.05 + 0.15*AOD)
    ee_upper = x + 0.05 + 0.15 * x
    ee_lower = x - 0.05 - 0.15 * x
    within_ee = np.sum((y >= ee_lower) & (y <= ee_upper))
    ee_pct = 100.0 * within_ee / n

    return {'N': n, 'R': round(r, 3), 'bias': round(bias, 4),
            'RMSE': round(rmse, 4), 'slope': round(slope, 3),
            'intercept': round(intercept, 4), 'EE_pct': round(ee_pct, 1)}

# ─── Compute stats for all stations ───
print("\n" + "="*80)
print("THREE-WAY VALIDATION RESULTS")
print("="*80)

all_stats = []
stations = sorted(three['station'].unique())

for station in stations:
    df = three[three['station'] == station]

    # 1. MODIS vs AERONET
    s1 = compute_stats(df['aeronet_aod550'].values, df['modis_dtdb_aod550'].values,
                       'AERONET', 'MODIS')
    s1.update({'station': station, 'comparison': 'MODIS_vs_AERONET'})

    # 2. CAMS vs AERONET
    s2 = compute_stats(df['aeronet_aod550'].values, df['cams_duaod550'].values,
                       'AERONET', 'CAMS')
    s2.update({'station': station, 'comparison': 'CAMS_vs_AERONET'})

    # 3. MODIS vs CAMS
    s3 = compute_stats(df['cams_duaod550'].values, df['modis_dtdb_aod550'].values,
                       'CAMS', 'MODIS')
    s3.update({'station': station, 'comparison': 'MODIS_vs_CAMS'})

    all_stats.extend([s1, s2, s3])

stats_df = pd.DataFrame(all_stats)
stats_df = stats_df[['station', 'comparison', 'N', 'R', 'bias', 'RMSE', 'slope', 'intercept', 'EE_pct']]

# Print results
for comp in ['MODIS_vs_AERONET', 'CAMS_vs_AERONET', 'MODIS_vs_CAMS']:
    print(f"\n--- {comp.replace('_', ' ')} ---")
    sub = stats_df[stats_df['comparison'] == comp]
    print(sub.to_string(index=False))

# Save stats
stats_df.to_csv(OUT_DIR / "three_way_stats.csv", index=False)
print(f"\nStats saved to {OUT_DIR / 'three_way_stats.csv'}")

# ─── Scatter plots per station ───
if HAS_MPL:
    print("\nGenerating scatter plots...")
    colors = {'MODIS_vs_AERONET': '#2196F3', 'CAMS_vs_AERONET': '#FF9800', 'MODIS_vs_CAMS': '#4CAF50'}
    for station in stations:
        df = three[three['station'] == station]
        if len(df) < 10:
            continue
        fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
        plt.tight_layout()
        fig.savefig(OUT_DIR / f"three_way_scatter_{station}.png", dpi=150, bbox_inches='tight')
        plt.close(fig)
else:
    print("\n[INFO] Matplotlib not installed in current environment; skipping PNG plot rendering.")

# ─── Also save the merged three-way dataset ───
three.to_csv(OUT_DIR / "three_way_merged.csv", index=False)
print(f"\nMerged dataset saved: {OUT_DIR / 'three_way_merged.csv'} ({len(three)} rows)")

print("\nDone! Check data/validation/ for all outputs.")
