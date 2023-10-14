# scraping_modules/invulnerable.py
import re

def extract_invulnerable(html_content):
    # Find the specific div
    div_dsInvulWrap = html_content.find("div", class_="dsInvulWrap")

    if div_dsInvulWrap:
        # Use regular expression to extract numeric values
        numbers = re.findall(r'\d+', ' '.join(div_dsInvulWrap.stripped_strings))

        if numbers:
            for num in numbers:
                return int(num)  # Return the invulnerable save as an integer
        else:
            return 0  # Return 0 if no numbers found
    else:
        return 0  # Return 0 if no Invulnerable Save
