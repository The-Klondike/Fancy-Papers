# -*- coding: utf-8 -*-
"""
Today we will continue with developing and testing functions. 

The function today will be used to extract the username from a row.

We can use the same test data as before. We may need to add some
new test inputs, and some types (join/quit and date change) are 
not relevant, since they shouldn't be passed to this function.

Note the comprehensive documentation of the is_message function. 

@author: lee
"""



#%% imports
import re



#%% define function from previous class 
# we will need this for the lab!
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
    # helpful to put function name in your print statement
    # print('is_message: ', row)
    if re.search(r'<', row[6:7]): 
        return True
    
    return False



#%% define function to extract usernames
def get_user_name(row):
    """ This function takes a chat row and find the 
    username of the person who wrote the chat message """
    
    username = re.search(r'<([ +])([\w]+)>', row)
    print('in get_username:', username.group(2))
    return username.group(2)


#%% test get_user_name()
# define some sample rows
comment_row_1 = '01:17 < HeavenGuard> hello?' 
comment_row_2= '19:29 <+Cogitabundus> Some like chaos.'
comment_row_3 = '19:29 <+Cogit1234> Some like chaos.'
comment_row_4 = '19:29 < leeroy> Some like < User1234>'
join_quit_1 = '00:01 -!- Guest40341 [AndChat2541@AN-pl0gl1.8e2d.64f9.r226rd.IP] has quit [Quit: Bye]'
join_quit_2 = '18:39 -!- Hex [Hex@Quantum.Time] has quit [ < Hex> ]'
log_open_1 = '--- Log opened Tue Sep 20 00:01:49 2016'

# define test function

def test_get_username():
    assert get_user_name(comment_row_1) == 'HeavenGuard'
    assert get_user_name(comment_row_2) == 'Cogitabundus'
    assert get_user_name(comment_row_3) == 'Cogit1234'
    assert get_user_name(comment_row_4) == 'leeroy'

# run test function
    test_get_username()

#%% load data
raw_log = ""
with open('Logs/hackers.log', 'r+', errors='ignore') as f:
    raw_log = f.readlines()
    
    
#%% lab
"""
print out usernames for comments (only print this) for the first 100 rows.
See the image on Slack for how this should look.
"""
# code from last time
for row in raw_log[0:100]:
    # print(row)
    if is_message(row):
        name = get_user_name(row)
       # print("row is message")
        print('username is', name)
    elif re.match(r'---', row[0:5]):
        pass
        # print("row is log on", row)
