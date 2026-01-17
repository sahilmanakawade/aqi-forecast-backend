import pandas as pd
import numpy as np


def build_features(df):
    df = df.copy()
    df = df.sort_values("date")
    for lag in range(1,25):
        df[f"pm2.5lag{lag}"]=df["pm2_5"].shift(lag)
        df[f"pm10lagP{lag}"]=df["pm10"].shift(lag)
    df["pm2.5roll7"]=df["pm2_5"].rolling(7).mean()
    df["pm2.5roll14"]=df["pm2_5"].rolling(14).mean()
    df["pm2.5roll21"]=df["pm2_5"].rolling(21).mean()
    df["pm10roll7"]=df["pm10"].rolling(7).mean()
    df["pm10roll14"]=df["pm10"].rolling(14).mean()
    df["pm10roll21"]=df["pm10"].rolling(21).mean()
    df=df.dropna()
    df.drop(["pm2_5","pm10"],axis=1,inplace=True)
    return df
