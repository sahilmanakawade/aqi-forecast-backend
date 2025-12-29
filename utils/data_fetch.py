import requests
import pandas as pd
from datetime import datetime
from functools import lru_cache


@lru_cache(maxsize=64)
def fetch_recent_data(lat: float, lon: float, days: int = 21):
    url_weather = "https://api.open-meteo.com/v1/forecast"
    url_air = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params_weather = {
        "latitude": lat,
        "longitude": lon,
        "past_days": days,
        "daily": "temperature_2m_mean,relative_humidity_2m_mean,wind_speed_10m_mean",
        "timezone": "auto"
    }

    params_air = {
        "latitude": lat,
        "longitude": lon,
        "past_days": days,
        "hourly": "pm2_5,pm10",
        "timezone": "auto"
    }

    weather = requests.get(url_weather, params_weather).json()
    air = requests.get(url_air, params_air).json()

    # -------------------------
    # Weather dataframe
    # -------------------------
    df_weather = pd.DataFrame(weather["daily"])
    df_weather["date"] = pd.to_datetime(df_weather["time"]).dt.date
    df_weather.drop(columns=["time"], inplace=True)

    # -------------------------
    # Air quality dataframe
    # -------------------------
    df_air = pd.DataFrame(air["hourly"])
    df_air["date"] = pd.to_datetime(df_air["time"]).dt.date
    df_air = df_air.groupby("date")[["pm2_5", "pm10"]].mean().reset_index()

    # -------------------------
    # Merge
    # -------------------------
    df = pd.merge(df_weather, df_air, on="date")
    df.columns = ["temperature", "humidity", "wind_speed", "date", "pm2.5", "pm10"]

    # -------------------------
    # 🔥 CRITICAL FIX: DROP FUTURE DATES
    # -------------------------
    today = datetime.utcnow().date()
    df = df[df["date"] <= today]

    df = df.sort_values("date").reset_index(drop=True)

    return df
