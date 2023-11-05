import requests
from bs4 import BeautifulSoup
import re
import json

# URL of the webpage
url = "https://wahapedia.ru/wh40k10ed/factions/tyranids/Norn-Emissary"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with class "dsLeftСol"
    ds_left_col_div = soup.find('div', class_='dsLeftСol')

    if ds_left_col_div:
        # Find the first table with class "wTable" within the dsLeftСol div
        wtable = ds_left_col_div.find('table', class_='wTable')

        if wtable:
            # Check if the word "RANGED" is found in the table
            if 'RANGED' in wtable.text:
                # Find all <tr> elements within the table
                rows = wtable.find_all('tr')

                # Initialize a flag to keep track of when to stop printing
                print_enabled = True

                # Initialize a list to store ranged weapons data
                ranged_weapons = []

                # Iterate through each row and format the output
                for row in rows:
                    text = row.get_text().strip()
                    if "MELEE WEAPONSRANGEAWSSAPD" in text:
                        # Disable printing when "MELEE WEAPONSRANGEAWSSAPD" is found
                        print_enabled = False
                    if "RANGED WEAPONSRANGEABSSAPD" in text:
                        # Exclude the specified string from printing
                        text = text.replace("RANGED WEAPONSRANGEABSSAPD", "")
                    if print_enabled:
                        # Check if the line contains modifiers in square brackets
                        if '[' in text:
                            weapon_name, modifiers_and_rest = re.split(r'\[', text, 1)
                            modifiers_and_rest = "[" + modifiers_and_rest
                            modifiers_match = re.search(r'\[(.*?)\]', modifiers_and_rest)
                            if modifiers_match:
                                modifiers_str = modifiers_match.group(1)
                                modifiers = [modifier.strip() for modifier in modifiers_str.split(',')]
                                rest = modifiers_and_rest.split(modifiers_str)[-1].strip()

                                # Extract the range from "rest"
                                range_match = re.search(r'\](\d+)\"', rest)
                                if range_match:
                                    range_value = int(range_match.group(1))
                                else:
                                    range_value = None

                                # Remove "]18\"" or similar from "rest"
                                rest = rest.replace(f"]{range_value}\"", "").strip()

                                if rest and rest != "]":
                                    # Replace "\u2013" with "-"
                                    weapon_name = weapon_name.replace("\u2013", "-")
                                    ranged_weapon = {
                                        "name": weapon_name.strip(),
                                        "modifiers": modifiers,
                                        "rest": rest,
                                        "range": range_value
                                    }
                                    ranged_weapons.append(ranged_weapon)
                        else:
                            # If no modifiers are found, treat the entire line as the weapon name
                            ranged_weapon = {
                                "name": text.strip(),
                                "modifiers": [],
                                "rest": "",
                                "range": None
                            }
                            ranged_weapons.append(ranged_weapon)

                # Filter out objects with both empty "rest" fields and "rest" equal to "]"
                filtered_ranged_weapons = [weapon for weapon in ranged_weapons if weapon["rest"] and weapon["rest"] != "]"]

                # Print the formatted output with filtering, replacement, and range attribute
                print('"rangedWeapons":', json.dumps(filtered_ranged_weapons, indent=2))
            else:
                print('"rangedWeapons": []')
        else:
            print("Table with class 'wTable' not found in dsLeftСol div.")
    else:
        print("Div with class 'dsLeftСol' not found on the page.")
else:
    print(f"Failed to retrieve the webpage (status code {response.status_code}).")
