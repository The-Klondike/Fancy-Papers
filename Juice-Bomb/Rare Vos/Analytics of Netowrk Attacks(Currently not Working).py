# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 21:16:29 2020

@author: kyler
"""

#%% Imports
import pandas as pd
import numpy as np
#%% Getting the data
# https://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html
names = pd.read_csv('/home/kyle-a/School/BFOR 416-516/data/kddcup.names.txt', header=None, delimiter=':', skiprows=(1))

names_list = names[0].tolist()

names_list.append('type')

print(names_list)

netattacks = pd.read_csv('/home/kyle-a/School/BFOR 416-516/data/kddcup.data.corrected', names=names_list, header=None, index_col=None)

#%% Dataframe statistics

netattacks.head(10)

netattacks.describe(include='all')

df_stats = netattacks.describe(include = 'all')

#%% Data Summary

type_counts = netattacks.groupby('type').count()

type_means = netattacks.groupby('type').mean()

type_counts = netattacks.groupby('type').agg(['count', 'mean'])

type_counts = netattacks['type'].value_counts()

type_counts.head()

#%% PLotting

netattacks['duration'].hist()

netattacks['count'].hist()

#%% Correlation statistic 

netattacks['duration'].corr(netattacks['count'])


netattacks['label'] = np.where(netattacks['type'] == 'normal.', 'good', 'bad')

netattacks['label'].value_counts()


#%% Lab Portion 

"""
1. Can you run correlations between continuous and categorical variables? Why or why not? 
2.Run a correlation between two or more other variables in the dataset. What might you interpret from this? 
3. Summarize by protocol (protocol_type). Are there more attacks using TCP or UDP?  ------ MORE TCP TYPE ATTACKS COMAPRED TO UDP  
"""
#1


""" you cannot run a correlation with a categorical data because correlation can only be done wiht numberical data and categorical data """

#2
netattacks['num_root'].corr(netattacks['duration'])
# Out[40]: 0.05676597485929489       There is a weak correlation between the time spent during an attack and the number of root files accessed
netattacks['src_bytes'].corr(netattacks['duration'])
# Out[42]: 0.004258230269512663     there is no correlation between duration and number of bytes sent drom the source.

#3

netattacks['protocol_type'].value_counts()
"""
There are more attacks done using TCP rather that UPD

Out[36]: 
icmp    283602
tcp     190065
udp      20354
Name: protocol_type, dtype: int64
"""
