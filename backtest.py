from binance_api import BinanceAPI
from config import *
from binance_api import *
import backtrader as bt


cerebro = bt.Cerebro()

bnc = BinanceAPI()
pdata = bnc.klines[WORKING_ASSETS[0]+WORKING_STABLE[0]
                   ][WORKING_TIMEFRAMES[5]].iloc[:, 0:6]  # BTCUSDT 1D
print(pdata)
pdata["Open Time"] = pd.to_datetime(
    pdata["Open Time"], unit='ms')

pdata = pdata.set_index('Open Time')
print(pdata.dtypes)
data = bt.feeds.PandasData(dataname=pdata)
cerebro.adddata(data)

# cerebro.run()
# cerebro.plot()
