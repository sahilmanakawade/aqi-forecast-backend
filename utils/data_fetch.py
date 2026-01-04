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
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }

    params_air = {
        "latitude": lat,
        "longitude": lon,
        "past_days": days,
        "hourly": "pm2_5,pm10",
        "timezone": "auto"
    }

    weather = requests.get(url_weather, params=params_weather, timeout=10).json()
    air = requests.get(url_air, params=params_air, timeout=10).json()

    # 🔒 Graceful fallback (NO CRASH)
    if "hourly" not in weather or "hourly" not in air:
        return pd.DataFrame()

    # Weather → daily
    df_weather = pd.DataFrame(weather["hourly"])
    df_weather["date"] = pd.to_datetime(df_weather["time"]).dt.date
    df_weather = (
        df_weather
        .groupby("date")[["temperature_2m", "relative_humidity_2m", "wind_speed_10m"]]
        .mean()
        .reset_index()
    )
    df_weather.columns = ["date", "temperature", "humidity", "wind_speed"]

    # Air → daily
    df_air = pd.DataFrame(air["hourly"])
    df_air["date"] = pd.to_datetime(df_air["time"]).dt.date
    df_air = (
        df_air
        .groupby("date")[["pm2_5", "pm10"]]
        .mean()
        .reset_index()
    )

    df = pd.merge(df_weather, df_air, on="date", how="inner")

    today = datetime.utcnow().date()
    df = df[df["date"] <= today]

    return df.sort_values("date").reset_index(drop=True)
