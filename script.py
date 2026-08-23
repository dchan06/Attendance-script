import notion_API

import json

# key refers to the row name given in notion
def find_key(data, target_key, path=""):    # search function to find the detail I am looking for 
    matches = []
    
    if isinstance(data, dict): 
        for key, value in data.items(): 
            new_path = f"{path}.{key}" if path else key
            if key == target_key: 
                matches.append((new_path, value))
            matches.extend(find_key(value, target_key, new_path))   # extend makes this current list longer 
    elif isinstance(data, list): 
        for i, item in enumerate(data):     # enumerate assigns a number to the item starting from 0. Turns the objects in enumerate object into tuples
            new_path=f"{path}[{i}]"
            matches.extend(find_key(item, target_key, new_path))
            
    return matches

# item_needed refers to the actual item from the key needed to format the data nicely. Item must be a string
def find_item(data, item_key):
    if isinstance(data, dict): 
        for key, value in data.items(): 
            if key == item_key: 
                return value
            found = find_item(value, item_key)
            if found is not None: 
                return found
    return None

def format_data(page): 
    date_targets = ["start", "end"]
    data = find_key(page, "Dates")
    name = find_key(page, "Name")
    dates = [(item ,find_item(obj[1], item)) for obj in data for item in date_targets]
    print (dates)
    ...     
    '''
    TO-DO: 
        - If the data falls within the rage (21st of last month - 20th of this month) look for the name and remarks, 
        if not ignore it
            -> Use the path from using find key to determine which object from pages to look at.
            -> From there it should be easy
        - Format the data into a CSV 
    '''
    
        
    
def main(): 
    page = notion_API.get_data_from_database()
    format_data(page)

    # print (type(page[0]['object']))   # for debugging find_key function to check the the object's type
    
    # print(json.dumps(page[1], indent=2))    # pretty print for JSON data
    
if __name__ == "__main__": 
    main()