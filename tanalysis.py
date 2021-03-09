import talib
import csv
import numpy as np
import pandas as pd


class TAnalysis:
    def __init__(self) -> None:
        self.indicators = pd.DataFrame

        pass

    def rsi(price, period):
        rsi = talib.RSI(close, timeperiod=period)
        pass

    def make_sell_order(pair, amount, price):
        pass

    def cancel_order(orderId, amount, price):
        pass

    def get_info():
        pass


def ta_rsi(close, period):
    #rsi = np.array()
    rsi = talib.RSI(close, timeperiod=period)
    return np.around(rsi, decimals=6)


#data = np.genfromtxt('datasets/BTCUSDT-1D.csv', delimiter=',')

#rsi = ta_rsi(data[:, 1], data[:, 2], data[:, 3], data[:, 4])

# print(rsi)
