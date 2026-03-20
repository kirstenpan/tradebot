import alpaca_trade_api as tradeapi
import pandas as pd
import time

# --- CONFIGURATION (Get these from Alpaca Paper Dashboard) ---
API_KEY = "YOUR_API_KEY"
SECRET_KEY = "YOUR_SECRET_KEY"
BASE_URL = "https://paper-api.alpaca.markets"

SYMBOL = "TQQQ" # 3x Leveraged Nasdaq - high volatility for high gains
TRAILING_STOP_PERCENT = 5.0 # Sells if it drops 5% from its high

# Initialize API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def get_signal():
    """Simple trend following: is the price above its 15-min average?"""
    bars = api.get_bars(SYMBOL, '1Min', limit=15).df
    ma = bars['close'].mean()
    current = bars['close'].iloc[-1]
    return "BUY" if current > ma else "WAIT"

def roll_the_dice():
    print(f"Robot starting... Goal: Roll $100 into 10x-100x on {SYMBOL}")
    
    while True:
        try:
            # 1. Check if we are already in a trade
            try:
                api.get_position(SYMBOL)
                print("Holding position... letting it roll.")
            except:
                # 2. No position? Look for entry
                if get_signal() == "BUY":
                    account = api.get_account()
                    # Use ALL available buying power (Margin)
                    buying_power = float(account.buying_power)
                    current_price = api.get_latest_trade(SYMBOL).price
                    qty = int(buying_power / current_price)
                    
                    if qty > 0:
                        print(f"BUYING {qty} shares of {SYMBOL} at {current_price}")
                        api.submit_order(
                            symbol=SYMBOL,
                            qty=qty,
                            side='buy',
                            type='market',
                            time_in_force='gtc',
                            order_class='oto', # One-Triggers-Other
                            trailing_stop={"trail_percent": TRAILING_STOP_PERCENT}
                        )
            
            # 3. Sleep for 1 minute (Free tier friendly)
            time.sleep(60)
            
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    roll_the_dice()
