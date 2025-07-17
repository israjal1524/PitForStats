import pandas as pd
import requests
import os

DATA_DIR = "data"

def fetch_from_api(endpoint: str):
    url = f"https://api.openf1.org/v1/{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        if not df.empty:
            df.to_csv(os.path.join(DATA_DIR, f"{endpoint}.csv"), index=False)
        return df
    except:
        return None

def fetch_from_csv(endpoint: str):
    try:
        return pd.read_csv(os.path.join(DATA_DIR, f"{endpoint}.csv"))
    except:
        return pd.DataFrame()

def load_data(endpoint: str):
    df = fetch_from_api(endpoint)
    if df is not None and not df.empty:
        return df
    return fetch_from_csv(endpoint)

def load_all_data():
    endpoints = [
        "car_data", 
        "position_data", 
        "race_data", 
        "lap_times", 
        "pit_stops"
    ]
    data = {}
    for ep in endpoints:
        data[ep] = load_data(ep)
    return data
