import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
url = "https://wahapedia.ru/wh40k10ed/factions/space-marines/Devastator-Squad"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the section with "wargear options"
    wargear_section = soup.find(text="wargear options").find_parent('section')
    
    # Find the first <ul> inside the wargear section
    first_ul = wargear_section.find('ul')
    
    # Create an empty list to store the objects
    wargear_objects = []
    
    # Iterate through the <li> elements inside the first <ul>
    for li in first_ul.find_all('li', recursive=False):
        # Create an object to store the data
        wargear_object = {'description': '', 'items': []}
        
        # Extract the description from the <li>
        wargear_object['description'] = li.find(text=True, recursive=False)
        
        # Check if there's a nested <ul> inside the <li>
        nested_ul = li.find('ul')
        if nested_ul:
            # Extract the items from the nested <ul>
            wargear_object['items'] = [item.text for item in nested_ul.find_all('li')]
        
        # Append the object to the list
        wargear_objects.append(wargear_object)
    
    # Print the extracted data
    for obj in wargear_objects:
        print("Description:", obj['description'])
        print("Items:", obj['items'])
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
