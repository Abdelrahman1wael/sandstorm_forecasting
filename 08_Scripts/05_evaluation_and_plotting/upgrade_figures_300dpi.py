from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import MaxNLocator

ROOT = Path(r"c:\Users\hp\Desktop\sandstorm_forecasting")
RES_DIR = ROOT / "06_Data" / "results"
DATA_DIR = ROOT / "06_Data" / "data"
FIG_DIR = ROOT / "07_Figures"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial"],
    "font.size": 10,
    "axes.titlesize": 11.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8.5,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
    "#9467bd", "#8c564b", "#e377c2", "#17becf",
]


def save(fig, name):
    out = FIG_DIR / name
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {out.name}")


def plot_diurnal_and_windrose():
    df = pd.read_csv(
        DATA_DIR / "riyadh_hourly_clean_tvt.csv",
        usecols=["ts", "is_dust_event", "era5_wind_speed_10m", "drct"],
    )
    df["ts"] = pd.to_datetime(df["ts"])
    df["hour"] = df["ts"].dt.hour

    # 1. nb00_fig07.png: Hourly Diurnal Cycle (UTC)
    hr = df.groupby("hour").agg(
        dust=("is_dust_event", lambda s: s.mean() * 100.0),
        ws=("era5_wind_speed_10m", "mean"),
    )
    fig, ax1 = plt.subplots(figsize=(9.2, 3.8))
    bars = ax1.bar(hr.index, hr["dust"], color="#4C8CBF", alpha=0.72, label="Dust-Event Frequency (%)")
    ax1.set_xlabel("Hour of Day (UTC; Riyadh Local Time = UTC + 3 h)")
    ax1.set_ylabel("Dust-Event Frequency (%)", color="#1f4e78", fontweight="bold")
    ax1.tick_params(axis="y", labelcolor="#1f4e78")
    ax1.set_xticks(range(0, 24, 2))
    ax1.grid(axis="y", alpha=0.25, linestyle="--")

    ax2 = ax1.twinx()
    line = ax2.plot(hr.index, hr["ws"], color="#d62728", marker="o", lw=2.0, ms=5, label="Mean ERA5 10 m Wind Speed (km/h)")
    ax2.set_ylabel("Mean ERA5 10 m Wind Speed (km/h)", color="#b22222", fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#b22222")

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left", frameon=True, framealpha=0.92)
    ax1.set_title("Hourly Diurnal Cycle of Dust-Event Frequency and ERA5 10 m Wind Speed (UTC)")
    fig.tight_layout()
    save(fig, "nb00_fig07.png")

    # 2. nb00_fig09.png: Hourly Wind Rose (no overlapping radial labels & legend)
    ang = np.deg2rad(df["drct"].dropna())
    dang = np.deg2rad(df.loc[df["is_dust_event"] == 1, "drct"].dropna())
    fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(5.8, 5.4))
    ax.hist(ang, bins=24, density=True, alpha=0.45, color="#4C8CBF", label="All Hours (n = 86,928)")
    ax.hist(dang, bins=24, density=True, alpha=0.65, color="#e63946", label="Dust Hours (n = 5,745)")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(67.5)
    ax.set_thetagrids([0, 45, 90, 135, 180, 225, 270, 315],
                      ["N (0°)", "NE (45°)", "E (90°)", "SE (135°)", "S (180°)", "SW (225°)", "W (270°)", "NW (315°)"])
    ax.tick_params(axis="y", labelsize=8.5)
    ax.set_title("Hourly Surface Wind Rose at OERK (Shamal Corridor)", pad=16)
    ax.legend(loc="upper left", bbox_to_anchor=(0.82, 1.12), frameon=True, framealpha=0.95)
    fig.tight_layout()
    save(fig, "nb00_fig09.png")


def plot_line_a():
    cv_df = pd.read_csv(RES_DIR / "nb02_line_a_5fold_cv_hourly.csv")
    cls_df = pd.read_csv(RES_DIR / "nb02_line_a_classification_hourly.csv")
    reg_df = pd.read_csv(RES_DIR / "nb02_line_a_regression_hourly.csv")
    horizons = sorted(cls_df["Days"].unique())

    # nb02_fig01.png: 5-fold CV ROC-AUC
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    for i, m in enumerate(cv_df["Model"].unique()):
        sub = cv_df[cv_df["Model"] == m].sort_values("Days")
        ax.plot(sub["Days"], sub["CV_ROC"], marker="o", lw=2.0, ms=5.5, color=PALETTE[i % len(PALETTE)], label=m)
    ax.set_xticks(horizons)
    ax.set_xlabel("Forecast Horizon (days)")
    ax.set_ylabel("5-Fold Rolling-Origin CV ROC-AUC")
    ax.set_title("Main Line A: 5-Fold Rolling-Origin CV ROC-AUC Across Horizons (1–15 Days)")
    ax.grid(alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(ncol=2, frameon=True, loc="upper right")
    fig.tight_layout()
    save(fig, "nb02_fig01.png")

    # nb02_fig02.png: Validation vs Test ROC-AUC
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.1), sharey=False)
    for i, m in enumerate(cls_df["Model"].unique()):
        sub = cls_df[cls_df["Model"] == m].sort_values("Days")
        c = PALETTE[i % len(PALETTE)]
        axes[0].plot(sub["Days"], sub["Val_ROC"], marker="o", lw=1.9, ms=5.5, color=c, label=m)
        axes[1].plot(sub["Days"], sub["Test_ROC"], marker="s", lw=1.9, ms=5.5, color=c, label=m)
    axes[0].set_title("Validation Partition (2 Jan 2022 – 14 Jun 2023)")
    axes[1].set_title("Out-of-Sample Test Partition (29 Jun 2023 – 8 Dec 2024)")
    for ax in axes:
        ax.set_xticks(horizons)
        ax.set_xlabel("Forecast Horizon (days)")
        ax.set_ylabel("ROC-AUC")
        ax.grid(alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(fontsize=8, frameon=True, loc="lower left")
    fig.tight_layout()
    save(fig, "nb02_fig02.png")

    # nb02_fig03.png: Test PR-AUC and BSS
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.1))
    for i, m in enumerate(cls_df["Model"].unique()):
        sub = cls_df[cls_df["Model"] == m].sort_values("Days")
        c = PALETTE[i % len(PALETTE)]
        axes[0].plot(sub["Days"], sub["Test_PR"], marker="o", lw=1.9, ms=5.5, color=c, label=m)
        axes[1].plot(sub["Days"], sub["BSS"], marker="s", lw=1.9, ms=5.5, color=c, label=m)
    axes[0].set_title("Main Line A: Test PR-AUC")
    axes[0].set_ylabel("Test PR-AUC")
    axes[1].set_title("Main Line A: Test Brier Skill Score (BSS)")
    axes[1].set_ylabel("Brier Skill Score (BSS)")
    axes[1].axhline(0.0, color="black", lw=1.0, ls="--", alpha=0.6)
    for ax in axes:
        ax.set_xticks(horizons)
        ax.set_xlabel("Forecast Horizon (days)")
        ax.grid(alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(fontsize=8, frameon=True, loc="best")
    fig.tight_layout()
    save(fig, "nb02_fig03.png")

    # nb02_fig06.png: Regression RMSE & R2 (excluding extreme Persistence/MonthClimo lines for readability, or keeping all non-trivial + Trivial_Median)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.1))
    keep_models = [m for m in reg_df["Model"].unique() if m not in ("Persistence", "MonthClimo")]
    for i, m in enumerate(keep_models):
        sub = reg_df[reg_df["Model"] == m].sort_values("Days")
        c = PALETTE[i % len(PALETTE)]
        ls = "--" if m == "Trivial_Median" else "-"
        axes[0].plot(sub["Days"], sub["RMSE"], marker="o", lw=1.9, ls=ls, ms=5.2, color=c, label=m)
        axes[1].plot(sub["Days"], sub["R2"], marker="s", lw=1.9, ls=ls, ms=5.2, color=c, label=m)
    axes[0].set_title("Main Line A: Continuous PM₁₀ Test RMSE")
    axes[0].set_ylabel("Test RMSE (µg/m³)")
    axes[1].set_title("Main Line A: Continuous PM₁₀ Test R²")
    axes[1].set_ylabel("Test R²")
    axes[1].axhline(0.0, color="black", lw=1.0, ls="--", alpha=0.6)
    for ax in axes:
        ax.set_xticks(horizons)
        ax.set_xlabel("Forecast Horizon (days)")
        ax.grid(alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(fontsize=8, frameon=True, loc="best")
    fig.tight_layout()
    save(fig, "nb02_fig06.png")

    # nb02_fig07.png: Operational Lift@Top10%
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    for i, m in enumerate(cls_df["Model"].unique()):
        sub = cls_df[cls_df["Model"] == m].sort_values("Days")
        ax.plot(sub["Days"], sub["Lift10"], marker="o", lw=2.0, ms=5.5, color=PALETTE[i % len(PALETTE)], label=m)
    ax.axhline(1.0, color="black", lw=1.0, ls="--", alpha=0.6, label="Random Baseline (1.0x)")
    ax.set_xticks(horizons)
    ax.set_xlabel("Forecast Horizon (days)")
    ax.set_ylabel("Lift@Top10% (× Base Rate)")
    ax.set_title("Main Line A: Operational Lift@Top10% Across 1–15 Day Horizons")
    ax.grid(alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(ncol=2, frameon=True, loc="best")
    fig.tight_layout()
    save(fig, "nb02_fig07.png")


def plot_line_b_and_cross():
    cls_a = pd.read_csv(RES_DIR / "nb02_line_a_classification_hourly.csv")
    reg_a = pd.read_csv(RES_DIR / "nb02_line_a_regression_hourly.csv")
    cls_b = pd.read_csv(RES_DIR / "nb03_line_b_classification_hourly.csv")
    reg_b = pd.read_csv(RES_DIR / "nb03_line_b_regression_hourly.csv")
    horizons = sorted(cls_b["Days"].unique())

    # nb03_fig03.png: Line B Test ROC-AUC and BSS
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.1))
    for i, m in enumerate(cls_b["Model"].unique()):
        sub = cls_b[cls_b["Model"] == m].sort_values("Days")
        c = PALETTE[i % len(PALETTE)]
        axes[0].plot(sub["Days"], sub["Test_ROC"], marker="o", lw=2.0, ms=5.8, color=c, label=m)
        axes[1].plot(sub["Days"], sub["BSS"], marker="s", lw=2.0, ms=5.8, color=c, label=m)
    axes[0].set_title("Main Line B: Test ROC-AUC (3-Seed Mean)")
    axes[0].set_ylabel("Test ROC-AUC")
    axes[1].set_title("Main Line B: Test Brier Skill Score (BSS)")
    axes[1].set_ylabel("Brier Skill Score (BSS)")
    axes[1].axhline(0.0, color="black", lw=1.0, ls="--", alpha=0.6)
    for ax in axes:
        ax.set_xticks(horizons)
        ax.set_xlabel("Forecast Horizon (days)")
        ax.grid(alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(frameon=True, loc="best")
    fig.tight_layout()
    save(fig, "nb03_fig03.png")

    # nb03_fig04.png: Line B Regression Test RMSE and R2
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.1))
    for i, m in enumerate(reg_b["Model"].unique()):
        sub = reg_b[reg_b["Model"] == m].sort_values("Days")
        c = PALETTE[i % len(PALETTE)]
        axes[0].plot(sub["Days"], sub["RMSE"], marker="o", lw=2.0, ms=5.8, color=c, label=m)
        axes[1].plot(sub["Days"], sub["R2"], marker="s", lw=2.0, ms=5.8, color=c, label=m)
    axes[0].set_title("Main Line B: Continuous PM₁₀ Test RMSE")
    axes[0].set_ylabel("Test RMSE (µg/m³)")
    axes[1].set_title("Main Line B: Continuous PM₁₀ Test R²")
    axes[1].set_ylabel("Test R²")
    axes[1].axhline(0.0, color="black", lw=1.0, ls="--", alpha=0.6)
    for ax in axes:
        ax.set_xticks(horizons)
        ax.set_xlabel("Forecast Horizon (days)")
        ax.grid(alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(frameon=True, loc="best")
    fig.tight_layout()
    save(fig, "nb03_fig04.png")

    # nb03_fig05.png: Cross-Line Comparison
    best_roc_a = cls_a.groupby("Days")["Test_ROC"].max().reindex(horizons)
    best_roc_b = cls_b.groupby("Days")["Test_ROC"].max().reindex(horizons)
    best_rmse_a = reg_a.groupby("Days")["RMSE"].min().reindex(horizons)
    best_rmse_b = reg_b.groupby("Days")["RMSE"].min().reindex(horizons)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.0))
    axes[0].plot(horizons, best_roc_a, marker="o", lw=2.2, ms=6, color="#1f77b4", label="Main Line A (Calibrated Tabular)")
    axes[0].plot(horizons, best_roc_b, marker="s", lw=2.2, ms=6, color="#ff7f0e", label="Main Line B (PyTorch Deep Sequence)")
    axes[0].set_title("Best Test ROC-AUC Across Horizons (1–15 Days)")
    axes[0].set_ylabel("Best Test ROC-AUC")

    axes[1].plot(horizons, best_rmse_a, marker="o", lw=2.2, ms=6, color="#1f77b4", label="Main Line A (Calibrated Tabular)")
    axes[1].plot(horizons, best_rmse_b, marker="s", lw=2.2, ms=6, color="#ff7f0e", label="Main Line B (PyTorch Deep Sequence)")
    axes[1].set_title("Best Test PM₁₀ RMSE Across Horizons (1–15 Days)")
    axes[1].set_ylabel("Best Test RMSE (µg/m³)")

    for ax in axes:
        ax.set_xticks(horizons)
        ax.set_xlabel("Forecast Horizon (days)")
        ax.grid(alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(frameon=True, loc="best")
    fig.tight_layout()
    save(fig, "nb03_fig05.png")


def plot_xai_summary():
    xai_df = pd.read_csv(RES_DIR / "nb04_xai_clean_hourly_importance.csv")
    t12 = xai_df.head(12).iloc[::-1]

    # nb04_fig01.png: Global SHAP vs ExtraTrees Permutation ROC Drop (fix overlapping ticks!)
    fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.8))
    axes[0].barh(t12["Feature"], t12["Mean_Abs_SHAP"], color="#1f77b4", alpha=0.88)
    axes[0].set_title("XAI-1: Global SHAP Mean |Impact| (168 h)")
    axes[0].set_xlabel("Mean |SHAP Value| (log-odds impact)")
    axes[0].grid(axis="x", alpha=0.25, linestyle="--")
    axes[0].spines["top"].set_visible(False)
    axes[0].spines["right"].set_visible(False)

    axes[1].barh(t12["Feature"], t12["ET_Perm_ROC"], color="#2ca02c", alpha=0.88)
    axes[1].axvline(0.0, color="black", lw=0.8)
    axes[1].set_title("XAI-2: ExtraTrees Test Permutation ROC-AUC Drop")
    axes[1].set_xlabel("Test ROC-AUC Drop on Feature Permutation")
    axes[1].xaxis.set_major_locator(MaxNLocator(nbins=6))
    axes[1].grid(axis="x", alpha=0.25, linestyle="--")
    axes[1].spines["top"].set_visible(False)
    axes[1].spines["right"].set_visible(False)
    fig.tight_layout()
    save(fig, "nb04_fig01.png")

    # nb04_fig03.png: Modality-Level SHAP Attribution Share (%)
    def grp(f):
        if "era5" in f or "phys" in f or "sp_" in f or "t2m_" in f or "ws_" in f or "dryness" in f:
            return "ERA5_Physics"
        if "sat_" in f or "aod" in f:
            return "Satellite_Detrended"
        if "cams" in f or "nwp" in f:
            return "CAMS_NWP_Detrended"
        if "doy" in f or "hour" in f:
            return "Calendar_Diurnal"
        return "Ground_METAR"

    xai_df["Modality"] = [grp(f) for f in xai_df["Feature"]]
    mod_share = (xai_df.groupby("Modality")["Mean_Abs_SHAP"].sum())
    mod_share = (mod_share / mod_share.sum() * 100.0).sort_values()

    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    bars = ax.barh(mod_share.index, mod_share.values, color="#8856a7", alpha=0.9)
    for bar, val in zip(bars, mod_share.values):
        ax.text(val + 0.6, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%", va="center", fontsize=9.5, fontweight="bold")
    ax.set_xlim(0, mod_share.max() * 1.18)
    ax.set_xlabel("Share of Total Mean |SHAP| Attribution (%)")
    ax.set_ylabel("Observation Modality")
    ax.set_title("Modality-Level SHAP Attribution Share (%) at 168 h Horizon")
    ax.grid(axis="x", alpha=0.25, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    save(fig, "nb04_fig03.png")


def plot_fig3_9_domain_and_architecture():
    fig, (ax_map, ax_arch) = plt.subplots(1, 2, figsize=(13.2, 5.8), gridspec_kw={"width_ratios": [1.02, 1.15]})

    # Panel (a): Clean 6-Node Spatiotemporal Graph Domain
    nodes = [
        {"id": 0, "name": "Node 0: OERK (King Khalid Airport)", "lat": 24.96, "lon": 46.70, "color": "#d62728", "dx": -3.10, "dy": 0.85},
        {"id": 1, "name": "Node 1: Central Riyadh / Solar Village", "lat": 24.91, "lon": 46.41, "color": "#1f77b4", "dx": -2.70, "dy": -0.95},
        {"id": 2, "name": "Node 2: OERY (Riyadh Air Base)", "lat": 24.71, "lon": 46.73, "color": "#ff7f0e", "dx": 0.65, "dy": -0.95},
        {"id": 3, "name": "Node 3: Qassim Upwind (NW)", "lat": 26.30, "lon": 43.91, "color": "#2ca02c", "dx": 0.45, "dy": 0.45},
        {"id": 4, "name": "Node 4: Al Ahsa Corridor (E)", "lat": 25.29, "lon": 49.49, "color": "#9467bd", "dx": -2.05, "dy": -0.78},
        {"id": 5, "name": "Node 5: Wadi Ad-Dawasir (S)", "lat": 20.50, "lon": 44.80, "color": "#e377c2", "dx": 0.55, "dy": 0.15},
    ]

    # Graph edges connecting upwind corridors to Riyadh core
    core_lons = [46.70, 46.41, 46.73]
    core_lats = [24.96, 24.91, 24.71]
    for n in nodes[3:]:
        ax_map.plot([n["lon"], 46.61], [n["lat"], 24.86], ls="--", lw=1.1, color="#9aa5b1", zorder=1)
    for i in range(3):
        j = (i + 1) % 3
        ax_map.plot([nodes[i]["lon"], nodes[j]["lon"]], [nodes[i]["lat"], nodes[j]["lat"]], lw=1.4, color="#5c6f84", zorder=2)

    # Shamal NW-to-SE corridor arrow
    ax_map.annotate(
        "",
        xy=(46.25, 25.05),
        xytext=(44.35, 26.05),
        arrowprops=dict(arrowstyle="->,head_width=0.45,head_length=0.55", lw=2.8, color="#b22222", alpha=0.75),
        zorder=3,
    )
    ax_map.text(44.55, 25.20, "Prevailing Shamal\n(NW → SE Flux)", color="#9b1c1c", fontsize=8.5, fontweight="bold", ha="center")

    for n in nodes:
        ax_map.scatter(n["lon"], n["lat"], s=115, color=n["color"], edgecolors="black", linewidth=1.1, zorder=5)
        ax_map.annotate(
            n["name"],
            xy=(n["lon"], n["lat"]),
            xytext=(n["lon"] + n["dx"], n["lat"] + n["dy"]),
            fontsize=8.2,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=n["color"], lw=1.1, alpha=0.95),
            arrowprops=dict(arrowstyle="-", color=n["color"], lw=1.0, shrinkA=0, shrinkB=4),
            zorder=6,
        )

    ax_map.set_xlim(43.0, 50.4)
    ax_map.set_ylim(19.8, 27.3)
    ax_map.set_xlabel("Longitude (°E)")
    ax_map.set_ylabel("Latitude (°N)")
    ax_map.set_title("(a) Greater Riyadh 6-Node Spatiotemporal Domain")
    ax_map.grid(alpha=0.28, linestyle="--")

    # Panel (b): Clean Vector Dual-Pipeline Architecture Diagram
    ax_arch.axis("off")
    ax_arch.set_xlim(0, 10)
    ax_arch.set_ylim(0, 10)
    ax_arch.set_title("(b) Leakage-Free Dual-Pipeline & XAI Architecture")

    def draw_box(x, y, w, h, title, body, fc="#f8fafc", ec="#334155", title_c="#0f172a", title_fs=8.5, body_fs=7.6):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.14,rounding_size=0.18", fc=fc, ec=ec, lw=1.4)
        ax_arch.add_patch(box)
        ax_arch.text(x + w / 2, y + h - 0.30, title, ha="center", va="top", fontsize=title_fs, fontweight="bold", color=title_c)
        ax_arch.text(x + w / 2, y + h / 2 - 0.18, body, ha="center", va="center", fontsize=body_fs, color="#1e293b", linespacing=1.32)

    draw_box(
        0.3, 7.65, 9.4, 1.95,
        "1. Aligned Multimodal Hourly Dataset (86,928 h | 2015–2024 | 115 Clean Features)",
        "• Ground_METAR (OERK, OERY, OEGS, OEAH, OEWD; dust memory)   • ERA5_Physics (winds, BLH, soil moisture, VPD)\n"
        "• Calendar_Diurnal (sin/cos DOY & UTC hour)   • Satellite_Detrended & CAMS_NWP_Detrended",
        fc="#eff6ff", ec="#2563eb", title_c="#1e40af"
    )
    draw_box(
        0.3, 5.20, 9.4, 1.85,
        "2. Strict Causal Split & Train-Only Preprocessing (No Leakage / No SMOTE)",
        "70% Train (9 Jan 2015–18 Dec 2021; 10,142 6h) ─[15d / 360h Purge]→ 15% Val (2,114 6h) ─[15d Purge]→ 15% Test (2,114 6h)\n"
        "Train-only De-censoring (53.7 µg/m³ floor), Yeo-Johnson Power Transform & Cost-Sensitive Class Weighting",
        fc="#f0fdf4", ec="#16a34a", title_c="#166534"
    )
    draw_box(
        0.3, 2.35, 4.45, 2.25,
        "3A. Main Line A (Tabular)",
        "• LogReg_Bal_Cal, RandomForest_Cal,\n  ExtraTrees_Cal, HistGB_Cal, XGBoost_Cal\n"
        "• Validation-set Platt Calibration\n"
        "• Ridge Continuous PM₁₀ Regression\n"
        "• Horizons H ∈ {24, 72, 168, 216, 360} h",
        fc="#fff7ed", ec="#ea580c", title_c="#9a3412", title_fs=8.3, body_fs=7.3
    )
    draw_box(
        5.25, 2.35, 4.45, 2.25,
        "3B. Main Line B (PyTorch)",
        "• LineB_LSTM (24 h causal lookback)\n"
        "• LineB_Transformer (2-layer encoder)\n"
        "• LineB_PINN (monotone gust/dryness reg.)\n"
        "• Multi-seed evaluation (3 random seeds)\n"
        "• Horizons H ∈ {24, 72, 168, 216, 360} h",
        fc="#faf5ff", ec="#9333ea", title_c="#6b21a8", title_fs=8.3, body_fs=7.3
    )
    draw_box(
        0.3, 0.25, 9.4, 1.50,
        "4. Six-Module Explainable AI Audit & Operational Translation (XAI-1 to XAI-6)",
        "Global/Local SHAP • Permutation ROC Drop • 1D/2D PDP-ICE • Surrogate Tree • LSTM Saliency • 4-Tier Riyadh Action Matrix",
        fc="#f8fafc", ec="#475569", title_c="#0f172a"
    )

    arrow_kw = dict(arrowstyle="-|>,head_width=0.28,head_length=0.4", lw=1.5, color="#475569")
    ax_arch.annotate("", xy=(5.0, 7.08), xytext=(5.0, 7.62), arrowprops=arrow_kw)
    ax_arch.annotate("", xy=(2.55, 4.63), xytext=(3.6, 5.18), arrowprops=arrow_kw)
    ax_arch.annotate("", xy=(7.45, 4.63), xytext=(6.4, 5.18), arrowprops=arrow_kw)
    ax_arch.annotate("", xy=(2.55, 1.78), xytext=(2.55, 2.32), arrowprops=arrow_kw)
    ax_arch.annotate("", xy=(7.45, 1.78), xytext=(7.45, 2.32), arrowprops=arrow_kw)

    fig.tight_layout()
    save(fig, "fig3_9_domain_architecture.png")


def main():
    plot_diurnal_and_windrose()
    plot_line_a()
    plot_line_b_and_cross()
    plot_xai_summary()
    plot_fig3_9_domain_and_architecture()
    print("All 13 figures upgraded to 300 DPI successfully.")


if __name__ == "__main__":
    main()
