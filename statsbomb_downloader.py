from __future__ import annotations
from pathlib import Path
import json, requests

BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

def _save_json(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def _fetch_json(url: str):
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()

def download_competitions(dst_dir: Path) -> Path:
    data = _fetch_json(f"{BASE}/competitions.json")
    out = dst_dir / "competitions.json"
    _save_json(data, out); return out

def download_matches(competition_id: int, season_id: int, dst_dir: Path) -> Path:
    data = _fetch_json(f"{BASE}/matches/{competition_id}/{season_id}.json")
    out = dst_dir / f"matches_{competition_id}_{season_id}.json"
    _save_json(data, out); return out

def download_events(match_id: int, dst_dir: Path) -> Path:
    data = _fetch_json(f"{BASE}/events/{match_id}.json")
    out = dst_dir / f"events_{match_id}.json"
    _save_json(data, out); return out
