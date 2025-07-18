import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timezone

st.set_page_config(page_title="Live F1 Data", layout="wide")

# === Global styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Orbitron', sans-serif !important;
    }

    .stApp {
        background: url('https://i.postimg.cc/CLVt0CWN/pitforstats-back.gif') no-repeat center center fixed;
        background-size: cover;
        color: white;
    }

    .block-container {
        background-color: rgba(0, 0, 0, 0.75);
        padding: 2rem;
        border-radius: 10px;
    }

    section[data-testid="stSidebar"] > div:first-child {
        position: relative;
        z-index: 1;
        padding: 20px;
        border-radius: 0 10px 10px 0;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    .sidebar-title {
        font-family: 'Orbitron', sans-serif;
        color: #e10600;
        font-size: 20px;
        padding-bottom: 10px;
    }

    h1, h2, h3, h4 {
        color: #e10600;
    }
    </style>
""", unsafe_allow_html=True)

# === F1 Logo + Title
st.markdown("""
    <div style='text-align: center; padding: 40px 0 10px 0;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg' width='100'>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Live F1 Data</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Powered by OpenF1 API</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- Fetch last race results ---
@st.cache_data(ttl=300)
def fetch_last_results():
    url = "https://ergast.com/api/f1/current/last/results.json"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        results = data['MRData']['RaceTable']['Races'][0]['Results']
        df = pd.DataFrame(results)
        df = df[['position', 'Driver', 'Constructor', 'grid', 'laps', 'status', 'Time', 'FastestLap']]
        # flatten nested columns
        df['Driver'] = df['Driver'].apply(lambda d: d['givenName'] + ' ' + d['familyName'])
        df['Constructor'] = df['Constructor'].apply(lambda d: d['name'])
        df['Time'] = df['Time'].apply(lambda t: t['time'] if t else None)
        df['FastestLap'] = df['FastestLap'].apply(lambda f: f['Time']['time'] if f else None)
        return df
    except Exception as e:
        st.warning("Could not fetch live data — showing fallback example.")
        return pd.DataFrame({
            'position': ['1','2','3'],
            'Driver': ['Lando Norris','Oscar Piastri','Nico Hülkenberg'],
            'Constructor': ['McLaren','McLaren','Haas'],
            'grid': [3,2,19],
            'laps': [52,52,52],
            'status': ['Finished','Finished','Finished'],
            'Time': ['1:30:00', '1:30:10', '1:30:20'],
            'FastestLap': ['1:30.5','1:31.2','1:32.0']
        })

# --- Main display ---
st.header("Last Grand Prix Results")
df = fetch_last_results()
st.table(df)
