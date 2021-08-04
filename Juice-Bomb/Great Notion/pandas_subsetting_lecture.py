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
state.describe(include='all')

#%% basic data exploration

# see number of rows


#%% subsetting data
state['state'] == 'New York'
ny = state[state['state'] == 'New York']
# https://stackoverflow.com/questions/12096252/use-a-list-of-values-to-select-rows-from-a-pandas-dataframe
states_to_compare = ['New York', 'Michigan', 'Washington']
state['state'].isin(states_to_compare)


# subnett cumerically
state['cases'] >= 10
state_sub_df = state[state['state'].isin(states_to_compare) & (state['cases'] >= 10)]
#%% plot subsets
# https://stackoverflow.com/questions/34225839/groupby-multiple-values-and-plotting-results
# plot a comparison of two states
# include title and labels.

state_sub_plot = state_sub_df.groupby(['date', 'state',])['cases'].sum().unstack().plot(logy=True)
state_sub_plot.set(xlabel='Date', ylabel='Number Of Cases', title='comparison of cases')
state_sub_plot.get_figure()
state_sub_plot.get_figure().savefig('Output/state_comparison.pdf', bbox_inches='tight')
#%% lab

# plot a comparison of two states other than NY and MI
# include title and labels
# and save as .jpeg or .pdf
states_to_compare2 = ['New Jersey', 'California', 'Nebraska']
state['state'].isin(states_to_compare2)


state_sub_df2 = state[state['state'].isin(states_to_compare2) & (state['cases'] >= 10)]

state_sub_plot2 = state_sub_df2.groupby(['date', 'state',])['cases'].sum().unstack().plot(logy=True)
state_sub_plot2.set(xlabel='Date', ylabel='Number Of Cases', title='comparison of cases')
state_sub_plot2.get_figure()
state_sub_plot2.get_figure().savefig('Output/state_comparison2.pdf', bbox_inches='tight')
