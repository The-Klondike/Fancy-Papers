# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:25:17 2020

@author: kyler
"""


#%%
import numpy as np
import pandas as pd
from matplotlib.pyplot import hist

#%%  randomly generates a matrix

matrix = np.random.randint(0, 100, size=(100, 4))
print(matrix)
print(matrix[90:100, 0])

#%%  date Frames
random_df = pd.DataFrame(matrix, columns=list('ABCD'))
random_df['A']
random_df['A'].plot.hist()

#%% add new column
# generate numbers from a random norman distribution 
# with a mean of 5 and a standard dev. of 2

new_col = np.random.normal(5, 2, size=100)

# add this as a new column
random_df['E'] = new_col
random_df['E'].plot.hist()

#%% add text column

labels = np.random.choice(['A_1', 'A_2', 'B_1', 'B_2'], size=100)
random_df['labels'] = labels

#show column lable

list(random_df)

#%% modift string

label_group = random_df['labels'].str.split('_')
print(label_group)
print(label_group.str[1])

random_df['group'] = label_group.str[0]


random_df.head()
random_df.tail()
#%% summerize the data

random_df.describe(include='all')
random_df.groupby('group').mean()
random_df.groupby('group')['C', 'D'].count()

summary_df = random_df.groupby('group').mean() 


#%% read mtcars

mtcars= pd.read_csv('mtcars.csv')
list(mtcars)
mtcars.describe(include='all')

#rename unnamed0 to car model
mtcars.rename(columns={'Unnamed: 0': 'Make_Model'}, inplace=True)

list(mtcars)


#%% todays lab

"""
with mtcars data 
summarize; show mean, mpg and horse power for each compant 
plot a histogram of veihicle weights (wt column)
*****
Extra credit- find and print the row for the vehicle with the highest weight
"""

#%%Todays lab

manu= mtcars['Make_Model'].str.split(" ")
print(manu)
print(manu.str[0])
mtcars['Manufactuer'] = manu.str[0]



mtcars.describe(include='all')
mtcars.groupby('Manufactuer')['mpg', 'hp'].mean()





