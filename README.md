# luckastbot

TCC Trading Bot

### Python Libs - Installation

- pip install numpy
- pip install matplotlib
- pip install pandas
- pip install opencv-python
- pip install seaborn
- tensorflow==2.3.1
- tensorflow-gpu==2.3.1
- tensorboardx
- pip install python-binance
- pip install websocket
- pip install ta

Not in use (yet):

- pip install tradingview-ta (not in use)
- pip install backtrader
- pip install mplfinance

- TA-Lib (old):
  - Download VS Build Tools = https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16/ta-lib
  - https://github.com/mrjbq7
  - Follow every step

### To Do

- Class CustomAgent:
  - self.action_space = Ampliar possibilidades invés de buy, sell e hold. -> Step function:280
  - self.state_size = Entender o funcionamento
  - get_reward = Otimizar o reward da rede
