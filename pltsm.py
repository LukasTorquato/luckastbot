
from keras.layers import Activation
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Dense
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
import gc
import plotly.graph_objs as go
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import pytz
from plotly import tools
import chart_studio.plotly as py

# init_notebook_mode(connected=True)
# define a conversion function for the native timestamps in the csv file


def dateparse(time_in_secs):
    return pytz.utc.localize(datetime.datetime.fromtimestamp(float(time_in_secs)))


# data[['Volume', 'Volume MA']] = data[[
#    'Volume', 'Volume MA']].mul(data['close'], axis=0)
# load the dataset
data = pd.read_csv('datasets/BITSTAMP_BTCUSD_1D.csv',
                   parse_dates=[0], date_parser=dateparse)
data['time'] = data['time'].dt.tz_localize(None)
data = data.groupby([pd.Grouper(key='time', freq='H')]
                    ).first().reset_index()
data = data.set_index('time')
data = data[['close']]
data['close'].fillna(method='ffill', inplace=True)
data.info()


def plot_graph(data):
    # create valid date range
    start = datetime.datetime(2012, 1, 1, 0, 0, 0, 0, pytz.UTC)
    end = datetime.datetime(2020, 12, 31, 0, 0, 0, 0, pytz.UTC)

    # find rows between start and end time and find the first row (00:00 monday morning)
    weekly_rows = data[(data['time'] >= start) & (data['time'] <= end)].groupby(
        [pd.Grouper(key='time', freq='W-MON')]).first().reset_index()
    weekly_rows.head()

    # We use Plotly to create the plots https://plot.ly/python/

    trace1 = go.Scatter(
        x=weekly_rows['time'],
        y=weekly_rows['close'].astype(float),
        mode='lines',
        name='close'
    )

    trace2 = go.Scatter(
        x=weekly_rows['time'],
        y=weekly_rows['Price_Prediction'].astype(float),
        mode='lines',
        name='Price_Prediction'
    )

    layout = dict(
        title='Historical Bitcoin Prices (2012-2020) with the Slider ',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    # change the count to desired amount of months.
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=12,
                         label='1y',
                         step='month',
                         stepmode='backward'),
                    dict(count=36,
                         label='3y',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type='date'
        )
    )

    data = [trace1, trace2]
    fig = dict(data=data, layout=layout)
    plot(fig, filename="Time Series with Rangeslider")


# split data
split_date = '25-Jun-2020'
data_train = data.loc[data.index <= split_date].copy()
data_test = data.loc[data.index > split_date].copy()

# Data preprocess
training_set = data_train.values
training_set = np.reshape(training_set, (len(training_set), 1))
sc = MinMaxScaler()
training_set = sc.fit_transform(training_set)
X_train = training_set[0:len(training_set)-1]
y_train = training_set[1:len(training_set)]
X_train = np.reshape(X_train, (len(X_train), 1, 1))

# Importing the Keras libraries and packages


model = Sequential()
model.add(LSTM(128, activation="sigmoid", input_shape=(1, 1)))
model.add(Dropout(0.2))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, epochs=50, batch_size=50, verbose=2)

model.summary()

# Making the predictions
test_set = data_test.values
inputs = np.reshape(test_set, (len(test_set), 1))
inputs = sc.transform(inputs)
inputs = np.reshape(inputs, (len(inputs), 1, 1))
predicted_BTC_price = model.predict(inputs)
predicted_BTC_price = sc.inverse_transform(predicted_BTC_price)

data_test['Price_Prediction'] = predicted_BTC_price
data_all = pd.concat([data_test, data_train], sort=False)

# saving the predicted values in a common data frame for future comparision
final_data = data_all
final_data = final_data.reset_index()
# final_data.info()
final_data = final_data.rename(columns={'Price_Prediction': 'lstm'})
final_data = final_data[['time', 'close', 'lstm']]

f, ax = plt.subplots(1)
f.set_figheight(5)
f.set_figwidth(15)
_ = data_all[['Price_Prediction', 'close']].plot(ax=ax,
                                                 style=['-', '.'])
ax.set_xbound(lower='08-01-2018', upper='09-01-2018')
ax.set_ylim(0, 10000)
plot = plt.subtitle('August 2018 Forecast vs Actuals')
#_ = data_all[['close', 'Price_Prediction']].plot(figsize=(15, 5))
