import streamlit as st
import pandas as pd
from src.data_loader import load_all_data
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="Pit For Stats", layout="wide")

# === Function to load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

engine_lottie = load_lottie_url("https://lottie.host/2dd92f0c-c9b4-4554-9333-70b521165d2b/YRu6vXoq4q.json")  # Engine rev animation

# === Global styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Orbitron', sans-serif !important;
        background: none;
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
    <div style='text-align: center; padding: 10px 0;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg' width='100'>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Pit For Stats</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Formula 1 Analytics Dashboard</h4>", unsafe_allow_html=True)
st.markdown("---")

# === Cockpit Mode Start
st.subheader("🚀 Start Cockpit Mode")
st_lottie(engine_lottie, speed=1.2, height=200, key="engine")

st.markdown("""
<audio controls>
  <source src="https://assets.mixkit.co/sfx/preview/mixkit-sports-car-engine-rev-1580.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>
""", unsafe_allow_html=True)

st.markdown("---")

# === Load Data
data = load_all_data()
data['races']['year'] = pd.to_datetime(data['races']['date']).dt.year
available_years = sorted(data['races']['year'].unique(), reverse=True)

# === Sidebar Filter
selected_year = st.sidebar.selectbox("Select Year", available_years, index=0)

# === Filtered Data
races_this_year = data['races'][data['races']['year'] == selected_year]

# === Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Races", len(data['races']))
    st.metric("Total Drivers", len(data['drivers']))
with col2:
    st.metric("Constructors", len(data['constructors']))
    st.metric("Results Entries", len(data['results']))

st.markdown("---")

# === Race Calendar
st.markdown(f"### Race Calendar - {selected_year} Season")
st.dataframe(races_this_year.reset_index(drop=True))

# === Driver Overview
st.markdown("### Drivers Overview")
st.dataframe(data['drivers'].head())
