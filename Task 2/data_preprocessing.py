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
    # Load the data.
    return pd.read_excel(url)

    
def remove_missing_value(df):
    #Remove the rows which containing missing vales.
    return df.dropna(axis=0)

def transform(df):
    ordered_valuation = {'Never heard of it': 1,
                    'Willing to learn': 2,
                    'Basic understanding': 3,
                    'I can do this with very little guidance': 4,
                    'Skillful': 5,
                    'Can teach other': 6}

    for index, row in df.iterrows():
        for column in df:
            if column != 'Timestamp' and column != 'Employee':
                reviews = str(df.iloc[index][column]).split(',')
                sum_reviews = 0
                for review in reviews:
                    if review in ordered_valuation:
                        sum_reviews += ordered_valuation[review]
                df.at[index, column] = sum_reviews/len(reviews)
                
    for column in df:
        if column != 'Timestamp':
            df[column] = pd.to_numeric(df[column])
            
    return df