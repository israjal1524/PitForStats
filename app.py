import streamlit as st
from src.data_loader import load_all_data

# Custom UI styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Orbitron', sans-serif !important;
    }

    .stApp {
      background: url("https://i.ibb.co/WgK3W8P/racetrack-bg.jpg") no-repeat center center fixed;
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

    <div style='position: fixed; bottom: 20px; right: 20px; z-index: 1000;'>
        <img src='https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif' width='80'>
    </div>
""", unsafe_allow_html=True)

# Load all F1 data
data = load_all_data()

# Header
st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg", width=100)
st.markdown("<h1 style='text-align: center;'>PitForStats</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Formula 1 Analytics Dashboard</h4>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Filter Controls")
    st.markdown("Coming soon:")
    st.caption("• Year selector")
    st.caption("• Driver filter")
    st.caption("• Race track selection")

# Metrics
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Races", len(data['races']))
    st.metric("Total Drivers", len(data['drivers']))
with col2:
    st.metric("Constructors", len(data['constructors']))
    st.metric("Results Entries", len(data['results']))

st.markdown("---")

# Data previews
st.markdown("### Race Calendar")
st.dataframe(data['races'].head())

st.markdown("### Drivers Overview")
st.dataframe(data['drivers'].head())
