"""
Part 1: Honest 5-Fold Rolling-Origin CV for Multimodal Reliability Meta-Models
=============================================================================
Implements Fix 1 & Fix 2:
  - Chronological 5-fold TimeSeriesSplit with 72h gap (GAP = 12 steps at 6h stride)
  - Strict leak check: assert train_idx.max() + GAP < test_idx.min()
  - Inner-validation split (with GAP) for Platt calibration & F1 threshold tuning
    (NO tuning on test fold, NO SMOTE before split)
  - Majority-class baseline row + Balanced Accuracy, Macro-F1, PR-AUC, ROC-AUC
    with 7-day Moving Block Bootstrap 95% CIs, Brier, and Pooled BSS.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, average_precision_score, brier_score_loss
)
from xgboost import XGBClassifier

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "06_Data"
RESULTS_DIR = DATA_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
GAP = 12  # 72h at 6h stride

CANDIDATE_FEATURES = [
    "cams_duaod550", "lead_time_hours", "pm10_proxy", "pm25_proxy", "pm_ratio",
    "sin_doy", "cos_doy", "sin_hour", "cos_hour", "modis_aod_lag1",
    "ws10", "i10fg", "blh", "skt", "t2m", "swvl1", "cape", "thermal_gradient",
    "z_850", "u_850", "v_850", "t_850", "r_850",
    "z_700", "u_700", "v_700", "t_700", "r_700",
    "z_500", "u_500", "v_500", "t_500", "r_500"
]


def block_bootstrap_ci(y_true, y_score, metric_fn, block_size=28, n_boot=500, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    n_blocks = max(1, int(np.ceil(n / block_size)))
    starts = np.arange(0, max(1, n - block_size + 1))
    vals = []
    for _ in range(n_boot):
        chosen = rng.choice(starts, size=n_blocks, replace=True)
        idx = np.concatenate([np.arange(s, min(s + block_size, n)) for s in chosen])[:n]
        yt = y_true[idx]
        if len(np.unique(yt)) < 2:
            continue
        vals.append(metric_fn(yt, y_score[idx]))
    if not vals:
        v = float(metric_fn(y_true, y_score))
        return v, v
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def platt_calibrate(val_probs, y_val, test_probs):
    eps = 1e-6
    v_clip = np.clip(val_probs, eps, 1 - eps)
    t_clip = np.clip(test_probs, eps, 1 - eps)
    v_logit = np.log(v_clip / (1 - v_clip)).reshape(-1, 1)
    t_logit = np.log(t_clip / (1 - t_clip)).reshape(-1, 1)
    if len(np.unique(y_val)) < 2:
        return val_probs, test_probs
    lr = LogisticRegression(C=1.0, solver="lbfgs")
    lr.fit(v_logit, y_val)
    return lr.predict_proba(v_logit)[:, 1], lr.predict_proba(t_logit)[:, 1]


def tune_f1_threshold(y_val, val_probs):
    best_t, best_f1 = 0.5, -1.0
    for t in np.linspace(0.02, 0.80, 79):
        f1 = f1_score(y_val, (val_probs >= t).astype(int), zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_t = float(t)
    return best_t


def main():
    df = pd.read_csv(DATA_DIR / "meta_features.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)

    feat_cols = [c for c in CANDIDATE_FEATURES if c in df.columns]
    X_raw_df = df[feat_cols].copy()
    y = df["unreliable"].astype(int).values

    tscv = TimeSeriesSplit(n_splits=5, gap=GAP)
    model_names = ["RandomForest", "XGBoost", "HistGradientBoosting", "NeuralNetwork"]
    oof_y = []
    oof_probs = {m: [] for m in model_names}
    oof_preds = {m: [] for m in model_names}

    for fold, (tr_idx, te_idx) in enumerate(tscv.split(X_raw_df), start=1):
        assert tr_idx.max() + GAP < te_idx.min(), f"Leakage detected on fold {fold}!"

        # Inner validation split strictly before test fold, with GAP
        cut = int(0.80 * len(tr_idx))
        inner_tr = tr_idx[: max(1, cut - GAP)]
        inner_va = tr_idx[cut:]
        assert inner_tr.max() + GAP < inner_va.min(), f"Inner leakage on fold {fold}!"

        med = X_raw_df.iloc[inner_tr].median().fillna(0.0)
        X_itr = X_raw_df.iloc[inner_tr].fillna(med).replace([np.inf, -np.inf], 0.0).values
        X_iva = X_raw_df.iloc[inner_va].fillna(med).replace([np.inf, -np.inf], 0.0).values
        X_te = X_raw_df.iloc[te_idx].fillna(med).replace([np.inf, -np.inf], 0.0).values

        y_itr, y_iva, y_te = y[inner_tr], y[inner_va], y[te_idx]

        pt = PowerTransformer(method="yeo-johnson", standardize=True)
        X_itr_pt = pt.fit_transform(X_itr)
        X_iva_pt = pt.transform(X_iva)
        X_te_pt = pt.transform(X_te)

        sc = StandardScaler()
        X_itr_sc = sc.fit_transform(X_itr_pt)
        X_iva_sc = sc.transform(X_iva_pt)
        X_te_sc = sc.transform(X_te_pt)

        models = {
            "RandomForest": RandomForestClassifier(
                n_estimators=250, max_depth=8, min_samples_leaf=12,
                max_features=0.30, random_state=SEED, n_jobs=-1
            ),
            "XGBoost": XGBClassifier(
                n_estimators=220, max_depth=4, learning_rate=0.04,
                subsample=0.80, colsample_bytree=0.40, reg_lambda=8.0,
                random_state=SEED, n_jobs=-1, eval_metric="logloss"
            ),
            "HistGradientBoosting": HistGradientBoostingClassifier(
                max_iter=200, max_depth=5, learning_rate=0.04,
                max_features=0.35, l2_regularization=8.0, random_state=SEED
            ),
            "NeuralNetwork": MLPClassifier(
                hidden_layer_sizes=(64, 32), activation="relu", alpha=0.05,
                max_iter=200, early_stopping=True, validation_fraction=0.15,
                random_state=SEED
            ),
        }

        oof_y.append(y_te)
        for mname, clf in models.items():
            x_tr_use = X_itr_sc if mname == "NeuralNetwork" else X_itr_pt
            x_va_use = X_iva_sc if mname == "NeuralNetwork" else X_iva_pt
            x_te_use = X_te_sc if mname == "NeuralNetwork" else X_te_pt

            clf.fit(x_tr_use, y_itr)
            va_raw = clf.predict_proba(x_va_use)[:, 1]
            te_raw = clf.predict_proba(x_te_use)[:, 1]

            va_cal, te_cal = platt_calibrate(va_raw, y_iva, te_raw)
            thr = tune_f1_threshold(y_iva, va_cal)

            oof_probs[mname].append(te_cal)
            oof_preds[mname].append((te_cal >= thr).astype(int))

    oy = np.concatenate(oof_y)
    brier_ref = brier_score_loss(oy, np.full_like(oy, oy.mean(), dtype=float))
    maj_class = int(pd.Series(oy).value_counts().idxmax())
    maj_pred = np.full_like(oy, maj_class)
    maj_prob = np.full_like(oy, oy.mean(), dtype=float)

    rows = [{
        "Model": f"Majority_Class_Baseline (Always {maj_class})",
        "N_Eval": int(len(oy)),
        "Positives": int(oy.sum()),
        "Accuracy": round(float(accuracy_score(oy, maj_pred)), 4),
        "Balanced_Acc": round(float(balanced_accuracy_score(oy, maj_pred)), 4),
        "Precision": 0.0,
        "Recall": 0.0,
        "F1": 0.0,
        "Macro_F1": round(float(f1_score(oy, maj_pred, average="macro", zero_division=0)), 4),
        "ROC_AUC": 0.5000,
        "ROC_95CI": "[0.500,0.500]",
        "PR_AUC": round(float(oy.mean()), 4),
        "PR_95CI": f"[{oy.mean():.3f},{oy.mean():.3f}]",
        "Brier": round(float(brier_ref), 4),
        "BSS": 0.0000,
    }]

    for mname in model_names:
        op = np.concatenate(oof_probs[mname])
        oh = np.concatenate(oof_preds[mname])
        roc_ci = block_bootstrap_ci(oy, op, roc_auc_score)
        pr_ci = block_bootstrap_ci(oy, op, average_precision_score)
        b_m = brier_score_loss(oy, op)
        rows.append({
            "Model": mname,
            "N_Eval": int(len(oy)),
            "Positives": int(oy.sum()),
            "Accuracy": round(float(accuracy_score(oy, oh)), 4),
            "Balanced_Acc": round(float(balanced_accuracy_score(oy, oh)), 4),
            "Precision": round(float(precision_score(oy, oh, zero_division=0)), 4),
            "Recall": round(float(recall_score(oy, oh, zero_division=0)), 4),
            "F1": round(float(f1_score(oy, oh, zero_division=0)), 4),
            "Macro_F1": round(float(f1_score(oy, oh, average="macro", zero_division=0)), 4),
            "ROC_AUC": round(float(roc_auc_score(oy, op)), 4),
            "ROC_95CI": f"[{roc_ci[0]:.3f},{roc_ci[1]:.3f}]",
            "PR_AUC": round(float(average_precision_score(oy, op)), 4),
            "PR_95CI": f"[{pr_ci[0]:.3f},{pr_ci[1]:.3f}]",
            "Brier": round(float(b_m), 4),
            "BSS": round(float(1.0 - b_m / max(brier_ref, 1e-9)), 4),
        })

    out_df = pd.DataFrame(rows)
    out_path = RESULTS_DIR / "meta_model_rolling_cv_metrics.csv"
    out_df.to_csv(out_path, index=False)
    print("\n=== PART 1 META-MODEL HONEST 5-FOLD ROLLING-ORIGIN CV (INNER-VAL TUNED) ===")
    print(out_df.to_string(index=False))
    print(f"\nSaved -> {out_path}")


if __name__ == "__main__":
    main()

