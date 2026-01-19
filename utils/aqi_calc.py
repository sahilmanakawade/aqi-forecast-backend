import requests
import numpy as np
import pandas as pd
from datetime import datetime,timedelta,UTC
import warnings
warnings.simplefilter("ignore")
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
def aqi25(a,aqi_data):
    row=aqi_data[(aqi_data["bplo2.5"] <= a) & (aqi_data["bphi2.5"] >= a)]
    if row.empty:
        return None
    row=row.iloc[0]
    ihi=row["ihi"]
    ilo=row["ilo"]
    bphi2_5=row["bphi2.5"]
    bplo2_5=row["bplo2.5"]
    aqi2_5=((ihi - ilo) / (bphi2_5 - bplo2_5)) * (a - bplo2_5) + ilo
    return aqi2_5
def aqi10(a,aqi_data):
    row=aqi_data[(aqi_data["bplopm10"] <= a) & (aqi_data["bphipm10"] >= a)]

    if row.empty:
        return None
    row=row.iloc[0]
    ihi=row["ihi"]
    ilo=row["ilo"]
    bphi10=row["bphipm10"]
    bplo10=row["bplopm10"]
    aqi10=((ihi - ilo) / (bphi10 - bplo10)) * (a - bplo10) + ilo
    return aqi10
def compute_today_aqi(lat: float, lon: float):
    api_key = "bcf183f11bc94a8ec008ab3d4049ae88"
    url_current = "https://api.openweathermap.org/data/2.5/air_pollution/history"
    data = requests.get(
        url_current,
        params={"lat":lat,
                "lon":lon,
                "start":int((datetime.now()-timedelta(days=1)).timestamp()),
                "end":int((datetime.now()).timestamp()),
                "appid":api_key
               }).json()

    df1 = pd.DataFrame([i["components"] for i in data["list"]])
    if df1 is None or df1.empty:
        return None
    last = df1.iloc[-1]

    pm25 = last["pm2_5"]
    pm10 = last["pm10"]

    aqi25_val = aqi25(pm25, aqi_data)
    aqi10_val = aqi10(pm10, aqi_data)

    final_aqi = max(
        v for v in [aqi25_val, aqi10_val] if v is not None
    )
    return {
        "pm25": float(pm25),
        "pm10": float(pm10),
        "AQI": float(final_aqi),
        "type": "observed",
    }

print(compute_today_aqi(19.076090,72.877426))



