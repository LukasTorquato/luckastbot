import time
import csv
import websocket
from config import *
from binance.client import Client

# Conecta API
client = Client(API_KEY, API_SECRET)

# prices = client.get_all_tickers()  # Pega todos os preços de todos os pares

csvfile = open('candles.csv', 'w', newline='')

fieldnames = ['Time Init', 'Open', 'High', 'Low',
              'Close', 'Volume', 'Time Close', 'QAV', 'N Trades']

writer = csv.writer(csvfile, delimiter=',')
writer.writerow(fieldnames)

klines = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2012", "1 Jan, 2021")  # pega o candle do intervalo de tempo

candles = client.get_klines(
    symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1DAY)  # pega os últimos 500 candles da constante definida


for kline in klines:
    writer.writerow(kline)

csvfile.close()
