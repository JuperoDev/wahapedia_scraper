# main.py

from scraping_modules import parentUnit


def main():
    #  URL to scrape from wahapedia.ru
    url_to_scrape = "https://wahapedia.ru/wh40k10ed/factions/agents-of-the-imperium/Rogue-Trader-Entourage"

    # Calling the scrape function from parentUnit module
    parentUnit.scrape_parent_unit(url_to_scrape)


if __name__ == "__main__":
    main()
