# luckastbot

TCC Trading Bot

### CUDA Libs - Installation

#### Tensorflow GPU install:

- Main link = https://www.tensorflow.org/install/gpu?hl=pt-br
- pip install tensorflow==2.4.0
- pip install tensorflow-gpu==2.4.0

- CUDA 11.0.x = https://developer.nvidia.com/cuda-toolkit-archive
- cuDNN 8.0.x For CUDA 11.0 = https://developer.nvidia.com/rdp/cudnn-archive
- TensorRT 7.2.2 (Only Linux) = https://developer.nvidia.com/nvidia-tensorrt-7x-download
- pip install tensorboardx

### Python Libs - Installation

- pip install numpy==1.19.2
- pip install matplotlib
- pip install pandas
- pip install opencv-python
- pip install seaborn
- pip install python-binance
- pip install websocket
- pip install mplfinance
- pip install ta

Not in use (yet):

- pip install tradingview-ta (not in use)
- pip install backtrader

- TA-Lib (old):
  - Download VS Build Tools = https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16/ta-lib
  - https://github.com/mrjbq7
  - Follow every step

### To Do

- Class CustomAgent:
  - self.action_space = Ampliar possibilidades invés de buy, sell e hold. -> Step function:280
  - self.state_size = Entender o funcionamento
  - get_reward = Otimizar o reward da rede
