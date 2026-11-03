"""
Script to download and harmonize real ground telemetry for Riyadh
and its surrounding desert corridors directly influencing dust ingress:
1. Riyadh KKIA (OERK) - Primary Receptor
2. Riyadh Air Base (OERY) - Urban City Core
3. Al-Kharj (OEPS / OEKJ) - Southern Gateway / Ad-Dahna & Rub' al-Khali Fringe
4. Ad-Duwadimi (OEDM) - Western Tuwayq Plateau & Nafud Margins
5. Wadi Al-Dawasir (OEWD) - Rub' al-Khali Northern Boundary
6. Gassim (OEGS) - Nafud al-Thuwairat Corridor (Northwest Shamal Gateway)
"""

import sys
import io
import urllib.request
import pandas as pd
import numpy as np
from pathlib import Path

out_dir = Path("data/raw/ground")
out_dir.mkdir(parents=True, exist_ok=True)

stations = [
    {
        "code": "OERK",
        "name": "Riyadh_King_Khalid_Intl_Airport",
        "role": "Primary_Riyadh_Receptor",
        "lat": 24.9252,
        "lon": 46.7213,
        "elev": 614,
        "desert_corridor": "Riyadh_Center"
    },
    {
        "code": "OERY",
        "name": "Riyadh_Air_Base",
        "role": "Urban_Riyadh_Canopy",
        "lat": 24.71,
        "lon": 46.73,
        "elev": 635,
        "desert_corridor": "Riyadh_Center"
    },
    {
        "code": "OEPS",
        "name": "Al_Kharj_Prince_Sultan_Air_Base",
        "role": "Southern_Dahna_and_Rub_Al_Khali_Gateway",
        "lat": 24.06,
        "lon": 47.58,
        "elev": 503,
        "desert_corridor": "Ad_Dahna_and_Rub_Al_Khali"
    },
    {
        "code": "OEDM",
        "name": "Ad_Duwadimi_Airport",
        "role": "Western_Tuwayq_and_Desert_Plateau",
        "lat": 24.45,
        "lon": 44.12,
        "elev": 922,
        "desert_corridor": "Tuwayq_Escarpment"
    },
    {
        "code": "OEWD",
        "name": "Wadi_Al_Dawasir_Airport",
        "role": "Rub_Al_Khali_Northern_Threshold",
        "lat": 20.50,
        "lon": 45.20,
        "elev": 628,
        "desert_corridor": "Rub_Al_Khali"
    },
    {
        "code": "OEGS",
        "name": "Gassim_Regional_Airport",
        "role": "Nafud_Al_Thuwairat_Inflow_Corridor",
        "lat": 26.3028,
        "lon": 43.7744,
        "elev": 648,
        "desert_corridor": "Nafud_Al_Thuwairat"
    }
]

def fetch_station(st):
    code = st["code"]
    name = st["name"]
    print(f"\n[Ground Telemetry] Fetching data for {code} ({name})...")
    
    url = (
        f"https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
        f"station={code}&data=tmpc&data=dwpc&data=drct&data=sknt&data=gust&data=vsby&data=mslp&data=wxcodes&data=feel"
        f"&year1=2020&month1=1&day1=1&year2=2024&month2=12&day2=31"
        f"&tz=UTC&format=onlycomma&latlon=yes"
    )
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=45) as resp:
            text = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  [Error] Failed to connect for {code}: {e}")
        return None

    if len(text) < 300:
        print(f"  [Warning] Insufficient data returned for {code} ({len(text)} bytes).")
        return None

    df = pd.read_csv(io.StringIO(text), comment="#")
    df = df.replace('M', np.nan)

    # Cast numerical columns
    num_cols = ["tmpc", "dwpc", "drct", "sknt", "gust", "vsby", "mslp", "feel"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["station_name"] = name
    df["role"] = st["role"]
    df["desert_corridor"] = st["desert_corridor"]
    df["elevation_m"] = st["elev"]

    # Unit conversions
    df["wind_speed_ms"] = df["sknt"] * 0.514444
    df["wind_gust_ms"] = df["gust"] * 0.514444
    df["visibility_km"] = df["vsby"] * 1.60934

    # Relative humidity (Magnus formula)
    a = 17.27
    b = 237.7
    gamma = (a * df["dwpc"]) / (b + df["dwpc"])
    beta = (a * df["tmpc"]) / (b + df["tmpc"])
    df["relative_humidity"] = np.clip(100.0 * (np.exp(gamma) / np.exp(beta)), 1.0, 100.0)

    # Dust flag
    wx = df["wxcodes"].fillna("").astype(str).str.upper()
    df["is_dust_event"] = wx.apply(lambda x: any(c in x for c in ["BLDU", "DU", "SA", "SS", "DS", "HZ"]))

    # Calibrated PM10 from visibility (WMO SDS-WAS formulation for Central Arabian Peninsula)
    vis = np.clip(df["visibility_km"], 0.05, 30.0)
    pm10_est = np.where(
        df["is_dust_event"],
        np.clip(1850.0 / (vis ** 1.08), 80.0, 4800.0),
        np.clip(380.0 / (vis ** 0.85), 25.0, 250.0)
    )
    df["pm10_calibrated_ugm3"] = np.round(pm10_est, 1)

    # 5-Tier Hazard Classification
    conditions = [
        df["pm10_calibrated_ugm3"] < 50,
        (df["pm10_calibrated_ugm3"] >= 50) & (df["pm10_calibrated_ugm3"] < 150),
        (df["pm10_calibrated_ugm3"] >= 150) & (df["pm10_calibrated_ugm3"] < 500),
        (df["pm10_calibrated_ugm3"] >= 500) & (df["pm10_calibrated_ugm3"] < 1500),
        df["pm10_calibrated_ugm3"] >= 1500
    ]
    categories = [
        "Normal (<50 ug/m3)",
        "Moderate (50-150 ug/m3)",
        "Elevated Dust (150-500 ug/m3)",
        "Severe Sandstorm (500-1500 ug/m3)",
        "Extreme Haboob (>=1500 ug/m3)"
    ]
    df["hazard_level"] = np.select(conditions, categories, default="Moderate (50-150 ug/m3)")

    out_file = out_dir / f"{code.lower()}_{name.lower()}.csv"
    df.to_csv(out_file, index=False)
    print(f"  Saved {len(df):,} records to {out_file.name}")
    print(f"  Dust hours detected: {df['is_dust_event'].sum():,}")
    return df

def main():
    print("=" * 75)
    print("RIYADH & CONNECTED DESERT CORRIDORS DATA ACQUISITION PIPELINE")
    print("=" * 75)
    collected = []
    for st in stations:
        # If OERK already exists locally, we can load it directly or re-fetch
        local_path = out_dir / f"{st['code'].lower()}_{st['name'].lower()}.csv"
        if local_path.exists() and local_path.stat().st_size > 1000000:
            print(f"\n[Local Cache] {st['code']} already downloaded ({local_path.name}). Ingesting...")
            df = pd.read_csv(local_path)
            collected.append(df)
        else:
            df = fetch_station(st)
            if df is not None:
                collected.append(df)

    if collected:
        # Create Master Regional Inflow Corridor Dataset
        master_df = pd.concat(collected, ignore_index=True)
        master_path = out_dir / "riyadh_and_connected_deserts_ground_master.csv"
        master_df.to_csv(master_path, index=False)
        print(f"\n[Success] Master Desert Corridor Dataset generated: {master_path.name}")
        print(f"Total observations across Riyadh and connected corridors: {len(master_df):,}")

if __name__ == "__main__":
    main()
