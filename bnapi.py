from binance.client import Client
from binance.enums import *
from requests import NullHandler
from config import *
from tanalysis import *
import numpy as np
import websocket


class BinanceAPI:
    def __init__(self):
        # Conecta a API
        self.client = Client(BN_API_KEY, BN_API_SECRET)
        self.info = self.client.get_account()
        # Dataframe de Balances da conta
        self.balances = pd.DataFrame()
        for alias in np.concatenate([WORKING_ASSETS, WORKING_STABLE]):
            assetinfo = self.client.get_asset_balance(asset=alias)
            self.balances = self.balances.append(
                assetinfo, ignore_index=True)
        # Pega as ordens abertas
        self.update_open_orders()

    def make_buy_order(self, pair, amount, price):
        self.client.create_order(symbol=pair,
                                 side=SIDE_BUY, type=ORDER_TYPE_LIMIT,
                                 timeInForce=TIME_IN_FORCE_GTC, quantity=amount, price=price)
        self.update_open_orders()

    def make_sell_order(self, pair, amount, price):
        self.client.create_order(symbol=pair,
                                 side=SIDE_SELL, type=ORDER_TYPE_LIMIT,
                                 timeInForce=TIME_IN_FORCE_GTC, quantity=amount, price=price)
        self.update_open_orders()

    def update_open_orders(self):
        try:
            self.openOrders = pd.DataFrame(
                self.client.get_open_orders()).set_index('orderId')
        except:
            self.openOrders = pd.DataFrame()

    def cancel_order(self, pair, id):
        try:
            self.client.cancel_order(symbol=pair, orderId=id)
            self.update_open_orders()
        except:
            print('Order not found.')

    def cancel_all_pair_orders(self, pair):
        try:
            orderids = self.openOrders[self.openOrders['symbol']
                                       == pair].index.tolist()
            for order in orderids:
                self.client.cancel_order(symbol=pair, orderId=order)
            self.update_open_orders()
        except:
            print('Pair not found.')

    def cancel_all_orders(self):
        try:
            if not self.openOrders.empty:
                pairs = self.openOrders['symbol'].tolist()
                for pair in pairs:
                    self.cancel_all_pair_orders(pair)
                self.update_open_orders()
        except:
            print('No orders found.')

    def get_info():
        pass


bnComm = BinanceAPI()
print(bnComm.openOrders)
bnComm.cancel_all_orders()

# print(orderids)

print(bnComm.openOrders)

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
'''
