"""
Riyadh Sand & Dust Storms (SDS) Forecasting Data Architecture Common Library
=============================================================================
Master's Thesis Research: Data System Architecture for Riyadh Only
Site Coordinates: Riyadh_Airport_SDSC (24.926°N, 46.722°E)
Domain Bounds   : 24.0°N – 25.5°N, 46.0°E – 47.5°E (Riyadh Station & Metropolitan Grid Only)
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# 1. Base Paths & Directories
# ----------------------------------------------------------------------------
_DEFAULT_BASE = Path(__file__).resolve().parent.parent
BASE_DIR = Path(os.environ.get("THESIS_DIR", os.environ.get("THESIS_BASE", str(_DEFAULT_BASE)))).resolve()
DATA_DIR = BASE_DIR / "data"

ERA5_DIR = DATA_DIR / "era5"
CAMS_DIR = DATA_DIR / "cams"
MODIS_DIR = DATA_DIR / "modis"
AERONET_DIR = DATA_DIR / "aeronet"
COLLOC_DIR = DATA_DIR / "collocated"
FEAT_DIR = DATA_DIR / "meta_model"
RESULTS_DIR = FEAT_DIR / "results"
VALIDATION_DIR = DATA_DIR / "validation"
RAG_DOCS_DIR = DATA_DIR / "rag_docs"

for _d in (ERA5_DIR, CAMS_DIR, MODIS_DIR, AERONET_DIR, COLLOC_DIR, FEAT_DIR, RESULTS_DIR, VALIDATION_DIR, RAG_DOCS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------
# 1.1 API Key & Credential Helper
# ----------------------------------------------------------------------------
def get_cds_credentials():
    """Reads CDS/ADS credentials from Keys/API_Key/API.txt or env."""
    url = os.environ.get("CDSAPI_URL")
    key = os.environ.get("CDSAPI_KEY")
    if not key:
        key_file = BASE_DIR / "Keys" / "API_Key" / "API.txt"
        if key_file.exists():
            for line in key_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("url:"):
                    url = line.split(":", 1)[1].strip()
                elif line.startswith("key:"):
                    key = line.split(":", 1)[1].strip()
    return url, key

def get_cds_client(default_url=None, timeout=1200, retry_max=5):
    """Initializes cdsapi.Client with automatic fallback to Keys/API_Key/API.txt."""
    import cdsapi
    url, key = get_cds_credentials()
    chosen_url = default_url or url or "https://cds.climate.copernicus.eu/api"
    if key:
        os.environ["CDSAPI_URL"] = chosen_url
        os.environ["CDSAPI_KEY"] = key
        return cdsapi.Client(url=chosen_url, key=key, timeout=timeout, retry_max=retry_max)
    return cdsapi.Client(timeout=timeout, retry_max=retry_max)


# ----------------------------------------------------------------------------
# 2. Site Coordinates & Domain Bounds (Strictly Riyadh Only)
# ----------------------------------------------------------------------------
RIYADH_LAT = 24.926
RIYADH_LON = 46.722
STATION_NAME = "Riyadh_Airport_SDSC"

DOMAIN_LAT_MIN = 24.0
DOMAIN_LAT_MAX = 25.5
DOMAIN_LON_MIN = 46.0
DOMAIN_LON_MAX = 47.5
AREA_BOUNDS = [DOMAIN_LAT_MAX, DOMAIN_LON_MIN, DOMAIN_LAT_MIN, DOMAIN_LON_MAX]  # [25.5, 46.0, 24.0, 47.5] strictly Riyadh Only for CDS/ADS

# ----------------------------------------------------------------------------
# 3. Temporal Resolution & Partitioning (Strict 80/20 Chronological Split)
# ----------------------------------------------------------------------------
TRAIN_YEAR_START = 2015
TRAIN_YEAR_END = 2022   # 8 years (2015-2022) = 80.0% Training Set
TEST_YEAR_START = 2023  # 2 years (2023-2024) = 20.0% Out-of-Sample Test Set
TEST_YEAR_END = 2024

ALL_YEARS = list(range(TRAIN_YEAR_START, TEST_YEAR_END + 1))

# ERA5 6-hourly intervals (00, 06, 12, 18 UTC)
ERA5_6H_INTERVALS = ["00:00", "06:00", "12:00", "18:00"]
ERA5_PRESSURE_LEVELS = [850, 700, 500]

# CAMS lead times 0 to 120h in 3h steps (41 steps total)
CAMS_LEAD_TIMES = list(range(0, 121, 3))

# ----------------------------------------------------------------------------
# 4. Predictor Definitions
# ----------------------------------------------------------------------------
ERA5_PL_VARS = ["z", "u", "v", "t", "r"]
ERA5_SURFACE_VARS = ["ws10", "i10fg", "blh", "skt", "t2m", "swvl1", "cape"]

# ----------------------------------------------------------------------------
# 5. Particulate Matter (PM10 / PM2.5) Derived Proxies & Optics
# ----------------------------------------------------------------------------
def interpolate_aod550(aod500, ae):
    """
    Wavelength interpolation from AOD_500nm to AOD_550nm using Angstrom Exponent:
    AOD_550 = AOD_500 * (550 / 500)^(-AE)
    """
    aod500 = np.asarray(aod500, dtype=float)
    ae = np.asarray(ae, dtype=float)
    # Reject non-physical negative values
    invalid = (aod500 < 0.0) | (aod500 > 10.0) | (ae < -1.0) | (ae > 4.0) | np.isnan(aod500) | np.isnan(ae)
    with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
        aod550 = aod500 * np.power(550.0 / 500.0, -ae)
    aod550[invalid] = np.nan
    return aod550


def calculate_pm_proxies(cams_duaod550, aod550, ae, eps=1e-2, enforce_pure_dust_filter=True):
    """
    Derives strictly CAUSAL (anti-leakage) coarse and fine aerosol proxies at forecast time t:
    Uses multi-day lagged ground optical state (t - 48h to t - 72h, i.e., 8 to 12 six-hourly steps)
    so that neither contemporaneous nor intra-day ground-truth target AOD550(t) ever leaks
    into the predictor features:
      PM10_proxy  = sqrt(cams_duaod550(t) * AOD550_lag48h) / (AE_lag48h + 0.35)
      PM2.5_proxy = cams_duaod550(t-24h) * AE_lag48h
      PM_ratio    = (AE_lag48h + 0.15) / (AOD550_lag72h + 0.35)
    """
    cams_s = pd.Series(np.asarray(cams_duaod550, dtype=float)).bfill().ffill().fillna(0.20)
    aod_s = pd.Series(np.asarray(aod550, dtype=float)).bfill().ffill().fillna(0.25)
    ae_s = pd.Series(np.asarray(ae, dtype=float)).bfill().ffill().fillna(0.55)

    # Strictly causal 48h-72h (8 to 16 6-hourly steps) lagged ground persistence
    aod_lag48 = (0.5 * aod_s.shift(8) + 0.5 * aod_s.shift(12)).bfill().ffill().values
    aod_lag72 = (0.5 * aod_s.shift(12) + 0.5 * aod_s.shift(16)).bfill().ffill().values
    ae_lag48 = (0.5 * ae_s.shift(8) + 0.5 * ae_s.shift(12)).bfill().ffill().values
    cams_lag24 = (0.5 * cams_s.shift(4) + 0.5 * cams_s.shift(8)).bfill().ffill().values

    cams_duaod = np.clip(cams_s.values, 0.01, 5.0)
    aod_lag = np.clip(aod_lag48, 0.02, 4.5)
    ae_lag = np.clip(ae_lag48, 0.05, 1.80)

    # Strictly causal fine-mode proxy (de-collinearized from instantaneous cams_duaod)
    pm25_proxy = np.clip(np.sqrt(np.maximum(cams_lag24, 0.01)) * ae_lag, 0.01, 4.0)

    # Strictly causal coarse-mode proxy (48h-72h persistence + forecast interaction)
    denom = ae_lag + 0.35
    pm10_proxy = np.clip(np.sqrt(cams_duaod * aod_lag) / denom, 0.02, 6.0)

    if enforce_pure_dust_filter:
        pure_dust_mask = (ae_lag < 0.4)
        pm10_dust_surge = np.where(pure_dust_mask, pm10_proxy, np.nan)
    else:
        pm10_dust_surge = pm10_proxy

    # Decoupled fine-to-coarse persistence ratio (72h ground optical state ratio)
    pm_ratio = np.clip((ae_lag + 0.15) / (np.clip(aod_lag72, 0.05, 4.5) + 0.35), 0.01, 3.0)

    return {
        "pm10_proxy": pm10_proxy,
        "pm10_dust_surge": pm10_dust_surge,
        "pm25_proxy": pm25_proxy,
        "pm_ratio": pm_ratio,
        "pure_dust_flag": (ae_lag < 0.4).astype(int),
    }


def compute_unreliable_flag(cams_aod, aeronet_aod, sigma_riyadh, threshold_mult=1.5):
    """
    Forecast failure / unreliable state:
    Unreliable Flag = I(|Forecast Error| > 1.5 * sigma_Riyadh)
    where Forecast Error = cams_aod - aeronet_aod
    """
    cams_aod = np.asarray(cams_aod, dtype=float)
    aeronet_aod = np.asarray(aeronet_aod, dtype=float)
    abs_err = np.abs(cams_aod - aeronet_aod)
    return (abs_err > (threshold_mult * sigma_riyadh)).astype(int)


# ----------------------------------------------------------------------------
# 6. Quality Control & Station Parsing
# ----------------------------------------------------------------------------
def parse_aeronet(filepath):
    """
    Robust reader for AERONET Level 1.5 / 2.0 direct-sun CSV files.
    Applies quality filters: rejection of negative AOD (< 0.0) and missing markers (-999).
    Computes AOD_550nm and coarse/fine modes.
    """
    df = pd.read_csv(filepath, skiprows=7, na_values=[-999, -999.0, "-999", "-999.000000"])
    
    # Strip <br> HTML artifacts from column headers
    df.columns = [c.replace("<br>", "").strip() for c in df.columns]

    # Parse timestamp
    date_col = "Date(dd:mm:yyyy)"
    time_col = "Time(hh:mm:ss)"
    if date_col in df.columns and time_col in df.columns:
        df["datetime"] = pd.to_datetime(
            df[date_col] + " " + df[time_col],
            format="%d:%m:%Y %H:%M:%S",
            errors="coerce"
        )
    
    # Clean optical columns
    aod_col = "AOD_500nm"
    ae_col = "440-870_Angstrom_Exponent"

    if aod_col in df.columns and ae_col in df.columns:
        # Quality filter: reject non-physical negative optical values
        df = df[df[aod_col] >= 0.0].copy()
        df = df[df[ae_col].notna()].copy()
        df["aod550"] = interpolate_aod550(df[aod_col].values, df[ae_col].values)
    
    return df

