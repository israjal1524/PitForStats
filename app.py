import streamlit as st
import pandas as pd
import altair as alt
import os
from src.data_loader import load_all_data

st.set_page_config(page_title="Pit For Stats", layout="wide")

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

# === Load Data
data = load_all_data()

# Ensure 'year' column exists in races
if 'year' not in data['races'].columns:
    data['races']['year'] = pd.to_datetime(data['races']['date']).dt.year

# === Sidebar Filter: Year
available_years = sorted(data['races']['year'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Select Year", available_years, index=0)
races_this_year = data['races'][data['races']['year'] == selected_year]

# === Sidebar Filter: Driver
data['drivers']['driverName'] = data['drivers']['forename'] + ' ' + data['drivers']['surname']
driver_list = data['drivers'].sort_values('surname')['driverName'].tolist()
selected_driver = st.sidebar.selectbox("Select Driver", ["All Drivers"] + driver_list)

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

# === Driver Analysis
if selected_driver != "All Drivers":
    selected_driver_row = data['drivers'][data['drivers']['driverName'] == selected_driver].iloc[0]
    selected_driver_id = selected_driver_row['driverId']

    st.markdown(f"##  Career Overview: {selected_driver}")
    career_results = data['results'][data['results']['driverId'] == selected_driver_id]

    col1, col2, col3 = st.columns(3)
    col1.metric("Races", career_results['raceId'].nunique())
    col2.metric("Wins", (career_results['positionOrder'] == 1).sum())
    col3.metric("Points", int(career_results['points'].sum()))

    joined = career_results.merge(data['races'], on='raceId', how='inner')
    columns_to_show = [col for col in ['year', 'raceName', 'grid', 'positionOrder', 'points'] if col in joined.columns]

    st.markdown("###  Races Participated In")
    st.dataframe(joined[columns_to_show].sort_values(by='year'))

    # === Plot Button
    if st.button(" Plot Career Graph"):
        st.markdown("###  Points Over Time")
        chart_data = joined.groupby('year')['points'].sum().reset_index()
        chart = alt.Chart(chart_data).mark_line(point=True).encode(
            x=alt.X('year:O', title='Year'),
            y=alt.Y('points:Q', title='Total Points'),
            tooltip=['year', 'points']
        ).properties(width=700, height=400)

        st.altair_chart(chart)
else:
    st.info("Select a driver from the sidebar to see their career analysis.")
