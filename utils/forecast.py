import pandas as pd
from datetime import timedelta

def forecast_10_days(
    df_feat,
    rf_pm25,
    rf_pm10,
    df2_5,
    df10,
    features
):
    """
    Iterative 10-day AQI forecast (AUTO-REGRESSIVE)
    """

    forecasts = []

    # Start from last known row
    current = df_feat.iloc[-1].copy()
    current_date = pd.to_datetime(current["date"])

    for _ in range(10):
        X = pd.DataFrame([[current[f] for f in features]], columns=features)

        # Predict PM values
        pm25_pred = float(rf_pm25.predict(X)[0])
        pm10_pred = float(rf_pm10.predict(X)[0])

        # Store result
        forecasts.append({
            "date": (current_date + timedelta(days=1)).strftime("%Y-%m-%d"),
            "pm2.5": pm25_pred,
            "pm10": pm10_pred,
            "AQI": max(pm25_pred, pm10_pred),
            "type": "forecast"
        })

        # 🔁 UPDATE LAGS (CRITICAL)
        current["pm2.5_lag3"] = current["pm2.5_lag2"]
        current["pm2.5_lag2"] = current["pm2.5_lag1"]
        current["pm2.5_lag1"] = pm25_pred

        current["pm10_lag3"] = current["pm10_lag2"]
        current["pm10_lag2"] = current["pm10_lag1"]
        current["pm10_lag1"] = pm10_pred

        # Update rolling means (approximate)
        current["pm2.5_roll7"] = (
            current["pm2.5_roll7"] * 6 + pm25_pred
        ) / 7

        current["pm10_roll7"] = (
            current["pm10_roll7"] * 6 + pm10_pred
        ) / 7

        # Move date forward
        current_date += timedelta(days=1)

    return pd.DataFrame(forecasts)
