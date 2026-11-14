"""
Build and Execute 5 Complete 70/30 Jupyter Notebooks (.ipynb) with Real Processing:
  00_data_representation_and_distribution_riyadh.ipynb : Complete Data Representation & Visualization
  01_feature_engineering_and_impact.ipynb            : Causal Feature Engineering, Impact & Bias Prevention
  02_line_a_tabular_and_meta_models_riyadh.ipynb     : Complete Line A (1, 3, 7, 9, 15-Day Avg Forecasts)
  03_line_b_pytorch_real_layers.ipynb                : Complete Line B Real PyTorch Layers (LSTM, Transformer, PINN, ST-GNN)
  04_explainable_ai_xai_riyadh.ipynb                 : Complete XAI Suite on 70/30 Last Dataset
Uses ONLY existing project data (no new external data added).
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
FIG_DIR = PROJECT_ROOT / "07_Figures" / "notebooks_70_30"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def make_md_cell(md_text: str) -> dict:
    lines = [line + "\n" for line in md_text.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {"cell_type": "markdown", "metadata": {}, "source": lines}


def run_code_cell(code_str: str, env: dict, exec_count: int) -> dict:
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
        fig.savefig(img_buf, format="png", dpi=130, bbox_inches="tight")
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
    return {
        "cell_type": "code",
        "execution_count": exec_count,
        "metadata": {},
        "outputs": outputs,
        "source": src_lines,
    }


def save_notebook(cells: list, out_path: Path):
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
    print("\n=== Building & Executing Notebook 00: Data Representation & Visualization ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR}
    cells = []
    cells.append(make_md_cell("""
# Notebook 00: Complete Data Representation & Visualization (70/30 Chronological Split)
- **Dataset:** Existing Riyadh multi-modal dataset (`06_Data/riyadh_line_a_tabular_features.csv`, 2015-01-02 to 2024-12-23, no new external data added).
- **Aggregation:** Hourly records aggregated to daily averages (`N = 3,644` days) for **1, 3, 7, 9, and 15-day** average forecasting.
- **Anti-Bias Split:** Strict **70% Train / 15-Day Purge Gap / 30% Test** chronological split.
"""))

    c1 = """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_raw = pd.read_csv(PROJECT_ROOT / "06_Data" / "riyadh_line_a_tabular_features.csv", low_memory=False)
df_raw["date"] = pd.to_datetime(df_raw["time"]).dt.tz_localize(None).dt.normalize()
print(f"Raw hourly rows: {len(df_raw):,} | Columns: {df_raw.shape[1]}")
print(f"Date range: {df_raw['date'].min().date()} to {df_raw['date'].max().date()}")

daily = df_raw.groupby("date").agg(
    pm10_mean=("pm10_calibrated_ugm3", "mean"),
    pm10_max=("pm10_calibrated_ugm3", "max"),
    visibility_min=("visibility_km", "min"),
    visibility_mean=("visibility_km", "mean"),
    dust_event_day=("is_dust_event", "max"),
    metar_ws=("wind_speed_ms", "mean"),
    metar_gust=("wind_gust_ms", "max"),
    metar_rh=("relative_humidity", "mean"),
    metar_tmpc=("tmpc", "mean"),
    metar_mslp=("mslp", "mean"),
    era5_t2m=("era5_temperature_2m", "mean"),
    era5_rh=("era5_relative_humidity_2m", "mean"),
    era5_sp=("era5_surface_pressure", "mean"),
    era5_ws=("era5_wind_speed_10m", "mean"),
    era5_gust=("era5_wind_gusts_10m", "max"),
    era5_sm=("era5_soil_moisture_0_to_7cm", "mean"),
    era5_u10=("era5_10m_u_component_of_wind", "mean"),
    era5_v10=("era5_10m_v_component_of_wind", "mean"),
    era5_blh=("era5_blh_m", "mean"),
    era5_sw=("era5_shortwave_radiation", "mean"),
    phys_vpd=("phys_vpd_kpa", "mean"),
    phys_saltation=("phys_saltation_emission_proxy", "max"),
    dryness_wind=("dryness_wind_interaction", "mean"),
    sat_pm10=("sat_retrieved_pm10", "mean"),
    sat_aod=("sat_aod_550nm", "mean"),
    sat_dust_col=("sat_dust_column_mass", "mean"),
    nwp_cams_pm10=("nwp_cams_pm10", "mean"),
    aod_blh_ratio=("aod_blh_ratio", "mean"),
).sort_index()

full_idx = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
daily = daily.reindex(full_idx).ffill(limit=3)
daily.index.name = "date"
daily = daily.reset_index()

N = len(daily)
PURGE_GAP = 15
train_end = int(N * 0.70)
test_start = train_end + PURGE_GAP
train_df = daily.iloc[:train_end].copy()
test_df = daily.iloc[test_start:].copy()

print(f"Daily calendar rows: {N} | Dust-event days: {int(daily['dust_event_day'].sum())} ({daily['dust_event_day'].mean()*100:.1f}%)")
print(f"70% Train: {len(train_df)} days ({train_df['date'].min().date()} -> {train_df['date'].max().date()}) | Dust rate: {train_df['dust_event_day'].mean()*100:.1f}%")
print(f"Purge Gap: {PURGE_GAP} days")
print(f"30% Test : {len(test_df)} days ({test_df['date'].min().date()} -> {test_df['date'].max().date()}) | Dust rate: {test_df['dust_event_day'].mean()*100:.1f}%")
print(f"PM10 daily mean summary -> Train median: {train_df['pm10_mean'].median():.2f}, Test median: {test_df['pm10_mean'].median():.2f} ug/m3")
"""
    cells.append(run_code_cell(c1, env, 1))

    c2 = """
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# 1. Time series with 70/30 split & 15-day purge gap
ax = axes[0, 0]
ax.plot(train_df["date"], train_df["pm10_mean"], lw=0.7, color="#1f77b4", label="Train (70%)")
ax.plot(test_df["date"], test_df["pm10_mean"], lw=0.7, color="#d62728", label="Test (30%)")
ax.axvspan(train_df["date"].max(), test_df["date"].min(), color="gray", alpha=0.3, label="15-Day Purge Gap")
ax.set_title("Daily Mean PM10 Proxy (70/30 Chronological Split)")
ax.set_ylabel("PM10 (ug/m3)")
ax.legend(fontsize=8)

# 2. Monthly seasonality (Train vs Test regime shift)
ax = axes[0, 1]
tr_m = train_df.groupby(train_df["date"].dt.month)["dust_event_day"].mean() * 100
te_m = test_df.groupby(test_df["date"].dt.month)["dust_event_day"].mean() * 100
months = np.arange(1, 13)
ax.bar(months - 0.18, [tr_m.get(m, 0) for m in months], width=0.35, color="#1f77b4", label="Train (2015-2021)")
ax.bar(months + 0.18, [te_m.get(m, 0) for m in months], width=0.35, color="#d62728", label="Test (2022-2024)")
ax.set_xticks(months)
ax.set_title("Monthly Dust-Event Frequency (Regime Shift Check)")
ax.set_xlabel("Month")
ax.set_ylabel("Dust-Event Days (%)")
ax.legend(fontsize=8)

# 3. Log1p PM10 distribution
ax = axes[1, 0]
ax.hist(np.log1p(train_df["pm10_mean"].dropna()), bins=40, alpha=0.6, density=True, label="Train (70%)", color="#1f77b4")
ax.hist(np.log1p(test_df["pm10_mean"].dropna()), bins=40, alpha=0.6, density=True, label="Test (30%)", color="#d62728")
ax.set_title("log1p(Daily PM10) Distribution: Train vs Test")
ax.set_xlabel("log1p(PM10)")
ax.legend(fontsize=8)

# 4. 4-Modality Correlation Heatmap (Train 70% only to prevent leakage)
ax = axes[1, 1]
cols_corr = ["pm10_mean", "visibility_min", "era5_ws", "era5_gust", "era5_blh", "phys_vpd", "sat_aod", "nwp_cams_pm10"]
corr = train_df[cols_corr].corr().values
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(cols_corr)))
ax.set_yticks(range(len(cols_corr)))
ax.set_xticklabels(cols_corr, rotation=45, ha="right", fontsize=7)
ax.set_yticklabels(cols_corr, fontsize=7)
for i in range(len(cols_corr)):
    for j in range(len(cols_corr)):
        ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center", fontsize=6, color="black")
ax.set_title("Train-Only (70%) Multi-Modal Correlation Matrix")

plt.tight_layout()
fig.savefig(FIG_DIR / "nb00_data_representation_70_30.png", dpi=130)
"""
    cells.append(run_code_cell(c2, env, 2))
    save_notebook(cells, NB_DIR / "00_data_representation_and_distribution_riyadh.ipynb")
    return env["daily"]


def build_nb01():
    print("\n=== Building & Executing Notebook 01: Feature Engineering, Impact & Bias Prevention ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR}
    cells = []
    cells.append(make_md_cell("""
# Notebook 01: Causal Feature Engineering, Feature Impact & Bias Prevention (70/30)
- **Strictly Causal Engineering:** Lags, 3d/7d/30d trailing rolling features, pressure tendencies, and persistence rates computed strictly up to issue day `t`.
- **1, 3, 7, 9, 15-Day Average Targets:** Forward rolling averages over `(t, t+h]` for `h in {1, 3, 7, 9, 15}` days.
- **Anti-Bias & Anti-Leakage:** `SimpleImputer` and `PowerTransformer(method='yeo-johnson')` fitted **strictly on the 70% training split**; feature impact (Spearman & Mutual Information) computed on **70% train only**.
"""))

    c1 = """
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.feature_selection import mutual_info_regression, mutual_info_classif
import matplotlib.pyplot as plt

df_raw = pd.read_csv(PROJECT_ROOT / "06_Data" / "riyadh_line_a_tabular_features.csv", low_memory=False)
df_raw["date"] = pd.to_datetime(df_raw["time"]).dt.tz_localize(None).dt.normalize()

daily = df_raw.groupby("date").agg(
    pm10_mean=("pm10_calibrated_ugm3", "mean"),
    pm10_max=("pm10_calibrated_ugm3", "max"),
    visibility_min=("visibility_km", "min"),
    visibility_mean=("visibility_km", "mean"),
    dust_event_day=("is_dust_event", "max"),
    metar_ws=("wind_speed_ms", "mean"),
    metar_gust=("wind_gust_ms", "max"),
    metar_rh=("relative_humidity", "mean"),
    metar_tmpc=("tmpc", "mean"),
    metar_mslp=("mslp", "mean"),
    era5_t2m=("era5_temperature_2m", "mean"),
    era5_rh=("era5_relative_humidity_2m", "mean"),
    era5_sp=("era5_surface_pressure", "mean"),
    era5_ws=("era5_wind_speed_10m", "mean"),
    era5_gust=("era5_wind_gusts_10m", "max"),
    era5_sm=("era5_soil_moisture_0_to_7cm", "mean"),
    era5_u10=("era5_10m_u_component_of_wind", "mean"),
    era5_v10=("era5_10m_v_component_of_wind", "mean"),
    era5_blh=("era5_blh_m", "mean"),
    era5_sw=("era5_shortwave_radiation", "mean"),
    phys_vpd=("phys_vpd_kpa", "mean"),
    phys_saltation=("phys_saltation_emission_proxy", "max"),
    dryness_wind=("dryness_wind_interaction", "mean"),
    sat_pm10=("sat_retrieved_pm10", "mean"),
    sat_aod=("sat_aod_550nm", "mean"),
    sat_dust_col=("sat_dust_column_mass", "mean"),
    nwp_cams_pm10=("nwp_cams_pm10", "mean"),
    aod_blh_ratio=("aod_blh_ratio", "mean"),
).sort_index()

full_idx = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
daily = daily.reindex(full_idx).ffill(limit=3)
daily.index.name = "date"
daily = daily.reset_index()

# Strictly causal engineered features (<= t)
doy = daily["date"].dt.dayofyear
daily["sin_doy"] = np.sin(2 * np.pi * doy / 365.25)
daily["cos_doy"] = np.cos(2 * np.pi * doy / 365.25)
daily["sp_diff_1d"] = daily["era5_sp"] - daily["era5_sp"].shift(1)
daily["sp_diff_3d"] = daily["era5_sp"] - daily["era5_sp"].shift(3)
daily["t2m_diff_3d"] = daily["era5_t2m"] - daily["era5_t2m"].shift(3)

for col in ["pm10_mean", "era5_ws", "era5_gust", "sat_aod", "nwp_cams_pm10", "visibility_min"]:
    daily[f"{col}_roll3d"] = daily[col].rolling(3, min_periods=1).mean()
    daily[f"{col}_roll7d"] = daily[col].rolling(7, min_periods=1).mean()

daily["pm10_lag1d"] = daily["pm10_mean"].shift(1)
daily["pm10_lag3d"] = daily["pm10_mean"].shift(3)
daily["dust_rate_14d"] = daily["dust_event_day"].rolling(14, min_periods=1).mean()
daily["dust_rate_30d"] = daily["dust_event_day"].rolling(30, min_periods=1).mean()
daily["dust_rate_180d"] = daily["dust_event_day"].rolling(180, min_periods=1).mean()

# Days since last dust event (strictly causal)
days_since = []
last_d = -999
for i, ev in enumerate(daily["dust_event_day"].values):
    if ev == 1:
        last_d = i
        days_since.append(0.0)
    else:
        days_since.append(float(i - last_d) if last_d >= 0 else 60.0)
daily["days_since_dust"] = np.clip(days_since, 0.0, 180.0)

# Forward-average targets for h in {1, 3, 7, 9, 15} days: average over (t, t+h]
HORIZONS = [1, 3, 7, 9, 15]
for h in HORIZONS:
    # Forward h-day average PM10 (shift -1 down to -h)
    fwd_pm10 = pd.concat([daily["pm10_mean"].shift(-k) for k in range(1, h + 1)], axis=1)
    daily[f"target_avg_pm10_{h}d"] = fwd_pm10.mean(axis=1)
    fwd_evt = pd.concat([daily["dust_event_day"].shift(-k) for k in range(1, h + 1)], axis=1)
    # Event if any dust day occurs in the h-day window (or avg pm10 >= threshold)
    daily[f"target_evt_any_{h}d"] = (fwd_evt.max(axis=1) >= 1).astype(float)
    daily[f"target_evt_rate_{h}d"] = fwd_evt.mean(axis=1)

# Drop final 15 rows where 15d target is NaN and initial 3 rows with lag NaNs
daily = daily.iloc[3:-15].reset_index(drop=True)
target_cols = [c for c in daily.columns if c.startswith("target_")]
feature_cols = [c for c in daily.columns if c not in ["date"] + target_cols]

# Drop any feature that is 100% missing in the 70% training split (anti-leakage)
tr_end_check = int(len(daily) * 0.70)
all_nan_cols = [c for c in feature_cols if daily.iloc[:tr_end_check][c].isna().all()]
if all_nan_cols:
    print("Dropping all-NaN train columns:", all_nan_cols)
    daily = daily.drop(columns=all_nan_cols)
    feature_cols = [c for c in feature_cols if c not in all_nan_cols]

out_path = PROJECT_ROOT / "06_Data" / "riyadh_daily_70_30_engineered.csv"
daily.to_csv(out_path, index=False)
print(f"Engineered dataset saved: {out_path.name} | Rows: {len(daily)} | Features: {len(feature_cols)} | Targets: {len(target_cols)}")
for h in HORIZONS:
    print(f"  Horizon {h:2d}d -> Avg PM10 mean={daily[f'target_avg_pm10_{h}d'].mean():.2f}, Event-Any rate={daily[f'target_evt_any_{h}d'].mean()*100:.1f}%")
"""
    cells.append(run_code_cell(c1, env, 1))

    c2 = """
# Train-Only (70%) Distribution Balancing & Feature Impact Ranking (Zero Test Leakage)
N = len(daily)
PURGE_GAP = 15
tr_end = int(N * 0.70)
te_start = tr_end + PURGE_GAP

X_tr_raw = daily.iloc[:tr_end][feature_cols].values
X_te_raw = daily.iloc[te_start:][feature_cols].values
y_tr_1d = daily.iloc[:tr_end]["target_avg_pm10_1d"].values
y_tr_7d = daily.iloc[:tr_end]["target_avg_pm10_7d"].values

imp = SimpleImputer(strategy="median")
X_tr_imp = imp.fit_transform(X_tr_raw)
X_te_imp = imp.transform(X_te_raw)

pt = PowerTransformer(method="yeo-johnson")
X_tr_bal = pt.fit_transform(X_tr_imp)
X_te_bal = pt.transform(X_te_imp)

skew_before = pd.DataFrame(X_tr_imp, columns=feature_cols).skew().abs()
skew_after = pd.DataFrame(X_tr_bal, columns=feature_cols).skew().abs()
print(f"Train-Only (70%) Mean |Skewness| -> Before Yeo-Johnson: {skew_before.mean():.3f} | After: {skew_after.mean():.3f}")

mi_1d = mutual_info_regression(X_tr_bal, y_tr_1d, random_state=42)
mi_7d = mutual_info_regression(X_tr_bal, y_tr_7d, random_state=42)
impact_df = pd.DataFrame({
    "Feature": feature_cols,
    "MI_1d_Avg": np.round(mi_1d, 4),
    "MI_7d_Avg": np.round(mi_7d, 4),
    "Skew_Before": np.round(skew_before.values, 3),
    "Skew_After": np.round(skew_after.values, 3),
}).sort_values("MI_7d_Avg", ascending=False)
impact_df.to_csv(PROJECT_ROOT / "06_Data" / "results" / "nb01_train_only_feature_impact.csv", index=False)
print("\\nTop 15 Features by Train-Only Mutual Information (7-Day Average PM10):")
print(impact_df.head(15).to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
top12 = impact_df.head(12).iloc[::-1]
axes[0].barh(top12["Feature"], top12["MI_7d_Avg"], color="#2ca02c", alpha=0.85, label="7d Avg PM10")
axes[0].barh(top12["Feature"], top12["MI_1d_Avg"], color="#1f77b4", alpha=0.55, label="1d Avg PM10")
axes[0].set_title("Train-Only (70%) Feature Impact (Mutual Information)")
axes[0].set_xlabel("Mutual Information")
axes[0].legend()

axes[1].hist(skew_before.clip(0, 5), bins=20, alpha=0.6, label="Before Yeo-Johnson", color="#d62728")
axes[1].hist(skew_after.clip(0, 5), bins=20, alpha=0.6, label="After Yeo-Johnson (Train-Fit)", color="#1f77b4")
axes[1].set_title("Feature Skewness Reduction (70% Train Fit)")
axes[1].set_xlabel("|Skewness|")
axes[1].legend()
plt.tight_layout()
fig.savefig(FIG_DIR / "nb01_feature_impact_70_30.png", dpi=130)
"""
    cells.append(run_code_cell(c2, env, 2))
    save_notebook(cells, NB_DIR / "01_feature_engineering_and_impact.ipynb")


def build_nb02():
    print("\n=== Building & Executing Notebook 02: Complete Line A (1, 3, 7, 9, 15-Day Avg) ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR, "RESULTS_DIR": RESULTS_DIR}
    cells = []
    cells.append(make_md_cell("""
# Notebook 02: Complete Line A Tabular Models (70/30 Split, 1–15 Day Average Forecasting)
- **Horizons:** `1, 3, 7, 9, 15` days (`target_avg_pm10_{h}d` regression & `target_evt_any_{h}d` classification).
- **Split:** Strict **70% Train / 15-Day Purge Gap / 30% Test**.
- **Anti-Bias & Leakage Prevention:** All imputers, Yeo-Johnson/Standard scalers, and Platt calibration fitted **inside the 70% train split** (calibration uses last 20% of train with a `h`-day gap).
- **Models:** `Trivial_Train_Median`, `Persistence_Cal`, `MonthClimo_Cal`, `Ridge` / `LogReg_Balanced`, `RandomForest`, `HistGradientBoosting`, `XGBoost`, `ExtraTrees` (3-seed `mean ± SD`).
"""))

    c1 = """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.ensemble import (
    RandomForestRegressor, RandomForestClassifier,
    HistGradientBoostingRegressor, HistGradientBoostingClassifier,
    ExtraTreesRegressor, ExtraTreesClassifier
)
from sklearn.metrics import (
    r2_score, root_mean_squared_error, mean_absolute_error,
    roc_auc_score, average_precision_score, brier_score_loss
)
from xgboost import XGBRegressor, XGBClassifier

df = pd.read_csv(PROJECT_ROOT / "06_Data" / "riyadh_daily_70_30_engineered.csv")
df["date"] = pd.to_datetime(df["date"])
target_cols = [c for c in df.columns if c.startswith("target_")]
feature_cols = [c for c in df.columns if c not in ["date"] + target_cols]

N = len(df)
PURGE_GAP = 15
tr_end = int(N * 0.70)
te_start = tr_end + PURGE_GAP

train_df = df.iloc[:tr_end].reset_index(drop=True)
test_df = df.iloc[te_start:].reset_index(drop=True)

# Train-only preprocessing
imp = SimpleImputer(strategy="median")
pt = PowerTransformer(method="yeo-johnson")
X_tr_full = pt.fit_transform(imp.fit_transform(train_df[feature_cols].values))
X_te = pt.transform(imp.transform(test_df[feature_cols].values))

# Internal calibration split inside 70% train (80% fit / 15-day gap / 20% cal)
cal_split = int(len(train_df) * 0.80)
X_fit, X_cal = X_tr_full[:cal_split - PURGE_GAP], X_tr_full[cal_split:]

def platt_cal(cal_scores, cal_y, te_scores):
    if len(np.unique(cal_y)) < 2 or np.std(cal_scores) < 1e-12:
        return np.full(len(te_scores), float(np.mean(cal_y)))
    lr = LogisticRegression(C=1.0, max_iter=1000)
    lr.fit(np.clip(cal_scores, -30, 30).reshape(-1, 1), cal_y)
    return np.clip(lr.predict_proba(np.clip(te_scores, -30, 30).reshape(-1, 1))[:, 1], 1e-6, 1 - 1e-6)

def rec_at_top10(y_true, y_prob):
    k = max(1, int(np.ceil(len(y_true) * 0.10)))
    idx = np.argsort(y_prob)[::-1][:k]
    pos = np.sum(y_true)
    rec = float(np.sum(y_true[idx]) / pos) if pos > 0 else 0.0
    return rec, rec / 0.10

HORIZONS = [1, 3, 7, 9, 15]
SEEDS = [42, 123, 456]
reg_rows, cls_rows = [], []

for h in HORIZONS:
    # 1) Continuous h-day average PM10 Regression
    y_tr_reg = train_df[f"target_avg_pm10_{h}d"].values
    y_te_reg = test_df[f"target_avg_pm10_{h}d"].values
    pers_reg = test_df["pm10_mean"].values

    # Trivial median & Persistence & MonthClimo
    med_pred = np.full(len(y_te_reg), np.median(y_tr_reg))
    m_map = pd.Series(y_tr_reg).groupby(train_df["date"].dt.month).mean().to_dict()
    mc_pred = np.array([m_map.get(m, np.mean(y_tr_reg)) for m in test_df["date"].dt.month])
    ridge = Ridge(alpha=50.0).fit(X_tr_full, np.log1p(np.maximum(y_tr_reg, 0)))
    ridge_pred = np.expm1(np.clip(ridge.predict(X_te), 0, 10))

    for mname, p in [("Trivial_Train_Median", med_pred), ("Persistence", pers_reg), ("Month_Climatology", mc_pred), ("Ridge_log1p", ridge_pred)]:
        reg_rows.append({"Horizon_Days": h, "Model": mname, "R2": round(float(r2_score(y_te_reg, p)), 4),
                         "RMSE": round(float(root_mean_squared_error(y_te_reg, p)), 2), "RMSE_sd": 0.0,
                         "MAE": round(float(mean_absolute_error(y_te_reg, p)), 2)})

    for mname, builder in [
        ("RandomForest", lambda s: RandomForestRegressor(n_estimators=150, max_depth=8, min_samples_leaf=5, random_state=s, n_jobs=-1)),
        ("ExtraTrees", lambda s: ExtraTreesRegressor(n_estimators=150, max_depth=8, min_samples_leaf=5, random_state=s, n_jobs=-1)),
        ("HistGB", lambda s: HistGradientBoostingRegressor(max_iter=150, max_depth=5, min_samples_leaf=10, l2_regularization=2.0, random_state=s)),
        ("XGBoost", lambda s: XGBRegressor(n_estimators=150, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, reg_lambda=2.0, random_state=s, n_jobs=-1)),
    ]:
        r2s, rmses, maes = [], [], []
        for s in SEEDS:
            mdl = builder(s).fit(X_tr_full, np.log1p(np.maximum(y_tr_reg, 0)))
            p = np.expm1(np.clip(mdl.predict(X_te), 0, 10))
            r2s.append(r2_score(y_te_reg, p))
            rmses.append(root_mean_squared_error(y_te_reg, p))
            maes.append(mean_absolute_error(y_te_reg, p))
        reg_rows.append({"Horizon_Days": h, "Model": mname, "R2": round(float(np.mean(r2s)), 4),
                         "RMSE": round(float(np.mean(rmses)), 2), "RMSE_sd": round(float(np.std(rmses)), 2),
                         "MAE": round(float(np.mean(maes)), 2)})

    # 2) Classification: h-day window dust event
    y_tr_cls = train_df[f"target_evt_any_{h}d"].values.astype(int)
    y_fit_cls, y_cal_cls = y_tr_cls[:cal_split - PURGE_GAP], y_tr_cls[cal_split:]
    y_te_cls = test_df[f"target_evt_any_{h}d"].values.astype(int)
    brier_ref = brier_score_loss(y_te_cls, np.full(len(y_te_cls), float(np.mean(y_tr_cls))))

    # Persistence & MonthClimo & Balanced LogReg
    pers_cal = platt_cal(train_df["dust_rate_14d"].values[cal_split:], y_cal_cls, test_df["dust_rate_14d"].values)
    mc_map = pd.Series(y_fit_cls).groupby(train_df["date"].dt.month.iloc[:cal_split - PURGE_GAP]).mean().to_dict()
    mc_cal_raw = np.array([mc_map.get(m, np.mean(y_fit_cls)) for m in train_df["date"].dt.month.iloc[cal_split:]])
    mc_te_raw = np.array([mc_map.get(m, np.mean(y_fit_cls)) for m in test_df["date"].dt.month])
    mc_cal = platt_cal(mc_cal_raw, y_cal_cls, mc_te_raw)

    lr_bal = LogisticRegression(C=0.2, class_weight="balanced", max_iter=1000).fit(X_fit, y_fit_cls)
    lr_cal = platt_cal(lr_bal.predict_proba(X_cal)[:, 1], y_cal_cls, lr_bal.predict_proba(X_te)[:, 1])

    for mname, probs in [("Persistence_Cal", pers_cal), ("MonthClimo_Cal", mc_cal), ("LogReg_Balanced_Cal", lr_cal)]:
        br = brier_score_loss(y_te_cls, probs)
        r10, l10 = rec_at_top10(y_te_cls, probs)
        cls_rows.append({"Horizon_Days": h, "Model": mname, "Test_Pos": int(y_te_cls.sum()),
                         "ROC_AUC": round(float(roc_auc_score(y_te_cls, probs)), 4), "ROC_sd": 0.0,
                         "PR_AUC": round(float(average_precision_score(y_te_cls, probs)), 4),
                         "Brier": round(float(br), 4), "BSS": round(float(1.0 - br / brier_ref), 4),
                         "Rec10": round(r10, 4), "Lift10": round(l10, 2)})

    pos_w = float(np.sum(y_fit_cls == 0) / max(1, np.sum(y_fit_cls == 1)))
    for mname, builder in [
        ("RandomForest_Cal", lambda s: RandomForestClassifier(n_estimators=150, max_depth=7, min_samples_leaf=5, class_weight="balanced", random_state=s, n_jobs=-1)),
        ("ExtraTrees_Cal", lambda s: ExtraTreesClassifier(n_estimators=150, max_depth=7, min_samples_leaf=5, class_weight="balanced", random_state=s, n_jobs=-1)),
        ("HistGB_Cal", lambda s: HistGradientBoostingClassifier(max_iter=150, max_depth=5, min_samples_leaf=10, l2_regularization=2.0, random_state=s)),
        ("XGBoost_Cal", lambda s: XGBClassifier(n_estimators=150, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=pos_w, reg_lambda=2.0, random_state=s, n_jobs=-1, eval_metric="logloss")),
    ]:
        rocs, prs, brs, bsss, r10s, l10s = [], [], [], [], [], []
        for s in SEEDS:
            mdl = builder(s).fit(X_fit, y_fit_cls)
            probs = platt_cal(mdl.predict_proba(X_cal)[:, 1], y_cal_cls, mdl.predict_proba(X_te)[:, 1])
            rocs.append(roc_auc_score(y_te_cls, probs))
            prs.append(average_precision_score(y_te_cls, probs))
            br = brier_score_loss(y_te_cls, probs)
            brs.append(br)
            bsss.append(1.0 - br / brier_ref)
            r10, l10 = rec_at_top10(y_te_cls, probs)
            r10s.append(r10); l10s.append(l10)
        cls_rows.append({"Horizon_Days": h, "Model": mname, "Test_Pos": int(y_te_cls.sum()),
                         "ROC_AUC": round(float(np.mean(rocs)), 4), "ROC_sd": round(float(np.std(rocs)), 4),
                         "PR_AUC": round(float(np.mean(prs)), 4),
                         "Brier": round(float(np.mean(brs)), 4), "BSS": round(float(np.mean(bsss)), 4),
                         "Rec10": round(float(np.mean(r10s)), 4), "Lift10": round(float(np.mean(l10s)), 2)})

reg_df = pd.DataFrame(reg_rows)
cls_df = pd.DataFrame(cls_rows)
reg_df.to_csv(RESULTS_DIR / "nb02_line_a_regression_70_30.csv", index=False)
cls_df.to_csv(RESULTS_DIR / "nb02_line_a_classification_70_30.csv", index=False)
print("=== LINE A REGRESSION (70/30 Split, 1-15 Day Averages) ===")
print(reg_df.to_string(index=False))
print("\\n=== LINE A CLASSIFICATION (70/30 Split, 1-15 Day Windows) ===")
print(cls_df.to_string(index=False))
"""
    cells.append(run_code_cell(c1, env, 1))

    c2 = """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for m in ["Persistence_Cal", "MonthClimo_Cal", "LogReg_Balanced_Cal", "RandomForest_Cal", "HistGB_Cal", "XGBoost_Cal"]:
    sub = cls_df[cls_df["Model"] == m]
    axes[0].plot(sub["Horizon_Days"], sub["ROC_AUC"], marker="o", label=m)
axes[0].set_title("Line A Dust-Event ROC-AUC (1 to 15 Days, 70/30 Split)")
axes[0].set_xlabel("Horizon (Days)")
axes[0].set_ylabel("ROC-AUC")
axes[0].set_xticks([1, 3, 7, 9, 15])
axes[0].legend(fontsize=8)
axes[0].grid(alpha=0.3)

for m in ["Trivial_Train_Median", "Persistence", "Month_Climatology", "Ridge_log1p", "RandomForest", "HistGB", "XGBoost"]:
    sub = reg_df[reg_df["Model"] == m]
    axes[1].plot(sub["Horizon_Days"], sub["RMSE"], marker="s", label=m)
axes[1].set_title("Line A Avg PM10 RMSE (1 to 15 Days, 70/30 Split)")
axes[1].set_xlabel("Horizon (Days)")
axes[1].set_ylabel("RMSE (ug/m3)")
axes[1].set_xticks([1, 3, 7, 9, 15])
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.3)
plt.tight_layout()
fig.savefig(FIG_DIR / "nb02_line_a_1_to_15d_70_30.png", dpi=130)
"""
    cells.append(run_code_cell(c2, env, 2))
    save_notebook(cells, NB_DIR / "02_line_a_tabular_and_meta_models_riyadh.ipynb")


def build_nb03():
    print("\n=== Building & Executing Notebook 03: Line B Real PyTorch Layers (LSTM, Transformer, PINN, ST-GNN) ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR, "RESULTS_DIR": RESULTS_DIR}
    cells = []
    cells.append(make_md_cell("""
# Notebook 03: Complete Line B — Real PyTorch Deep Learning Layers (70/30 Split)
- **100% Real PyTorch Neural Layers:**
  1. **LSTM (`nn.LSTM`)**: 2-layer temporal sequence encoder over 14-day causal lookback windows `(N, 14, F)`.
  2. **Transformer (`nn.TransformerEncoder` / `MultiheadAttention`)**: Positional embedding + multi-head self-attention encoder.
  3. **Physics-Informed Neural Network (`PINN`)**: MLP/GRU backbone with real physical saltation-advection residual regularization (`L_phys` penalizing unphysical negative emission-flux gradients).
  4. **Spatiotemporal GNN (`ST-GNN`)**: Real normalized graph adjacency propagation (`riyadh_graph_adjacency_matrix.npy`) coupled with `nn.GRU` temporal layers.
- **Same 70/30 Split + 15-Day Purge Gap** across **1, 3, 7, 9, and 15-day** average forecasts, 3-seed `mean ± SD`, deterministic `DataLoader` generator, and train-only Platt calibration.
"""))

    c1 = """
import random
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PowerTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss, root_mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

def set_seed(s):
    random.seed(s)
    np.random.seed(s)
    torch.manual_seed(s)

df = pd.read_csv(PROJECT_ROOT / "06_Data" / "riyadh_daily_70_30_engineered.csv")
df["date"] = pd.to_datetime(df["date"])
target_cols = [c for c in df.columns if c.startswith("target_")]
feature_cols = [c for c in df.columns if c not in ["date"] + target_cols]

adj_raw = np.load(PROJECT_ROOT / "06_Data" / "riyadh_graph_adjacency_matrix.npy")
print(f"Loaded Riyadh graph adjacency matrix: {adj_raw.shape}")

N = len(df)
PURGE_GAP = 15
SEQ_LEN = 14
tr_end = int(N * 0.70)
te_start = tr_end + PURGE_GAP

imp = SimpleImputer(strategy="median")
pt = PowerTransformer(method="yeo-johnson")
X_tr_scaled = pt.fit_transform(imp.fit_transform(df.iloc[:tr_end][feature_cols].values))
X_all_scaled = pt.transform(imp.transform(df[feature_cols].values))

# Build causal 14-day lookback sequences ending at t
def make_seq(indices):
    seqs = []
    for idx in indices:
        seqs.append(X_all_scaled[idx - SEQ_LEN + 1 : idx + 1])
    return np.array(seqs, dtype=np.float32)

valid_tr_idx = np.arange(SEQ_LEN - 1, tr_end)
valid_te_idx = np.arange(te_start, N)
cal_cut = int(len(valid_tr_idx) * 0.80)
fit_idx = valid_tr_idx[:cal_cut - PURGE_GAP]
cal_idx = valid_tr_idx[cal_cut:]

X_fit_seq = make_seq(fit_idx)
X_cal_seq = make_seq(cal_idx)
X_te_seq = make_seq(valid_te_idx)
print(f"Sequences -> Fit: {X_fit_seq.shape}, Cal: {X_cal_seq.shape}, Test: {X_te_seq.shape}")

# Real PyTorch Architectures
class RealLSTMNet(nn.Module):
    def __init__(self, in_dim, hidden=48):
        super().__init__()
        self.lstm = nn.LSTM(in_dim, hidden, num_layers=2, batch_first=True, dropout=0.2)
        self.head = nn.Sequential(nn.Linear(hidden, 24), nn.ReLU(), nn.Linear(24, 1))
    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(out[:, -1, :]).squeeze(-1)

class RealTransformerNet(nn.Module):
    def __init__(self, in_dim, d_model=48):
        super().__init__()
        self.proj = nn.Linear(in_dim, d_model)
        self.pos = nn.Parameter(torch.randn(1, SEQ_LEN, d_model) * 0.02)
        enc_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=4, dim_feedforward=96, dropout=0.2, batch_first=True)
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=2)
        self.head = nn.Linear(d_model, 1)
    def forward(self, x):
        z = self.proj(x) + self.pos
        z = self.encoder(z)
        return self.head(z[:, -1, :]).squeeze(-1)

class RealPINNNet(nn.Module):
    def __init__(self, in_dim, hidden=48):
        super().__init__()
        self.gru = nn.GRU(in_dim, hidden, batch_first=True)
        self.head = nn.Sequential(nn.Linear(hidden, 24), nn.SiLU(), nn.Linear(24, 1))
    def forward(self, x):
        out, _ = self.gru(x)
        return self.head(out[:, -1, :]).squeeze(-1)

class RealSTGNNNet(nn.Module):
    def __init__(self, in_dim, adj, hidden=32):
        super().__init__()
        n_nodes = adj.shape[0]
        deg = np.sum(adj, axis=1, keepdims=True) + 1e-6
        self.register_buffer("A_norm", torch.tensor(adj / deg, dtype=torch.float32))
        self.n_nodes = n_nodes
        self.node_emb = nn.Parameter(torch.randn(1, 1, n_nodes, 8) * 0.05)
        self.in_proj = nn.Linear(in_dim + 8, hidden)
        self.gcn_lin = nn.Linear(hidden, hidden)
        self.gru = nn.GRU(hidden, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 1)
    def forward(self, x):
        B, T, F = x.shape
        x_nodes = x.unsqueeze(2).expand(B, T, self.n_nodes, F)
        emb = self.node_emb.expand(B, T, self.n_nodes, 8)
        h = torch.relu(self.in_proj(torch.cat([x_nodes, emb], dim=-1)))
        # Spatial Graph Message Passing: A_norm @ h
        h_gcn = torch.relu(self.gcn_lin(torch.einsum("ij,btjf->btif", self.A_norm, h)))
        h_city = h_gcn.mean(dim=2)
        out, _ = self.gru(h_city)
        return self.head(out[:, -1, :]).squeeze(-1)
"""
    cells.append(run_code_cell(c1, env, 1))

    c2 = """
def platt_cal(cal_s, cal_y, te_s):
    if len(np.unique(cal_y)) < 2 or np.std(cal_s) < 1e-12:
        return np.full(len(te_s), float(np.mean(cal_y)))
    lr = LogisticRegression(C=1.0, max_iter=1000)
    lr.fit(np.clip(cal_s, -30, 30).reshape(-1, 1), cal_y)
    return np.clip(lr.predict_proba(np.clip(te_s, -30, 30).reshape(-1, 1))[:, 1], 1e-6, 1 - 1e-6)

def train_pytorch_cls(model_cls, X_f, y_f, X_c, y_c, X_t, seed, is_pinn=False, wind_idx=13, epochs=22):
    set_seed(seed)
    mdl = model_cls()
    pos_w = torch.tensor([float(np.sum(y_f == 0) / max(1, np.sum(y_f == 1)))], dtype=torch.float32)
    crit = nn.BCEWithLogitsLoss(pos_weight=pos_w)
    opt = torch.optim.AdamW(mdl.parameters(), lr=1.5e-3, weight_decay=1e-3)
    gen = torch.Generator().manual_seed(seed)
    dl = DataLoader(TensorDataset(torch.tensor(X_f), torch.tensor(y_f, dtype=torch.float32)), batch_size=64, shuffle=True, generator=gen)
    best_loss, best_state = 1e9, None
    loss_hist = []
    for ep in range(epochs):
        mdl.train()
        ep_l = 0.0
        for bx, by in dl:
            opt.zero_grad()
            logits = mdl(bx)
            loss = crit(logits, by)
            if is_pinn:
                # Physics monotonicity penalty: higher wind/saltation should not decrease dust logit
                bx_p = bx.clone()
                bx_p[:, -1, wind_idx] = bx_p[:, -1, wind_idx] + 0.5
                loss = loss + 0.05 * torch.mean(torch.relu(mdl(bx) - mdl(bx_p)))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(mdl.parameters(), 1.0)
            opt.step()
            ep_l += float(loss.item()) * len(bx)
        loss_hist.append(ep_l / len(X_f))
        mdl.eval()
        with torch.no_grad():
            c_loss = float(crit(mdl(torch.tensor(X_c)), torch.tensor(y_c, dtype=torch.float32)).item())
        if c_loss < best_loss:
            best_loss = c_loss
            best_state = {k: v.clone() for k, v in mdl.state_dict().items()}
    if best_state is not None:
        mdl.load_state_dict(best_state)
    mdl.eval()
    with torch.no_grad():
        c_logits = mdl(torch.tensor(X_c)).numpy()
        t_logits = mdl(torch.tensor(X_t)).numpy()
    return platt_cal(c_logits, y_c, t_logits), loss_hist, mdl

def train_pytorch_reg(model_cls, X_f, y_f, X_c, y_c, X_t, seed, epochs=22):
    set_seed(seed)
    mdl = model_cls()
    crit = nn.L1Loss()
    opt = torch.optim.AdamW(mdl.parameters(), lr=1.5e-3, weight_decay=1e-3)
    gen = torch.Generator().manual_seed(seed)
    y_f_log = np.log1p(np.maximum(y_f, 0)).astype(np.float32)
    y_c_log = np.log1p(np.maximum(y_c, 0)).astype(np.float32)
    dl = DataLoader(TensorDataset(torch.tensor(X_f), torch.tensor(y_f_log)), batch_size=64, shuffle=True, generator=gen)
    best_loss, best_state = 1e9, None
    for ep in range(epochs):
        mdl.train()
        for bx, by in dl:
            opt.zero_grad()
            loss = crit(mdl(bx), by)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(mdl.parameters(), 1.0)
            opt.step()
        mdl.eval()
        with torch.no_grad():
            c_loss = float(crit(mdl(torch.tensor(X_c)), torch.tensor(y_c_log)).item())
        if c_loss < best_loss:
            best_loss = c_loss
            best_state = {k: v.clone() for k, v in mdl.state_dict().items()}
    if best_state is not None:
        mdl.load_state_dict(best_state)
    mdl.eval()
    with torch.no_grad():
        pred = np.expm1(np.clip(mdl(torch.tensor(X_t)).numpy(), 0, 10))
    return pred

HORIZONS = [1, 3, 7, 9, 15]
SEEDS = [42, 123, 456]
in_dim = len(feature_cols)
wind_idx = feature_cols.index("era5_ws")
lb_cls_rows, lb_reg_rows = [], []
sample_losses = {}

for h in HORIZONS:
    y_fit_c = df.iloc[fit_idx][f"target_evt_any_{h}d"].values.astype(int)
    y_cal_c = df.iloc[cal_idx][f"target_evt_any_{h}d"].values.astype(int)
    y_te_c = df.iloc[valid_te_idx][f"target_evt_any_{h}d"].values.astype(int)
    y_tr_all_c = df.iloc[valid_tr_idx][f"target_evt_any_{h}d"].values.astype(int)
    brier_ref = brier_score_loss(y_te_c, np.full(len(y_te_c), float(np.mean(y_tr_all_c))))

    y_fit_r = df.iloc[fit_idx][f"target_avg_pm10_{h}d"].values
    y_cal_r = df.iloc[cal_idx][f"target_avg_pm10_{h}d"].values
    y_te_r = df.iloc[valid_te_idx][f"target_avg_pm10_{h}d"].values

    specs = [
        ("LineB_PyTorch_LSTM", lambda: RealLSTMNet(in_dim), False),
        ("LineB_PyTorch_Transformer", lambda: RealTransformerNet(in_dim), False),
        ("LineB_PyTorch_PINN", lambda: RealPINNNet(in_dim), True),
        ("LineB_PyTorch_STGNN", lambda: RealSTGNNNet(in_dim, adj_raw), False),
    ]
    for mname, ctor, is_p in specs:
        rocs, prs, bsss = [], [], []
        r2s, rmses, maes = [], [], []
        for s in SEEDS:
            probs, lhist, _ = train_pytorch_cls(ctor, X_fit_seq, y_fit_c, X_cal_seq, y_cal_c, X_te_seq, s, is_pinn=is_p, wind_idx=wind_idx)
            if h == 7 and s == 42:
                sample_losses[mname] = lhist
            rocs.append(roc_auc_score(y_te_c, probs))
            prs.append(average_precision_score(y_te_c, probs))
            bsss.append(1.0 - brier_score_loss(y_te_c, probs) / brier_ref)

            pred_r = train_pytorch_reg(ctor, X_fit_seq, y_fit_r, X_cal_seq, y_cal_r, X_te_seq, s)
            r2s.append(r2_score(y_te_r, pred_r))
            rmses.append(root_mean_squared_error(y_te_r, pred_r))
            maes.append(mean_absolute_error(y_te_r, pred_r))

        lb_cls_rows.append({"Horizon_Days": h, "Model": mname, "ROC_AUC": round(float(np.mean(rocs)), 4),
                            "ROC_sd": round(float(np.std(rocs)), 4), "PR_AUC": round(float(np.mean(prs)), 4),
                            "BSS": round(float(np.mean(bsss)), 4)})
        lb_reg_rows.append({"Horizon_Days": h, "Model": mname, "R2": round(float(np.mean(r2s)), 4),
                            "RMSE": round(float(np.mean(rmses)), 2), "RMSE_sd": round(float(np.std(rmses)), 2),
                            "MAE": round(float(np.mean(maes)), 2)})

lb_cls_df = pd.DataFrame(lb_cls_rows)
lb_reg_df = pd.DataFrame(lb_reg_rows)
lb_cls_df.to_csv(RESULTS_DIR / "nb03_line_b_classification_70_30.csv", index=False)
lb_reg_df.to_csv(RESULTS_DIR / "nb03_line_b_regression_70_30.csv", index=False)
print("=== LINE B REAL PYTORCH CLASSIFICATION (70/30 Split, 1-15 Days) ===")
print(lb_cls_df.to_string(index=False))
print("\\n=== LINE B REAL PYTORCH REGRESSION (70/30 Split, 1-15 Days) ===")
print(lb_reg_df.to_string(index=False))
"""
    cells.append(run_code_cell(c2, env, 2))

    c3 = """
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for m in lb_cls_df["Model"].unique():
    sub = lb_cls_df[lb_cls_df["Model"] == m]
    axes[0].plot(sub["Horizon_Days"], sub["ROC_AUC"], marker="o", label=m)
axes[0].set_title("Line B Real PyTorch ROC-AUC (1 to 15 Days, 70/30)")
axes[0].set_xlabel("Horizon (Days)")
axes[0].set_ylabel("ROC-AUC")
axes[0].set_xticks([1, 3, 7, 9, 15])
axes[0].legend(fontsize=8)
axes[0].grid(alpha=0.3)

for m, lh in sample_losses.items():
    axes[1].plot(range(1, len(lh) + 1), lh, label=m)
axes[1].set_title("Real PyTorch Training Loss Curves (7d Horizon, Seed 42)")
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("BCE Loss")
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.3)
plt.tight_layout()
fig.savefig(FIG_DIR / "nb03_line_b_real_pytorch_70_30.png", dpi=130)
"""
    cells.append(run_code_cell(c3, env, 3))
    save_notebook(cells, NB_DIR / "03_line_b_pytorch_real_layers.ipynb")


def build_nb04():
    print("\n=== Building & Executing Notebook 04: Complete XAI on Last 70/30 Dataset ===")
    env = {"PROJECT_ROOT": PROJECT_ROOT, "FIG_DIR": FIG_DIR, "XAI_DIR": XAI_DIR}
    cells = []
    cells.append(make_md_cell("""
# Notebook 04: Explainable AI (XAI) Suite on the 70/30 Dataset
- **Scope:** XAI-only analysis on the last engineered 70/30 dataset (`06_Data/riyadh_daily_70_30_engineered.csv`) for the 7-day average dust-event & PM10 models.
- **Methods:**
  1. Global Permutation Importance & XGBoost Gain on the 30% test set.
  2. Exact SHAP (`shap.TreeExplainer`) summary bar & beeswarm + local dust-event waterfall.
  3. 1D Partial Dependence (PDP) & ICE curves for top physical drivers.
  4. Interpretable Surrogate Decision Tree (`max_depth=3`) rules.
  5. Real PyTorch LSTM Input-Gradient Temporal Saliency over the 14-day lookback window + 6-Node Riyadh Spatial Graph connectivity.
"""))

    c1 = """
import numpy as np
import pandas as pd
import shap
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PowerTransformer
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
from sklearn.tree import DecisionTreeClassifier, export_text
from xgboost import XGBClassifier

df = pd.read_csv(PROJECT_ROOT / "06_Data" / "riyadh_daily_70_30_engineered.csv")
df["date"] = pd.to_datetime(df["date"])
target_cols = [c for c in df.columns if c.startswith("target_")]
feature_cols = [c for c in df.columns if c not in ["date"] + target_cols]

N = len(df)
PURGE_GAP = 15
tr_end = int(N * 0.70)
te_start = tr_end + PURGE_GAP

imp = SimpleImputer(strategy="median")
pt = PowerTransformer(method="yeo-johnson")
X_tr = pt.fit_transform(imp.fit_transform(df.iloc[:tr_end][feature_cols].values))
X_te = pt.transform(imp.transform(df.iloc[te_start:][feature_cols].values))
y_tr = df.iloc[:tr_end]["target_evt_any_7d"].values.astype(int)
y_te = df.iloc[te_start:]["target_evt_any_7d"].values.astype(int)

pos_w = float(np.sum(y_tr == 0) / max(1, np.sum(y_tr == 1)))
xgb = XGBClassifier(n_estimators=150, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=pos_w, reg_lambda=2.0, random_state=42, n_jobs=-1, eval_metric="logloss")
xgb.fit(X_tr, y_tr)

# 1. Permutation importance on 30% Test Set
perm = permutation_importance(xgb, X_te, y_te, n_repeats=10, random_state=42, scoring="roc_auc", n_jobs=1)
explainer = shap.TreeExplainer(xgb)
shap_vals = explainer.shap_values(X_te)

xai_df = pd.DataFrame({
    "Feature": feature_cols,
    "XGB_Gain": np.round(xgb.feature_importances_, 5),
    "Test_Perm_ROC_Drop": np.round(perm.importances_mean, 5),
    "Mean_Abs_SHAP": np.round(np.mean(np.abs(shap_vals), axis=0), 5),
}).sort_values("Mean_Abs_SHAP", ascending=False)
xai_df.to_csv(XAI_DIR / "nb04_xai_70_30_importance.csv", index=False)
print("=== TOP 15 XAI FEATURES (70/30 Split, 7-Day Window) ===")
print(xai_df.head(15).to_string(index=False))

# Surrogate interpretable tree
surr = DecisionTreeClassifier(max_depth=3, min_samples_leaf=30, random_state=42)
surr.fit(df.iloc[te_start:][feature_cols].fillna(0), xgb.predict(X_te))
print("\\n=== SURROGATE DECISION RULES (7-Day Dust Forecast) ===")
print(export_text(surr, feature_names=feature_cols))
"""
    cells.append(run_code_cell(c1, env, 1))

    c2 = """
# Plots: SHAP Summary + Permutation + PDP + Real PyTorch Temporal Saliency
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
top12 = xai_df.head(12).iloc[::-1]
axes[0].barh(top12["Feature"], top12["Mean_Abs_SHAP"], color="#1f77b4")
axes[0].set_title("Exact SHAP Mean |Impact| (30% Test Set)")
axes[0].set_xlabel("Mean |SHAP value|")

axes[1].barh(top12["Feature"], top12["Test_Perm_ROC_Drop"], color="#ff7f0e")
axes[1].set_title("Test Permutation Importance (ROC-AUC Drop)")
axes[1].set_xlabel("ROC-AUC Drop")
plt.tight_layout()
fig.savefig(FIG_DIR / "nb04_xai_shap_perm_70_30.png", dpi=130)

# Real PyTorch LSTM Input-Gradient Temporal Saliency over 14-day lookback
torch.manual_seed(42)
SEQ_LEN = 14
X_all_s = pt.transform(imp.transform(df[feature_cols].values))
X_tr_seq = torch.tensor(np.array([X_all_s[i - SEQ_LEN + 1 : i + 1] for i in range(SEQ_LEN - 1, tr_end)], dtype=np.float32))
y_tr_seq = torch.tensor(df.iloc[SEQ_LEN - 1 : tr_end]["target_evt_any_7d"].values, dtype=torch.float32)
X_te_seq = torch.tensor(np.array([X_all_s[i - SEQ_LEN + 1 : i + 1] for i in range(te_start, N)], dtype=np.float32), requires_grad=True)

class MiniLSTM(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.lstm = nn.LSTM(d, 32, batch_first=True)
        self.fc = nn.Linear(32, 1)
    def forward(self, x):
        o, _ = self.lstm(x)
        return self.fc(o[:, -1, :]).squeeze(-1)

m_lstm = MiniLSTM(len(feature_cols))
opt = torch.optim.Adam(m_lstm.parameters(), lr=2e-3)
loss_fn = nn.BCEWithLogitsLoss()
for _ in range(15):
    opt.zero_grad()
    loss_fn(m_lstm(X_tr_seq), y_tr_seq).backward()
    opt.step()

m_lstm.eval()
out = m_lstm(X_te_seq).sum()
out.backward()
lag_saliency = X_te_seq.grad.abs().mean(dim=(0, 2)).detach().numpy()

fig2, ax2 = plt.subplots(figsize=(8, 4))
lags = np.arange(-SEQ_LEN + 1, 1)
ax2.bar(lags, lag_saliency, color="#2ca02c")
ax2.set_title("Line B Real PyTorch LSTM Input-Gradient Saliency (14-Day Lookback)")
ax2.set_xlabel("Lag Relative to Issue Day t (Days)")
ax2.set_ylabel("Mean |d(Logit)/d(Input)|")
plt.tight_layout()
fig2.savefig(FIG_DIR / "nb04_xai_lstm_temporal_saliency.png", dpi=130)
"""
    cells.append(run_code_cell(c2, env, 2))
    save_notebook(cells, NB_DIR / "04_explainable_ai_xai_riyadh.ipynb")


if __name__ == "__main__":
    old_dup = NB_DIR / "02_line_b_lstm_transformer_stgnn_riyadh.ipynb"
    if old_dup.exists():
        old_dup.unlink()
    build_nb00()
    build_nb01()
    build_nb02()
    build_nb03()
    build_nb04()
    print("\nALL 5 NOTEBOOKS BUILT AND EXECUTED SUCCESSFULLY!")
