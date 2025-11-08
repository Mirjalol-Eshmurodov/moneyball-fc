# scripts/plot_top_players.py
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIG ---
match_id = 2275117 # kerak bo'lsa shu raqamni o'zgartiring

# --- PATHS ---
ROOT = Path(__file__).resolve().parent.parent     # .../moneyball-fc-starter
PROC = ROOT / "data" / "processed"
VIZ  = ROOT / "visualisations"
VIZ.mkdir(parents=True, exist_ok=True)

csv_path = PROC / f"player_summary_{match_id}.csv"
df = pd.read_csv(csv_path)

# Qo'shimcha metrik: finishing_plusminus = goals - xg_proxy
df["finishing_plusminus"] = df["goals"] - df["xg_proxy"]

# --- TOP 5 by xg_proxy ---
top_xg = df.sort_values("xg_proxy", ascending=False).head(5)
plt.figure(figsize=(10,6))
plt.barh(top_xg["player"], top_xg["xg_proxy"])
plt.gca().invert_yaxis()
plt.title(f"Top 5 Players by xG (Match {match_id})")
plt.xlabel("xG (proxy)")
for i, v in enumerate(top_xg["xg_proxy"]):
    plt.text(v, i, f" {v:.2f}", va="center")
out1 = VIZ / f"top5_xg_{match_id}.png"
plt.tight_layout()
plt.savefig(out1, dpi=200)
plt.close()

# --- TOP 5 by goals ---
top_goals = df.sort_values("goals", ascending=False).head(5)
plt.figure(figsize=(10,6))
plt.barh(top_goals["player"], top_goals["goals"])
plt.gca().invert_yaxis()
plt.title(f"Top 5 Players by Goals (Match {match_id})")
plt.xlabel("Goals")
for i, v in enumerate(top_goals["goals"]):
    plt.text(v, i, f" {int(v)}", va="center")
out2 = VIZ / f"top5_goals_{match_id}.png"
plt.tight_layout()
plt.savefig(out2, dpi=200)
plt.close()

# --- TOP 5 by finishing_plusminus (kim xG'dan ko'proq/gam kam urgan) ---
top_finish = df.sort_values("finishing_plusminus", ascending=False).head(5)
plt.figure(figsize=(10,6))
plt.barh(top_finish["player"], top_finish["finishing_plusminus"])
plt.gca().invert_yaxis()
plt.title(f"Top 5 Finishing +/- (Goals − xG) — Match {match_id}")
plt.xlabel("Finishing +/-")
for i, v in enumerate(top_finish["finishing_plusminus"]):
    plt.text(v, i, f" {v:.2f}", va="center")
out3 = VIZ / f"top5_finishing_plusminus_{match_id}.png"
plt.tight_layout()
plt.savefig(out3, dpi=200)
plt.close()

print("✅ Saved:", out1)
print("✅ Saved:", out2)
print("✅ Saved:", out3)