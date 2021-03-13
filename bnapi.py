from binance.client import Client
from binance.enums import *
from binance.exceptions import *
from requests import NullHandler
from config import *
from tanalysis import *
import numpy as np
import websocket


class BinanceAPI:

    def __init__(self):
        # Conecta a API
        self.client = Client(BN_API_KEY, BN_API_SECRET)
        # Verifica se servidor está normal ou sob manutenção
        self.server_status = self.client.get_system_status()
        if(self.server_status['status'] == 0):
            self.info = self.client.get_account()
            # Dataframe de Balances da conta
            self.balances = pd.DataFrame()
            for alias in np.concatenate([WORKING_ASSETS, WORKING_STABLE]):
                assetinfo = self.client.get_asset_balance(asset=alias)
                self.balances = self.balances.append(
                    assetinfo, ignore_index=True)
            # Pega as ordens abertas
            self.update_open_orders()
            self.depth_order = dict()
        else:
            print("Servidor em manutenção.")

    def make_buy_order(self, pair, amount, price):
        try:
            self.client.create_order(symbol=pair,
                                     side=SIDE_BUY, type=ORDER_TYPE_LIMIT,
                                     timeInForce=TIME_IN_FORCE_GTC, quantity=amount, price=price)
            self.update_open_orders()
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No buy order created: Invalid character.")
            elif (e.code == -2010):
                print("No buy order created: Insufficient Balance.")
            elif (e.code == -1121):
                print("No buy order created: Invalid Symbol.")
            else:
                print(e.code, e.message)

    def make_sell_order(self, pair, amount, price):
        try:
            self.client.create_order(symbol=pair,
                                     side=SIDE_SELL, type=ORDER_TYPE_LIMIT,
                                     timeInForce=TIME_IN_FORCE_GTC, quantity=amount, price=price)
            self.update_open_orders()
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No sell order created: Invalid character.")
            elif (e.code == -2010):  # Funcdos insuficientes
                print("No sell order created: Insufficient Balance.")
            elif (e.code == -1121):
                print("No sell order created: Invalid Symbol.")
            else:
                print(e.code, e.message)

    def update_open_orders(self):
        try:
            self.openOrders = pd.DataFrame(
                self.client.get_open_orders()).set_index('orderId')
        except KeyError as e:
            print("No orders found.")
            self.openOrders = pd.DataFrame()

    def cancel_order(self, pair, id):
        try:
            self.client.cancel_order(symbol=pair, orderId=id)
            self.update_open_orders()
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No order canceled: Invalid character.")
            if (e.code == -2011):
                print("No order canceled: Order not found.")
            elif (e.code == -1121):
                print("No order canceled: Invalid Symbol.")
            else:
                print(e.code, e.message)

    def cancel_all_pair_orders(self, pair):
        try:
            orderids = self.openOrders[self.openOrders['symbol']
                                       == pair].index.tolist()
            for order in orderids:
                self.client.cancel_order(symbol=pair, orderId=order)
            self.update_open_orders()
        except KeyError as e:
            print("No order canceled - This pair doesn`t have any orders.")

    def cancel_all_orders(self):
        if not self.openOrders.empty:
            pairs = self.openOrders['symbol'].tolist()
            for pair in pairs:
                self.cancel_all_pair_orders(pair)
            self.update_open_orders()

    def get_order_book(self, pair):
        try:
            depth = self.client.get_order_book(symbol=pair)
            self.depth_order[pair] = dict()
            self.depth_order[pair]['bids'] = pd.DataFrame(
                depth['bids'], columns=['value', 'qtd'])
            self.depth_order[pair]['asks'] = pd.DataFrame(
                depth['asks'], columns=['value', 'qtd'])
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No order book: Invalid character.")
            elif (e.code == -1121):
                print("No order book found: Invalid Symbol.")
            else:
                print(e.code, e.message)

    def get_prices(self, pair):
        return self.client.get_ticker()

    def get_info():
        pass


bnComm = BinanceAPI()
# bnComm.make_buy_order('CAKEBUSD', 1.2, 10.0)
bnComm.get_order_book("ZZZZZZ")
print(bnComm.depth_order)
# print(orderids)

# print(bnComm.openOrders)

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
