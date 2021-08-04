# -*- coding: utf-8 -*-
"""
THE BAD NEWS:
    This code runs but is ugly af and doesn't actually give correct results
    most of the time. 

THE GOOD NEWS:
    Fixing this code will give you a lot of the information needed to 
    solve 1.2 and 1.3 on homework 4. 


GUIDANCE:
    Follow this code review checklist:
        https://nyu-cds.github.io/effective-code-reviews/03-checklist/
    
    

@author: lee
"""

#%% imports

import re
import time
import logging
#%% set up logging
FORMAT = "[%(asctime)s %(filename)s:%(lineno)s %(funcName)s] %(levelname)s: %(message)s"
logging.getLogger()
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename="4-30debug.log")

logging.debug('Test Message')
logging.info('test message')
logging.warning('test message')
logging.error('oh no')
#%% Testing Data

join_quit_row_1 = '00:15 -!- _CyBruh_ [-Cybruh@AN-gm6.oj9.rj1tv4.IP] has quit [Quit: Leaving]'
join_quit_row_2 = '04:38 -!- gucci|bebe [guccibebe@errrrthang.guc.ci] has joined #hackers'
join_quit_row_3 = '10:06 -!- Whiskey-Tango-Down [Whiskey-Tan@she.wuz.ded.already.piig] has joined #hackers'
join_quit_row_4 = '10:49 -!- azorean [Mr.NoOne@AN-tga.mto.vlu2el.IP] has joined #hackers'

#%% Defining the function
# TODO add test for this function
# TODO figure out what function does
# TODO Add Docuumentation to this function
# TODO Rename Function and variables names
def p(row): 
    r = {} 

    if 'has joined' in row:   #Chech if a user joins
        r['status'] = "join" 
    elif "has quit" in row:  #Tells when the user has quit
        r['status'] = "quit"
    else:   #Anything else
        return 
    
        try:        
            r['user_name'] = re.search(r'- ([\[\w\]]+) ', row).group(1)
            user_string = re.search(r'\[([\w\d]+)@([\w\d\-.]+)\]', row) 
            r['user_id'] = user_string.group(1)
            r['address_id'] = user_string.group(2)
        except AttributeError:
            logging.error(row)
        except:
            logging.error(row)
            raise
            
        r['row_time'] = re.search('([0-9]{2}):([0-9]{2})', row[0:5])
        logging.debug('test')
        return(r)

def is_join_quit_row(row):
    """
Test if row is join quit(True or false)

    """
    
    
    
    return 


#%% Load Data

raw_log = ""
with open('Logs/hackers.log', 'r+', errors='ignore') as f:
    raw_log = f.readlines()
    

raw_log = raw_log[0:200]
#%% Search Through Rows    

i = 0
start = time.time()
while (i < len(raw_log)):  
   # raw_log[i] 
    logging.debug(raw_log[i])
    if re.match(r'---', raw_log[i][0:5]):   # chech is log is on row
        logging.debug("row is log on %s", raw_log[i])
    elif re.match(r' -!- ', raw_log[i][5:10]):   #Checking for join/ quit messages
        logging.debug('meta_row')
        meta_data = p(raw_log[i])
        logging.debug(meta_data)
        logging.debug('row %d username is %s', i, meta_data) 

        """
    elif re.match(r' <', row[5:10]):
        print(row)
        """
    else:
        pass
    i += 1 
    
logging.info('done, time (in seconds): %f', time.time() - start)
        