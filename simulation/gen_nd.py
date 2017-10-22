import random
import math

"""
Generate Normal distribution
"""

def nd_generator(R1, R2):
    """
    A function to generate normal distribution by using random number of R1 and R2
    
    Parameters:
    -----------
    R1: random number between 0-1
    R2: random number between 0-1

    Returns:
    --------
    Z1: standard normal variate
    Z2: standard normal variate
    """
    Z1 = (-2.0*math.log(R1))**(0.5)*math.cos(2*math.pi*R2)
    Z2 = (-2.0*math.log(R1))**(0.5)*math.sin(2*math.pi*R2)
    return Z1, Z2

if __name__ == "__main__":
    """
    Generate 100 standard normal variate
    """
    nd_random = []
    for i in range(50):
        R1 = random.random()
        R2 = random.random()
        Z1, Z2 = nd_generator(R1, R2)
        nd_random.append(Z1)
        nd_random.append(Z2)

 
        

    




