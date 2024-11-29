# First install required packages:
# pip install requests beautifulsoup4 pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict

class WebScraper:
    def __init__(self, headers: Dict = None):
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def get_soup(self, url: str) -> BeautifulSoup:
        """Make request to URL and return BeautifulSoup object"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_books_toscrape(self) -> List[Dict]:
        """Scrape books from books.toscrape.com"""
        base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
        books = []
        
        for page in range(1, 3):  # Limit to 2 pages for example
            url = base_url.format(page)
            soup = self.get_soup(url)
            
            if not soup:
                continue
                
            for book in soup.select('article.product_pod'):
                title = book.h3.a['title']
                price = book.select_one('p.price_color').text
                availability = book.select_one('p.availability').text.strip()
                
                books.append({
                    'title': title,
                    'price': price,
                    'availability': availability
                })
                
            time.sleep(1)  # Be nice to the server
            
        return books

    def scrape_quotes_toscrape(self) -> List[Dict]:
        """Scrape quotes from quotes.toscrape.com"""
        url = 'http://quotes.toscrape.com'
        soup = self.get_soup(url)
        quotes = []
        
        if not soup:
            return quotes
            
        for quote in soup.select('div.quote'):
            text = quote.select_one('span.text').text
            author = quote.select_one('small.author').text
            tags = [tag.text for tag in quote.select('a.tag')]
            
            quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })
            
        return quotes

def main():
    scraper = WebScraper()
    
    # Scrape books
    print("Scraping books...")
    books = scraper.scrape_books_toscrape()
    books_df = pd.DataFrame(books)
    print(f"Found {len(books)} books")
    print(books_df.head())
    
    # Scrape quotes
    print("\nScraping quotes...")
    quotes = scraper.scrape_quotes_toscrape()
    quotes_df = pd.DataFrame(quotes)
    print(f"Found {len(quotes)} quotes")
    print(quotes_df.head())
    
    # Save to CSV
    books_df.to_csv('books.csv', index=False)
    quotes_df.to_csv('quotes.csv', index=False)

if __name__ == "__main__":
    main()