import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

data = []
url = "https://visitmarrakech.com/en/explore/?type=restaurants"
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
            img_url = img_url.replace("'", "")
            item['image'] = img_url
        else:
            print("Image style not found for a card.")

        title_elem = card.find("div", class_='rz-title')
        if title_elem:
            item['Title'] = title_elem.text.strip() 
        else:
            print("Title element not found for a card.")
            continue 

        # type_elem = card.find("div",class_='rz-listing-details rz-listing-details-content')
        # if type_elem :
        #     item['type'] = type_elem.text.strip().split()[1]
        # else:
        #     print("type element not found for a card.")
        #     continue  
        City_elem = card.find("div",class_='rz-listing-details rz-listing-details-content')
        if City_elem :
            item['City'] = City_elem .text.strip().split()[0]
        else:
            print("City element not found for a card.")
            continue  
        item['type'] = "restaurants"
        item['Price'] = ""
        item['date_P'] = ""
        item['categorie'] = "Restaut & Cafe"
        data.append(item)
        #Very important
        # Sleep for 2 seconds before making the next request
        time.sleep(2)

# Create DataFrame
df = pd.DataFrame(data)

df.to_csv("ScrapRs.csv", index=False)
