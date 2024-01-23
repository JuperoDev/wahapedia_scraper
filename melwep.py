import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://wahapedia.ru/wh40k10ed/factions/space-wolves/Blood-Claws"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the text "MELEE WEAPONS"
    melee_weapons_tag = soup.find(string='MELEE WEAPONS')

    if melee_weapons_tag:
        # Find all following <span> elements and <div class="ct"> elements
        for tag in melee_weapons_tag.find_all_next():
            if tag.name == 'span':
                print(f"Found <span>: {tag.text.strip()}")
            elif tag.name == 'div' and 'ct' in tag.get('class', []):
                print(f"Found <div class='ct'>: {tag.text.strip()}")
            elif tag.name == 'table':
                # Stop searching after encountering a new table
                break
    else:
        print("Text 'MELEE WEAPONS' not found in the table.")
else:
    print("Failed to retrieve the webpage.")
