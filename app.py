import streamlit as st
from src.data_loader import load_all_data

st.title("PitForStats – Data Load Test")

data = load_all_data()
st.write(" Previewing datasets:")

for name, df in data.items():
    st.subheader(name.upper())
    st.dataframe(df.head(5))

