# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:24:09 2020

@author: kyler
"""


#%% imports
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
#%% trying to build a function to get logons and put them in its own dataframe. here is the function for that dataframe



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
            time = is_time(row)
            username = get_user_name(row)   # this row was created in class
            username = username.replace("evilbot","")
            message = get_chat_message(row)  # this row was created in class 
            df_row = {'time': time, 'username': username, 'message': message}
            #df_row = {'username': username, 'message': message}   # this row was created in class
            chat_records.append(df_row)   # this row was created in class
        
        elif re.match(r'---', row[0:5]):     # this row was created in class
            pass      # this row was created in class
        
        else:
            pass      # this row was created in class
            
            
#%% greatest logons 

        
#%%#%% Saves our data in a dataframe allowing for easier manipulation

    chat_records_df = pd.DataFrame(chat_records)
    # actually turns the data into a dataframe
    chat_records_df['username'].replace("", np.nan, inplace=True)
    #replaces the blank usernames left from removing evilbots chat messages with NaN
    chat_records_df.dropna(subset=['username'], inplace=True)
    #removes the rows with NaN in the username 
    chat_records_df.tail(5)
    
    #%% above is all things done in the past