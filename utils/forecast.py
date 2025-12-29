import pandas as pd
from utils.aqi_calc import aqi

def forecast_10_days(
    df,
    rf_pm25,
    rf_pm10,
    df2_5,
    df10,
    features
):
    results = []

    df = df.copy()

    for i in range(10):
        last_row = df.iloc[-1]

        X = pd.DataFrame([last_row[features]])

        pm25_pred = rf_pm25.predict(X)[0]
        pm10_pred = rf_pm10.predict(X)[0]

        aqi25 = aqi(pm25_pred, df2_5)
        aqi10 = aqi(pm10_pred, df10)
        aqi_val = max(aqi25, aqi10)

        next_date = last_row["date"] + pd.Timedelta(days=1)

        new_row = {
            "date": next_date,
            "pm2.5": pm25_pred,
            "pm10": pm10_pred,
            "AQI": aqi_val,
        }

        # --- ADD LAGS ---
        new_row["pm2.5_lag1"] = last_row["pm2.5"]
        new_row["pm2.5_lag2"] = last_row["pm2.5_lag1"]
        new_row["pm2.5_lag3"] = last_row["pm2.5_lag2"]

        new_row["pm10_lag1"] = last_row["pm10"]
        new_row["pm10_lag2"] = last_row["pm10_lag1"]
        new_row["pm10_lag3"] = last_row["pm10_lag2"]

        # --- ROLLING ---
        new_row["pm2.5_roll7"] = (
            df["pm2.5"].tail(6).sum() + pm25_pred
        ) / 7

        new_row["pm10_roll7"] = (
            df["pm10"].tail(6).sum() + pm10_pred
        ) / 7

        # Fill static weather (or keep last known)
        new_row["temperature"] = last_row["temperature"]
        new_row["humidity"] = last_row["humidity"]
        new_row["wind_speed"] = last_row["wind_speed"]

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        results.append({
            "date": next_date.strftime("%Y-%m-%d"),
            "pm2.5": pm25_pred,
            "pm10": pm10_pred,
            "AQI": aqi_val,
            "type": "forecast"
        })

    return pd.DataFrame(results)
