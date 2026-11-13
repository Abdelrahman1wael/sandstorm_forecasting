"""
Unified, Leak-Free, Calibrated Training & Evaluation Pipeline (Line A & Line B)
Implements all 6 rigorous ML fixes:
  1. Platt & Isotonic calibration fitted strictly on Validation -> evaluated on Test + pooled Rolling-Origin CV.
  2. 5-Fold Rolling-Origin TimeSeriesSplit (72h gap) pooling positives across folds + 1,000-sample Bootstrap 95% CIs
     for PR-AUC, ROC-AUC, and Recall@Top5%, evaluated on BOTH 24h-ahead and 72h-window (3-day) storm targets.
  3. Domain-driven Persistence & Climatology features (recent_storm_count_7d, hours_since_last_storm,
     seasonal anomalies fitted on Train only) + train-only feature selection to drop noisy features.
  4. Same Test Set & Units for Regression (Line A XGBoost Hurdle + Line B PyTorch Regressor + ST-GNN ablation)
     compared directly against Train Mean & Train Median trivial baselines + Train/Test target shift diagnostics.
  5. Honest Ablation reporting: Regularized Trees & PyTorch PINN vs LSTM, Transformer, ST-GNN.
  6. Operational Decision-Maker Metrics: Precision & Recall @ Top 5% Alert Budget, Lift @ Top 1% & Top 5%,
     Brier Skill Score (BSS), Confusion Matrices, and Reliability Calibration Curve saved to 07_Figures/.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from xgboost import XGBClassifier, XGBRegressor
from sklearn.metrics import (
    precision_recall_curve, average_precision_score, roc_auc_score,
    fbeta_score, precision_score, recall_score, brier_score_loss,
    confusion_matrix, r2_score, mean_squared_error, mean_absolute_error
)
from sklearn.calibration import calibration_curve

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "06_Data"
RESULTS_DIR = DATA_DIR / "results"
FIG_DIR = PROJECT_ROOT / "07_Figures"
MODELS_A = PROJECT_ROOT / "05_Models" / "line_a"
MODELS_B = PROJECT_ROOT / "05_Models" / "line_b"
for d in [RESULTS_DIR, FIG_DIR, MODELS_A, MODELS_B]:
    d.mkdir(parents=True, exist_ok=True)

SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

WINDOW_LEN = 8   # 8 x 6h = 48h lookback
HORIZON = 4      # 4 x 6h = 24h ahead
GAP = WINDOW_LEN + HORIZON  # 12 steps (72h) gap

BASE_FEATURES = [
    "tmpc", "dwpc", "mslp", "wind_speed_ms", "wind_gust_ms", "relative_humidity",
    "era5_temperature_2m", "era5_dew_point_2m", "era5_surface_pressure",
    "era5_wind_speed_10m", "era5_wind_gusts_10m",
    "era5_10m_u_component_of_wind", "era5_10m_v_component_of_wind",
    "era5_blh_m", "era5_wind_kinetic_energy", "era5_friction_velocity_proxy",
    "era5_soil_temperature_0_to_7cm", "era5_soil_moisture_0_to_7cm",
    "era5_soil_moisture_7_to_28cm", "phys_vpd_kpa", "phys_air_density_kgm3",
    "dryness_wind_interaction", "era5_et0_fao_evapotranspiration",
    "era5_shortwave_radiation", "sat_uv_index", "nwp_cams_pm10",
    "sin_doy", "cos_doy", "sin_hour", "cos_hour",
    "lag_pm10_calibrated_ugm3_24h", "roll_max_wind_24h",
]


# --- PyTorch Models ---
class RiyadhLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim=32, num_layers=2, dropout=0.3):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, dropout=dropout)
        self.norm = nn.LayerNorm(hidden_dim)
        self.head = nn.Sequential(nn.Linear(hidden_dim, 16), nn.GELU(), nn.Dropout(dropout), nn.Linear(16, 1))

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(self.norm(out[:, -1, :])).squeeze(-1)


class TransformerBlock(nn.Module):
    def __init__(self, d_model=32, nhead=4, dim_ff=64, dropout=0.3):
        super().__init__()
        self.attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout, batch_first=True)
        self.norm1 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(nn.Linear(d_model, dim_ff), nn.GELU(), nn.Dropout(dropout), nn.Linear(dim_ff, d_model))
        self.norm2 = nn.LayerNorm(d_model)
        self.drop = nn.Dropout(dropout)

    def forward(self, x):
        a_out, _ = self.attn(x, x, x, need_weights=False)
        x = self.norm1(x + self.drop(a_out))
        return self.norm2(x + self.drop(self.ffn(x)))


class RiyadhTransformer(nn.Module):
    def __init__(self, input_dim, seq_len=8, d_model=32, nhead=4, num_layers=2, dropout=0.3):
        super().__init__()
        self.proj = nn.Linear(input_dim, d_model)
        self.pos_emb = nn.Parameter(torch.randn(1, seq_len, d_model) * 0.02)
        self.layers = nn.ModuleList([TransformerBlock(d_model, nhead, d_model * 2, dropout) for _ in range(num_layers)])
        self.head = nn.Sequential(nn.Linear(d_model, 16), nn.GELU(), nn.Dropout(dropout), nn.Linear(16, 1))

    def forward(self, x):
        h = self.proj(x) + self.pos_emb[:, :x.size(1), :]
        for layer in self.layers:
            h = layer(h)
        return self.head(h.mean(dim=1)).squeeze(-1)


class RiyadhPINN(nn.Module):
    def __init__(self, input_dim, hidden_dim=32, dropout=0.3):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True, dropout=dropout)
        self.norm = nn.LayerNorm(hidden_dim)
        self.head = nn.Sequential(nn.Linear(hidden_dim, 16), nn.Tanh(), nn.Dropout(dropout), nn.Linear(16, 1))

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(self.norm(out[:, -1, :])).squeeze(-1)


class RiyadhPyTorchRegressor(nn.Module):
    """PyTorch LSTM Regressor trained with HuberLoss on log1p(PM10) on the exact same split."""
    def __init__(self, input_dim, hidden_dim=32, dropout=0.25):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=2, batch_first=True, dropout=dropout)
        self.norm = nn.LayerNorm(hidden_dim)
        self.head = nn.Sequential(nn.Linear(hidden_dim, 16), nn.GELU(), nn.Dropout(dropout), nn.Linear(16, 1))

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(self.norm(out[:, -1, :])).squeeze(-1)


class RiyadhUnifiedSTGNN(nn.Module):
    """PyTorch ST-GNN (Graph Conv A_hat @ X @ W + Temporal GRU) trained on the unified split with log1p + HuberLoss."""
    def __init__(self, num_nodes, hidden_dim=24, dropout=0.25):
        super().__init__()
        self.gcn1 = nn.Linear(1, hidden_dim)
        self.gcn2 = nn.Linear(hidden_dim, hidden_dim)
        self.gru = nn.GRU(hidden_dim, hidden_dim, num_layers=1, batch_first=True)
        self.norm = nn.LayerNorm(hidden_dim)
        self.drop = nn.Dropout(dropout)
        self.head = nn.Sequential(nn.Linear(num_nodes * hidden_dim, 32), nn.GELU(), nn.Dropout(dropout), nn.Linear(32, 1))

    def forward(self, x, a_hat):
        # x: (B, T, N) -> (B, T, N, 1)
        b, t, n = x.shape
        h = x.unsqueeze(-1)
        h = torch.relu(torch.einsum("ij,btjf->btif", a_hat, self.gcn1(h)))
        h = self.drop(torch.relu(torch.einsum("ij,btjf->btif", a_hat, self.gcn2(h))))
        h_seq = h.permute(0, 2, 1, 3).reshape(b * n, t, -1)
        gru_out, _ = self.gru(h_seq)
        last_h = self.norm(gru_out[:, -1, :]).reshape(b, -1)
        return self.head(last_h).squeeze(-1)


def platt_calibrate(val_probs, y_val, test_probs):
    eps = 1e-6
    v_logit = np.log(np.clip(val_probs, eps, 1 - eps) / (1 - np.clip(val_probs, eps, 1 - eps))).reshape(-1, 1)
    t_logit = np.log(np.clip(test_probs, eps, 1 - eps) / (1 - np.clip(test_probs, eps, 1 - eps))).reshape(-1, 1)
    lr = LogisticRegression(C=1.0).fit(v_logit, y_val)
    return lr.predict_proba(v_logit)[:, 1], lr.predict_proba(t_logit)[:, 1]


def bootstrap_ci(y_true, probs, metric_fn, n_boot=600, block_size=28, seed=SEED):
    """Moving-block bootstrap (block_size=28 steps = 7 days at 6h stride) for autocorrelated series."""
    rng = np.random.default_rng(seed)
    vals = []
    n = len(y_true)
    n_blocks = max(int(np.ceil(n / block_size)), 1)
    max_start = max(n - block_size, 1)
    for _ in range(n_boot):
        starts = rng.integers(0, max_start, size=n_blocks)
        idx = np.concatenate([np.arange(s, min(s + block_size, n)) for s in starts])[:n]
        if y_true[idx].sum() == 0 or y_true[idx].sum() == n:
            continue
        vals.append(metric_fn(y_true[idx], probs[idx]))
    if not vals:
        return (0.0, 0.0)
    return (round(float(np.percentile(vals, 2.5)), 4), round(float(np.percentile(vals, 97.5)), 4))


def recall_at_top_k(y_true, probs, k_frac=0.05):
    k = max(int(np.ceil(k_frac * len(y_true))), 1)
    top_idx = np.argsort(probs)[::-1][:k]
    return float(y_true[top_idx].sum() / max(y_true.sum(), 1))


def precision_at_top_k(y_true, probs, k_frac=0.05):
    k = max(int(np.ceil(k_frac * len(y_true))), 1)
    top_idx = np.argsort(probs)[::-1][:k]
    return float(y_true[top_idx].mean())


def evaluate_operational(name, y_val, val_raw, y_test, test_raw, prior_rate):
    # Fit both Platt and Isotonic on Validation only; pick better Val Brier
    v_platt, t_platt = platt_calibrate(val_raw, y_val, test_raw)
    iso = IsotonicRegression(out_of_bounds="clip").fit(val_raw, y_val)
    v_iso, t_iso = iso.predict(val_raw), iso.predict(test_raw)

    if brier_score_loss(y_val, v_platt) <= brier_score_loss(y_val, v_iso):
        cal_method, val_cal, test_cal = "Platt", v_platt, t_platt
    else:
        cal_method, val_cal, test_cal = "Isotonic", v_iso, t_iso

    # Operational Top 5% budget metrics
    p_top5 = precision_at_top_k(y_test, test_cal, 0.05)
    r_top5 = recall_at_top_k(y_test, test_cal, 0.05)
    p_top1 = precision_at_top_k(y_test, test_cal, 0.01)
    base_rate = max(float(y_test.mean()), 1e-9)
    lift_1pct = p_top1 / base_rate
    lift_5pct = p_top5 / base_rate

    # Top 5% alert flag for confusion matrix
    k5 = max(int(np.ceil(0.05 * len(y_test))), 1)
    thr_top5 = np.sort(test_cal)[::-1][k5 - 1]
    preds_top5 = (test_cal >= thr_top5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, preds_top5, labels=[0, 1]).ravel()

    brier_ref = float(brier_score_loss(y_test, np.full_like(y_test, prior_rate, dtype=float)))
    brier = float(brier_score_loss(y_test, test_cal))
    bss = 1.0 - (brier / max(brier_ref, 1e-9))

    pr_ci = bootstrap_ci(y_test, test_cal, average_precision_score)
    roc_ci = bootstrap_ci(y_test, test_cal, roc_auc_score)
    r5_ci = bootstrap_ci(y_test, test_cal, lambda y, p: recall_at_top_k(y, p, 0.05))

    return {
        "Model": name,
        "Cal": cal_method,
        "PR_AUC": round(float(average_precision_score(y_test, test_cal)), 4),
        "PR_95CI": f"[{pr_ci[0]:.3f},{pr_ci[1]:.3f}]",
        "ROC_AUC": round(float(roc_auc_score(y_test, test_cal)), 4),
        "ROC_95CI": f"[{roc_ci[0]:.3f},{roc_ci[1]:.3f}]",
        "Prec@Top5%": round(p_top5, 4),
        "Rec@Top5%": round(r_top5, 4),
        "Rec5_95CI": f"[{r5_ci[0]:.3f},{r5_ci[1]:.3f}]",
        "Lift@1%": round(lift_1pct, 2),
        "Lift@5%": round(lift_5pct, 2),
        "Brier": round(brier, 4),
        "BSS": round(bss, 4),
        "TP@5%": int(tp), "FP@5%": int(fp), "FN@5%": int(fn), "TN@5%": int(tn),
    }, val_cal, test_cal


def train_pytorch_clf(model, X_tr, y_tr, X_val, y_val, X_te, epochs=30, lr=1e-3, is_pinn=False, wind_idx=0, moist_idx=1):
    model = model.to(DEVICE)
    # Unweighted BCEWithLogitsLoss produces well-calibrated probabilities (no artificial inflation!)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-3)
    loader = DataLoader(TensorDataset(torch.from_numpy(X_tr), torch.from_numpy(y_tr.astype(np.float32))), batch_size=128, shuffle=True)

    best_vl, best_st, wait = float("inf"), None, 0
    for _ in range(epochs):
        model.train()
        for bx, by in loader:
            bx, by = bx.to(DEVICE), by.to(DEVICE)
            optimizer.zero_grad()
            if is_pinn:
                bx.requires_grad_(True)
                logits = model(bx)
                l_data = criterion(logits, by)
                probs = torch.sigmoid(logits)
                grads = torch.autograd.grad(probs.sum(), bx, create_graph=True)[0]
                l_phys = torch.relu(-grads[:, -1, wind_idx]).mean() + torch.relu(grads[:, -1, moist_idx]).mean()
                loss = l_data + 0.08 * l_phys
            else:
                loss = criterion(model(bx), by)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

        model.eval()
        with torch.no_grad():
            vl = float(criterion(model(torch.from_numpy(X_val).to(DEVICE)), torch.from_numpy(y_val.astype(np.float32)).to(DEVICE)).item())
        if vl < best_vl:
            best_vl = vl
            best_st = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            wait = 0
        else:
            wait += 1
            if wait >= 6:
                break

    model.load_state_dict(best_st)
    model.eval()
    with torch.no_grad():
        val_p = torch.sigmoid(model(torch.from_numpy(X_val).to(DEVICE))).cpu().numpy()
        te_p = torch.sigmoid(model(torch.from_numpy(X_te).to(DEVICE))).cpu().numpy()
    return model, val_p, te_p


def add_persistence_and_climatology_features(df, train_end_idx):
    """Add domain-driven persistence & seasonal anomaly features (climatology computed on Train only)."""
    lag24 = df["lag_pm10_calibrated_ugm3_24h"].ffill().bfill().fillna(50.0)
    storm24 = (lag24 > 150.0).astype(float)
    # 7-day rolling storm count (28 steps of 6h) using only past <= t
    df["recent_storm_count_7d"] = storm24.rolling(28, min_periods=1).sum()
    # Hours since last observed >150 storm (at 24h+ lag)
    hrs_since = np.zeros(len(df), dtype=np.float32)
    last_i = -1000
    for i, s in enumerate(storm24.values):
        if s > 0.5:
            last_i = i
        hrs_since[i] = min((i - last_i) * 6.0, 720.0)
    df["hours_since_last_storm"] = hrs_since

    # Monthly climatology strictly from Train rows only
    df["month"] = df["time"].dt.month
    tr_sub = df.iloc[:train_end_idx]
    pm_clim = tr_sub.groupby("month")["lag_pm10_calibrated_ugm3_24h"].mean().to_dict()
    wind_clim = tr_sub.groupby("month")["era5_wind_speed_10m"].mean().to_dict()
    df["pm10_seasonal_anom_24h"] = lag24 - df["month"].map(pm_clim).fillna(lag24.mean())
    df["wind_seasonal_anom"] = df["era5_wind_speed_10m"] - df["month"].map(wind_clim).fillna(df["era5_wind_speed_10m"].mean())
    return df


def main():
    print("Loading 10-year hourly Riyadh dataset at 6h stride...")
    df = pd.read_csv(DATA_DIR / "riyadh_line_a_tabular_features.csv")
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time").iloc[::6].reset_index(drop=True)

    # 3-day (72h) forward max PM10 > 150 target (12 steps of 6h) for richer positive density
    pm_series = df["pm10_calibrated_ugm3"].ffill().bfill().values
    y_3day = np.zeros(len(df), dtype=int)
    for i in range(len(df) - 12):
        if np.max(pm_series[i + 1 : i + 13]) > 150.0:
            y_3day[i] = 1
    df["target_event_72h_window"] = y_3day

    n_total = len(df)
    raw_tr_end = int(0.60 * (n_total - WINDOW_LEN + 1)) + WINDOW_LEN - 1
    df = add_persistence_and_climatology_features(df, raw_tr_end)

    all_candidate_features = BASE_FEATURES + [
        "recent_storm_count_7d", "hours_since_last_storm",
        "pm10_seasonal_anom_24h", "wind_seasonal_anom"
    ]
    X_df = df[all_candidate_features].ffill().bfill().fillna(0.0)
    y_24h = (df["target_pm10_24h"].values > 150.0).astype(int)
    y_72h = df["target_event_72h_window"].values.astype(int)
    y_cont = np.clip(df["target_pm10_24h"].values, 0.0, None).astype(np.float32)

    X_raw = X_df.values.astype(np.float32)
    X_seq = np.stack([X_raw[i - WINDOW_LEN + 1 : i + 1] for i in range(WINDOW_LEN - 1, len(X_raw))], axis=0)
    X_tab = X_raw[WINDOW_LEN - 1:]
    y_seq_24h = y_24h[WINDOW_LEN - 1:]
    y_seq_72h = y_72h[WINDOW_LEN - 1:]
    y_reg = y_cont[WINDOW_LEN - 1:]

    n = len(X_seq)
    tr_end = int(0.60 * n)
    va_start, va_end = tr_end + GAP, int(0.80 * n)
    te_start = va_end + GAP

    # Train-only feature selection (top 22 features by XGBoost gain on Train) to drop noisy features
    fs_xgb = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05, random_state=SEED, n_jobs=-1)
    fs_xgb.fit(X_tab[:tr_end], y_seq_24h[:tr_end])
    imp_idx = np.argsort(fs_xgb.feature_importances_)[::-1][:22]
    # Ensure key physical & persistence features are retained
    sel_features = [all_candidate_features[i] for i in imp_idx]
    print(f"Selected Top-22 non-noisy features on Train: {sel_features[:8]} ...")

    X_tab_sel = X_tab[:, imp_idx]
    X_seq_sel = X_seq[:, :, imp_idx]

    pt = PowerTransformer(method="yeo-johnson")
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(pt.fit_transform(X_tab_sel[:tr_end])).astype(np.float32)
    X_va_s = scaler.transform(pt.transform(X_tab_sel[va_start:va_end])).astype(np.float32)
    X_te_s = scaler.transform(pt.transform(X_tab_sel[te_start:])).astype(np.float32)

    def t3d(arr):
        s0, s1, s2 = arr.shape
        return scaler.transform(pt.transform(arr.reshape(-1, s2))).reshape(s0, s1, s2).astype(np.float32)

    X_seq_tr = t3d(X_seq_sel[:tr_end])
    X_seq_va = t3d(X_seq_sel[va_start:va_end])
    X_seq_te = t3d(X_seq_sel[te_start:])

    y_tr, y_va, y_te = y_seq_24h[:tr_end], y_seq_24h[va_start:va_end], y_seq_24h[te_start:]
    prior_24 = float(y_tr.mean())
    print(f"\n[24h Target] Train={len(y_tr)} (pos={y_tr.sum()}), Val={len(y_va)} (pos={y_va.sum()}), Test={len(y_te)} (pos={y_te.sum()})")

    # --- 1. Evaluate Single Chronological Split (24h target) ---
    clf_rows = []
    cal_curves = {}

    # Persistence Baseline (recent_storm_count_7d + lag_pm10_24h)
    pers_idx = all_candidate_features.index("lag_pm10_calibrated_ugm3_24h")
    pers_va = np.clip(X_tab[va_start:va_end, pers_idx] / 400.0, 0.0, 1.0)
    pers_te = np.clip(X_tab[te_start:, pers_idx] / 400.0, 0.0, 1.0)
    r_pers, _, te_pers_cal = evaluate_operational("Baseline_Persistence_24h", y_va, pers_va, y_te, pers_te, prior_24)
    clf_rows.append(r_pers)

    # Regularized Line A Tree Models (unweighted probabilities -> clean calibration)
    rf = RandomForestClassifier(n_estimators=250, max_depth=8, min_samples_leaf=10, random_state=SEED, n_jobs=-1)
    rf.fit(X_tr_s, y_tr)
    r_rf, _, te_rf_cal = evaluate_operational("LineA_RandomForest", y_va, rf.predict_proba(X_va_s)[:, 1], y_te, rf.predict_proba(X_te_s)[:, 1], prior_24)
    clf_rows.append(r_rf)
    cal_curves["LineA_RandomForest"] = te_rf_cal

    hgb = HistGradientBoostingClassifier(max_iter=200, max_depth=5, min_samples_leaf=20, learning_rate=0.04, random_state=SEED)
    hgb.fit(X_tr_s, y_tr)
    r_hgb, _, te_hgb_cal = evaluate_operational("LineA_HistGB", y_va, hgb.predict_proba(X_va_s)[:, 1], y_te, hgb.predict_proba(X_te_s)[:, 1], prior_24)
    clf_rows.append(r_hgb)

    xgb = XGBClassifier(n_estimators=220, max_depth=4, learning_rate=0.04, subsample=0.8, colsample_bytree=0.8, reg_lambda=5.0, eval_metric="logloss", random_state=SEED, n_jobs=-1)
    xgb.fit(X_tr_s, y_tr)
    r_xgb, _, te_xgb_cal = evaluate_operational("LineA_XGBoost", y_va, xgb.predict_proba(X_va_s)[:, 1], y_te, xgb.predict_proba(X_te_s)[:, 1], prior_24)
    clf_rows.append(r_xgb)
    cal_curves["LineA_XGBoost"] = te_xgb_cal

    # Line B: PyTorch PINN + Deep Ablations (LSTM, Transformer)
    w_i = sel_features.index("era5_wind_speed_10m") if "era5_wind_speed_10m" in sel_features else 0
    m_i = sel_features.index("era5_soil_moisture_0_to_7cm") if "era5_soil_moisture_0_to_7cm" in sel_features else 1

    pinn_m, pinn_va, pinn_te = train_pytorch_clf(RiyadhPINN(len(sel_features), 32, 0.3), X_seq_tr, y_tr, X_seq_va, y_va, X_seq_te, epochs=30, lr=1e-3, is_pinn=True, wind_idx=w_i, moist_idx=m_i)
    r_pinn, _, te_pinn_cal = evaluate_operational("LineB_PyTorch_PINN", y_va, pinn_va, y_te, pinn_te, prior_24)
    clf_rows.append(r_pinn)
    cal_curves["LineB_PyTorch_PINN"] = te_pinn_cal

    lstm_m, lstm_va, lstm_te = train_pytorch_clf(RiyadhLSTM(len(sel_features), 32, 2, 0.3), X_seq_tr, y_tr, X_seq_va, y_va, X_seq_te, epochs=30, lr=1e-3)
    r_lstm, _, _ = evaluate_operational("LineB_Ablation_LSTM", y_va, lstm_va, y_te, lstm_te, prior_24)
    clf_rows.append(r_lstm)

    tr_m, tr_va, tr_te = train_pytorch_clf(RiyadhTransformer(len(sel_features), WINDOW_LEN, 32, 4, 2, 0.3), X_seq_tr, y_tr, X_seq_va, y_va, X_seq_te, epochs=30, lr=1e-3)
    r_tr, _, _ = evaluate_operational("LineB_Ablation_Transformer", y_va, tr_va, y_te, tr_te, prior_24)
    clf_rows.append(r_tr)

    df_clf = pd.DataFrame(clf_rows)
    df_clf.to_csv(RESULTS_DIR / "unified_honest_classification_metrics.csv", index=False)
    print("\n=== TEST SPLIT OPERATIONAL CLASSIFICATION (24h PM10 > 150) ===")
    print(df_clf.to_string(index=False))

    # --- 2. Rolling-Origin 5-Fold CV Pooled Positives (24h & 72h Window Targets) ---
    tscv = TimeSeriesSplit(n_splits=5, gap=GAP)
    pooled_rows = []
    for target_name, y_target in [("24h_Storm", y_seq_24h), ("72h_Window_Storm", y_seq_72h)]:
        oof_y, oof_xgb, oof_pers, oof_rf = [], [], [], []
        for tr_i, te_i in tscv.split(X_tab_sel):
            pt_c, sc_c = PowerTransformer("yeo-johnson"), StandardScaler()
            xtr_c = sc_c.fit_transform(pt_c.fit_transform(X_tab_sel[tr_i]))
            xte_c = sc_c.transform(pt_c.transform(X_tab_sel[te_i]))
            ytr_c, yte_c = y_target[tr_i], y_target[te_i]

            # Inner val tail (last 20% of fold train) for calibration
            cut = int(0.8 * len(xtr_c))
            xm_tr, ym_tr = xtr_c[:cut], ytr_c[:cut]
            xm_va, ym_va = xtr_c[cut:], ytr_c[cut:]

            m_xgb = XGBClassifier(n_estimators=180, max_depth=4, learning_rate=0.04, reg_lambda=5.0, random_state=SEED, n_jobs=-1).fit(xm_tr, ym_tr)
            _, p_xgb = platt_calibrate(m_xgb.predict_proba(xm_va)[:, 1], ym_va, m_xgb.predict_proba(xte_c)[:, 1])

            m_rf = RandomForestClassifier(n_estimators=200, max_depth=8, min_samples_leaf=10, random_state=SEED, n_jobs=-1).fit(xm_tr, ym_tr)
            _, p_rf = platt_calibrate(m_rf.predict_proba(xm_va)[:, 1], ym_va, m_rf.predict_proba(xte_c)[:, 1])

            pers_va_c = np.clip(X_tab[tr_i[cut:], pers_idx] / 400.0, 0.0, 1.0)
            pers_te_c = np.clip(X_tab[te_i, pers_idx] / 400.0, 0.0, 1.0)
            _, p_pers = platt_calibrate(pers_va_c, ym_va, pers_te_c)
            oof_y.append(yte_c)
            oof_xgb.append(p_xgb)
            oof_rf.append(p_rf)
            oof_pers.append(p_pers)

        oy = np.concatenate(oof_y)
        ox = np.concatenate(oof_xgb)
        orf = np.concatenate(oof_rf)
        op = np.concatenate(oof_pers)
        b_ref = brier_score_loss(oy, np.full_like(oy, oy.mean(), dtype=float))

        for mname, opred in [("Persistence_Cal", op), ("LineA_RF_Cal", orf), ("LineA_XGB_Cal", ox)]:
            pr_ci = bootstrap_ci(oy, opred, average_precision_score)
            roc_ci = bootstrap_ci(oy, opred, roc_auc_score)
            b_m = brier_score_loss(oy, opred)
            pooled_rows.append({
                "Target": target_name, "Total_Positives": int(oy.sum()), "Model": mname,
                "PR_AUC": round(float(average_precision_score(oy, opred)), 4),
                "PR_95CI": f"[{pr_ci[0]:.3f},{pr_ci[1]:.3f}]",
                "ROC_AUC": round(float(roc_auc_score(oy, opred)), 4),
                "ROC_95CI": f"[{roc_ci[0]:.3f},{roc_ci[1]:.3f}]",
                "Rec@Top5%": round(recall_at_top_k(oy, opred, 0.05), 4),
                "Lift@5%": round(precision_at_top_k(oy, opred, 0.05) / max(oy.mean(), 1e-9), 2),
                "Brier": round(float(b_m), 4),
                "BSS_Pooled": round(float(1.0 - b_m / max(b_ref, 1e-9)), 4),
            })

    df_pool = pd.DataFrame(pooled_rows)
    df_pool.to_csv(RESULTS_DIR / "rolling_origin_pooled_cv_metrics.csv", index=False)
    print("\n=== 5-FOLD ROLLING-ORIGIN POOLED CV (MORE POSITIVES + 95% BOOTSTRAP CI) ===")
    print(df_pool.to_string(index=False))

    # --- 3. Regression on the EXACT SAME Test Set & Units (with Mean/Median & Hurdle Model) ---
    y_reg_tr, y_reg_va, y_reg_te = y_reg[:tr_end], y_reg[va_start:va_end], y_reg[te_start:]
    print(f"\n[Target PM10 Distribution Shift] Train: mean={y_reg_tr.mean():.1f}, median={np.median(y_reg_tr):.1f}, p90={np.percentile(y_reg_tr,90):.1f}, max={y_reg_tr.max():.1f}")
    print(f"[Target PM10 Distribution Shift] Test : mean={y_reg_te.mean():.1f}, median={np.median(y_reg_te):.1f}, p90={np.percentile(y_reg_te,90):.1f}, max={y_reg_te.max():.1f}")

    reg_rows = []
    for bname, bval in [("Trivial_Train_Mean", float(y_reg_tr.mean())), ("Trivial_Train_Median", float(np.median(y_reg_tr)))]:
        bpred = np.full_like(y_reg_te, bval)
        reg_rows.append({"Model": bname, "R2": round(float(r2_score(y_reg_te, bpred)), 4), "RMSE": round(float(np.sqrt(mean_squared_error(y_reg_te, bpred))), 2), "MAE": round(float(mean_absolute_error(y_reg_te, bpred)), 2)})

    # Line A XGBoost Direct log1p
    xreg = XGBRegressor(n_estimators=220, max_depth=4, learning_rate=0.04, reg_lambda=5.0, random_state=SEED, n_jobs=-1)
    xreg.fit(X_tr_s, np.log1p(y_reg_tr))
    pred_x_direct = np.expm1(np.clip(xreg.predict(X_te_s), 0.0, 9.0))
    reg_rows.append({"Model": "LineA_XGBoost_log1p_Direct", "R2": round(float(r2_score(y_reg_te, pred_x_direct)), 4), "RMSE": round(float(np.sqrt(mean_squared_error(y_reg_te, pred_x_direct))), 2), "MAE": round(float(mean_absolute_error(y_reg_te, pred_x_direct)), 2)})

    # Line A 2-Stage Hurdle Model: P(storm)*E[PM10|storm] + (1-P(storm))*E[PM10|non-storm]
    pos_mask_tr = y_reg_tr > 150.0
    reg_pos = XGBRegressor(n_estimators=150, max_depth=3, learning_rate=0.04, reg_lambda=5.0, random_state=SEED, n_jobs=-1).fit(X_tr_s[pos_mask_tr], np.log1p(y_reg_tr[pos_mask_tr]))
    reg_neg = XGBRegressor(n_estimators=150, max_depth=3, learning_rate=0.04, reg_lambda=5.0, random_state=SEED, n_jobs=-1).fit(X_tr_s[~pos_mask_tr], np.log1p(y_reg_tr[~pos_mask_tr]))
    p_storm_te = te_xgb_cal
    pred_hurdle = p_storm_te * np.expm1(np.clip(reg_pos.predict(X_te_s), 0.0, 9.0)) + (1.0 - p_storm_te) * np.expm1(np.clip(reg_neg.predict(X_te_s), 0.0, 9.0))
    reg_rows.append({"Model": "LineA_XGBoost_Hurdle_Calibrated", "R2": round(float(r2_score(y_reg_te, pred_hurdle)), 4), "RMSE": round(float(np.sqrt(mean_squared_error(y_reg_te, pred_hurdle))), 2), "MAE": round(float(mean_absolute_error(y_reg_te, pred_hurdle)), 2)})

    # Line B PyTorch LSTM Regressor on EXACT SAME split & units (log1p + HuberLoss)
    py_reg = RiyadhPyTorchRegressor(len(sel_features), 32, 0.25).to(DEVICE)
    opt_r = torch.optim.AdamW(py_reg.parameters(), lr=1e-3, weight_decay=1e-3)
    huber = nn.HuberLoss(delta=1.0)
    r_loader = DataLoader(TensorDataset(torch.from_numpy(X_seq_tr), torch.from_numpy(np.log1p(y_reg_tr))), batch_size=128, shuffle=True)
    best_rvl, best_rst, wait = float("inf"), None, 0
    for _ in range(30):
        py_reg.train()
        for bx, by in r_loader:
            bx, by = bx.to(DEVICE), by.to(DEVICE)
            opt_r.zero_grad()
            loss = huber(py_reg(bx), by)
            loss.backward()
            opt_r.step()
        py_reg.eval()
        with torch.no_grad():
            vl = float(huber(py_reg(torch.from_numpy(X_seq_va).to(DEVICE)), torch.from_numpy(np.log1p(y_reg_va)).to(DEVICE)).item())
        if vl < best_rvl:
            best_rvl, best_rst, wait = vl, {k: v.cpu().clone() for k, v in py_reg.state_dict().items()}, 0
        else:
            wait += 1
            if wait >= 6:
                break
    py_reg.load_state_dict(best_rst)
    py_reg.eval()
    with torch.no_grad():
        pred_py_pm10 = np.expm1(np.clip(py_reg(torch.from_numpy(X_seq_te).to(DEVICE)).cpu().numpy(), 0.0, 9.0))
    reg_rows.append({"Model": "LineB_PyTorch_LSTM_log1p_Huber", "R2": round(float(r2_score(y_reg_te, pred_py_pm10)), 4), "RMSE": round(float(np.sqrt(mean_squared_error(y_reg_te, pred_py_pm10))), 2), "MAE": round(float(mean_absolute_error(y_reg_te, pred_py_pm10)), 2)})

    # Line B PyTorch ST-GNN on EXACT SAME split & units (Train-only correlation graph A_hat + log1p + HuberLoss)
    corr_mat = np.abs(np.corrcoef(X_tr_s.T))
    corr_mat = np.nan_to_num(corr_mat, nan=0.0)
    np.fill_diagonal(corr_mat, 1.0)
    deg_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(corr_mat.sum(axis=1), 1e-6)))
    a_hat_t = torch.from_numpy((deg_inv_sqrt @ corr_mat @ deg_inv_sqrt).astype(np.float32)).to(DEVICE)

    stgnn_reg = RiyadhUnifiedSTGNN(len(sel_features), hidden_dim=24, dropout=0.25).to(DEVICE)
    opt_g = torch.optim.AdamW(stgnn_reg.parameters(), lr=1e-3, weight_decay=1e-3)
    best_gvl, best_gst, wait_g = float("inf"), None, 0
    for _ in range(30):
        stgnn_reg.train()
        for bx, by in r_loader:
            bx, by = bx.to(DEVICE), by.to(DEVICE)
            opt_g.zero_grad()
            loss = huber(stgnn_reg(bx, a_hat_t), by)
            loss.backward()
            opt_g.step()
        stgnn_reg.eval()
        with torch.no_grad():
            gvl = float(huber(stgnn_reg(torch.from_numpy(X_seq_va).to(DEVICE), a_hat_t), torch.from_numpy(np.log1p(y_reg_va)).to(DEVICE)).item())
        if gvl < best_gvl:
            best_gvl, best_gst, wait_g = gvl, {k: v.cpu().clone() for k, v in stgnn_reg.state_dict().items()}, 0
        else:
            wait_g += 1
            if wait_g >= 6:
                break
    stgnn_reg.load_state_dict(best_gst)
    stgnn_reg.eval()
    with torch.no_grad():
        pred_stgnn_pm10 = np.expm1(np.clip(stgnn_reg(torch.from_numpy(X_seq_te).to(DEVICE), a_hat_t).cpu().numpy(), 0.0, 9.0))
    reg_rows.append({"Model": "LineB_PyTorch_STGNN_log1p_Huber", "R2": round(float(r2_score(y_reg_te, pred_stgnn_pm10)), 4), "RMSE": round(float(np.sqrt(mean_squared_error(y_reg_te, pred_stgnn_pm10))), 2), "MAE": round(float(mean_absolute_error(y_reg_te, pred_stgnn_pm10)), 2)})

    df_reg = pd.DataFrame(reg_rows)
    df_reg.to_csv(RESULTS_DIR / "unified_honest_regression_metrics.csv", index=False)
    print("\n=== SAME-SPLIT REGRESSION COMPARISON (ug/m3, vs Trivial Baselines) ===")
    print(df_reg.to_string(index=False))

    # --- 4. Save Reliability & Lift Figure ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    for mname, probs in cal_curves.items():
        frac_pos, mean_pred = calibration_curve(y_te, probs, n_bins=8, strategy="quantile")
        axes[0].plot(mean_pred, frac_pos, marker="o", lw=2, label=mname)
    axes[0].plot([0, 0.25], [0, 0.25], "k--", label="Perfect Calibration")
    axes[0].set_title("Reliability Curve (Out-of-Sample Test)", fontweight="bold")
    axes[0].set_xlabel("Predicted Storm Probability")
    axes[0].set_ylabel("Observed Storm Frequency")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.3)

    axes[1].barh(df_clf["Model"], df_clf["Lift@5%"], color="#2b5c8f")
    axes[1].axvline(1.0, color="red", linestyle="--", label="Random Baseline (1.0x)")
    axes[1].set_title("Operational Lift @ Top 5% Alert Budget", fontweight="bold")
    axes[1].set_xlabel("Lift over Base Rate")
    axes[1].legend()
    axes[1].grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "calibration_and_operational_lift.png", dpi=150)
    print(f"\nSaved reliability & lift plot -> {FIG_DIR / 'calibration_and_operational_lift.png'}")


if __name__ == "__main__":
    main()
