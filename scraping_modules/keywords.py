# keywords.py

import requests
from bs4 import BeautifulSoup

def scrape_keywords(url):
    # Fetch HTML content from the URL
    response = requests.get(url)
    html = response.text

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find the element with class "dsLeftСolKW"
    keywords_element = soup.find('div', class_='dsLeftСolKW')

    # Extract text content and convert to lowercase
    keywords_text = keywords_element.get_text().lower()

    # Remove "keywords:" from the text
    keywords_text = keywords_text.replace('keywords:', '').strip()

    # Split by commas and strip whitespace
    keywords_list = [word.strip() for word in keywords_text.split(',')]

    # Join kwb spans with a space
    keywords_list = [' '.join(word.split()) for word in keywords_list]

    return keywords_list
