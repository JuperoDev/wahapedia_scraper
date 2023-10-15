# scraping_modules/parentUnit.py

import os
import requests
from bs4 import BeautifulSoup
import json


def scrape_parent_unit(url):
    try:
        # Sending a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parsing the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finding the div with the specified class
        header_div = soup.find('div', class_='dsH2Header')

        # Extracting the text content of the div
        parent_unit_name = header_div.text.strip()

        # Printing the result
        print(f"Parent unit name: {parent_unit_name}")

        # Creating a JSON object
        data = {"parentUnit": parent_unit_name}

        # Creating the 'fetched-units' folder if it doesn't exist
        folder_path = 'fetched-units'
        os.makedirs(folder_path, exist_ok=True)

        # Writing JSON to a file in 'fetched-units' with hyphenated name
        filename = f"{parent_unit_name.replace(' ', '-').lower()}.json"
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)
            print(f"JSON file created: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Example URL
    url_to_scrape = "https://example.com"

    # Calling the scrape function with the provided URL
    scrape_parent_unit(url_to_scrape)
