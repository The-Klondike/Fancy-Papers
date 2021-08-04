#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:34:35 2020

@author: kyler
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy
#%% state and county data

county = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
state = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
worldwide= pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')


#%% Converting to proper date column
# convert dates
state['date'] = pd.to_datetime(state['date'])
county['date'] = pd.to_datetime(county['date'])
# ^ converts to propper date time
#%% Percent Change to Cases and Deaths Daily- from class

"""  https://pandas.pydata.org/pandas-docs/stable/reference/frame.html 
     Pandas how to work with a dataframe
     possibly find the difference from day to day in order to graph it"""

daily = state.groupby('date').sum()

daily['cfr'] = daily['deaths'] / daily['cases']
#^ Finds the Case Fatality Rate
daily['Case_Difference'] = daily['cases'] - daily['cases'].shift(1) 
#^ This line does the daily difference in number of cases and adds it to the dataframe

daily['Pct_Chg_Cases'] = daily['cases'].pct_change()
daily['Pct_Chg_Deaths'] = daily['deaths'].pct_change()
#^ adds the Percent change of deaths and cases to the Daily Dataframe
#%% State and County highest CFR as of most recent day

statecfr = state.groupby(['state', 'date']).sum()
statecfr['cfr'] = statecfr['deaths'] / statecfr['cases']


countycfr = county.groupby('county').sum()
countycfr['cfr'] = countycfr['deaths'] / countycfr['cases']


#%% Graphs

cfr_plot = daily.plot(y='cfr', title='Daily Case Fatality Rate in the US')

cfr_plot.set(xlabel='Date', ylabel='Case Fatality Rate')
cfr_plot.get_figure().savefig('output/HW3/CFR_Plot.pdf', bbb_inches='tight')
# ^ charts the case fatality rate in the US

pct_plot = daily.plot(y='Case_Difference', title='Daily Difference In Number of Cases in The United States')  # Run this line Seperate
pct_plot.get_figure().savefig('output/HW3/Daily_Diff_Cases.pdf', bbb_inches='tight')
# ^ charts the daily difference in number of cases

daily_case_death =state.groupby(['date'])['cases', 'deaths'].sum().plot(logy=True, legend=True)
daily_case_death.get_figure().savefig('output/HW3/Daily_Case_Death.pdf', bbb_inches='tight')
# ^ charts the daily cases and deaths on one line chart

states_to_compare2 = ['Wyoming', 'Florida', 'Texas', 'New York']

state_sub_df2 = state[state['state'].isin(states_to_compare2) & (state['cases'] >= 10)]

state_sub_plot2 = state_sub_df2.groupby(['date', 'state',])['cases'].sum().unstack().plot(logy=True)
state_sub_plot2.set(xlabel='Date', ylabel='Number Of Cases', title='comparison of cases')
state_sub_plot2.get_figure().savefig('output/HW3/State_Comparison.pdf', bbb_inches='tight')
# ^compare the number of cases in 3 states 
#

#%% Summarizing The Data
#%% State Data

highest_ST = state.sort_values(by=['state', 'date'], ascending=False)
# ^ Sumarizes state data by finding top 5 states by number of cases

highest_ST['date']= pd.to_datetime(highest_ST['date'])

highest_ST['Case_Difference'] = highest_ST['cases'] - highest_ST['cases'].shift(-1) 

highest_ST = highest_ST.dropna()
highest_ST.sort_values(by=['date', 'Case_Difference'], ascending=False).drop_duplicates(subset=['state'], keep='first').head(5)
# ^ finds the states with the most new cases by moost recent day


highest_ST['Daily_PCT_Increase'] = highest_ST.sort_values(['date'], ascending=[True] ).groupby(['state']).cases.pct_change()
highest_ST = highest_ST.dropna()
highest_ST.sort_values(by=['date','Daily_PCT_Increase'], ascending=False).drop_duplicates(subset=['state'], keep='first').head(5)
# ^ sumarizes state data finding the percent change in number of case's bassed on newest date

#%% County Data

highest_CT = county.sort_values(by=['county','date'], ascending=False)
# ^ Finds the counties with the highest number of cases 

highest_CT['date']=pd.to_datetime(highest_CT['date'])

highest_CT['Case_Difference'] = highest_CT['cases'] - highest_CT['cases'].shift(-1)

highest_CT = highest_CT.dropna()
highest_CT.sort_values(by=['date', 'Case_Difference'], ascending=False).drop_duplicates(subset=['county'], keep='first').head(5)
# ^ finds the county with the most new cases from the previous day

highest_CT['PCT_Move'] = highest_CT.sort_values(['date'], ascending=[True] ).groupby(['county']).cases.pct_change()
highest_CT = highest_CT.dropna()
highest_CT.sort_values(by=['date', 'PCT_Move'], ascending=False).drop_duplicates(subset=['county'], keep='first').head(5)
# ^ Sumarizes state data by finding top 5 counties by number of cases


#%% Worldwide Data analysis
x=range('1/22/20', '4/22/20')
countries_to_compare = ['Italy', 'US', 'Spain', 'China', 'Japan']

country_sub_df = worldwide[worldwide['Country/Region'].isin(countries_to_compare)]

worldwide.plot.groupby(['1/22/20 : 4/22/20', ])
#%% Export to CSV
daily.to_csv (r'C:\Users\kyler\Bfor206\Output\HW3\Daily.csv', header=True)
county.to_csv (r'C:\Users\kyler\Bfor206\Output\HW3\County.csv', header=True)
countycfr.to_csv (r'C:\Users\kyler\Bfor206\Output\HW3\Countycfr.csv', header=True)
highest_CT.to_csv (r'C:\Users\kyler\Bfor206\Output\HW3\Highest_County.csv', header=True)
highest_ST.to_csv (r'C:\Users\kyler\Bfor206\Output\HW3\Highest_State.csv', header=True)
state.to_csv (r'C:\Users\kyler\Bfor206\Output\HW3\state.csv', header=True)
statecfr.to_csv (r'C:\Users\kyler\Bfor206\Output\HW3\statecfr.csv', header=True)

