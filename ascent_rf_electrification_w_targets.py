# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:15:49 2024

@author: sweeneyiiid
"""

import pandas as pd
from random import random
from math import exp
import numpy as np

out_path_actuals = './main_annual_data_v2.csv'
out_path_targets = './target_data_v2.csv'

# =============================================================================
# STEP 1: set up targets, then actuals will be randomized based on them
# =============================================================================

#phases
phases = np.array(['COMESA',
                   'TDB',
                   'AO',
                   'BI',
                   'BW',
                   'CD',
                   'ET',
                   'KE',
                   'KM',
                   'LS',
                   'MG',
                   'MW',
                   'MZ',
                   'NA',
                   'RW',
                   'SO',
                   'SS',
                   'ST',
                   'SZ',
                   'TZ',
                   'UG',
                   'ZA',
                   'ZM'])

# targets (all except COMESA,TDB,BI,RW,SO,ST,TZ are made up to sum to 100M)
final_targets = np.array([5000000,  
                          6000000,
                          1200000,
                          900000,
                          5000000,
                          400000,
                          16000000,
                          18000000,
                          400000,
                          350000,
                          2000000,
                          1500000,
                          3000000,
                          1600000,
                          1880000,
                          1820000,
                          1207000,
                          43000,
                          700000,
                          4000000,
                          14000000,
                          12000000,
                          3000000])

#years in program 
start_year = 2024
end_year = 2030

# get baseline coeff to end up with final target after exponential growth
denom_for_cum_target = 1/(exp(0.5*(end_year-start_year)))

base_target_coeff = final_targets*denom_for_cum_target

#get baseline for constructing annual targets
target_dict = {}
for i in range(len(phases)):
    target_dict[phases[i]] = base_target_coeff[i]

#get target dataset
cum_data = []

#want to have a 0 starting point
for k in target_dict.keys():
    cum_data.append({'phase': k, 'year':(start_year-1), 'cumulative_target':0})

# actual years
for y in range(start_year, end_year+1):
    for k in target_dict.keys():
        cum_target = target_dict[k]*exp(0.5*(y-start_year))

        cum_data.append({'phase':k,'year':y, 'cumulative_target':cum_target})

target_df = pd.DataFrame(cum_data)


# get annual targets as diff of cumulative targets
target_df['people_target'] = target_df.groupby('phase')['cumulative_target'].diff().fillna(0)

#create date column from year column
target_df['date'] = pd.to_datetime(target_df['year'].astype(str) + '-12-31')

#round calculated values to whole numbers
target_df['people_target'] = target_df.people_target.round(0)
target_df['cumulative_target'] = target_df.cumulative_target.round(0)

target_df[['phase', 'date', 'people_target']].to_csv(out_path_targets, index=False)


# =============================================================================
# Simulate actual data
# =============================================================================

# create a baseline dict for simulating actuals
actual_base = {}
for k in phases:
    for y in range(start_year-1, end_year+1):
        
        actual_base[(k,y)] = target_df[(target_df.phase == k) & 
                                       (target_df.year == y)]['people_target'].values.item()

# Technology and demographic variables (MAKE SURE EACH SUMS to 1)
tech = {'Standalone solar':0.4, 
        'Mini-grid':0.2, 
        'Grid':0.3,
        'PUE':0.1}

cust_type = {'Residential':0.5, 
             'Commercial':0.2, 
             'Institutional':0.1, 
             'Unknown':0.2}

hh = {'Male':0.6, 'Female':0.3, 'Unknown':0.1}


# People vs. connections
people_per_conn = {}
for k in phases:
    people_per_conn[k] = 4 + 2*random()


# GENERATE DATA
main_row_list = []
for phase_k in phases:
    for year_k in range(start_year-1, end_year+1):
        for tech_k in tech.keys():
            for cust_k in cust_type.keys():
                for hh_k in hh.keys():
                
                    #number of people
                    n_people = round((0.5 +random()/2) * \
                                     actual_base[(phase_k, year_k)] * \
                                         tech[tech_k] * \
                                             cust_type[cust_k] * \
                                                 hh[hh_k])
                    
                    #number of connections
                    n_conn = round(n_people / people_per_conn[phase_k])
                    
                    #create row
                    main_row_list.append({'phase':phase_k,
                                          'year':year_k,
                                          'technology':tech_k,
                                          'customer_type':cust_k,
                                          'hh_gender':hh_k,
                                          'n_connections':n_conn,
                                          'n_people':n_people})

# print to CSV                    
main_df = pd.DataFrame(main_row_list)

main_df['date'] = pd.to_datetime(main_df['year'].astype(str) + '-12-31')

main_df.to_csv(out_path_actuals, index=False)











