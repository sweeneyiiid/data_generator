from exponential_targets import generate_exponential_increase
from linear_targets import linear_targets
from gen_floats import float_generator
import pandas as pd

def get_country_level_df(no_of_countries,start_year,no_of_years,total_achieved,distribution_type,no_of_sub_categories):
    """
    start_year is the year you want the reading to start from (int)
    no_of_countries & no_of_years should be integers
    distribution_type has to be either 'linear' or 'exp'
    no_of_sub_categories refers to the distinct count of sub categories you need in a country,
      e.g. clean cooking has 5 (Biogas,electric, ethanol,ICS, LPG)
    """
    if distribution_type == 'exp':
        yearly_values = generate_exponential_increase(no_of_years,total_achieved)
    yearly_values = linear_targets(end_value=total_achieved,num_points=no_of_years)

    master_list = []
    for val in yearly_values:
        master_list.extend([int(val * n) for n in float_generator(no_of_countries)])
    # the above func generates a list of what each country achieved in each year i.e., [NG_y1,TZ_y2,...NG_y1,TZ_y2]
    new_list = []
    for val in master_list:
        new_list.extend([int(val * n) for n in float_generator(no_of_sub_categories)])

    subcat_col = list(range(no_of_sub_categories))*int(len(new_list)/no_of_sub_categories)

    print (len(new_list)/no_of_countries)

    country_col = [i for i in range(no_of_countries) for _ in range(int(len(new_list)/no_of_countries))]

    year_col = [i for i in range(start_year,no_of_years+start_year) for _ in range(int(len(new_list)/no_of_years))]

    return pd.DataFrame(
        {'Year':year_col,
         'Country':country_col,
         'Sub_category':subcat_col,
         'achieved':new_list
        }
        )

    """
    Finally, map your countries to each value in the country col, and your sub_category to each val in the subcat col
    """


if __name__ == '__main__':
    try:
        df = get_country_level_df(10,2000,5,100000,'linear',4)
        df.to_csv('mock_data.csv',index=False)
    except Exception as e:
        print (e)


# get yearly targets
# divide each by n to get what n countries achieved in each year
    ## each year would have a different distribution
# divide each by n again to get what each did in n sub sectors
    ## each sub would have a different distribution 
# create identifier col - iterate 1 - sub-sector - n over and over again - to know what row belongs to what sub secotr
# create another identifier col - reprsenting each country



