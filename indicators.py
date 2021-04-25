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
from config import *
from ta.trend import *
from ta.others import *
from ta.volume import *
from ta.momentum import *
from ta.volatility import *


def add_volume_indicators(df):
    # On-balance volume (OBV)
    if VOLUME_INDICATORS["OBV"]:
        df["obv"] = on_balance_volume(
            close=df["Close"], volume=df["Volume"], fillna=True)


def add_momentum_indicators(df, period):

    # Relative Strength Index (RSI)
    if MOMENTUM_INDICATORS["RSI"]:
        df["rsi"] = rsi(close=df["Close"], window=period, fillna=True)

    # Stochastic Oscillator (STOCH)
    if MOMENTUM_INDICATORS["STOCH"]:
        df["stoch"] = stoch(close=df["Close"], high=df["High"],
                            low=df["Low"], window=period, fillna=True)
        df["stochs"] = stoch_signal(
            close=df["Close"], high=df["High"], low=df["Low"], window=period, fillna=True)

    # Stochastic RSI (SRSI)
    if MOMENTUM_INDICATORS["SRSI"]:
        df["srsi"] = stochrsi(close=df["Close"], window=period, fillna=True)
        df["srsid"] = stochrsi_d(close=df["Close"], window=period, fillna=True)
        df["srsik"] = stochrsi_k(close=df["Close"], window=period, fillna=True)

    # Awesome Oscillator (AO)
    if MOMENTUM_INDICATORS["AO"]:
        df["ao"] = awesome_oscillator(
            high=df["High"], low=df["Low"], fillna=True)

    # Williams %R
    if MOMENTUM_INDICATORS["WR"]:
        df["wr"] = williams_r(high=df["High"],
                              low=df["Low"], close=df["Close"], fillna=True)

    # Ultimate Oscillator
    if MOMENTUM_INDICATORS["UO"]:
        df["uo"] = ultimate_oscillator(high=df["High"],
                                       low=df["Low"], close=df["Close"], fillna=True)


def add_volatility_indicators(df):

    # Bollinger Bands (BB) indicator
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
        # df["sma200"] = SMAIndicator(close=df["Close"], window=200, fillna=True).sma_indicator()

    # Exponential Moving Average (EMA)
    if TREND_INDICATORS["EMA"]:
        df["ema7"] = EMAIndicator(
            close=df["Close"], window=7, fillna=True).ema_indicator()
        df["ema25"] = EMAIndicator(
            close=df["Close"], window=25, fillna=True).ema_indicator()
        df["ema99"] = EMAIndicator(
            close=df["Close"], window=99, fillna=True).ema_indicator()
        df["ema200"] = EMAIndicator(
            close=df["Close"], window=200, fillna=True).ema_indicator()

    # Average Directional Movement Index (ADX)
    if TREND_INDICATORS["ADX"]:
        df["adx"] = adx(high=df['High'], low=df["Low"], close=df["Close"])
        df["adxn"] = adx_neg(high=df['High'], low=df["Low"], close=df["Close"])
        df["adxp"] = adx_pos(high=df['High'], low=df["Low"], close=df["Close"])

    # Ichimoku Kinkō Hyō (Ichimoku)
    if TREND_INDICATORS["ICMK"]:
        df["icmka"] = IchimokuIndicator(
            high=df["High"], low=df["Low"], fillna=True).ichimoku_a()
        df["icmkb"] = IchimokuIndicator(
            high=df["High"], low=df["Low"], fillna=True).ichimoku_b()
        df["icmkbl"] = IchimokuIndicator(
            high=df["High"], low=df["Low"], fillna=True).ichimoku_base_line()
        df["icmkcl"] = IchimokuIndicator(
            high=df["High"], low=df["Low"], fillna=True).ichimoku_conversion_line()

    # Parabolic Stop and Reverse (Parabolic SAR)
    if TREND_INDICATORS["PSAR"]:
        df['psar'] = PSARIndicator(
            high=df["High"], low=df["Low"], close=df["Close"], step=0.02, max_step=2, fillna=True).psar()

    # Moving Average Convergence Divergence (MACD)
    if TREND_INDICATORS["MACD"]:
        df["macd"] = macd(close=df["Close"], window_slow=26,
                          window_fast=12, fillna=True)

    if TREND_INDICATORS["CCI"]:
        # Commodity Channel Index (CCI)
        df["cci"] = cci(high=df["High"], low=df["Low"],
                        close=df["Close"], fillna=True)


def add_others_indicators(df):
    pass


def AddIndicators(df):

    add_volume_indicators(df)
    add_momentum_indicators(df, 14)
    add_volatility_indicators(df)
    add_trend_indicators(df)
    add_others_indicators(df)

    return df


if __name__ == "__main__":
    df = pd.read_csv('datasets/BTCUSDT-1H.csv')
    # df = df.sort_values('Date')
    df = AddIndicators(df)

    test_df = df[-400:]

    print(df)
    # Plot_OHCL(df)
