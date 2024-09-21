import os
import pandas as pd

def save_data_locally(etf_rsi_data, filename='etf_data.pkl'):
    pd.to_pickle(etf_rsi_data, filename)

def load_local_data(filename='etf_data.pkl'):
    return pd.read_pickle(filename) if os.path.exists(filename) else None
