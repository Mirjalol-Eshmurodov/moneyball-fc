import typer
from pathlib import Path
import pandas as pd
from src.data.loaders import events_df
from src.analysis.features import shot_features, player_summary_from_shots

app = typer.Typer()

@app.command("shots-table")
def shots_table(competition_id: int, season_id: int, match_id: int):
    events = events_df(Path("data/raw"), match_id=match_id)
    shots = shot_features(events)
    out = Path("data/processed") / f"shots_{match_id}.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    shots.to_parquet(out, index=False)
    typer.echo(f"Saved {out} with {len(shots)} shots")

@app.command("player-summary")
def player_summary(match_id: int):
    shots_path = Path("data/processed") / f"shots_{match_id}.parquet"
    if not shots_path.exists():
        raise SystemExit("Run `shots-table` first to generate shot features.")
    shots = pd.read_parquet(shots_path)
    summary = player_summary_from_shots(shots)
    out = Path("data/processed") / f"player_summary_{match_id}.csv"
    summary.to_csv(out, index=False); typer.echo(f"Saved {out}")

if __name__ == "__main__":
    app()
