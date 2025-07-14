
import os
import pandas as pd
from kagglehub import dataset_download

# Optional: Use secrets when running on Streamlit Cloud
if "KAGGLE_USERNAME" in os.environ and "KAGGLE_KEY" in os.environ:
    os.environ["KAGGLE_USERNAME"] = os.environ["KAGGLE_USERNAME"]
    os.environ["KAGGLE_KEY"] = os.environ["KAGGLE_KEY"]

def load_all_data():
    # Downloads and caches the Kaggle dataset locally
    base_path = dataset_download("rohanrao/formula-1-world-championship-1950-2020")

    def load(file_name):
        file_path = os.path.join(base_path, file_name)
        return pd.read_csv(file_path)

    return {
        "races": load("races.csv"),
        "drivers": load("drivers.csv"),
        "constructors": load("constructors.csv"),
        "results": load("results.csv")
    }
