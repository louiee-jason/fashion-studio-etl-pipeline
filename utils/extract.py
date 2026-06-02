import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def scrape_main(base_url="https://fashion-studio.dicoding.dev", total_pages=50):
    data = []
    session = requests.Session()
    
    for page in range(1, total_pages + 1):
        url = f"{base_url}/?page={page}"
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            products = soup.find_all('div', class_='collection-card')
            
            for prod in products:
                title_elem = prod.find('h3', class_='product-title')
                title = title_elem.text.strip() if title_elem else "Unknown Product"
                
                price_elem = prod.find('span', class_='price')
                price = price_elem.text.strip() if price_elem else None
                
                paragraphs = prod.find_all('p')
                rating = None
                colors = None
                size = None
                gender = None
                
                for p in paragraphs:
                    text = p.text.strip()
                    if 'Rating:' in text or '⭐' in text:
                        rating = text.replace('Rating:', '').replace('⭐', '').strip()
                    elif 'Colors' in text:
                        colors = text
                    elif 'Size:' in text:
                        size = text
                    elif 'Gender:' in text:
                        gender = text
                
                timestamp = datetime.now().isoformat()
                
                data.append({
                    'Title': title,
                    'Price': price,
                    'Rating': rating,
                    'Colors': colors,
                    'Size': size,
                    'Gender': gender,
                    'timestamp': timestamp
                })
                
            logging.info(f"Successfully scraped page {page}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error scraping page {page}: {e}")
            continue
            
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = scrape_main(total_pages=2)
    print(df.head())
