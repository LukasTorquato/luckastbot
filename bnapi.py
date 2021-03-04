# import ta-lib
# import tradingview-ta
import csv
import websocket
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
csvfile = open('datasets/ETHUSDT.csv', 'w', newline='')

fieldnames = ['Time Init', 'Open', 'High', 'Low',
              'Close', 'Volume', 'Time Close', 'QAV', 'N Trades']
writer = csv.writer(csvfile, delimiter=',')
writer.writerow(fieldnames)

klines = client.get_historical_klines(
    "ETHUSDT", Client.KLINE_INTERVAL_4HOUR, "1 Jan, 2012", "23 Feb, 2021")  # pega o candle do intervalo de tempo

for kline in klines:
    writer.writerow(kline[0:9])

csvfile.close()
