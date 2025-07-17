import streamlit as st
import pandas as pd
import altair as alt
import os
from src.data_loader import load_all_data, get_flag

st.set_page_config(page_title="Pit For Stats")

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

    .sidebar .sidebar-content {
        background-color: #0f0f0f;
        color: white;
    }

    </style>
""", unsafe_allow_html=True)

# === F1 Logo + Title
st.markdown("""
    <div style='text-align: center; padding: 50px 0 10px 0;'>
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
st.sidebar.markdown("""<h3 style='color: #e10600;'>Analytics Controls</h3>""", unsafe_allow_html=True)
available_years = sorted(data['races']['year'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Select Year", available_years, index=0)
races_this_year = data['races'][data['races']['year'] == selected_year]

# === Sidebar Filter: Driver
data['drivers']['driverFlagged'] = data['drivers'].apply(
    lambda row: f"{get_flag(row['nationality'])} {row['forename']} {row['surname']}", axis=1
)
driver_list = data['drivers'].sort_values('surname')['driverFlagged'].tolist()
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
    driver_name_only = selected_driver.split(' ', 1)[1]
    selected_driver_row = data['drivers'][data['drivers']['driverFlagged'] == selected_driver].iloc[0]
    selected_driver_id = selected_driver_row['driverId']

    st.markdown(f"## Career Overview: {driver_name_only}")
    career_results = data['results'][data['results']['driverId'] == selected_driver_id]

    col1, col2, col3 = st.columns(3)
    col1.metric("Races", career_results['raceId'].nunique())
    col2.metric("Wins", (career_results['positionOrder'] == 1).sum())
    col3.metric("Points", int(career_results['points'].sum()))

    joined = career_results.merge(data['races'], on='raceId', how='inner')
    if 'year' not in joined.columns:
        joined['year'] = pd.to_datetime(joined['date']).dt.year

    columns_to_show = [col for col in ['year', 'raceName', 'grid', 'positionOrder', 'points'] if col in joined.columns]
    st.markdown("### Races Participated In")
    st.dataframe(joined[columns_to_show].sort_values(by='year'))

    # === Plot Button
    if st.button(" Plot Career Graph"):
        st.markdown("### Points Over Time")
        chart_data = joined.groupby('year')['points'].sum().reset_index()

        base = alt.Chart(chart_data).encode(
            x=alt.X('year:O', title='Season', axis=alt.Axis(labelFont='Orbitron', titleFont='Orbitron')),
            y=alt.Y('points:Q', title='Total Points', axis=alt.Axis(labelFont='Orbitron', titleFont='Orbitron'))
        )

        line = base.mark_line(
            color='#e10600',
            strokeWidth=3
        )

        points = base.mark_circle(
            size=80,
            color='white',
            opacity=1,
            stroke='#e10600',
            strokeWidth=2
        )

        final_chart = (line + points).properties(
            width=700,
            height=400,
            background='#0f0f0f'
        ).configure_view(
            stroke=None
        )

        st.altair_chart(final_chart)
else:
    st.info("Select a driver from the sidebar to see their career analysis.")
