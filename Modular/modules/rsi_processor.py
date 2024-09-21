from datetime import datetime, timedelta, date
from modules.utils import is_market_open
from modules.file_manager import load_local_data, save_data_locally
from modules.data_downloader import download_etf_data
import streamlit as st

def get_latest_rsi_data(etf_codes, days_difference=729, filename='etf_data.pkl'):
    # Load data from the local file
    etf_rsi_data = load_local_data(filename)
    
    today = date.today()
    start_date = today - timedelta(days=days_difference)
    
    # If the file doesn't exist or data is empty, download fresh data
    if not etf_rsi_data:
        st.write("No local data found. Downloading fresh data...")
        etf_rsi_data = download_etf_data(etf_codes, start_date=start_date, interval='60m')
        save_data_locally(etf_rsi_data, filename)
        return etf_rsi_data

    # If today is a weekend, use local data
    if today.weekday() >= 5:
        st.write("Today is a weekend. Using local data.")
        return etf_rsi_data
    
    # Check if the market is currently open
    current_time = datetime.now().time()
    if not is_market_open(current_time):
        st.write("Market is closed. Using local data.")
        return etf_rsi_data
    
    # Check if the local data is up-to-date (latest date is today)
    latest_dates = {etf: df.index[-1].date() for etf, df in etf_rsi_data.items()}
    if all(latest_date == today for latest_date in latest_dates.values()):
        last_update_time = datetime.now() - timedelta(hours=1)
        last_data_time = max([df.index[-1] for df in etf_rsi_data.values()]).time()
        
        # Use the local data if it was updated within the last hour
        if last_data_time > last_update_time.time():
            st.write("Using recently updated local data from this hour.")
            return etf_rsi_data

    # Download fresh data if the local data is outdated
    st.write("Downloading new data from Yahoo Finance...")
    etf_rsi_data = download_etf_data(etf_codes, start_date=start_date, interval='60m')
    save_data_locally(etf_rsi_data, filename)
    
    return etf_rsi_data
