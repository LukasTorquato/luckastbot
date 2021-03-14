from binance_api import BinanceAPI
from config import *
from binance_api import *
import backtrader as bt


class PandasData(bt.feed.DataBase):
    '''
    The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    '''

    params = (
        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', "Open Time"),

        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', "Open"),
        ('high', "High"),
        ('low', "Low"),
        ('close', "Close"),
        ('volume', "Outer Volume"),
    )


cerebro = bt.Cerebro()

bnc = BinanceAPI()
pdata = bnc.klines[WORKING_ASSETS[0]+WORKING_STABLE[0]
                   ][WORKING_TIMEFRAMES[0]]  # BTCUSDT 1D
#pdata["Open Time"] = pd.to_datetime(pdata["Open Time"], unit='ms')
#pdata = pdata.set_index('Open Time')
print(pdata)

data = PandasData(dataname=pdata)
cerebro.adddata(data)

cerebro.run()
cerebro.plot()
