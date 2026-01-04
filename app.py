from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, joblib

from utils.data_fetch import fetch_recent_data
from utils.feature_engineering import build_features
from utils.forecast import forecast_10_days
from utils.aqi_calc import compute_today_aqi

app = FastAPI(title="AQI Forecast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

rf_pm25 = joblib.load(os.path.join(BASE_DIR, "model", "rf_pm25.pkl"))
rf_pm10 = joblib.load(os.path.join(BASE_DIR, "model", "rf_pm10.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "model", "features.pkl"))
df2_5 = joblib.load(os.path.join(BASE_DIR, "model", "aqi_pm25_table.pkl"))
df10 = joblib.load(os.path.join(BASE_DIR, "model", "aqi_pm10_table.pkl"))

@app.get("/")
def home():
    return {"status": "AQI Forecast API running"}

@app.get("/forecast")
def forecast(lat: float, lon: float):
    df_recent = fetch_recent_data(lat, lon)

    if df_recent is None:
        return {
            "status": "temporary_unavailable",
            "message": "External weather/AQI API limit exceeded. Please try again later.",
        }

    today = compute_today_aqi(df_recent, df2_5, df10)
    if today is None:
        return {
            "status": "temporary_unavailable",
            "message": "Insufficient AQI data.",
        }

    df_feat = build_features(df_recent)

    forecast_df = forecast_10_days(
        df_feat,
        rf_pm25,
        rf_pm10,
        df2_5,
        df10,
        features,
    )

    return [today] + forecast_df.to_dict(orient="records")
