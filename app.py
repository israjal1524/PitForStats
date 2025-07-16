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

    html, body, [class*="css"], h1, h2, h3, h4, h5, h6, .stText, .stMarkdown, .stDataFrame, .stMetricLabel, .stMetricValue {
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

    h1, h2, h3, h4 {
        color: #e10600;
    }
    /* Sidebar container */
section[data-testid="stSidebar"] {
    background-color: #121212 !important;
    padding: 2rem 1rem;
    border-right: 2px solid #e10600;
}

/* Sidebar headings and labels */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label {
    font-family: 'Orbitron', sans-serif !important;
    color: #ffffff !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 500;
}

/* Sidebar select box styling */
section[data-testid="stSidebar"] .stSelectbox > div {
    background-color: #1c1c1c;
    border: 1px solid #444;
    color: white;
    border-radius: 6px;
}

/* Sidebar selected text */
section[data-testid="stSidebar"] .stSelectbox div span {
    color: #e10600 !important;
    font-weight: bold;
}

    </style>
""", unsafe_allow_html=True)

# === F1 Logo + Title
st.markdown("""
    <div style= padding:60px 10px 0;'>
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

    st.markdown(f"## Career Overview: {selected_driver}")
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
        st.markdown("###  Points Over Time")
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
