import requests
from bs4 import BeautifulSoup

# Define the URL you want to scrape
url = "https://wahapedia.ru/wh40k10ed/factions/tyranids/Genestealers"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all div elements with class="dsAbility"
    ds_ability_divs = soup.find_all("div", class_="dsAbility")

    # Initialize variables to store header and text
    header = None
    text = []

    # Loop through the third dsAbility div
    for element in ds_ability_divs[2]:
        if element.name == "b":
            # If a new header is found, print the previous header and text
            if header:
                print(header)
                print(" ".join(text))
                print()

            # Update the header
            header = element.text.strip()
            text = []
        elif isinstance(element, str) and element.strip():
            text.append(element.strip())

    # Print the last header and text
    if header:
        print(header)
        print(" ".join(text))
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
