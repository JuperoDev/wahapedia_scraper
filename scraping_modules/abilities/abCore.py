import requests
from bs4 import BeautifulSoup

# URL of the page you want to scrape
url = "https://wahapedia.ru/wh40k10ed/factions/tyranids/Broodlord"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with class "dsRightСol"
    ds_right_col_div = soup.find('div', class_='dsRightСol')

    if ds_right_col_div:
        # Find the first div with class "dsAbility" within dsRightСol
        ds_ability_div = ds_right_col_div.find('div', class_='dsAbility')

        if ds_ability_div:
            # Extract the text content and split it into a list
            content = ds_ability_div.get_text()
            data_list = [item.strip('""') for item in content.split(',')]

            # Remove the "CORE:" prefix from the first item in the list
            if data_list:
                data_list[0] = data_list[0].replace('CORE:', '').strip()

            # Print the result in the desired format
            print("[", end=" ")
            for i, item in enumerate(data_list):
                print(f'"{item}"', end=", " if i < len(data_list) - 1 else " ")
            print("]")
        else:
            print("No div with class 'dsAbility' found.")
    else:
        print("No div with class 'dsRightСol' found.")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
