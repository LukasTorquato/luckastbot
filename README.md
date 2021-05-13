# luckastbot

TCC Trading Bot

### CUDA Libs - Installation

#### Tensorflow GPU install:

- Main link = https://www.tensorflow.org/install/gpu?hl=pt-br
- CUDA 11.0.x = https://developer.nvidia.com/cuda-toolkit-archive
- cuDNN 8.0.x For CUDA 11.0 = https://developer.nvidia.com/rdp/cudnn-archive

Not in use (yet):

- pip install tradingview-ta (not in use)

- TA-Lib (old):
  - Download VS Build Tools = https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16/ta-lib
  - https://github.com/mrjbq7
  - Follow every step

### To Do

- Class CustomAgent:
  - self.action_space = Ampliar possibilidades invés de buy, sell e hold. -> Step function:280
  - self.state_size = Entender o funcionamento
  - get_reward = Otimizar o reward da rede
