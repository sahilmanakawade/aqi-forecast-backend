import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values("date")

    # Lag features (PM2.5 → pm25)
    df["pm25_lag1"] = df["pm25"].shift(1)
    df["pm10_lag1"] = df["pm10"].shift(1)

    df["pm25_lag2"] = df["pm25"].shift(2)
    df["pm10_lag2"] = df["pm10"].shift(2)

    df["pm25_lag3"] = df["pm25"].shift(3)
    df["pm10_lag3"] = df["pm10"].shift(3)

    # Rolling mean
    df["pm25_roll7"] = df["pm25"].rolling(7).mean()
    df["pm10_roll7"] = df["pm10"].rolling(7).mean()

    # Drop NaNs created by lags/rolling
    df = df.dropna().reset_index(drop=True)

    return df
