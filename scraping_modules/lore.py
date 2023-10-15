# scraping_modules/lore.py

import requests
from bs4 import BeautifulSoup


def get_pic_legend_title(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the div with class 'picLegend' and get its title attribute
        pic_legend_div = soup.find('div', class_='picLegend')
        if pic_legend_div:
            title = pic_legend_div.get('title')
            if title:
                return title
            else:
                return "Title not found in div with class 'picLegend'"
        else:
            return "Div with class 'picLegend' not found"
    else:
        return f"Failed to fetch URL. Status code: {response.status_code}"
