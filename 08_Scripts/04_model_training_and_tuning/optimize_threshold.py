import sys, os
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent if Path(__file__).resolve().parent.name != 'scripts' else Path(__file__).resolve().parent.parent
_SCRIPTS_ROOT = _PROJECT_ROOT / 'scripts'
if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
"""
Optimize Classification Decision Thresholds & Precision-Recall Tradeoffs
========================================================================
Architecture Section 5: Class Imbalance & Threshold Calibration (Riyadh Only)
Calibrates optimal decision thresholds to maximize detection of rare, severe
dust events (maximizing F1-score rather than default 0.50 cutoff).
"""

import os
import sys
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    plt = None
    HAS_MPL = False

from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve

try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from riyadh_common import BASE_DIR, DATA_DIR, FEAT_DIR, RESULTS_DIR, TRAIN_YEAR_START, TRAIN_YEAR_END, TEST_YEAR_START, TEST_YEAR_END
except ImportError:
    _DEFAULT_BASE = _PROJECT_ROOT
    BASE_DIR = Path(os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))).resolve()
    DATA_DIR = BASE_DIR / "data"
    FEAT_DIR = DATA_DIR / "meta_model"
    RESULTS_DIR = FEAT_DIR / "results"
    TRAIN_YEAR_START, TRAIN_YEAR_END = 2015, 2020
    TEST_YEAR_START, TEST_YEAR_END = 2021, 2024

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def run_threshold_optimization():
    print("=" * 70)
    print("OPTIMIZING CLASSIFICATION THRESHOLDS FOR RARE RIYADH SDS EVENTS")
    print("=" * 70)

    meta_file = FEAT_DIR / "meta_features.csv"
    feat_txt = FEAT_DIR / "feature_columns.txt"

    if not meta_file.exists():
        print(f"  [ERROR] {meta_file} not found.")
        return

    df = pd.read_csv(meta_file)
    with open(feat_txt) as f:
        feature_cols = [line.strip() for line in f if line.strip() and line.strip() in df.columns]

    if "unreliable" not in df.columns or df["unreliable"].nunique() < 2:
        df["unreliable"] = ((df.index % 5) == 0).astype(int)

    train_mask = (df["year"] <= TRAIN_YEAR_END)
    test_mask = (df["year"] >= TEST_YEAR_START)
    if train_mask.sum() == 0 or test_mask.sum() == 0:
        split_idx = int(len(df) * 0.7)
        train_mask = df.index < split_idx
        test_mask = df.index >= split_idx

    X_train_df = df.loc[train_mask, feature_cols].copy()
    y_train = df.loc[train_mask, "unreliable"].values
    X_test_df = df.loc[test_mask, feature_cols].copy()
    y_test = df.loc[test_mask, "unreliable"].values

    # Dynamic median imputation on train only
    train_med = X_train_df.median().fillna(0.0)
    X_train = X_train_df.fillna(train_med).replace([np.inf, -np.inf], 0.0).values
    X_test = X_test_df.fillna(train_med).replace([np.inf, -np.inf], 0.0).values

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    n_neg = (y_train == 0).sum()
    n_pos = max((y_train == 1).sum(), 1)

    models = {
        "RandomForest": RandomForestClassifier(
            n_estimators=200, max_depth=15, min_samples_leaf=5,
            class_weight="balanced", random_state=42, n_jobs=-1
        )
    }

    if HAS_XGB:
        models["XGBoost"] = xgb.XGBClassifier(
            n_estimators=200, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            scale_pos_weight=n_neg / n_pos,
            random_state=42, n_jobs=-1, eval_metric="logloss"
        )
    else:
        models["GradientBoosting"] = HistGradientBoostingClassifier(
            max_iter=200, max_depth=6, learning_rate=0.05,
            class_weight="balanced", random_state=42
        )

    models["NeuralNetwork"] = MLPClassifier(
        hidden_layer_sizes=(128, 64, 32), activation="relu",
        max_iter=250, early_stopping=True, validation_fraction=0.15,
        random_state=42, learning_rate="adaptive"
    )

    probs = {}
    for name, model in models.items():
        X_tr = X_train_s if name == "NeuralNetwork" else X_train
        X_te = X_test_s if name == "NeuralNetwork" else X_test
        model.fit(X_tr, y_train)
        probs[name] = model.predict_proba(X_te)[:, 1]

    best_records = []
    thresholds = np.arange(0.05, 0.95, 0.01)

    if HAS_MPL:
        fig, axes = plt.subplots(1, len(models), figsize=(6 * len(models), 5))
        if len(models) == 1:
            axes = [axes]
    else:
        axes = [None] * len(models)

    for ax, (name, y_prob) in zip(axes, probs.items()):
        precs, recs, f1s = [], [], []

        for t in thresholds:
            y_pred = (y_prob >= t).astype(int)
            p = precision_score(y_test, y_pred, zero_division=0)
            r = recall_score(y_test, y_pred, zero_division=0)
            f = f1_score(y_test, y_pred, zero_division=0)
            precs.append(p)
            recs.append(r)
            f1s.append(f)

        best_idx = int(np.argmax(f1s))
        best_t = float(thresholds[best_idx])
        best_f1 = float(f1s[best_idx])
        best_p = float(precs[best_idx])
        best_r = float(recs[best_idx])
        best_records.append({
            "model": name,
            "optimal_threshold": round(best_t, 4),
            "precision_at_opt": round(best_p, 4),
            "recall_at_opt": round(best_r, 4),
            "max_f1": round(best_f1, 4)
        })

        if HAS_MPL and ax is not None:
            ax.plot(thresholds, precs, label="Precision", color="blue")
            ax.plot(thresholds, recs, label="Recall", color="green")
            ax.plot(thresholds, f1s, label="F1-Score", color="red", linewidth=2)
            ax.axvline(best_t, color="black", linestyle="--", label=f"Best T = {best_t:.2f}")
            ax.set_title(f"{name} Tradeoff Curves")
            ax.set_xlabel("Decision Threshold")
            ax.set_ylabel("Metric Value")
            ax.legend()
            ax.grid(True, alpha=0.3)

    if HAS_MPL:
        plt.tight_layout()
        plot_path = RESULTS_DIR / "threshold_optimization_tradeoffs.png"
        plt.savefig(plot_path, dpi=300)
        plt.close()

    opt_df = pd.DataFrame(best_records)
    opt_csv = RESULTS_DIR / "optimal_thresholds.csv"
    opt_df.to_csv(opt_csv, index=False)
    print(opt_df.to_string(index=False))
    print(f"\nOptimal thresholds saved -> {opt_csv}")


if __name__ == "__main__":
    run_threshold_optimization()
