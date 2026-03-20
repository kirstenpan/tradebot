import alpaca_trade_api as tradeapi
import os
import time

# --- CONFIG ---
API_KEY = os.getenv('ALPACA_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET')
BASE_URL = "https://paper-api.alpaca.markets"
SYMBOL = "TQQQ"

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def roll_forever():
    print("Robot status: 24/7 Active. Searching for alpha...")
    while True:
        try:
            # 1. Get 1-minute data for the 'Vibe Check'
            bars = api.get_bars(SYMBOL, '1Min', limit=20).df
            current_price = bars['close'].iloc[-1]
            sma = bars['close'].mean()

            # 2. Check current holdings
            positions = api.list_positions()
            is_holding = any(p.symbol == SYMBOL for p in positions)

            # 3. 24/5 Trading Logic
            if current_price > sma and not is_holding:
                print(f"BULLISH: Entry at {current_price}")
                api.submit_order(
                    symbol=SYMBOL,
                    qty=1, # Adjust based on your $100 balance
                    side='buy',
                    type='limit', # 24/5 trading requires LIMIT orders
                    limit_price=current_price,
                    time_in_force='day',
                    extended_hours=True # THIS IS KEY FOR 24/5
                )

            # 4. Sleep to stay within API rate limits (and stay free)
            time.sleep(60) 

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30) # Wait before retry

if __name__ == "__main__":
    roll_forever()
