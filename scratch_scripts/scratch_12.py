import requests
from PIL import Image, ImageTk
import tkinter as tk
from io import BytesIO

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

# Function to download and display champion icons
def display_champion_icons(champion_info):
    root = tk.Tk()
    root.title("League of Legends Champions")

    row = 0
    col = 0

    for champ_name, champ_details in champion_info.items():
        # Download the icon image
        response = requests.get(champ_details['icon_url'])
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((64, 64), Image.LANCZOS)  # Resize the icon to 64x64 pixels
        photo = ImageTk.PhotoImage(img)

        # Create a label with the champion name and icon
        label = tk.Label(root, text=champ_details['name'], image=photo, compound='top')
        label.image = photo  # Keep a reference to the image to avoid garbage collection
        label.grid(row=row, column=col, padx=10, pady=10)

        col += 1
        if col > 5:  # Change this value to adjust the number of icons per row
            col = 0
            row += 1

    root.mainloop()

# Display the champion icons
display_champion_icons(champion_info)
