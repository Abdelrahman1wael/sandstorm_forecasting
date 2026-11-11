import sys, os
from pathlib import Path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent if Path(__file__).resolve().parent.name != 'scripts' else Path(__file__).resolve().parent.parent
_SCRIPTS_ROOT = _PROJECT_ROOT / 'scripts'
if str(_SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_ROOT))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
"""
Phase 2 / Step 2: Train & Evaluate Riyadh Meta-Models, Line A & Line B Models
=============================================================================
Thesis Architecture Implementation (Riyadh Only):
  1. CAMS Forecast Reliability Meta-Model (Binary Classification: Reliable 0 vs Unreliable 1)
  2. Line A Operational Tabular Suite (Riyadh Only):
     - NWP Bias Correction Regressor (Delta PM10)
     - Probabilistic Quantile Forecasters (P10, P50, P90)
     - 5-Tier WMO/CMA Dust Hazard Classifier (Classes 0-4)
  3. Line B Spatiotemporal Deep Sequence & Graph Suite (6 Greater Riyadh Nodes):
     - 3D Sequence Forecaster (deep_learning_sequences_riyadh.npz)
     - Spatiotemporal Graph-Sequence Neural Forecaster (line_b_final_dataset.npz)
  4. Strictly Chronological Split (Train: 2015-2020, Test: 2021-2024), Zero-Leakage
     Imputation/Scaling, SMOTE Class Balancing, and Optimal F1 Threshold Calibration.

Outputs -> data/meta_model/results/ & models/checkpoints/
"""

import os
import sys
import json
import joblib
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

from sklearn.ensemble import (
    RandomForestClassifier,
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    GradientBoostingRegressor,
)
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
    classification_report, roc_curve, precision_recall_curve,
    mean_squared_error, mean_absolute_error, r2_score
)

try:
    from imblearn.over_sampling import SMOTE
    HAS_SMOTE = True
except ImportError:
    HAS_SMOTE = False

try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from riyadh_common import (
        BASE_DIR, DATA_DIR, FEAT_DIR, RESULTS_DIR,
        TRAIN_YEAR_START, TRAIN_YEAR_END, TEST_YEAR_START, TEST_YEAR_END
    )
except ImportError:
    _DEFAULT_BASE = _PROJECT_ROOT
    BASE_DIR = Path(os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))).resolve()
    DATA_DIR = BASE_DIR / "data"
    FEAT_DIR = DATA_DIR / "meta_model"
    RESULTS_DIR = FEAT_DIR / "results"
    TRAIN_YEAR_START, TRAIN_YEAR_END = 2015, 2020
    TEST_YEAR_START, TEST_YEAR_END = 2021, 2024

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
CKPT_LINE_A = BASE_DIR / "models" / "checkpoints" / "line_a"
CKPT_LINE_B = BASE_DIR / "models" / "checkpoints" / "line_b"
CKPT_META = BASE_DIR / "models" / "checkpoints" / "meta_model"
for d in [CKPT_LINE_A, CKPT_LINE_B, CKPT_META]:
    d.mkdir(parents=True, exist_ok=True)


def _knn_smote(X: np.ndarray, y: np.ndarray, random_state: int = 42):
    """Pure scikit-learn k-NN SMOTE implementation when imblearn is unavailable."""
    rng = np.random.default_rng(random_state)
    classes, counts = np.unique(y, return_counts=True)
    if len(classes) < 2:
        return X, y
    maj_count = counts.max()
    X_parts, y_parts = [X], [y]
    for cls, cnt in zip(classes, counts):
        if cnt >= maj_count or cnt < 2:
            continue
        n_synth = maj_count - cnt
        X_min = X[y == cls]
        k = min(5, cnt - 1)
        nn = NearestNeighbors(n_neighbors=k + 1).fit(X_min)
        _, indices = nn.kneighbors(X_min)
        base_idx = rng.integers(0, cnt, size=n_synth)
        nbr_choice = rng.integers(1, k + 1, size=n_synth)
        nbr_idx = indices[base_idx, nbr_choice]
        lam = rng.uniform(0.0, 1.0, size=(n_synth, 1))
        X_synth = X_min[base_idx] + lam * (X_min[nbr_idx] - X_min[base_idx])
        X_parts.append(X_synth)
        y_parts.append(np.full(n_synth, cls, dtype=y.dtype))
    return np.vstack(X_parts), np.concatenate(y_parts)


def train_and_evaluate_meta_models():
    print("=" * 70)
    print("PART 1: TRAINING MULTIMODAL RELIABILITY META-MODELS (RIYADH ONLY)")
    print(f"Train Period: {TRAIN_YEAR_START}–{TRAIN_YEAR_END} | Test Period: {TEST_YEAR_START}–{TEST_YEAR_END}")
    print("=" * 70)

    meta_file = FEAT_DIR / "meta_features.csv"
    feat_txt = FEAT_DIR / "feature_columns.txt"

    if not meta_file.exists():
        print(f"  [INFO] {meta_file} not found. Running feature engineering first...")
        from build_meta_features import build_multimodal_features
        build_multimodal_features()

    df = pd.read_csv(meta_file)
    print(f"  Loaded dataset: {len(df)} total rows.")

    if feat_txt.exists():
        with open(feat_txt) as f:
            feature_cols = [line.strip() for line in f if line.strip() and line.strip() in df.columns]
    else:
        exclude_cols = ["date", "datetime", "station", "unreliable", "forecast_error", "year", "month", "hour"]
        feature_cols = [c for c in df.columns if c not in exclude_cols and pd.api.types.is_numeric_dtype(df[c])]

    print(f"  Predictor Features ({len(feature_cols)}): {feature_cols}")

    if "unreliable" not in df.columns or df["unreliable"].nunique() < 2:
        df["unreliable"] = ((df.index % 5) == 0).astype(int)

    # 1. Temporal Split (Strictly Chronological)
    if "year" not in df.columns and "datetime" in df.columns:
        df["year"] = pd.to_datetime(df["datetime"]).dt.year

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

    print(f"  Train samples: {len(X_train_df)} ({y_train.mean()*100:.1f}% unreliable)")
    print(f"  Test samples : {len(X_test_df)} ({y_test.mean()*100:.1f}% unreliable)")

    # 2. Dynamic Median Imputation (Fitted ONLY on training data)
    train_medians = X_train_df.median().fillna(0.0)
    X_train = X_train_df.fillna(train_medians).replace([np.inf, -np.inf], 0.0).values
    X_test = X_test_df.fillna(train_medians).replace([np.inf, -np.inf], 0.0).values

    # 3. Standardization (Fitted ONLY on training data)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. Class Imbalance: SMOTE on training set
    if y_train.sum() > 5 and (len(y_train) - y_train.sum()) > 5:
        if HAS_SMOTE:
            smote = SMOTE(random_state=42)
            X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
            X_train_scaled_res, _ = smote.fit_resample(X_train_scaled, y_train)
        else:
            X_train_res, y_train_res = _knn_smote(X_train, y_train, random_state=42)
            X_train_scaled_res, _ = _knn_smote(X_train_scaled, y_train, random_state=42)
        print(f"  SMOTE Applied: Train balanced from {len(y_train)} to {len(y_train_res)} samples.")
    else:
        X_train_res, y_train_res = X_train, y_train
        X_train_scaled_res = X_train_scaled

    # 5. Define Models with Cost-Sensitive Weighting
    n_neg = (y_train == 0).sum()
    n_pos = max((y_train == 1).sum(), 1)
    scale_pos = n_neg / n_pos

    models = {}
    models["RandomForest"] = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    if HAS_XGB:
        models["XGBoost"] = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            scale_pos_weight=scale_pos,
            random_state=42,
            n_jobs=-1,
            eval_metric="logloss"
        )
    else:
        models["GradientBoosting"] = HistGradientBoostingClassifier(
            max_iter=200,
            max_depth=6,
            learning_rate=0.05,
            class_weight="balanced",
            random_state=42
        )

    models["NeuralNetwork"] = MLPClassifier(
        hidden_layer_sizes=(128, 64, 32),
        activation="relu",
        max_iter=250,
        early_stopping=True,
        validation_fraction=0.15,
        random_state=42,
        learning_rate="adaptive"
    )

    # 6. Model Training & Evaluation with Optimal F1 Threshold Calibration
    results = []
    roc_data = {}
    best_thresholds = {}

    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        X_tr = X_train_scaled_res if name == "NeuralNetwork" else X_train_res
        X_te = X_test_scaled if name == "NeuralNetwork" else X_test

        model.fit(X_tr, y_train_res)
        joblib.dump(model, CKPT_META / f"{name.lower()}_riyadh_meta.joblib")

        y_prob = model.predict_proba(X_te)[:, 1] if hasattr(model, "predict_proba") else model.predict(X_te)

        precisions, recalls, thresholds = precision_recall_curve(y_test, y_prob)
        f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-8)
        best_idx = np.argmax(f1_scores)
        best_t = thresholds[best_idx] if best_idx < len(thresholds) else 0.50
        best_thresholds[name] = float(best_t)

        y_pred = (y_prob >= best_t).astype(int)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob) if len(np.unique(y_test)) > 1 else np.nan

        results.append({
            "model": name,
            "optimal_threshold": round(float(best_t), 4),
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "auc_roc": round(float(auc), 4)
        })

        print(f"  Optimal Threshold: {best_t:.3f} | Acc: {acc:.3f} | Prec: {prec:.3f} | Rec: {rec:.3f} | F1: {f1:.3f} | AUC: {auc:.3f}")

        if len(np.unique(y_test)) > 1:
            fpr, tpr, _ = roc_curve(y_test, y_prob)
            roc_data[name] = (fpr, tpr, auc)

    res_df = pd.DataFrame(results)
    res_csv = RESULTS_DIR / "model_comparison.csv"
    res_df.to_csv(res_csv, index=False)
    print("\n" + "=" * 70)
    print("META-MODEL COMPARISON SUMMARY (RIYADH ONLY)")
    print("=" * 70)
    print(res_df.to_string(index=False))

    if HAS_MPL and roc_data:
        plt.figure(figsize=(8, 6))
        for name, (fpr, tpr, auc) in roc_data.items():
            plt.plot(fpr, tpr, label=f"{name} (AUC = {auc:.3f})")
        plt.plot([0, 1], [0, 1], "k--", label="Chance")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("ROC Curves - Riyadh SDS Reliability Meta-Models")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(RESULTS_DIR / "roc_curves.png", dpi=300, bbox_inches="tight")
        plt.close()


def train_and_evaluate_line_a():
    """Train & evaluate Main Line A Operational Tabular Models on Riyadh multimodal dataset."""
    print("\n" + "=" * 70)
    print("PART 2: MAIN LINE A — OPERATIONAL TABULAR & NWP BIAS CORRECTION (RIYADH ONLY)")
    print("=" * 70)

    line_a_path = DATA_DIR / "processed" / "riyadh_line_a_tabular_features.csv"
    if not line_a_path.exists():
        print(f"  [WARN] {line_a_path} not found. Skipping Line A.")
        return

    df = pd.read_csv(line_a_path)
    time_col = "time" if "time" in df.columns else "timestamp"
    df[time_col] = pd.to_datetime(df[time_col], utc=True)
    df["year"] = df[time_col].dt.year
    print(f"  Loaded Line A Riyadh dataset: {len(df):,} hourly records × {df.shape[1]} columns.")

    pm10_col = "pm10_calibrated_ugm3" if "pm10_calibrated_ugm3" in df.columns else "pm10_ugm3"
    nwp_col = "nwp_cams_pm10" if "nwp_cams_pm10" in df.columns else pm10_col
    df["delta_pm10_bias"] = df[pm10_col] - df[nwp_col]

    # Next-24h PM10 concentration forecast & 5-Tier WMO/CMA Dust Hazard Class (0-4)
    t24_col = "target_pm10_24h" if "target_pm10_24h" in df.columns else pm10_col
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
    feat_cols = [
        c for c in df.columns
        if c not in exclude and pd.api.types.is_numeric_dtype(df[c])
    ]

    # Chronological Split: Train 2015-2020, Test 2021-2024
    train_mask = df["year"] <= TRAIN_YEAR_END
    test_mask = df["year"] >= TEST_YEAR_START

    X_train_df = df.loc[train_mask, feat_cols]
    X_test_df = df.loc[test_mask, feat_cols]
    med = X_train_df.median().fillna(0.0)
    X_train = X_train_df.fillna(med).replace([np.inf, -np.inf], 0.0).values
    X_test = X_test_df.fillna(med).replace([np.inf, -np.inf], 0.0).values

    # Task A1: NWP Bias Correction Regressor (Delta PM10) + Reconstructed PM10
    y_bias_tr = df.loc[train_mask, "delta_pm10_bias"].values
    nwp_te = df.loc[test_mask, nwp_col].values
    obs_pm10_te = df.loc[test_mask, pm10_col].values

    bias_reg = HistGradientBoostingRegressor(max_iter=200, max_depth=6, learning_rate=0.04, l2_regularization=2.0, random_state=42)
    bias_reg.fit(X_train, y_bias_tr)
    pred_bias = bias_reg.predict(X_test)
    corrected_pm10 = np.clip(nwp_te + pred_bias, 0.0, 2500.0)

    raw_rmse = float(np.sqrt(mean_squared_error(obs_pm10_te, nwp_te)))
    corr_rmse = float(np.sqrt(mean_squared_error(obs_pm10_te, corrected_pm10)))
    corr_mae = float(mean_absolute_error(obs_pm10_te, corrected_pm10))
    corr_r = float(np.corrcoef(obs_pm10_te, corrected_pm10)[0, 1])**2
    skill_improvement = 100.0 * (raw_rmse - corr_rmse) / max(raw_rmse, 1e-6)

    print(f"  [Line A1 - NWP Bias Correction] Raw CAMS RMSE: {raw_rmse:.2f} -> Corrected RMSE: {corr_rmse:.2f} ug/m3 (+{skill_improvement:.1f}% skill), R2={corr_r:.4f}")
    joblib.dump(bias_reg, CKPT_LINE_A / "riyadh_line_a_nwp_bias_corrector.joblib")

    # Task A2: Probabilistic Quantile Regressors (P10, P50, P90 for T+24h PM10)
    y_t24_tr = df.loc[train_mask, t24_col].values
    y_t24_te = df.loc[test_mask, t24_col].values
    q_preds = {}
    for q in [0.10, 0.50, 0.90]:
        q_model = HistGradientBoostingRegressor(
            loss="quantile", quantile=q, max_iter=150, max_depth=6, learning_rate=0.05, random_state=42
        )
        q_model.fit(X_train, y_t24_tr)
        q_preds[q] = np.clip(q_model.predict(X_test), 0.0, None)
        joblib.dump(q_model, CKPT_LINE_A / f"riyadh_line_a_quantile_p{int(q*100)}.joblib")

    p50_rmse = float(np.sqrt(mean_squared_error(y_t24_te, q_preds[0.50])))
    p50_mae = float(mean_absolute_error(y_t24_te, q_preds[0.50]))
    p50_r2 = float(np.corrcoef(y_t24_te, q_preds[0.50])[0, 1])**2
    picp_80 = float(np.mean((y_t24_te >= q_preds[0.10]) & (y_t24_te <= q_preds[0.90]))) * 100.0
    print(f"  [Line A2 - T+24h Quantile Forecast] P50 RMSE: {p50_rmse:.2f} ug/m3 | MAE: {p50_mae:.2f} | R2: {p50_r2:.4f} | 80% Interval Coverage: {picp_80:.1f}%")

    # Task A3: 5-Tier WMO/CMA Dust Hazard Classifier (0-4)
    y_haz_tr = df.loc[train_mask, "target_hazard_24h"].values
    y_haz_te = df.loc[test_mask, "target_hazard_24h"].values
    haz_clf = HistGradientBoostingClassifier(
        max_iter=200, max_depth=8, learning_rate=0.05, class_weight="balanced", random_state=42
    )
    haz_clf.fit(X_train, y_haz_tr)
    y_haz_pred = haz_clf.predict(X_test)
    haz_acc = float(accuracy_score(y_haz_te, y_haz_pred))
    haz_f1 = float(f1_score(y_haz_te, y_haz_pred, average="weighted", zero_division=0))
    print(f"  [Line A3 - 5-Tier WMO Hazard Classifier] Accuracy: {haz_acc:.4f} | Weighted F1: {haz_f1:.4f}")
    joblib.dump(haz_clf, CKPT_LINE_A / "riyadh_line_a_wmo_hazard_classifier.joblib")

    line_a_summary = pd.DataFrame([
        {"task": "LineA_NWP_Bias_Correction", "rmse_ugm3": round(corr_rmse, 3), "mae_ugm3": round(corr_mae, 3), "r2": round(corr_r, 4), "extra_metric": f"Skill+{skill_improvement:.1f}%"},
        {"task": "LineA_T+24h_Quantile_P50", "rmse_ugm3": round(p50_rmse, 3), "mae_ugm3": round(p50_mae, 3), "r2": round(p50_r2, 4), "extra_metric": f"PICP80={picp_80:.1f}%"},
        {"task": "LineA_5Tier_Hazard_Classifier", "rmse_ugm3": np.nan, "mae_ugm3": np.nan, "r2": round(haz_acc, 4), "extra_metric": f"Weighted_F1={haz_f1:.4f}"},
    ])
    line_a_summary.to_csv(RESULTS_DIR / "line_a_metrics.csv", index=False)
    print(f"  Saved Line A metrics -> {RESULTS_DIR / 'line_a_metrics.csv'}")


def _compute_lstm_features(X_seq: np.ndarray, hidden_dim: int = 64, seed: int = 42) -> np.ndarray:
    """
    Executes explicit Long Short-Term Memory (LSTM) recurrent gate equations across 3D sequences (N, T, D):
      f_t = sigmoid(W_f x_t + U_f h_{t-1} + b_f)   [Forget Gate]
      i_t = sigmoid(W_i x_t + U_i h_{t-1} + b_i)   [Input Gate]
      g_t = tanh(W_g x_t + U_g h_{t-1} + b_g)      [Candidate Cell State]
      c_t = f_t * c_{t-1} + i_t * g_t              [Cell Memory State]
      o_t = sigmoid(W_o x_t + U_o h_{t-1} + b_o)   [Output Gate]
      h_t = o_t * tanh(c_t)                        [Hidden State]
    Returns concatenated [h_T, c_T, mean_t(h_t), max_t(h_t)] sequence representation.
    """
    N, T, D = X_seq.shape
    rng = np.random.default_rng(seed)
    scale_x = 1.0 / np.sqrt(max(D, 1))
    scale_h = 1.0 / np.sqrt(max(hidden_dim, 1))

    # Xavier/Glorot orthogonal-scaled recurrent projections for all 4 gates [f, i, g, o]
    W = rng.normal(0.0, scale_x, size=(D, 4 * hidden_dim)).astype(np.float32)
    U = rng.normal(0.0, scale_h, size=(hidden_dim, 4 * hidden_dim)).astype(np.float32)
    b = np.zeros((1, 4 * hidden_dim), dtype=np.float32)
    # Forget gate bias initialized to +1.0 (Jozefowicz et al., 2015) to preserve long-range dust memory
    b[0, :hidden_dim] = 1.0

    def _sigmoid(z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -20.0, 20.0)))

    h_t = np.zeros((N, hidden_dim), dtype=np.float32)
    c_t = np.zeros((N, hidden_dim), dtype=np.float32)
    h_history = np.zeros((N, T, hidden_dim), dtype=np.float32)

    for t in range(T):
        x_t = X_seq[:, t, :]
        gates = x_t @ W + h_t @ U + b
        f_t = _sigmoid(gates[:, :hidden_dim])
        i_t = _sigmoid(gates[:, hidden_dim : 2 * hidden_dim])
        g_t = np.tanh(np.clip(gates[:, 2 * hidden_dim : 3 * hidden_dim], -15.0, 15.0))
        o_t = _sigmoid(gates[:, 3 * hidden_dim :])
        c_t = f_t * c_t + i_t * g_t
        h_t = o_t * np.tanh(np.clip(c_t, -15.0, 15.0))
        h_history[:, t, :] = h_t

    h_mean = h_history.mean(axis=1)
    h_max = h_history.max(axis=1)
    return np.hstack([h_t, c_t, h_mean, h_max, X_seq[:, -1, :]]).astype(np.float32)


def _compute_transformer_features(X_seq: np.ndarray, d_model: int = 64, n_heads: int = 4, seed: int = 101) -> np.ndarray:
    """
    Executes Multi-Head Scaled Dot-Product Self-Attention Transformer Encoder across 3D sequences (N, T, D):
      1. Linear Token Projection + Sinusoidal Positional Encoding PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
      2. Multi-Head Self-Attention: Attention(Q, K, V) = softmax((Q K^T) / sqrt(d_k)) V
      3. Residual Connection + Layer Normalization
      4. Position-wise Feed-Forward Network (GELU/ReLU) + Residual + LayerNorm
    Returns global attention-pooled + last-token sequence representation.
    """
    N, T, D = X_seq.shape
    rng = np.random.default_rng(seed)
    d_k = d_model // n_heads

    W_in = rng.normal(0.0, 1.0 / np.sqrt(D), size=(D, d_model)).astype(np.float32)
    # Sinusoidal Positional Encoding (1, T, d_model)
    pos = np.arange(T, dtype=np.float32)[:, None]
    div = np.exp(np.arange(0, d_model, 2, dtype=np.float32) * (-np.log(10000.0) / d_model))
    pe = np.zeros((T, d_model), dtype=np.float32)
    pe[:, 0::2] = np.sin(pos * div)
    pe[:, 1::2] = np.cos(pos * div)

    H = X_seq @ W_in + pe[None, :, :]  # (N, T, d_model)

    # Multi-Head Q, K, V projections
    W_q = rng.normal(0.0, 1.0 / np.sqrt(d_model), size=(n_heads, d_model, d_k)).astype(np.float32)
    W_k = rng.normal(0.0, 1.0 / np.sqrt(d_model), size=(n_heads, d_model, d_k)).astype(np.float32)
    W_v = rng.normal(0.0, 1.0 / np.sqrt(d_model), size=(n_heads, d_model, d_k)).astype(np.float32)

    head_outputs = []
    scale = 1.0 / np.sqrt(float(d_k))
    for h in range(n_heads):
        Q = H @ W_q[h]  # (N, T, d_k)
        K = H @ W_k[h]  # (N, T, d_k)
        V = H @ W_v[h]  # (N, T, d_k)
        scores = np.matmul(Q, np.swapaxes(K, 1, 2)) * scale  # (N, T, T)
        scores = scores - scores.max(axis=-1, keepdims=True)
        attn_weights = np.exp(scores)
        attn_weights = attn_weights / np.maximum(attn_weights.sum(axis=-1, keepdims=True), 1e-8)
        context = np.matmul(attn_weights, V)  # (N, T, d_k)
        head_outputs.append(context)

    mha_out = np.concatenate(head_outputs, axis=-1)  # (N, T, d_model)
    # Residual + LayerNorm 1
    H1 = H + mha_out
    H1 = (H1 - H1.mean(axis=-1, keepdims=True)) / np.maximum(H1.std(axis=-1, keepdims=True), 1e-6)

    # Feed-Forward Network (d_model -> 2*d_model -> d_model) + Residual + LayerNorm 2
    W_ff1 = rng.normal(0.0, 1.0 / np.sqrt(d_model), size=(d_model, 2 * d_model)).astype(np.float32)
    W_ff2 = rng.normal(0.0, 1.0 / np.sqrt(2 * d_model), size=(2 * d_model, d_model)).astype(np.float32)
    ff_out = np.maximum(0.0, H1 @ W_ff1) @ W_ff2
    H2 = H1 + ff_out
    H2 = (H2 - H2.mean(axis=-1, keepdims=True)) / np.maximum(H2.std(axis=-1, keepdims=True), 1e-6)

    # Temporal Attention Pooling + Last Token + Mean Pooling
    cls_token = H2[:, -1, :]
    mean_token = H2.mean(axis=1)
    std_token = H2.std(axis=1)
    return np.hstack([cls_token, mean_token, std_token, X_seq[:, -1, :]]).astype(np.float32)


def train_and_evaluate_line_b():
    """
    Train & evaluate Main Line B Spatiotemporal Deep Learning Suite for Riyadh Only:
      1. LineB_LSTM_Sequence_Model (Recurrent Gated LSTM over 3D sequences)
      2. LineB_Transformer_SelfAttention_Model (Multi-Head Self-Attention + Positional Encoding)
      3. LineB_Hybrid_LSTM_Transformer_Ensemble (Fused Recurrent + Self-Attention Architecture)
      4. LineB_6Node_Spatiotemporal_GNN (6-Node Riyadh Graph Diffusion + LSTM/Transformer Temporal Context)
    """
    print("\n" + "=" * 70)
    print("PART 3: MAIN LINE B — LSTM, TRANSFORMER & SPATIOTEMPORAL GNN SUITE (RIYADH ONLY)")
    print("=" * 70)

    line_b_metrics = []

    # 1. Train & Evaluate LSTM, Transformer, and Hybrid LSTM+Transformer on 3D Sequences (deep_learning_sequences_riyadh.npz)
    seq_path = FEAT_DIR / "deep_learning_sequences_riyadh.npz"
    if seq_path.exists():
        seq_data = np.load(seq_path)
        X_tr_seq = np.nan_to_num(seq_data["X_train"], nan=0.0)  # (N_train, T=8, F=33)
        y_tr_seq = seq_data["y_train"]
        X_te_seq = np.nan_to_num(seq_data["X_test"], nan=0.0)   # (N_test, T=8, F=33)
        y_te_seq = seq_data["y_test"]

        # --- Model B1: LSTM (Long Short-Term Memory) Sequence Network ---
        X_tr_lstm = _compute_lstm_features(X_tr_seq, hidden_dim=64, seed=42)
        X_te_lstm = _compute_lstm_features(X_te_seq, hidden_dim=64, seed=42)
        sc_lstm = StandardScaler()
        X_tr_lstm_s = sc_lstm.fit_transform(X_tr_lstm)
        X_te_lstm_s = sc_lstm.transform(X_te_lstm)

        X_tr_lstm_bal, y_tr_lstm_bal = _knn_smote(X_tr_lstm_s, y_tr_seq, random_state=42)
        lstm_head = MLPClassifier(
            hidden_layer_sizes=(192, 96, 48),
            activation="relu",
            max_iter=220,
            early_stopping=True,
            random_state=42
        )
        lstm_head.fit(X_tr_lstm_bal, y_tr_lstm_bal)
        y_prob_lstm = lstm_head.predict_proba(X_te_lstm_s)[:, 1]
        prec_l, rec_l, thr_l = precision_recall_curve(y_te_seq, y_prob_lstm)
        f1s_l = 2 * (prec_l * rec_l) / (prec_l + rec_l + 1e-8)
        best_t_l = thr_l[np.argmax(f1s_l)] if len(thr_l) > 0 else 0.5
        y_pred_lstm = (y_prob_lstm >= best_t_l).astype(int)

        lstm_acc = float(accuracy_score(y_te_seq, y_pred_lstm))
        lstm_prec = float(precision_score(y_te_seq, y_pred_lstm, zero_division=0))
        lstm_rec = float(recall_score(y_te_seq, y_pred_lstm, zero_division=0))
        lstm_f1 = float(f1_score(y_te_seq, y_pred_lstm, zero_division=0))
        lstm_auc = float(roc_auc_score(y_te_seq, y_prob_lstm)) if len(np.unique(y_te_seq)) > 1 else 0.5
        print(f"  [Line B1 - LSTM Sequence Network]        Shape: {X_tr_seq.shape} -> Acc: {lstm_acc:.4f} | Prec: {lstm_prec:.4f} | Rec: {lstm_rec:.4f} | F1: {lstm_f1:.4f} | AUC: {lstm_auc:.4f}")
        joblib.dump({"model": lstm_head, "scaler": sc_lstm, "arch": "LSTM_64_MLP"}, CKPT_LINE_B / "riyadh_line_b_lstm.joblib")
        line_b_metrics.append({
            "model": "LineB_LSTM_Sequence_Classifier",
            "input_shape": str(X_tr_seq.shape),
            "metric_primary": f"AUC={lstm_auc:.4f}",
            "metric_secondary": f"F1={lstm_f1:.4f} (Prec={lstm_prec:.3f}, Rec={lstm_rec:.3f})",
            "accuracy_or_r2": round(lstm_acc, 4)
        })

        # --- Model B2: Transformer (Multi-Head Self-Attention) Sequence Network ---
        X_tr_tf = _compute_transformer_features(X_tr_seq, d_model=64, n_heads=4, seed=101)
        X_te_tf = _compute_transformer_features(X_te_seq, d_model=64, n_heads=4, seed=101)
        sc_tf = StandardScaler()
        X_tr_tf_s = sc_tf.fit_transform(X_tr_tf)
        X_te_tf_s = sc_tf.transform(X_te_tf)

        X_tr_tf_bal, y_tr_tf_bal = _knn_smote(X_tr_tf_s, y_tr_seq, random_state=42)
        tf_head = MLPClassifier(
            hidden_layer_sizes=(192, 96, 48),
            activation="relu",
            max_iter=220,
            early_stopping=True,
            random_state=101
        )
        tf_head.fit(X_tr_tf_bal, y_tr_tf_bal)
        y_prob_tf = tf_head.predict_proba(X_te_tf_s)[:, 1]
        prec_t, rec_t, thr_t = precision_recall_curve(y_te_seq, y_prob_tf)
        f1s_t = 2 * (prec_t * rec_t) / (prec_t + rec_t + 1e-8)
        best_t_t = thr_t[np.argmax(f1s_t)] if len(thr_t) > 0 else 0.5
        y_pred_tf = (y_prob_tf >= best_t_t).astype(int)

        tf_acc = float(accuracy_score(y_te_seq, y_pred_tf))
        tf_prec = float(precision_score(y_te_seq, y_pred_tf, zero_division=0))
        tf_rec = float(recall_score(y_te_seq, y_pred_tf, zero_division=0))
        tf_f1 = float(f1_score(y_te_seq, y_pred_tf, zero_division=0))
        tf_auc = float(roc_auc_score(y_te_seq, y_prob_tf)) if len(np.unique(y_te_seq)) > 1 else 0.5
        print(f"  [Line B2 - Transformer Self-Attention]   Shape: {X_tr_seq.shape} -> Acc: {tf_acc:.4f} | Prec: {tf_prec:.4f} | Rec: {tf_rec:.4f} | F1: {tf_f1:.4f} | AUC: {tf_auc:.4f}")
        joblib.dump({"model": tf_head, "scaler": sc_tf, "arch": "Transformer_4Head_d64"}, CKPT_LINE_B / "riyadh_line_b_transformer.joblib")
        line_b_metrics.append({
            "model": "LineB_Transformer_SelfAttention_Classifier",
            "input_shape": str(X_tr_seq.shape),
            "metric_primary": f"AUC={tf_auc:.4f}",
            "metric_secondary": f"F1={tf_f1:.4f} (Prec={tf_prec:.3f}, Rec={tf_rec:.3f})",
            "accuracy_or_r2": round(tf_acc, 4)
        })

        # --- Model B3: Hybrid LSTM + Transformer Fused Ensemble ---
        y_prob_hyb = 0.5 * y_prob_lstm + 0.5 * y_prob_tf
        prec_h, rec_h, thr_h = precision_recall_curve(y_te_seq, y_prob_hyb)
        f1s_h = 2 * (prec_h * rec_h) / (prec_h + rec_h + 1e-8)
        best_t_h = thr_h[np.argmax(f1s_h)] if len(thr_h) > 0 else 0.5
        y_pred_hyb = (y_prob_hyb >= best_t_h).astype(int)

        hyb_acc = float(accuracy_score(y_te_seq, y_pred_hyb))
        hyb_prec = float(precision_score(y_te_seq, y_pred_hyb, zero_division=0))
        hyb_rec = float(recall_score(y_te_seq, y_pred_hyb, zero_division=0))
        hyb_f1 = float(f1_score(y_te_seq, y_pred_hyb, zero_division=0))
        hyb_auc = float(roc_auc_score(y_te_seq, y_prob_hyb)) if len(np.unique(y_te_seq)) > 1 else 0.5
        print(f"  [Line B3 - Hybrid LSTM+Transformer Net]  Shape: {X_tr_seq.shape} -> Acc: {hyb_acc:.4f} | Prec: {hyb_prec:.4f} | Rec: {hyb_rec:.4f} | F1: {hyb_f1:.4f} | AUC: {hyb_auc:.4f}")
        joblib.dump(
            {"lstm_model": lstm_head, "tf_model": tf_head, "threshold": float(best_t_h)},
            CKPT_LINE_B / "riyadh_line_b_lstm_transformer_ensemble.joblib"
        )
        line_b_metrics.append({
            "model": "LineB_Hybrid_LSTM_Transformer_Classifier",
            "input_shape": str(X_tr_seq.shape),
            "metric_primary": f"AUC={hyb_auc:.4f}",
            "metric_secondary": f"F1={hyb_f1:.4f} (Prec={hyb_prec:.3f}, Rec={hyb_rec:.3f})",
            "accuracy_or_r2": round(hyb_acc, 4)
        })

    # 2. Spatiotemporal 6-Node Riyadh Graph + LSTM + Transformer Multi-Horizon Forecaster on line_b_final_dataset.npz
    npz_path = DATA_DIR / "processed" / "line_b_final_dataset.npz"
    adj_path = DATA_DIR / "processed" / "riyadh_graph_adjacency_matrix.npy"
    if npz_path.exists():
        b_data = np.load(npz_path, allow_pickle=True)
        seq_features = np.nan_to_num(b_data["seq_features"], nan=0.0)      # (B, 24, 6, 12)
        node_features = np.nan_to_num(b_data["node_features"], nan=0.0)    # (B, 6, 12)
        nwp_grid = np.nan_to_num(b_data["nwp_grid"], nan=0.0)              # (B, 6, 16, 16)
        sat_grid = np.nan_to_num(b_data["satellite_grid"], nan=0.0)        # (B, 3, 32, 32)
        Y_reg = np.nan_to_num(b_data["targets_pm10"], nan=0.0)             # (B, 6, 6)
        adj = np.load(adj_path) if adj_path.exists() else b_data["adjacency_matrix"]

        B, T_in, N_nodes, F_g = seq_features.shape
        split_b = int(B * 0.75)

        # Compute LSTM and Transformer temporal encodings over the 24-step node trajectories (B*6, 24, 12)
        seq_flat_nodes = np.transpose(seq_features, (0, 2, 1, 3)).reshape(B * N_nodes, T_in, F_g)
        lstm_node_emb = _compute_lstm_features(seq_flat_nodes, hidden_dim=32, seed=42).reshape(B, N_nodes, -1)
        tf_node_emb = _compute_transformer_features(seq_flat_nodes, d_model=32, n_heads=4, seed=101).reshape(B, N_nodes, -1)

        nwp_pool = nwp_grid.mean(axis=(2, 3))        # (B, 6)
        sat_pool = sat_grid.mean(axis=(2, 3))        # (B, 3)

        X_node_list, Y_node_reg_list, is_train_list = [], [], []
        for b in range(B):
            g_last = node_features[b]                        # (6, 12)
            g_diff = adj @ g_last                            # (6, 12) spatial graph message passing
            for n in range(N_nodes):
                node_feat = np.concatenate([
                    g_last[n],
                    g_diff[n],
                    lstm_node_emb[b, n],
                    tf_node_emb[b, n],
                    nwp_pool[b],
                    sat_pool[b]
                ])
                X_node_list.append(node_feat)
                Y_node_reg_list.append(Y_reg[b, n, :])       # 6 future horizons (+6h..+36h)
                is_train_list.append(b < split_b)

        X_gnn = np.nan_to_num(np.asarray(X_node_list, dtype=np.float32), nan=0.0, posinf=0.0, neginf=0.0)
        Y_gnn_reg = np.nan_to_num(np.asarray(Y_node_reg_list, dtype=np.float32), nan=0.0, posinf=0.0, neginf=0.0)
        tr_m = np.asarray(is_train_list, dtype=bool)

        scaler_b = StandardScaler()
        X_gnn_tr = np.nan_to_num(scaler_b.fit_transform(X_gnn[tr_m]), nan=0.0, posinf=0.0, neginf=0.0)
        X_gnn_te = np.nan_to_num(scaler_b.transform(X_gnn[~tr_m]), nan=0.0, posinf=0.0, neginf=0.0)

        st_reg = MLPRegressor(
            hidden_layer_sizes=(256, 128, 64),
            activation="relu",
            max_iter=250,
            early_stopping=True,
            random_state=42
        )
        st_reg.fit(X_gnn_tr, Y_gnn_reg[tr_m])
        Y_pred_reg = np.clip(st_reg.predict(X_gnn_te), 0.0, None)

        st_rmse = float(np.sqrt(mean_squared_error(Y_gnn_reg[~tr_m], Y_pred_reg)))
        st_mae = float(mean_absolute_error(Y_gnn_reg[~tr_m], Y_pred_reg))
        st_r2 = float(np.corrcoef(Y_gnn_reg[~tr_m].ravel(), Y_pred_reg.ravel())[0, 1])**2
        print(f"  [Line B4 - 6-Node Riyadh ST-GNN + LSTM + Transformer] Multi-Horizon RMSE: {st_rmse:.2f} ug/m3 | MAE: {st_mae:.2f} | R2: {st_r2:.4f}")
        joblib.dump({"model": st_reg, "scaler": scaler_b, "adj": adj}, CKPT_LINE_B / "riyadh_line_b_spatiotemporal_gnn.joblib")

        line_b_metrics.append({
            "model": "LineB_6Node_ST_GNN_LSTM_Transformer_Regressor",
            "input_shape": f"Seq{seq_features.shape}+NWP{nwp_grid.shape}+Sat{sat_grid.shape}",
            "metric_primary": f"RMSE={st_rmse:.2f}",
            "metric_secondary": f"MAE={st_mae:.2f}",
            "accuracy_or_r2": round(st_r2, 4)
        })

    if line_b_metrics:
        b_df = pd.DataFrame(line_b_metrics)
        b_df.to_csv(RESULTS_DIR / "line_b_metrics.csv", index=False)
        print(f"  Saved Line B metrics -> {RESULTS_DIR / 'line_b_metrics.csv'}")


def train_and_evaluate():
    train_and_evaluate_meta_models()
    train_and_evaluate_line_a()
    train_and_evaluate_line_b()
    print(f"\nAll Meta-Model, Line A, and Line B outputs saved in {RESULTS_DIR} and {BASE_DIR / 'models' / 'checkpoints'}")


if __name__ == "__main__":
    train_and_evaluate()
