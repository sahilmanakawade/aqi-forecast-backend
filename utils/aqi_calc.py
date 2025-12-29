def aqi(c, dfp):
    """
    Calculate CPCB AQI sub-index for a given concentration c
    using breakpoint table dfp
    """
    row = dfp[(dfp["BPhi"] > c) & (dfp["BPlo"] <= c)]

    if row.empty:
        return None

    Ihi = row["Ihi"].iloc[0]
    Ilo = row["Ilo"].iloc[0]
    BPhi = row["BPhi"].iloc[0]
    BPlo = row["BPlo"].iloc[0]

    return ((Ihi - Ilo) / (BPhi - BPlo)) * (c - BPlo) + Ilo


def compute_today_aqi(df, df2_5, df10):
    """
    Compute today's observed AQI using real PM values
    (NO machine learning here)
    """
    last = df.iloc[-1]

    aqi25 = aqi(last["pm2.5"], df2_5)
    aqi10 = aqi(last["pm10"], df10)

    return {
        "date": str(last["date"]),
        "pm2.5": float(last["pm2.5"]),
        "pm10": float(last["pm10"]),
        "AQI": float(max(aqi25, aqi10)),
        "type": "observed"
    }


