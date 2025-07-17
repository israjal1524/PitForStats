import streamlit as st
from src.data_loader import load_all_data

st.set_page_config(page_title="PitForStats Dashboard")

# Title
st.title(" PitForStats – Formula 1 Live Dashboard")

# Load data
with st.spinner("Fetching race data..."):
    data, mode = load_all_data()

# Feedback on source
if all(df.empty for df in data.values()):
    st.error("Failed to load any data from API or CSV.")
elif mode == "API":
    st.success("Live data loaded from OpenF1 API.")
else:
    st.warning("Offline Mode: Some datasets loaded from CSV.")

# Show summary
st.subheader("Dataset Summary")
for name, df in data.items():
    st.markdown(f"### {name.upper()}")
    if df.empty:
        st.error(f"No data available for `{name}`.")
    else:
        st.success(f"Loaded {len(df)} rows.")
        st.dataframe(df.head(), use_container_width=True)
