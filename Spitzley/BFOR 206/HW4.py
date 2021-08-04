# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:40:43 2020

@author: kyler
"""

#%%Imports

import re
import pytest
import pandas as pd
import numpy as np

#%% defining our functions
def is_message(row):
    """
    Determine if a row contains a message.

    Parameters
    ----------
    row : str
        row from chat log.

    Returns
    -------
    bool
        True if row belongs to chat log.

    """
    if re.search(r'<', row[6]):
        return True
    
    return False

def get_user_name(row):
    """
    Find the username in a chat row.

    Parameters
    ----------
    row : str
        row that contains a message.

    Returns
    -------
    string containing username.

    """
    #print('get_user_name: row=', row)
    username = re.search(r'<([ @+%&^_~\\])([\w{\}^_`|\\[\]-]+)>', row)
    #print('in get_user_name:', username.group(2))
    return username.group(2)


def get_chat_message(row):
    row_parts = re.split(r'> ', row)
    #print('get_chat_message : row_parts', row_parts)
    message = "> ".join(row_parts[1:])
    #print('get_chat_message: message', message)
    return message
#test_get_chat_message()
""" Take a row and find the chat message content """
def is_time(row):
    
    time = re.search(r'([0-9][0-9]):([0-9][0-9])', row)
    return time.group(0)

#%% for date and time
# lines for reference
#--- Log opened Tue Sep 20 00:01:49 2016
#--- Day changed Wed Sep 21 2016
from datetime import datetime

#%% for log oppen         DOES NOT WORK
datestring = "--- Log opened Tue Sep 20 00:01:49 2016"
parts = datestring.split(' ')
raw_date = " ".join([parts[7], parts[4], parts[5]])
date_formatted = datetime.strptime(raw_date, '%Y %b %d')
print(date_formatted)

def log_is_open(row):
    parts_for_open = datestring.split(' ')
    raw_date = " ".join([parts_for_open[7], parts_for_open[4], parts_for_open[5]])
    date_formatted_on_log = datetime.strptime(raw_date, '%Y %b %d')
    return date_formatted_on_log
#%% day change        WORKS
date_day = "--- Day changed Wed Sep 21 2016"
parts_day = date_day.split(' ')
raw_date_day = " ".join([parts_day[6], parts_day[4], parts_day[5]])
print(raw_date_day)
date_formatted_day = datetime.strptime(raw_date_day, '%Y %b %d')
print(date_formatted_day)

def is_date(row):
    parts_day = row.split(' ')
    raw_date_day = " ".join([parts_day[6], parts_day[4], parts_day[5]])
    date_formatted_day = datetime.strptime(raw_date_day, '%Y %b %d')
    return date_formatted_day

#%% need function now to find the date change/log open
def is_day(row):
    
        if re.search(r'---( +[\w][\w]+)( [\w]+)', row):
            return True
        return False
#make a true false where if day make true and another to find the actual day
   


    

#%% load data
raw_log = ""
with open('Logs/hackers.log', 'r+', errors='ignore') as f:
    raw_log = f.readlines()

    





#%% build for loop

def main():
    
    raw_log = ""
    with open('Logs/hackers.log', 'r+', errors='ignore') as f:
        raw_log = f.readlines()
            

    # create empty list to store chat records
    chat_records = []

    # iterate through the rows. 
    for row in raw_log:
        if is_message(row):
#            the_date = is_date(row)
            the_time = is_time(row)
            the_day_is = is_day(row)
#            day_is = log_is_open(row)
#            log_day = log_is_open(row)
            username = get_user_name(row)   # this row was created in class
            username = username.replace("evilbot","")
            message = get_chat_message(row)  # this row was created in class 
            df_row = {'date_change ': the_day_is,  ''' 'day': log_day,'''   'time': the_time, 'username': username, 'message': message}
            #df_row = {'day': date_formatted_day, username': username, 'message': message}   # this row was created in class
            chat_records.append(df_row)   # this row was created in class
        
        elif re.search(r'---', row[0:5]):      
            pass      # this row was created in class
        else : 
            pass      # this row was created in class
        
        
        #%% build the loop for the is day  IGNORE DOESNT WORK

for row in raw_log:
    if is_day(row):
        date = is_day(row)
        date_row = {'date': date}
        chat_records.append(df_row)
        return date
#%% Saves our data in a dataframe allowing for easier manipulation

    chat_records_df = pd.DataFrame(chat_records)
    # actually turns the data into a dataframe
    chat_records_df['username'].replace("", np.nan, inplace=True)
    #replaces the blank usernames left from removing evilbots chat messages with NaN
    chat_records_df.dropna(subset=['username'], inplace=True)
    #removes the rows with NaN in the username 
    chat_records_df.tail(5)

    chat_records_df.username.value_counts()
#finds the users that post the most
    chat_records_df.message.count()
#Finds the total number opf messages that are posted43
    chat_records_df.message.value_counts().head(30)     #not what he wants
    #find the most common string and messages
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.cat.html
#%% to find URL / web addresses posted in chat

# saving the dataframe to a CSV file
chat_records_df.to_csv(r'C:\Users\kyler\School\BFOR 206\chat_records.csv', index=False)

#imports             
import collections 
from collections import Counter

web_address = re.findall(r'(?P<url>https?://[^\s]+)', open('chat_records.csv', encoding="utf8").read().lower())
# Find URL's in the chat 
web_address_df = pd.DataFrame(web_address)
#Makes it a dataframe
web_address_df.count()
# number of posted URL/web addresses
most_common = collections.Counter(web_address).most_common(10)
# Finds the most common URL's

