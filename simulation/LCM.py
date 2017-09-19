#!/usr/bin/env python
# coding=utf-8

def lcm(a, c, m, x0):
    """
    Linear Congruential Method to generate random number

    Xn+1 = (aXn + c) % m
    Rn = Xn/(float(m))

    Parameters:
    -----------
    (parameters see introduction of this function)
    a: 
    c:
    m:
    X0:

    Return:
    -------
    Rn: random number
    """
    Rn = []
    x_list = []
    x_list.append(x0)
    r = x0/float(m)
    while r not in Rn:
        Rn.append(r)
        x_list.append((a*x_list[-1] + c) % m)
        r = x_list[-1]/float(m)
    return Rn, x_list

if __name__ == "__main__":
    a = 9
    m = 16
    c = [0, 3]
    x0 = [1, 2, 3, 4]

    Rn = []
    X_list = []
    for ci in c:
        for xi in x0:
            r, x_list = lcm(a, ci, m, xi)
            Rn.append(r)
            X_list.append(x_list)
    
        







