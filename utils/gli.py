import pandas as pd

def load_gli_data(filepath="data/gli.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df

def calculate_gli_index(df):
    df = df.copy()
    components = ["fed_balance", "ecb_balance", "boj_balance", "pboc_reserves"]
    for col in components:
        df[col + "_norm"] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    df["GLI"] = df[[c + "_norm" for c in components]].mean(axis=1)
    return df[["date", "GLI"]]
