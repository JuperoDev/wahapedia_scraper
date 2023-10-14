# attributes.py
def fetch_attributes(char_wrap):
    # Extracting data from dsCharWrap
    movement = extract_value(char_wrap, 0)
    toughness = extract_value(char_wrap, 1)
    save = extract_value(char_wrap, 2)
    wounds = extract_value(char_wrap, 3)
    leadership = extract_value(char_wrap, 4)
    objective_control = extract_value(char_wrap, 5)

    # Print the extracted data
    print("Movement:", movement)
    print("Toughness:", toughness)
    print("Save:", save)
    print("Wounds:", wounds)
    print("Leadership:", leadership)
    print("Objective Control:", objective_control)

    # Save to a list with a single dictionary
    attributes_data = [{
        "movement": movement,
        "toughness": toughness,
        "save": save,
        "wounds": wounds,
        "leadership": leadership,
        "objectiveControl": objective_control
    }]

    return attributes_data


def extract_value(char_wrap, index):
    # Find the dsCharWrap div
    ds_char_wrap = char_wrap.find_all('div', class_='dsCharWrap')[index]

    # Find the dsCharValue div
    ds_char_value = ds_char_wrap.find('div', class_='dsCharValue')

    # Extract the text from dsCharValue
    text = ds_char_value.get_text(strip=True)

    # Process the text to get the desired value
    value = process_text(text)

    return value


def process_text(text):
    # Add your logic here to process the text and extract the desired value
    # For example, you can check if the text contains a number or a number followed by a plus symbol, etc.
    # Customize this according to your specific requirements.

    # Placeholder logic (you might need to adjust this based on actual text patterns)
    if '+' in text:
        value = int(text.split('+')[0])
    elif '"' in text or "'" in text:
        value = int(''.join(filter(str.isdigit, text)))
    else:
        value = int(text)

    return value
