import pandas as pd

REQUIRED_COLUMNS = {'Open', 'High', 'Low', 'Close', 'Volume'}

def load_data(path):
    df = pd.read_csv(path)

    # Validate required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    # Auto-detect and parse a date column, set as index
    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col])
            df.set_index(col, inplace=True)
            df.sort_index(inplace=True)
            break

    df.dropna(inplace=True)
    return df

def add_indicators(df):
    df = df.copy()
    df["SMA"] = df["Close"].rolling(5).mean()
    df["EMA"] = df["Close"].ewm(span=5).mean()
    df.dropna(inplace=True)
    return df
