import streamlit as st
from src.data_loader import load_all_data

# Custom Styling
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

# Load Data
data = load_all_data()
available_years = sorted(data["races"]["year"].unique(), reverse=True)

# Header
st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg", width=100)
st.markdown("<h1 style='text-align: center;'>PitForStats</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Formula 1 Analytics Dashboard</h4>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Filter Controls")

    selected_year = st.selectbox(
        "Select Year",
        available_years,
        index=0,
        help="Choose a season to view race data"
    )


# 📈 Stats
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Races", len(data['races']))
    st.metric("Total Drivers", len(data['drivers']))
with col2:
    st.metric("Constructors", len(data['constructors']))
    st.metric("Results Entries", len(data['results']))

st.markdown("---")

# 🧾 Data Previews
# Filter races by selected year
races_this_year = data["races"][data["races"]["year"] == selected_year]

st.markdown(f"### Race Calendar - {selected_year} Season")
st.dataframe(races_this_year.reset_index(drop=True))


st.markdown("### Drivers Overview")
st.dataframe(data['drivers'].head())
