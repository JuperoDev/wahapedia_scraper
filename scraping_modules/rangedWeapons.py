import requests
from bs4 import BeautifulSoup
import re
import json


def scrape_ranged_weapons(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ds_left_col_div = soup.find('div', class_='dsLeftСol')

        if ds_left_col_div:
            wtable = ds_left_col_div.find('table', class_='wTable')

            if wtable:
                if 'RANGED' in wtable.text:
                    rows = wtable.find_all('tr')
                    print_enabled = True
                    ranged_weapons = []

                    for row in rows:
                        text = row.get_text().strip()
                        if "MELEE WEAPONSRANGEAWSSAPD" in text:
                            print_enabled = False
                        if "RANGED WEAPONSRANGEABSSAPD" in text:
                            text = text.replace("RANGED WEAPONSRANGEABSSAPD", "")
                        if print_enabled:
                            if '[' in text:
                                weapon_name, modifiers_and_rest = re.split(r'\[', text, 1)
                                modifiers_and_rest = "[" + modifiers_and_rest
                                modifiers_match = re.search(r'\[(.*?)\]', modifiers_and_rest)

                                if modifiers_match:
                                    modifiers_str = modifiers_match.group(1)
                                    modifiers = [modifier.strip() for modifier in modifiers_str.split(',')]
                                    rest = modifiers_and_rest.split(modifiers_str)[-1].strip()
                                    range_match = re.search(r'\](\d+)\"', rest)

                                    if range_match:
                                        range_value = int(range_match.group(1))
                                    else:
                                        range_value = None

                                    rest = rest.replace(f"]{range_value}\"", "").strip()
                                    strength_match = re.search(r'[+A](\d+)(?=[-0])', rest)

                                    if strength_match:
                                        strength = int(strength_match.group(1))
                                        rest = rest.replace(f"+{strength}", "").strip()
                                    else:
                                        strength = None

                                    if rest and rest != "]":
                                        weapon_name = weapon_name.replace("\u2013", "-")
                                        ranged_weapon = {
                                            "name": weapon_name.strip(),
                                            "modifiers": modifiers,
                                            "range": range_value,
                                            "attacks": 2,
                                            "ballistic-skills": 3,
                                            "strength": strength,
                                            "armor-penetration": 1,
                                            "damage": 1,
                                            "singleChoice": False
                                        }
                                        ranged_weapons.append(ranged_weapon)
                            else:
                                ranged_weapon = {
                                    "name": text.strip(),
                                    "modifiers": [],
                                    "range": None,
                                    "strength": None,
                                    "attacks": 0,
                                    "ballistic-skills": 0,
                                    "armor-penetration": 0,
                                    "damage": 0,
                                    "singleChoice": False
                                }
                                ranged_weapons.append(ranged_weapon)

                    filtered_ranged_weapons = [weapon for weapon in ranged_weapons if weapon["range"] is not None]
                    filtered_ranged_weapons_without_rest = [
                        {
                            "name": weapon["name"],
                            "modifiers": weapon["modifiers"],
                            "range": weapon["range"],
                            "strength": weapon["strength"],
                            "attacks": weapon["attacks"],
                            "ballistic-skills": weapon["ballistic-skills"],
                            "armor-penetration": weapon["armor-penetration"],
                            "damage": weapon["damage"],
                            "singleChoice": weapon["singleChoice"]
                        }
                        for weapon in filtered_ranged_weapons
                    ]
                    return filtered_ranged_weapons_without_rest
                else:
                    return []
            else:
                return []
        else:
            return []
    else:
        return []


if __name__ == "__main__":
    url_to_scrape = "https://wahapedia.ru/wh40k10ed/factions/adepta-sororitas/Aestred-Thurga-And-Agathae-Dolan"
    ranged_weapons_data = scrape_ranged_weapons(url_to_scrape)
    print(json.dumps(ranged_weapons_data, indent=2))
