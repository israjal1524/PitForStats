import streamlit as st
import pandas as pd
import requests

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

    <!-- 🏁 Floating Checkered Flag -->
    <div style='position: fixed; bottom: 20px; right: 20px; z-index: 1000;'>
        <img src='https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif' width='80'>
    </div>
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

last_race = fetch_last_race()

if last_race:
    st.markdown(f"### 🏁 Last Grand Prix: {last_race['raceName']}")
    st.markdown(f"**Location:** {last_race['location']}, {last_race['country']}")
    st.markdown(f"**Circuit:** {last_race['circuit']}")
    st.markdown(f"**Date:** {last_race['date']}")
    st.markdown(f"**Round:** {last_race['round']}")
else:
    st.error("Failed to load last race information.")
