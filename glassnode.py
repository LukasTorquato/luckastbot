# import ta-lib
# import tradingview-ta
from config import *
import json
import requests
import pandas as pd

# make API request
res = requests.get(INACTIVE_SUPPLY,
                   params={'a': 'BTC', 'api_key': GN_API_KEY})

# convert to pandas dataframe
df = pd.read_json(res.text)  # , convert_dates=['t'])
df.to_csv('datasets/BTC-inactiveSupply-1D.csv')
