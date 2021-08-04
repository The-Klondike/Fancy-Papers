# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 18:52:47 2020

@author: kyler
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy
#%% External Data

county = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')

#%% Setting Variables 

today = datetime.date.today()

print(today)

output = 'output/capital_comparison_' + str(today) + '.jpg'
date_title = 'COVID-19 Cases in the Capital Region (' + str(today)+ ")"

date_deaths_title = 'COVID-19 Deaths in New York as of (' + str(today)+ ")"

#%%Date Conversion

county['date'] = pd.to_datetime(county['date'])

#%% Column Summary

print(county.describe(include='all', datetime_is_numeric = True ))

#%% class portion

# County Names
cr = ['Albany', 'Columbia', 'Fulton', 'Greene', 'Montgomery', 'Rensselaer', 
      'Saratoga', 'Schenectady', 'Schoharie', 'Warren', 'Washington']

# select only the data from NY where the county names are in the list above
alb =  county[(county['state'] == 'New York') & (county['county'].isin(cr)) & (county['cases'] > 0)]

county_plot = alb.groupby(['date', 'state'])['cases'].sum('date').unstack().plot(logy=False, figsize=(10,5))


# PLotting cases by county
county_plot = alb.groupby(['date', 'county'])['cases'].sum(cr).unstack().plot(logy=False, figsize=(10,5))
county_plot.set(xlabel='date', ylabel='Number of Cases', title=date_title)
county_plot.get_figure()

# PLotting Deaths by county in the capital region
cr_death = alb.groupby(['date', 'state'])['deaths'].sum('date').unstack().plot(logy=True, figsize=(10,5))
cr_death.set(xlabel='date', ylabel='Number of Cases', title=date_title)
cr_death.get_figure()



# Save the Fig

county_plot.get_figure().savefig(output, bbox_inches='tight', dpi=300)

#%% Deaths per county in the CaPITAL REGION

# County Names
cr = ['Albany', 'Columbia', 'Fulton', 'Greene', 'Montgomery', 'Rensselaer', 
      'Saratoga', 'Schenectady', 'Schoharie', 'Warren', 'Washington']

# select only the data from NY where the county names are in the list above
alb =  county[(county['state'] == 'New York') & (county['county'].isin(cr)) & (county['cases'] > 0)]

county_plot = alb.groupby(['date', 'state'])['cases'].sum('date').unstack().plot(logy=False, figsize=(10,5))


# PLotting cases by county
county_plot = alb.groupby(['date', 'county'])['cases'].sum(cr).unstack().plot(logy=False, figsize=(10,5))
county_plot.set(xlabel='date', ylabel='Number of Cases', title=date_title)
county_plot.get_figure()

# Save the Fig

county_plot.get_figure().savefig(output, bbox_inches='tight', dpi=300)



#%% Total cases in the capital region 

cr_case = alb.groupby(['date', 'state'])['cases'].sum('date').unstack().plot(figsize=(10,5))
cr_case.set(xlabel='date', ylabel='Number of Cases', title=date_title)
cr_case.get_figure()

#%% Deaths in capital region

alb_death =  county[(county['state'] == 'New York') & (county['county'].isin(cr)) & (county['deaths'] > 0)]

alb_death.sum(axis = 1, skipna= True)

county_deaths_plot = alb_death.groupby(['date', 'state'])['deaths'].sum('deaths').unstack().plot(logy=False, figsize=(10,5))
county_deaths_plot.set(xlabel='date', ylabel='Number of deaths', title=date_deaths_title)
county_deaths_plot.get_figure()


#%% PLotting the Total Deaths in the USA

alb_total_death =  county[(county['state'] == 'New York') & (county['deaths'] > 0)]

county_deaths_plot1 = alb_total_death.groupby(['date'])['deaths'].sum('deaths').plot(logy=False, figsize=(10,5))
county_deaths_plot1.set(xlabel='date', ylabel='Number of deaths', title=date_deaths_title)




#%% Go back over upper code block for the number of deaths. also check slack for a response to my question ^^^^^^^^^^^^^^^^