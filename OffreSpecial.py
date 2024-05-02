import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

data = []
url = "https://visitmarrakech.com/explore/?listing_category=offres&listing_tag=famille&listing_region=marrakech"
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
            continue
        
        img_style = card.find("a", class_='rz-image')['style']
        if img_style:
            img_url = img_style.split("url(")[-1].split(")")[0]
            img_url = img_url.replace("'", "")  # Supprimer les apostrophes simples du lien
            item['image'] = img_url
        else:
            print("Image style not found for a card.")


        title_elem = card.find("div", class_='rz-title')
        if title_elem:
            item['Title'] = title_elem.text.strip() 
        else:
            print("Title element not found for a card.")
            continue

        city_elem = card.find("div", class_='rz-listing-details rz-listing-details-content')
        if city_elem:
            item['City'] = city_elem.text.strip().split()[0]
        else:
            print("City element not found for a card.")
            continue  

        price_elem = card.find("div", class_='rz-listing-tagline')
        if price_elem:
            item['Price'] = price_elem.text.strip()
            
        else:
            print("Price element not found for a card.")
            continue  
        item['categorie'] = "Special Offers"
        item['date_P'] = ""
        item['type'] = ""

        data.append(item)
        time.sleep(2)


df = pd.DataFrame(data)



df.to_csv("OffreSpecial.csv", index=False)
