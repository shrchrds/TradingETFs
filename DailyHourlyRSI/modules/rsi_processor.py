from datetime import datetime, timedelta, date
from modules.utils import is_market_open
from modules.file_manager import load_local_data, save_data_locally
from modules.data_downloader import download_etf_data, download_etf_daily_data
import streamlit as st

def get_latest_rsi_data(etf_codes, days_difference=729, filename='etf_data.pkl', daily_filename='etf_daily_data.pkl'):
    # Load hourly data from the local file
    etf_rsi_data = load_local_data(filename)
    
    # Load daily data from the local file
    etf_daily_rsi_data = load_local_data(daily_filename)
    
    today = date.today()
    start_date = today - timedelta(days=days_difference)
    
    # If the file doesn't exist or data is empty, download fresh hourly and daily data
    if not etf_rsi_data:
        st.write("No local hourly data found. Downloading fresh hourly data...")
        etf_rsi_data = download_etf_data(etf_codes, start_date=start_date, interval='60m')
        save_data_locally(etf_rsi_data, filename)
    
    if not etf_daily_rsi_data:
        st.write("No local daily data found. Downloading fresh daily data...")
        etf_daily_rsi_data = download_etf_daily_data(etf_codes, start_date=start_date)
        save_data_locally(etf_daily_rsi_data, daily_filename)
    
    # If today is a weekend, use local data
    if today.weekday() >= 5:
        st.write("Today is a weekend. Using local data.")
        return etf_rsi_data, etf_daily_rsi_data
    
    # Check if the market is currently open
    current_time = datetime.now().time()
    if not is_market_open(current_time):
        st.write("Market is closed. Using local data.")
        return etf_rsi_data, etf_daily_rsi_data
    
    # Check if the local hourly data is up-to-date (latest date is today)
    latest_dates = {etf: df.index[-1].date() for etf, df in etf_rsi_data.items()}
    if all(latest_date == today for latest_date in latest_dates.values()):
        last_update_time = datetime.now() - timedelta(hours=1)
        last_data_time = max([df.index[-1] for df in etf_rsi_data.values()]).time()
        
        if last_data_time > last_update_time.time():
            st.write("Using recently updated hourly local data from this hour.")
            return etf_rsi_data, etf_daily_rsi_data
    
    # If the hourly data is outdated, download fresh data
    st.write("Downloading new hourly data from Yahoo Finance...")
    etf_rsi_data = download_etf_data(etf_codes, start_date=start_date, interval='60m')
    save_data_locally(etf_rsi_data, filename)
    
    # Download fresh daily data if needed
    st.write("Downloading new daily data from Yahoo Finance...")
    etf_daily_rsi_data = download_etf_daily_data(etf_codes, start_date=start_date)
    save_data_locally(etf_daily_rsi_data, daily_filename)
    
    return etf_rsi_data, etf_daily_rsi_data

