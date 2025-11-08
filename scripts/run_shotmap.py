# scripts/run_shotmap.py
from pathlib import Path
import json
import numpy as np
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt

# ---- PATHS ----
ROOT = Path(__file__).resolve().parent.parent      # .../moneyball-fc-starter
RAW = ROOT / "raw"
PROC = ROOT / "data" / "processed"
VIZ = ROOT / "visualisations"
PROC.mkdir(parents=True, exist_ok=True)
VIZ.mkdir(parents=True, exist_ok=True)

# ---- CONFIG ----
match_id = 2275117
events_path = RAW / f"events_{match_id}.json"
matches_path = RAW / "matches_43_3.json"          # 2018 World Cup

# ---- LOAD JSONS ----
with open(events_path, "r", encoding="utf-8") as f:
    events = json.load(f)
df = pd.DataFrame(events)

# match info
home_away = None
try:
    with open(matches_path, "r", encoding="utf-8") as f:
        matches = pd.DataFrame(json.load(f))
    row = matches[matches["match_id"] == match_id].iloc[0]
    home_away = f'{row["home_team"]["name"]} vs {row["away_team"]["name"]} — {row["match_date"]}'
except Exception:
    home_away = f"Match {match_id}"

# ---- FILTER SHOTS ----
is_shot = df["type"].apply(lambda x: isinstance(x, dict) and x.get("name") == "Shot")
shots = df[is_shot].copy()

# basic columns
shots["team"] = shots["team"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
shots["player"] = shots["player"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
shots["outcome"] = shots["shot"].apply(lambda s: s.get("outcome", {}).get("name") if isinstance(s, dict) else None)

# coordinates (StatsBomb pitch 120x80)
def get_xy(row):
    loc = row.get("location", None)
    if isinstance(loc, list) and len(loc) >= 2:
        return pd.Series({"x": loc[0], "y": loc[1]})
    return pd.Series({"x": np.nan, "y": np.nan})
shots[["x", "y"]] = shots.apply(get_xy, axis=1)

# simple xG proxy (course-safe)
goal_x, goal_y = 120.0, 40.0
dx = (goal_x - shots["x"]).clip(lower=1e-6)
dy = (goal_y - shots["y"]).abs().clip(lower=1e-6)
dist = np.hypot(dx, dy)
angle = np.arctan2(7.32 / 2, dist)
shots["xg_proxy"] = 1 / (1 + np.exp(-(1.2 * angle - 0.04 * dist)))
shots["is_goal"] = (shots["outcome"] == "Goal").astype(int)

# ---- SAVE TABLES ----
shots_out = PROC / f"shots_{match_id}.parquet"
shots.to_parquet(shots_out, index=False)

player_summary = (
    shots.groupby(["team", "player"])
         .agg(shots=("x", "count"),
              goals=("is_goal", "sum"),
              xg_proxy=("xg_proxy", "sum"),
              xg_per_shot=("xg_proxy", "mean"))
         .reset_index()
         .sort_values(["xg_per_shot", "shots"], ascending=[False, False])
)
summary_out = PROC / f"player_summary_{match_id}.csv"
player_summary.to_csv(summary_out, index=False)

# ---- PLOT SHOT MAP ----
pitch = Pitch(pitch_type="statsbomb", pitch_color="white", line_color="black")
fig, ax = pitch.draw(figsize=(10, 7))
goals = shots[shots["is_goal"] == 1]
misses = shots[shots["is_goal"] == 0]
if len(goals):
    pitch.scatter(goals["x"], goals["y"], s=80, ax=ax, marker="*", edgecolor="black", zorder=3)
if len(misses):
    pitch.scatter(misses["x"], misses["y"], s=40, ax=ax, marker="o", edgecolor="black", alpha=0.6, zorder=2)
title = f"{home_away} — Shot Map" if home_away else f"Match {match_id} — Shot Map"
ax.set_title(title)

png_path = VIZ / f"shot_map_{match_id}.png"
fig.savefig(png_path, dpi=200, bbox_inches="tight")

print("✅ Saved:", shots_out)
print("✅ Saved:", summary_out)
print("✅ Saved:", png_path)