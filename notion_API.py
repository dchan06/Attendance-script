import os, requests 
from dotenv import load_dotenv

load_dotenv()

def get_database_ids(headers): 
    search = requests.post(
        "https://api.notion.com/v1/search",
        headers=headers,
        json={"filter": {"property": "object", "value": "data_source"}},
    )
    for r in search.json()["results"]:
        title = r.get("title", [{}])
        name = title[0]["plain_text"] if title else "(untitled)"
        print(r["id"], "-", name)
        
def get_data_from_database(): 
    headers = {
            "Authorization": f"Bearer {os.getenv('NOTION_KEY')}", 
            "Notion-Version": "2026-03-11", 
            "Content-Type": "Application/json",
        }
    data_source_id = os.getenv('NOTION_DB_ID')
    
    response = requests.post(
        f"https://api.notion.com/v1/data_sources/{data_source_id}/query", 
        headers=headers,
    )
    response.raise_for_status()
    return response.json()["results"]

def main(): 
    results = get_data_from_database()
    print(results)
    
if __name__ == "__main__":
    main() 
