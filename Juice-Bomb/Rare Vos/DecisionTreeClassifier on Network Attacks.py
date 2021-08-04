#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 01:55:28 2020

@author: kyle-a
"""
#%%imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import metrics

#%%
# https://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html
names= pd.read_csv('/home/kyle-a/School/BFOR 416-516/data/kddcup.names.txt', header=None, delimiter=(':'), skiprows=(1))

name_list = names[0].tolist()

name_list.append('type')

#%% read the main dataframe
netattacks = pd.read_csv('/home/kyle-a/School/BFOR 416-516/data/kddcup.data.corrected', names=name_list, header=None, index_col=(None))

netattacks['label'] = np.where(netattacks['type']=='normal.', 'good', 'bad')

#%% segment the data

train, test = train_test_split(netattacks, test_size=0.25)
print("rows in Train:", len(train))
print("rows in Test:", len(test))

#%% Train the model
dt = tree.DecisionTreeClassifier(random_state=(10),criterion=("entropy"),splitter="random")

dt.fit(train.iloc[:, 22:23], train['label'])

#%% Predict labels for test

predicted = dt.predict(test.iloc[:, 22:23])
print(predicted[:5])

from collections import Counter
test_labels_stats = Counter(test['label'])
print("Labels in the test data:", test_labels_stats)

predicted_labels_stats = Counter(predicted)
print("Labels in the predictions:", predicted_labels_stats)

#%% Model stats

metrics.confusion_matrix(y_true=test['label'], y_pred=predicted, labels=['good','bad'])

metrics.plot_confusion_matrix(dt, test.iloc[:, 22:23], test['label'], labels=['good','bad'])

#%% Accuracy

baseline = test_labels_stats['bad'] / (test_labels_stats['good'] + test_labels_stats['bad'])
print("baseline accuracy is:", baseline)

acc = metrics.accuracy_score(test['label'], predicted)
print("observed accuracy is:", acc)

result = metrics.classification_report(test['label'], predicted, digits=4)
print(result)
