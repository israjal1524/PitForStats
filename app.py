import streamlit as st
from src.data_loader import load_all_data

# ----- Custom Style -----
st.markdown("""
    <style>
        body {
            background-image: url("https://i.ibb.co/GsRX8bp/carbon.jpg");
            background-size: cover;
        }
        .main {
            font-family: 'Orbitron', sans-serif;
            color: white;
        }
        .css-1v0mbdj, .stApp {
            background-color: transparent;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ----- Title and Sidebar -----
st.title("🏎️ PitForStats – Formula 1 Analytics Dashboard")

with st.sidebar:
    st.header("🔧 Analytics Controls")
    selected_sections = st.multiselect(
        "Select sections to display:",
        ["Car Data", "Position Data", "Race Data", "Lap Times", "Pit Stops"],
        default=["Car Data", "Position Data"]
    )
    st.markdown("---")
    st.info("Live API fallback enabled.\nIf API fails, fallback to offline data.")

# ----- Load Data -----
data = load_all_data()

# ----- Main Display -----
st.markdown("### 📊 Dataset Overview")
for section in selected_sections:
    key = section.lower().replace(" ", "_")
    df = data.get(key, pd.DataFrame())
    
    st.subheader(f"📁 {section}")
    if df.empty:
        st.error(f"{section} is unavailable.")
    else:
        st.dataframe(df.head(30), use_container_width=True)
