def aqi(c, dfp):
    """
    Calculate CPCB AQI sub-index for a given concentration c
    using breakpoint table dfp
    """
    if c is None:
        return None

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
    Compute today's observed AQI using real PM values.
    Safe against empty or missing data.
    """

    # 🚨 SAFETY CHECK (CRITICAL)
    if df is None or df.empty:
        return None

    last = df.iloc[-1]

    aqi25 = aqi(last.get("pm2.5"), df2_5)
    aqi10 = aqi(last.get("pm10"), df10)

    if aqi25 is None and aqi10 is None:
        return None

    return {
        "date": str(last["date"]),
        "pm2.5": float(last["pm2.5"]),
        "pm10": float(last["pm10"]),
        "AQI": float(max(aqi25 or 0, aqi10 or 0)),
        "type": "observed"
    }
