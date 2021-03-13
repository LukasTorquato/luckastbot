from binance.client import Client
from binance.enums import *
from binance.exceptions import *
from tanalysis import *
import numpy as np

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
WORKING_ASSETS = ['BTC', 'ADA', 'ETH', 'BNB']
WORKING_STABLE = ['USDT', 'BUSD', 'BRL']
WORKING_TIMEFRAMES = [KLINE_INTERVAL_1MINUTE, KLINE_INTERVAL_5MINUTE,
                      KLINE_INTERVAL_15MINUTE, KLINE_INTERVAL_1HOUR, KLINE_INTERVAL_4HOUR, KLINE_INTERVAL_1DAY]
