import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Live F1 Data", layout="centered")

# === Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');

    html, body, [class*="css"] {
        font-family: 'Orbitron', sans-serif !important;
    }
    h1, h2, h3, h4 {
        color: #e10600;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Live F1 Data - Powered by OpenF1 API")
st.markdown("---")

# === Fetch Live Data from OpenF1 API
def get_upcoming_event():
    url = "https://api.openf1.org/v1/sessions"
    try:
        response = requests.get(url)
        sessions = response.json()
        upcoming = [s for s in sessions if s.get("session_end_utc") > datetime.datetime.utcnow().isoformat()]
        if not upcoming:
            return None

        next_race = sorted(upcoming, key=lambda x: x["session_start_utc"])[0]
        return {
            "season": next_race.get("season") or "",
            "event": next_race.get("event_name") or "",
            "location": next_race.get("location") or "",
            "country": next_race.get("country_code") or "",
            "start": next_race.get("session_start_utc") or "",
            "session": next_race.get("session_type") or ""
        }
    except Exception as e:
        return None

# === Display Data
next_gp = get_upcoming_event()
if next_gp:
    st.subheader("Next Grand Prix")
    st.write(f"**Season**: {next_gp['season']}")
    st.write(f"**Event**: {next_gp['event']}")
    st.write(f"**Location**: {next_gp['location']} ({next_gp['country']})")
    st.write(f"**Session Type**: {next_gp['session'].capitalize()}")
    st.write(f"**Start Time (UTC)**: {next_gp['start']}")
else:
    st.warning("Could not fetch upcoming event. API might be down or changed.")

st.markdown("---")
st.info("This is the live page of PitForStats. More live analytics and pole predictions coming soon!")
