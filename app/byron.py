import threading

from pandas.core.frame import DataFrame
from config import *
from binance_api import *
from indicators import AddIndicators

'''
STRATEGY PLAN
- 1st Thread:
    - Consome preços atuais do BTC
- 2nd Thread:
    - Realiza Operações de Compra/Venda
- 3rd Thread:
    - Verifica o modelo se vale ou não a

'''

window = pd.DataFrame()


class ByronBot:

    def __init__(self):
        self.bn_connection = BinanceAPI()

        pass

    def run():
        # implementar thread
        c = True
        while(c):
            keyPress = input()
            if keyPress == 'b':
                c = False
        return

    def info():
        pass


def isFloat(x):
    try:
        float(x)
        return True
    except:
        return False


def update_queue(msg):
    # print(f"message type: {msg['e']}")
    global window
    update = {key: float(value) for key, value
              in msg['k'].items()
              if isFloat(value)}
    # update = [dict([a, float(x)] for a, x in msg['k'].items())]

    if (window.iloc[-1, window.columns.get_loc('Date')] == msg['k']['t']):
        window.iloc[-1, window.columns.get_loc('Open')] = update['o']
        window.iloc[-1, window.columns.get_loc('High')] = update['h']
        window.iloc[-1, window.columns.get_loc('Low')] = update['l']
        window.iloc[-1, window.columns.get_loc('Close')] = update['c']
        window.iloc[-1, window.columns.get_loc('Volume')] = update['q']
        window.iloc[-1, window.columns.get_loc('N. Trades')] = update['n']
    else:
        window = window.append({'Date': update['t'], 'Open': update['o'], 'High': update['h'], 'Low': update['l'],
                                'Close': update['c'], 'Volume': update['q'], 'N. Trades': update['n']}, ignore_index=True)
        window.drop(index=window.index[0], inplace=True)

    window = AddIndicators(window, runtime=True)
    print(window)


def main():
    global window
    symbol = 'BTCUSDT'
    interval = KLINE_INTERVAL_1MINUTE
    bncom = BinanceAPI()
    window = bncom.update_recent_klines(symbol, interval, True)
    window[["Open", "High", "Low", "Close", "Volume", "N. Trades"]] = window[[
        "Open", "High", "Low", "Close", "Volume", "N. Trades"]].apply(pd.to_numeric)
    # window['Date'] = pd.to_datetime(window['Date']/1000, unit='s')
    window = AddIndicators(window, runtime=True)

    print(window)
    twm = ThreadedWebsocketManager(
        api_key=BN_API_KEY, api_secret=BN_API_SECRET)
    # start is required to initialise its internal loop
    twm.start()
    twm.start_kline_socket(callback=update_queue,
                           symbol=symbol, interval=interval)

    # twm.join()


if __name__ == "__main__":
    main()

# byron = ByronBot()
# byron.run()
