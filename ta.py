import talib
import csv
import numpy as np
import pandas as pd


def ta_rsi(close, period):
    #rsi = np.array()
    rsi = talib.RSI(close, timeperiod=period)
    return np.around(rsi, decimals=6)


#data = np.genfromtxt('datasets/BTCUSDT-1D.csv', delimiter=',')

#rsi = ta_rsi(data[:, 1], data[:, 2], data[:, 3], data[:, 4])

# print(rsi)
