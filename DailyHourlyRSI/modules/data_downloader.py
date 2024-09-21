import yfinance as yf
import ta

def download_etf_data(etf_codes, start_date, interval='60m', rsi_window=14):
    etf_rsi = {}
    for etf in etf_codes:
        try:
            df = yf.download(etf, start=start_date, interval=interval)
            if df.empty:
                print(f"No data found for ETF: {etf}")
                continue
            df['RSI'] = ta.momentum.rsi(df['Close'], window=rsi_window)
            etf_rsi[etf.split('.')[0]] = df
        except Exception as e:
            print(f"Error downloading data for ETF {etf}: {str(e)}")
    return etf_rsi

def download_etf_daily_data(etf_codes, start_date, rsi_window=14):
    etf_daily_rsi = {}
    
    # Use a list comprehension to download data and calculate RSI for daily interval
    for etf in etf_codes:
        try:
            df = yf.download(etf, start=start_date, interval='1d')  # Daily interval
            if df.empty:
                print(f"No data found for ETF: {etf}")
                continue
            
            # Calculate RSI for daily data
            df['RSI'] = ta.momentum.rsi(df['Close'], window=rsi_window)
            etf_daily_rsi[etf.split('.')[0]] = df  # Store with ETF name without suffix

        except Exception as e:
            print(f"Error downloading data for ETF {etf}: {str(e)}")

    return etf_daily_rsi
