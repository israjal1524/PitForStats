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

# === Fetch Last Race Info
def fetch_last_race():
    url = "https://ergast.com/api/f1/current/last.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        race = data['MRData']['RaceTable']['Races'][0]
        return {
            'raceName': race['raceName'],
            'circuit': race['Circuit']['circuitName'],
            'location': race['Circuit']['Location']['locality'],
            'country': race['Circuit']['Location']['country'],
            'date': race['date'],
            'round': race['round']
        }
    else:
        return None

def is_race_live(race_date_str):
    try:
        race_time = datetime.strptime(race_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return race_time <= now <= race_time.replace(hour=race_time.hour + 3)
    except:
        return False

# === Fetch Last Race Results
@st.cache_data(ttl=300)
def fetch_last_results():
    url = "https://ergast.com/api/f1/current/last/results.json"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        results = data['MRData']['RaceTable']['Races'][0]['Results']
        df = pd.DataFrame(results)
        df['Driver'] = df['Driver'].apply(lambda d: d['givenName'] + ' ' + d['familyName'])
        df['Constructor'] = df['Constructor'].apply(lambda d: d['name'])
        df['Time'] = df['Time'].apply(lambda t: t['time'] if t else None)
        df['FastestLap'] = df['FastestLap'].apply(lambda f: f['Time']['time'] if f and 'Time' in f else None)
        df = df[['position', 'Driver', 'Constructor', 'grid', 'laps', 'status', 'Time', 'FastestLap']]
        return df
    except:
        return pd.DataFrame()

# === Fetch Lap Times (Optional Extension)
@st.cache_data(ttl=300)
def fetch_lap_times():
    url = "https://ergast.com/api/f1/current/last/laps.json?limit=200"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        laps = data['MRData']['RaceTable']['Races'][0]['Laps']
        lap_data = []
        for lap in laps:
            for timing in lap['Timings']:
                lap_data.append({
                    'lap': int(lap['number']),
                    'driverId': timing['driverId'],
                    'position': int(timing['position']),
                    'time': timing['time']
                })
        return pd.DataFrame(lap_data)
    except:
        return pd.DataFrame()

last_race = fetch_last_race()

if last_race:
    if is_race_live(last_race['date']):
        st.success("Race is LIVE! Stay tuned for live updates.")
        st.markdown(f"###  Live Grand Prix: {last_race['raceName']}")
    else:
        st.info("No race is currently live.")
        st.markdown(f"###  Last Grand Prix: {last_race['raceName']}")

    st.markdown(f"**Location:** {last_race['location']}, {last_race['country']}")
    st.markdown(f"**Circuit:** {last_race['circuit']}")
    st.markdown(f"**Date:** {last_race['date']}")
    st.markdown(f"**Round:** {last_race['round']}")
else:
    st.error("Failed to load last race information.")

# === Optional: Lap Times (under development)
lap_df = fetch_lap_times()
if not lap_df.empty:
    st.subheader("⏱ Lap Times Overview")
    st.dataframe(lap_df.head(50))
else:
    st.warning("Lap time data not available for the last race.")
