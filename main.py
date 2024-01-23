import json
import os

# Import your scraping modules as needed
from scraping_modules import parentUnit, factionKeywords, supremeCommander, damaged, lore, keywords
from scraping_modules.leader import scrape_leader
from scraping_modules.attributes import scrape_attributes
from scraping_modules import rangedWeapons
from scraping_modules.abilities import abCore
from scraping_modules.abilities import abFaction
from scraping_modules.abilities import abOther
from scraping_modules.wargear import scrape_wargear  # Import the wargear module

def save_json(data, filename):
    folder_path = 'fetched-units'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
        print(f"JSON file created: {file_path}")

def scrape_and_save_url(url_to_scrape):
    scraped_data = {}  # Initialize an empty dictionary for each URL

    # Perform scraping for the current URL and populate scraped_data dictionary
    scraped_data = parentUnit.scrape_parent_unit(url_to_scrape)

    if scraped_data:
        filename = f"{scraped_data['parentUnit'].replace(' ', '-').lower()}.json"

        faction_keywords_data = factionKeywords.scrape_data(url_to_scrape)
        scraped_data['factionKeywords'] = faction_keywords_data

        damaged_data = damaged.scrape_damage_info(url_to_scrape)
        scraped_data['damaged'] = damaged_data

        supreme_commander_present = supremeCommander.check_supreme_commander(url_to_scrape)
        scraped_data['supremeCommander'] = supreme_commander_present

        lore_text = lore.get_pic_legend_title(url_to_scrape)
        scraped_data['lore'] = lore_text

        keywords_list = keywords.scrape_keywords(url_to_scrape)
        scraped_data['keywords'] = keywords_list

        # Use the URL from main.py to scrape attributes
        attributes_data = scrape_attributes(url_to_scrape)
        scraped_data['attributes'] = attributes_data

        # Use the URL from main.py to scrape leader data
        leader_list = scrape_leader(url_to_scrape)
        scraped_data['leader'] = leader_list  # Include leader data in scraped_data

        # Use the URL from main.py to scrape ranged weapons data
        ranged_weapons_data = rangedWeapons.scrape_ranged_weapons(url_to_scrape)
        scraped_data['rangedWeapons'] = ranged_weapons_data  # Include ranged weapons data in scraped_data

        # Use the URL from main.py to scrape abilities data (abCore)
        abilities_data_core = abCore.scrape_abilities(url_to_scrape)
        scraped_data['abilities'] = {"core": abilities_data_core}  # Include abilities data (abCore) in scraped_data

        # Use the URL from main.py to scrape abilities data (abFaction)
        abilities_data_faction = abFaction.scrape_faction_abilities(url_to_scrape)
        scraped_data['abilities']['faction'] = abilities_data_faction  # Include abilities data (abFaction) in scraped_data

        # Use the URL from main.py to scrape abilities data (abOther)
        abilities_data_other = abOther.scrape_other_abilities(url_to_scrape)
        scraped_data['abilities']['otherAbilities'] = abilities_data_other  # Include abilities data (abOther) as otherAbilities

        # Use the URL from main.py to scrape wargear data
        wargear_data = scrape_wargear(url_to_scrape)
        scraped_data['wargear'] = wargear_data  # Include wargear data in scraped_data

    return scraped_data

def print_fetched_data(scraped_data):
    print("Fetched data:")
    print(f'\n"parentUnit": "{scraped_data["parentUnit"]}",')
    print('"factionKeywords": [')
    for keyword in scraped_data["factionKeywords"]:
        print(f'    "{keyword}",')
    print(f']\n"supremeCommander": "{scraped_data["supremeCommander"]}",')

    damaged_info = scraped_data.get('damaged', {})
    print('"damaged": {')
    if damaged_info:
        print(f'    "remainingWounds": {damaged_info["remainingWounds"]},')
        print(f'    "description": "{damaged_info["description"]}",')
    else:
        print('    {},')
    print('}')

    print(f'"lore": "{scraped_data["lore"]}",')
    print('"keywords": [')
    for keyword in scraped_data["keywords"]:
        print(f'    "{keyword}",')
    print(']')

    # Check if 'leader' data is present in the dictionary
    if "leader" in scraped_data:
        print('"leader": [')
        for leader in scraped_data["leader"]:
            print(f'    "{leader}",')
        print(']')
    else:
        print('"leader": []')  # Handle case when 'leader' data is not present

    # Print attributes information directly as an array
    print('"attributes":')
    print(json.dumps(scraped_data["attributes"], indent=2, ensure_ascii=False))

    # Print abilities data (abCore)
    print('\n"abilities": {')
    print(f'    "core": {json.dumps(scraped_data["abilities"]["core"], indent=2, ensure_ascii=False)},')

    # Print abilities data (abFaction)
    print(f'    "faction": {json.dumps(scraped_data["abilities"]["faction"], indent=2, ensure_ascii=False)},')

    # Print abilities data (abOther) as otherAbilities
    print(f'    "otherAbilities": {json.dumps(scraped_data["abilities"]["otherAbilities"], indent=2, ensure_ascii=False)},')

    # Print wargear data
    print(f'    "wargear": {json.dumps(scraped_data["wargear"], indent=2, ensure_ascii=False)},')

    print('}')

def main():
    # Read the list of URLs from a text file
    with open('urls.txt', 'r') as file:
        urls = file.read().splitlines()

    for url_to_scrape in urls:
        scraped_data = scrape_and_save_url(url_to_scrape)

        # Save the scraped data to a separate JSON file for each URL
        filename = f"{url_to_scrape.split('/')[-1].replace(' ', '-').lower()}.json"
        save_json(scraped_data, filename)
        print_fetched_data(scraped_data)

if __name__ == "__main__":
    main()
