# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#%% Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn import tree
from sklearn import ensemble
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
#%% data

hf = pd.read_csv('C:/Users/kyler/Documents/Code/Python/Digital-Forensics/Bfor 416/Data/heart_failure_clinical_records_dataset.csv')

#%% Peprocessing

print(hf.describe())

#%% Train / Test Split

np.random.seed(516)

# Creating Train and Test Model 

train, test = train_test_split(hf, test_size=0.25)
print("Rows in train:", len(train))
print("Rows in test:"), len(test)

#view some stats by different variables

train_stats=train.groupby('DEATH_EVENT')[['age','sex','diabetes']].agg(['mean','count'])
print("training data:\n", train_stats)
test_stats=test.groupby('DEATH_EVENT')[['age','sex','diabetes']].agg(['mean','count'])
print("Testing data:\n", test_stats)

pred_vars = ['age','sex','smoking','diabetes']

# decision tree
dtree=tree.DecisionTreeClassifier()
dtree.fit(train[pred_vars], train['DEATH_EVENT'])

#Random Forest
"""   random forest classifier consists of many decision trees with randomized parameters (hence the name). One of the parameters is the number of trees in the classifier   """
rf=ensemble.RandomForestClassifier()
rf.fit(train[pred_vars], train['DEATH_EVENT'])

#Neural Network
mlp=MLPClassifier()
mlp.fit(train[pred_vars],train['DEATH_EVENT'])

#Support Vector Machine
svc=svm.SVC(probability=True)
svc.fit(train[pred_vars], train['DEATH_EVENT'])

# Naive Bayes
nb = GaussianNB()
nb.fit(train[pred_vars], train['DEATH_EVENT'])

#logistic Regression
lr=LogisticRegression()
lr.fit(train[pred_vars], train['DEATH_EVENT'])

#Evaluation

#list of our models

fitted= [dtree, rf, mlp, svc, nb, lr]

#empty dataframe to store the results

result_table= pd.DataFrame(columns=(['classifier_name', 'fpr','tpr','auc', 'log_loss', 'clf_report']))

for clf in fitted:
    # print the name of the classifier
    print(clf.__class__.__name__)
    
    # get predictions
    yproba = clf.predict_proba(test[pred_vars])
    yclass = clf.predict(test[pred_vars])
    
    # auc information
    fpr, tpr, _ = metrics.roc_curve(test['DEATH_EVENT'],  yproba[:,1])
    auc = metrics.roc_auc_score(test['DEATH_EVENT'], yproba[:,1])
    
    # log loss
    log_loss = metrics.log_loss(test['DEATH_EVENT'], yproba[:,1])
    
    # add some other stats based on confusion matrix
    clf_report = metrics.classification_report(test['DEATH_EVENT'], yclass)
    
    # add the results to the dataframe
    result_table = result_table.append({'classifier_name':clf.__class__.__name__,
                                        'fpr':fpr, 
                                        'tpr':tpr, 
                                        'auc':auc,
                                        'log_loss': log_loss,
                                        'clf_report': clf_report}, ignore_index=True)

#%% View Results

result_table.set_index('classifier_name', inplace=True)
print(result_table)

for i in result_table.index:
    print('\n---- statistic for', i, "----\n")
    print(result_table.loc[i, 'clf_report'])
    print("Model log loss:", result_table.loc[i, 'log_loss'])


fig = plt.figure(figsize=(14,12))

for i in result_table.index:
    plt.plot(result_table.loc[i]['fpr'],
             result_table.loc[i]['fpr'],
             label="{}, AUC={:.3f}".format(i, result_table.loc[i]['auc']))
    
plt.plot([0,1], [0,1], color='orange', linestyle='--')

plt.xticks(np.arange(0.0, 1.1, step=0.1))
plt.xlabel("False Positive Rate", fontsize=15)

plt.yticks(np.arange(0.0, 1.1, step=0.1))
plt.ylabel("True Positive Rate", fontsize=15)

plt.title('ROC Curve Analysis', fontweight='bold', fontsize=15)
plt.legend(prop={'size':13}, loc='lower right')

plt.show()
