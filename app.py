import streamlit as st
from src.data_loader import load_all_data

# Styling and Animated Glowing Title
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

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

    h1.glow-title {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 64px;
        font-weight: 700;
        letter-spacing: 2px;
        color: white;
        text-shadow: 0 0 5px #ff0000,
                     0 0 10px #ff0000,
                     0 0 20px #ff0000,
                     0 0 30px #ff0000;
        animation: glowPulse 2s infinite alternate;
        margin-bottom: 0;
    }

    @keyframes glowPulse {
        from {
            text-shadow: 0 0 5px #ff0000,
                         0 0 10px #ff0000,
                         0 0 15px #ff0000,
                         0 0 20px #ff0000;
        }
        to {
            text-shadow: 0 0 10px #ff1a1a,
                         0 0 20px #ff1a1a,
                         0 0 30px #ff1a1a,
                         0 0 40px #ff1a1a;
        }
    }

    .subtitle {
        text-align: center;
        color: #CCCCCC;
        font-weight: 400;
        font-size: 18px;
        margin-top: 5px;
    }

    hr.fancy-line {
        border: 1px solid #444;
        width: 60%;
        margin: auto;
        margin-top: 20px;
    }
    </style>

    <!-- 🏁 Floating Checkered Flag -->
    <div style='position: fixed; bottom: 20px; right: 20px; z-index: 1000;'>
        <img src='https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif' width='80'>
    </div>

    <h1 class="glow-title">Pit For Stats</h1>
    <h4 class="subtitle">Formula 1 Analytics Dashboard</h4>
    <hr class="fancy-line">
""", unsafe_allow_html=True)

#  Load Data
data = load_all_data()

#  Sidebar
with st.sidebar:
    st.header("Filter Controls")
    st.markdown("Coming soon:")
    st.caption("• Year selector")
    st.caption("• Driver filter")
    st.caption("• Race track selection")

#  Key Stats
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Races", len(data['races']))
    st.metric("Total Drivers", len(data['drivers']))
with col2:
    st.metric("Constructors", len(data['constructors']))
    st.metric("Results Entries", len(data['results']))

st.markdown("---")

#  Data Previews
st.markdown("### Race Calendar")
st.dataframe(data['races'].head())

st.markdown("### Drivers Overview")
st.dataframe(data['drivers'].head())
