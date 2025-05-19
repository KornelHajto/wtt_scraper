import pandas as pd

# Load the match data CSV
df = pd.read_csv("matches.csv")

# Determine if the match is doubles or singles
def is_doubles(team1, team2):
    return '/' in team1 or '/' in team2

# Apply the check
df['is_doubles'] = df.apply(lambda row: is_doubles(row['team1'], row['team2']), axis=1)

# Split into two DataFrames
df_doubles = df[df['is_doubles'] == True].drop(columns='is_doubles')
df_singles = df[df['is_doubles'] == False].drop(columns='is_doubles')

# Save to CSV files
df_doubles.to_csv("matches_doubles.csv", index=False)
df_singles.to_csv("matches_singles.csv", index=False)

print("✅ Created 'matches_doubles.csv' and 'matches_singles.csv'")
