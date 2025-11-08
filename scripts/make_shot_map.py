import typer
from pathlib import Path
import pandas as pd
from src.visualize.pitch import shot_map

app = typer.Typer()

@app.command()
def plot(match_id:2275117, int):
    shots_path = Path("data/processed") / f"shots_{match_id}.parquet"
    if not shots_path.exists(): raise SystemExit("Run build_features.py shots-table first.")
    shots = pd.read_parquet(shots_path)
    fig, ax = shot_map(shots, title=f"Match {match_id} — Shot Map")
    outdir = Path("visualisations"); outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / f"shot_map_{match_id}.png", dpi=200, bbox_inches="tight")
    print(f"Saved {outdir / f'shot_map_{match_id}.png'}")

if __name__ == "__main__":
    app()
