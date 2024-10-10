# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:15:49 2024

@author: sweeneyiiid
"""

import pandas as pd
from random import random
from math import exp


out_path = './main_annual_data.csv'

BASE_NUM = 80000000

phase = ['COMESA', 'TDB', None] # None would mean country specific phase

country = {'BI':0.25,
           'RW':0.2,
           'ST':0.1,
           'SO':0.3,
           'TZ':0.15}

region = {'BI':[a,b,d]}

tech = {'Stand Alone Solar':0.5, 
        'Mini Grid':0.2, 
        'Grid Extenstion':0.1,
        'PUE':0.1,
        'CC':0.1}

cust_type = {'Residential':0.5, 
             'Commercial':0.2, 
             'Institutional':0.1, 
             'Unknown':0.2}

hh = {'Male':0.6, 'Female':0.3, 'Unknown':0.1}

years = {2023:0.1, 
         2024:0.2,
         2025:0.3,
         2026:0.4, 
         2027:0.5,
         2028:0.6,
         2029:0.7,
         2030:0.8}

# =============================================================================
# More granular:
#     MTF tier
#     Company
#     sub-use??
#     other??
# =============================================================================

main_row_list = []
for phase_k in phase:
    for country_k in country.keys():
        for tech_k in tech.keys():
            for cust_k in cust_type.keys():
                for hh_k in hh.keys():
                    for year_k in years.keys():
                            
                        #number of connections
                        n_conn = round(random()*BASE_NUM * \
                            #no multiplier for phase cause all equal
                            country[country_k] * \
                            tech[tech_k] * \
                            cust_type[cust_k] * \
                            hh[hh_k] * \
                            years[year_k] )
                        
                        #create row
                        main_row_list.append({'phase':phase_k,
                                              'country':country_k,
                                              'technology':tech_k,
                                              'customer_type':cust_k,
                                              'hh_gender':hh_k,
                                              'year':year_k,
                                              'n_customers':n_conn})

# print to CSV                    
main_df = pd.DataFrame(main_row_list)
main_df.to_csv(out_path, index=False)


                 








