from __future__ import annotations
from pathlib import Path
import json, pandas as pd

def read_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def competitions_df(raw_dir: Path) -> pd.DataFrame:
    return pd.DataFrame(read_json(raw_dir / "competitions.json"))

def matches_df(raw_dir: Path, competition_id: int, season_id: int) -> pd.DataFrame:
    return pd.DataFrame(read_json(raw_dir / f"matches_{competition_id}_{season_id}.json"))

def events_df(raw_dir: Path, match_id: int) -> pd.DataFrame:
    return pd.DataFrame(read_json(raw_dir / f"events_{match_id}.json"))
