import pandas as pd

def load_csv(filename):
    return pd.read_csv(f"data/{filename}")

def load_all_data():
    return {
        "races": load_csv("races.csv"),
        "results": load_csv("results.csv"),
        "drivers": load_csv("drivers.csv"),
        "constructors": load_csv("constructors.csv"),
    }
