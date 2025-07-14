import os
import pandas as pd
from kagglehub import dataset_download

# Optional: Set Kaggle credentials if running on Streamlit Cloud
if "KAGGLE_USERNAME" in os.environ and "KAGGLE_KEY" in os.environ:
    os.environ["KAGGLE_USERNAME"] = os.environ["KAGGLE_USERNAME"]
    os.environ["KAGGLE_KEY"] = os.environ["KAGGLE_KEY"]

def load_all_data():
    """
    Downloads the F1 dataset from KaggleHub (cached after first run)
    and loads required CSV files into a dictionary of DataFrames.
    """
    try:
        base_path = dataset_download("rohanrao/formula-1-world-championship-1950-2020")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to download dataset: {e}")

    def load(file_name):
        path = os.path.join(base_path, file_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {file_name}")
        return pd.read_csv(path)

    return {
        "races": load("races.csv"),
        "drivers": load("drivers.csv"),
        "constructors": load("constructors.csv"),
        "results": load("results.csv"),
        # You can add more below as needed
        # "lap_times": load("lap_times.csv"),
        # "qualifying": load("qualifying.csv"),
        # "pit_stops": load("pit_stops.csv")
    }
