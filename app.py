import streamlit as st
import pandas as pd
from src.data_loader import load_all_data

# 🎨 Styling and visuals
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

#  Title
st.markdown("<h1 style='text-align: center;'>Pit For Stats</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Formula 1 Analytics Dashboard</h4>", unsafe_allow_html=True)
st.markdown("---")

# Load data
data = load_all_data()

#  Extract 'year' from 'date' column in races
data['races']['year'] = pd.to_datetime(data['races']['date']).dt.year
available_years = sorted(data['races']['year'].unique(), reverse=True)

# 📊 Sidebar filters
with st.sidebar:
    st.header("Filter Controls")
    selected_year = st.selectbox("Select Year", available_years, index=0)

#  Filtered races
races_this_year = data['races'][data['races']['year'] == selected_year]

#  Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Races", len(data['races']))
    st.metric("Total Drivers", len(data['drivers']))
with col2:
    st.metric("Constructors", len(data['constructors']))
    st.metric("Results Entries", len(data['results']))

st.markdown("---")

#  Filtered race calendar
st.markdown(f"### Race Calendar - {selected_year} Season")
st.dataframe(races_this_year.reset_index(drop=True))

#  Drivers Overview
st.markdown("### Drivers Overview")
st.dataframe(data['drivers'].head())
