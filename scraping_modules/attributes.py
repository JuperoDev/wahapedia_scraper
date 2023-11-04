import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_attributes(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        ds_profile_base_wrap_divs = soup.find_all('div', class_='dsProfileBaseWrap')

        attributes_list = []

        for div in ds_profile_base_wrap_divs:
            model_name_div = div.find('span', class_='dsModelName')

            if model_name_div:
                name = model_name_div.text.strip().lower()
                profile_wrap_left_div = div.find('div', class_='dsProfileWrapLeft')

                if profile_wrap_left_div:
                    char_frame_back_divs = profile_wrap_left_div.find_all('div', class_='dsCharFrameBack')
                    char_attributes = []

                    for char_frame_back_div in char_frame_back_divs:
                        char_text = char_frame_back_div.text.strip()
                        char_values = char_text.split()
                        char_attributes.extend(char_values)

                    char_dict = {
                        "name": name,
                        "movement": int(re.search(r'\d+', char_attributes[0]).group()),
                        "toughness": int(re.search(r'\d+', char_attributes[1]).group()),
                        "salvation": int(re.search(r'\d+', char_attributes[2]).group()),
                        "wounds": int(re.search(r'\d+', char_attributes[3]).group()),
                        "leadership": int(re.search(r'\d+', char_attributes[4]).group()),
                        "objectiveControl": int(re.search(r'\d+', char_attributes[5]).group())
                    }

                    attributes_list.append(char_dict)

        return attributes_list

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

# Example usage:
# url = "https://wahapedia.ru/wh40k10ed/factions/thousand-sons/Rubric-Marines"
# attributes_list = scrape_attributes(url)
# print(attributes_list)
