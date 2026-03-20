import alpaca_trade_api as tradeapi
import os
import sys

# --- CONFIGURATION (Using GitHub Secrets for Security) ---
API_KEY = os.getenv('ALPACA_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET')
BASE_URL = "https://paper-api.alpaca.markets"
SYMBOL = "TQQQ"

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def run_robot():
    try:
        account = api.get_account()
        if float(account.cash) < 1.0 and not api.list_positions():
            print("Account empty. Deposit $100 virtual cash in Alpaca.")
            return

        # 1. Simple "Vibe" Check (Price vs 15-min average)
        bars = api.get_bars(SYMBOL, '1Min', limit=15).df
        current_price = bars['close'].iloc[-1]
        ma = bars['close'].mean()

        # 2. Check if we already have a position
        positions = api.list_positions()
        has_position = any(p.symbol == SYMBOL for p in positions)

        # 3. Execution Logic
        if current_price > ma and not has_position:
            # Use 95% of buying power to account for fluctuations
            qty = int((float(account.buying_power) * 0.95) / current_price)
            if qty > 0:
                print(f"BULLISH VIBE: Buying {qty} shares of {SYMBOL}")
                api.submit_order(
                    symbol=SYMBOL, qty=qty, side='buy', type='market', 
                    time_in_force='gtc', order_class='oto',
                    trailing_stop={"trail_percent": 5.0} # Roll the gains!
                )
        elif current_price < ma and has_position:
            print("BEARISH VIBE: Selling position to protect capital.")
            api.submit_order(symbol=SYMBOL, qty=qty, side='sell', type='market', time_in_force='gtc')
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_robot()
