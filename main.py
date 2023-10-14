# main.py
from scraping_modules import scraper, attributes, keywords
from bs4 import BeautifulSoup
import json

# Define the save_to_json function
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
        char_wrap = BeautifulSoup(response.text, 'html.parser').find('div', class_='dsCharWrap')
        unit_attributes = attributes.fetch_attributes(char_wrap)
        extracted_keywords = keywords.extract_keywords(response.text)

        # Combine adjacent words with a space
        combined_keywords = []
        current_word = ""
        for word in extracted_keywords:
            if word.isalpha():
                combined_keywords.append(word.strip())
            else:
                combined_keywords.append(word.strip())

        # Create a dictionary with the data
        data = {
            "parentUnit": fetched_text,
            "attributes": [unit_attributes],
            "keywords": combined_keywords,
            # "raw_html": response.text  # Save the raw HTML if needed
        }

        # Save to JSON file
        save_to_json(filename, data)
        print(f"Data saved to {filename}")

        if combined_keywords:
            print(f"Extracted Keywords: {', '.join(combined_keywords)}")
    else:
        print("Unable to fetch data.")

if __name__ == "__main__":
    main()
