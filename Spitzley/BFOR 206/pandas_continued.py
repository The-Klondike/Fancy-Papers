#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic analysis of COVID-19 data

Setup for Homework 3

@author: leespitzley
"""

import pandas as pd


#%% read in data

county = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
state = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')

# get column information
print(county.info())
print(state.info())
#%% data cleaning

# convert dates
county['date'] = pd.to_datetime(county['date'])
state['date'] = pd.to_datetime(state['date'])
# get column information

#%% basic data exploration
print(county.count())
print(state.count())
# see number of rows



#%% summary statistics
county.describe(include='all')
state.describe(include='all')
#%% aggregate

# get total daily cases in the US

# important note for aggregation: How do you need your data to look?
# check out https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html

daily = county.groupby('date').sum()
daily.tail()

#%% plot chart

# see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html

#linear

daily['cases'].plot.line()  

# log scale (good for visualizing exponentail growth)
daily['cases'].plot.line(logy=True)

#%% today's lab
daily['cases'].plot.line(logy=True, legend=True)
daily['deaths'].plot.line(logy=True, legend=True)
# plot in a single chart (with log scale) total cases and total deaths.
