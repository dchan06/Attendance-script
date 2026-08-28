import notion_API
from datetime import date, timedelta

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
    elif isinstance(data, list) or isinstance(data, tuple): 
        for i, item in enumerate(data): 
            found = find_item(item, item_key)
            if found is not None: 
                return found
    return None

def date_falls_within(period, start_date: str, end_date: str, line_item: str): 
    # print(f"{line_item}: {start_date} - {end_date}")
    # start_date_list = start_date.split("-")
    # new_start_date = date(int(start_date_list[0]), int(start_date_list[1]), int(start_date_list[2]))  # if I had to parse it myself I would make this a function
    new_start_date = date.fromisoformat(start_date)     # Since date is already in a YYYY-MM-DD format I can use date.fromisoformat instead of parsing it myself
    new_end_date = date.fromisoformat(end_date)
    # not within period
    if new_end_date < period[0] or new_start_date > period[1]:
        return None
    # if all the dates are within this period
    if new_start_date >= period[0] and new_end_date <= period[1]: 
        current = new_start_date
        end = new_end_date 
    elif new_start_date >= period[0] and new_end_date > period[1]: 
        current = new_start_date
        end = period[1]
    elif new_start_date < period[0] and new_end_date <= period[1]: 
        current = period[0]
        end = new_end_date
        
    dates = []
    while current <= end: 
        dates.append(current)
        current += timedelta(days=1)
    return dates

def format_absence_data(period: tuple[date, date]=(date(2026, 7, 21), date(2026, 8, 20))):
    page = notion_API.get_data_from_database()
    for obj in page: 
        date_obj = find_key(obj, "Dates")
        date_str = (find_item(date_obj, "start"), find_item(date_obj, "end"))
        name_obj = find_key(obj, "Name")
        name_str = find_item(name_obj, "content")
        ''' 
        Why I used find key first
            - In notion there might be multiple rows where the type is date (e.g Dates & Completed date)
            - In this case if I were to want to find the start date for 'Completed date', and I do find_key(page, "start") 
            I would get the start value for the wrong field ('Dates' instead of 'Complete date')
        '''
        absent_dates = date_falls_within(period, date_str[0], date_str[1], name_str)
        '''
        If date_falls_within is none: 
            Don't do anything
        Do format it to CSV in a way that can be easily imported to my Excel
        '''
    return absent_dates
    
        
    
def main(): 
    format_absence_data()

    # print (type(page[0]['object']))   # for debugging find_key function to check the the object's type
    
    # print(json.dumps(page[1], indent=2))    # pretty print for JSON data
    
if __name__ == "__main__": 
    main()