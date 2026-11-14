"""Export the final winning clean-hourly Line A (.joblib) and Line B PyTorch (.pt) models.

Archives older pre-clean-hourly checkpoints in 05_Models/archive/ and saves the
final clean-hourly models to 05_Models/ and 09_Final_Results/models/.
"""

from pathlib import Path
import random
import shutil
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, root_mean_squared_error
from sklearn.preprocessing import PowerTransformer
from xgboost import XGBClassifier

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
DATA_PATH = ROOT / "06_Data" / "riyadh_hourly_clean_tvt.csv"
NPZ_PATH = ROOT / "06_Data" / "line_b_final_dataset.npz"
ADJ_PATH = ROOT / "06_Data" / "riyadh_graph_adjacency_matrix.npy"

MODELS_DIR = ROOT / "05_Models"
FINAL_MODELS_DIR = ROOT / "09_Final_Results" / "models"


def set_seed(seed: int = 42) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def archive_old_models() -> None:
    arch = MODELS_DIR / "archive"
    arch.mkdir(parents=True, exist_ok=True)
    for sub in ["line_a", "line_b", "meta_model"]:
        src = MODELS_DIR / sub
        dst = arch / sub
        if src.exists():
            dst.mkdir(parents=True, exist_ok=True)
            for f in src.iterdir():
                if f.is_file():
                    shutil.move(str(f), str(dst / f.name))


class RealLSTMNet(nn.Module):
    def __init__(self, in_dim: int, hidden: int = 48):
        super().__init__()
        self.lstm = nn.LSTM(in_dim, hidden, num_layers=2, batch_first=True, dropout=0.2)
        self.head = nn.Sequential(nn.Linear(hidden, 24), nn.ReLU(), nn.Linear(24, 1))

    def forward(self, x):
        o, _ = self.lstm(x)
        return self.head(o[:, -1, :]).squeeze(-1)


class RealTransformerNet(nn.Module):
    def __init__(self, in_dim: int, seq_len: int = 24, d_model: int = 48):
        super().__init__()
        self.proj = nn.Linear(in_dim, d_model)
        self.pos = nn.Parameter(torch.randn(1, seq_len, d_model) * 0.02)
        enc = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=4, dim_feedforward=96, dropout=0.2, batch_first=True
        )
        self.encoder = nn.TransformerEncoder(enc, num_layers=2)
        self.head = nn.Linear(d_model, 1)

    def forward(self, x):
        return self.head(self.encoder(self.proj(x) + self.pos)[:, -1, :]).squeeze(-1)


class RealPINNNet(nn.Module):
    def __init__(self, in_dim: int, hidden: int = 48):
        super().__init__()
        self.gru = nn.GRU(in_dim, hidden, batch_first=True)
        self.head = nn.Sequential(nn.Linear(hidden, 24), nn.SiLU(), nn.Linear(24, 1))

    def forward(self, x):
        o, _ = self.gru(x)
        return self.head(o[:, -1, :]).squeeze(-1)


class MultiModalNPZNet(nn.Module):
    def __init__(self, adj: np.ndarray):
        super().__init__()
        deg = np.sum(adj, axis=1, keepdims=True) + 1e-6
        self.register_buffer("A_norm", torch.tensor(adj / deg, dtype=torch.float32))
        self.nwp_cnn = nn.Sequential(nn.Conv2d(6, 16, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1))
        self.sat_cnn = nn.Sequential(nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(1))
        self.node_lin = nn.Linear(12, 24)
        self.gru = nn.GRU(24, 24, batch_first=True)
        self.head = nn.Sequential(nn.Linear(24 + 16 + 16, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(self, nwp, sat, seq):
        fn = self.nwp_cnn(nwp).flatten(1)
        fs = self.sat_cnn(sat).flatten(1)
        h = torch.relu(self.node_lin(seq))
        hg = torch.einsum("ij,btjf->btif", self.A_norm, h).mean(dim=2)
        fg, _ = self.gru(hg)
        return self.head(torch.cat([fg[:, -1, :], fn, fs], dim=-1)).squeeze(-1)


def main() -> None:
    set_seed(42)
    archive_old_models()

    la_dir = MODELS_DIR / "line_a"
    lb_dir = MODELS_DIR / "line_b"
    la_dir.mkdir(parents=True, exist_ok=True)
    lb_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    df["ts"] = pd.to_datetime(df["ts"])
    target_cols = [c for c in df.columns if c.startswith("target_")]
    feature_cols = [c for c in df.columns if c not in ["ts"] + target_cols]

    n_rows = len(df)
    gap_h, seq_len, stride = 360, 24, 6
    tr_end = int(n_rows * 0.70)
    val_start = tr_end + gap_h
    val_end = int(n_rows * 0.85)
    te_start = val_end + gap_h

    train_df = df.iloc[:tr_end:stride].reset_index(drop=True)
    val_df = df.iloc[val_start:val_end:stride].reset_index(drop=True)
    test_df = df.iloc[te_start::stride].reset_index(drop=True)

    imp = SimpleImputer(strategy="median")
    pt = PowerTransformer(method="yeo-johnson")
    X_tr = pt.fit_transform(imp.fit_transform(train_df[feature_cols].values))
    X_va = pt.transform(imp.transform(val_df[feature_cols].values))
    X_te = pt.transform(imp.transform(test_df[feature_cols].values))

    joblib.dump(
        {"imputer": imp, "power_transformer": pt, "feature_cols": feature_cols},
        la_dir / "clean_hourly_preprocessor.joblib",
    )

    # 1. Line A winning calibrated classifiers per horizon
    la_winners = {
        24: "RandomForest_Cal",
        72: "RandomForest_Cal",
        168: "RandomForest_Cal",
        216: "XGBoost_Cal",
        360: "XGBoost_Cal",
    }
    for h, mname in la_winners.items():
        y_tr = train_df[f"target_evt_any_{h}h"].values.astype(int)
        y_va = val_df[f"target_evt_any_{h}h"].values.astype(int)
        y_te = test_df[f"target_evt_any_{h}h"].values.astype(int)
        if mname.startswith("RandomForest"):
            clf = RandomForestClassifier(
                n_estimators=100, max_depth=8, min_samples_leaf=8,
                class_weight="balanced", random_state=42, n_jobs=-1,
            ).fit(X_tr, y_tr)
        else:
            pw = float(np.sum(y_tr == 0) / max(1, np.sum(y_tr == 1)))
            clf = XGBClassifier(
                n_estimators=120, max_depth=4, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, scale_pos_weight=pw,
                reg_lambda=2.0, random_state=42, n_jobs=-1, eval_metric="logloss",
            ).fit(X_tr, y_tr)
        va_p = clf.predict_proba(X_va)[:, 1]
        te_p = clf.predict_proba(X_te)[:, 1]
        cal = LogisticRegression(C=1.0, max_iter=1000).fit(va_p.reshape(-1, 1), y_va)
        roc = roc_auc_score(y_te, cal.predict_proba(te_p.reshape(-1, 1))[:, 1])
        out_path = la_dir / f"line_a_{mname.lower()}_{h}h.joblib"
        joblib.dump({"model": clf, "platt_calibrator": cal, "horizon_h": h, "test_roc_seed42": roc}, out_path)
        print(f"Saved {out_path.name} (Test ROC={roc:.4f})")

    # 2. Line B PyTorch winning models
    X_all_s = pt.transform(imp.transform(df[feature_cols].values))
    tr_idx = np.arange(seq_len, tr_end, stride)
    va_idx = np.arange(val_start, val_end, stride)
    te_idx = np.arange(te_start, n_rows, stride)

    def make_seq(indices):
        return np.array([X_all_s[i - seq_len + 1 : i + 1] for i in indices], dtype=np.float32)

    X_tr_seq, X_va_seq, X_te_seq = make_seq(tr_idx), make_seq(va_idx), make_seq(te_idx)
    wind_idx = feature_cols.index("era5_wind_speed_10m")

    lb_cls_winners = {
        24: ("LineB_PINN", lambda: RealPINNNet(len(feature_cols)), True),
        72: ("LineB_Transformer", lambda: RealTransformerNet(len(feature_cols), seq_len), False),
        168: ("LineB_PINN", lambda: RealPINNNet(len(feature_cols)), True),
        216: ("LineB_Transformer", lambda: RealTransformerNet(len(feature_cols), seq_len), False),
        360: ("LineB_Transformer", lambda: RealTransformerNet(len(feature_cols), seq_len), False),
    }
    for h, (mname, ctor, is_pinn) in lb_cls_winners.items():
        set_seed(42)
        y_tr = df.iloc[tr_idx][f"target_evt_any_{h}h"].values.astype(int)
        y_va = df.iloc[va_idx][f"target_evt_any_{h}h"].values.astype(int)
        y_te = df.iloc[te_idx][f"target_evt_any_{h}h"].values.astype(int)
        mdl = ctor()
        pw = torch.tensor([float(np.sum(y_tr == 0) / max(1, np.sum(y_tr == 1)))], dtype=torch.float32)
        crit = nn.BCEWithLogitsLoss(pos_weight=pw)
        opt = torch.optim.AdamW(mdl.parameters(), lr=1.5e-3, weight_decay=1e-3)
        gen = torch.Generator().manual_seed(42)
        dl = DataLoader(TensorDataset(torch.tensor(X_tr_seq), torch.tensor(y_tr, dtype=torch.float32)),
                        batch_size=128, shuffle=True, generator=gen)
        best_vl, best_sd = 1e9, None
        for _ in range(12):
            mdl.train()
            for bx, by in dl:
                opt.zero_grad()
                lg = mdl(bx)
                loss = crit(lg, by)
                if is_pinn:
                    bxp = bx.clone()
                    bxp[:, -1, wind_idx] += 0.5
                    loss = loss + 0.05 * torch.mean(torch.relu(lg - mdl(bxp)))
                loss.backward()
                torch.nn.utils.clip_grad_norm_(mdl.parameters(), 1.0)
                opt.step()
            mdl.eval()
            with torch.no_grad():
                vl = float(crit(mdl(torch.tensor(X_va_seq)), torch.tensor(y_va, dtype=torch.float32)).item())
            if vl < best_vl:
                best_vl = vl
                best_sd = {k: v.clone() for k, v in mdl.state_dict().items()}
        if best_sd:
            mdl.load_state_dict(best_sd)
        mdl.eval()
        with torch.no_grad():
            vs = mdl(torch.tensor(X_va_seq)).numpy()
            ts = mdl(torch.tensor(X_te_seq)).numpy()
        cal = LogisticRegression(C=1.0, max_iter=1000).fit(np.clip(vs, -30, 30).reshape(-1, 1), y_va)
        tp = cal.predict_proba(np.clip(ts, -30, 30).reshape(-1, 1))[:, 1]
        roc = roc_auc_score(y_te, tp)
        out_path = lb_dir / f"{mname.lower()}_{h}h_cls.pt"
        torch.save(
            {"state_dict": mdl.state_dict(), "platt_calibrator": cal, "horizon_h": h, "in_dim": len(feature_cols), "test_roc_seed42": roc},
            out_path,
        )
        print(f"Saved {out_path.name} (Test ROC={roc:.4f})")

    # 3. LineB_LSTM 360h Regressor (beat Trivial_Median)
    set_seed(42)
    y_tr = np.log1p(np.maximum(df.iloc[tr_idx]["target_avg_pm10_360h"].values, 0)).astype(np.float32)
    y_va = np.log1p(np.maximum(df.iloc[va_idx]["target_avg_pm10_360h"].values, 0)).astype(np.float32)
    y_te = df.iloc[te_idx]["target_avg_pm10_360h"].values
    lstm_reg = RealLSTMNet(len(feature_cols))
    crit = nn.L1Loss()
    opt = torch.optim.AdamW(lstm_reg.parameters(), lr=1.5e-3, weight_decay=1e-3)
    gen = torch.Generator().manual_seed(42)
    dl = DataLoader(TensorDataset(torch.tensor(X_tr_seq), torch.tensor(y_tr)), batch_size=128, shuffle=True, generator=gen)
    best_vl, best_sd = 1e9, None
    for _ in range(12):
        lstm_reg.train()
        for bx, by in dl:
            opt.zero_grad()
            crit(lstm_reg(bx), by).backward()
            torch.nn.utils.clip_grad_norm_(lstm_reg.parameters(), 1.0)
            opt.step()
        lstm_reg.eval()
        with torch.no_grad():
            vl = float(crit(lstm_reg(torch.tensor(X_va_seq)), torch.tensor(y_va)).item())
        if vl < best_vl:
            best_vl = vl
            best_sd = {k: v.clone() for k, v in lstm_reg.state_dict().items()}
    if best_sd:
        lstm_reg.load_state_dict(best_sd)
    lstm_reg.eval()
    with torch.no_grad():
        pred = np.expm1(np.clip(lstm_reg(torch.tensor(X_te_seq)).numpy(), 0, 10))
    rmse = root_mean_squared_error(y_te, pred)
    out_reg = lb_dir / "lineb_lstm_360h_reg.pt"
    torch.save({"state_dict": lstm_reg.state_dict(), "horizon_h": 360, "in_dim": len(feature_cols), "test_rmse_seed42": rmse}, out_reg)
    print(f"Saved {out_reg.name} (Test RMSE={rmse:.2f})")

    # 4. MultiModalNPZNet on line_b_final_dataset.npz
    set_seed(42)
    npz = np.load(NPZ_PATH, allow_pickle=True)
    n_npz = len(npz["seq_features"])
    t1, t2 = int(n_npz * 0.70), int(n_npz * 0.85)
    nwp_t = torch.tensor(npz["nwp_grid"])
    sat_t = torch.tensor(npz["satellite_grid"])
    seq_t = torch.tensor(npz["seq_features"])
    y_npz = torch.tensor(np.log1p(np.maximum(npz["targets_pm10"][:, 0, 0], 0)), dtype=torch.float32)
    mm_mdl = MultiModalNPZNet(npz["adjacency_matrix"])
    opt = torch.optim.AdamW(mm_mdl.parameters(), lr=2e-3)
    crit = nn.L1Loss()
    dl_npz = DataLoader(TensorDataset(nwp_t[:t1], sat_t[:t1], seq_t[:t1], y_npz[:t1]), batch_size=32, shuffle=True)
    for _ in range(25):
        mm_mdl.train()
        for bn, bs, bq, by in dl_npz:
            opt.zero_grad()
            crit(mm_mdl(bn, bs, bq), by).backward()
            opt.step()
    mm_mdl.eval()
    out_mm = lb_dir / "multimodal_npz_net.pt"
    torch.save({"state_dict": mm_mdl.state_dict()}, out_mm)
    print(f"Saved {out_mm.name}")

    # Copy active 05_Models/{line_a, line_b} to 09_Final_Results/models/
    if FINAL_MODELS_DIR.exists():
        shutil.rmtree(FINAL_MODELS_DIR)
    shutil.copytree(la_dir, FINAL_MODELS_DIR / "line_a")
    shutil.copytree(lb_dir, FINAL_MODELS_DIR / "line_b")
    print(f"Copied final models to {FINAL_MODELS_DIR}")


if __name__ == "__main__":
    main()

