import os
import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_parent_unit(url):
    try:
        # Sending a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parsing the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finding the div with the specified class
        header_div = soup.find('div', class_='dsH2Header')

        # Extracting the text content of the div and removing anything within parentheses
        parent_unit_name = re.sub(r'\([^)]*\)', '', header_div.text).strip()

        # Creating a JSON object
        data = {"parentUnit": parent_unit_name}

        # Printing the fetched data
        print(f"Fetched data: {data}")

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
