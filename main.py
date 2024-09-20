import streamlit as st
import yfinance as yf
import ta
import os
import pandas as pd
from datetime import date, timedelta,datetime, time

# ETF codes
etf_codes = [
    'CPSEETF.NS', 'GOLDBEES.NS', 'NIF100IETF.NS', 'LOWVOLIETF.NS', 'ALPHAETF.NS', 
    'HDFCMOMENT.NS', 'QUAL30IETF.NS', 'NIFTYBEES.NS', 'EQUAL50ADD.NS', 'NV20IETF.NS', 
    'MONIFTY500.NS', 'ALPHA.NS', 'ALPL30IETF.NS', 'AUTOIETF.NS', 'BANKETFADD.NS', 
    'COMMOIETF.NS', 'DIVOPPBEES.NS', 'BFSI.NS', 'FINIETF.NS', 'FMCGIETF.NS', 
    'HEALTHY.NS', 'CONSUMBEES.NS', 'TNIDETF.NS', 'MAKEINDIA.NS', 'INFRABEES.NS',
    'ITBEES.NS', 'MOM100.NS', 'MIDCAPETF.NS', 'MIDSMALL.NS', 'MNC.NS',
    'JUNIORBEES.NS', 'PHARMABEES.NS', 'PVTBANIETF.NS', 'PSUBNKBEES.NS',
    'MOREALTY.NS', 'HDFCSML250.NS', 'SMALLCAP.NS', 'BSE500IETF.NS',
    'ICICIB22.NS', 'MOVALUE.NS', 'MOHEALTH.NS', 'MIDSELIETF.NS', 'EVINDIA.NS', 'MAFANG.NS'
    'HDFCSENSEX.NS', 'SILVERBEES.NS', 'MONQ50.NS', 'ESG.NS', 'MODEFENCE.NS', 'MULTICAP.NS','ABSLPSE.NS'
]

def download_etf_data(etf_codes, start_date, interval='60m', rsi_window=14):
    etf_rsi = {}
    
    # Use a list comprehension to download data and calculate RSI
    for etf in etf_codes:
        try:
            df = yf.download(etf, start=start_date, interval=interval)
            if df.empty:
                print(f"No data found for ETF: {etf}")
                continue
            
            # Calculate RSI directly if data is available
            df['RSI'] = round(ta.momentum.rsi(df['Close'], window=rsi_window),2)
            etf_rsi[etf.split('.')[0]] = df  # Store with ETF name without suffix

        except Exception as e:
            print(f"Error downloading data for ETF {etf}: {str(e)}")

    return etf_rsi

def save_data_locally(etf_rsi_data, filename='etf_data.pkl'):
    pd.to_pickle(etf_rsi_data, filename)  # Directly use pandas' function

def load_local_data(filename='etf_data.pkl'):
    return pd.read_pickle(filename) if os.path.exists(filename) else None
    
def get_latest_rsi_data(etf_codes, days_difference=729, filename='etf_data.pkl'):
    etf_rsi_data = load_local_data(filename)
    
    today = date.today()
    start_date = today - timedelta(days=days_difference)
    
    # Check if today is a weekday (Monday to Friday)
    if today.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        st.write("Today is a weekend. Using local data.")
        return etf_rsi_data
    
    # Check if current time is within the market hours (9:15 AM to 3:30 PM)
    current_time = datetime.now().time()
    market_open = time(9, 15)
    market_close = time(15, 30)
    
    # Update data on hourly basis during market hours
    if not (market_open <= current_time <= market_close):
        st.write("Market is closed. Using local data.")
        return etf_rsi_data

    # Check if local data already has today's data and update every hour
    if etf_rsi_data:
        latest_dates = {etf: df.index[-1].date() for etf, df in etf_rsi_data.items()}
        if all(latest_date == today for latest_date in latest_dates.values()):
            last_update_time = datetime.now() - timedelta(hours=1)  # Check for hourly update
            last_data_time = max([df.index[-1] for df in etf_rsi_data.values()]).time()
            if last_data_time > last_update_time.time():
                st.write("Using recently updated local data from this hour.")
                return etf_rsi_data

    # If it's a weekday and within market hours, download the latest data
    st.write("Downloading new data from Yahoo Finance...")
    etf_rsi_data = download_etf_data(etf_codes, start_date=start_date, interval='60m')  # Fetch hourly data
    save_data_locally(etf_rsi_data, filename)
    
    return etf_rsi_data

st.title("ETF Latest RSI Dashboard")
st.write("This dashboard displays the latest RSI value for each ETF.")

etf_rsi_data = get_latest_rsi_data(etf_codes)

# Prepare DataFrame directly from the dictionary
rsi_df = pd.DataFrame({
    "ETF": [etf.split('.')[0] for etf in etf_rsi_data.keys()],
    "RSI": [df['RSI'].dropna().iloc[-1] for df in etf_rsi_data.values()]
}).sort_values(by='RSI')

def highlight_rsi(val):
    return f'color: {"red" if val < 40 else "black"}'

styled_df = rsi_df.style.map(highlight_rsi, subset=['RSI'])
st.table(styled_df)
