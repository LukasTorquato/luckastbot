import csv
import websocket
import numpy as np
from ta import *
from config import *
from binance.client import Client
from binance.enums import *
from tradingview_ta import TA_Handler, Interval, Exchange


# Conecta API
client = Client(BN_API_KEY, BN_API_SECRET)
'''
# prices = client.get_all_tickers()  # Pega todos os preços de todos os pares

orders = client.get_all_orders(symbol='ADABUSD')
# cancelorder = client.cancel_order(
#     symbol='ADABUSD', orderId=orders[0]['orderId'])

for order in orders:
    print(order)

'''
csvfile = open('datasets/BTCUSDT-1D-RSI.csv', 'w', newline='')

fieldnames = ['Time Init', 'Open', 'High', 'Low',
              'Close', 'Volume', 'Time Close', 'QAV', 'N Trades', 'RSI']
writer = csv.writer(csvfile, delimiter=',')
writer.writerow(fieldnames)

klines = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2012", "5 Mar, 2021")  # pega o candle do intervalo de tempo


klines = np.asarray(klines, dtype=np.float64)

rsi = np.asarray(ta_rsi(klines[:, 4]), dtype=np.float64)

klines = np.column_stack((klines[:, 0:9], rsi))

for kline in klines:
    writer.writerow(kline[0:10])

csvfile.close()
