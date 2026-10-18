import pandas as pd
from pathlib import Path

file = Path(__file__).resolve().parents[1] / "data/raw/team_games_2024_25.csv"

df = pd.read_csv(file, dtype={"GAME_ID": str})

print("\nFIRST FIVE ROWS:")
print(df.head().to_string(index=False))

print("\nCOLUMNS:")
print(df.columns.tolist())

print("\nMISSING VALUES:")
print(df.isna().sum()[df.isna().sum() > 0])

print("\nDUPLICATE TEAM-GAME RECORDS:")
print(df.duplicated(["GAME_ID", "TEAM_ID"]).sum())

print("\nRECORDS PER GAME:")
print(df.groupby("GAME_ID").size().value_counts().sort_index())