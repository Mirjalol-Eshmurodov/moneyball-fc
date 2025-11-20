import typer
from pathlib import Path
from src.data.statsbomb_downloader import download_competitions, download_matches, download_events

app = typer.Typer()

@app.command()
def competitions():
    out = download_competitions(Path("data/raw")); typer.echo(f"Saved {out}")

@app.command()
def matches(competition_id: int, season_id: int):
    out = download_matches(competition_id, season_id, Path("data/raw")); typer.echo(f"Saved {out}")

@app.command()
def events(match_id: int):
    out = download_events(match_id, Path("data/raw")); typer.echo(f"Saved {out}")

@app.command()
def sample_world_cup():
    matches(43, 3)  # 2018 World Cup

if __name__ == "__main__":
    app()
