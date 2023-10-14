# scraping_modules/attributes.py
from bs4 import Tag
import re


def extract_attribute_value(char_wrap: Tag, char_name: str) -> int:
    char_name_element = char_wrap.find('div', class_='dsCharName', string=char_name)

    if char_name_element:
        char_frame = char_name_element.find_next('div', class_='dsCharFrame')
        char_frame_back = char_frame.find('div', class_='dsCharFrameBack')
        char_value_element = char_frame_back.find('div', class_='dsCharValue')

        if char_value_element:
            char_value_text = char_value_element.text.strip()

            # Use regular expression to extract the number
            match = re.search(r'\d+', char_value_text)

            if match:
                char_value = int(match.group())
                return char_value

    return 0


def fetch_attributes(char_wrap: Tag):
    # Fetch the first sibling dsCharWrap for 'toughness'
    toughness_char_wrap = char_wrap.find_next_sibling('div', class_='dsCharWrap')



    attributes = {
        "movement": extract_attribute_value(char_wrap, 'M'),
        "toughness": extract_attribute_value(toughness_char_wrap, 'T'),
        "save": extract_attribute_value(char_wrap, 'S'),
        "wounds": extract_attribute_value(char_wrap, 'W'),
        "leadership": extract_attribute_value(char_wrap, 'Ld'),
        "objectiveControl": extract_attribute_value(char_wrap, 'OC'),
    }

    return attributes
