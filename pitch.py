from __future__ import annotations
from mplsoccer import Pitch

def shot_map(shots_df, title: str = "Shot Map"):
    pitch = Pitch(pitch_type="statsbomb", pitch_color="white", line_color="black")
    fig, ax = pitch.draw(figsize=(10,7))
    goals = shots_df[shots_df["is_goal"]==1]; misses = shots_df[shots_df["is_goal"]==0]
    if not goals.empty: pitch.scatter(goals["x"], goals["y"], s=80, ax=ax, marker="*", edgecolor="black", zorder=3)
    if not misses.empty: pitch.scatter(misses["x"], misses["y"], s=40, ax=ax, marker="o", edgecolor="black", alpha=0.6, zorder=2)
    ax.set_title(title); return fig, ax
