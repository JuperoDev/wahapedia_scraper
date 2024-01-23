import requests
from bs4 import BeautifulSoup
import json

def scrape_wargear(url):
    wargear_list = []

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        if "WARGEAR OPTIONS" in soup.text:
            first_ul = soup.find("ul")

            if first_ul:
                wargear_list = process_ul(first_ul)

    for item in wargear_list:
        description = item["description"]
        if ":" in description:
            item["description"] = description.split(":", 1)[0].strip()

    return wargear_list

def process_ul(ul_tag):
    items = []

    for li_tag in ul_tag.find_all("li", recursive=False):
        description = li_tag.text.strip()
        item = {"description": description, "items": []}

        nested_ul = li_tag.find("ul")
        if nested_ul:
            item["items"] = [nested_li.text.strip() for nested_li in nested_ul.find_all("li")]
        
        items.append(item)

    return items
