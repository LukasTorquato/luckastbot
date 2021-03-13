from config import *
from binance_api import *


class TAnalysis:
    def __init__(self, bna) -> None:
        print("$$$$$ Starting TA Indicators $$$$$")
        print("$ Calculating RSI...")
        self.rsi = dict()
        for alias in bna.klines:
            self.rsi[alias] = dict()
            for interval in WORKING_TIMEFRAMES:
                self.rsi[alias][interval] = self.update_rsi(
                    bna.klines[alias][interval]['Close'], 14)

    def update_rsi(self, prices, period):
        # Retorna um Pandas Series (dataframe de 1 coluna)
        rsi = talib.RSI(prices, timeperiod=period)
        return np.around(rsi, decimals=4)

    def make_sell_order(pair, amount, price):
        pass

    def cancel_order(orderId, amount, price):
        pass

    def get_info():
        pass


bnComm = BinanceAPI()
ta = TAnalysis(bnComm)


#data = np.genfromtxt('datasets/BTCUSDT-1D.csv', delimiter=',')

#rsi = ta_rsi(data[:, 1], data[:, 2], data[:, 3], data[:, 4])

# print(rsi)
