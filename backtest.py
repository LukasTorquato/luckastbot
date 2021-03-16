from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from config import *
from binance_api import *
from strategy import *
import backtrader as bt


cerebro = bt.Cerebro()
# Add a strategy
cerebro.addstrategy(RSIStrategy)
data = bt.feeds.GenericCSVData(
    dataname='datasets/ADAUSDT-15MIN.csv',
    dtformat=1,
    compression=15,
    timeframe=bt.TimeFrame.Minutes)

cerebro.adddata(data)
cerebro.run()
cerebro.plot()
