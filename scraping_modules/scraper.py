# scraping_modules/scraper.py
import requests
from bs4 import BeautifulSoup


def fetch_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div with class 'dsH2Header'
    header_div = soup.find('div', class_='dsH2Header')

    if header_div:
        # Find the inner div with text
        inner_div = header_div.find('div')

        if inner_div:
            # Extract the text content
            fetched_text = inner_div.text.strip()
            return fetched_text

    return None


def get_page(url):
    return requests.get(url)


def main():
    url = "https://wahapedia.ru/wh40k10ed/factions/tyranids/Winged-Hive-Tyrant"
    fetched_text = fetch_text(url)

    if fetched_text:
        # Replace spaces with "-" and convert to lowercase
        filename = f"{fetched_text.replace(' ', '-').lower()}.json"

        # Fetch the page
        response = get_page(url)

        # Create a dictionary with the data
        data = {
            "parentUnit": fetched_text,
            "raw_html": response.text  # Save the raw HTML if needed
        }




if __name__ == "__main__":
    main()
