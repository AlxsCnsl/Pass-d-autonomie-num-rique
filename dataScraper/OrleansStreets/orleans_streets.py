import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.annuaire-mairie.fr/rue-orleans.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

print(response.status_code)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    divs = soup.find('div', class_="h2div listevoie")
    streets = [a.get_text(strip=True) for div in divs for a in div.find_all("a", href=True)]
    
    pk = 1
    streets_data = []
    for street in streets:
        data = {
        "model": "api.street",
        "pk": pk,
        "fields": {
            "town": 1,
            "name": f"{street}"
            }
        }
        streets_data.append(data)
        pk+=1
        
    print(streets_data)        
else:
    print(f"Erreur: {response.status_code}")['href']
    
    
with open("orleans_street.json", "w", encoding="utf-8") as file:
    json.dump(streets_data, file, indent=4, ensure_ascii=False)