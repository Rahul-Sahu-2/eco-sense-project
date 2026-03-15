import os
import pandas as pd
from datetime import datetime
from backend.config import CSV_PATH


def _ensure_dir():
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)


def get_all_reports() -> list[dict]:
    try:
        df = pd.read_csv(CSV_PATH)
        return df.fillna("").to_dict(orient="records")
    except Exception:
        return []


def get_stats() -> dict:
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception:
        return {"total": 0, "high": 0, "medium": 0, "low": 0, "avg_waste": 0}

    if df.empty:
        return {"total": 0, "high": 0, "medium": 0, "low": 0, "avg_waste": 0}

    total = len(df)
    high = int((df["waste_percent"] > 80).sum())
    medium = int(((df["waste_percent"] > 50) & (df["waste_percent"] <= 80)).sum())
    low = total - high - medium
    avg_waste = round(float(df["waste_percent"].mean()), 1)

    return {
        "total": total,
        "high": high,
        "medium": medium,
        "low": low,
        "avg_waste": avg_waste,
    }


def get_waste_level(percent: float) -> str:
    if percent >= 80:
        return "HIGH"
    elif percent >= 50:
        return "MEDIUM"
    return "LOW"


def save_report(
    name: str,
    waste_type: str,
    waste_percent: float,
    lat: float,
    lon: float,
    wallet: str = "",
    tx_hash: str = "",
    tokens: int = 0,
):
    _ensure_dir()
    waste_level = get_waste_level(waste_percent)

    new_row = {
        "name": name,
        "waste_type": waste_type,
        "waste_percent": waste_percent,
        "waste_level": waste_level,
        "lat": lat,
        "lon": lon,
        "wallet": wallet,
        "tokens_earned": tokens,
        "tx_hash": tx_hash,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(CSV_PATH, index=False)
    return new_row
