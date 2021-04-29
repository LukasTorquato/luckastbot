from binance.client import Client
from binance.enums import *
from binance.exceptions import *
import matplotlib
import numpy as np
import pandas as pd

# Binance
WEB_SOCKET = "wss://stream.binance.com:9443/ws/"  # btcusdt@kline_5m
BN_API_KEY = "8iX7ylrqiBjFqte6IjVdLdfCAHmFjN73QaVeSeo0vaOWy9TABRb18jfkflrIxLyF"
BN_API_SECRET = "qiM2Y32WVmKCQurCwmDcS5Oj1vd0XMHmoxUAUFAfKv9pDto3uercSA6HCAKnUcDl"

# Glassnode
GN_API_KEY = "f8fe19a3-fdef-4825-88ca-80c8dd58f77f"
SENDING_ADDRESS = "https://api.glassnode.com/v1/metrics/addresses/sending_count"
ACTIVE_ADDRESS = "https://api.glassnode.com/v1/metrics/addresses/active_count"
INACTIVE_SUPPLY = "https://api.glassnode.com/v1/metrics/supply/active_more_1y_percent"

# Settings
MARKET_TREND = 1  # 1 - BULL Market / 0 - BEAR Market
AGGRESSIVENESS = 0
WORKING_ASSETS = ['BTC']  # , 'ADA', 'ETH', 'BNB']
WORKING_STABLE = ['USDT']  # , 'BUSD', 'BRL']
WORKING_TIMEFRAMES = [KLINE_INTERVAL_1DAY]

# User Settings
INITIAL_CAPITAL = 10000

# Technical Indicators
TREND_INDICATORS = {"SMA": 1, "EMA": 1,
                    "ADX": 1, "PSAR": 1,
                    "MACD": 1, "ICMK": 1,
                    "CCI": 1}
MOMENTUM_INDICATORS = {"RSI": 1, "STOCH": 1,
                       "AO": 1, "SRSI": 0,
                       "WR": 1, "UO": 1}
VOLATILITY_INDICATORS = {"BOLB": 1}
VOLUME_INDICATORS = {"OBV": 1}
