import requests
from bs4 import BeautifulSoup

def scrape_abilities(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Initialize an empty list to store abilities
    abilities = []

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class "dsRightСol"
        ds_right_col_div = soup.find('div', class_='dsRightСol')

        if ds_right_col_div:
            # Find the first div with class "dsAbility" within dsRightCol
            ds_ability_div = ds_right_col_div.find('div', class_='dsAbility')

            if ds_ability_div:
                # Extract the text content and split it into a list
                content = ds_ability_div.get_text()
                data_list = [item.strip() for item in content.split(',')]

                # Remove the "CORE:" prefix from the first item in the list
                if data_list:
                    data_list[0] = data_list[0].replace('CORE:', '').strip()

                # Add the abilities to the abilities list
                abilities.extend(data_list)

    return abilities
