import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

data = []
url = "https://visitmarrakech.com/explore/?onpage=1&listing_category=evenements&listing_region=marrakech"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser") 

if soup.title.text == "404 Not Found":
    print("The URL is not found.")
else:
    all_cards = soup.find_all("li", class_="rz-listing-item rz-display-type--grid")
    
    for card in all_cards:
        item = {}
        link_elem = card.find("a", class_='rz-listing-content')
        if link_elem:
            item['Link'] = link_elem.attrs.get("href", "Link not found") 
        else:
            print("Link element not found for a card.")
            item['Link'] = None
        
        img_elem = card.find("a", class_='rz-image')
        if img_elem and 'style' in img_elem.attrs:
            img_style = img_elem['style']
            img_url = img_style.split("url(")[-1].split(")")[0]
            img_url = img_url.replace("'", "") 
            item['image'] = img_url
        else:
            print("Image style not found for a card.")
            item['image'] = None

        title_elem = card.find("div", class_='rz-title')
        if title_elem:
            item['Title'] = title_elem.text.strip() 
        else:
            print("Title element not found for a card.")
            item['Title'] = None

        item['City'] = "Marrakech"
        
        date_elem = card.find("div", class_='rz-listing-tagline')
        if date_elem:
            item['date_P'] = date_elem.text.strip()            
        else:
            print("Date element not found for a card.")
            item['date_P'] = None

        # Add Price and type attributes with null values
        item['Price'] = ""
        item['type'] = ""
        item['categorie'] = "Evenement"

        data.append(item)
        time.sleep(2)

df = pd.DataFrame(data)
df.to_csv("evenement.csv", index=False)
