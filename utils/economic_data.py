import pandas as pd

def load_interest_rates(filepath="data/interest_rates.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])
    return df
