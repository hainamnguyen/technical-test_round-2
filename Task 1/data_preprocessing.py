# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 21:45:25 2017

@author: X1 Carbon
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

def load_data(url):
    #1. Load the data.
    df = pd.read_csv(url, index_col   = 'student_id')
    2#. Randomly shuffle the data.
    return shuffle(df)
    
def remove_missing_value(df):
    #Remove the rows which containing missing vales.
    return df.dropna(axis=0)

def corr(df):
    # Plot the correlation table between features.
    plt.imshow(df.corr(), cmap=plt.cm.Blues, interpolation='nearest')
    plt.colorbar()
    tick_marks = [i for i in range(len(df.columns))]
    plt.xticks(tick_marks, df.columns, rotation='vertical')
    plt.yticks(tick_marks, df.columns)
    plt.show()