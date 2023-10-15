# attributes.py
def fetch_attributes(char_wrap):
    # Extracting name if available
    name = extract_name(char_wrap)

    # Extracting data from dsCharWrap
    attributes_data = extract_values(char_wrap)

    # Extracting invulnerable save
    invulnerable_save = extract_invulnerable_save(char_wrap)

    # Extracting base size
    base_size = extract_base_size(char_wrap)

    # Adding name to each set of attributes if available
    for attributes_set in attributes_data:
        attributes_set["name"] = name

    # Adding invulnerable save and base size to each set of attributes
    for attributes_set in attributes_data:
        attributes_set["invulnerableSave"] = invulnerable_save
        attributes_set["base"] = base_size

    return attributes_data


def extract_name(char_wrap):
    # Find the dsModelName div
    ds_model_name = char_wrap.find('div', class_='dsModelName')

    if ds_model_name:
        return ds_model_name.get_text(strip=True)
    else:
        return None


def extract_values(char_wrap):
    attributes_data = []

    # Find the dsProfileWrapLeft div
    ds_profile_wrap_left = char_wrap.find('div', class_='dsProfileWrapLeft')

    if ds_profile_wrap_left:
        # Find all dsCharWrap divs inside dsProfileWrapLeft
        ds_char_wraps = ds_profile_wrap_left.find_all('div', class_='dsCharWrap')

        for ds_char_wrap in ds_char_wraps:
            # Create a dictionary to store the values
            values = {}

            # Extract the values
            values["movement"] = extract_value(ds_char_wrap, 0)
            values["toughness"] = extract_value(ds_char_wrap, 1)
            values["save"] = extract_value(ds_char_wrap, 2)
            values["wounds"] = extract_value(ds_char_wrap, 3)
            values["leadership"] = extract_value(ds_char_wrap, 4)
            values["objectiveControl"] = extract_value(ds_char_wrap, 5)

            # Add the values to the list
            attributes_data.append(values)

    return attributes_data


def extract_value(ds_char_wrap, index):
    # Find the dsCharValue div
    ds_char_value = ds_char_wrap.find_all('div', class_='dsCharValue')[index]

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


def extract_invulnerable_save(char_wrap):
    # Find the dsInvulWrap div
    ds_invul_wrap = char_wrap.find('div', class_='dsInvulWrap')

    if ds_invul_wrap:
        # Extract the text from dsInvulWrap
        invulnerable_save = ds_invul_wrap.get_text(strip=True)

        # Process the text to get the desired value
        return process_text(invulnerable_save)
    else:
        return 0  # Default value if dsInvulWrap is not present


def extract_base_size(char_wrap):
    # Find the dsModelBase div
    ds_model_base = char_wrap.find('div', class_='dsModelBase')

    if ds_model_base:
        # Extract the text from dsModelBase
        base_size = ds_model_base.get_text(strip=True)

        return base_size
    else:
        return None  # Default value if dsModelBase is not present
