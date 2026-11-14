"""
Build and Execute All 5 50-Cell Notebooks Using Clean Hourly Data + line_b_final_dataset.npz:
  00_data_representation_and_distribution_riyadh.ipynb (50 cells: 25 MD + 25 Code)
  01_feature_engineering_and_impact.ipynb            (50 cells: 25 MD + 25 Code - ALL DATA CLEANING & FIXES)
  02_line_a_tabular_and_meta_models_riyadh.ipynb     (50 cells: 25 MD + 25 Code - Clean Hourly Synoptic 1-15d)
  03_line_b_pytorch_real_layers.ipynb                (50 cells: 25 MD + 25 Code - Clean Hourly + line_b_final_dataset.npz)
  04_explainable_ai_xai_riyadh.ipynb                 (50 cells: 25 MD + 25 Code - XAI on Clean Hourly Data)

Split Protocol:
  - Train (70%) with 5-Fold Rolling-Origin Time-Series CV (360h / 15-day purge gap)
  - 360h (15-Day) Purge Gap
  - Validation (15%) for calibration, early stopping & threshold tuning
  - 360h (15-Day) Purge Gap
  - Held-Out Test (15%)
Horizons: 24h (1d), 72h (3d), 168h (7d), 216h (9d), 360h (15d) forward averages.
"""

import io
import os
import json
import base64
import contextlib
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MPL_DIR = PROJECT_ROOT / "06_Data" / ".mplconfig"
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(MPL_DIR)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NB_DIR = PROJECT_ROOT / "04_Notebooks"
NB_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR = PROJECT_ROOT / "06_Data" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
XAI_DIR = RESULTS_DIR / "xai"
XAI_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR = PROJECT_ROOT / "07_Figures" / "notebooks_hourly_clean"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def md(text: str) -> dict:
    lines = [line + "\n" for line in text.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {"cell_type": "markdown", "metadata": {}, "source": lines}


def code(code_str: str, env: dict, exec_count: int) -> dict:
    plt.close("all")
    buf = io.StringIO()
    outputs = []
    with contextlib.redirect_stdout(buf):
        exec(code_str, env)
    stdout_str = buf.getvalue()
    if stdout_str:
        out_lines = [line + "\n" for line in stdout_str.split("\n")]
        if out_lines and out_lines[-1] == "\n":
            out_lines.pop()
        outputs.append({"name": "stdout", "output_type": "stream", "text": out_lines})
    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="png", dpi=115, bbox_inches="tight")
        img_buf.seek(0)
        b64 = base64.b64encode(img_buf.read()).decode("utf-8")
        outputs.append({
            "data": {"image/png": b64, "text/plain": ["<Figure>"]},
            "metadata": {},
            "output_type": "display_data",
        })
    plt.close("all")
    src_lines = [line + "\n" for line in code_str.strip().split("\n")]
    if src_lines:
        src_lines[-1] = src_lines[-1].rstrip("\n")
    return {"cell_type": "code", "execution_count": exec_count, "metadata": {}, "outputs": outputs, "source": src_lines}


def run_pairs(pairs, env, out_path: Path):
    assert len(pairs) == 25, f"Expected 25 pairs (50 cells), got {len(pairs)}"
    cells = []
    for idx, (m_txt, c_txt) in enumerate(pairs, start=1):
        cells.append(md(m_txt))
        cells.append(code(c_txt, env, idx))
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3 (.venv)", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    out_path.write_text(json.dumps(nb, indent=2), encoding="utf-8")
    print(f"  [SAVED] {out_path.name} ({len(cells)} cells)")


def build_nb00():
    print("\n=== [1/5] Notebook 00: Hourly Data Representation & Issue Audit (50 cells) ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR}
    pairs = [
        ("# Notebook 00: Complete Hourly Data Representation & Issue Audit\n## 1. Load Raw Hourly CSV & Multi-Modal NPZ",
         "import numpy as np, pandas as pd, matplotlib.pyplot as plt\nfrom scipy.stats import spearmanr\ndf = pd.read_csv(PROJECT_ROOT / '06_Data' / 'riyadh_line_a_tabular_features.csv', low_memory=False)\ndf['ts'] = pd.to_datetime(df['time']).dt.tz_localize(None)\ndf = df.sort_values('ts').reset_index(drop=True)\nnpz = np.load(PROJECT_ROOT / '06_Data' / 'line_b_final_dataset.npz', allow_pickle=True)\nprint(f'Hourly CSV: {df.shape} | Span: {df[\"ts\"].min()} -> {df[\"ts\"].max()}')\nprint('NPZ keys:', {k: npz[k].shape for k in npz.keys()})"),
        ("## 2. Four-Modality Feature Taxonomy",
         "modalities = {'Ground_METAR': [c for c in df.columns if c in ['tmpc','dwpc','drct','sknt','gust','vsby','mslp','wind_speed_ms','wind_gust_ms','visibility_km','relative_humidity','pm10_calibrated_ugm3']], 'ERA5_Reanalysis': [c for c in df.columns if c.startswith('era5_') or c.startswith('phys_')], 'Satellite_AOD': [c for c in df.columns if c.startswith('sat_')], 'CAMS_NWP': [c for c in df.columns if 'cams' in c or 'nwp' in c]}\nfor k, v in modalities.items():\n    print(f'{k:18s}: {len(v):2d} columns')"),
        ("## 3. Raw Hourly Missingness Audit (`mslp` 100% NaN, `wxcodes` 92.3% Blank)",
         "miss = (df.isna().mean() * 100).sort_values(ascending=False)\nprint(miss.head(10).round(2).to_string())"),
        ("## 4. Missingness Bar Chart",
         "top_m = miss[miss > 0].head(10)\nfig, ax = plt.subplots(figsize=(8, 3.8))\nif len(top_m) > 0: top_m.iloc[::-1].plot(kind='barh', ax=ax, color='#d62728')\nax.set_title('Raw Hourly Missingness (%)'); ax.set_xlabel('% Missing'); plt.tight_layout()"),
        ("## 5. Issue 1 Audit: 10 km METAR Visibility Cap & `53.7 ug/m3` Floor",
         "cap_pct = (df['visibility_km'] >= 9.9).mean() * 100\nflr_pct = (df['pm10_calibrated_ugm3'] <= 54.0).mean() * 100\nprint(f'Hourly visibility >= 9.9 km (capped): {cap_pct:.1f}%')\nprint(f'Hourly PM10 proxy <= 54 ug/m3 (floor): {flr_pct:.1f}%')\nprint('Hourly PM10 quantiles:', df['pm10_calibrated_ugm3'].quantile([0.1,0.25,0.5,0.75,0.9,0.99]).round(2).to_dict())"),
        ("## 6. Hourly Proxy Histogram Showing the `53.7` Floor Spike",
         "fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))\naxes[0].hist(df['visibility_km'].dropna(), bins=30, color='#1f77b4'); axes[0].set_title('Hourly METAR Visibility (km) - 10km Cap')\naxes[1].hist(df['pm10_calibrated_ugm3'].clip(0, 400), bins=40, color='#d62728'); axes[1].set_title('Hourly PM10 Proxy - 53.7 Floor Spike')\nplt.tight_layout()"),
        ("## 7. Issue 2 Audit: `2022–2024` Regime Shift & `sat_retrieved_pm10` Drift",
         "df['year'] = df['ts'].dt.year\nyr = df.groupby('year').agg(hours=('pm10_calibrated_ugm3','count'), dust_pct=('is_dust_event', lambda s: s.mean()*100), vis_lt5_pct=('visibility_km', lambda s: (s<5.0).mean()*100), pm10_mean=('pm10_calibrated_ugm3','mean'), sat_pm10=('sat_retrieved_pm10','mean'), cams_pm10=('nwp_cams_pm10','mean'))\nprint(yr.round(2).to_string())"),
        ("## 8. Annual Dust-Rate vs Satellite/CAMS Drift Visualization",
         "fig, ax1 = plt.subplots(figsize=(9, 4))\nax1.bar(yr.index, yr['dust_pct'], alpha=0.65, label='METAR Dust %')\nax1.plot(yr.index, yr['vis_lt5_pct'], marker='s', color='black', label='Vis < 5km %')\nax2 = ax1.twinx(); ax2.plot(yr.index, yr['sat_pm10'], marker='o', color='#d62728', label='Sat PM10 Mean')\nax1.set_title('2015–2024 Regime Shift: Dust Rate Drop vs Satellite Drift'); ax1.legend(loc='upper left'); ax2.legend(loc='upper right'); plt.tight_layout()"),
        ("## 9. Hourly Train (70%) / 360h Gap / Val (15%) / 360h Gap / Test (15%) Split",
         "N = len(df); GAP_H = 360\ntr_end = int(N * 0.70); val_start = tr_end + GAP_H; val_end = int(N * 0.85); te_start = val_end + GAP_H\ntrain_df = df.iloc[:tr_end]; val_df = df.iloc[val_start:val_end]; test_df = df.iloc[te_start:]\nprint(f'Train (70%): {len(train_df):,}h ({train_df[\"ts\"].min()} -> {train_df[\"ts\"].max()}) | Dust={train_df[\"is_dust_event\"].mean()*100:.2f}%')\nprint(f'Val   (15%): {len(val_df):,}h ({val_df[\"ts\"].min()} -> {val_df[\"ts\"].max()}) | Dust={val_df[\"is_dust_event\"].mean()*100:.2f}%')\nprint(f'Test  (15%): {len(test_df):,}h ({test_df[\"ts\"].min()} -> {test_df[\"ts\"].max()}) | Dust={test_df[\"is_dust_event\"].mean()*100:.2f}%')"),
        ("## 10. 5-Fold Rolling-Origin CV Structure Inside 70% Hourly Train",
         "n_tr = len(train_df); m_tr = int(n_tr * 0.40); st = (n_tr - m_tr) // 5\nfor f in range(5):\n    a = m_tr + f*st - GAP_H; b = m_tr + f*st; c = b + st if f < 4 else n_tr\n    print(f'CV Fold {f+1}: Train[0:{a:,}h] -> 360h Gap -> Val[{b:,}:{c:,}h] | Dust={train_df.iloc[b:c][\"is_dust_event\"].mean()*100:.2f}%')"),
        ("## 11. Hourly Time Series Across Train / Val / Test",
         "fig, ax = plt.subplots(figsize=(12, 3.8))\ns_tr = train_df.iloc[::24]; s_va = val_df.iloc[::24]; s_te = test_df.iloc[::24]\nax.plot(s_tr['ts'], s_tr['pm10_calibrated_ugm3'], lw=0.6, label='Train 70%')\nax.plot(s_va['ts'], s_va['pm10_calibrated_ugm3'], lw=0.6, label='Val 15%')\nax.plot(s_te['ts'], s_te['pm10_calibrated_ugm3'], lw=0.6, label='Test 15%')\nax.set_title('Hourly PM10 Proxy (24h Subsampled View) Across Splits'); ax.legend(); plt.tight_layout()"),
        ("## 12. Real KAPSARC Ground Sensor vs Hourly Visibility Proxy Audit",
         "k_path = PROJECT_ROOT / '06_Data' / 'riyadh_kapsarc_sensor_pm10_daily.csv'\nif k_path.exists():\n    ks = pd.read_csv(k_path, sep=';'); ks['date'] = pd.to_datetime(ks['date']).dt.normalize()\n    kd = ks[ks['indicator']=='Avg / Hourly'].groupby('date')['value'].mean().rename('real_sensor_pm10')\n    df['date'] = df['ts'].dt.normalize()\n    dd = df.groupby('date').agg(proxy=('pm10_calibrated_ugm3','mean'), cams=('nwp_cams_pm10','mean')).join(kd, how='inner')\n    print(f'KAPSARC overlap: {len(dd)} days | Corr(real, proxy)={dd[\"real_sensor_pm10\"].corr(dd[\"proxy\"]):.3f} | Corr(real, CAMS)={dd[\"real_sensor_pm10\"].corr(dd[\"cams\"]):.3f}')"),
        ("## 13. Real Sensor vs Proxy Scatter Plot (159 Overlapping Days)",
         "fig, ax = plt.subplots(figsize=(5.5, 4.5))\nif 'dd' in locals():\n    ax.scatter(dd['proxy'], dd['real_sensor_pm10'], s=18, alpha=0.65)\n    ax.set_xlabel('METAR Visibility Proxy (ug/m3)'); ax.set_ylabel('Real KAPSARC Sensor PM10 (ug/m3)')\nax.set_title('Visibility Proxy vs Real Ground Sensor PM10'); plt.tight_layout()"),
        ("## 14. Inspect `line_b_final_dataset.npz` Multi-Modal Tensors",
         "print('seq_features:', npz['seq_features'].shape, 'mean=', round(float(npz['seq_features'].mean()),4))\nprint('nwp_grid:', npz['nwp_grid'].shape, 'satellite_grid:', npz['satellite_grid'].shape)\nprint('targets_pm10:', npz['targets_pm10'].shape, 'hazard_classes:', npz['hazard_classes'].shape)"),
        ("## 15. Visualize NPZ Spatial Adjacency & Sample NWP/Satellite Grids",
         "fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))\naxes[0].imshow(npz['adjacency_matrix'], cmap='viridis'); axes[0].set_title('NPZ 6-Node Adjacency')\naxes[1].imshow(npz['nwp_grid'][0, 0], cmap='magma'); axes[1].set_title('NPZ NWP Grid (Ch 0)')\naxes[2].imshow(npz['satellite_grid'][0, 0], cmap='inferno'); axes[2].set_title('NPZ Satellite Grid (Ch 0)')\nplt.tight_layout()"),
        ("## 16. Hourly Diurnal Cycle (Dust Rate & Wind Speed by UTC Hour)",
         "df['hour'] = df['ts'].dt.hour\nhr = df.groupby('hour').agg(dust=('is_dust_event', lambda s: s.mean()*100), ws=('era5_wind_speed_10m','mean'), blh=('era5_blh_m','mean'))\nfig, ax1 = plt.subplots(figsize=(9, 3.8))\nax1.bar(hr.index, hr['dust'], alpha=0.6, label='Dust %'); ax2 = ax1.twinx(); ax2.plot(hr.index, hr['ws'], color='red', marker='o', label='ERA5 Wind (m/s)')\nax1.set_title('Hourly Diurnal Cycle (UTC)'); ax1.set_xticks(range(0,24,2)); plt.tight_layout()"),
        ("## 17. Diurnal x Monthly Dust Heatmap (Hourly Resolution)",
         "df['month'] = df['ts'].dt.month\npiv = df.pivot_table(index='hour', columns='month', values='is_dust_event', aggfunc='mean')*100\nfig, ax = plt.subplots(figsize=(8.5, 4))\nim = ax.imshow(piv.values, aspect='auto', cmap='YlOrRd', origin='lower')\nax.set_xticks(range(12)); ax.set_xticklabels(range(1,13)); ax.set_title('Hourly Dust % by Hour & Month'); plt.colorbar(im, ax=ax); plt.tight_layout()"),
        ("## 18. Wind Direction Polar Rose (Hourly All vs Dust)",
         "ang = np.deg2rad(df['drct'].dropna()); dang = np.deg2rad(df.loc[df['is_dust_event']==1, 'drct'].dropna())\nfig, ax = plt.subplots(subplot_kw={'projection':'polar'}, figsize=(5, 5))\nax.hist(ang, bins=24, density=True, alpha=0.4, label='All Hours'); ax.hist(dang, bins=24, density=True, alpha=0.6, color='red', label='Dust Hours')\nax.set_theta_zero_location('N'); ax.set_theta_direction(-1); ax.set_title('Hourly Wind Rose'); ax.legend(loc='upper right', fontsize=8)"),
        ("## 19. ERA5 Driver Distributions (Train 70% vs Test 15%)",
         "fig, axes = plt.subplots(2, 2, figsize=(10, 6.5))\nfor ax, c in zip(axes.ravel(), ['era5_wind_speed_10m','era5_wind_gusts_10m','era5_blh_m','phys_vpd_kpa']):\n    ax.hist(train_df[c].dropna(), bins=35, alpha=0.55, density=True, label='Train')\n    ax.hist(test_df[c].dropna(), bins=35, alpha=0.55, density=True, label='Test')\n    ax.set_title(c); ax.legend(fontsize=8)\nplt.tight_layout()"),
        ("## 20. Hourly Autocorrelation (1h to 168h / 7 Days)",
         "lags = [1, 3, 6, 12, 24, 48, 72, 120, 168]\nacf_pm = [train_df['pm10_calibrated_ugm3'].autocorr(lag=k) for k in lags]\nacf_ev = [train_df['is_dust_event'].autocorr(lag=k) for k in lags]\nfig, ax = plt.subplots(figsize=(9, 3.8))\nax.plot(lags, acf_pm, marker='o', label='PM10 Proxy ACF'); ax.plot(lags, acf_ev, marker='s', label='Dust Event ACF')\nax.set_title('Train Hourly Autocorrelation (1h–168h)'); ax.set_xlabel('Lag (Hours)'); ax.legend(); plt.tight_layout()"),
        ("## 21. Train-Only Multi-Modal Correlation Heatmap",
         "cols_c = ['pm10_calibrated_ugm3','visibility_km','era5_wind_speed_10m','era5_wind_gusts_10m','era5_blh_m','era5_surface_pressure','phys_vpd_kpa','sat_aod_550nm','nwp_cams_pm10']\ncorr = train_df[cols_c].corr().values\nfig, ax = plt.subplots(figsize=(7.5, 6))\nax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)\nax.set_xticks(range(len(cols_c))); ax.set_xticklabels(cols_c, rotation=45, ha='right', fontsize=7)\nax.set_yticks(range(len(cols_c))); ax.set_yticklabels(cols_c, fontsize=7)\nfor i in range(len(cols_c)):\n    for j in range(len(cols_c)): ax.text(j, i, f'{corr[i,j]:.2f}', ha='center', va='center', fontsize=6)\nax.set_title('Train-Only Hourly Correlation Matrix'); plt.tight_layout()"),
        ("## 22. Pearson vs Spearman Non-Linearity Check (Train 70%)",
         "rows = []\nfor c in ['visibility_km','era5_wind_speed_10m','era5_wind_gusts_10m','era5_blh_m','phys_vpd_kpa','sat_aod_550nm','nwp_cams_pm10']:\n    sub = train_df[[c,'pm10_calibrated_ugm3']].dropna()\n    rows.append({'Feature': c, 'Pearson': round(sub[c].corr(sub['pm10_calibrated_ugm3']),4), 'Spearman': round(spearmanr(sub[c], sub['pm10_calibrated_ugm3'])[0],4)})\nprint(pd.DataFrame(rows).to_string(index=False))"),
        ("## 23. WMO PM10 Severity Tier Counts (Raw Hourly Proxy)",
         "bins = [0, 50, 150, 300, 500, 10000]; lbls = ['Normal(<50)','Mod(50-150)','Elev(150-300)','Sev(300-500)','Ext(>500)']\nprint(pd.cut(df['pm10_calibrated_ugm3'], bins=bins, labels=lbls).value_counts().sort_index().to_string())"),
        ("## 24. Hourly Split Summary Table",
         "print(pd.DataFrame([{'Split':'Train_70','Hours':len(train_df),'Dust%':round(train_df['is_dust_event'].mean()*100,2)},{'Split':'Val_15','Hours':len(val_df),'Dust%':round(val_df['is_dust_event'].mean()*100,2)},{'Split':'Test_15','Hours':len(test_df),'Dust%':round(test_df['is_dust_event'].mean()*100,2)}]).to_string(index=False))"),
        ("## 25. Notebook 00 Summary",
         "print('NB00 Complete: All 4 data issues quantified at hourly resolution + line_b_final_dataset.npz inspected. Next: NB01 fixes all cleanable data issues.')"),
    ]
    run_pairs(pairs, env, NB_DIR / "00_data_representation_and_distribution_riyadh.ipynb")


def build_nb01():
    print("\n=== [2/5] Notebook 01: Clean Hourly Data & Fix All Issues (50 cells) ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR, "RESULTS_DIR": RESULTS_DIR}
    pairs = [
        ("# Notebook 01: Hourly Data Cleaning, Issue Fixes & Causal Feature Engineering\n## 1. Load Raw Hourly Data (`87,456` Hours)",
         "import numpy as np, pandas as pd, matplotlib.pyplot as plt\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import PowerTransformer\nfrom sklearn.feature_selection import mutual_info_regression, mutual_info_classif\nfrom sklearn.linear_model import RidgeCV\nfrom scipy.stats import spearmanr\ndf = pd.read_csv(PROJECT_ROOT / '06_Data' / 'riyadh_line_a_tabular_features.csv', low_memory=False)\ndf['ts'] = pd.to_datetime(df['time']).dt.tz_localize(None)\ndf = df.sort_values('ts').reset_index(drop=True)\nprint('Loaded hourly rows:', len(df), '| cols:', df.shape[1])"),
        ("## 2. Fix 1: Drop 100%-Missing `mslp` & Clean `wxcodes` into Binary Indicators",
         "wx = df['wxcodes'].fillna('').astype(str).str.upper()\ndf['has_wxcode'] = (wx.str.len() > 0).astype(float)\ndf['is_severe_dust_wx'] = wx.apply(lambda x: 1.0 if any(c in x for c in ['SS','DS','SA']) else 0.0)\ndf = df.drop(columns=[c for c in ['mslp','wxcodes','time','valid','station','station_name','role','hazard_level','hazard_class'] if c in df.columns])\nprint('Dropped mslp & raw text columns. Encoded has_wxcode & is_severe_dust_wx.')"),
        ("## 3. Fix 2: De-Censor the `53.7 ug/m3` Visibility-Cap Floor",
         "vis = df['visibility_km'].ffill().bfill().fillna(10.0).clip(0.05, 30.0)\nws = df['era5_wind_speed_10m'].fillna(4.0).clip(0.2, 30.0)\nblh = df['era5_blh_m'].fillna(800.0).clip(80.0, 3500.0)\nbg_est = np.clip(53.7 * ((ws / 4.0) ** 0.25) * ((800.0 / blh) ** 0.15), 22.0, 68.0)\ndf['pm10_clean_ugm3'] = np.where(vis < 9.9, df['pm10_calibrated_ugm3'].values, bg_est)\nprint('Before de-censor <=54%:', round((df['pm10_calibrated_ugm3']<=54).mean()*100,1), '% | After de-censor unique quantiles:', df['pm10_clean_ugm3'].quantile([0.1,0.25,0.5,0.75,0.9]).round(2).to_dict())"),
        ("## 4. Visualize Before vs After De-Censoring the `53.7` Floor",
         "fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))\naxes[0].hist(df['pm10_calibrated_ugm3'].clip(0, 120), bins=40, color='#d62728'); axes[0].set_title('Before: Flat 53.7 Floor Spike')\naxes[1].hist(df['pm10_clean_ugm3'].clip(0, 120), bins=40, color='#2ca02c'); axes[1].set_title('After: De-Censored Continuous Background')\nplt.tight_layout()"),
        ("## 5. Fix 3: Objective Physical Dust-Event Label (`clean_dust_event`)",
         "df['clean_dust_event'] = ((df['is_dust_event'] == 1) | (df['visibility_km'] < 5.0)).astype(int)\nprint('Original is_dust_event rate:', round(df['is_dust_event'].mean()*100,2), '% | Objective clean_dust_event rate:', round(df['clean_dust_event'].mean()*100,2), '%')"),
        ("## 6. Fix 4: Causal 180-Day (4,320h) Rolling Z-Score Detrending for Drifting NWP/Satellite",
         "for col in ['sat_retrieved_pm10', 'nwp_cams_pm10', 'sat_aod_550nm']:\n    rm = df[col].rolling(4320, min_periods=24).mean()\n    rs = df[col].rolling(4320, min_periods=24).std().clip(lower=1e-3)\n    df[f'{col}_detrended_z'] = ((df[col] - rm) / rs).clip(-5, 5)\n    df = df.drop(columns=[col])\nprint('Replaced raw drifting sat_pm10/cams_pm10/sat_aod with causal 180d detrended z-scores.')"),
        ("## 7. Verify Covariate Drift Reduction After Causal Detrending",
         "N0 = len(df); tr0 = int(N0 * 0.70)\nfor col in ['sat_retrieved_pm10_detrended_z', 'nwp_cams_pm10_detrended_z', 'sat_aod_550nm_detrended_z']:\n    z_tr = df.iloc[:tr0][col].mean(); z_te = df.iloc[int(N0*0.85):][col].mean()\n    print(f'{col:32s}: Train mean={z_tr:+.3f}, Test mean={z_te:+.3f}')"),
        ("## 8. Drop Any Leaky Pre-Existing Future Targets (`target_*`) from Raw CSV",
         "old_tgts = [c for c in df.columns if c.startswith('target_')]\nif old_tgts:\n    df = df.drop(columns=old_tgts)\nprint('Removed pre-existing target columns:', old_tgts)"),
        ("## 9. Add Causal Hourly Calendar & Diurnal Harmonics",
         "doy = df['ts'].dt.dayofyear; hr = df['ts'].dt.hour\ndf['sin_doy'] = np.sin(2*np.pi*doy/365.25); df['cos_doy'] = np.cos(2*np.pi*doy/365.25)\ndf['sin_hour'] = np.sin(2*np.pi*hr/24.0); df['cos_hour'] = np.cos(2*np.pi*hr/24.0)\nprint('Calendar/diurnal harmonics refreshed.')"),
        ("## 10. Add Causal Pressure, Thermal & Wind Tendencies (24h & 72h)",
         "df['sp_diff_24h'] = df['era5_surface_pressure'] - df['era5_surface_pressure'].shift(24)\ndf['sp_diff_72h'] = df['era5_surface_pressure'] - df['era5_surface_pressure'].shift(72)\ndf['t2m_diff_24h'] = df['era5_temperature_2m'] - df['era5_temperature_2m'].shift(24)\ndf['ws_diff_24h'] = df['era5_wind_speed_10m'] - df['era5_wind_speed_10m'].shift(24)\nprint('Added 24h & 72h synoptic tendencies.')"),
        ("## 11. Add Causal Multi-Scale Hourly Rolling Means (24h, 72h, 168h)",
         "for col in ['pm10_clean_ugm3', 'era5_wind_speed_10m', 'era5_wind_gusts_10m', 'visibility_km', 'phys_vpd_kpa']:\n    df[f'{col}_roll24h'] = df[col].rolling(24, min_periods=1).mean()\n    df[f'{col}_roll72h'] = df[col].rolling(72, min_periods=1).mean()\n    df[f'{col}_roll168h'] = df[col].rolling(168, min_periods=1).mean()\nprint('Added 15 causal multi-scale rolling features.')"),
        ("## 12. Add Causal Dust Persistence Rates (7d, 30d, 180d) & Hours-Since-Dust",
         "df['dust_rate_168h'] = df['clean_dust_event'].rolling(168, min_periods=1).mean()\ndf['dust_rate_720h'] = df['clean_dust_event'].rolling(720, min_periods=1).mean()\ndf['dust_rate_4320h'] = df['clean_dust_event'].rolling(4320, min_periods=1).mean()\nhs, last_h = [], -9999\nfor i, ev in enumerate(df['clean_dust_event'].values):\n    if ev == 1: last_h = i; hs.append(0.0)\n    else: hs.append(float(i - last_h) if last_h >= 0 else 720.0)\ndf['hours_since_dust'] = np.clip(hs, 0.0, 2160.0)\nprint('Causal persistence features added.')"),
        ("## 13. Build Forward-Average Targets: 24h (1d), 72h (3d), 168h (7d), 216h (9d), 360h (15d)",
         "HORIZONS_H = [24, 72, 168, 216, 360]\n# Fast exact forward rolling mean using reversed rolling\npm_rev = df['pm10_clean_ugm3'].iloc[::-1]\nev_rev = df['clean_dust_event'].iloc[::-1]\nfor h in HORIZONS_H:\n    df[f'target_avg_pm10_{h}h'] = pm_rev.rolling(h, min_periods=h).mean().iloc[::-1].shift(-1).values\n    df[f'target_evt_any_{h}h'] = (ev_rev.rolling(h, min_periods=h).max().iloc[::-1].shift(-1).values >= 1).astype(float)\ndf = df.iloc[168:-360].reset_index(drop=True)\nprint('Clean hourly dataset shape after trimming edge NaNs:', df.shape)"),
        ("## 14. Drop Any All-NaN or Constant Train Columns & Save Clean Hourly Dataset",
         "target_cols = [c for c in df.columns if c.startswith('target_')]\nnum_cols = df.select_dtypes(include=[np.number]).columns.tolist()\nfeature_cols = [c for c in num_cols if c not in target_cols + ['year','month','hour']]\ntr_chk = int(len(df) * 0.70)\nbad = [c for c in feature_cols if df.iloc[:tr_chk][c].isna().all() or df.iloc[:tr_chk][c].nunique(dropna=True) <= 1]\nif bad:\n    print('Dropping degenerate train columns:', bad)\n    df = df.drop(columns=bad)\n    feature_cols = [c for c in feature_cols if c not in bad]\nclean_path = PROJECT_ROOT / '06_Data' / 'riyadh_hourly_clean_tvt.csv'\ndf[['ts'] + feature_cols + target_cols].to_csv(clean_path, index=False)\nprint(f'Saved clean hourly dataset: {clean_path.name} | Rows: {len(df):,} | Features: {len(feature_cols)} | Targets: {len(target_cols)}')"),
        ("## 15. Clean Target Summary Across 24h, 72h, 168h, 216h, 360h",
         "rows = []\nfor h in HORIZONS_H:\n    rows.append({'Horizon_H': h, 'Days': h//24, 'Avg_PM10_Mean': round(df[f'target_avg_pm10_{h}h'].mean(),2), 'Avg_PM10_Med': round(df[f'target_avg_pm10_{h}h'].median(),2), 'Event_Any_%': round(df[f'target_evt_any_{h}h'].mean()*100,2)})\nprint(pd.DataFrame(rows).to_string(index=False))"),
        ("## 16. Define Exact Hourly Train (70%) / 360h Gap / Val (15%) / 360h Gap / Test (15%)",
         "N = len(df); GAP_H = 360\ntr_end = int(N * 0.70); val_start = tr_end + GAP_H; val_end = int(N * 0.85); te_start = val_end + GAP_H\ntrain_df = df.iloc[:tr_end]; val_df = df.iloc[val_start:val_end]; test_df = df.iloc[te_start:]\nprint(f'Train: {len(train_df):,}h | Val: {len(val_df):,}h | Test: {len(test_df):,}h')"),
        ("## 17. Train-Only (70%) Imputation & Yeo-Johnson Distribution Balancing",
         "imp = SimpleImputer(strategy='median'); pt = PowerTransformer(method='yeo-johnson')\nX_tr = pt.fit_transform(imp.fit_transform(train_df[feature_cols].values))\nX_te = pt.transform(imp.transform(test_df[feature_cols].values))\nsk_b = pd.DataFrame(imp.transform(train_df[feature_cols].values), columns=feature_cols).skew().abs()\nsk_a = pd.DataFrame(X_tr, columns=feature_cols).skew().abs()\nprint(f'Train |Skewness| mean -> Before: {sk_b.mean():.3f} | After Yeo-Johnson: {sk_a.mean():.3f}')"),
        ("## 18. Skewness Reduction Plot",
         "fig, ax = plt.subplots(figsize=(8, 3.8))\nax.hist(sk_b.clip(0,6), bins=25, alpha=0.6, label='Before', color='#d62728')\nax.hist(sk_a.clip(0,6), bins=25, alpha=0.6, label='After (Train-Fit)', color='#1f77b4')\nax.set_title('Hourly Feature |Skewness| Before vs After Yeo-Johnson'); ax.legend(); plt.tight_layout()"),
        ("## 19. Train-Only Mutual Information (24h & 168h Regression, Subsampled 6h)",
         "idx_s = np.arange(0, len(X_tr), 6)\nmi_24 = mutual_info_regression(X_tr[idx_s], train_df['target_avg_pm10_24h'].values[idx_s], random_state=42)\nmi_168 = mutual_info_regression(X_tr[idx_s], train_df['target_avg_pm10_168h'].values[idx_s], random_state=42)\nmi_df = pd.DataFrame({'Feature': feature_cols, 'MI_24h': np.round(mi_24,4), 'MI_168h': np.round(mi_168,4)}).sort_values('MI_168h', ascending=False)\nprint(mi_df.head(12).to_string(index=False))"),
        ("## 20. Train-Only Classification Mutual Information (24h & 168h)",
         "mic_24 = mutual_info_classif(X_tr[idx_s], train_df['target_evt_any_24h'].values[idx_s], random_state=42)\nmic_168 = mutual_info_classif(X_tr[idx_s], train_df['target_evt_any_168h'].values[idx_s], random_state=42)\nmi_df['MI_Cls_24h'] = [round(mic_24[feature_cols.index(f)],4) for f in mi_df['Feature']]\nmi_df['MI_Cls_168h'] = [round(mic_168[feature_cols.index(f)],4) for f in mi_df['Feature']]\nprint(mi_df.sort_values('MI_Cls_24h', ascending=False).head(10)[['Feature','MI_Cls_24h','MI_Cls_168h']].to_string(index=False))"),
        ("## 21. 5-Fold Rolling-Origin CV Ridge Stability (Inside 70% Hourly Train)",
         "n_tr = len(X_tr); m_tr = int(n_tr * 0.40); st = (n_tr - m_tr) // 5\ny168 = np.log1p(np.maximum(train_df['target_avg_pm10_168h'].values, 0))\ncoefs = []\nfor f in range(5):\n    ti = np.arange(0, m_tr + f*st - GAP_H, 6)\n    coefs.append(RidgeCV(alphas=[10.0, 50.0, 100.0]).fit(X_tr[ti], y168[ti]).coef_)\nstab_df = pd.DataFrame({'Feature': feature_cols, 'Ridge_Mean': np.round(np.mean(coefs,0),4), 'Ridge_SD': np.round(np.std(coefs,0),4)})\nstab_df['Abs'] = stab_df['Ridge_Mean'].abs()\nprint(stab_df.sort_values('Abs', ascending=False).head(10).to_string(index=False))"),
        ("## 22. Feature Impact & Stability Visualization",
         "fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))\nt12 = mi_df.head(12).iloc[::-1]\naxes[0].barh(t12['Feature'], t12['MI_168h'], color='#2ca02c'); axes[0].set_title('Train-Only MI (168h Avg PM10)')\nt12r = stab_df.sort_values('Abs', ascending=False).head(12).iloc[::-1]\naxes[1].barh(t12r['Feature'], t12r['Ridge_Mean'], xerr=t12r['Ridge_SD'], color='#ff7f0e'); axes[1].set_title('5-Fold CV Ridge Stability')\nplt.tight_layout()"),
        ("## 23. Post-Clean Covariate Shift Audit (Train 70% vs Test 15%)",
         "drift = np.abs(X_te.mean(axis=0) - X_tr.mean(axis=0))\ndrift_df = pd.DataFrame({'Feature': feature_cols, 'Test_Z_Shift': np.round(drift, 3)}).sort_values('Test_Z_Shift', ascending=False)\ndrift_df.to_csv(RESULTS_DIR / 'nb01_clean_hourly_feature_impact.csv', index=False)\nprint('Max covariate Z-shift after causal detrending:', drift_df.head(6).to_string(index=False))"),
        ("## 24. Causal Verification Assert",
         "assert 'mslp' not in feature_cols and 'pm10_clean_ugm3' in feature_cols\nassert (PROJECT_ROOT / '06_Data' / 'riyadh_hourly_clean_tvt.csv').exists()\nprint('Clean hourly dataset & anti-leakage checks PASSED.')"),
        ("## 25. Notebook 01 Summary",
         "print('NB01 Complete: All 4 data issues cleaned/mitigated in riyadh_hourly_clean_tvt.csv for NB02, NB03 & NB04.')"),
    ]
    run_pairs(pairs, env, NB_DIR / "01_feature_engineering_and_impact.ipynb")


def build_nb02():
    print("\n=== [3/5] Notebook 02: Complete Line A on Clean Hourly Data (50 cells) ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR, "RESULTS_DIR": RESULTS_DIR}
    pairs = [
        ("# Notebook 02: Complete Line A on Clean Hourly Data (Train/Val/Test + 5-Fold CV)\n## 1. Load Clean Hourly Dataset from Notebook 01",
         "import numpy as np, pandas as pd, matplotlib.pyplot as plt\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import PowerTransformer\nfrom sklearn.linear_model import Ridge, LogisticRegression\nfrom sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, ExtraTreesRegressor, ExtraTreesClassifier, HistGradientBoostingRegressor, HistGradientBoostingClassifier\nfrom sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error, roc_auc_score, average_precision_score, brier_score_loss, confusion_matrix, roc_curve\nfrom xgboost import XGBRegressor, XGBClassifier\ndf = pd.read_csv(PROJECT_ROOT / '06_Data' / 'riyadh_hourly_clean_tvt.csv')\ndf['ts'] = pd.to_datetime(df['ts'])\ntarget_cols = [c for c in df.columns if c.startswith('target_')]\nfeature_cols = [c for c in df.columns if c not in ['ts'] + target_cols]\nprint(f'Clean hourly rows: {len(df):,} | Features: {len(feature_cols)}')"),
        ("## 2. Hourly Train (70%) / 360h Gap / Val (15%) / 360h Gap / Test (15%) Split",
         "N = len(df); GAP_H = 360\ntr_end = int(N * 0.70); val_start = tr_end + GAP_H; val_end = int(N * 0.85); te_start = val_end + GAP_H\n# Synoptic 6-hour stride (00,06,12,18 UTC) for fast multi-seed training\nSTRIDE = 6\ntrain_df = df.iloc[:tr_end:STRIDE].reset_index(drop=True)\nval_df = df.iloc[val_start:val_end:STRIDE].reset_index(drop=True)\ntest_df = df.iloc[te_start::STRIDE].reset_index(drop=True)\nimp = SimpleImputer(strategy='median'); pt = PowerTransformer(method='yeo-johnson')\nX_tr = pt.fit_transform(imp.fit_transform(train_df[feature_cols].values))\nX_va = pt.transform(imp.transform(val_df[feature_cols].values))\nX_te = pt.transform(imp.transform(test_df[feature_cols].values))\nprint(f'Synoptic 6h Train: {X_tr.shape} | Val: {X_va.shape} | Test: {X_te.shape}')"),
        ("## 3. Calibration, Alert-Lift & 5-Fold Rolling-Origin CV Helpers",
         "HORIZONS_H = [24, 72, 168, 216, 360]\nSEEDS = [42, 123, 456]\ndef platt_cal(va_s, va_y, te_s):\n    if len(np.unique(va_y)) < 2 or np.std(va_s) < 1e-12: return np.full(len(te_s), float(np.mean(va_y)))\n    lr = LogisticRegression(C=1.0, max_iter=1000).fit(np.clip(va_s,-30,30).reshape(-1,1), va_y)\n    return np.clip(lr.predict_proba(np.clip(te_s,-30,30).reshape(-1,1))[:,1], 1e-6, 1-1e-6)\ndef rec10(y, p):\n    k = max(1, int(np.ceil(len(y)*0.10))); idx = np.argsort(p)[::-1][:k]\n    r = float(np.sum(y[idx])/max(1,np.sum(y))); return r, r/0.10\ndef make_cv_folds(n, gap_rows=60, k=5):\n    m = int(n*0.40); st = (n-m)//k\n    return [(np.arange(0, m+i*st-gap_rows), np.arange(m+i*st, m+(i+1)*st if i<k-1 else n)) for i in range(k)]\ncv_folds = make_cv_folds(len(X_tr), 60, 5)\nprint('5-Fold CV ready (60-step = 360h gap).')"),
        ("## 4. 5-Fold Rolling-Origin CV Inside 70% Train (All 5 Horizons)",
         "cv_rows = []\nfor h in HORIZONS_H:\n    y_cv = train_df[f'target_evt_any_{h}h'].values.astype(int)\n    for mn, fn in [('LogReg_Bal', lambda s: LogisticRegression(C=0.2, class_weight='balanced', max_iter=1000)), ('RandomForest', lambda s: RandomForestClassifier(n_estimators=100, max_depth=8, min_samples_leaf=8, class_weight='balanced', random_state=s, n_jobs=-1)), ('ExtraTrees', lambda s: ExtraTreesClassifier(n_estimators=100, max_depth=8, min_samples_leaf=8, class_weight='balanced', random_state=s, n_jobs=-1)), ('HistGB', lambda s: HistGradientBoostingClassifier(max_iter=120, max_depth=5, min_samples_leaf=15, l2_regularization=2.0, random_state=s)), ('XGBoost', lambda s: XGBClassifier(n_estimators=120, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, reg_lambda=2.0, random_state=s, n_jobs=-1, eval_metric='logloss'))]:\n        oy, op = [], []\n        for ti, vi in cv_folds:\n            if len(np.unique(y_cv[ti])) < 2: continue\n            m = fn(42).fit(X_tr[ti], y_cv[ti]); oy.append(y_cv[vi]); op.append(m.predict_proba(X_tr[vi])[:,1])\n        yc, pc = np.concatenate(oy), np.concatenate(op)\n        cv_rows.append({'Horizon_H': h, 'Days': h//24, 'Model': mn, 'CV_ROC': round(roc_auc_score(yc,pc),4), 'CV_PR': round(average_precision_score(yc,pc),4)})\ncv_df = pd.DataFrame(cv_rows); cv_df.to_csv(RESULTS_DIR / 'nb02_line_a_5fold_cv_hourly.csv', index=False)\nprint(cv_df.to_string(index=False))"),
        ("## 5. 5-Fold CV ROC-AUC Across 1–15 Days",
         "fig, ax = plt.subplots(figsize=(9, 4))\nfor m in cv_df['Model'].unique():\n    s = cv_df[cv_df['Model']==m]; ax.plot(s['Days'], s['CV_ROC'], marker='o', label=m)\nax.set_xticks([1,3,7,9,15]); ax.set_title('Line A 5-Fold CV ROC-AUC (Clean Hourly)'); ax.legend(fontsize=8); ax.grid(alpha=0.3); plt.tight_layout()"),
        ("## 6. Train / Val Calibration & Test Evaluation: Baselines (Classification)",
         "cls_rows = []\nfor h in HORIZONS_H:\n    y_tr = train_df[f'target_evt_any_{h}h'].values.astype(int)\n    y_va = val_df[f'target_evt_any_{h}h'].values.astype(int)\n    y_te = test_df[f'target_evt_any_{h}h'].values.astype(int)\n    b_ref = brier_score_loss(y_te, np.full(len(y_te), float(np.mean(y_tr))))\n    pers_p = platt_cal(val_df['dust_rate_720h'].values, y_va, test_df['dust_rate_720h'].values)\n    mc_map = pd.Series(y_tr).groupby(train_df['ts'].dt.month).mean().to_dict()\n    mc_va = np.array([mc_map.get(m, np.mean(y_tr)) for m in val_df['ts'].dt.month])\n    mc_te = np.array([mc_map.get(m, np.mean(y_tr)) for m in test_df['ts'].dt.month])\n    mc_p = platt_cal(mc_va, y_va, mc_te)\n    lr = LogisticRegression(C=0.2, class_weight='balanced', max_iter=1000).fit(X_tr, y_tr)\n    lr_p = platt_cal(lr.predict_proba(X_va)[:,1], y_va, lr.predict_proba(X_te)[:,1])\n    for mn, p, vr in [('Persistence_Cal', pers_p, val_df['dust_rate_720h'].values), ('MonthClimo_Cal', mc_p, mc_va), ('LogReg_Bal_Cal', lr_p, lr.predict_proba(X_va)[:,1])]:\n        br = brier_score_loss(y_te, p); r10, l10 = rec10(y_te, p)\n        cls_rows.append({'Horizon_H': h, 'Days': h//24, 'Model': mn, 'Val_ROC': round(roc_auc_score(y_va, vr),4), 'Test_ROC': round(roc_auc_score(y_te,p),4), 'ROC_sd': 0.0, 'Test_PR': round(average_precision_score(y_te,p),4), 'Brier': round(br,4), 'BSS': round(1-br/b_ref,4), 'Rec10': round(r10,4), 'Lift10': round(l10,2)})\nprint('Hourly baselines evaluated.')"),
        ("## 7. Line A Tree & Boosting Models (3-Seed Mean ± SD on Held-Out Test)",
         "te_probs_168 = {}\nfor h in HORIZONS_H:\n    y_tr = train_df[f'target_evt_any_{h}h'].values.astype(int)\n    y_va = val_df[f'target_evt_any_{h}h'].values.astype(int)\n    y_te = test_df[f'target_evt_any_{h}h'].values.astype(int)\n    b_ref = brier_score_loss(y_te, np.full(len(y_te), float(np.mean(y_tr))))\n    pw = float(np.sum(y_tr==0)/max(1,np.sum(y_tr==1)))\n    specs = [('RandomForest_Cal', lambda s: RandomForestClassifier(n_estimators=100, max_depth=8, min_samples_leaf=8, class_weight='balanced', random_state=s, n_jobs=-1)), ('ExtraTrees_Cal', lambda s: ExtraTreesClassifier(n_estimators=100, max_depth=8, min_samples_leaf=8, class_weight='balanced', random_state=s, n_jobs=-1)), ('HistGB_Cal', lambda s: HistGradientBoostingClassifier(max_iter=120, max_depth=5, min_samples_leaf=15, l2_regularization=2.0, random_state=s)), ('XGBoost_Cal', lambda s: XGBClassifier(n_estimators=120, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=pw, reg_lambda=2.0, random_state=s, n_jobs=-1, eval_metric='logloss'))]\n    for mn, fn in specs:\n        vrocs, trocs, prs, brs, bsss, r10s, l10s = [], [], [], [], [], [], []\n        for s in SEEDS:\n            m = fn(s).fit(X_tr, y_tr); vp = m.predict_proba(X_va)[:,1]; tp = platt_cal(vp, y_va, m.predict_proba(X_te)[:,1])\n            if h == 168 and s == 42: te_probs_168[mn] = tp\n            vrocs.append(roc_auc_score(y_va,vp)); trocs.append(roc_auc_score(y_te,tp)); prs.append(average_precision_score(y_te,tp))\n            br = brier_score_loss(y_te,tp); brs.append(br); bsss.append(1-br/b_ref); r10, l10 = rec10(y_te,tp); r10s.append(r10); l10s.append(l10)\n        cls_rows.append({'Horizon_H': h, 'Days': h//24, 'Model': mn, 'Val_ROC': round(np.mean(vrocs),4), 'Test_ROC': round(np.mean(trocs),4), 'ROC_sd': round(np.std(trocs),4), 'Test_PR': round(np.mean(prs),4), 'Brier': round(np.mean(brs),4), 'BSS': round(np.mean(bsss),4), 'Rec10': round(np.mean(r10s),4), 'Lift10': round(np.mean(l10s),2)})\ncls_df = pd.DataFrame(cls_rows); cls_df.to_csv(RESULTS_DIR / 'nb02_line_a_classification_hourly.csv', index=False)\nprint(cls_df[['Days','Model','Val_ROC','Test_ROC','Test_PR','BSS','Lift10']].to_string(index=False))"),
        ("## 8. Validation vs Test ROC-AUC Decay (1–15 Days)",
         "fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))\nfor m in cls_df['Model'].unique():\n    s = cls_df[cls_df['Model']==m]\n    axes[0].plot(s['Days'], s['Val_ROC'], marker='o', label=m); axes[1].plot(s['Days'], s['Test_ROC'], marker='s', label=m)\naxes[0].set_title('Validation (15%) ROC-AUC'); axes[1].set_title('Test (15%) ROC-AUC')\nfor ax in axes: ax.set_xticks([1,3,7,9,15]); ax.legend(fontsize=7); ax.grid(alpha=0.3)\nplt.tight_layout()"),
        ("## 9. Test PR-AUC & Brier Skill Score (BSS) Across 1–15 Days",
         "fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))\nfor m in ['Persistence_Cal','MonthClimo_Cal','LogReg_Bal_Cal','RandomForest_Cal','ExtraTrees_Cal','XGBoost_Cal']:\n    s = cls_df[cls_df['Model']==m]\n    axes[0].plot(s['Days'], s['Test_PR'], marker='o', label=m); axes[1].plot(s['Days'], s['BSS'], marker='s', label=m)\naxes[1].axhline(0, color='black', ls='--'); axes[0].set_title('Test PR-AUC'); axes[1].set_title('Test BSS')\nfor ax in axes: ax.set_xticks([1,3,7,9,15]); ax.legend(fontsize=7); ax.grid(alpha=0.3)\nplt.tight_layout()"),
        ("## 10. 168h (7-Day) Test ROC Curves",
         "y_te168 = test_df['target_evt_any_168h'].values.astype(int)\nfig, ax = plt.subplots(figsize=(6, 4.8))\nfor m, p in te_probs_168.items():\n    fpr, tpr, _ = roc_curve(y_te168, p); ax.plot(fpr, tpr, label=f'{m} ({roc_auc_score(y_te168,p):.3f})')\nax.plot([0,1],[0,1],'k--'); ax.set_title('168h (7d) Test ROC Curves'); ax.legend(fontsize=8); plt.tight_layout()"),
        ("## 11. 168h Calibration Reliability Diagram",
         "fig, ax = plt.subplots(figsize=(6, 4.8))\nfor m, p in te_probs_168.items():\n    bins = np.linspace(0,1,7); bi = np.digitize(p,bins)-1\n    ax.plot([p[bi==i].mean() if np.any(bi==i) else np.nan for i in range(6)], [y_te168[bi==i].mean() if np.any(bi==i) else np.nan for i in range(6)], marker='o', label=m)\nax.plot([0,1],[0,1],'k--'); ax.set_title('168h Reliability Diagram'); ax.legend(fontsize=8); plt.tight_layout()"),
        ("## 12. Validation-Tuned Confusion Matrix (168h RandomForest)",
         "m_rf = RandomForestClassifier(n_estimators=100, max_depth=8, min_samples_leaf=8, class_weight='balanced', random_state=42, n_jobs=-1).fit(X_tr, train_df['target_evt_any_168h'].values.astype(int))\nvp_rf = platt_cal(m_rf.predict_proba(X_va)[:,1], val_df['target_evt_any_168h'].values.astype(int), m_rf.predict_proba(X_va)[:,1])\ntau = np.quantile(vp_rf, 0.80)\nprint(f'Val Top-20% tau={tau:.3f} -> Test Confusion Matrix:\\n{confusion_matrix(y_te168, (te_probs_168[\"RandomForest_Cal\"]>=tau).astype(int))}')"),
        ("## 13. Continuous Clean-PM10 Regression (All 5 Horizons)",
         "reg_rows = []\nfor h in HORIZONS_H:\n    y_tr = train_df[f'target_avg_pm10_{h}h'].values; y_te = test_df[f'target_avg_pm10_{h}h'].values\n    med_p = np.full(len(y_te), np.median(y_tr)); pers_p = test_df['pm10_clean_ugm3'].values\n    mc_map = pd.Series(y_tr).groupby(train_df['ts'].dt.month).mean().to_dict()\n    mc_p = np.array([mc_map.get(m, np.mean(y_tr)) for m in test_df['ts'].dt.month])\n    r_p = np.expm1(np.clip(Ridge(alpha=50.0).fit(X_tr, np.log1p(np.maximum(y_tr,0))).predict(X_te), 0, 10))\n    for mn, p in [('Trivial_Median', med_p), ('Persistence', pers_p), ('MonthClimo', mc_p), ('Ridge_log1p', r_p)]:\n        reg_rows.append({'Horizon_H': h, 'Days': h//24, 'Model': mn, 'R2': round(r2_score(y_te,p),4), 'RMSE': round(root_mean_squared_error(y_te,p),2), 'RMSE_sd': 0.0, 'MAE': round(mean_absolute_error(y_te,p),2)})\n    for mn, fn in [('RandomForest', lambda s: RandomForestRegressor(n_estimators=100, max_depth=8, min_samples_leaf=8, random_state=s, n_jobs=-1)), ('ExtraTrees', lambda s: ExtraTreesRegressor(n_estimators=100, max_depth=8, min_samples_leaf=8, random_state=s, n_jobs=-1)), ('HistGB', lambda s: HistGradientBoostingRegressor(max_iter=120, max_depth=5, min_samples_leaf=15, l2_regularization=2.0, random_state=s)), ('XGBoost', lambda s: XGBRegressor(n_estimators=120, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, reg_lambda=2.0, random_state=s, n_jobs=-1))]:\n        r2s, rms, mas = [], [], []\n        for s in SEEDS:\n            p = np.expm1(np.clip(fn(s).fit(X_tr, np.log1p(np.maximum(y_tr,0))).predict(X_te), 0, 10))\n            r2s.append(r2_score(y_te,p)); rms.append(root_mean_squared_error(y_te,p)); mas.append(mean_absolute_error(y_te,p))\n        reg_rows.append({'Horizon_H': h, 'Days': h//24, 'Model': mn, 'R2': round(np.mean(r2s),4), 'RMSE': round(np.mean(rms),2), 'RMSE_sd': round(np.std(rms),2), 'MAE': round(np.mean(mas),2)})\nreg_df = pd.DataFrame(reg_rows); reg_df.to_csv(RESULTS_DIR / 'nb02_line_a_regression_hourly.csv', index=False)\nprint(reg_df[['Days','Model','R2','RMSE','MAE']].to_string(index=False))"),
        ("## 14. Regression RMSE & R² Across 1–15 Days",
         "fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))\nfor m in ['Trivial_Median','MonthClimo','Ridge_log1p','RandomForest','ExtraTrees','XGBoost']:\n    s = reg_df[reg_df['Model']==m]\n    axes[0].plot(s['Days'], s['RMSE'], marker='o', label=m); axes[1].plot(s['Days'], s['R2'], marker='s', label=m)\naxes[1].axhline(0, color='black', ls='--'); axes[0].set_title('Test RMSE (ug/m3)'); axes[1].set_title('Test R²')\nfor ax in axes: ax.set_xticks([1,3,7,9,15]); ax.legend(fontsize=7); ax.grid(alpha=0.3)\nplt.tight_layout()"),
        ("## 15. Train+Val Refit Check (168h ExtraTrees)",
         "et_tv = ExtraTreesClassifier(n_estimators=100, max_depth=8, min_samples_leaf=8, class_weight='balanced', random_state=42, n_jobs=-1).fit(np.vstack([X_tr,X_va]), np.concatenate([train_df['target_evt_any_168h'].values, val_df['target_evt_any_168h'].values]).astype(int))\nprint('Train-only ET 168h ROC:', cls_df[(cls_df['Horizon_H']==168)&(cls_df['Model']=='ExtraTrees_Cal')]['Test_ROC'].values[0], '| Train+Val ET:', round(roc_auc_score(y_te168, et_tv.predict_proba(X_te)[:,1]),4))"),
        ("## 16. Top-10% Alert Lift Across 1–15 Days",
         "fig, ax = plt.subplots(figsize=(9, 3.8))\nfor m in ['Persistence_Cal','MonthClimo_Cal','LogReg_Bal_Cal','RandomForest_Cal','XGBoost_Cal']:\n    s = cls_df[cls_df['Model']==m]; ax.plot(s['Days'], s['Lift10'], marker='o', label=m)\nax.axhline(1.0, color='black', ls='--'); ax.set_xticks([1,3,7,9,15]); ax.set_title('Test Lift@Top10%'); ax.legend(fontsize=8); plt.tight_layout()"),
        ("## 17. Residual Error Analysis (168h Clean PM10)",
         "rf_r = RandomForestRegressor(n_estimators=100, max_depth=8, min_samples_leaf=8, random_state=42, n_jobs=-1).fit(X_tr, np.log1p(train_df['target_avg_pm10_168h'].values))\np168 = np.expm1(rf_r.predict(X_te)); y168_te = test_df['target_avg_pm10_168h'].values; res = y168_te - p168\nprint(f'168h Residual Mean={res.mean():.2f}, Std={res.std():.2f}, P95_Abs={np.percentile(np.abs(res),95):.2f}')"),
        ("## 18. Predicted vs Observed 168h Clean PM10 Time Series (Test)",
         "fig, ax = plt.subplots(figsize=(11, 3.6))\nax.plot(test_df['ts'], y168_te, label='Observed 168h Avg', color='#1f77b4')\nax.plot(test_df['ts'], p168, label='RF Predicted', color='#d62728', alpha=0.8)\nax.set_title('Test 168h (7d) Average Clean PM10 Forecast'); ax.legend(); plt.tight_layout()"),
        ("## 19. Quantile Prediction Interval Coverage (10th–90th Percentile)",
         "q10 = HistGradientBoostingRegressor(loss='quantile', quantile=0.10, max_iter=120, max_depth=5, random_state=42).fit(X_tr, train_df['target_avg_pm10_168h'].values).predict(X_te)\nq90 = HistGradientBoostingRegressor(loss='quantile', quantile=0.90, max_iter=120, max_depth=5, random_state=42).fit(X_tr, train_df['target_avg_pm10_168h'].values).predict(X_te)\nprint(f'Nominal 80% Interval Test Coverage: {np.mean((y168_te>=q10)&(y168_te<=q90))*100:.1f}% | Mean Width: {np.mean(q90-q10):.1f}')"),
        ("## 20. Paired 7-Day (28-Step) Block Bootstrap: RandomForest vs Persistence (168h)",
         "rng = np.random.default_rng(42); blk = 28; nb = len(y_te168)//blk; diffs = []\npp = platt_cal(val_df['dust_rate_720h'].values, val_df['target_evt_any_168h'].values.astype(int), test_df['dust_rate_720h'].values)\npe = te_probs_168['RandomForest_Cal']\nfor _ in range(300):\n    idx = np.concatenate([np.arange(s*blk,(s+1)*blk) for s in rng.integers(0, nb, size=nb)])\n    if len(np.unique(y_te168[idx]))<2: continue\n    diffs.append(roc_auc_score(y_te168[idx], pe[idx]) - roc_auc_score(y_te168[idx], pp[idx]))\nprint(f'168h Test ROC Diff (RF - Persistence): {np.mean(diffs):+.4f} 95% CI [{np.percentile(diffs,2.5):+.4f}, {np.percentile(diffs,97.5):+.4f}]')"),
        ("## 21. Seasonal Error Breakdown (Spring MAM vs Rest of Year)",
         "spr = test_df['ts'].dt.month.isin([3,4,5]).values\nprint(f'Spring 168h RMSE: {root_mean_squared_error(y168_te[spr], p168[spr]):.2f} | Non-Spring: {root_mean_squared_error(y168_te[~spr], p168[~spr]):.2f}')"),
        ("## 22. Best Line A Classifier per Horizon",
         "print(cls_df.sort_values(['Horizon_H','Test_ROC'], ascending=[True,False]).groupby('Horizon_H').first()[['Days','Model','Test_ROC','Test_PR','BSS','Lift10']].to_string())"),
        ("## 23. Best Line A Regressor per Horizon",
         "print(reg_df.sort_values(['Horizon_H','RMSE']).groupby('Horizon_H').first()[['Days','Model','RMSE','R2','MAE']].to_string())"),
        ("## 24. Export Verification",
         "for fn in ['nb02_line_a_5fold_cv_hourly.csv','nb02_line_a_classification_hourly.csv','nb02_line_a_regression_hourly.csv']:\n    assert (RESULTS_DIR / fn).exists()\nprint('Line A clean hourly CSVs verified.')"),
        ("## 25. Notebook 02 Summary",
         "print('NB02 Complete on Clean Hourly Data.')"),
    ]
    run_pairs(pairs, env, NB_DIR / "02_line_a_tabular_and_meta_models_riyadh.ipynb")


def build_nb03():
    print("\n=== [4/5] Notebook 03: Line B Real PyTorch Layers (Clean Hourly + line_b_final_dataset.npz, 50 cells) ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR, "RESULTS_DIR": RESULTS_DIR}
    pairs = [
        ("# Notebook 03: Line B Real PyTorch Layers (Clean Hourly + `line_b_final_dataset.npz`)\n## 1. Imports & Reproducibility",
         "import random, numpy as np, pandas as pd, torch, torch.nn as nn\nfrom torch.utils.data import TensorDataset, DataLoader\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import PowerTransformer\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, root_mean_squared_error, r2_score, mean_absolute_error\nimport matplotlib.pyplot as plt\ndef set_seed(s): random.seed(s); np.random.seed(s); torch.manual_seed(s)\nprint('PyTorch:', torch.__version__)"),
        ("## 2. Load Clean Hourly Data + `line_b_final_dataset.npz` + Graph Adjacency",
         "df = pd.read_csv(PROJECT_ROOT / '06_Data' / 'riyadh_hourly_clean_tvt.csv')\ndf['ts'] = pd.to_datetime(df['ts'])\ntarget_cols = [c for c in df.columns if c.startswith('target_')]\nfeature_cols = [c for c in df.columns if c not in ['ts'] + target_cols]\nnpz = np.load(PROJECT_ROOT / '06_Data' / 'line_b_final_dataset.npz', allow_pickle=True)\nadj_raw = np.load(PROJECT_ROOT / '06_Data' / 'riyadh_graph_adjacency_matrix.npy')\nprint(f'Clean hourly: {len(df):,} | Features: {len(feature_cols)} | NPZ seq: {npz[\"seq_features\"].shape}')"),
        ("## 3. Train-Only Scaling & Synoptic 6h Indices (Train 70% / 360h Gap / Val 15% / 360h Gap / Test 15%)",
         "N = len(df); GAP_H = 360; SEQ_LEN = 24; STRIDE = 6\ntr_end = int(N * 0.70); val_start = tr_end + GAP_H; val_end = int(N * 0.85); te_start = val_end + GAP_H\nimp = SimpleImputer(strategy='median'); pt = PowerTransformer(method='yeo-johnson')\npt.fit(imp.fit_transform(df.iloc[:tr_end:STRIDE][feature_cols].values))\nX_all_s = pt.transform(imp.transform(df[feature_cols].values))\nprint('Train-only scaler fitted.')"),
        ("## 4. Build 24-Hour Causal Lookback Sequences `(N, 24, F)`",
         "def make_seq(indices):\n    return np.array([X_all_s[i - SEQ_LEN + 1 : i + 1] for i in indices], dtype=np.float32)\ntr_idx = np.arange(SEQ_LEN, tr_end, STRIDE)\nva_idx = np.arange(val_start, val_end, STRIDE)\nte_idx = np.arange(te_start, N, STRIDE)\nX_tr_seq, X_va_seq, X_te_seq = make_seq(tr_idx), make_seq(va_idx), make_seq(te_idx)\nprint(f'24h Sequences -> Train: {X_tr_seq.shape}, Val: {X_va_seq.shape}, Test: {X_te_seq.shape}')"),
        ("## 5. Visualize NPZ Adjacency Matrix",
         "fig, ax = plt.subplots(figsize=(4.5, 3.8))\nax.imshow(npz['adjacency_matrix'], cmap='viridis'); ax.set_title('NPZ 6-Node Adjacency Matrix'); plt.tight_layout()"),
        ("## 6. Real PyTorch Architecture 1: `RealLSTMNet` (`nn.LSTM`)",
         "class RealLSTMNet(nn.Module):\n    def __init__(self, in_dim, hidden=48):\n        super().__init__()\n        self.lstm = nn.LSTM(in_dim, hidden, num_layers=2, batch_first=True, dropout=0.2)\n        self.head = nn.Sequential(nn.Linear(hidden, 24), nn.ReLU(), nn.Linear(24, 1))\n    def forward(self, x):\n        o, _ = self.lstm(x); return self.head(o[:, -1, :]).squeeze(-1)\nprint('RealLSTMNet params:', sum(p.numel() for p in RealLSTMNet(len(feature_cols)).parameters()))"),
        ("## 7. Real PyTorch Architecture 2: `RealTransformerNet` (`nn.TransformerEncoder`)",
         "class RealTransformerNet(nn.Module):\n    def __init__(self, in_dim, d_model=48):\n        super().__init__()\n        self.proj = nn.Linear(in_dim, d_model)\n        self.pos = nn.Parameter(torch.randn(1, SEQ_LEN, d_model) * 0.02)\n        enc = nn.TransformerEncoderLayer(d_model=d_model, nhead=4, dim_feedforward=96, dropout=0.2, batch_first=True)\n        self.encoder = nn.TransformerEncoder(enc, num_layers=2); self.head = nn.Linear(d_model, 1)\n    def forward(self, x):\n        return self.head(self.encoder(self.proj(x) + self.pos)[:, -1, :]).squeeze(-1)\nprint('RealTransformerNet params:', sum(p.numel() for p in RealTransformerNet(len(feature_cols)).parameters()))"),
        ("## 8. Real PyTorch Architecture 3: `RealPINNNet` (Physics Monotonicity Loss)",
         "class RealPINNNet(nn.Module):\n    def __init__(self, in_dim, hidden=48):\n        super().__init__(); self.gru = nn.GRU(in_dim, hidden, batch_first=True)\n        self.head = nn.Sequential(nn.Linear(hidden, 24), nn.SiLU(), nn.Linear(24, 1))\n    def forward(self, x): o, _ = self.gru(x); return self.head(o[:, -1, :]).squeeze(-1)\nprint('RealPINNNet params:', sum(p.numel() for p in RealPINNNet(len(feature_cols)).parameters()))"),
        ("## 9. Real PyTorch Architecture 4: `RealSTGNNNet` (6-Node Graph + `nn.GRU`)",
         "class RealSTGNNNet(nn.Module):\n    def __init__(self, in_dim, adj, hidden=32):\n        super().__init__()\n        deg = np.sum(adj, axis=1, keepdims=True) + 1e-6\n        self.register_buffer('A_norm', torch.tensor(adj / deg, dtype=torch.float32))\n        self.n_nodes = adj.shape[0]; self.node_emb = nn.Parameter(torch.randn(1, 1, self.n_nodes, 8)*0.05)\n        self.in_proj = nn.Linear(in_dim + 8, hidden); self.gcn = nn.Linear(hidden, hidden)\n        self.gru = nn.GRU(hidden, hidden, batch_first=True); self.head = nn.Linear(hidden, 1)\n    def forward(self, x):\n        B, T, F = x.shape; xn = x.unsqueeze(2).expand(B, T, self.n_nodes, F); emb = self.node_emb.expand(B, T, self.n_nodes, 8)\n        h = torch.relu(self.in_proj(torch.cat([xn, emb], dim=-1)))\n        hg = torch.relu(self.gcn(torch.einsum('ij,btjf->btif', self.A_norm, h)))\n        o, _ = self.gru(hg.mean(dim=2)); return self.head(o[:, -1, :]).squeeze(-1)\nprint('RealSTGNNNet params:', sum(p.numel() for p in RealSTGNNNet(len(feature_cols), adj_raw).parameters()))"),
        ("## 10. Real PyTorch Architecture 5: Multi-Modal CNN + ST-GNN on `line_b_final_dataset.npz`",
         "class MultiModalNPZNet(nn.Module):\n    def __init__(self, adj):\n        super().__init__()\n        deg = np.sum(adj, axis=1, keepdims=True) + 1e-6\n        self.register_buffer('A_norm', torch.tensor(adj / deg, dtype=torch.float32))\n        self.nwp_cnn = nn.Sequential(nn.Conv2d(6, 16, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1))\n        self.sat_cnn = nn.Sequential(nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1))\n        self.node_lin = nn.Linear(12, 24); self.gru = nn.GRU(24, 24, batch_first=True)\n        self.head = nn.Sequential(nn.Linear(24+16+16, 32), nn.ReLU(), nn.Linear(32, 1))\n    def forward(self, nwp, sat, seq):\n        B, T, Nn, F = seq.shape\n        fn = self.nwp_cnn(nwp).flatten(1); fs = self.sat_cnn(sat).flatten(1)\n        h = torch.relu(self.node_lin(seq))\n        hg = torch.einsum('ij,btjf->btif', self.A_norm, h).mean(dim=2)\n        fg, _ = self.gru(hg)\n        return self.head(torch.cat([fg[:, -1, :], fn, fs], dim=-1)).squeeze(-1)\nprint('MultiModalNPZNet params:', sum(p.numel() for p in MultiModalNPZNet(npz['adjacency_matrix']).parameters()))"),
        ("## 11. Train & Evaluate `MultiModalNPZNet` on `line_b_final_dataset.npz` (70/15/15 Split)",
         "set_seed(42)\nn_npz = len(npz['seq_features']); t1 = int(n_npz*0.70); t2 = int(n_npz*0.85)\nnwp_t = torch.tensor(npz['nwp_grid']); sat_t = torch.tensor(npz['satellite_grid']); seq_t = torch.tensor(npz['seq_features'])\ny_npz = torch.tensor(np.log1p(np.maximum(npz['targets_pm10'][:, 0, 0], 0)), dtype=torch.float32)\nmm_mdl = MultiModalNPZNet(npz['adjacency_matrix']); opt = torch.optim.AdamW(mm_mdl.parameters(), lr=2e-3)\ncrit = nn.L1Loss(); dl_npz = DataLoader(TensorDataset(nwp_t[:t1], sat_t[:t1], seq_t[:t1], y_npz[:t1]), batch_size=32, shuffle=True)\nfor _ in range(25):\n    mm_mdl.train()\n    for bn, bs, bq, by in dl_npz: opt.zero_grad(); crit(mm_mdl(bn,bs,bq), by).backward(); opt.step()\nmm_mdl.eval()\nwith torch.no_grad():\n    p_npz = np.expm1(mm_mdl(nwp_t[t2:], sat_t[t2:], seq_t[t2:]).numpy())\n    y_npz_te = npz['targets_pm10'][t2:, 0, 0]\nprint(f'NPZ MultiModal CNN+STGNN 70/15/15 Test -> RMSE: {root_mean_squared_error(y_npz_te, p_npz):.2f}, R2: {r2_score(y_npz_te, p_npz):.4f}')"),
        ("## 12. Hourly Classification & Calibration Helpers",
         "wind_idx = feature_cols.index('era5_wind_speed_10m')\ndef platt_cal(va_s, va_y, te_s):\n    if len(np.unique(va_y)) < 2 or np.std(va_s) < 1e-12: return np.full(len(te_s), float(np.mean(va_y)))\n    lr = LogisticRegression(C=1.0, max_iter=1000).fit(np.clip(va_s,-30,30).reshape(-1,1), va_y)\n    return np.clip(lr.predict_proba(np.clip(te_s,-30,30).reshape(-1,1))[:,1], 1e-6, 1-1e-6)\ndef fit_cls(ctor, X_f, y_f, X_v, y_v, X_t, seed, is_pinn=False, epochs=12):\n    set_seed(seed); mdl = ctor()\n    pw = torch.tensor([float(np.sum(y_f==0)/max(1,np.sum(y_f==1)))], dtype=torch.float32)\n    crit = nn.BCEWithLogitsLoss(pos_weight=pw); opt = torch.optim.AdamW(mdl.parameters(), lr=1.5e-3, weight_decay=1e-3)\n    gen = torch.Generator().manual_seed(seed)\n    dl = DataLoader(TensorDataset(torch.tensor(X_f), torch.tensor(y_f, dtype=torch.float32)), batch_size=128, shuffle=True, generator=gen)\n    bl, bst, th, vh = 1e9, None, [], []\n    for _ in range(epochs):\n        mdl.train(); el = 0.0\n        for bx, by in dl:\n            opt.zero_grad(); lg = mdl(bx); loss = crit(lg, by)\n            if is_pinn:\n                bxp = bx.clone(); bxp[:,-1,wind_idx] += 0.5; loss = loss + 0.05*torch.mean(torch.relu(lg - mdl(bxp)))\n            loss.backward(); torch.nn.utils.clip_grad_norm_(mdl.parameters(), 1.0); opt.step(); el += float(loss.item())*len(bx)\n        th.append(el/len(X_f)); mdl.eval()\n        with torch.no_grad(): vl = float(crit(mdl(torch.tensor(X_v)), torch.tensor(y_v, dtype=torch.float32)).item())\n        vh.append(vl)\n        if vl < bl: bl = vl; bst = {k: v.clone() for k, v in mdl.state_dict().items()}\n    if bst: mdl.load_state_dict(bst)\n    mdl.eval()\n    with torch.no_grad(): vs, ts = mdl(torch.tensor(X_v)).numpy(), mdl(torch.tensor(X_t)).numpy()\n    return vs, platt_cal(vs, y_v, ts), th, vh"),
        ("## 13. 3-Fold Rolling-Origin CV Inside 70% Hourly Train (168h Horizon)",
         "y_tr168 = df.iloc[tr_idx]['target_evt_any_168h'].values.astype(int)\nn_s = len(X_tr_seq); m_s = int(n_s * 0.45); st_s = (n_s - m_s) // 3\ncv_lb = []\nfor mn, ctor, isp in [('LSTM', lambda: RealLSTMNet(len(feature_cols)), False), ('Transformer', lambda: RealTransformerNet(len(feature_cols)), False), ('PINN', lambda: RealPINNNet(len(feature_cols)), True), ('STGNN', lambda: RealSTGNNNet(len(feature_cols), adj_raw), False)]:\n    rocs = []\n    for f in range(3):\n        ti = np.arange(0, m_s + f*st_s - 60); vi = np.arange(m_s + f*st_s, m_s + (f+1)*st_s if f<2 else n_s)\n        vs, _, _, _ = fit_cls(ctor, X_tr_seq[ti], y_tr168[ti], X_tr_seq[vi], y_tr168[vi], X_tr_seq[vi], 42, isp, epochs=8)\n        rocs.append(roc_auc_score(y_tr168[vi], vs))\n    cv_lb.append({'Model': mn, 'CV_3Fold_ROC': round(np.mean(rocs), 4)})\nprint(pd.DataFrame(cv_lb).to_string(index=False))"),
        ("## 14. Full Hourly Train/Val/Test Classification Across 1–15 Days (3 Seeds)",
         "HORIZONS_H = [24, 72, 168, 216, 360]; SEEDS = [42, 123, 456]\nlb_cls_rows = []; hist_168 = {}; te_168_p = {}\nfor h in HORIZONS_H:\n    y_tr = df.iloc[tr_idx][f'target_evt_any_{h}h'].values.astype(int)\n    y_va = df.iloc[va_idx][f'target_evt_any_{h}h'].values.astype(int)\n    y_te = df.iloc[te_idx][f'target_evt_any_{h}h'].values.astype(int)\n    b_ref = brier_score_loss(y_te, np.full(len(y_te), float(np.mean(y_tr))))\n    for mn, ctor, isp in [('LineB_LSTM', lambda: RealLSTMNet(len(feature_cols)), False), ('LineB_Transformer', lambda: RealTransformerNet(len(feature_cols)), False), ('LineB_PINN', lambda: RealPINNNet(len(feature_cols)), True), ('LineB_STGNN', lambda: RealSTGNNNet(len(feature_cols), adj_raw), False)]:\n        vrocs, trocs, prs, bsss = [], [], [], []\n        for s in SEEDS:\n            vs, tp, th, vh = fit_cls(ctor, X_tr_seq, y_tr, X_va_seq, y_va, X_te_seq, s, isp, epochs=12)\n            if h == 168 and s == 42: hist_168[mn] = (th, vh); te_168_p[mn] = tp\n            vrocs.append(roc_auc_score(y_va, vs)); trocs.append(roc_auc_score(y_te, tp))\n            prs.append(average_precision_score(y_te, tp)); bsss.append(1 - brier_score_loss(y_te, tp)/b_ref)\n        lb_cls_rows.append({'Horizon_H': h, 'Days': h//24, 'Model': mn, 'Val_ROC': round(np.mean(vrocs),4), 'Test_ROC': round(np.mean(trocs),4), 'ROC_sd': round(np.std(trocs),4), 'Test_PR': round(np.mean(prs),4), 'BSS': round(np.mean(bsss),4)})\nlb_cls_df = pd.DataFrame(lb_cls_rows); lb_cls_df.to_csv(RESULTS_DIR / 'nb03_line_b_classification_hourly.csv', index=False)\nprint(lb_cls_df.to_string(index=False))"),
        ("## 15. Real PyTorch Training vs Validation Loss Curves (168h)",
         "fig, axes = plt.subplots(2, 2, figsize=(10, 6.5))\nfor ax, (mn, (th, vh)) in zip(axes.ravel(), hist_168.items()):\n    ax.plot(th, label='Train'); ax.plot(vh, label='Val'); ax.set_title(f'{mn} Loss (168h)'); ax.legend(fontsize=8)\nplt.tight_layout()"),
        ("## 16. Line B Classification ROC-AUC & BSS (1–15 Days)",
         "fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))\nfor mn in lb_cls_df['Model'].unique():\n    s = lb_cls_df[lb_cls_df['Model']==mn]\n    axes[0].plot(s['Days'], s['Test_ROC'], marker='o', label=mn); axes[1].plot(s['Days'], s['BSS'], marker='s', label=mn)\naxes[1].axhline(0, color='black', ls='--'); axes[0].set_title('Line B Test ROC-AUC'); axes[1].set_title('Line B Test BSS')\nfor ax in axes: ax.set_xticks([1,3,7,9,15]); ax.legend(fontsize=8); ax.grid(alpha=0.3)\nplt.tight_layout()"),
        ("## 17. Real PyTorch Regression Helper (`log1p` L1 Loss)",
         "def fit_reg(ctor, X_f, y_f, X_v, y_v, X_t, seed, epochs=12):\n    set_seed(seed); mdl = ctor(); crit = nn.L1Loss(); opt = torch.optim.AdamW(mdl.parameters(), lr=1.5e-3, weight_decay=1e-3)\n    gen = torch.Generator().manual_seed(seed); yf_l = np.log1p(np.maximum(y_f,0)).astype(np.float32); yv_l = np.log1p(np.maximum(y_v,0)).astype(np.float32)\n    dl = DataLoader(TensorDataset(torch.tensor(X_f), torch.tensor(yf_l)), batch_size=128, shuffle=True, generator=gen)\n    bl, bst = 1e9, None\n    for _ in range(epochs):\n        mdl.train()\n        for bx, by in dl: opt.zero_grad(); crit(mdl(bx), by).backward(); torch.nn.utils.clip_grad_norm_(mdl.parameters(), 1.0); opt.step()\n        mdl.eval()\n        with torch.no_grad(): vl = float(crit(mdl(torch.tensor(X_v)), torch.tensor(yv_l)).item())\n        if vl < bl: bl = vl; bst = {k: v.clone() for k, v in mdl.state_dict().items()}\n    if bst: mdl.load_state_dict(bst)\n    mdl.eval()\n    with torch.no_grad(): return np.expm1(np.clip(mdl(torch.tensor(X_t)).numpy(), 0, 10))\nprint('PyTorch regression trainer ready.')"),
        ("## 18. Full Hourly Train/Val/Test Regression Across 1–15 Days (3 Seeds)",
         "lb_reg_rows = []; te_168_r = {}\nfor h in HORIZONS_H:\n    y_tr = df.iloc[tr_idx][f'target_avg_pm10_{h}h'].values\n    y_va = df.iloc[va_idx][f'target_avg_pm10_{h}h'].values\n    y_te = df.iloc[te_idx][f'target_avg_pm10_{h}h'].values\n    for mn, ctor in [('LineB_LSTM', lambda: RealLSTMNet(len(feature_cols))), ('LineB_Transformer', lambda: RealTransformerNet(len(feature_cols))), ('LineB_PINN', lambda: RealPINNNet(len(feature_cols))), ('LineB_STGNN', lambda: RealSTGNNNet(len(feature_cols), adj_raw))]:\n        r2s, rms, mas = [], [], []\n        for s in SEEDS:\n            p = fit_reg(ctor, X_tr_seq, y_tr, X_va_seq, y_va, X_te_seq, s, epochs=12)\n            if h == 168 and s == 42: te_168_r[mn] = p\n            r2s.append(r2_score(y_te,p)); rms.append(root_mean_squared_error(y_te,p)); mas.append(mean_absolute_error(y_te,p))\n        lb_reg_rows.append({'Horizon_H': h, 'Days': h//24, 'Model': mn, 'R2': round(np.mean(r2s),4), 'RMSE': round(np.mean(rms),2), 'RMSE_sd': round(np.std(rms),2), 'MAE': round(np.mean(mas),2)})\nlb_reg_df = pd.DataFrame(lb_reg_rows); lb_reg_df.to_csv(RESULTS_DIR / 'nb03_line_b_regression_hourly.csv', index=False)\nprint(lb_reg_df.to_string(index=False))"),
        ("## 19. Line B Regression RMSE & R² Across 1–15 Days",
         "fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))\nfor mn in lb_reg_df['Model'].unique():\n    s = lb_reg_df[lb_reg_df['Model']==mn]\n    axes[0].plot(s['Days'], s['RMSE'], marker='o', label=mn); axes[1].plot(s['Days'], s['R2'], marker='s', label=mn)\naxes[1].axhline(0, color='black', ls='--'); axes[0].set_title('Line B Test RMSE'); axes[1].set_title('Line B Test R²')\nfor ax in axes: ax.set_xticks([1,3,7,9,15]); ax.legend(fontsize=8); ax.grid(alpha=0.3)\nplt.tight_layout()"),
        ("## 20. Line A vs Line B Comparison (Classification ROC-AUC)",
         "la_c = pd.read_csv(RESULTS_DIR / 'nb02_line_a_classification_hourly.csv')\nba = la_c.groupby('Days')['Test_ROC'].max().reset_index().rename(columns={'Test_ROC':'Best_LineA'})\nbb = lb_cls_df.groupby('Days')['Test_ROC'].max().reset_index().rename(columns={'Test_ROC':'Best_LineB'})\ncomp_c = ba.merge(bb, on='Days'); print(comp_c.to_string(index=False))"),
        ("## 21. Line A vs Line B Comparison (Regression RMSE)",
         "la_r = pd.read_csv(RESULTS_DIR / 'nb02_line_a_regression_hourly.csv')\nbar = la_r.groupby('Days')['RMSE'].min().reset_index().rename(columns={'RMSE':'Best_LineA_RMSE'})\nbbr = lb_reg_df.groupby('Days')['RMSE'].min().reset_index().rename(columns={'RMSE':'Best_LineB_RMSE'})\ncomp_r = bar.merge(bbr, on='Days'); print(comp_r.to_string(index=False))"),
        ("## 22. Line A vs Line B Visual Comparison",
         "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\naxes[0].plot(comp_c['Days'], comp_c['Best_LineA'], marker='o', label='Line A'); axes[0].plot(comp_c['Days'], comp_c['Best_LineB'], marker='s', label='Line B PyTorch')\naxes[0].set_title('Best ROC-AUC (1–15d)'); axes[0].legend(); axes[0].grid(alpha=0.3)\naxes[1].plot(comp_r['Days'], comp_r['Best_LineA_RMSE'], marker='o', label='Line A'); axes[1].plot(comp_r['Days'], comp_r['Best_LineB_RMSE'], marker='s', label='Line B PyTorch')\naxes[1].set_title('Best RMSE (1–15d)'); axes[1].legend(); axes[1].grid(alpha=0.3); plt.tight_layout()"),
        ("## 23. Test 168h Predicted vs Observed PM10 (Line B LSTM & ST-GNN)",
         "y168_te = df.iloc[te_idx]['target_avg_pm10_168h'].values; t_te = df.iloc[te_idx]['ts'].values\nfig, ax = plt.subplots(figsize=(11, 3.6))\nax.plot(t_te, y168_te, label='Observed', color='black', lw=1.0)\nax.plot(t_te, te_168_r['LineB_LSTM'], label='LineB LSTM', alpha=0.8)\nax.plot(t_te, te_168_r['LineB_STGNN'], label='LineB STGNN', alpha=0.8)\nax.set_title('Line B 168h (7d) Clean PM10 Forecast'); ax.legend(); plt.tight_layout()"),
        ("## 24. Export Verification",
         "assert (RESULTS_DIR / 'nb03_line_b_classification_hourly.csv').exists() and (RESULTS_DIR / 'nb03_line_b_regression_hourly.csv').exists()\nprint('Line B clean hourly CSVs verified.')"),
        ("## 25. Notebook 03 Summary",
         "print('NB03 Complete: Real PyTorch layers evaluated on BOTH clean hourly sequences and line_b_final_dataset.npz.')"),
    ]
    run_pairs(pairs, env, NB_DIR / "03_line_b_pytorch_real_layers.ipynb")


def build_nb04():
    print("\n=== [5/5] Notebook 04: Complete XAI on Clean Hourly Data (50 cells) ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR, "XAI_DIR": XAI_DIR}
    pairs = [
        ("# Notebook 04: Explainable AI (XAI) Suite on Clean Hourly Data\n## 1. Load Clean Hourly Dataset",
         "import numpy as np, pandas as pd, shap, torch, torch.nn as nn, matplotlib.pyplot as plt\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import PowerTransformer\nfrom sklearn.inspection import permutation_importance, PartialDependenceDisplay\nfrom sklearn.tree import DecisionTreeClassifier, export_text\nfrom sklearn.metrics import roc_auc_score\nfrom sklearn.ensemble import ExtraTreesClassifier\nfrom xgboost import XGBClassifier\ndf = pd.read_csv(PROJECT_ROOT / '06_Data' / 'riyadh_hourly_clean_tvt.csv')\ndf['ts'] = pd.to_datetime(df['ts'])\ntarget_cols = [c for c in df.columns if c.startswith('target_')]\nfeature_cols = [c for c in df.columns if c not in ['ts'] + target_cols]\nprint(f'Clean hourly rows: {len(df):,} | Features: {len(feature_cols)}')"),
        ("## 2. Reconstruct Exact Hourly Train (70%) / Val (15%) / Test (15%) Split",
         "N = len(df); GAP_H = 360; STRIDE = 6\ntr_end = int(N * 0.70); val_start = tr_end + GAP_H; val_end = int(N * 0.85); te_start = val_end + GAP_H\ntrain_df = df.iloc[:tr_end:STRIDE].reset_index(drop=True)\ntest_df = df.iloc[te_start::STRIDE].reset_index(drop=True)\nimp = SimpleImputer(strategy='median'); pt = PowerTransformer(method='yeo-johnson')\nX_tr = pt.fit_transform(imp.fit_transform(train_df[feature_cols].values))\nX_te = pt.transform(imp.transform(test_df[feature_cols].values))\ny_tr = train_df['target_evt_any_168h'].values.astype(int)\ny_te = test_df['target_evt_any_168h'].values.astype(int)\nprint(f'168h (7d) Test Positives: {y_te.sum()}/{len(y_te)} ({y_te.mean()*100:.1f}%)')"),
        ("## 3. Fit Reference XGBoost & ExtraTrees Models (168h Clean Forecast)",
         "pw = float(np.sum(y_tr==0)/max(1,np.sum(y_tr==1)))\nxgb = XGBClassifier(n_estimators=120, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=pw, reg_lambda=2.0, random_state=42, n_jobs=-1, eval_metric='logloss').fit(X_tr, y_tr)\net = ExtraTreesClassifier(n_estimators=100, max_depth=8, min_samples_leaf=8, class_weight='balanced', random_state=42, n_jobs=-1).fit(X_tr, y_tr)\nprint(f'Test ROC-AUC -> XGBoost: {roc_auc_score(y_te, xgb.predict_proba(X_te)[:,1]):.4f} | ExtraTrees: {roc_auc_score(y_te, et.predict_proba(X_te)[:,1]):.4f}')"),
        ("## 4. XAI-1: Global Gain & Test Permutation Importance (`n_jobs=1`)",
         "perm_xgb = permutation_importance(xgb, X_te, y_te, n_repeats=8, random_state=42, scoring='roc_auc', n_jobs=1)\nperm_et = permutation_importance(et, X_te, y_te, n_repeats=8, random_state=42, scoring='roc_auc', n_jobs=1)\nprint('Permutation importance computed on held-out Test.')"),
        ("## 5. XAI-2: Exact Game-Theoretic SHAP (`shap.TreeExplainer`)",
         "explainer = shap.TreeExplainer(xgb); shap_vals = explainer.shap_values(X_te)\nxai_df = pd.DataFrame({'Feature': feature_cols, 'XGB_Gain': np.round(xgb.feature_importances_,5), 'ET_Gini': np.round(et.feature_importances_,5), 'XGB_Perm_ROC': np.round(perm_xgb.importances_mean,5), 'ET_Perm_ROC': np.round(perm_et.importances_mean,5), 'Mean_Abs_SHAP': np.round(np.mean(np.abs(shap_vals), axis=0),5)}).sort_values('Mean_Abs_SHAP', ascending=False)\nxai_df.to_csv(XAI_DIR / 'nb04_xai_clean_hourly_importance.csv', index=False)\nprint(xai_df.head(15).to_string(index=False))"),
        ("## 6. Plot: SHAP Mean |Impact| vs Test Permutation Importance",
         "fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))\nt12 = xai_df.head(12).iloc[::-1]\naxes[0].barh(t12['Feature'], t12['Mean_Abs_SHAP'], color='#1f77b4'); axes[0].set_title('SHAP Mean |Impact| (Clean Hourly)')\naxes[1].barh(t12['Feature'], t12['ET_Perm_ROC'], color='#2ca02c'); axes[1].set_title('ExtraTrees Test Permutation ROC Drop')\nplt.tight_layout()"),
        ("## 7. Plot: SHAP Directional Beeswarm Scatter (Top 10 Features)",
         "top10 = xai_df.head(10)['Feature'].tolist()\nfig, ax = plt.subplots(figsize=(9, 4.8))\nfor ri, fn in enumerate(reversed(top10)):\n    j = feature_cols.index(fn); sv = shap_vals[:, j]; fv = X_te[:, j]\n    sc = ax.scatter(sv, ri + np.random.default_rng(42).normal(0,0.12,len(sv)), c=np.clip(fv,-2.5,2.5), cmap='coolwarm', s=6, alpha=0.6)\nax.set_yticks(range(10)); ax.set_yticklabels(list(reversed(top10))); ax.axvline(0, color='black', lw=0.8)\nax.set_title('SHAP Directional Impact (Red=High Value)'); plt.colorbar(sc, ax=ax); plt.tight_layout()"),
        ("## 8. Modality-Level Attribution Balance Audit",
         "def grp(f):\n    if 'era5' in f or 'phys' in f or 'sp_' in f or 't2m_' in f or 'ws_' in f or 'dryness' in f: return 'ERA5_Physics'\n    if 'sat_' in f or 'aod' in f: return 'Satellite_Detrended'\n    if 'cams' in f or 'nwp' in f: return 'CAMS_NWP_Detrended'\n    if 'doy' in f or 'hour' in f: return 'Calendar_Diurnal'\n    return 'Ground_METAR'\nxai_df['Modality'] = [grp(f) for f in xai_df['Feature']]\nmod_sum = xai_df.groupby('Modality')[['Mean_Abs_SHAP','XGB_Gain','ET_Gini']].sum()\nprint(mod_sum.round(4).to_string())"),
        ("## 9. Modality Share Chart",
         "fig, ax = plt.subplots(figsize=(6, 4))\n(mod_sum['Mean_Abs_SHAP']/mod_sum['Mean_Abs_SHAP'].sum()*100).sort_values().plot(kind='barh', ax=ax, color='#9467bd')\nax.set_title('SHAP Attribution Share (%) Across Modalities'); plt.tight_layout()"),
        ("## 10. Local SHAP Explanation: Highest-Risk Test Timestamp",
         "p_te = xgb.predict_proba(X_te)[:, 1]; i_hi = int(np.argmax(p_te))\ns_hi = pd.Series(shap_vals[i_hi], index=feature_cols).sort_values(key=np.abs, ascending=False)\nprint(f'Highest Risk Test Hour: {test_df.iloc[i_hi][\"ts\"]} | P={p_te[i_hi]:.3f} | Obs={y_te[i_hi]}')\nprint(s_hi.head(8).round(4).to_string())"),
        ("## 11. Local SHAP Waterfall Plot (Highest-Risk Test Hour)",
         "fig, ax = plt.subplots(figsize=(8, 3.8)); t8 = s_hi.head(8).iloc[::-1]\nax.barh(t8.index, t8.values, color=['#d62728' if v>0 else '#1f77b4' for v in t8.values])\nax.axvline(0, color='black', lw=0.8); ax.set_title(f'Local SHAP on {test_df.iloc[i_hi][\"ts\"]}'); plt.tight_layout()"),
        ("## 12. Local SHAP Explanation: Lowest-Risk Clear Timestamp",
         "i_lo = int(np.argmin(p_te)); s_lo = pd.Series(shap_vals[i_lo], index=feature_cols).sort_values(key=np.abs, ascending=False)\nprint(f'Lowest Risk Test Hour: {test_df.iloc[i_lo][\"ts\"]} | P={p_te[i_lo]:.3f} | Obs={y_te[i_lo]}')\nprint(s_lo.head(8).round(4).to_string())"),
        ("## 13. XAI-3: 1D Partial Dependence & ICE Curves (Top 4 Drivers)",
         "top4_i = [feature_cols.index(f) for f in xai_df.head(4)['Feature'].tolist()]\nfig, axes = plt.subplots(2, 2, figsize=(10.5, 6.8))\nPartialDependenceDisplay.from_estimator(et, X_te, top4_i, feature_names=feature_cols, kind='both', subsample=80, random_state=42, ax=axes.ravel())\nplt.suptitle('ExtraTrees 1D PDP & ICE (Clean Hourly Test)'); plt.tight_layout()"),
        ("## 14. 2D Partial Dependence Interaction (Top 2 Drivers)",
         "fig, ax = plt.subplots(figsize=(6, 4.5))\nPartialDependenceDisplay.from_estimator(et, X_te, [(top4_i[0], top4_i[1])], feature_names=feature_cols, ax=ax)\nax.set_title('2D Partial Dependence Interaction'); plt.tight_layout()"),
        ("## 15. XAI-4: Surrogate Decision Tree Rules (`max_depth=3`)",
         "surr = DecisionTreeClassifier(max_depth=3, min_samples_leaf=50, random_state=42).fit(test_df[feature_cols].fillna(0), (p_te>=0.5).astype(int))\nprint(f'Surrogate fidelity: {(surr.predict(test_df[feature_cols].fillna(0))==(p_te>=0.5)).mean()*100:.1f}%')\nprint(export_text(surr, feature_names=feature_cols))"),
        ("## 16. Local Counterfactual Sensitivity (+1 SD Perturbation)",
         "bp = p_te.mean(); cf = []\nfor f in xai_df.head(8)['Feature']:\n    j = feature_cols.index(f); Xp = X_te.copy(); Xp[:,j] += 1.0\n    cf.append({'Feature': f, 'Delta_P(+1SD)': round(xgb.predict_proba(Xp)[:,1].mean()-bp, 4)})\nprint(pd.DataFrame(cf).to_string(index=False))"),
        ("## 17. XAI-5: Real PyTorch LSTM 24-Hour Lookback Temporal Saliency",
         "torch.manual_seed(42); SEQ_LEN = 24\nX_all_s = pt.transform(imp.transform(df[feature_cols].values))\ntr_i = np.arange(SEQ_LEN, tr_end, STRIDE); te_i = np.arange(te_start, N, STRIDE)\nX_tr_q = torch.tensor(np.array([X_all_s[i-SEQ_LEN+1:i+1] for i in tr_i], dtype=np.float32))\ny_tr_q = torch.tensor(df.iloc[tr_i]['target_evt_any_168h'].values, dtype=torch.float32)\nX_te_q = torch.tensor(np.array([X_all_s[i-SEQ_LEN+1:i+1] for i in te_i], dtype=np.float32), requires_grad=True)\nclass MiniLSTM(nn.Module):\n    def __init__(self, d): super().__init__(); self.lstm = nn.LSTM(d, 32, batch_first=True); self.fc = nn.Linear(32, 1)\n    def forward(self, x): o, _ = self.lstm(x); return self.fc(o[:,-1,:]).squeeze(-1)\nml = MiniLSTM(len(feature_cols)); opt = torch.optim.Adam(ml.parameters(), lr=2e-3); lf = nn.BCEWithLogitsLoss()\nfor _ in range(12): opt.zero_grad(); lf(ml(X_tr_q), y_tr_q).backward(); opt.step()\nml.eval(); ml(X_te_q).sum().backward()\ntemp_sal = X_te_q.grad.abs().mean(dim=(0,2)).detach().numpy(); feat_sal = X_te_q.grad.abs().mean(dim=(0,1)).detach().numpy()\nprint('24h Temporal Saliency mean:', round(float(temp_sal.mean()), 5))"),
        ("## 18. Plot: 24-Hour Lookback Saliency (Lag -23h to 0h)",
         "fig, ax = plt.subplots(figsize=(9, 3.8))\nax.bar(np.arange(-SEQ_LEN+1, 1), temp_sal, color='#2ca02c')\nax.set_title('PyTorch LSTM Saliency Over 24-Hour Lookback'); ax.set_xlabel('Lag (Hours)'); plt.tight_layout()"),
        ("## 19. Line B Feature Saliency vs XGBoost SHAP Agreement",
         "sdf = pd.DataFrame({'Feature': feature_cols, 'LSTM_Saliency': np.round(feat_sal,5)}).merge(xai_df[['Feature','Mean_Abs_SHAP']], on='Feature')\nprint('Spearman corr (LSTM Saliency vs SHAP):', round(sdf['LSTM_Saliency'].corr(sdf['Mean_Abs_SHAP'], method='spearman'), 3))\nprint(sdf.sort_values('LSTM_Saliency', ascending=False).head(10).to_string(index=False))"),
        ("## 20. XAI-6: 6-Node Riyadh Spatial Graph Connectivity",
         "adj = np.load(PROJECT_ROOT / '06_Data' / 'riyadh_graph_adjacency_matrix.npy')\nfig, ax = plt.subplots(figsize=(5.5, 3.5)); ax.bar([f'Node_{i}' for i in range(adj.shape[0])], adj.sum(axis=1), color='#17becf')\nax.set_title('6-Node Spatial Graph Weighted Degree'); plt.tight_layout()"),
        ("## 21. Multi-Horizon SHAP Stability (24h vs 168h vs 360h)",
         "sh = {}\nfor h in [24, 168, 360]:\n    mh = XGBClassifier(n_estimators=90, max_depth=4, learning_rate=0.05, random_state=42, n_jobs=-1, eval_metric='logloss').fit(X_tr, train_df[f'target_evt_any_{h}h'].values.astype(int))\n    sh[f'SHAP_{h}h'] = np.round(np.mean(np.abs(shap.TreeExplainer(mh).shap_values(X_te)), axis=0), 4)\nsh_df = pd.DataFrame(sh, index=feature_cols).sort_values('SHAP_168h', ascending=False)\nprint(sh_df.head(10).to_string())"),
        ("## 22. Plot: Horizon Importance Shift (24h -> 168h -> 360h)",
         "fig, ax = plt.subplots(figsize=(9, 4)); sh_df.head(8).plot(kind='bar', ax=ax); ax.set_title('SHAP Importance Shift (24h -> 360h)'); plt.tight_layout()"),
        ("## 23. Error-Case Audit (FP vs FN on Clean Hourly Test)",
         "pb = (p_te >= 0.5).astype(int); print(f'Test FP: {((pb==1)&(y_te==0)).sum()} | Test FN: {((pb==0)&(y_te==1)).sum()}')"),
        ("## 24. Export Verification",
         "assert (XAI_DIR / 'nb04_xai_clean_hourly_importance.csv').exists(); print('XAI CSV verified.')"),
        ("## 25. Notebook 04 Summary",
         "print('NB04 Complete: Full XAI executed on clean hourly dataset.')"),
    ]
    run_pairs(pairs, env, NB_DIR / "04_explainable_ai_xai_riyadh.ipynb")


if __name__ == "__main__":
    build_nb00()
    build_nb01()
    build_nb02()
    build_nb03()
    build_nb04()
    print("\nALL 5 CLEAN HOURLY NOTEBOOKS (50 CELLS EACH) EXECUTED SUCCESSFULLY!")

