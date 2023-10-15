# factionKeywords.py

from bs4 import BeautifulSoup


def extract_faction_keywords(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    faction_keywords_div = soup.find('div', class_='dsRightСolKW')

    if faction_keywords_div:
        faction_keywords_span = faction_keywords_div.find_all('span', class_='kwb')

        faction_keywords = [span.get_text(strip=True).lower() for span in faction_keywords_span]

        # If there are commas, split the faction keywords
        faction_keywords = [keyword for keywords in faction_keywords for keyword in keywords.split(', ')]

        return {"factionKeyword": faction_keywords}

    return {"factionKeyword": []}
