import numpy as np
import pandas as pd 

def generate_exponential_increase(n, value):
    # Generate n values exponentially spaced between 1 and value
    exp_values = np.geomspace(1, value, num=n)
    exp_values = exp_values.astype(int)
    print (exp_values)
    exp = [1]
    for num in range(1,n):
        exp.append(exp_values[num] - exp_values[num - 1])
    # Return the values as integers
    return exp

# print (generate_exponential_increase(12,1000))

def target_dataframe_gen(**kwargs):

    """
    I require the following to run successfully
    start_year,end_year,targets= {
        'target1':2000,
    'target2':1000...
    }
    """

    # get the values
    start_year = kwargs.get('start_year')
    end_year = kwargs.get('end_year')
    targets = kwargs.get('targets')

    # get the time range
    years = range(start_year,end_year)
    df = pd.DataFrame({'Date':years})

    # create cols by looping over each target
    for key, target_value in targets.items():
        df[key] = generate_exponential_increase(value=target_value, n=len(years))
    
    return df 



if __name__ == '__main__':
    df  = target_dataframe_gen(
        start_year = 2024,
        end_year = 2036,
        targets= {
        'target1':2000,
    'target2':1000
        })

    df.to_csv('exp_targets.csv',index=False)