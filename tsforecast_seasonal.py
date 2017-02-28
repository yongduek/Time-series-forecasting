
# coding: utf-8

# # package: seasonal 0.3.1
# 
# Robustly estimate and remove trend and periodicity in a timeseries.
# 
# Seasonal can recover sharp trend and period estimates from noisy timeseries data with only a few periods. It is intended for estimating season, trend, and level when initializing structural timeseries models like Holt-Winters. Input samples are assumed evenly-spaced from a continuous real-valued signal with noise but no anomalies.
# 
# The seasonal estimate will be a list of period-over-period averages at each seasonal offset. You may specify a period length, or have it estimated from the data. The latter is an interesting capability of this package.
# 
# Trend removal in this package is in service of isolating and estimating the periodic (non-trend) variation. A lowpass smoothing of the data is removed from the original series, preserving original seasonal variation. Detrending is accomplishd by a coarse fitted spline, mean or median filters, or a fitted line.
# 
# See https://github.com/welch/seasonal for details on installation, API, theory, and examples.

# In[1]:

import math
import pandas as pd
import numpy as np
import seasonal as pkg_seasonal
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 10


# make a trended sine wave

# In[2]:

tseries = np.array( [10*math.sin(0.6 + i*2*math.pi / 25) + i*i/200.0 + 15 for i in range(100)] )


# In[3]:

rcParams['figure.figsize'] = 5,5
plt.plot(tseries,label='data')


# In[22]:

def seasonal_decomp(input_data, figure=True):
    input_tseries = np.array(input_data)
    '''
        input_data : np.ndarray
        
        output:
            trend: trend sequence
            residual:
            seasonal: seasonal of input length
            seasonal_period: period of seasonal series
            
        ---
        adjusted = input_ts - seasonal
        trend = a moving average
        residual = adjusted - trend
        
        input_ts = adjusted + seasonal
                 = residual + trend + seasonal
    '''
    seasons, trend = pkg_seasonal.fit_seasons(input_tseries)
    adjusted = pkg_seasonal.adjust_seasons(input_tseries,seasons=seasons)
    residual = adjusted - trend

    print ('$$ period of seasonal data = ', seasons.size)

    # append seasons so that the length equals input_tseries
    eseas = seasons
    while eseas.size < input_tseries.size:
        eseas = np.append(eseas,seasons)
    for i in range(seasons.size):
        if eseas.size < input_tseries.size:
            eseas.append(seasons[i])
            
    if eseas.size != input_tseries.size:
        print ('!! bug: seasonal data length {} not the same as input {}'.format(eseas.size,input_tseries.size))

    recon = trend+residual+eseas
    diff = np.abs(recon - input_tseries)
    min_error_th = 1E-12
    if np.max(diff) > min_error_th:
        print ('!! bug: The reconstruction error should be almost zero, but not max={}: ', np.max(diff))

    if figure==True:
        rcParams['figure.figsize'] = 15,7
        plt.figure()
        plt.grid()
        plt.plot(input_tseries,label='input', color='blue')
        plt.plot(trend, label='trend', color='red')
        plt.plot(residual, label='residual', color='black')
        #plt.plot(adjusted, label='adjusted', color='green')
        plt.plot(eseas, label='seasonal', color='green')
        plt.legend(loc='best')

    if isinstance(input_data, pd.Series):
        print ('$$ output type conversion to {}'.format(type(input_data)))
        trend = pd.Series (trend, index=input_data.index, name='Trend')
        residual = pd.Series (residual, index=input_data.index, name='Residual')
        eseas = pd.Series (eseas, index=input_data.index, name='Seasonal')

    return trend, residual, eseas, seasons.size
#end


# In[23]:

#seasons, trend = seasonal.fit_seasons(tseries)
#adjusted = seasonal.adjust_seasons(tseris,seasons=seasons)
#residual = adjusted - trend

print (type(tseries), isinstance(tseries,np.ndarray))

t,r,s,sn = seasonal_decomp(tseries)

print ('period of seansal data = ', sn)

recon = t+r+s
diff = np.abs(recon - tseries)
print ('This reconstruction error should be almost zero: recon - tseries: ', np.max(diff))


# In[24]:

import pandas as pd
from datetime import datetime

data = pd.read_csv('AirPassengers.csv', index_col='Month', parse_dates=True)
print ('--- some data in head ---')
print (data.head())
print ('--- some data in tail ---')
print (data.tail())
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

airlog = np.log(ts)
plt.plot(airlog)


# In[25]:

# Seasonal decomposition

trend,residual,seasonal,seasonal_period = seasonal_decomp(airlog)


# In[26]:

print (type(airlog))
print (type(np.array(airlog)))
print (type(trend))

#trend = pd.Series (trend, index=airlog.index, name='trend')
#residual = pd.Series (residual, index=airlog.index, name='residual')

print (type(trend), isinstance(trend, pd.Series))


# In[27]:

print (trend.head(3), trend.tail(5))
print ('residual:\n', residual.tail(5))


# In[28]:

print (airlog.index)


# In[ ]:




# In[ ]:



