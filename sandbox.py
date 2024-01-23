import requests
from bs4 import BeautifulSoup
import json

# Define a function to process <ul> elements
def process_ul(ul_tag):
    items = []

    for li_tag in ul_tag.find_all("li", recursive=False):
        description = li_tag.text.strip()
        item = {"description": description, "items": []}

        nested_ul = li_tag.find("ul")
        if nested_ul:
            item["items"] = [nested_li.text.strip() for nested_li in nested_ul.find_all("li")]
        
        items.append(item)

    return items

# Define the URL
url = "https://wahapedia.ru/wh40k10ed/factions/space-wolves/Blood-Claws"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Initialize a list to store wargear items as dictionaries
wargear_list = []

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, "html.parser")

    # Check if the "WARGEAR OPTIONS" text exists on the page
    if "WARGEAR OPTIONS" in soup.text:
        # Find the first <ul> tag on the entire page
        first_ul = soup.find("ul")

        # Check if the <ul> tag exists and contains <li> elements
        if first_ul:
            wargear_list = process_ul(first_ul)

# Remove text after ":" in the "description" field
for item in wargear_list:
    description = item["description"]
    if ":" in description:
        item["description"] = description.split(":", 1)[0].strip()

# Convert the result list to JSON and print it
print(json.dumps(wargear_list, indent=2))
