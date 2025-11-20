import streamlit as st
import pandas as pd
from pathlib import Path
from src.visualize.pitch import shot_map

st.set_page_config(page_title="Moneyball FC", layout="centered")
st.title("Moneyball FC — Quick Dashboard")

match_id = st.text_input("Enter match_id", "7581")
shots_path = Path("data/processed") / f"shots_{match_id}.parquet"
if shots_path.exists():
    shots = pd.read_parquet(shots_path)
    st.write("Shots table", shots.head())
    fig, ax = shot_map(shots, title=f"Match {match_id} — Shot Map")
    st.pyplot(fig)
else:
    st.info("No processed shots found. First run: python scripts/build_features.py shots-table --competition_id 43 --season_id 3 --match_id <ID>")
