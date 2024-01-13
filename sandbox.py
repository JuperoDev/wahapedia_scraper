import requests
from bs4 import BeautifulSoup
import re
import json

# Define the URL to scrape
url = "https://wahapedia.ru/wh40k10ed/factions/space-marines/Devastator-Squad"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the "wargear options" section
    wargear_options = soup.find(string=re.compile("wargear options"))

    # Check if the "wargear options" section exists
    if wargear_options:
        # Find the first <ul> element after the "wargear options" section
        first_ul = wargear_options.find_next("ul")

        # Initialize an empty list to store the objects
        items_list = []

        # Iterate through the <li> elements within the first <ul>
        for li in first_ul.find_all("li", recursive=False):
            # Create an object for each <li>
            item = {"description": li.get_text(strip=True)}
            nested_ul = li.find("ul")

            if nested_ul:
                # If a nested <ul> exists, extract its <li> elements
                item["items"] = [nested_li.get_text(strip=True) for nested_li in nested_ul.find_all("li")]

            # Append the object to the list
            items_list.append(item)

        # Print the result as a JSON array
        print(json.dumps(items_list, indent=2))
    else:
        print("No 'wargear options' section found on the page.")
else:
    print("Failed to fetch the webpage. Status code:", response.status_code)
