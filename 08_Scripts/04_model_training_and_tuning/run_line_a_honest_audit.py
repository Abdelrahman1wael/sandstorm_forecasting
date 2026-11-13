"""
Line A Honest Audit: Baselines, True R2, High-PM10 Error, Interval Widths,
Balanced Accuracy, Macro-F1 & Per-Class Recall (Fixes 2, 3, 4)
===========================================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score, recall_score,
    mean_squared_error, mean_absolute_error, r2_score
)
from xgboost import XGBRegressor, XGBClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "06_Data"
RESULTS_DIR = DATA_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
GAP_HOURS = 72


def main():
    df = pd.read_csv(DATA_DIR / "riyadh_line_a_tabular_features.csv")
    time_col = "time" if "time" in df.columns else "timestamp"
    df[time_col] = pd.to_datetime(df[time_col], utc=True)
    df = df.sort_values(time_col).reset_index(drop=True)
    df["year"] = df[time_col].dt.year

    pm10_col = "pm10_calibrated_ugm3" if "pm10_calibrated_ugm3" in df.columns else "pm10_ugm3"
    nwp_col = "nwp_cams_pm10"
    t24_col = "target_pm10_24h"
    df["delta_pm10_bias"] = df[pm10_col] - df[nwp_col]
    df["target_hazard_24h"] = pd.cut(
        df[t24_col],
        bins=[-np.inf, 50.0, 150.0, 500.0, 1500.0, np.inf],
        labels=[0, 1, 2, 3, 4]
    ).astype(int)

    exclude = {
        "time", "timestamp", "valid", "station", "station_id", "station_name", "role",
        "wxcodes", "hazard_level", "year", "delta_pm10_bias", "target_residual_pm10",
        "target_pm10_24h", "target_event_24h", "target_pm10_72h", "target_event_72h",
        "target_pm10_120h", "target_event_120h", "target_pm10_168h", "target_event_168h",
        "target_hazard_24h", pm10_col
    }
    feat_cols = [c for c in df.columns if c not in exclude and pd.api.types.is_numeric_dtype(df[c])]

    train_idx = np.where(df["year"] <= 2022)[0]
    test_idx = np.where(df["year"] >= 2023)[0]
    # Enforce 72h chronological gap before test
    train_idx = train_idx[train_idx < test_idx.min() - GAP_HOURS]
    assert train_idx.max() + GAP_HOURS < test_idx.min(), "Leakage: gap violated!"

    X_tr_df = df.iloc[train_idx][feat_cols]
    X_te_df = df.iloc[test_idx][feat_cols]
    med = X_tr_df.median().fillna(0.0)
    X_tr = X_tr_df.fillna(med).replace([np.inf, -np.inf], 0.0).values
    X_te = X_te_df.fillna(med).replace([np.inf, -np.inf], 0.0).values

    # =========================================================================
    # FIX 4: Line A1 — NWP Bias Correction vs Raw CAMS + High-PM10 Hours
    # =========================================================================
    y_bias_tr = df.iloc[train_idx]["delta_pm10_bias"].values
    nwp_te = df.iloc[test_idx][nwp_col].values
    obs_te = df.iloc[test_idx][pm10_col].values
    high_mask = obs_te >= 150.0

    raw_rmse = float(np.sqrt(mean_squared_error(obs_te, nwp_te)))
    raw_mae = float(mean_absolute_error(obs_te, nwp_te))
    raw_r2 = float(r2_score(obs_te, nwp_te))
    raw_high_rmse = float(np.sqrt(mean_squared_error(obs_te[high_mask], nwp_te[high_mask])))
    raw_high_mae = float(mean_absolute_error(obs_te[high_mask], nwp_te[high_mask]))

    a1_rows = [{
        "Model": "Raw_CAMS_Baseline",
        "RMSE": round(raw_rmse, 2),
        "MAE": round(raw_mae, 2),
        "R2": round(raw_r2, 4),
        "RMSE_Red_vs_Raw_CAMS_Pct": 0.0,
        "N_High_PM10": int(high_mask.sum()),
        "High_PM10_RMSE": round(raw_high_rmse, 2),
        "High_PM10_MAE": round(raw_high_mae, 2),
        "High_RMSE_Red_vs_Raw_CAMS_Pct": 0.0,
    }]

    a1_models = {
        "LineA1_HistGB_NWP_Bias_Correction": HistGradientBoostingRegressor(
            max_iter=200, max_depth=6, learning_rate=0.04, max_features=0.35, l2_regularization=4.0, random_state=SEED
        ),
        "LineA1_XGBoost_NWP_Bias_Correction": XGBRegressor(
            n_estimators=220, max_depth=6, learning_rate=0.04, subsample=0.80,
            colsample_bytree=0.45, reg_lambda=6.0, random_state=SEED, n_jobs=-1, tree_method="hist"
        ),
    }
    for name, reg in a1_models.items():
        reg.fit(X_tr, y_bias_tr)
        corr = np.clip(nwp_te + reg.predict(X_te), 0.0, 2500.0)
        rmse = float(np.sqrt(mean_squared_error(obs_te, corr)))
        mae = float(mean_absolute_error(obs_te, corr))
        r2 = float(r2_score(obs_te, corr))
        red = 100.0 * (raw_rmse - rmse) / max(raw_rmse, 1e-6)
        h_rmse = float(np.sqrt(mean_squared_error(obs_te[high_mask], corr[high_mask])))
        h_mae = float(mean_absolute_error(obs_te[high_mask], corr[high_mask]))
        h_red = 100.0 * (raw_high_rmse - h_rmse) / max(raw_high_rmse, 1e-6)
        a1_rows.append({
            "Model": name,
            "RMSE": round(rmse, 2),
            "MAE": round(mae, 2),
            "R2": round(r2, 4),
            "RMSE_Red_vs_Raw_CAMS_Pct": round(red, 2),
            "N_High_PM10": int(high_mask.sum()),
            "High_PM10_RMSE": round(h_rmse, 2),
            "High_PM10_MAE": round(h_mae, 2),
            "High_RMSE_Red_vs_Raw_CAMS_Pct": round(h_red, 2),
        })

    df_a1 = pd.DataFrame(a1_rows)
    df_a1.to_csv(RESULTS_DIR / "line_a1_honest_audit.csv", index=False)

    # =========================================================================
    # FIX 3: Line A2 — T+24h vs Trivial Train Median + Interval Width & Storm Coverage
    # =========================================================================
    y_t24_tr = df.iloc[train_idx][t24_col].values
    y_t24_te = df.iloc[test_idx][t24_col].values
    storm_te = y_t24_te >= 150.0

    tr_median = float(np.median(y_t24_tr))
    med_pred = np.full_like(y_t24_te, tr_median)

    q_preds = {}
    for q in [0.10, 0.50, 0.90]:
        qm = HistGradientBoostingRegressor(
            loss="quantile", quantile=q, max_iter=150, max_depth=6, learning_rate=0.05, max_features=0.35, random_state=SEED
        )
        qm.fit(X_tr, y_t24_tr)
        q_preds[q] = np.clip(qm.predict(X_te), 0.0, None)

    xgb_t24 = XGBRegressor(
        n_estimators=200, max_depth=6, learning_rate=0.04, subsample=0.80,
        colsample_bytree=0.45, reg_lambda=6.0, random_state=SEED, n_jobs=-1, tree_method="hist"
    ).fit(X_tr, y_t24_tr)
    xgb_t24_pred = np.clip(xgb_t24.predict(X_te), 0.0, None)

    width_all = float(np.mean(q_preds[0.90] - q_preds[0.10]))
    picp_all = float(np.mean((y_t24_te >= q_preds[0.10]) & (y_t24_te <= q_preds[0.90]))) * 100.0
    width_storm = float(np.mean(q_preds[0.90][storm_te] - q_preds[0.10][storm_te]))
    picp_storm = float(np.mean((y_t24_te[storm_te] >= q_preds[0.10][storm_te]) & (y_t24_te[storm_te] <= q_preds[0.90][storm_te]))) * 100.0

    a2_rows = [
        {
            "Model": f"Trivial_Train_Median ({tr_median:.1f})",
            "RMSE": round(float(np.sqrt(mean_squared_error(y_t24_te, med_pred))), 2),
            "MAE": round(float(mean_absolute_error(y_t24_te, med_pred)), 2),
            "R2": round(float(r2_score(y_t24_te, med_pred)), 4),
            "Mean_Width_80": np.nan,
            "PICP80_Pct": np.nan,
            "N_Storm_Hours": int(storm_te.sum()),
            "Storm_RMSE": round(float(np.sqrt(mean_squared_error(y_t24_te[storm_te], med_pred[storm_te]))), 2),
            "Storm_MAE": round(float(mean_absolute_error(y_t24_te[storm_te], med_pred[storm_te])), 2),
            "Storm_Width_80": np.nan,
            "Storm_PICP80_Pct": np.nan,
        },
        {
            "Model": "LineA2_HistGB_T+24h_Quantile_P50",
            "RMSE": round(float(np.sqrt(mean_squared_error(y_t24_te, q_preds[0.50]))), 2),
            "MAE": round(float(mean_absolute_error(y_t24_te, q_preds[0.50])), 2),
            "R2": round(float(r2_score(y_t24_te, q_preds[0.50])), 4),
            "Mean_Width_80": round(width_all, 2),
            "PICP80_Pct": round(picp_all, 1),
            "N_Storm_Hours": int(storm_te.sum()),
            "Storm_RMSE": round(float(np.sqrt(mean_squared_error(y_t24_te[storm_te], q_preds[0.50][storm_te]))), 2),
            "Storm_MAE": round(float(mean_absolute_error(y_t24_te[storm_te], q_preds[0.50][storm_te])), 2),
            "Storm_Width_80": round(width_storm, 2),
            "Storm_PICP80_Pct": round(picp_storm, 1),
        },
        {
            "Model": "LineA2_XGBoost_T+24h_Forecaster",
            "RMSE": round(float(np.sqrt(mean_squared_error(y_t24_te, xgb_t24_pred))), 2),
            "MAE": round(float(mean_absolute_error(y_t24_te, xgb_t24_pred)), 2),
            "R2": round(float(r2_score(y_t24_te, xgb_t24_pred)), 4),
            "Mean_Width_80": np.nan,
            "PICP80_Pct": np.nan,
            "N_Storm_Hours": int(storm_te.sum()),
            "Storm_RMSE": round(float(np.sqrt(mean_squared_error(y_t24_te[storm_te], xgb_t24_pred[storm_te]))), 2),
            "Storm_MAE": round(float(mean_absolute_error(y_t24_te[storm_te], xgb_t24_pred[storm_te])), 2),
            "Storm_Width_80": np.nan,
            "Storm_PICP80_Pct": np.nan,
        },
    ]
    df_a2 = pd.DataFrame(a2_rows)
    df_a2.to_csv(RESULTS_DIR / "line_a2_honest_audit.csv", index=False)

    # =========================================================================
    # FIX 2: Line A3 — 5-Tier Hazard Classifier vs Majority Baseline + Macro-F1, BalAcc, Per-Class Recall
    # =========================================================================
    le = LabelEncoder()
    y_haz_tr = le.fit_transform(df.iloc[train_idx]["target_hazard_24h"].values)
    y_haz_te = le.transform(df.iloc[test_idx]["target_hazard_24h"].values)
    classes = list(le.classes_)

    maj_cls = int(pd.Series(y_haz_te).value_counts().idxmax())
    maj_pred_haz = np.full_like(y_haz_te, maj_cls)

    haz_hgb = HistGradientBoostingClassifier(
        max_iter=200, max_depth=8, learning_rate=0.05, max_features=0.35, class_weight="balanced", random_state=SEED
    ).fit(X_tr, y_haz_tr)
    haz_xgb = XGBClassifier(
        n_estimators=200, max_depth=6, learning_rate=0.05, subsample=0.80,
        colsample_bytree=0.45, reg_lambda=5.0, random_state=SEED, n_jobs=-1, tree_method="hist", eval_metric="mlogloss"
    ).fit(X_tr, y_haz_tr)

    a3_rows = []
    for name, pred in [
        (f"Majority_Class_Baseline (Always Tier {classes[maj_cls]})", maj_pred_haz),
        ("LineA3_HistGB_5Tier_Hazard", haz_hgb.predict(X_te)),
        ("LineA3_XGBoost_5Tier_Hazard", haz_xgb.predict(X_te)),
    ]:
        rec_per = recall_score(y_haz_te, pred, labels=list(range(len(classes))), average=None, zero_division=0)
        row = {
            "Model": name,
            "Accuracy": round(float(accuracy_score(y_haz_te, pred)), 4),
            "Balanced_Accuracy": round(float(balanced_accuracy_score(y_haz_te, pred)), 4),
            "Macro_F1": round(float(f1_score(y_haz_te, pred, average="macro", zero_division=0)), 4),
            "Weighted_F1": round(float(f1_score(y_haz_te, pred, average="weighted", zero_division=0)), 4),
        }
        for idx_c, cls_id in enumerate(classes):
            cnt = int((y_haz_te == idx_c).sum())
            row[f"Recall_Tier{cls_id} (n={cnt})"] = round(float(rec_per[idx_c]), 4)
        a3_rows.append(row)

    df_a3 = pd.DataFrame(a3_rows)
    df_a3.to_csv(RESULTS_DIR / "line_a3_honest_audit.csv", index=False)

    print("=== LINE A1 HONEST AUDIT ===")
    print(df_a1.to_string(index=False))
    print("\n=== LINE A2 HONEST AUDIT ===")
    print(df_a2.to_string(index=False))
    print("\n=== LINE A3 HONEST AUDIT ===")
    print(df_a3.to_string(index=False))


if __name__ == "__main__":
    main()

