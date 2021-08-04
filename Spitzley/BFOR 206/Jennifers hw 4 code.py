# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:31:41 2020

@author: kyler
"""


#%%Imports

import re
import pytest
import pandas as pd
import numpy as np



#%% defining functions
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

#%% load data
raw_log = ""
with open('Logs/hackers.log', 'r+', errors='ignore') as f:
    raw_log = f.readlines()
    
#%% getting the number of chat messages in log 

def main():
    
    raw_log = ""
    with open('Logs/hackers.log', 'r+', errors='ignore') as f:
        raw_log = f.readlines()
    

    # create empty list to store chat records
    chat_records = []

    # iterate through the rows. 
    for row in raw_log:
        if is_message(row):
            username = get_user_name(row)  
            #print('row is message. Username is', username)
            username = username.replace("evilbot","")
            message = get_chat_message(row)  
            #print(message)
            df_row = {'username': username, 'message': message}
            #print(df_row)
            chat_records.append(df_row) 
        elif re.match(r'---', row[0:5]):    
            pass     
        
        else:
            pass     
# setting up that data frame 
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
#Finds the total number opf messages that are posted

# saving the dataframe to a CSV file
chat_records_df.to_csv(r'C:\Users\kyler\School\BFOR 206\chat_records.csv', index=False)

#%% most common words 

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


#%% top 5 words not in english 

#imports
from nltk.corpus import words
import nltk
nltk.download('words')

#empty list for messages to go to
message_list =[]

#%% setting up the dataframe 

# empty list for the words 
words_list = []
word_list2 = []


#iterate through the rows to split messages on spaces 
for row in raw_log:
    message = get_chat_message(row).split(" ")
    words_list.extend(message)
    var = (re.sub('[^a-zA-Z0-9]+', ' ', _ ) for _ in words_list)
    words_list.extend(var)
    word_count = Counter(word_list2)
else:
    pass
#creating the dataframe     
word_list2_df = pd.DataFrame(word_list2)

#%% finding and rakning top 5 non english words
# iterate through the words to sort english and non-english
for value in word_list2:
    if value in words.words():
        pass
    else:
        print(value)
        df_list = {'word': value}
        print(df_list)
        message_list.append(df_list)  
 
#count the most common words in the non-english list 
word_count = Counter(message_list)
print(word_count.most_common(5))