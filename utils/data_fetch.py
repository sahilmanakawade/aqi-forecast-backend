import requests
import pandas as pd
from datetime import datetime

def fetch_recent_data(lat: float, lon: float, days: int = 21):
    url_weather = "https://api.open-meteo.com/v1/forecast"
    url_air = "https://air-quality-api.open-meteo.com/v1/air-quality"

    try:
        weather = requests.get(
            url_weather,
            params={
                "latitude": lat,
                "longitude": lon,
                "past_days": days,
                "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
                "timezone": "auto",
            },
            timeout=10,
        ).json()

        air = requests.get(
            url_air,
            params={
                "latitude": lat,
                "longitude": lon,
                "past_days": days,
                "hourly": "pm2_5,pm10",
                "timezone": "auto",
            },
            timeout=10,
        ).json()

        # 🚨 HARD GUARD — NEVER CRASH
        if "hourly" not in weather or "hourly" not in air:
            return None

        # -------------------------
        # Weather → daily mean
        # -------------------------
        df_weather = pd.DataFrame(weather["hourly"])
        df_weather["date"] = pd.to_datetime(df_weather["time"]).dt.date

        df_weather = (
            df_weather
            .groupby("date")[["temperature_2m", "relative_humidity_2m", "wind_speed_10m"]]
            .mean()
            .reset_index()
        )

        df_weather.rename(
            columns={
                "temperature_2m": "temperature",
                "relative_humidity_2m": "humidity",
                "wind_speed_10m": "wind_speed",
            },
            inplace=True,
        )

        # -------------------------
        # Air → daily mean
        # -------------------------
        df_air = pd.DataFrame(air["hourly"])
        df_air["date"] = pd.to_datetime(df_air["time"]).dt.date

        df_air = (
            df_air
            .groupby("date")[["pm2_5", "pm10"]]
            .mean()
            .reset_index()
        )

        # -------------------------
        # Merge
        # -------------------------
        df = pd.merge(df_weather, df_air, on="date", how="inner")

        # 🔒 FINAL SCHEMA NORMALIZATION (CRITICAL)
        df.rename(
            columns={
                "pm2_5": "pm25",
                "pm10": "pm10",
            },
            inplace=True,
        )

        # -------------------------
        # Drop future dates
        # -------------------------
        today = datetime.utcnow().date()
        df = df[df["date"] <= today]

        if df.empty:
            return None

        return df.sort_values("date").reset_index(drop=True)

    except Exception:
        # 🚨 NEVER RAISE IN PRODUCTION API
        return None
