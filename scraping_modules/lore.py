# scraping_modules/lore.py
from bs4 import BeautifulSoup
from html import unescape

def extract_lore(html):
    soup = BeautifulSoup(html, 'html.parser')
    lore_div = soup.find('div', class_='picLegend')

    if lore_div:
        # Extract text from the title attribute, unescape HTML entities, and decode
        lore_text = unescape(str(lore_div.get('title', '')))

        print("Lore found:", lore_text)

        return lore_text
    else:
        print("Lore div not found.")
        return None
