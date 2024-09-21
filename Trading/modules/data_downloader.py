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
    etf_daily_rsi_ma = {}
    
    # Loop through ETFs to download daily data and calculate RSI + Moving Averages
    for etf in etf_codes:
        try:
            df = yf.download(etf, start=start_date, interval='1d')  # Daily interval
            if df.empty:
                print(f"No data found for ETF: {etf}")
                continue
            
            # Calculate Daily RSI
            df['RSI'] = ta.momentum.rsi(df['Close'], window=rsi_window)
            
            # Calculate Moving Averages
            df['20DMA'] = df['Close'].rolling(window=20).mean()
            df['50DMA'] = df['Close'].rolling(window=50).mean()
            df['100DMA'] = df['Close'].rolling(window=100).mean()
            df['200DMA'] = df['Close'].rolling(window=200).mean()
            
            # Store the dataframe with RSI and Moving Averages
            etf_daily_rsi_ma[etf.split('.')[0]] = df  # Store with ETF name without suffix

        except Exception as e:
            print(f"Error downloading data for ETF {etf}: {str(e)}")

    return etf_daily_rsi_ma
