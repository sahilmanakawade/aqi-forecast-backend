import requests
import pandas as pd
from datetime import datetime
from functools import lru_cache


@lru_cache(maxsize=64)
def fetch_recent_data(lat: float, lon: float, days: int = 21):
    url_weather = "https://api.open-meteo.com/v1/forecast"
    url_air = "https://air-quality-api.open-meteo.com/v1/air-quality"

    # -------------------------
    # WEATHER (HOURLY – NO QUOTA ISSUE)
    # -------------------------
    params_weather = {
        "latitude": lat,
        "longitude": lon,
        "past_days": days,
        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        ),
        "timezone": "auto"
    }

    # -------------------------
    # AIR QUALITY (HOURLY)
    # -------------------------
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
    # SAFETY CHECKS
    # -------------------------
    if "hourly" not in weather:
        raise ValueError(f"Weather API error: {weather}")

    if "hourly" not in air:
        raise ValueError(f"Air quality API error: {air}")

    # -------------------------
    # WEATHER → DAILY AGGREGATION
    # -------------------------
    df_weather = pd.DataFrame(weather["hourly"])

    if df_weather.empty:
        raise ValueError("Weather hourly data is empty")

    df_weather["date"] = pd.to_datetime(df_weather["time"]).dt.date

    df_weather = (
        df_weather
        .groupby("date")[[
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m"
        ]]
        .mean()
        .reset_index()
    )

    df_weather.rename(
        columns={
            "temperature_2m": "temperature",
            "relative_humidity_2m": "humidity",
            "wind_speed_10m": "wind_speed"
        },
        inplace=True
    )

    # -------------------------
    # AIR QUALITY → DAILY AGGREGATION
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
    # MERGE
    # -------------------------
    df = pd.merge(df_weather, df_air, on="date", how="inner")

    # -------------------------
    # DROP FUTURE DATES
    # -------------------------
    today = datetime.utcnow().date()
    df = df[df["date"] <= today]

    df = df.sort_values("date").reset_index(drop=True)

    if df.empty:
        raise ValueError("Merged dataframe is empty after filtering")

    return df
