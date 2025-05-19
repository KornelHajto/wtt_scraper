import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

LIST_ID = 31  # Fixed list ID based on the website's URL structure

def fetch_player_matches(player_name, pid):
    url = f'https://results.ittf.link/index.php/matches/players-matches/list/{LIST_ID}?resetfilters=0&abc={pid}&clearordering=0&clearfilters=0'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': f'https://results.ittf.link/index.php/matches/players-matches/list/{LIST_ID}?resetfilters=1&abc={pid}',
        'Origin': 'https://results.ittf.link',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
    }

    data = {
        f'fabrik_list_filter_all_{LIST_ID}_com_fabrik_{LIST_ID}': '',
        f'limit{LIST_ID}': '250',
        f'limitstart{LIST_ID}': '0',
        'option': 'com_fabrik',
        'orderdir': '',
        'orderby': '',
        'view': 'list',
        f'listid': str(LIST_ID),
        f'listref': f'{LIST_ID}_com_fabrik_{LIST_ID}',
        'Itemid': '443',
        'fabrik_referrer': f'/index.php/matches/players-matches/list/{LIST_ID}?resetfilters=1&abc={pid}',
        '999fcc1e01dba5af8b7e421150508153': '1',
        'format': 'html',
        'packageId': '0',
        'task': 'list.filter',
        'fabrik_listplugin_name': '',
        'fabrik_listplugin_renderOrder': '',
        'fabrik_listplugin_options': '',
        'incfilters': '1'
    }

    print(f"\nRequesting matches for {player_name} (PID {pid})")
    print(f"POST URL: {url}")

    try:
        response = requests.post(url, headers=headers, data=data, timeout=20)
        print(f"Response status code: {response.status_code}")
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch matches for {player_name} (PID {pid}): {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('tbody.fabrik_groupdata tr.fabrik_row')

    matches = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 14:  # Adjusted to check for minimum required cells
            print(f"Skipping row with only {len(cells)} cells")
            continue

        # Extract team members
        player_a = cells[2].get_text(strip=True)
        player_b = cells[3].get_text(strip=True)
        player_x = cells[4].get_text(strip=True)
        player_y = cells[5].get_text(strip=True)

        # Form teams (handle singles/doubles)
        team1 = [p for p in [player_a, player_b] if p]
        team2 = [p for p in [player_x, player_y] if p]

        if not team1 or not team2:
            print(f"Skipping row due to empty team: {team1} vs {team2}")
            continue

        match_info = {
            "queried_player": player_name,
            "year": cells[0].get_text(strip=True),
            "tournament": cells[1].get_text(strip=True),
            "team1": " / ".join(team1),  # Combine players for doubles
            "team2": " / ".join(team2),
            "event": cells[6].get_text(strip=True),
            "stage": cells[7].get_text(strip=True),
            "round": cells[8].get_text(strip=True),
            "result": cells[9].get_text(strip=True),
            "games": cells[10].get_text(strip=True),
            "winner_name": cells[11].get_text(strip=True),
            "winners_names": cells[12].get_text(strip=True),  # Full winner team
        }
        matches.append(match_info)

    print(f"{player_name} (PID {pid}): Recorded {len(matches)} matches")
    return matches

# Load players CSV (ensure the path is correct)
players_df = pd.read_csv('players.csv')

all_matches = []

for _, row in players_df.head(500).iterrows():
    player_name = row['Name']
    pid = str(row['PID'])
    matches = fetch_player_matches(player_name, pid)
    all_matches.extend(matches)
    time.sleep(2)  # Be polite between requests

df_all_matches = pd.DataFrame(all_matches)
df_all_matches.to_csv('matches.csv', index=False)
print("Saved all matches to matches.csv")