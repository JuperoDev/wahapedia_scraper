# scraping_modules/ability.py
from bs4 import BeautifulSoup

def extract_abilities(html):
    soup = BeautifulSoup(html, 'html.parser')
    abilities_div = soup.find('div', class_='dsRightСol dsColorFrBA')

    if abilities_div:
        # Find all divs with class 'dsAbility'
        ability_divs = abilities_div.find_all('div', class_='dsAbility')

        # Organize abilities in a dictionary
        abilities_dict = {
            "core": [],
            "faction": [],
            "otherAbilities": []
        }

        current_ability = None  # Keep track of the current ability being processed

        for ability_div in ability_divs:
            # Extract the ability text and remove extra spaces
            ability_text = ' '.join(ability_div.stripped_strings)

            # Check if this line contains the ability name
            if ':' in ability_text:
                # If a previous ability was being processed, add it to the dictionary
                if current_ability is not None:
                    if "abilities" in current_ability:
                        abilities_dict[current_ability["category"]].append(current_ability)
                    else:
                        abilities_dict[current_ability["category"]].append({"name": current_ability["name"], "description": current_ability["description"]})

                # Split the line into name and description
                name, description = map(str.strip, ability_text.split(':', 1))

                # Determine the category of the ability
                if name.upper() == "CORE":
                    current_ability = {"category": "core", "abilities": [ability.strip().lower() for ability in description.split(',')]}
                elif name.upper() == "FACTION":
                    current_ability = {"category": "faction", "abilities": [ability.strip().lower() for ability in description.split(',')]}
                else:
                    current_ability = {"category": "otherAbilities", "name": name.strip(), "description": description.strip()}

            elif current_ability is not None:
                # If it's not a line with ':' and a previous ability was being processed, add this line to the description
                current_ability["description"] += ' ' + ability_text.strip()

        # Add the last ability to the dictionary
        if current_ability is not None:
            if "abilities" in current_ability:
                abilities_dict[current_ability["category"]].append(current_ability)
            else:
                abilities_dict[current_ability["category"]].append({"name": current_ability["name"], "description": current_ability["description"]})

        return abilities_dict
    else:
        print("Abilities div not found.")
        return {}
