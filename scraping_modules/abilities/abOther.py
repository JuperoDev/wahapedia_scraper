import requests
from bs4 import BeautifulSoup

def scrape_other_abilities(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Initialize dictionaries to store other abilities
    other_abilities = {}

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the third div element with class "dsAbility"
        ds_ability_divs = soup.find_all('div', class_='dsAbility')

        if len(ds_ability_divs) >= 3:
            third_ds_ability_div = ds_ability_divs[2]

            # Initialize variables to store header and text
            header = None
            text = []

            # Loop through the elements inside the third dsAbility div
            for element in third_ds_ability_div.stripped_strings:
                if element.endswith(":"):
                    # If a new header is found, store the previous header and text
                    if header:
                        other_abilities[header] = " ".join(text)
                    # Update the header
                    header = element.strip()
                    text = []
                else:
                    text.append(element.strip())

            # Store the last header and text
            if header:
                other_abilities[header] = " ".join(text)

    return other_abilities
