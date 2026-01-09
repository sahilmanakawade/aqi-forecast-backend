import pandas as pd
from datetime import timedelta
from utils.aqi_calc import aqi


def smooth(prev, pred, max_change=0.25):
    upper = prev * (1 + max_change)
    lower = prev * (1 - max_change)
    return max(min(pred, upper), lower)


def forecast_10_days(
    df_feat,
    rf_pm25,
    rf_pm10,
    df2_5,
    df10,
    features
):
    if df_feat is None or df_feat.empty:
        return pd.DataFrame()

    forecasts = []

    current = df_feat.iloc[-1].copy()
    current_date = pd.to_datetime(current["date"])

    last_pm25 = current.get("pm2.5", current.get("pm2.5_lag1", 100))
    last_pm10 = current.get("pm10", current.get("pm10_lag1", 100))

    for _ in range(10):
        X = pd.DataFrame([[current[f] for f in features]], columns=features)

        raw_pm25 = float(rf_pm25.predict(X)[0])
        raw_pm10 = float(rf_pm10.predict(X)[0])

        # 🔒 SMOOTHING (key fix)
        pm25_pred = smooth(last_pm25, raw_pm25)
        pm10_pred = smooth(last_pm10, raw_pm10)

        # ✅ CORRECT AQI CALCULATION
        aqi_val = max(
            aqi(pm25_pred, df2_5),
            aqi(pm10_pred, df10)
        )

        next_date = current_date + timedelta(days=1)

        forecasts.append({
            "date": next_date.strftime("%Y-%m-%d"),
            "pm2.5": round(pm25_pred, 2),
            "pm10": round(pm10_pred, 2),
            "AQI": round(aqi_val, 1),
            "type": "forecast"
        })

        # 🔁 Update lags
        current["pm2.5_lag3"] = current.get("pm2.5_lag2", pm25_pred)
        current["pm2.5_lag2"] = current.get("pm2.5_lag1", pm25_pred)
        current["pm2.5_lag1"] = pm25_pred

        current["pm10_lag3"] = current.get("pm10_lag2", pm10_pred)
        current["pm10_lag2"] = current.get("pm10_lag1", pm10_pred)
        current["pm10_lag1"] = pm10_pred

        current["pm2.5_roll7"] = (current["pm2.5_roll7"] * 6 + pm25_pred) / 7
        current["pm10_roll7"] = (current["pm10_roll7"] * 6 + pm10_pred) / 7

        last_pm25 = pm25_pred
        last_pm10 = pm10_pred
        current_date = next_date

    return pd.DataFrame(forecasts)
