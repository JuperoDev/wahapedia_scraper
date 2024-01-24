import requests
from bs4 import BeautifulSoup
import json
import re

# Define the URL to scrape
url = "https://wahapedia.ru/wh40k10ed/factions/space-marines/Ancient-In-Terminator-Armour"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with class 'wTable'
    table = soup.find('table', class_='wTable')

    if table:
        # Find the tbody with class 'bkg_reset'
        bkg_reset = table.find('tbody', class_='bkg_reset')

        if bkg_reset:
            # Find all tbody elements with class 'bkg' that come after 'bkg_reset'
            bkg_elements = bkg_reset.find_all_next('tbody', class_='bkg')

            # Initialize an empty list to store the modified objects
            meleeWeapons = []

            # Loop through each 'bkg' tbody and extract the text
            for bkg_element in bkg_elements:
                # Extract the text from each <td> within the 'bkg' tbody
                td_elements = bkg_element.find_all('td')
                parameters = [td.get_text(strip=True) for td in td_elements]
                
                # Check if the object is not empty (has at least one non-empty parameter)
                if any(parameters) and not any("MELEE WEAPONS" in parameter for parameter in parameters):
                    # Extract content within square brackets for modifiers
                    modifiers_text = re.search(r'\[(.*?)\]', parameters[3])
                    modifiers = modifiers_text.group(1) if modifiers_text else ""

                    # Remove content within square brackets (including brackets) from name
                    name = re.sub(r'\[.*?\]', '', parameters[1])

                    # Convert "armor-penetration" to a numeric value (remove minus sign)
                    armor_penetration = int(parameters[8].replace('-', ''))

                    # Convert "strength" to a numeric value
                    strength = int(parameters[7])

                    melee_weapon_obj = {
                        "name": name.strip(),
                        "modifiers": modifiers.strip(),
                        "attacks": parameters[5],
                        "weapons-skills": parameters[6],
                        "strength": strength,
                        "armor-penetration": armor_penetration,
                        "damage": parameters[9]
                    }

                    meleeWeapons.append(melee_weapon_obj)

            # Create a dictionary with the 'meleeWeapons' array
            result = {'meleeWeapons': meleeWeapons}

            # Print the result as JSON-like format
            formatted_result = json.dumps(result, indent=4)
            print(formatted_result)
        else:
            print("No tbody with class 'bkg_reset' found.")
    else:
        print("No table with class 'wTable' found.")
else:
    print("Failed to retrieve the webpage.")
