from __future__ import annotations
import pandas as pd, numpy as np

def shot_features(events: pd.DataFrame) -> pd.DataFrame:
    # filter shots
    shots = events[events["type"].apply(lambda x: isinstance(x, dict) and x.get("name")=="Shot")].copy()
    if shots.empty: return pd.DataFrame()
    shots["team"] = shots["team"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
    shots["player"] = shots["player"].apply(lambda x: x.get("name") if isinstance(x, dict) else None)
    shots["outcome"] = shots["shot"].apply(lambda s: s.get("outcome",{}).get("name") if isinstance(s, dict) else None)

    # coords (StatsBomb 120x80)
    def get_xy(row):
        loc = row.get("location", None)
        if isinstance(loc, list) and len(loc)>=2: return pd.Series(dict(x=loc[0], y=loc[1]))
        return pd.Series(dict(x=np.nan, y=np.nan))
    shots[["x","y"]] = shots.apply(get_xy, axis=1)

    # quick xG proxy (for coursework only)
    goal_x, goal_y = 120.0, 40.0
    dx = (goal_x - shots["x"]).clip(lower=1e-6); dy = (goal_y - shots["y"]).abs().clip(lower=1e-6)
    dist = np.hypot(dx, dy); angle = np.arctan2(7.32/2, dist)
    shots["xg_proxy"] = 1/(1+np.exp(-(1.2*angle - 0.04*dist)))
    shots["is_goal"] = (shots["outcome"]=="Goal").astype(int)
    return shots[["team","player","x","y","xg_proxy","is_goal","outcome"]]

def player_summary_from_shots(shots: pd.DataFrame) -> pd.DataFrame:
    if shots.empty: return pd.DataFrame()
    g = shots.groupby(["team","player"]).agg(
        shots=("x","count"), goals=("is_goal","sum"),
        xg_proxy=("xg_proxy","sum"), xg_per_shot=("xg_proxy","mean"),
    ).reset_index()
    g["finishing_plusminus"] = g["goals"] - g["xg_proxy"]
    return g.sort_values(["xg_per_shot","shots"], ascending=[False, False])
