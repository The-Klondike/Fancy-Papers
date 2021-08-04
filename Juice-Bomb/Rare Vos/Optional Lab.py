# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 21:00:48 2020

@author: kyler
"""
#%% Imports
import pandas as pd
import datetime
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from sklearn import metrics

#%% Data
last_ten_alb = pd.read_csv('../forecast_comp/last_ten_alb.csv')
last_ten_alb['date'] = pd.to_datetime(last_ten_alb['YEARMODA'])
last_ten_alb.set_index('date', inplace=True)
last_ten_alb.index = last_ten_alb.index.to_period('D')

# creatinga  smaller dataset


test = last_ten_alb.tail(90)
print(test['MAX'])


#%% Time Series Prediction

ar_model = AutoReg(endog=last_ten_alb['MAX'], lags=[1, 2, 3], missing='drop').fit()
ar_model.summary()

#%% Auto Regression Prediction
start_date = last_ten_alb.index.max() - datetime.timedelta(days=89)
end_date = last_ten_alb.index.max() 
ar_pred = ar_model.predict(start=start_date, end=end_date)

print(ar_pred)
print(test['MAX'])

#%% Evaluation
ar_rmse = metrics.mean_squared_error(test['MAX'], ar_pred, squared=False)
print("RMSE:", ar_rmse)

#%%Visuals
ar_pred.plot()
test['MAX'].plot()

#%% Future Prediction


train = last_ten_alb.head(-10)
test = last_ten_alb.tail(10)
ar_new = AutoReg(endog=train['MAX'], lags=[1, 2, 3], missing='drop').fit()
ar_new.summary()

#%% Generating Future Predictions 
start_date = train.index.max() + 1
end_date = start_date + datetime.timedelta(days=9)
ar_pred = ar_new.predict(start=start_date, end=end_date)

ar_rmse = metrics.mean_squared_error(test['MAX'], ar_pred, squared=False)
print("RMSE:", ar_rmse)

ar_pred.plot()
test['MAX'].plot()

