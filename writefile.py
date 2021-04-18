from binance_api import *

bncom = BinanceAPI()

hist = bncom.get_historical_klines('BTCUSDT', KLINE_INTERVAL_1HOUR, 3600, True)
hist.drop('Close Time', inplace=True, axis=1)
hist.drop('Inner Volume', inplace=True, axis=1)
hist.rename(columns={"Outer Volume": "Volume"}, inplace=True)
hist['Open Time'] = pd.to_datetime(
    hist['Open Time']/1000, unit='s')
hist.to_csv('datasets/BTCUSDT-1H.csv', index=False)
print(hist)
