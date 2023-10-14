# scraping_modules/ability.py
from bs4 import BeautifulSoup

def extract_abilities(html):
    soup = BeautifulSoup(html, 'html.parser')
    abilities_div = soup.find('div', class_='dsRightСol dsColorFrBA')

    if abilities_div:
        # Find all divs with class 'dsAbility'
        ability_divs = abilities_div.find_all('div', class_='dsAbility')

        # Extract and print the text from each ability div
        abilities = []
        for index, ability_div in enumerate(ability_divs, start=1):
            ability_text = ability_div.get_text(strip=True)
            abilities.append(f"Ability {index}: {ability_text}")

        return abilities
    else:
        print("Abilities div not found.")
        return []
