# -*- coding: utf-8 -*-
"""
In today's class, we will convert our basic print
statements to logging statements. Logging is similar
to printing, but it has many additional features.

Print statements are good for small scripts or to
quickly find some information. Logging is a little
extra work to set up, but it offers many advatages
over a print statment.

Logs have different priority levels. The lowest
level, DEBUG, will show all messages at DEBUG priority
and higher. INFO level messages are the next level of priority,
followed by WARNING and ERROR. If you only want to log
WARNING or greater messages, you do not need to comment
out all of the other lines. Instead, just switch the logging
level to WARNING.

Logging can also produce more information than print.
For example, it can show the time for each message, the filename,
the line number where the statement came from, the name of the
function the statement is located, and you can do special
formatting of numbers.

Logging information can be shown in the console, like
a print statement. It can also be redirected to a file
or over a network, or to multiple locations.

We will only work with the basic logging functionality
in Python. The basic settings are usually enough for
most situations.

@author: lee
"""

#%% imports
import re
import logging

#%% set up logging
FORMAT = "[%(asctime)s %(filename)s:%(lineno)s %(funcName)s] %(levelname)s: %(message)s"
logging.getLogger()
logging.basicConfig(format=FORMAT, level=logging.info)

logging.debug('This is a debug message')
logging.info('this is an info message')
logging.warning('this is a warning message')
logging.error('this is an error message')
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
    # note for debugging! need to add %! # and add tests
    #logging.debug('testing username %s', row)
    username = re.search(r'<([ +%~])([\w]+)>', row)
    print('in get_user_name:', username.group(2))
    return username.group(2)



def get_chat_message(row):
    """
    Separate the text content from a message row

    Parameters
    ----------
    row : str
        row that contains a message.

    Returns
    -------
    Message that the user posted in the chat room.

    """

    text = re.split(r'> ', row)[1:]

    message = "> ".join(text)
    print('get_chat_message: chat_row= ', message)
    return message


#%% load data
def main():
    """ load and process data. """
    raw_log = ""
    with open('Logs/hackers.log', 'r+', errors='ignore') as f:
        raw_log = f.readlines()

    print('Data Successfully loaded')
    # create empty list to store chat records
    chat_rows = []

    # iterate through the rows.
    for row in raw_log[0:10]:
        print(row)
        if is_message(row):
            # print("row is message", row)
            username = get_user_name(row)
            print("row is message. Username is ", username)
            message = get_chat_message(row)
            print("message is:", message)
            chat_rows.append({'username': username, 'message': message})
        elif re.match(r'---', row[0:5]):
            print('Date Changed ', row)
            # print("row is log on", row)
        else:
            print('Row Type not found ')
            # print("row type not found:", row)

#%%
if __name__ == '__main__':
    main()
    print('Program Completed')



#%% lab
"""
Convert all print statements to logs, submit the log file (or screenshot of it)
"""

logging.debug(__name__)
