import random
import pandas as pd 

def generate_random_decimals(start, end, n):
    # Generate n random decimal numbers between start and end
    random_decimals = [round(random.uniform(start, end),2) for _ in range(n)]
    return random_decimals


if __name__ == '__main__':
    random_decimals = generate_random_decimals(0.1, 0.8, 147)
    df = pd.DataFrame({'distribution':random_decimals})
    df.to_csv('distribution.csv',index=False)