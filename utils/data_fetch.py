import requests
import numpy as np
import pandas as pd
from datetime import datetime,timedelta,UTC
import json
def fetch_recent_data(lat,lon):
    api_key="bcf183f11bc94a8ec008ab3d4049ae88"
    url_air = "https://api.openweathermap.org/data/2.5/air_pollution/history"
    response=requests.get(url_air,
                          params={
                              "lat":lat,
                              "lon":lon,
                              "start": int((datetime.now()-timedelta(days=100)).timestamp()),
                              "end": int((datetime.now()).timestamp()),
                              "appid" : api_key
                          })
    data=response.text
    df=json.loads(data)
    date=[]
    for i in df["list"]:
        date.append(i["dt"])
    components=[]
    for i in df["list"]:
        components.append(i["components"])
    date=pd.DataFrame(date)
    components=pd.DataFrame(components)
    components.drop(["no","no2","o3","so2","nh3","co"],axis=1,inplace=True)
    df=pd.concat([date,components],axis=1)
    df.columns=["date","pm2_5","pm10"]
    df["date"]=df["date"].apply(lambda x : datetime.fromtimestamp(x))
    df["date"]=df["date"].dt.date
    df=df.groupby("date")[["pm2_5","pm10"]].mean().reset_index()
    return df
