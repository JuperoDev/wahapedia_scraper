# main.py
from scraping_modules import scraper, attributes
from bs4 import BeautifulSoup
import json

def save_to_json(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def main():
    url = "https://wahapedia.ru/wh40k10ed/factions/tyranids/Neurolictor"
    fetched_text = scraper.fetch_text(url)

    if fetched_text:
        # Replace spaces with "-" and convert to lowercase
        filename = f"{fetched_text.replace(' ', '-').lower()}.json"

        # Fetch the page
        response = scraper.get_page(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        char_wrap = soup.find('div', class_='dsCharWrap')
        unit_attributes = attributes.fetch_attributes(char_wrap)

        # Create a dictionary with the data
        data = {
            "parentUnit": fetched_text,
            "attributes": [unit_attributes],
           # "raw_html": response.text  # Save the raw HTML if needed
        }

        # Save to JSON file
        save_to_json(filename, data)
        print(f"Data saved to {filename}")
    else:
        print("Unable to fetch data.")

if __name__ == "__main__":
    main()
