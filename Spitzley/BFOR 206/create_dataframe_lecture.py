# -*- coding: utf-8 -*-
"""
In today's class, we will work on creating
a pandas DataFrame from chat records in 
our dataset. 

It will build on the previous labs. First we will
create a new function to get the message content 
out from a chat row. Then we will create a 
dataframe with usernames and messages. 

We may also run into some unexpected issues.
We will work on debugging these issues. 
Debugging is perhaps the most important
skill for a programmer. 

@author: lee
"""

#%% imports
import re
import pytest
import pandas as pd
import numpy as np


#%% functions from previous weeks
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

test = '00:10 < xclmrk> -tools'
print(row[5])

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


def is_time(row):
    
    time = re.search(r'([0-9][0-9]):([0-9][0-9])', row)
    return time.group(0)
    print(row_parts[1])

#def is_day(row):
#    date = re.match(r'---( +[\w][\w]+)( [\w]+)', row)
#    return date
#make a true false where if day make true and another to find the actual day
#    print(date)
#%% fuction tests from prior weeks
# data



#%% create function to get the chat message and a test
def get_chat_message(row):
    row_parts = re.split(r'> ', row)
    #print('get_chat_message : row_parts', row_parts)
    message = "> ".join(row_parts[1:])
    #print('get_chat_message: message', message)
    return message



#test_get_chat_message()
""" Take a row and find the chat message content """


#%% load data
raw_log = ""
with open('Logs/hackers.log', 'r+', errors='ignore') as f:
    raw_log = f.readlines()
    
    
#%% build up for loop

def main():
    
    raw_log = ""
    with open('Logs/hackers.log', 'r+', errors='ignore') as f:
        raw_log = f.readlines()
    

    # create empty list to store chat records
    chat_records = []

    # iterate through the rows. 
    for row in raw_log:
    # print(row)
        if is_message(row):
        # print("row is message", row)
            #date = is_day(row)    
            time = is_time(row)
            username = get_user_name(row)   # this row was created in class
            username = username.replace("evilbot","")
            #print("row is message. Username is", username)
            message = get_chat_message(row)  # this row was created in class
            df_row = {'time': time, 'username': username, 'message': message}   # this row was created in class
            #df_row = {'date':date, 'time': time, 'username': username, 'message': message}
            #df_row = {'message': message}
            chat_records.append(df_row)   # this row was created in class
         
        
        
        elif re.match(r'---', row[0:5]):     # this row was created in class
            pass      # this row was created in class
        # print("row is log on", row)
        else:
            pass      # this row was created in class
        # print("row type not found:", row)
        
        
        
        
        
        
#%% test to get chat row except for evilbot

#this was not created in class 

        #print( list(filter(None, re.split(r'evilbot', r))) )
#%% lab
    """
    create dataframe with first 1000 rows (chat only) and print results
    """
    
    #chat_records_df = pd.DataFrame(chat_records)
    #chat_records_df['message'].replace('', np.nan, inplace=True)
    #chat_records_df.dropna(subset=['message'], inplace=True)
    
    
    
    """                 This is used instead if the abover for loop has username restored  """
    chat_records_df = pd.DataFrame(chat_records)
    chat_records_df['username'].replace("", np.nan, inplace=True)
    chat_records_df.dropna(subset=['username'], inplace=True)
    chat_records_df.tail(5)

    chat_records_df['time'] = pd.to_datetime(chat_records_df['time'])
    chat_records_df.time.split(" ")
    
    
    chat_records_df['time'] = chat_records_df['time'].dt.time
    chat_records_df['time'].between_time('00:00', '01:00', include_start = False)

    
    print(chat_records_df)

    if __name__ == '__main__':
        main()