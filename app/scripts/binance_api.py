from config import *


class BinanceAPI:

    def __init__(self):
        # Conecta a API
        print("##### Starting Binance connection #####")
        self.client = Client(BN_API_KEY, BN_API_SECRET)
        # Verifica se servidor está normal ou sob manutenção
        self.server_status = self.client.get_system_status()
        if(self.server_status['status'] == 0):
            print("# Connection succeded.")
            # Dataframe de Balances da conta
            print("# Updating balances...")
            self.update_balance()
            # Dataframe dos Tokens escolhidos
            print("# Updating prices...")
            self.update_prices()
            # Pega as ordens abertas
            print("# Updating open orders...")
            self.update_open_orders()
            # Livro de ordens
            self.depth_order = dict()

            # Klines Storage
            print("# Getting recent Klines...")
            self.klines = dict()
            for alias in WORKING_ASSETS:
                self.klines[alias + "USDT"] = dict()
                for interval in WORKING_TIMEFRAMES:
                    self.klines[alias + "USDT"][interval] = self.update_recent_klines(
                        alias+"USDT", interval)
        else:
            print("# Server in maintenance.")

    def make_buy_order(self, pair, amount, price):
        try:
            self.client.create_order(symbol=pair,
                                     side=SIDE_BUY, type=ORDER_TYPE_LIMIT,
                                     timeInForce=TIME_IN_FORCE_GTC, quantity=amount, price=price)
            self.update_open_orders()
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No buy order created: Invalid character - "+pair)
            elif (e.code == -2010):
                print("No buy order created: Insufficient Balance.")
            elif (e.code == -1121):
                print("No buy order created: Invalid Symbol - "+pair)
            else:
                print(e.code, e.message)

    def make_sell_order(self, pair, amount, price):
        try:
            self.client.create_order(symbol=pair,
                                     side=SIDE_SELL, type=ORDER_TYPE_LIMIT,
                                     timeInForce=TIME_IN_FORCE_GTC, quantity=amount, price=price)
            self.update_open_orders()
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No sell order created: Invalid character - "+pair)
            elif (e.code == -2010):  # Funcdos insuficientes
                print("No sell order created: Insufficient Balance.")
            elif (e.code == -1121):
                print("No sell order created: Invalid Symbol - "+pair)
            else:
                print(e.code, e.message)

    def update_open_orders(self):
        try:
            self.openOrders = pd.DataFrame(
                self.client.get_open_orders()).set_index('orderId')
        except KeyError as e:
            print("No orders found.")
            self.openOrders = pd.DataFrame()

    def update_balance(self):
        self.balances = pd.DataFrame()
        for alias in np.concatenate([WORKING_ASSETS, WORKING_STABLE]):
            assetinfo = self.client.get_asset_balance(asset=alias)
            self.balances = self.balances.append(
                assetinfo, ignore_index=True)

    def update_prices(self):
        self.asset_prices = pd.DataFrame()
        for alias in WORKING_ASSETS:
            assetprice = self.client.get_ticker(symbol=alias+'USDT')
            self.asset_prices = self.asset_prices.append(
                assetprice, ignore_index=True)

    def cancel_order(self, pair, id):
        try:
            self.client.cancel_order(symbol=pair, orderId=id)
            self.update_open_orders()
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No order canceled: Invalid character - "+pair)
            if (e.code == -2011):
                print("No order canceled: Order not found.")
            elif (e.code == -1121):
                print("No order canceled: Invalid Symbol - "+pair)
            else:
                print(e.code, e.message)

    def cancel_all_pair_orders(self, pair):
        try:
            orderids = self.openOrders[self.openOrders['symbol']
                                       == pair].index.tolist()
            for order in orderids:
                self.client.cancel_order(symbol=pair, orderId=order)
            self.update_open_orders()
        except KeyError as e:
            print("No order canceled - This pair (" +
                  pair+") doesn`t have any orders.")

    def cancel_all_orders(self):
        if not self.openOrders.empty:
            pairs = self.openOrders['symbol'].tolist()
            for pair in pairs:
                self.cancel_all_pair_orders(pair)
            self.update_open_orders()

    def get_order_book(self, pair):
        try:
            depth = self.client.get_order_book(symbol=pair)
            self.depth_order[pair] = dict()
            self.depth_order[pair]['bids'] = pd.DataFrame(
                depth['bids'], columns=['value', 'qtd'])
            self.depth_order[pair]['asks'] = pd.DataFrame(
                depth['asks'], columns=['value', 'qtd'])
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No order book: Invalid character - "+pair)
            elif (e.code == -1121):
                print("No order book found: Invalid Symbol - "+pair)
            else:
                print(e.code, e.message)

    def update_recent_klines(self, pair, k_interval, inUnix=False):

        try:
            klines = pd.DataFrame()
            recent = self.client.get_klines(symbol=pair, interval=k_interval)
            klines = klines.append(recent, ignore_index=True)
            klines = klines.rename(columns={0: 'Open Time', 1: 'Open', 2: 'High', 3: 'Low',
                                            4: 'Close', 5: 'Inner Volume', 6: 'Close Time', 7: 'Outer Volume', 8: 'N. Trades'})
            if not inUnix:
                klines['Open Time'] = pd.to_datetime(
                    klines['Open Time'], unit='ms')
                klines['Close Time'] = pd.to_datetime(
                    klines['Close Time'], unit='ms')
            return klines.drop([9, 10, 11], axis=1)
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No klines found: Invalid character - "+pair)
            elif (e.code == -1121):
                print("No klines found: Invalid Symbol - "+pair)
            else:
                print(e.code, e.message)

    def get_historical_klines(self, pair, k_interval, days_ago, inUnix=False):

        try:
            klines = pd.DataFrame()
            history = self.client.get_historical_klines(
                pair, k_interval, "24 Jun, 2019")
            # pair, k_interval, str(days_ago)+"days ago UTC")
            klines = klines.append(history, ignore_index=True)
            klines = klines.rename(columns={0: 'Open Time', 1: 'Open', 2: 'High', 3: 'Low',
                                            4: 'Close', 5: 'Inner Volume', 6: 'Close Time', 7: 'Outer Volume', 8: 'N. Trades'})

            if not inUnix:
                klines['Open Time'] = pd.to_datetime(
                    klines['Open Time'], unit='ms')
                klines['Close Time'] = pd.to_datetime(
                    klines['Close Time'], unit='ms')

            return klines.drop([9, 10, 11], axis=1)
        except BinanceAPIException as e:
            if (e.code == -1100):  # Illegal Character no Par
                print("No Hist. klines found: Invalid character - "+pair)
            elif (e.code == -1121):
                print("No Hist. klines found: Invalid Symbol - "+pair)
            else:
                print(e.code, e.message)
