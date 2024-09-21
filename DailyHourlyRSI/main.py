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

# Prepare DataFrame for daily RSI and Moving Averages
# Prepare DataFrame for daily RSI and Moving Averages
rsi_ma_df_daily = pd.DataFrame({
    "ETF": [etf.split('.')[0] for etf in etf_daily_rsi_ma_data.keys()],
    "Daily RSI": [df['RSI'].dropna().iloc[-1] if not df['RSI'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
    "20DMA": [df['20DMA'].dropna().iloc[-1] if not df['20DMA'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
    "50DMA": [df['50DMA'].dropna().iloc[-1] if not df['50DMA'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
    "100DMA": [df['100DMA'].dropna().iloc[-1] if not df['100DMA'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()],
    "200DMA": [df['200DMA'].dropna().iloc[-1] if not df['200DMA'].dropna().empty else None for df in etf_daily_rsi_ma_data.values()]
})

# Merge both DataFrames to display both Hourly and Daily RSI + Moving Averages
combined_rsi_df = pd.merge(rsi_df_hourly, rsi_ma_df_daily, on='ETF')
combined_rsi_df = combined_rsi_df.sort_values(by=["200DMA", "100DMA", "50DMA", "20DMA", "Daily RSI"])
# Highlight cells where RSI < 40 or specific moving averages are of interest
def highlight_rsi_ma(val):
    if val < 40:  # Highlight RSI if less than 40
        return 'color: red'
    elif isinstance(val, float):  # Highlight Moving Averages (for visual purposes)
        return 'color: blue'
    return ''

styled_df = combined_rsi_df.style.map(highlight_rsi_ma, subset=['Hourly RSI', 'Daily RSI', '20DMA', '50DMA', '100DMA', '200DMA'])
st.table(styled_df)

