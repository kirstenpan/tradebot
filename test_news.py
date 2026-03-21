import yfinance as yf
ticker = yf.Ticker("VOO")
print(ticker.news)
