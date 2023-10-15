# supremeCommander.py

import requests
from bs4 import BeautifulSoup

def check_supreme_commander(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with the specified class
        ds_right_col_div = soup.find('div', class_='dsRightСol')

        # Check if the div is found
        if ds_right_col_div:
            # Check if the text "SUPREME COMMANDER" is present
            supreme_commander_present = "SUPREME COMMANDER" in ds_right_col_div.get_text()

            return supreme_commander_present
        else:
            print("Couldn't find the specified div.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
