import requests
import pandas as pd
import os

# Only CSVs we have
CSV_AVAILABLE = {
    "drivers": "drivers.csv",
    "lap_times": "lap_times.csv",
    "pit_data": "pit_data.csv"
}

API_ENDPOINTS = {
    "drivers": "drivers",
    "lap_times": "lap_times",
    "car_data": "car_data",
    "position_data": "position",
    "pit_data": "pit"
}

def load_from_api(endpoint: str) -> pd.DataFrame:
    try:
        response = requests.get(f"https://api.openf1.org/v1/{endpoint}", timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception:
        return None

def load_from_csv(filename: str) -> pd.DataFrame:
    try:
        path = os.path.join("data", filename)
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

def load_all_data():
    data = {}
    mode = "API"

    for key, endpoint in API_ENDPOINTS.items():
        df = load_from_api(endpoint)

        if (df is None or df.empty):
            # Fallback only if CSV exists for this data type
            if key in CSV_AVAILABLE:
                mode = "CSV"
                df = load_from_csv(CSV_AVAILABLE[key])
            else:
                df = pd.DataFrame()  # keep empty if no CSV fallback

        data[key] = df

    return data, mode
