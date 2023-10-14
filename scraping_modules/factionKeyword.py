# scraping_modules/factionKeyword.py
from bs4 import BeautifulSoup

def extract_faction_keywords(html):
    soup = BeautifulSoup(html, 'html.parser')
    faction_keywords_div = soup.find('div', class_='dsRightСolKW')

    if faction_keywords_div:
        # Extract text and replace line breaks with spaces
        faction_keywords_text = ' '.join(faction_keywords_div.stripped_strings)

        # Convert to lowercase and remove "FACTION KEYWORDS:"
        faction_keywords_text = faction_keywords_text.lower().replace("faction keywords:", "")

        # Split the keywords into a list
        faction_keywords_list = [keyword.strip() for keyword in faction_keywords_text.split(',')]

        print("Faction Keywords found:", faction_keywords_list)

        return faction_keywords_list
    else:
        print("Faction Keywords div not found.")
        return None
