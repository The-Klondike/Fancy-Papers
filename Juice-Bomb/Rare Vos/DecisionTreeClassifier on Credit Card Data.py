# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 19:39:06 2020

@author: kyler
"""
#%% Imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn import tree
from sklearn import metrics
#%% Data 

ccfraud = pd.read_csv('C:/Users/kyler/Digital Forensics/Bfor 416/Data/creditcard.csv')
ccfraud.describe()

ccstats = ccfraud.groupby('Class')['Amount'].agg(['mean','count'])

print("Fraudulent transaction ratio:", ccstats.loc[1, 'count']/ccstats['count'].sum())

#%% Training and testing the data 
np.random.seed(516)

train, test = train_test_split(ccfraud, test_size=0.25)

print("Rows in train:", len(train))
print("Rows in Test:", len(test))

train_stats=train.groupby('Class')['Amount'].agg(['mean', 'count'])
print("Training data:\n", train_stats)

test_stats=test.groupby('Class')['Amount'].agg(['mean', 'count'])
print("Training data:\n", test_stats)


#%% Train the model

print(list(ccfraud.columns))

pred_vars = ['Time', 'Amount', 'V8','V1']
print(ccfraud.loc[:, pred_vars])

dtree = tree.DecisionTreeClassifier(criterion="entropy")

dtree.fit(train.loc[:, pred_vars], train['Class'])

print(dtree.get_n_leaves())

print(dtree.get_depth())

#%% Evaluating the performance 

pred_labels = dtree.predict(test.loc[:, pred_vars])
pred_labels[0:4]

metrics.plot_confusion_matrix(dtree, test.loc[:, pred_vars], test['Class'])

print(metrics.classification_report(test['Class'], pred_labels, digits=5))

#%% Probabilistic Evaluation

pred_probs = dtree.predict_proba(test.loc[:, pred_vars])
pred_probs[0:5, :]


#%% Area Under The Curve

metrics.roc_auc_score(test['Class'], pred_probs[:,1])

metrics.plot_roc_curve(dtree, test.loc[:, pred_vars], test['Class'])

metrics.average_precision_score(test['Class'], pred_probs[:,1])

metrics.plot_precision_recall_curve(dtree, test.loc[:, pred_vars], test['Class'])

#%% Log Loss

print(metrics.log_loss(test['Class'], pred_probs[:,1]))
