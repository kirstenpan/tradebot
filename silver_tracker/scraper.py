import yfinance as yf
import sqlite3
import time
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'silver.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS silver_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_price(price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO silver_prices (timestamp, price)
        VALUES (?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price))
    conn.commit()
    conn.close()

def scrape_silver_price():
    print("Scraping silver price...")
    try:
        import requests
        from bs4 import BeautifulSoup
        
        req = requests.get('https://markets.businessinsider.com/commodities/silver-price', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        soup = BeautifulSoup(req.text, "html.parser")
        val_span = soup.find('span', {'class': 'price-section__current-value'})
        
        if val_span:
            # removing commas since prices > 1,000 can have commas e.g. "1,000.50"
            price_str = val_span.text.replace(',', '').strip()
            price = float(price_str)
            save_price(price)
            print(f"[{datetime.now()}] Scraped Silver Price: ${price:.2f}")
            return price
        else:
            print("No data available from Business Insider html.")
    except Exception as e:
        print(f"Error scraping price: {e}")
    return None

if __name__ == '__main__':
    init_db()
    # Run once upon execution
    scrape_silver_price()
