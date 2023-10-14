# scraping_modules/lore.py
from bs4 import BeautifulSoup

def extract_lore(html):
    soup = BeautifulSoup(html, 'html.parser')
    lore_div = soup.find('div', class_='picLegend')

    if lore_div:
        # Extract text from the title attribute
        lore_text = lore_div['title']

        print("Lore found:", lore_text)

        return lore_text
    else:
        print("Lore div not found.")
        return None
