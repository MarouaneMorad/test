from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_hotels(page):
    hotels = page.locator('//div[@data-testid="property-card"]').all()
    hotels_list = []

    for hotel in hotels:
        hotel_dict = {}
        try:
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text().split()[0]
            
            #hotel_dict['image'] = hotel.locator('//img[contains(@class, "hotel-image")]/@src').get_attribute('src')
        except Exception as e:
            print(f"Error occurred while scraping hotel data: {e}")
            continue
        
        hotels_list.append(hotel_dict)

    return hotels_list

def main():
    with sync_playwright() as p:
        # IMPORTANT: Change dates to future dates, otherwise it won't work
        checkin_date = '2024-05-01'
        checkout_date = '2024-05-02'
        page_url = f'https://www.booking.com/searchresults.fr.html?label=bin859jc-1DCAMojAE4mANIDVgDaIwBiAEBmAENuAEXyAEM2AED6AEB-AECiAIBqAIDuALnvKWwBsACAdICJDAyZjMzNDEzLWEyYTQtNGIxYy1hZTQ4LTJlOTVkMWZiM2QwZNgCBOACAQ&sid=b10d0ae1f4795c05f4dce9417c23d050&aid=357028&checkin={checkin_date}&checkout={checkout_date}&dest_id=-40775&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0'

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)  # Augmenter le délai d'attente à 60 secondes (60000 millisecondes)


        hotels_list = scrape_hotels(page)

        df = pd.DataFrame(hotels_list)
        df.to_excel('hotel_list.xlsx', index=False) 
        df.to_csv('hotel_list.csv', index=False) 

        browser.close()

if __name__ == '__main__':
    main()
