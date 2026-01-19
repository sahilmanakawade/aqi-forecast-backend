import requests
import numpy as np
import pandas as pd
from datetime import datetime,timedelta
import warnings
warnings.simplefilter("ignore")
aqi_data={
    "ihi":[50,100,200,300,400,500,700],
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

def aqi25(a,aqi_data):
    row=aqi_data[(aqi_data["bplo2.5"] <= a) & (aqi_data["bphi2.5"] >= a)]
    ihi=aqi_data["ihi"].iloc[0]
    ilo=aqi_data["ilo"].iloc[0]
    bphi2_5=aqi_data["bphi2.5"].iloc[0]
    bplo2_5=aqi_data["bplo2.5"].iloc[0]

    aqi2_5=((ihi - ilo) / (bphi2_5 - bplo2_5)) * (a - bplo2_5) + ilo
    return aqi2_5
def aqi10(a,aqi_data):
@@ -64,22 +56,8 @@
    ).json()

    df1 = pd.DataFrame([i["components"] for i in data["list"]])

    if df1.empty:

    ihi=aqi_data["ihi"].iloc[0]
    ilo=aqi_data["ilo"].iloc[0]
    bphi10=aqi_data["bphipm10"].iloc[0]
    bplo10=aqi_data["bplopm10"].iloc[0]
    aqi10=((ihi - ilo) / (bphi10 - bplo10)) * (a - bplo10) + ilo
    return aqi10

def compute_today_aqi(df, df2_5, df10):
    if df is None or df.empty:

    if df1 is None or df1.empty:
        return None


    last = df1.iloc[-1]

    pm25 = last["pm2_5"]
@@ -91,11 +69,11 @@
    final_aqi = max(
        v for v in [aqi25_val, aqi10_val] if v is not None
    )

    return {
        "pm25": float(pm25),
        "pm10": float(pm10),
        "AQI": float(final_aqi),
        "type": "observed",
    }
