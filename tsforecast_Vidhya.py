# -*- coding: utf-8 -*-

'''
    https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/
    https://github.com/aarshayj/Analytics_Vidhya/blob/master/Articles/Time_Series_Analysis/Time_Series_AirPassenger.ipynb


'''

import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pylab as plt
#matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6

# Note: aim is not to teach stock price forecasting. It's a very complex domain and I have almost no clue about it.
# Here I will demonstrate the various techniques which can be used for time-series forecasting
data = pd.read_csv('AirPassengers.csv')
print (data.head())
print ('\n Data Types:')
print (data.dtypes)

#
# reading as datetime format
#
#dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
#dateparse('1962-01')
#data = pd.read_csv('AirPassengers.csv', parse_dates='Month', index_col='Month',date_parser=dateparse)
data = pd.read_csv('AirPassengers.csv', index_col='Month', parse_dates=True)
print (data.head())
print ('$$ data index will show dtype=datetime64[ns]')

print ('# check datatype of index')
print (data.index)

print ('# extract a column and convert it to time series:')
ts = data['#Passengers']
print(ts.head(10), '\n')
print ('ts at 1949-01-01 is {}'.format(ts['1949-01-01']))
print ('ts at 1949-01-01 is {}'.format(ts[datetime(1949,1,1)]))
print ('ts in 1949 is\n{}'.format(ts['1949']))

print ('# now plot a ts')
plt.plot(ts)
#plt.show() # blocking
plt.title (' input sequence ')
plt.draw()

#
# functions for testing stationarity of the time series
#

from statsmodels.tsa.stattools import adfuller

def test_stationarity (tseries):
    # determine rolling statistics
    rolling = tseries.rolling(window=12)
    rolmean = rolling.mean()
    rolstd = rolling.std()

    #plot rolling statistiscs
    plt.figure()
    orig = plt.plot(tseries, color='blue', label='original')
    mean = plt.plot(rolmean, color='red', label='rolling mean')
    std = plt.plot(rolmean+rolstd, color='black', label='rolling std')
    std2 = plt.plot(rolmean-rolstd, color='black')

    plt.legend (loc='best');
    plt.title ('rolling mean & std')
    plt.show (block=False)

    # perform Augmented Dickey-Fuller test
    # https://www.otexts.org/fpp/8/1 : adf test can be used to test the stationarity of a signal.
    print ('# results of Dickey-Fuller Test: ')
    dftest = adfuller(tseries, autolag='AIC')
    dfoutput = pd.Series (dftest[0:4], index=['test stat', 'p-val', '#lags used', '# observations used'])
    for key, v in dftest[4].items():
        dfoutput['Critical Value {}'.format(key)] = v
    print (dfoutput)
    print ('## Large p-values are indicative of non-stationarity, and small p-values suggest stationarity\n',
           'Using the usual 5% threshold, differencing is required if the p-value is > 0.05\n',
           'Another popular unit root test is the Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test.'
           )

    if dfoutput['p-val']>0.05:
        print ('!! this time series is not stationary at all p-val({})>0.05'.format(dfoutput['p-val']))
    else:
        print ('!! this time series looks stationary because p-val < 0.05')
#

test_stationarity(ts)

#
# Making a TS Stationary
#

# first way is difference of log-scales

# 1. log scale
tslog = np.log (ts)
plt.figure()
plt.plot (tslog)
plt.title (' log (ts)')

window = 12
# 2. moving average
mavg = tslog.rolling (window=window).mean()
plt.plot (mavg, color='red')
plt.title (' moving average ')

tslog_mavg = tslog - mavg
print (tslog_mavg.head(window))
tslog_mavg.dropna (inplace=True)
print (tslog_mavg.head(window))

test_stationarity(tslog_mavg)

# another moving average method is Exponentially weighted moving average
exp_mavg = tslog.ewm(halflife=window).mean()
plt.figure()
plt.title (' exponentially weighted moving average')
plt.plot(tslog)
plt.plot(exp_mavg, color='red')

tslog_expmavg = tslog - exp_mavg
tslog_expmavg.dropna(inplace=True)

test_stationarity(tslog_expmavg)
print ('# Kill the plot window to finish.')
plt.show()

