import streamlit as st
import pandas as pd
from src.data_loader import load_all_data

# === Cockpit Experience Toggle
cockpit_mode = st.sidebar.toggle(" Cockpit Experience Mode", value=True)

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

    <!-- Floating Checkered Flag -->
    <div style='position: fixed; bottom: 20px; right: 20px; z-index: 1000;'>
        <img src='https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif' width='80'>
    </div>
""", unsafe_allow_html=True)

# === F1 Logo
st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg' width='100'>
    </div>
""", unsafe_allow_html=True)

# === Title
st.markdown("<h1 style='text-align: center;'>Pit For Stats</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Formula 1 Analytics Dashboard</h4>", unsafe_allow_html=True)
st.markdown("---")

# === Cockpit FX Scripts
if cockpit_mode:
    st.markdown("""
    <!-- Rev sound on load -->
    <audio id="engineRevOnLoad" autoplay hidden>
      <source src="https://assets.mixkit.co/sfx/preview/mixkit-sports-car-engine-rev-1580.mp3" type="audio/mpeg">
    </audio>
    <script>
      window.addEventListener('load', () => {
        const audio = document.getElementById('engineRevOnLoad');
        if (audio) {
          audio.volume = 0.8;
          audio.play().catch(() => {});
        }
      });
    </script>

    <!-- Scroll-end red flash + rev -->
    <style>
      @keyframes flash {
        0%, 100% { background-color: transparent; }
        50% { background-color: rgba(255, 0, 0, 0.5); }
      }
      .scroll-flash {
        animation: flash 0.5s ease-in-out;
      }
    </style>
    <script>
      window.addEventListener('scroll', function () {
        const atBottom = Math.ceil(window.innerHeight + window.scrollY) >= document.body.scrollHeight;
        if (atBottom) {
          const body = document.body;
          body.classList.add('scroll-flash');
          setTimeout(() => body.classList.remove('scroll-flash'), 500);
          
          const revAudio = new Audio("https://assets.mixkit.co/sfx/preview/mixkit-sports-car-engine-rev-1580.mp3");
          revAudio.volume = 0.9;
          revAudio.play().catch(() => {});
        }
      });
    </script>
    """, unsafe_allow_html=True)

# === Load Data
data = load_all_data()
data['races']['year'] = pd.to_datetime(data['races']['date']).dt.year
available_years = sorted(data['races']['year'].unique(), reverse=True)

# === Sidebar: Year Selection
selected_year = st.sidebar.selectbox("Select Year", available_years, index=0)

# === Filter races
races_this_year = data['races'][data['races']['year'] == selected_year]

# === Metrics Section
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
