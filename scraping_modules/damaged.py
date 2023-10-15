# damaged.py

import requests
import re
from bs4 import BeautifulSoup

def scrape_damage_info(url):
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
            # Look for the specific pattern "DAMAGED: 1-6 WOUNDS REMAINING"
            pattern_damaged = re.compile(r'DAMAGED: (\d+-\d+) WOUNDS REMAINING')
            match_damaged = pattern_damaged.search(ds_right_col_div.get_text())

            if match_damaged:
                # Extract the range of numbers
                damaged_range = match_damaged.group(1)
                remaining_wounds = int(damaged_range.split('-')[-1])

                # Look for the expression "While this model has 1-6 wounds remaining"
                pattern_while_this_model_has = re.compile(r'While this model has (\d+-\d+ wounds remaining, [^\.]+)\.')
                match_while_this_model_has = pattern_while_this_model_has.search(ds_right_col_div.get_text())

                if match_while_this_model_has:
                    # Extract the entire sentence containing the pattern
                    while_this_model_has_sentence = match_while_this_model_has.group(0)

                    # Return the damaged information
                    damaged_info = {
                        "remainingWounds": remaining_wounds,
                        "description": while_this_model_has_sentence
                    }

                    return damaged_info

    # Return an empty dictionary if no damaged information is found
    return {}
