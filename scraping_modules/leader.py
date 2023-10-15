from bs4 import BeautifulSoup
import requests

def scrape_leader(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        ds_right_col_div = soup.find('div', class_='dsRightСol dsColorFrAS')

        if ds_right_col_div:
            lower_text = ds_right_col_div.get_text().lower()
            target_text = "this model can be attached to the following".lower()

            if target_text in lower_text:
                a_tags = ds_right_col_div.select('.dsAbility ul li a.kwbOne')
                result_list = [a_tag.text.strip().lower() for a_tag in a_tags]
                return result_list
            else:
                return []
        else:
            return []
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

# Example usage:
# url = "https://wahapedia.ru/wh40k10ed/factions/thousand-sons/Rubric-Marines"
# leader_list = scrape_leader(url)
# print(leader_list)
