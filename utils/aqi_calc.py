def aqi25(a,aqi_data):
    row=aqi_data[(aqi_data["bplo2.5"] <= a) & (aqi_data["bphi2.5"] >= a)]
    ihi=aqi_data["ihi"].iloc[0]
    ilo=aqi_data["ilo"].iloc[0]
    bphi2_5=aqi_data["bphi2.5"].iloc[0]
    bplo2_5=aqi_data["bplo2.5"].iloc[0]
    aqi2_5=((ihi - ilo) / (bphi2_5 - bplo2_5)) * (a - bplo2_5) + ilo
    return aqi2_5
def aqi10(a,aqi_data):
    row=aqi_data[(aqi_data["bplopm10"] <= a) & (aqi_data["bphipm10"] >= a)]
    ihi=aqi_data["ihi"].iloc[0]
    ilo=aqi_data["ilo"].iloc[0]
    bphi10=aqi_data["bphipm10"].iloc[0]
    bplo10=aqi_data["bplopm10"].iloc[0]
    aqi10=((ihi - ilo) / (bphi10 - bplo10)) * (a - bplo10) + ilo
    return aqi10

def compute_today_aqi(df, df2_5, df10):
    if df is None or df.empty:
        return None

    last = df.iloc[-1]

    pm25 = last.get("pm25")
    pm10 = last.get("pm10")

    if pm25 is None or pm10 is None:
        return None

    aqi25 = aqi(pm25, df2_5)
    aqi10 = aqi(pm10, df10)

    if aqi25 is None and aqi10 is None:
        return None

    return {
        "date": str(last["date"]),
        "pm25": float(pm25),
        "pm10": float(pm10),
        "AQI": float(max(aqi25 or 0, aqi10 or 0)),
        "type": "observed",
    }
