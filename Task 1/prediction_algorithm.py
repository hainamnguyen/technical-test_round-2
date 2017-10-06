# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 21:57:36 2017

@author: X1 Carbon
"""
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

def prepare_data(data):
    #1. Try to change some features from categorical to norminal.
    data.is_copy = False
    data['objective'] = data.objective.astype("category").cat.codes
    data['test_id'] = data.test_id.astype("category").cat.codes
    
    #2. Split the data into 2 sets: Training set and test set.
    y = data.pass_test
    X = data.drop(labels = 'pass_test', axis = 1)
    
    return  train_test_split(X, y, test_size=0.3)

def prediction_model(X_train, y_train):
    #Use the decision tree algorithm to build a model to predict the Pass/Fail of the student. 
    model = tree.DecisionTreeClassifier(criterion = 'entropy')
    
    return model.fit(X_train, y_train)

def prediction_result(model, X_test, y_test):
    # Exam the model by using test set.
    y_result = model.predict(X_test)
    print('f1 score: ', f1_score(y_test, y_result))
    print('Accuracy score:', sum(y_result == y_test)/len(y_test))
