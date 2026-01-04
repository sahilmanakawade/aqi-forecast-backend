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
    last_row = df_feat.iloc[-1].copy()

    # 🔁 FEATURE NAME ALIASING (CRITICAL FIX)
    rename_map = {
        "pm25_lag1": "pm2.5_lag1",
        "pm25_lag2": "pm2.5_lag2",
        "pm25_lag3": "pm2.5_lag3",
        "pm25_roll7": "pm2.5_roll7",
    }

    last_row.rename(index=rename_map, inplace=True)

    X = pd.DataFrame([last_row[features]])

    preds = []
    last_date = df_feat["date"].iloc[-1]

    for i in range(10):
        pm25_pred = rf_pm25.predict(X)[0]
        pm10_pred = rf_pm10.predict(X)[0]

        preds.append({
            "date": str(last_date + timedelta(days=i + 1)),
            "pm25": float(pm25_pred),
            "pm10": float(pm10_pred),
            "AQI": float(max(pm25_pred, pm10_pred)),
            "type": "forecast"
        })

    return pd.DataFrame(preds)
