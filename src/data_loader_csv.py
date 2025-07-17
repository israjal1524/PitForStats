import pandas as pd
import os

DATA_PATH = "data"
FILES_TO_LOAD = ["races", "results", "drivers", "constructors"]

def load_csv(name):
    path = os.path.join(DATA_PATH, f"{name}.csv")
    return pd.read_csv(path)

def load_all_data():
    data = {}
    for name in FILES_TO_LOAD:
        try:
            data[name] = load_csv(name)
        except FileNotFoundError:
            print(f"Warning: {name}.csv not found, skipping.")
    return data
