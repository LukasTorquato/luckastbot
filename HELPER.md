# Binance API Info:

### Functions:

###### WebSocket:

- url = "wss://stream.binance.com:9443/ws/btcusdt@trade"
  Pega os trades de BTC/USDT que estão acontecendo
- wss://stream.binance.com:9443/ws/btcusdt@kline_5m"
  Pega os Kline em tempo real

#### API:

###### Data:

- **client.get_all_tickers()**
  Pega todos os pares de trade e seu preço atual

- **client.get_order_book(symbol='BNBBTC')**
  Pega o livro de ordens atual para o par escolhido

- **client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)**
  Pega os últimos 500 candles do par selecionado, e no intervalo selecionado

- **client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")**
- **client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")**
- **client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")**
  Pega os candles no intervalo de tempo selecionado histórico

###### Trade:

- **client.create_order( symbol='BNBBTC', side=SIDE_BUY, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, quantity=100, price='0.00001')**
- **client.order_limit_buy( symbol='BNBBTC', quantity=100, price='0.00001)**
- **client.order_limit_sell( symbol='BNBBTC', quantity=100, price='0.00001)**
- **client.get_open_orders(symbol='BNBBTC')**
- **client.get_all_orders(symbol='BNBBTC')**
- **client.cancel_order(symbol='ADABUSD', orderId=orders[0]['orderid'])**
