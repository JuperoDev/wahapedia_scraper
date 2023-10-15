# main.py

from scraping_modules import parentUnit, factionKeywords, supremeCommander, damaged  # Import damaged from scraping_modules
import json
import os

def save_json(data, filename):
    # Creating the 'fetched-units' folder if it doesn't exist
    folder_path = 'fetched-units'
    os.makedirs(folder_path, exist_ok=True)

    # Writing JSON to a file in 'fetched-units' with the provided filename
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)
        print(f"JSON file created: {file_path}")

def print_fetched_data(scraped_data):
    print("Fetched data:")
    print(f'\n"parentUnit": "{scraped_data["parentUnit"]}",')
    print('"factionKeywords": [')
    for keyword in scraped_data["factionKeywords"]:
        print(f'    "{keyword}",')
    print(f']\n"supremeCommander": "{scraped_data["supremeCommander"]}",')

    # Print damaged information if available
    damaged_info = scraped_data.get('damaged', {})
    print('"damaged": {')
    if damaged_info:
        print(f'    "remainingWounds": {damaged_info["remainingWounds"]},')
        print(f'    "description": "{damaged_info["description"]}",')
    else:
        print('    {},')
    print('}')

def main():
    # URL to scrape from wahapedia.ru
    url_to_scrape = "https://wahapedia.ru/wh40k10ed/factions/world-eaters/Angron"

    # Calling the scrape function from parentUnit module
    scraped_data = parentUnit.scrape_parent_unit(url_to_scrape)

    if scraped_data:
        # Creating a hyphenated filename
        filename = f"{scraped_data['parentUnit'].replace(' ', '-').lower()}.json"

        # Use the URL from main.py in factionKeywords.scrape_data directly
        faction_keywords_data = factionKeywords.scrape_data(url_to_scrape)
        scraped_data['factionKeywords'] = faction_keywords_data

        # Use the URL from main.py in damaged.scrape_damage_info directly
        damaged_data = damaged.scrape_damage_info(url_to_scrape)
        scraped_data['damaged'] = damaged_data  # Include damaged data in scraped_data

        # Call the function from supremeCommander module
        supreme_commander_present = supremeCommander.check_supreme_commander(url_to_scrape)
        scraped_data['supremeCommander'] = supreme_commander_present

        # Saving the JSON data using the save_json function
        save_json(scraped_data, filename)

        # Print the fetched data
        print_fetched_data(scraped_data)

if __name__ == "__main__":
    main()
