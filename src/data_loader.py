import pandas as pd
import requests

def fetch_data_from_api(endpoint, params=None):
    base_url = "https://api.openf1.org/v1"
    url = f"{base_url}/{endpoint}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json())

def load_all_data():
    try:
        races = fetch_data_from_api("sessions", {"session_type": "R"})
        results = fetch_data_from_api("results")
        drivers = fetch_data_from_api("drivers")
        constructors = fetch_data_from_api("teams")  # If available

        return {
            "races": races,
            "results": results,
            "drivers": drivers,
            "constructors": constructors
        }
    except:
        # Fallback to local CSVs if API fails
        print("Using local backup CSVs")
        return {
            "races": pd.read_csv("data/races.csv"),
            "results": pd.read_csv("data/results.csv"),
            "drivers": pd.read_csv("data/drivers.csv"),
            "constructors": pd.read_csv("data/constructors.csv")
        }
