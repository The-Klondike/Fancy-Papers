#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic analysis of COVID-19 data

@author: leespitzley
"""

import pandas as pd
import matplotlib.pyplot as plt

#%% read in data

county = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
state = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')


#%% data cleaning

# convert dates

state['date'] = pd.to_datetime(state['date'])

# get column information

state.info()

#%% basic data exploration

daily = state.groupby('date').sum()


# see number of rows

#%% case fatality rate
# number of deaths / number of cases

daily['cfr'] = daily['deaths'] / daily['cases']
state.describe(include='all')


# make the line plot with title, legends, etc.

cfr_plot = daily.plot(y='cfr', title='Daily Case Fatality Rate in the US')

cfr_plot.set(xlabel='Date', ylabel='Case Fatality Rate')

cfr_plot.get_figure()
# save the plot as a PDF
# https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.savefig

# https://stackoverflow.com/questions/6774086/why-is-my-xlabel-cut-off-in-my-matplotlib-plot

cfr_plot.get_figure().savefig('output/cfr_plot.pdf', bbb_inches="tight")

#%% percent changes, day-by-day



# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pct_change.html

daily['Pct_Chg_Cases'] = daily['cases'].pct_change()
daily['Pct_Chg_Deaths'] = daily['deaths'].pct_change()




#%% lab

# plot the daily percent change in the US. 
pct_plot = daily.plot(y=['Pct_Chg_Cases', 'Pct_Chg_Deaths'])
# include title and labels
# and save as .jpeg
pct_plot.get_figure().savefig('output/pct_plot.pdf', bbb_inches="tight")

