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
        "daily": (
            "temperature_2m_mean,"
            "relative_humidity_2m_mean,"
            "wind_speed_10m_mean"
        ),
        "timezone": "auto"
    }

    params_air = {
        "latitude": lat,
        "longitude": lon,
        "past_days": days,
        "hourly": "pm2_5,pm10",
        "timezone": "auto"
    }

    weather_resp = requests.get(url_weather, params=params_weather, timeout=10)
    air_resp = requests.get(url_air, params=params_air, timeout=10)

    weather = weather_resp.json()
    air = air_resp.json()

    # -------------------------
    # 🚨 SAFETY CHECKS (FIXES YOUR CRASH)
    # -------------------------
    if "daily" not in weather:
        raise ValueError(f"Weather API error or format change: {weather}")

    if "hourly" not in air:
        raise ValueError(f"Air quality API error or format change: {air}")

    # -------------------------
    # Weather dataframe
    # -------------------------
    df_weather = pd.DataFrame(weather["daily"])

    if df_weather.empty:
        raise ValueError("Weather daily data is empty")

    df_weather["date"] = pd.to_datetime(df_weather["time"]).dt.date
    df_weather.drop(columns=["time"], inplace=True)

    # Rename columns early (cleaner)
    df_weather.rename(
        columns={
            "temperature_2m_mean": "temperature",
            "relative_humidity_2m_mean": "humidity",
            "wind_speed_10m_mean": "wind_speed"
        },
        inplace=True
    )

    # -------------------------
    # Air quality dataframe
    # -------------------------
    df_air = pd.DataFrame(air["hourly"])

    if df_air.empty:
        raise ValueError("Air quality hourly data is empty")

    df_air["date"] = pd.to_datetime(df_air["time"]).dt.date
    df_air = (
        df_air
        .groupby("date")[["pm2_5", "pm10"]]
        .mean()
        .reset_index()
    )

    # -------------------------
    # Merge weather + air
    # -------------------------
    df = pd.merge(df_weather, df_air, on="date", how="inner")

    # -------------------------
    # 🔥 DROP FUTURE DATES (CRITICAL)
    # -------------------------
    today = datetime.utcnow().date()
    df = df[df["date"] <= today]

    df = df.sort_values("date").reset_index(drop=True)

    # -------------------------
    # Final sanity check
    # -------------------------
    if df.empty:
        raise ValueError("Merged dataframe is empty after filtering")

    return df
