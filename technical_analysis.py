from config import *
from binance_api import *


class TAnalysis:
    def __init__(self, bnc) -> None:
        print("$$$$$ Starting TA Indicators $$$$$")
        print("$ Calculating RSI...")
        self.rsi = dict()
        for alias in bnc.klines:
            self.rsi[alias] = dict()
            for interval in WORKING_TIMEFRAMES:
                self.rsi[alias][interval] = self.update_rsi(
                    bnc.klines[alias][interval]['Close'], 14)

    def update_rsi(self, prices, period):
        # Retorna um Pandas Series (dataframe de 1 coluna)
        rsi = talib.RSI(prices, timeperiod=period)
        return np.around(rsi, decimals=4)


bnComm = BinanceAPI()
ta = TAnalysis(bnComm)
