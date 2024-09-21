import streamlit as st
import pandas as pd
from modules.rsi_processor import get_latest_rsi_data

etf_codes = [
    'CPSEETF.NS', 'GOLDBEES.NS', 'NIF100IETF.NS', 'LOWVOLIETF.NS', 'ALPHAETF.NS', 
    'HDFCMOMENT.NS', 'QUAL30IETF.NS', 'NIFTYBEES.NS', 'EQUAL50ADD.NS', 'NV20IETF.NS', 
    'MONIFTY500.NS', 'ALPHA.NS', 'ALPL30IETF.NS', 'AUTOIETF.NS', 'BANKETFADD.NS', 
    'COMMOIETF.NS', 'DIVOPPBEES.NS', 'BFSI.NS', 'FINIETF.NS', 'FMCGIETF.NS', 
    'HEALTHY.NS', 'CONSUMBEES.NS', 'TNIDETF.NS', 'MAKEINDIA.NS', 'INFRABEES.NS',
    'ITBEES.NS', 'MOM100.NS', 'MIDCAPETF.NS', 'MIDSMALL.NS', 'MNC.NS',
    'JUNIORBEES.NS', 'PHARMABEES.NS', 'PVTBANIETF.NS', 'PSUBNKBEES.NS',
    'MOREALTY.NS', 'HDFCSML250.NS', 'SMALLCAP.NS', 'BSE500IETF.NS',
    'ICICIB22.NS', 'MOVALUE.NS', 'MOHEALTH.NS', 'MIDSELIETF.NS',
    'HDFCSENSEX.NS', 'SILVERBEES.NS', 'MONQ50.NS', 'ESG.NS'
]

st.title("ETF Latest RSI Dashboard")
st.write("This dashboard displays the latest RSI value for each ETF.")

etf_rsi_data, etf_daily_rsi_ma_data = get_latest_rsi_data(etf_codes)

# Prepare DataFrame for hourly RSI
rsi_df_hourly = pd.DataFrame({
    "ETF": [etf.split('.')[0] for etf in etf_rsi_data.keys()],
    "Hourly RSI": [df['RSI'].dropna().iloc[-1] for df in etf_rsi_data.values()]
})

# Prepare DataFrame for daily RSI, Moving Averages, and Current Price with % drop
rsi_ma_df_daily = pd.DataFrame({
    "ETF": [etf.split('.')[0] for etf in etf_daily_rsi_ma_data.keys()],
    "Current Price": [df['Close'].dropna().iloc[-1] if not df['Close'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
    "Daily RSI": [df['RSI'].dropna().iloc[-1] if not df['RSI'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
    "20DMA": [df['20DMA'].dropna().iloc[-1] if not df['20DMA'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
    "50DMA": [df['50DMA'].dropna().iloc[-1] if not df['50DMA'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
    "100DMA": [df['100DMA'].dropna().iloc[-1] if not df['100DMA'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
    "200DMA": [df['200DMA'].dropna().iloc[-1] if not df['200DMA'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
})

# Calculate percentage drop from 20, 50, 100, 200 DMAs
rsi_ma_df_daily['% from 20DMA'] = ((rsi_ma_df_daily['Current Price'] - rsi_ma_df_daily['20DMA']) / rsi_ma_df_daily['20DMA']) * 100
rsi_ma_df_daily['% from 50DMA'] = ((rsi_ma_df_daily['Current Price'] - rsi_ma_df_daily['50DMA']) / rsi_ma_df_daily['50DMA']) * 100
rsi_ma_df_daily['% from 100DMA'] = ((rsi_ma_df_daily['Current Price'] - rsi_ma_df_daily['100DMA']) / rsi_ma_df_daily['100DMA']) * 100
rsi_ma_df_daily['% from 200DMA'] = ((rsi_ma_df_daily['Current Price'] - rsi_ma_df_daily['200DMA']) / rsi_ma_df_daily['200DMA']) * 100

# Sort by highest drop from 200DMA (or any DMA)
sorted_rsi_ma_df = rsi_ma_df_daily.sort_values(by=['% from 200DMA','% from 100DMA', '% from 50DMA', '% from 20DMA'])

# Display the DataFrame with the sorted values in Streamlit
st.write("ETF Daily RSI, Moving Averages, Current Price, and % Drop from DMAs (sorted by highest drop from 200DMA)")
st.dataframe(sorted_rsi_ma_df.style.format({
    "Current Price": "{:.2f}", 
    "Daily RSI": "{:.2f}", 
    "20DMA": "{:.2f}", 
    "50DMA": "{:.2f}", 
    "100DMA": "{:.2f}", 
    "200DMA": "{:.2f}", 
    "% from 20DMA": "{:.2f}%", 
    "% from 50DMA": "{:.2f}%", 
    "% from 100DMA": "{:.2f}%", 
    "% from 200DMA": "{:.2f}%"
}))
