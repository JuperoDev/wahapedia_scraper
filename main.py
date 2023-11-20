import json
import os
from scraping_modules import parentUnit, factionKeywords, supremeCommander, damaged, lore, keywords
from scraping_modules.leader import scrape_leader
from scraping_modules.attributes import scrape_attributes
from scraping_modules import rangedWeapons
from scraping_modules.abilities import abCore  # Import the abCore module

def save_json(data, filename):
    folder_path = 'fetched-units'
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
        print(f"JSON file created: {file_path}")

def main():
    url_to_scrape = "https://wahapedia.ru/wh40k10ed/factions/adepta-sororitas/Aestred-Thurga-And-Agathae-Dolan"

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

        # Use the URL from main.py to scrape abilities data
        abilities_data = abCore.scrape_abilities(url_to_scrape)
        scraped_data['abilities'] = {"core": abilities_data}  # Include abilities data in scraped_data

        # Print the scraped rangedWeapons data
        print("Scraped Ranged Weapons Data:")
        print(json.dumps(ranged_weapons_data, indent=2, ensure_ascii=False))

        save_json(scraped_data, filename)
        print_fetched_data(scraped_data)

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

if __name__ == "__main__":
    main()
