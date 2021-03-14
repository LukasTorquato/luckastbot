from config import *
from binance_api import *


class TAnalysis:
    def __init__(self, bnc) -> None:
        print("$$$$$ Starting TA oscillators $$$$$")
        print("$ Calculating oscillators...")
        self.oscillators = dict()
        for alias in bnc.klines:
            self.oscillators[alias] = dict()
            for interval in WORKING_TIMEFRAMES:
                pricesdf = bnc.klines[alias][interval]
                self.oscillators[alias][interval] = dict()
                self.oscillators[alias][interval]['RSI'] = self.update_rsi(
                    pricesdf['Close'])
                self.oscillators[alias][interval]['STOCH'] = self.update_stoch(
                    pricesdf['High'], pricesdf['Low'], pricesdf['Close'])
                self.oscillators[alias][interval]['CCI'] = self.update_cci(
                    pricesdf['High'], pricesdf['Low'], pricesdf['Close'])
                self.oscillators[alias][interval]['CCI'] = self.update_adx(
                    pricesdf['High'], pricesdf['Low'], pricesdf['Close'])

    def update_rsi(self, prices):
        # Retorna um Pandas Series (dataframe de 1 coluna)
        rsi = talib.RSI(prices, timeperiod=14)
        return np.around(rsi, decimals=4)

    def update_stoch(self, high, low, close):
        # Retorna uma matrix Nx2
        stoch = talib.STOCH(high, low, close, fastk_period=14, slowk_period=3,
                            slowk_matype=0, slowd_period=3, slowd_matype=0)
        return np.around(stoch, decimals=4)

    def update_cci(self, high, low, close):
        # Retorna uma matrix Nx2
        cci = talib.CCI(high, low, close, timeperiod=20)
        return np.around(cci, decimals=4)

    def update_cci(self, high, low, close):
        # Retorna uma matrix Nx2
        adx = talib.ADX(high, low, close, timeperiod=20)
        return np.around(adx, decimals=4)


bnComm = BinanceAPI()
ta = TAnalysis(bnComm)
print(ta.oscillators['BTCUSDT'][KLINE_INTERVAL_1DAY]['CCI'])
