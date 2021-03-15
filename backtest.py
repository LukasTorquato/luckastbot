from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from config import *
from binance_api import *
import backtrader as bt


class RSIStrategy(bt.Strategy):

    def __init__(self):
        super().__init__()
        self.rsi = bt.talib.RSI(self.data, period=14)

    def next(self):
        if self.rsi < 25 and not self.position:
            self.buy(size=41000)
        if self.rsi > 90 and self.position:
            self.close()


cerebro = bt.Cerebro()
# Add a strategy
cerebro.addstrategy(RSIStrategy)
data = bt.feeds.GenericCSVData(dataname='datasets/ADAUSDT-1D.csv', dtformat=1)
cerebro.adddata(data)
cerebro.run()
cerebro.plot()
