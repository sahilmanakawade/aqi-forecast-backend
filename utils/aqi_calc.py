def aqi(c, dfp):
    row = dfp[(dfp["BPhi"] > c) & (dfp["BPlo"] <= c)]
    if row.empty:
        return None

    Ihi, Ilo = row["Ihi"].iloc[0], row["Ilo"].iloc[0]
    BPhi, BPlo = row["BPhi"].iloc[0], row["BPlo"].iloc[0]

    return ((Ihi - Ilo) / (BPhi - BPlo)) * (c - BPlo) + Ilo


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
