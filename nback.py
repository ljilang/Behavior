#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 10:25:18 2021

@author: Lara
"""

########
##
# Analysis of fMRI n-back performance 
## 
########

####_________________
# Import modules     \_______________________________________________________________
####

import pandas as pd
import numpy as np
from scipy import stats

####_________________
# Import data & prep \_______________________________________________________________
####

nback = pd.read_excel('nback.xlsx', sheet_name='Blad2')

# Create Group column based on Subject ID values
conditions = [
    (nback['SubjectID'] < 100),
    (nback['SubjectID'] >= 100) & (nback['SubjectID'] < 200),
    (nback['SubjectID'] >= 200) & (nback['SubjectID'] < 300),
    (nback['SubjectID'] >= 300)
]

values = ['HC', 'd1', 'd2', 'd3']
nback['Group'] = np.select(conditions, values)
print(nback)

####_________________
# Get sum scores     \_______________________________________________________________

# Create new data frame with 4 columns: 1) number of correct responses to target stimuli and 2) number of correct responses to non target stimuli per subject and nback condition (skipping 0-back))

# Create variable with all unique subject IDs
unique_IDs = nback['SubjectID'].unique()

# 1-BACK
# For target stimuli 
Oneback_target_sum_scores = []
for subj in unique_IDs:
    df_single_subj = nback[nback['SubjectID']==subj]
    #print(subj, df_single_subj.query('NBacks==2')['Target.ACC'].sum())
    oneback_target = df_single_subj.query('NBacks==2')['Target.ACC'].sum()
    Oneback_target_sum_scores.append(oneback_target)
    
# For non-target stimuli
Oneback_nontarget_sum_scores = []
for subj in unique_IDs:
    df_single_subj = nback[nback['SubjectID']==subj]
    #print(df_single_subj.query('NBacks==2')['NonTarget.ACC'].sum())
    oneback_nontarget = df_single_subj.query('NBacks==2')['NonTarget.ACC'].sum()
    Oneback_nontarget_sum_scores.append(oneback_nontarget)
    
# 2-BACK
# For target stimuli 
Twoback_target_sum_scores = []
for subj in unique_IDs:
    df_single_subj = nback[nback['SubjectID']==subj]
    #print(df_single_subj.query('NBacks==3')['Target.ACC'].sum())
    twoback_target = df_single_subj.query('NBacks==3')['Target.ACC'].sum()
    Twoback_target_sum_scores.append(twoback_target)
    
# For non-target stimuli 
Twoback_nontarget_sum_scores = []
for subj in unique_IDs:
    df_single_subj = nback[nback['SubjectID']==subj]
    #print(df_single_subj.query('NBacks==3')['NonTarget.ACC'].sum())
    twoback_nontarget = df_single_subj.query('NBacks==3')['NonTarget.ACC'].sum()
    Twoback_nontarget_sum_scores.append(twoback_nontarget)
    
# Combine the above into a dataframe
all_sum_scores = pd.DataFrame(
    {'Subject_IDs': unique_IDs,
     '1_back_target': Oneback_target_sum_scores,
     '1_back_nontarget': Oneback_nontarget_sum_scores,
     '2_back_target': Twoback_target_sum_scores,
     '2_back_nontarget': Twoback_nontarget_sum_scores
    })

# Add Group column to above data frame
# Start by getting the group column from original data frame and getting rid of duplicates 
labels = nback[['SubjectID', 'Group']]
labels_uniq = labels[~labels.duplicated()]
# Merge the two data frames
all_sum_scores = all_sum_scores.merge(labels_uniq, left_on='Subject_IDs', right_on='SubjectID')

####_________________
# Compare groups     \_______________________________________________________________

# Subset the data 
SLE = all_sum_scores.loc[all_sum_scores['Group'] == 'd1']
HC = all_sum_scores.loc[all_sum_scores['Group'] == 'HC']

# Compare group means of SLE and HC for the different conditions
stats.ttest_ind(SLE['1_back_target'], HC['1_back_target']) 
stats.ttest_ind(SLE['1_back_nontarget'], HC['1_back_nontarget']) 
stats.ttest_ind(SLE['2_back_target'], HC['2_back_target']) 
stats.ttest_ind(SLE['2_back_nontarget'], HC['2_back_nontarget'])

    
####_________________
# Export results     \_______________________________________________________________

nback.to_excel('nback_output.xlsx', index=None)
