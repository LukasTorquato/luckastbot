import talib
import csv
import numpy as np


def ta_rsi(open, high, low, close):
    #rsi = np.array()
    rsi = talib.RSI(close, timeperiod=14)
    return rsi


data = np.genfromtxt('datasets/BTCUSDT-15MIN.csv', delimiter=',')

rsi = ta_rsi(data[:, 1], data[:, 2], data[:, 3], data[:, 4])

print(rsi)
