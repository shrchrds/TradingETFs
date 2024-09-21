from datetime import time

def is_market_open(current_time):
    market_open = time(9, 15)
    market_close = time(15, 30)
    return market_open <= current_time <= market_close
