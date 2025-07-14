import streamlit as st
from src.data_loader import load_all_data

# Load data
data = load_all_data()

# Header
st.image("https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg", width=100)
st.title("PitForStats")
st.subheader("Formula 1 Analytics Dashboard")
st.markdown("---")

# Sidebar (optional placeholder for filters)
with st.sidebar:
    st.header("Filters")
    st.markdown("Year filter (coming soon)")
    st.markdown("Driver filter (coming soon)")

# Metrics layout
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Races", len(data['races']))
    st.metric("Total Drivers", len(data['drivers']))

with col2:
    st.metric("Total Constructors", len(data['constructors']))
    st.metric("Total Results", len(data['results']))

st.markdown("---")

# Data previews
st.markdown("### Race Calendar")
st.dataframe(data['races'].head())

st.markdown("### Drivers Overview")
st.dataframe(data['drivers'].head())
