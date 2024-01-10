import requests
from bs4 import BeautifulSoup

def scrape_faction_abilities(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Initialize an empty list to store faction abilities
    faction_abilities = []

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the div elements with the class 'dsAbility'
        ds_ability_divs = soup.find_all('div', class_='dsAbility')

        # Check if there are at least two 'dsAbility' divs
        if len(ds_ability_divs) >= 2:
            # Get the data from the second 'dsAbility' div
            second_ds_ability_div = ds_ability_divs[1]

            # Extract the text content of the second 'dsAbility' div
            data_from_second_ds_ability = second_ds_ability_div.get_text()

            # Check if "FACTION:" is present in the text
            if "FACTION:" in data_from_second_ds_ability:
                # Remove the "FACTION" prefix
                data_without_faction = data_from_second_ds_ability.replace("FACTION:", "").strip()

                # Split the data by commas and remove leading/trailing spaces
                faction_abilities = [ability.strip() for ability in data_without_faction.split(',')]

    return faction_abilities
