import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage to scrape
url = "https://wahapedia.ru/wh40k10ed/factions/adepta-sororitas/Aestred-Thurga-And-Agathae-Dolan"

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
                        char_dict["movement"] = int(attr.split('"')[0])  # Extract and convert to int
                    elif i == 2:
                        char_dict["toughness"] = int(attr)  # Convert to int
                    elif i == 3:
                        char_dict["salvation"] = int(attr.split('+')[0])  # Extract and convert to int
                    elif i == 4:
                        char_dict["wounds"] = int(attr)  # Convert to int
                    elif i == 5:
                        char_dict["leadership"] = int(attr.split('+')[0])  # Extract and convert to int
                    elif i == 6:
                        char_dict["objetiveControl"] = int(attr)  # Convert to int

                # Append the extracted name and attributes to the list
                attributes.append({"name": name, **char_dict})

    # Create the desired output dictionary
    output = {"attributes": attributes}

    # Format the output as JSON-like string with indentation
    formatted_output = json.dumps(output, indent=4)

    # Print the formatted output
    print(formatted_output)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
