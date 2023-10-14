# main.py
from scraping_modules import scraper, attributes, keywords, lore, factionKeyword, ability, invulnerable
from bs4 import BeautifulSoup
import json

def save_to_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

def main():
    url = "https://wahapedia.ru/wh40k10ed/factions/blood-angels/Sanguinary-Priest"
    fetched_text = scraper.fetch_text(url)

    if fetched_text:
        response = scraper.get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        char_wrap = soup.find('div', class_='dsProfileBaseWrap').find('div', class_='dsProfileWrapLeft').find('div', class_='dsProfileWrap')

        unit_attributes = attributes.fetch_attributes(char_wrap)
        unit_keywords = keywords.extract_keywords(response.text)
        unit_lore = lore.extract_lore(response.text)
        unit_faction_keywords = factionKeyword.extract_faction_keywords(response.text)
        unit_abilities = ability.extract_abilities(response.text)

        # Use the invulnerable module to extract invulnerable save
        invulnerable_save = invulnerable.extract_invulnerable(soup)

        # Update the last dictionary in the attributes list with invulnerableSave
        unit_attributes[-1]["invulnerableSave"] = invulnerable_save

        data = {
            "parentUnit": fetched_text,
            "attributes": unit_attributes,
            "keywords": unit_keywords,
            "lore": unit_lore,
            "faction_keywords": unit_faction_keywords,
            "abilities": unit_abilities,
        }

        filename = f"{fetched_text.replace(' ', '-').lower()}.json"
        save_to_json(filename, data)
        print(f"Data saved to {filename}")
    else:
        print("Unable to fetch data.")

if __name__ == "__main__":
    main()
