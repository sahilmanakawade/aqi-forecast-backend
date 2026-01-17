import pandas as pd
from utils.aqi_calc import aqi25, aqi10
aqi_data={
    "ihi":[50,100,200,300,400,500,600],
    "ilo":[0,51,101,201,301,401,501],
    "bphi2.5":[30,60,90,120,250,550,1000],
    "bplo2.5":[0,31,61,91,121,251,551],
    "bphipm10":[50,100,250,350,430,500,1000],
    "bplopm10":[0,51,101,251,351,431,501],
    "bphico":[1,2,10,17,34,50,1000],
    "bploco":[0,1.1,2.1,10.1,17.1,50.1,1000],
    "bphio3":[50,100,168,208,748,1000,10000],
    "bploo3":[0,51,101,169,209,749,10000],
    "bphino2":[40,80,180,280,400,600,10000],
    "bplono2":[0,41,81,181,281,401,10000],
    "bphiso2":[40,80,380,800,1600,2000,10000],
    "bploso2":[0,41,81,381,801,1601,10000],
    "bphinh3":[200,400,800,1200,1800,2000,10000],
    "bplonh3":[0,201,401,801,1201,1801,10000]
}
aqi_data=pd.DataFrame(aqi_data)


def forecast_10_day(features: pd.DataFrame, rf_10, rf_25, df: pd.DataFrame):
    last_known = features.iloc[-1].copy()
    if "date" in last_known:
        last_known = last_known.drop("date")
    feature_order = rf_25.feature_names_in_
    last_known = last_known[feature_order]

    future_pm25 = []
    future_pm10 = []
    for _ in range(10):
        X = last_known.to_frame().T

        next_pm25 = float(rf_25.predict(X)[0])
        next_pm10 = float(rf_10.predict(X)[0])

        future_pm25.append(next_pm25)
        future_pm10.append(next_pm10)
        for i in range(24, 1, -1):
            last_known[f"pm2.5lag{i}"] = last_known[f"pm2.5lag{i-1}"]
        last_known["pm2.5lag1"] = next_pm25
        for i in range(24, 1, -1):
            last_known[f"pm10lagP{i}"] = last_known[f"pm10lagP{i-1}"]
        last_known["pm10lagP1"] = next_pm10
        pm25_vals = [last_known[f"pm2.5lag{i}"] for i in range(1, 25)]
        pm10_vals = [last_known[f"pm10lagP{i}"] for i in range(1, 25)]

        last_known["pm2.5roll7"] = sum(pm25_vals[:7]) / 7
        last_known["pm2.5roll14"] = sum(pm25_vals[:14]) / 14
        last_known["pm2.5roll21"] = sum(pm25_vals[:21]) / 21

        last_known["pm10roll7"] = sum(pm10_vals[:7]) / 7
        last_known["pm10roll14"] = sum(pm10_vals[:14]) / 14
        last_known["pm10roll21"] = sum(pm10_vals[:21]) / 21
        last_known = last_known[feature_order]
    future_dates = pd.date_range(
        start=pd.to_datetime(df["date"].iloc[-1]) + pd.Timedelta(days=1),
        periods=10,
        freq="D"
    )
    forecast = pd.DataFrame({
        "date": future_dates,
        "pm2_5": future_pm25,
        "pm10": future_pm10
    })
    forecast["aqi_pm25"] = forecast["pm2_5"].apply(lambda x:aqi25(x,aqi_data))
    forecast["aqi_pm10"] = forecast["pm10"].apply(lambda x:aqi25(x,aqi_data))
    forecast["AQI"] = forecast[["aqi_pm25", "aqi_pm10"]].max(axis=1)
    forecast["type"] = "forecast"
    return forecast[["date", "pm2_5", "pm10", "AQI", "type"]]
