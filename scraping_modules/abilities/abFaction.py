import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = "https://wahapedia.ru/wh40k10ed/factions/tyranids/Tervigon"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the div elements with the class 'dsAbility'
    ds_ability_divs = soup.find_all('div', class_='dsAbility')

    # Check if there are at least two 'dsAbility' divs
    if len(ds_ability_divs) >= 2:
        # Get the data from the second 'dsAbility' div
        second_ds_ability_div = ds_ability_divs[1]

        # Extract the text content of the second 'dsAbility' div
        data_from_second_ds_ability = second_ds_ability_div.get_text()

        # Remove the "FACTION" prefix
        data_without_faction = data_from_second_ds_ability.replace("FACTION:", "").strip()

        # Print the modified data
        print(data_without_faction)
    else:
        print("Not enough 'dsAbility' divs found on the page.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
