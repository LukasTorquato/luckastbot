# ================================================================
#
#   File name   : indicators.py
#   Author      : PyLessons
#   Created date: 2021-01-20
#   Website     : https://pylessons.com/
#   GitHub      : https://github.com/pythonlessons/RL-Bitcoin-trading-bot
#   Description : Used to plot 5 indicators with OHCL bars
#
# ================================================================
import pandas as pd
from config import *
from ta.trend import *
from ta.others import *
from ta.volume import *
from ta.momentum import *
from ta.volatility import *


from utils import Plot_OHCL


def add_volume_indicators(df):
    pass


def add_momentum_indicators(df):

    # Relative Strength Index (RSI) indicator
    if MOMENTUM_INDICATORS["RSI"]:
        df["RSI"] = rsi(close=df["Close"], window=14, fillna=True)

    # Stochastic RSI (SRSI)
    if MOMENTUM_INDICATORS["STOCH"]:
        df["stoch"] = stochrsi(close=df["Close"], window=14, fillna=True)
        df["stochd"] = stochrsi_d(close=df["Close"], window=14, fillna=True)
        df["stochk"] = stochrsi_k(close=df["Close"], window=14, fillna=True)


def add_volatility_indicators(df):

    # Add Bollinger Bands indicator
    if VOLATILITY_INDICATORS["BOLB"]:
        indicator_bb = BollingerBands(
            close=df["Close"], window=20, window_dev=2)
        df['bb_bbm'] = indicator_bb.bollinger_mavg()
        df['bb_bbh'] = indicator_bb.bollinger_hband()
        df['bb_bbl'] = indicator_bb.bollinger_lband()


def add_trend_indicators(df):

    # Simple Moving Average (SMA)
    if TREND_INDICATORS["SMA"]:
        df["sma7"] = SMAIndicator(
            close=df["Close"], window=7, fillna=True).sma_indicator()
        df["sma25"] = SMAIndicator(
            close=df["Close"], window=25, fillna=True).sma_indicator()
        df["sma99"] = SMAIndicator(
            close=df["Close"], window=99, fillna=True).sma_indicator()
        df["sma200"] = SMAIndicator(
            close=df["Close"], window=200, fillna=True).sma_indicator()

    # Exponential Moving Average (EMA)
    if TREND_INDICATORS["EMA"]:
        df["ema7"] = EMAIndicator(
            df["Close"], window=7, fillna=True).ema_indicator()
        df["ema25"] = EMAIndicator(
            df["Close"], window=25, fillna=True).ema_indicator()
        df["ema99"] = EMAIndicator(
            df["Close"], window=99, fillna=True).ema_indicator()
        df["ema200"] = EMAIndicator(
            df["Close"], window=200, fillna=True).ema_indicator()

    # Average Directional Movement Index (ADX)
    if TREND_INDICATORS["ADX"]:
        df["adx"] = adx(df['High'], df["Low"], df["Close"])
        df["adxn"] = adx_neg(df['High'], df["Low"], df["Close"])
        df["adxp"] = adx_pos(df['High'], df["Low"], df["Close"])

    # Ichimoku Kinkō Hyō (Ichimoku)
    if TREND_INDICATORS["ICMK"]:
        df["icmka"] = IchimokuIndicator(
            df["High"], df["Low"], fillna=True).ichimoku_a()
        df["icmkb"] = IchimokuIndicator(
            df["High"], df["Low"], fillna=True).ichimoku_b()
        df["icmkbl"] = IchimokuIndicator(
            df["High"], df["Low"], fillna=True).ichimoku_base_line()
        df["icmkcl"] = IchimokuIndicator(
            df["High"], df["Low"], fillna=True).ichimoku_conversion_line()

    # Add Parabolic Stop and Reverse (Parabolic SAR) indicator
    if TREND_INDICATORS["PSAR"]:
        indicator_psar = PSARIndicator(
            high=df["High"], low=df["Low"], close=df["Close"], step=0.02, max_step=2, fillna=True)
        df['psar'] = indicator_psar.psar()

    # Add Moving Average Convergence Divergence (MACD) indicator
    if TREND_INDICATORS["MACD"]:
        df["MACD"] = macd(close=df["Close"], window_slow=26,
                          window_fast=12, fillna=True)  # mazas


def add_others_indicators(df):
    pass


def AddIndicators(df):

    add_volume_indicators(df)
    add_momentum_indicators(df)
    add_volatility_indicators(df)
    add_trend_indicators(df)
    add_others_indicators(df)

    return df


if __name__ == "__main__":
    df = pd.read_csv('../../datasets/BTCUSDT-1H.csv')
    # df = df.sort_values('Date')
    df = AddIndicators(df)

    test_df = df[-400:]

    print(df)
    # Plot_OHCL(df)
