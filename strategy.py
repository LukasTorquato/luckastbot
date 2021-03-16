from config import *
import backtrader as bt


class RSIStrategy(bt.Strategy):

    def __init__(self):
        super().__init__()
        self.rsi = bt.talib.RSI(self.data, period=14)

    def next(self):
        if self.rsi < 25 and not self.position:
            self.buy(size=41000)
        if self.rsi > 92 and self.position:
            self.close()
