# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 22:11:22 2020

@author: kyler
"""

#%% Imports
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn import metrics

#%% Pre-Processing

ld = pd.read_csv('C:/Users/kyler/Documents/Code/Python/Digital-Forensics/Bfor 416/Data/lendingclub_2015-2018.csv')
ld.head()
tmp = ld.tail()
display(tmp)

#%% Interest Rate Hist

ld['int_rate'].hist()

#%% Loan Duration

# view unique values
ld['term'].unique()

# split rows into parts
term_split = ld['term'].str.split(' ')

# view first five rows
print(term_split[:5])

# the str function can retrieve a specific list element for all rows
term_split.str[1]
ld['duration'] = term_split.str[1]

# add this to the dataframe
display(ld['duration'].head())
# this column is not in integer format. Must fix!

# convert column to integer
ld['duration'] = ld['duration'].apply(int)
display(ld['duration'].head())

#%% Rescaling the data
ld['log_loan_amnt'] = np.log(ld['loan_amnt'])
ld['log_annual_inc'] = np.log(ld['annual_inc'])


#%% COrrelations 
cols = ['int_rate', 'log_loan_amnt', 'installment', 'log_annual_inc', 'duration', 'fico_range_low', 'revol_util', 'dti']
corr = ld[cols].corr()
corr.style.background_gradient(cmap='coolwarm')

# ld[cols].corr() # <--- use this if you just want the table in non-graphical format
#   Original    pred_vars = ['log_loan_amnt', 'log_annual_inc', 'fico_range_low', 'revol_util', 'dti', 'duration']
#pred_vars = ['log_loan_amnt', 'log_annual_inc', 'fico_range_low','total_acc', 'dti', 'duration'] # NO revlo util,  instead open_acc
pred_vars = ['log_loan_amnt', 'log_annual_inc', 'fico_range_low', 'revol_util', 'dti', 'duration', 'all_util']
"""   
Greatest corr

int rate
INstallment

"""

#%% Drop Rows Without values

print("before dropping rows with missing data", len(ld))
ld = ld.dropna(subset=pred_vars)
print("after dropping rows with missing data", len(ld))

#%% TRaining and test Data

from sklearn.model_selection import train_test_split

# use index-based sampling since we have time series data
train, test = train_test_split(ld, test_size=0.25, shuffle=False)

# earliest and latest dates in train
print("training data starts\n", train['issue_d'].head())
print("training data ends\n", train['issue_d'].tail())
# earliest and latest in test
print("testing data starts\n", test['issue_d'].head())
print("testing data ends\n", test['issue_d'].tail())

reg_fico = sm.OLS(train['int_rate'], train['fico_range_low']).fit()
reg_fico.summary()

#%% Adding Additional Variables

reg_multi = sm.OLS(train['int_rate'], train[pred_vars], hasconst=False).fit()
reg_multi.summary()

#%% Evaluation

print(reg_fico.aic)
print(reg_multi.aic)

sm.stats.anova_lm(reg_fico, reg_multi)


#%% Prediction

fico_pred = reg_fico.predict(test['fico_range_low'])

fico_rmse = metrics.mean_squared_error(test['int_rate'], fico_pred, squared=False)
print("RMSE:", fico_rmse)

multi_pred = reg_multi.predict(test[pred_vars])

multi_rmse = metrics.mean_squared_error(test['int_rate'], multi_pred, squared=False)
print("RMSE:", multi_rmse)
