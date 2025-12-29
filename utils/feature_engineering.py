import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df.sort_values("date")

    # Lag features
    df["pm2.5_lag1"] = df["pm2.5"].shift(1)
    df["pm10_lag1"] = df["pm10"].shift(1)

    df["pm2.5_lag2"] = df["pm2.5"].shift(2)
    df["pm10_lag2"] = df["pm10"].shift(2)

    df["pm2.5_lag3"] = df["pm2.5"].shift(3)
    df["pm10_lag3"] = df["pm10"].shift(3)

    # Rolling mean
    df["pm2.5_roll7"] = df["pm2.5"].rolling(7).mean()
    df["pm10_roll7"] = df["pm10"].rolling(7).mean()

    # Drop NaNs from lag/rolling
    df = df.dropna().reset_index(drop=True)

    return df
