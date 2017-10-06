# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 21:45:25 2017

@author: X1 Carbon
"""
import pandas as pd
import numpy as np

def matching_skills(project_skills, dataset_skills):
    matched_skills = []
    for i in dataset_skills:
        for j in project_skills:
            if j in i:
                matched_skills += [i]
                
    return matched_skills

def similarity_func(capacity_requirements, employees_skills):
    evaluated_result = []
    for i in employees_skills:
        result = 0
        for j in range(len(i[1])):
            result += capacity_requirements[j] * (i[1][j] - capacity_requirements[j] + 1)
        evaluated_result.append([i[0], i[1], result])
        
    return evaluated_result

def best_of_k_list(evaluated_result, k):
    evaluated_result.sort(key = lambda x: x[2], reverse = True)
    
    return evaluated_result[:k]