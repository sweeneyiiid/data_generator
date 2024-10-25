# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:15:49 2024

@author: sweeneyiiid
"""

# C:\Users\reeep\OneDrive\Desktop\wb_mpa\second_round\mock_data

import pandas as pd
from random import random
from math import exp
import numpy as np



in_path_targets = './input_targets_v3.csv'

out_path_actuals = './output_data/main_annual_data_v3.csv'
out_path_targets = './output_data/main_target_data_v3.csv'

out_cc_actuals = './output_data/cc_annual_data_v3.csv'
out_cc_targets = './output_data/cc_target_data_v3.csv'

out_he_actuals = './output_data/health_ed_annual_data_v3.csv'
out_he_targets = './output_data/health_ed_target_data_v3.csv'

out_capital_actuals = './output_data/capital_annual_data_v3.csv'
out_capital_targets = './output_data/capital_target_data_v3.csv'

out_ghg_actuals = './output_data/ghg_annual_data_v3.csv'
out_ghg_targets = './output_data/ghg_target_data_v3.csv'

out_combined_targets = './output_data/combined_target_data_v3.csv'


# =============================================================================
# FUNCTION to generate target curves from CSV with target totals
# =============================================================================

def annualize_targets(target_str,
                      in_path=in_path_targets,
                      start_year=2024,
                      end_year=2030):

    #load total targets from csv
    in_targets = pd.read_csv(in_path_targets, na_values=[], keep_default_na=False)

    #phases
    phases = np.array(in_targets["phase"])
    
    # people targets
    final_targets = np.array(in_targets[target_str])

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
    target_df[target_str + '_target'] = target_df.groupby('phase')['cumulative_target'].diff().fillna(0)
    
    #create date column from year column
    target_df['date'] = pd.to_datetime(target_df['year'].astype(str) + '-12-31')
    
    #round calculated values to whole numbers
    target_df[target_str + '_target'] = target_df[target_str + '_target'].round(0)
    target_df['cumulative_target'] = target_df.cumulative_target.round(0)
    
    return target_df


# =============================================================================
# FUNCTION to simulate actual data after targets are generated
# =============================================================================
def actual_given_targets(target_str,
                         target_df,
                         tech,
                         sub_tech,
                         cust_type,
                         sub_cust,
                         hh,
                         start_year=2024,
                         end_year=2030):

    phases = np.array(target_df.groupby("phase")[target_str + '_target'].sum().reset_index()["phase"])
    start_year = 2024
    end_year = 2030
    
    # create a baseline dict for simulating actuals
    actual_base = {}
    for k in phases:
        for y in range(start_year-1, end_year+1):
            
            actual_base[(k,y)] = target_df[(target_df.phase == k) & 
                                           (target_df.year == y)][target_str + '_target'].values.item()
    
    
    
    # People vs. connections: only apply to residential
    people_per_conn = {}
    for k in phases:
        people_per_conn[k] = 4 + 2*random()
    
    
    # GENERATE DATA
    main_row_list = []
    for phase_k in phases:
        for year_k in range(start_year-1, end_year+1):
            for tech_k in tech.keys():
                for st_k in sub_tech[tech_k].keys():
                    for cust_k in cust_type.keys():
                        for sc_k in sub_cust[cust_k].keys():
                            for hh_k in hh.keys():
                            
                                # number of people:
                                # for each set of parameters, will be
                                # between 0.5 and 1.0 of their expected
                                # contribution to target
                                n_people = round((0.5 +random()/2) * \
                                                 actual_base[(phase_k, year_k)] * \
                                                     tech[tech_k] * \
                                                         sub_tech[tech_k][st_k] * \
                                                             cust_type[cust_k] * \
                                                                 sub_cust[cust_k][sc_k] * \
                                                                 hh[hh_k])
                                
                                #number of connections
                                #
                                if cust_k in ('Residential', 'Unknown'):
                                    n_conn = round(n_people / people_per_conn[phase_k])
                                else:
                                    n_conn = n_people
                                
                                #create row
                                main_row_list.append({'phase':phase_k,
                                                      'year':year_k,
                                                      'technology':tech_k,
                                                      'sub_technology':st_k,
                                                      'customer_type':cust_k,
                                                      'customer_sub_type': sc_k,
                                                      'hh_gender':hh_k,
                                                      'n_connections':n_conn,
                                                      'n_'+target_str:n_people})
    main_df = pd.DataFrame(main_row_list)
    main_df['date'] = pd.to_datetime(main_df['year'].astype(str) + '-12-31')
    
    return main_df    

# =============================================================================
# get PEOPLE and CONNECTIONS
# =============================================================================

# targets --------------------------------------------------------------------

target_str = 'people'

target_df = annualize_targets(target_str)

# print to csv
main_target_df = target_df[['phase', 'date', target_str + '_target']].copy()
main_target_df.to_csv(out_path_targets, index=False)

# actuals ------------------------------------------------------------------

# Technology and demographic variables (MAKE SURE EACH SUMS to 1)
tech = {'Solar Energy Kit':0.4, 
        'Mini-grid':0.2, 
        'Grid':0.3,
        'PUE':0.1}

cust_type = {'Residential':0.5, 
             'Commercial':0.2, 
             'Institutional':0.1, 
             'Unknown':0.2}

hh = {'Male':0.6, 'Female':0.3, 'Unknown':0.1}

sub_tech = {'Solar Energy Kit':{'Solar Energy Kit':1.0}, 
            'Mini-grid':{'Mini-grid':1.0}, 
            'Grid':{'Grid':1.0},
            'PUE':{'PUE':1.0}}

sub_cust = {'Residential':{'Residential':1.0}, 
             'Commercial':{'Commercial':1.0}, 
             'Institutional':{'Education':0.7, 'Health':0.3}, 
             'Unknown':{'Unknown':1.0}}

main_df = actual_given_targets(target_str,
                         target_df,
                         tech,
                         sub_tech,
                         cust_type,
                         sub_cust,
                         hh)

#print to CSV
main_df.to_csv(out_path_actuals, index=False)


# =============================================================================
# Clean Cooking
# - for now assuming all cooking is residential and people per system
#   is the same as people per connection
# - if what target is really systems sold, then drop connections column
# - sub techs: Biogas, Electric, Ethanol, ICS, LPG
# =============================================================================


# targets --------------------------------------------------------------------

target_str = 'cooking'

target_df = annualize_targets(target_str)

# print to csv
cc_target_df = target_df[['phase', 'date', target_str + '_target']].copy()
cc_target_df.to_csv(out_cc_targets, index=False)

# actuals ------------------------------------------------------------------

# Technology and demographic variables (MAKE SURE EACH SUMS to 1)
tech = {'Clean Cooking':1.0}

cust_type = {'Residential':1.0}

hh = {'Male':0.2, 'Female':0.7, 'Unknown':0.1}

sub_tech = {'Clean Cooking':{'Biogas':0.2,
                             'Electric':0.2,
                             'Ethanol':0.1,
                             'ICS':0.4,
                             'LPG':0.1}}

sub_cust = {'Residential':{'Residential':1.0}}

main_df = actual_given_targets(target_str,
                         target_df,
                         tech,
                         sub_tech,
                         cust_type,
                         sub_cust,
                         hh)

#print to CSV
main_df.to_csv(out_cc_actuals, index=False)



# =============================================================================
# Finance
# - use capital for targets
# - for actuals, maybe change n_people to USD (drop connections)
# =============================================================================

# targets --------------------------------------------------------------------

target_str = 'capital'

target_df = annualize_targets(target_str)

# print to csv
capital_target_df = target_df[['phase', 'date', target_str + '_target']].copy()
capital_target_df.to_csv(out_capital_targets, index=False)

# actuals ------------------------------------------------------------------

# Technology and demographic variables (MAKE SURE EACH SUMS to 1)
tech = {'Solar Energy Kit':0.3, 
        'Mini-grid':0.4, 
        'PUE':0.1,
        'Clean Cooking':0.2}

cust_type ={'dummy':1.0}

hh = {'dummy':1.0}

sub_tech = {'Solar Energy Kit':{'Solar Energy Kit':1.0}, 
            'Mini-grid':{'Mini-grid':1.0}, 
            'PUE':{'PUE':1.0},
            'Clean Cooking':{'Clean Cooking':1.0}}

sub_cust = {'dummy':{'dummy':1.0}}

main_df = actual_given_targets(target_str,
                         target_df,
                         tech,
                         sub_tech,
                         cust_type,
                         sub_cust,
                         hh)

#print to CSV
main_df.drop(labels='n_connections', axis=1, inplace=True)
main_df.to_csv(out_capital_actuals, index=False)

# =============================================================================
# CO2
# - use ghg for targets
# - for actuals, maybe change n_people to tons_co2 (drop connections)
# - for categories, maybe drop "grid" and add "clean cooking"
# =============================================================================

# targets --------------------------------------------------------------------

target_str = 'ghg'

target_df = annualize_targets(target_str)

# print to csv
ghg_target_df = target_df[['phase', 'date', target_str + '_target']].copy()
ghg_target_df.to_csv(out_ghg_targets, index=False)


# actuals ------------------------------------------------------------------


# Technology and demographic variables (MAKE SURE EACH SUMS to 1)
tech = {'Solar Energy Kit':0.1, 
        'Mini-grid':0.4, 
        'PUE':0.1,
        'Clean Cooking':0.4}

cust_type ={'dummy':1.0}

hh = {'dummy':1.0}

sub_tech = {'Solar Energy Kit':{'Solar Energy Kit':1.0}, 
            'Mini-grid':{'Solar':0.7, 'Hybrid':0.3}, 
            'PUE':{'PUE':1.0},
            'Clean Cooking':{'Biogas':0.1,
                             'Electric':0.5,
                             'Ethanol':0.1,
                             'ICS':0.2,
                             'LPG':0.1}}

sub_cust = {'dummy':{'dummy':1.0}}

main_df = actual_given_targets(target_str,
                         target_df,
                         tech,
                         sub_tech,
                         cust_type,
                         sub_cust,
                         hh)

#print to CSV
main_df.drop(labels='n_connections', axis=1, inplace=True)
main_df.to_csv(out_ghg_actuals, index=False)


# =============================================================================
# COMBINE TARGETS
# =============================================================================

combined_target_df = main_target_df.merge(cc_target_df, on=['phase','date'])
combined_target_df = combined_target_df.merge(capital_target_df, on=['phase','date'])
combined_target_df = combined_target_df.merge(ghg_target_df, on=['phase','date'])

# for now, health and ed is just gonna be a subset of people
# - note: in dashboard just filter results to institution only
combined_target_df["health_ed_target"] = combined_target_df.people_target / 10.0

combined_target_df["health_ed_target"] = combined_target_df.health_ed_target.round(0)

combined_target_df.to_csv(out_combined_targets, index=False)





