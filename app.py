from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import joblib
from functools import lru_cache

from utils.data_fetch import fetch_recent_data
from utils.feature_engineering import build_features
from utils.forecast import forecast_10_days
from utils.aqi_calc import compute_today_aqi

# -------------------------
# Create FastAPI app
# -------------------------
app = FastAPI(
    title="AQI Forecast API",
    description="10-day AQI forecast using Machine Learning",
    version="1.0"
)

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Load models & assets
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

rf_pm25 = joblib.load(os.path.join(BASE_DIR, "model", "rf_pm25.pkl"))
rf_pm10 = joblib.load(os.path.join(BASE_DIR, "model", "rf_pm10.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "model", "features.pkl"))
df2_5 = joblib.load(os.path.join(BASE_DIR, "model", "aqi_pm25_table.pkl"))
df10 = joblib.load(os.path.join(BASE_DIR, "model", "aqi_pm10_table.pkl"))

# -------------------------
# Routes
# -------------------------
@app.get("/")
def home():
    return {"status": "AQI Forecast API running"}

# -------------------------
# Cached forecast logic
# -------------------------
@lru_cache(maxsize=32)
def cached_forecast(lat: float, lon: float):

    # 1️⃣ Fetch recent real data
    df_recent = fetch_recent_data(lat, lon)

    # 🚨 GUARD: No data available
    if df_recent is None or df_recent.empty:
        return {
            "status": "temporary_unavailable",
            "message": "External weather/AQI API limit exceeded. Please try again later."
        }

    # 2️⃣ Compute TODAY AQI (safe)
    today = compute_today_aqi(df_recent, df2_5, df10)

    # 3️⃣ Build ML features
    df_feat = build_features(df_recent)

    # 4️⃣ Forecast next 10 days
    forecast_df = forecast_10_days(
        df_feat,
        rf_pm25,
        rf_pm10,
        df2_5,
        df10,
        features
    )

    # 5️⃣ Combine results safely
    result = []
    if today is not None:
        result.append(today)

    result.extend(forecast_df.to_dict(orient="records"))

    return result


# -------------------------
# API endpoint
# -------------------------
@app.get("/forecast")
def forecast(lat: float, lon: float):
    return cached_forecast(lat, lon)
