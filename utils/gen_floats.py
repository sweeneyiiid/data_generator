import random

def float_generator(n):
    """Generates n unevenly distributed floats between 0 and 1 that sum to 1."""

  # Generate random floats
    floats = [random.random() for _ in range(n)]

  # Normalize floats to sum to 1
    total = sum(floats)
    floats = [round(float(f / total),2) for f in floats]
#    print (floats)
   # randomize
    random.shuffle(floats)
    return floats

if __name__ == '__main__':
    n = 10
    floats = float_generator(n)
    print(floats)
    print (sum(floats))