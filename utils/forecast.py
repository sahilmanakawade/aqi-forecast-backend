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
    Safe iterative 10-day AQI forecast
    (NO crashes, NO constant output)
    """

    # 🚨 SAFETY: need enough rows
    if df_feat is None or df_feat.empty or len(df_feat) < 1:
        return pd.DataFrame()

    forecasts = []

    # Use last valid row
    current = df_feat.iloc[-1].copy()

    # 🔐 SAFETY: date handling
    if "date" in current:
        current_date = pd.to_datetime(current["date"])
    else:
        current_date = pd.Timestamp.utcnow()

    # 🔐 SAFETY: ensure all required features exist
    for f in features:
        if f not in current:
            current[f] = 0.0

    for _ in range(10):
        # Build model input
        X = pd.DataFrame([[current[f] for f in features]], columns=features)

        # Predict
        pm25_pred = float(rf_pm25.predict(X)[0])
        pm10_pred = float(rf_pm10.predict(X)[0])

        # Store forecast
        next_date = current_date + timedelta(days=1)
        forecasts.append({
            "date": next_date.strftime("%Y-%m-%d"),
            "pm2.5": pm25_pred,
            "pm10": pm10_pred,
            "AQI": max(pm25_pred, pm10_pred),
            "type": "forecast"
        })

        # 🔁 UPDATE LAGS SAFELY
        if "pm2.5_lag3" in current:
            current["pm2.5_lag3"] = current.get("pm2.5_lag2", pm25_pred)
        if "pm2.5_lag2" in current:
            current["pm2.5_lag2"] = current.get("pm2.5_lag1", pm25_pred)
        if "pm2.5_lag1" in current:
            current["pm2.5_lag1"] = pm25_pred

        if "pm10_lag3" in current:
            current["pm10_lag3"] = current.get("pm10_lag2", pm10_pred)
        if "pm10_lag2" in current:
            current["pm10_lag2"] = current.get("pm10_lag1", pm10_pred)
        if "pm10_lag1" in current:
            current["pm10_lag1"] = pm10_pred

        # 🔁 Rolling mean (robust)
        if "pm2.5_roll7" in current:
            current["pm2.5_roll7"] = (
                current["pm2.5_roll7"] * 6 + pm25_pred
            ) / 7

        if "pm10_roll7" in current:
            current["pm10_roll7"] = (
                current["pm10_roll7"] * 6 + pm10_pred
            ) / 7

        current_date = next_date

    return pd.DataFrame(forecasts)
