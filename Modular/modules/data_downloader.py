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
