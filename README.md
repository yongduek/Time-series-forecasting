# Time Series Decomposition & Forecasting

Various techniques are experimented.

0. Time series forecasting using CNTK
1. https://pypi.python.org/pypi/seasonal : a package for time series decomposition, X13, forecasting, etc

### Time-series-forecasting-using-CNTK

The code to accompany [“Time-series-forecasting-using-CNTK” tutorial][1] on Cortana Intelligence Gallery.

[1]: https://gallery.cortanaintelligence.com/Tutorial/Forecasting-Short-Time-Series-with-LSTM-Neural-Networks-2

#### Data: see http://irafm.osu.cz/cif/main.php?c=Static&page=download

#### Data Files
cif-dataset.txt : dataset for learning.
ci-results.txt : uncovered values that had to be forcasted.

#### Competition Data Format

Data file containing time series to be predicted is a text file having the following format:

- Each row contains a single time series data record;
- items in the row are delimited with semicolon (";");
- the first item is an ID of the time series;
- the second item determines the forecasting horizon, i.e., the number of values to be forecasted;
- the third item determines the frequency of the time series (this year "monthly" only);
- the rest of the row contains numeric data of the time series;
- the number of values in each row may differ because each time series is of different length.
- Example of the competition data format:
```
ts1;4;yearly;26.5;38.2;5.3
ts2;12;monthly;1;2;4;5;5;6;8;9;10
...
ts72;12;daily;1;2;4;5;5;6;8;9;10
```

The following command executes R with the script and makes a directory named 'data' and puts there some sequence data for learning.
```
  $ Rscript CIF2016/src/cifPrepStl.R
```
