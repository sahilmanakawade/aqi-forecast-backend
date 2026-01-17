from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import joblib
import pandas as pd

from utils.data_fetch import fetch_recent_data
from utils.aqi_calc import compute_today_aqi
from utils.feature_engineering import build_features
from utils.forecast import forecast_10_day

app = FastAPI(title="AQI Forecast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# load models
rf_pm25 = joblib.load(os.path.join(BASE_DIR, "model", "rf_25.pkl"))
rf_pm10 = joblib.load(os.path.join(BASE_DIR, "model", "rf_10.pkl"))


@app.get("/")
def home():
    return {"status": "AQI Forecast API running"}


@app.get("/forecast")
def forecast(lat: float, lon: float):
    df_recent = fetch_recent_data(lat, lon)
    print("df_recent shape:", df_recent.shape)

    today = compute_today_aqi(lat, lon)
    print("today AQI:", today)

    df_features = build_features(df_recent)
    print("df_features shape:", df_features.shape)

    forecast_df = forecast_10_day(
        features=df_features,
        rf_10=rf_pm10,
        rf_25=rf_pm25,
        df=df_recent
    )

    return [today] + forecast_df.to_dict(orient="records")
