# scraping_modules/keywords.py
from bs4 import BeautifulSoup


def extract_keywords(html):
    soup = BeautifulSoup(html, 'html.parser')
    ds_left_col_kw = soup.find('div', class_='dsLeftСolKW')

    if ds_left_col_kw:
        keywords_text = ds_left_col_kw.get_text(strip=True)

        # Replace non-breaking space with a regular space
        keywords_text = keywords_text.replace('\xa0', ' ')

        # Remove "KEYWORDS: " text and split the keywords
        raw_keywords = keywords_text.split('KEYWORDS:')[1].split(',')

        # Further split each word and add a space
        keywords_list = [word.strip().lower() for keyword in raw_keywords for word in keyword.replace(" ", "").split()]

        return keywords_list
    else:
        return None
