# TradeBot Terminal Dashboard

A real-time stock portfolio monitoring dashboard with institutional-grade analysis, live price feeds, news aggregation using web-scraping.

---

## Quick Start

### Prerequisites

- **Python 3.9+** — [Download here](https://www.python.org/downloads/)
- **pip** (comes bundled with Python)
- Internet connection (live data is pulled from Yahoo Finance)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/kirstenpan/tradebot.git
cd tradebot
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**macOS / Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
python app.py
```

You should see output like:

```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:8080
```

Open your browser and navigate to:

**[http://localhost:8080](http://localhost:8080)**

---

## Main Features

- **Live Portfolio Prices** — Real-time price, % change, and volume for all tracked tickers
- **Market Status** — Countdown to market open/close
- **Intelligence Reports** — Click any ticker to generate a full institutional analysis report
- **News Feed** — Top headlines per ticker aggregated automatically
- **Volume Anomaly Alerts** — Flags tickers with abnormal trading volume
- **Manual Refresh** — Trigger an immediate data refresh at any time

### Tracked Portfolio

| Ticker | DESC |
|--------|-------------|
| VOO | Vanguard S&P 500 ETF |
| QQQ | Invesco NASDAQ-100 ETF |
| GOOG | Alphabet Inc. |
| AG | First Majestic Silver |
| EXK | Endeavour Silver Corp |
| HL | Hecla Mining |
| ITRG | Integra Resources |
| UAMY | US Antimony Corp |
| NB | NioCorp Developments |
| MTA | Metalla Royalty & Streaming |
| UPS | United Parcel Service |

---

## Data Refresh

- Data automatically refreshes every **60 minutes** while the market is open.
- To force an immediate refresh, click the **"↻ MANUAL TRIGGER SYNC"** button on the dashboard.

---

## Project Structure

```
tradebot/
├── app.py              # Main Flask application & data logic
├── templates/
│   └── dashboard.html  # Frontend dashboard UI
├── test_news.py        # News feed test script
├── test_yf.py          # Yahoo Finance connectivity test
└── README.md
```

---

## Troubleshooting

**Port already in use:**
```bash
# Find the process using port 8080
lsof -i :8080
# Kill it
kill -9 <PID>
```

**Module not found errors:**
Make sure your virtual environment is activated before running `python app.py`.

**Blank page / no data:**
The app fetches data in a background thread on startup. Wait ~10–15 seconds and then click **"↻ MANUAL TRIGGER SYNC"**.

---
