# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%% Imports
import numpy as np
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import vader
    
#%%
debates = pd.read_csv('/home/kyle-a/School/Spitzley/BFOR 416-516/data/all_debates.csv', index_col=0)
debates.reset_index(inplace=True, drop=True)

# drop rows with names of speakers
exclude_list = ['PARTICIPANTS', 'MODERATORS']
debates = debates[~debates['speaker'].isin(exclude_list)]

# add column for debate year
debates['year'] = pd.DatetimeIndex(debates['date']).year

#%% Basic Descriptive stats
debate_counts = debates.groupby(['speaker']).count().sort_values(by='debate', ascending=False)
debate_counts['debate'].head(15).plot.bar()


#%% Sentiment analysis
vader_analyzer = vader.SentimentIntensityAnalyzer()

omalley = debates.loc[41, 'text']
print(omalley)
vader_analyzer.polarity_scores(omalley)


#%% Bernie
bernie =  debates.loc[140, 'text']
print(bernie)
vader_analyzer.polarity_scores(bernie)

#%% Clinton
clinton = debates.loc[153, 'text']
print(clinton)
vader_analyzer.polarity_scores(clinton)


#%% COmpute Sentiment for all utterances 
vader_analyzer = vader.SentimentIntensityAnalyzer()
results = debates['text'].apply(vader_analyzer.polarity_scores)

results_df = pd.DataFrame(list(results))

sent_df = pd.concat([debates, results_df.reindex(debates.index)], axis=1)


#%% Summarizing the dataframe
sent_df['turn'].corr(sent_df['compound'])

speaker_summary = sent_df.groupby(['speaker']).agg(['mean', 'count'])

print(speaker_summary['compound'][['mean', 'count']].sort_values(by='count', ascending=False).head(15))

#%%Classification

# list candidates from 2008 - 2020 (2012 is missing)
presidential_candidates = ['MCCAIN', 'OBAMA', 'CLINTON', 'TRUMP']
winners = ['OBAMA', 'TRUMP']

# subset winners
presidential = sent_df[(debates['party'] == 'P') & 
                       (debates['speaker'].isin(presidential_candidates)) &
                       (debates['date'] < '2020')]

# get average sentiment
pres_summary = presidential.groupby(['year', 'speaker'], as_index=False)[['compound', 'neg', 'pos', 'neu']].mean()

# label results
pres_summary['win'] = np.where(pres_summary[ 'speaker'].isin(winners), 'win', 'lose')
print(pres_summary)

from sklearn import tree

dtree = tree.DecisionTreeClassifier(max_depth=(1),splitter="random")

pred_vars = ['compound', 'neg', 'pos', 'neu']
dtree.fit(pres_summary[pred_vars], pres_summary['win'])
tree.plot_tree(dtree)


#%% Predictions
this_year = sent_df[(debates['party'] == 'P') & 
                    (debates['speaker'].isin(presidential_candidates)) &
                    (debates['date'] > '2020')]
this_summary = this_year.groupby(['year', 'speaker'], as_index=False)[['compound', 'neg', 'pos', 'neu']].mean()

# get predictions
this_summary['p_win'] = dtree.predict(this_summary[pred_vars])
display(this_summary)


#%% Exercise 
"""

    Which candidate had the greatest percent of extreme positive turns-at-talk (compound score > 0.5)?
    
    The decision tree above could simulataneously predict a win for both candidates. 
    How could you reshape the data to prevent this?
    
    With text analysis, the variables that you can construct are only limited by your imagination. 
    Try computing the word counts for each candidate (see this) or compute the variance in sentiment using .var() to 
    summarize rather than .mean(). How does it change the models?

    1. Trump had the lower compund score of .02497 compared to bidens compund score of .48370. Trump is given the win under this 
    currently model
    2. 

    

 """