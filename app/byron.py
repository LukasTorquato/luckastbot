import threading
from config import *
from binance_api import *

'''
STRATEGY PLAN
- 1st Thread: 
    - Consome preços atuais do BTC
- 2nd Thread:
    - Realiza Operações de Compra/Venda
- 3rd Thread:
    - Verifica o modelo se vale ou não a

'''


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


def main():

    symbol = 'BTCUSDT'

    twm = ThreadedWebsocketManager(
        api_key=BN_API_KEY, api_secret=BN_API_SECRET)
    # start is required to initialise its internal loop
    twm.start()

    def handle_socket_message(msg):
        print(f"message type: {msg['e']}")
        print(msg)

    twm.start_kline_socket(callback=handle_socket_message, symbol=symbol)

    # or a multiplex socket can be started like this
    # see Binance docs for stream names
    streams = ['btcusdt@miniTicker', 'btcusdt@bookTicker']
    # twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)

    twm.join()


if __name__ == "__main__":
    main()

# byron = ByronBot()
# byron.run()
