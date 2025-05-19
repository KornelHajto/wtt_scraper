import pandas as pd

# Load the data
matches_df = pd.read_csv("matches.csv")
players_df = pd.read_csv("players.csv")

# Get unique queried player names
queried_players = set(matches_df['queried_player'].str.strip())

# Filter players that are not in the queried list
not_queried_df = players_df[~players_df['Name'].str.strip().isin(queried_players)]

# Save to CSV
not_queried_df.to_csv("not_queried_players.csv", index=False)

print("Saved missing players to 'not_queried_players.csv'")
