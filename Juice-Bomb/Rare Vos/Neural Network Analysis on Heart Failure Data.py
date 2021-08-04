# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 16:46:33 2020

@author: kyler
"""

#%% Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.model_selection import (KFold, ShuffleSplit,
                                     StratifiedKFold, 
                                     StratifiedShuffleSplit)

from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
#%% data

hf = pd.read_csv('C:/Users/kyler/Documents/Code/Python/Digital-Forensics/Bfor 416/Data/heart_failure_clinical_records_dataset.csv')

#%% Prediction Variables

pred_vars = ['age', 'sex', 'smoking', 'diabetes', 'serum_creatinine', 'ejection_fraction']

#%% Visualizing Cross Validation



def visualize_groups(classes):
    # Visualize dataset groups
    cmap_data = plt.cm.Paired
    fig, ax = plt.subplots()
    ax.scatter(range(len(classes)),  [2] * len(classes), c=classes, marker='_',
               lw=50, cmap=cmap_data)
    ax.set(ylim=[-1, 5], yticks=[2],
           yticklabels=['Data\nclass'], xlabel="Sample index")


visualize_groups(hf['DEATH_EVENT'])

def plot_cv_indices(cv, X, y, ax, n_splits, lw=10):
    """Create a sample plot for indices of a cross-validation object."""
    cmap_data = plt.cm.Paired
    cmap_cv = plt.cm.coolwarm
    # Generate the training/testing visualizations for each CV split
    for ii, (tr, tt) in enumerate(cv.split(X=X, y=y)):
        # Fill in indices with the training/test groups
        #print(ii)
        #print(tt, tr)
        indices = np.array([np.nan] * len(X))
        indices[tt] = 1
        indices[tr] = 0
        #print(indices)
        # Visualize the results
        ax.scatter(range(len(indices)), [ii + .5] * len(indices),
                   c=indices, marker='_', lw=lw, cmap=cmap_cv,
                   vmin=-.2, vmax=1.2)

    # Plot the data classes and groups at the end
    ax.scatter(range(len(X)), [ii + 1.5] * len(X),
               c=y, marker='_', lw=lw, cmap=cmap_data)



    # Formatting
    yticklabels = list(range(n_splits)) + ['class']
    ax.set(yticks=np.arange(n_splits+1) + .5, yticklabels=yticklabels,
           xlabel='Sample index', ylabel="CV iteration",
           ylim=[n_splits+1.2, -.2], xlim=[0, len(y)])
    ax.set_title('{}'.format(type(cv).__name__), fontsize=15)
    
    ax.legend([Patch(color=cmap_cv(.8)), Patch(color=cmap_cv(.02))],
          ['Testing set', 'Training set'], loc=(1.02, .8))
    # Make the legend fit
    plt.tight_layout()
    fig.subplots_adjust(right=.7)
    
    return ax

#%% Simple k-fold subsetting

# define number of folds
n_splits = 5

# create empty plot
fig, ax = plt.subplots()
# get subset folds
cv = KFold(n_splits)
# call plot function
plot_cv_indices(cv, hf[pred_vars], hf['DEATH_EVENT'], ax, n_splits)

#%% Randomized K-Fold

fig, ax = plt.subplots()
cv = ShuffleSplit(n_splits)
plot_cv_indices(cv, hf[pred_vars], hf['DEATH_EVENT'], ax, n_splits)

#%%Stratified k-fold without randomization

fig, ax = plt.subplots()
cv = StratifiedKFold(n_splits)
plot_cv_indices(cv, hf[pred_vars], hf['DEATH_EVENT'], ax, n_splits)

#%% Stratified with randomization

# stratified with randomization
fig, ax = plt.subplots()
cv = StratifiedShuffleSplit(n_splits)
plot_cv_indices(cv, hf[pred_vars], hf['DEATH_EVENT'], ax, n_splits)

#%% Create train and test sets

np.random.seed(516)

# create train and test
train, test = train_test_split(hf, test_size=0.20, stratify=hf['DEATH_EVENT'])
print("Rows in train:", len(train))
print("Rows in test:", len(test))

# view some stats by different variables
train_stats = train.groupby('DEATH_EVENT')[['age', 'sex', 'diabetes']].agg(['mean', 'count'])
print("Training data:\n", train_stats)
test_stats = test.groupby('DEATH_EVENT')[['age', 'sex', 'diabetes']].agg(['mean', 'count'])
print("Testing data:\n", test_stats)

#%% and view results

scoring = ['accuracy', 'neg_log_loss', 'f1', 'roc_auc']
rf_base = RandomForestClassifier()
cv_rf = cross_validate(rf_base, train[pred_vars], train['DEATH_EVENT'], cv=StratifiedShuffleSplit(n_splits), scoring=scoring)
print(cv_rf)

# view a single statistic over the models
print(cv_rf['test_roc_auc'])
print("mean model AUC", np.mean(cv_rf['test_roc_auc']))

print(cv_rf['test_neg_log_loss'])
# note that this uses negative log loss (log loss * (-1)), meaning that 
# higher values (those closer to 0) are better.
print("mean model log loss ", np.mean(cv_rf['test_neg_log_loss']))

#%% Tuning the model

params = {'criterion': ['gini', 'entropy'], 'max_depth': [5, 10, 15, None]}

rf_base = RandomForestClassifier()
rf_tuned = GridSearchCV(rf_base, param_grid=params, cv=StratifiedShuffleSplit(n_splits), scoring='roc_auc')
rf_tuned.fit(train[pred_vars], train['DEATH_EVENT'])

print(rf_tuned.cv_results_)

print(rf_tuned.cv_results_['mean_test_score'])
print(rf_tuned.cv_results_['mean_test_score'].mean())

# viewing the setting that provided the best results 

print(rf_tuned.best_estimator_)

#%% Trtaining a Neural Network

import warnings
warnings.filterwarnings('ignore')

nnet_base = MLPClassifier()

params = {'hidden_layer_sizes': [(100,), (10,10), (5,5,5)], 
          'solver': ['adam', 'lbfgs', 'sgd']}
# 9 different param combos, 5 cv = total of 45 models
# try with differnt scoring methods
# we get different results with accuracy & log_loss
nnet_tuned = GridSearchCV(nnet_base, param_grid=params, cv=StratifiedShuffleSplit(n_splits), scoring='roc_auc')
nnet_tuned.fit(train[pred_vars], train['DEATH_EVENT'])
# nnet_tuned.get_params()
print(nnet_tuned.cv_results_)

print(nnet_tuned.cv_results_['mean_test_score'])

print(nnet_tuned.best_estimator_)

#%% Evaulation
fitted = [rf_tuned, nnet_tuned]

result_table = pd.DataFrame(columns=['classifier_name', 'fpr','tpr','auc', 
                                     'log_loss', 'clf_report'])

for clf in fitted:
    print(clf.estimator)
    yproba = clf.predict_proba(test[pred_vars])
    yclass = clf.predict(test[pred_vars])
    
    # auc information
    fpr, tpr, _ = metrics.roc_curve(test['DEATH_EVENT'],  yproba[:,1])
    auc = metrics.roc_auc_score(test['DEATH_EVENT'], yproba[:,1])
    
    # log loss
    log_loss = metrics.log_loss(test['DEATH_EVENT'], yproba[:,1])
    
    # add some other stats based on confusion matrix
    clf_report = metrics.classification_report(test['DEATH_EVENT'], yclass)
    
    
    result_table = result_table.append({'classifier_name':str(clf.estimator),
                                        'fpr':fpr, 
                                        'tpr':tpr, 
                                        'auc':auc,
                                        'log_loss': log_loss,
                                        'clf_report': clf_report}, ignore_index=True)
    


result_table.set_index('classifier_name', inplace=True)
print(result_table)




fig = plt.figure(figsize=(14,12))

for i in result_table.index:
    plt.plot(result_table.loc[i]['fpr'], 
             result_table.loc[i]['tpr'], 
             label="{}, AUC={:.3f}".format(i, result_table.loc[i]['auc']))
    
plt.plot([0,1], [0,1], color='orange', linestyle='--')

plt.xticks(np.arange(0.0, 1.1, step=0.1))
plt.xlabel("False Positive Rate", fontsize=15)

plt.yticks(np.arange(0.0, 1.1, step=0.1))
plt.ylabel("True Positive Rate", fontsize=15)

plt.title('ROC Curve Analysis', fontweight='bold', fontsize=15)
plt.legend(prop={'size':13}, loc='lower right')

plt.show()

#%% exercise 

from sklearn import svm
# Simple Vector Machine
svc = svm.SVC(probability=True, break_ties=True, kernel=('poly'))
svc.fit(train[pred_vars], train['DEATH_EVENT'])

from sklearn import tree
# decision tree
dtree=tree.DecisionTreeClassifier(splitter="random", max_features=("log2") )
dtree.fit(train[pred_vars], train['DEATH_EVENT'])

from sklearn.linear_model import LogisticRegression
lr=LogisticRegression(dual=(False),penalty='none',tol= 1e-6 )
lr.fit(train[pred_vars], train['DEATH_EVENT'])

fitted_exercise = [dtree, svc, lr, rf_tuned, nnet_tuned]
result_table_fitted = pd.DataFrame(columns=['classifier_name', 'fpr','tpr','auc', 
                                     'log_loss', 'clf_report'])

for clf in fitted_exercise:
    print(clf.__class__.__name__)
    yproba = clf.predict_proba(test[pred_vars])
    yclass = clf.predict(test[pred_vars])
    
    # auc information
    fpr, tpr, _ = metrics.roc_curve(test['DEATH_EVENT'],  yproba[:,1])
    auc = metrics.roc_auc_score(test['DEATH_EVENT'], yproba[:,1])
    
    # log loss
    log_loss = metrics.log_loss(test['DEATH_EVENT'], yproba[:,1])
    
    # add some other stats based on confusion matrix
    clf_report = metrics.classification_report(test['DEATH_EVENT'], yclass)
    
    
    result_table_fitted = result_table_fitted.append({'classifier_name': clf.__class__.__name__,
                                        'fpr':fpr, 
                                        'tpr':tpr, 
                                        'auc':auc,
                                        'log_loss': log_loss,
                                        'clf_report': clf_report}, ignore_index=True)
    


result_table_fitted.set_index('classifier_name', inplace=True)
print(result_table_fitted)




fig = plt.figure(figsize=(14,12))

for i in result_table_fitted.index:
    plt.plot(result_table_fitted.loc[i]['fpr'], 
             result_table_fitted.loc[i]['tpr'], 
             label="{}, AUC={:.3f}".format(i, result_table_fitted.loc['auc']))
    
plt.plot([0,1], [0,1], color='orange', linestyle='--')

plt.xticks(np.arange(0.0, 1.1, step=0.1))
plt.xlabel("False Positive Rate", fontsize=15)

plt.yticks(np.arange(0.0, 1.1, step=0.1))
plt.ylabel("True Positive Rate", fontsize=15)

plt.title('ROC Curve Analysis', fontweight='bold', fontsize=15)
plt.legend(prop={'size':13}, loc='lower right')

plt.show()
