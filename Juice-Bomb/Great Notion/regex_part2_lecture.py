# -*- coding: utf-8 -*-
"""
#############################################################
OVERVIEW
#############################################################
If you have looked through the hackers.log file,
you may have noticed a few types of data in the rows.

One type of row is that which indicates when the log
was opened or when the date changes. We found these
rows last week.

Today we will search for rows where chat participants
post messages. We will again be using regular expressions.


Instead of putting the check for whether the message
belongs to a user or someone else in the if statement, we will 
instead put it into a function. This will make the code
more readable and also easy to test (and therefore debug!). 


#############################################################
CREATING TESTS
#############################################################

By creating small functions that perform simple, specific
tasks, you can break your program into small pieces. 
For each of these small pieces, you can test how
the function reacts to different inputs. You can 
identify inputs that your function will receive, and 
determine what should come out of the function for each 
of these inputs. This is known as testing, and if done 
well, it will reduce the likelihood of bugs in your code,
it will save time on development, and it can be automated
so that you will know if a code change causes problems.

=============================================================
To get pytest functionality in your console,
install pytest.
From a console, run
conda install pytest

You can also add testing in Spyder:
conda install -c spyder-ide spyder-unittest
=============================================================

@author: lee
"""

#%% imports
import re

#%% define function to check if text is a user message
def is_message(row):
    """ chechs row to see if it is a char message (True/False)"""

    if re.search(r'<', row[6]):
        return True
        
    return False
    
#%% define tests

# define some sample rows
comment_row_1 = '01:17 < HeavenGuard> hello?'
comment_row_2 = '19:29 <+Cogitabundus> Some like chaos.'
join_quit_1 = '00:01 -!- Guest40341 [AndChat2541@AN-pl0gl1.8e2d.64f9.r226rd.IP] has quit [Quit: Bye]'
join_quit_2 = '18:39 -!- Hex [Hex@Quantum.Time] has quit [ < Hex> ]'
log_open_1 = '--- Log opened Tue Sep 20 00:01:49 2016'

# define the test functon
def test_is_message():
    print('Running Tests')
    assert is_message(comment_row_1) == True
    assert is_message(comment_row_2) == True
    assert is_message(join_quit_1) == False
    assert is_message(join_quit_2) == False
    assert is_message(log_open_1) == False
#%% call test function
test_is_message()

#%% load data

raw_log = []
with open('Logs/hackers.log', 'r', errors='ignore') as f:
    # read into list 
    raw_log = f.readlines()
    
    
    

    
#%% iterate through the rows (first 100)
for row in raw_log[0:100]:
     print('working on row:', row)
     if is_message(row):
         print('row contains a message', row)
     elif re.match(r'---', row[0:5]):
        print("row is log on", row)
     else:
        print("row type not found:", row)
        
#%% today's lab
"""
1. Show that your test of is_message() passes
2. Show the for loop using is_message() finds message rows:
    - Only print output with messages (first 100 rows of full dataset)


"""

        
        
    