# import ta-lib
# import tradingview-ta
from config import *
import json
import requests
import pandas as pd

# make API request
res = requests.get(ACTIVE_ADDRESS,
                   params={'a': 'ETH', 'api_key': GN_API_KEY})

# convert to pandas dataframe
df = pd.read_json(res.text)  # , convert_dates=['t'])
df.to_csv('datasets/ETH-ActiveAddress-1D.csv')
