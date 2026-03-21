# TradeBot Terminal Dashboard

A real-time stock portfolio monitoring dashboard with institutional-grade analysis, live price feeds, news aggregation using web-scraping.

---

Quick Start for New Users
Follow these steps to get the dashboard running on your local machine.

1. Clone the Repository
Open your terminal and run:

Bash
git clone https://github.com/kirstenpan/tradebot.git
cd tradebot
2. Set Up a Virtual Environment (Recommended)
This ensures the app's dependencies don't interfere with your global Python settings.

macOS / Linux:

Bash
python3 -m venv venv
source venv/bin/activate
Windows:

Bash
python -m venv venv
.\venv\Scripts\activate
3. Install Dependencies
Install the required libraries (Flask, yfinance, etc.) using the included "grocery list":

Bash
pip install -r requirements.txt
4. Run the Application
Bash
python app.py
Using the Dashboard
Once the app is running, open your browser and go to:
http://localhost:8080

Key Features
Live Portfolio Tracking: Real-time data for VOO, QQQ, and high-conviction silver/mining stocks (AG, EXK, HL, etc.).

Institutional Intelligence: Automated reports and news aggregation for every ticker in the portfolio.

Manual Sync: Use the "↻ MANUAL TRIGGER SYNC" button to force a data refresh if the market is moving fast.

Project Structure
Plaintext
tradebot/
├── app.py              # Core logic, Flask server, and data fetching
├── templates/          # Frontend UI (HTML/CSS)
│   └── dashboard.html  
├── requirements.txt    # List of necessary Python libraries
├── .gitignore          # Prevents bulky 'venv' files from being uploaded
├── test_news.py        # Utility for testing news scraping logic
└── test_yf.py          # Utility for testing Yahoo Finance API
Troubleshooting
"ModuleNotFoundError"
Ensure you have activated your virtual environment (Step 3) before running the app. You should see (venv) at the start of your terminal line.

Port 8080 is Busy
If another app is using port 8080, you can kill the process:

Mac: lsof -i :8080 then kill -9 [PID]

Windows: netstat -ano | findstr :8080 then taskkill /PID [PID] /F

Data is Blank on Startup
The app fetches institutional data in the background. If the table is empty, wait 15 seconds and click the Manual Trigger Sync button to populate the dashboard.

