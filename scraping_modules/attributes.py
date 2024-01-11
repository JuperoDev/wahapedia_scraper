import requests
from bs4 import BeautifulSoup
import re

def scrape_attributes(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        char_dict = {
            "movement": 0,
            "toughness": 0,
            "salvation": 0,
            "wounds": 0,
            "leadership": 0,
            "objectiveControl": 0,
            "invulnerableSave": 0
        }

        ds_char_wrap_divs = soup.find_all('div', class_='dsCharWrap')

        for char_wrap in ds_char_wrap_divs:
            char_name_div = char_wrap.find('div', class_='dsCharName')
            char_value_div = char_wrap.find('div', class_='dsCharValue')

            if char_name_div and char_value_div:
                char_name = char_name_div.text.strip()
                char_value = char_value_div.text.strip()

                if "M" in char_name:
                    char_dict["movement"] = int(re.search(r'\d+', char_value).group())
                elif "T" in char_name:
                    char_dict["toughness"] = int(re.search(r'\d+', char_value).group())
                elif "Sv" in char_name:
                    char_dict["salvation"] = int(re.search(r'\d+', char_value).group())
                elif "W" in char_name:
                    char_dict["wounds"] = int(re.search(r'\d+', char_value).group())
                elif "Ld" in char_name:
                    char_dict["leadership"] = int(re.search(r'\d+', char_value).group())
                elif "OC" in char_name:
                    char_dict["objectiveControl"] = int(re.search(r'\d+', char_value).group())

        invul_value_div = soup.find('div', class_='dsCharInvulValue')
        if invul_value_div:
            invulnerable_save_value = invul_value_div.text.strip()
            char_dict["invulnerableSave"] = int(re.search(r'\d+', invulnerable_save_value).group())

        return char_dict

    print("No attributes found on the page.")
    return {}

# Example usage:
# url = "https://wahapedia.ru/wh40k10ed/factions/thousand-sons/Rubric-Marines"
# attributes_dict = scrape_attributes(url)
# print(attributes_dict)
