from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'silver.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    conn = get_db_connection()
    # Get last 50 data points
    cursor = conn.execute('SELECT * FROM silver_prices ORDER BY timestamp ASC LIMIT 50')
    rows = cursor.fetchall()
    conn.close()
    
    data = []
    labels = []
    for row in rows:
        labels.append(row['timestamp'])
        data.append(row['price'])
        
    return jsonify({'labels': labels, 'data': data})

if __name__ == '__main__':
    # Initialize DB just in case scraper hasn't run yet
    from scraper import init_db, scrape_silver_price
    init_db()
    # Scrape 1 data point so the DB isn't empty, if empty
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM silver_prices')
    count = cur.fetchone()[0]
    conn.close()
    if count == 0:
        scrape_silver_price()
        
    app.run(debug=True, port=5000)
