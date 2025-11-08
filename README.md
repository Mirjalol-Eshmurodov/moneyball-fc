# Moneyball FC — Football Analytics (StatsBomb Open Data)

End-to-end Python template for scouting players from event data.
Covers: GitHub usage, project org, I/O, manipulation, scientific computing, viz; optional Streamlit app (bonus).

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Download matches (2018 World Cup)
python scripts/download_statsbomb.py matches --competition_id 43 --season_id 3

# Download events for one match (replace ID with any from data/raw/)
python scripts/download_statsbomb.py events --match_id 7581

# Build features and a shot table
python scripts/build_features.py shots-table --competition_id 43 --season_id 3 --match_id 7581

# Make a shot map
python scripts/make_shot_map.py plot --match_id 7581

# (Bonus) Streamlit app
streamlit run app.py
```
> StatsBomb Open Data index: https://github.com/statsbomb/open-data
