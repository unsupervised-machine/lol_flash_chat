import requests
import json

# Get the latest version of the game
version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
versions = requests.get(version_url).json()
latest_version = versions[0]

# Get the champion data for the latest version
champion_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
champion_data = requests.get(champion_url).json()

# Extract champion names and icon URLs
champions = champion_data['data']
champion_info = {}

for champ_name, champ_data in champions.items():
    champion_info[champ_name] = {
        "name": champ_data['name'],
        "icon_url": f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{champ_data['image']['full']}"
    }

# Print the champion names and their icon URLs
for champ_name, champ_details in champion_info.items():
    print(f"{champ_details['name']}: {champ_details['icon_url']}")