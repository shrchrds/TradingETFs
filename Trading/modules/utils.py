from datetime import time

def is_market_open(current_time):
    market_open = time(9, 15)
    market_close = time(15, 30)
    return market_open <= current_time <= market_close

import pandas as pd
import ta

def calculate_rsi(df, window=14):

    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=window).rsi()
    return df

def calculate_moving_averages(df, windows=[20, 50, 100, 200]):

    for window in windows:
        df[f'{window}DMA'] = ta.trend.SMAIndicator(df['Close'], window=window).sma_indicator()
    
    return df
