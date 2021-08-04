#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
- Basic regular expressions
- Introduction to IRC homework dataset

@author: leespitzley

#####################################################
DEFINING REGULAR EXPRESSIONS
#####################################################


What is a regular expression?
https://en.wikipedia.org/wiki/Regular_expression
"a sequence of characters that define a search pattern"

A way to search for patterns in a string.

For example, how many words are in the following sentence?:
    "Are there 8 words or 10 words in this sentence?"

Or, what is the hour of the day? What is the minute of the hour?:
    "08:45"
    "10:15"

#####################################################
WHY DO WE NEED THEM?
#####################################################

This is obvious to us a human, but computers are dumb.
It is our job to tell them what to look for.
It is especially important when we need to perform this task
thousands or millions of times. 

You should use a regex website to help build and test your expressions!
I recommmend https://regex101.com but there are many others

"""

#%% intro to regular expressions
# https://docs.python.org/3/library/re.html
import re

# find the first occurrence of something
print(re.search(r'BFOR', "BFOR 206: Programming for Analytics BFOR"))

# find all occurences of something
kyle = re.findall(r'kyle', 'kylekylekyleeee')
print(kyle)

#%%% find all occurrences of something
# get list of findings:
print(re.findall(r'BFOR', "BFOR 206: Programming for Analytics BFOR"))

# create iterable of matches (show where it found matches)
result = re.finditer(r'BFOR', "BFOR 206: Programming for Analytics BFOR")
for r in result:
    print(r)
    
#%% special tokens
# \t is tab \n is newline
hh_mm = "The time is \t10:43 \nOK."
print(hh_mm)

# find whitespaces (includes \t and ' ')
re.search(r'\s', hh_mm)
re.split(r'\s', hh_mm) # leaves empty entries in list (usually not desirable)
re.split(r'\s+', hh_mm)

#%% matching list(s)
re.search(r'[0-9]{2}:[0-9]{2}', hh_mm)

#%% groups
group_result = re.search(r'([0-9]{2}):([0-9]{2})', hh_mm)
print(group_result)
print(group_result.group(0)) # all
print(group_result.group(1)) # hours
print(group_result.group(2)) # minutes

#%% or statements
re.findall(r'BFOR|bfor|206', "BFOR 206: Programming for Analytics BFOR")


if re.search(r'BFOR|bfor|206', 'BFOR 206: Programming for Analytics BFOR'):
    print('found match')

#%% processing real text

""" 
The data for this lab and for the next homework comes from
the AZSecure Project. The data is available at:
    https://www.azsecure-data.org/internet-relay-chat.html
You should download the Hacker IRC data and add the 
hacker.log file to your current working directory. 
"""
# debug file locations
import os
os.getcwd()
os.listdir()
os.listdir('Logs')

# open data
raw_log = []
with open('Logs/hackers.log', 'r', errors='ignore') as f:
    # read into list 
    raw_log = f.readlines()

#%% view first 10 rows
print(raw_log[0:50])


#%% use a for loop to process rows
# only use first 10 rows
for row in raw_log:
    # print(row)
    # find row showing log opened
    if re.search(r'---', row[0:3]):
        print('found log opened row', row)

        
#%% today's lab
"""
For today's lab, show that you can identify
rows that that show that the log was opened.

"""


