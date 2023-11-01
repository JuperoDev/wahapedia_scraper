import requests
from bs4 import BeautifulSoup
import json
import re

# URL of the webpage to scrape
url = "https://wahapedia.ru/wh40k10ed/factions/adepta-sororitas/Missionary"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the div elements with class "dsProfileBaseWrap"
    divs = soup.find_all('div', class_='dsProfileBaseWrap')

    # Determine the number of divs found
    num_divs = len(divs)

    # Create a list to store the extracted information for each div
    attributes = []

    if num_divs == 2:
        # Case with two dsProfileBaseWrap divs (as before)
        for div in divs:
            # Find the "dsModelName" div within each "dsProfileBaseWrap" div
            model_name_div = div.find('span', class_='dsModelName')

            if model_name_div:
                # Extract the text (name) from the "dsModelName" div and convert to lowercase
                name = model_name_div.text.strip().lower()

                # Find the "dsProfileWrapLeft" div within the current "dsProfileBaseWrap" div
                profile_wrap_left_div = div.find('div', class_='dsProfileWrapLeft')

                if profile_wrap_left_div:
                    # Find all the "dsCharFrameBack" divs within the "dsProfileWrapLeft" div
                    char_frame_back_divs = profile_wrap_left_div.find_all('div', class_='dsCharFrameBack')

                    # Extract the text from each "dsCharFrameBack" div and split them into separate attributes
                    char_attributes = []
                    for char_frame_back_div in char_frame_back_divs:
                        char_text = char_frame_back_div.text.strip()
                        char_values = char_text.split()
                        char_attributes.extend(char_values)

                    # Create a dictionary to store the extracted attributes with renamed fields
                    char_dict = {}
                    for i, attr in enumerate(char_attributes, start=1):
                        if i == 1:
                            char_dict["movement"] = int(re.search(r'\d+', attr).group())  # Extract and convert to int
                        elif i == 2:
                            char_dict["toughness"] = int(re.search(r'\d+', attr).group())  # Extract and convert to int
                        elif i == 3:
                            char_dict["salvation"] = int(re.search(r'\d+', attr).group())  # Extract and convert to int
                        elif i == 4:
                            char_dict["wounds"] = int(re.search(r'\d+', attr).group())  # Extract and convert to int
                        elif i == 5:
                            char_dict["leadership"] = int(re.search(r'\d+', attr).group())  # Extract and convert to int
                        elif i == 6:
                            char_dict["objetiveControl"] = int(
                                re.search(r'\d+', attr).group())  # Extract and convert to int

                    # Append the extracted name and attributes to the list
                    attributes.append({"name": name, **char_dict})
    elif num_divs == 1:
        # Case with one dsProfileBaseWrap div
        div = divs[0]
        # Find the "dsProfileWrap" div within the single "dsProfileBaseWrap" div
        profile_wrap_div = div.find('div', class_='dsProfileWrap')

        if profile_wrap_div:
            # Find all the "dsCharWrap" divs within the "dsProfileWrap" div
            char_wrap_divs = profile_wrap_div.find_all('div', class_='dsCharWrap')

            if len(char_wrap_divs) == 6:
                # There are six dsCharWrap divs as expected
                char_attributes = [char_wrap_div.text.strip() for char_wrap_div in char_wrap_divs]

                # Create a dictionary to store the extracted attributes with renamed fields
                char_dict = {
                    "movement": int(re.search(r'\d+', char_attributes[0]).group()),  # Extract and convert to int
                    "toughness": int(re.search(r'\d+', char_attributes[1]).group()),  # Extract and convert to int
                    "salvation": int(re.search(r'\d+', char_attributes[2]).group()),  # Extract and convert to int
                    "wounds": int(re.search(r'\d+', char_attributes[3]).group()),  # Extract and convert to int
                    "leadership": int(re.search(r'\d+', char_attributes[4]).group()),  # Extract and convert to int
                    "objetiveControl": int(re.search(r'\d+', char_attributes[5]).group())  # Extract and convert to int
                }

                # Append the extracted attributes to the list
                attributes.append(char_dict)

    # Create the desired output dictionary
    output = {"attributes": attributes}

    # Format the output as JSON-like string with indentation
    formatted_output = json.dumps(output, indent=4)

    # Print the formatted output
    print(formatted_output)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
