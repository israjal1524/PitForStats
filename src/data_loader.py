# src/data_loader.py

import pandas as pd
import os

DATA_PATH = "data"

def load_csv(filename):
    path = os.path.join(DATA_PATH, filename)
    return pd.read_csv(path)

def load_all_data():
    races = load_csv("races.csv")
    results = load_csv("results.csv")
    drivers = load_csv("drivers.csv")
    constructors = load_csv("constructors.csv")
    pit_stops = load_csv("pit_stops.csv")

    return {
        "races": races,
        "results": results,
        "drivers": drivers,
        "constructors": constructors,
        "pit_stops": pit_stops
    }

