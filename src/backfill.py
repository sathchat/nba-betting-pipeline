
from pathlib import Path
from time import sleep

import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "raw" / "team_games"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Test a small sample of seasons before the full backfill
SEASONS = ["1946-47", "1980-81", "2024-25"]

for season in SEASONS:
    output_file = OUTPUT / f"{season}.csv"

    if output_file.exists():
        print(f"Skipping {season}: already downloaded")
        continue

    print(f"Downloading {season}...")

    try:
        df = leaguegamefinder.LeagueGameFinder(
            season_nullable=season,
            season_type_nullable="Regular Season",
            league_id_nullable="00",
            player_or_team_abbreviation="T",
            timeout=60
        ).get_data_frames()[0]

        if df.empty:
            print(f"No records returned for {season}")
            continue

        if df.duplicated(["GAME_ID", "TEAM_ID"]).any():
            raise ValueError("Duplicate team-game records")

        counts = df.groupby("GAME_ID").size()

        if not counts.eq(2).all():
            raise ValueError("Some games do not have two team records")

        df.to_csv(output_file, index=False)

        print(
            f"Saved {season}: "
            f"{len(df):,} team records, "
            f"{df['GAME_ID'].nunique():,} games"
        )

    except Exception as error:
        print(f"Failed {season}: {error}")

    sleep(3)

print("Test backfill finished.")
