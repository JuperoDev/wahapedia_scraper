from scraping_modules import parentUnit
import json
import re
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

def main():
    # URL to scrape from wahapedia.ru
    url_to_scrape = "https://wahapedia.ru/wh40k10ed/factions/blood-angels/Astorath"

    # Calling the scrape function from parentUnit module
    scraped_data = parentUnit.scrape_parent_unit(url_to_scrape)

    if scraped_data:
        # Creating a hyphenated filename
        filename = f"{scraped_data['parentUnit'].replace(' ', '-').lower()}.json"

        # Saving the JSON data using the save_json function
        save_json(scraped_data, filename)

if __name__ == "__main__":
    main()
