# factionKeywords.py

import requests
from bs4 import BeautifulSoup

def scrape_data(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class 'ds2colKW'
        target_div = soup.find('div', class_='ds2colKW')

        # Check if the div is found
        if target_div:
            # Find the div with class 'dsRightСolKW' inside the 'ds2colKW' div
            right_col_div = target_div.find('div', class_='dsRightСolKW')

            # Check if the 'tooltipTyranids' span is present
            tyranids_tooltip_span = right_col_div.find('span', class_='tooltipTyranids')

            if tyranids_tooltip_span:
                # If 'tooltipTyranids' span is found, return the specific message for Tyranids
                return ['tyranids']
            else:
                # Remove the text "FACTION KEYWORDS:" and split the remaining text by ","
                elements = right_col_div.text.replace("FACTION KEYWORDS:", "").strip().lower().split(',')

                # Remove leading and trailing spaces from each element
                elements = [element.strip() for element in elements]

                # Use a set to store unique elements
                unique_elements = set(elements)

                # Return the list of unique elements
                return list(unique_elements)
        else:
            return None
    else:
        return None
