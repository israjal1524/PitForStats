import streamlit as st
from src.data_loader import load_all_data  # Import the data loading function

# Main dashboard title
st.title("PitForStats – Data Load Test")

# Call the function to load all datasets
data = load_all_data()

# Display each dataset with a header and table
st.write("Previewing datasets:")
for name, df in data.items():
    st.subheader(name.upper())
    st.dataframe(df.head(5))  # Shows first 5 rows of each dataset
