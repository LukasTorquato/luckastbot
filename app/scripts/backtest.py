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
    dataname='datasets/ADAUSDT-1D.csv',
    dtformat=1,
    compression=1,  # QTD de Minutos - Horas - Dias
    timeframe=bt.TimeFrame.Days)  # Minutes - Hours - Days

cerebro.adddata(data)

cerebro.run()

cerebro.plot()
