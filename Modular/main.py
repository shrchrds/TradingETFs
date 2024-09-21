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

etf_rsi_data = get_latest_rsi_data(etf_codes)

# Prepare DataFrame directly from the dictionary
rsi_df = pd.DataFrame({
    "ETF": [etf.split('.')[0] for etf in etf_rsi_data.keys()],
    "RSI": [int(df['RSI'].dropna().iloc[-1]) for df in etf_rsi_data.values()]
}).sort_values(by='RSI')

def highlight_rsi(val):
    return f'color: {"red" if val < 40 else "black"}'

styled_df = rsi_df.style.map(highlight_rsi, subset=['RSI'])
st.table(styled_df)
