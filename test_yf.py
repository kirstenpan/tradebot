import yfinance as yf
def test():
    try:
        data = yf.Ticker("VOO").history(period="1d")
        print("VOO:", data['Close'].iloc[-1])
    except Exception as e:
        print("Error:", e)
test()
