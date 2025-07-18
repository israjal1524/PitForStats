import streamlit as st
import pandas as pd
import requests

# --- Fetch last race results ---
@st.cache_data(ttl=300)
def fetch_last_results():
    url = "https://ergast.com/api/f1/current/last/results.json"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        results = data['MRData']['RaceTable']['Races'][0]['Results']
        df = pd.DataFrame(results)
        df = df[['position', 'Driver', 'Constructor', 'grid', 'laps', 'status', 'Time', 'FastestLap']]
        # flatten nested columns
        df['Driver'] = df['Driver'].apply(lambda d: d['givenName'] + ' ' + d['familyName'])
        df['Constructor'] = df['Constructor'].apply(lambda d: d['name'])
        df['Time'] = df['Time'].apply(lambda t: t['time'] if t else None)
        df['FastestLap'] = df['FastestLap'].apply(lambda f: f['Time']['time'] if f else None)
        return df
    except Exception as e:
        st.warning("Could not fetch live data — showing fallback example.")
        return pd.DataFrame({
            'position': ['1','2','3'],
            'Driver': ['Lando Norris','Oscar Piastri','Nico Hülkenberg'],
            'Constructor': ['McLaren','McLaren','Haas'],
            'grid': [3,2,19],
            'laps': [52,52,52],
            'status': ['Finished','Finished','Finished'],
            'Time': ['1:30:00', '1:30:10', '1:30:20'],
            'FastestLap': ['1:30.5','1:31.2','1:32.0']
        })

# --- Main display ---
st.header("🏆 Last Grand Prix Results")
df = fetch_last_results()
st.table(df)

# --- Podium Image ---
st.subheader("Podium Finishers")
st.image(
    "https://images.unsplash.com/photo-1595855014810-77fb13c92901",
    caption="Race winners celebrating on the podium",
    use_column_width=True
)
