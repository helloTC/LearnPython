#!/usr/bin/env python
# coding=utf-8

import math
import numpy as np

def lcm_bs(a, c, m, X):
    """
    """
    X_new = (a*X+c) % m
    R = X/float(m)
    return X_new, R

def lcm(a, c, m, X0):
    """
    A function to use Linear Congruential Method (LCM) to generate random number
    Here we use generator to make it faster and clearer.
    
    LCM: Xn+1 = (aXn+c) mod m
         Rn = Xn/float(m)

    Parameters:
    -----------
    a, c, m, X0   parameters

    Return:
    -------
    R: generator of random number
    """
    X_new = X0
    while 1:
        X_new, R = lcm_bs(a, c, m, X_new)
        yield R, X_new

def neg_exp_distribute(mean_time, U):
    """
    Generate series satisfied negative exponential distribution

    X = -mean*lnU
    
    Parameters:
    -----------
    mean_time: mean time
    U: a list as a parameter for negative exponential time

    Return:
    -------
    X: Generated time (interarrival time or service time)
    """
    return [-1.0*mean_time*math.log(u) for u in U]


if __name__ == '__main__':

    h_count = 5

    x0_iat = 1155192169
    # interarrival time series
    iat_gen = lcm(16807, 0, 2147483647, x0_iat)
    # generate first 50 random numbers and Xn (Xn will contains 51 numbers)
    iat_rd = [iat_gen.next() for i in range(h_count-1)]

    xn_iat = [j for i, j in iat_rd]
    u0_iat = 1.0*x0_iat/2147483647
    un_iat = [1.0*x/2147483647 for x in xn_iat]
    un_iat = [u0_iat] + un_iat

    iat = neg_exp_distribute(5, un_iat)
        
    x0_st = 1806794933
    # serice time series
    st_gen = lcm(16807, 0, 2147483647, 1806794933)
    # generate first 50 random numbers and Xn (Xn will contains 51 numbers) 
    st_rd = [st_gen.next() for i in range(h_count-1)]
    
    xn_st = [j for i, j in st_rd]
    u0_st = 1.0*x0_st/2147483647
    un_st = [1.0*x/2147483647 for x in xn_st]
    un_st = [u0_st] + un_st

    st = neg_exp_distribute(8, un_st)
    
#    queue_time_series = []
#     # the average time in queue
#     for i in np.arange(1, len(iat)):
#         queue_time_series.append(sum(st[:i]) - sum(iat[:(i+1)]))
     
     
    # the average time being serviced
    avg_st_time = np.mean(st)    

    # the average time in system
    if np.sum(iat) < np.sum(st[:-2]):
        avg_time = (np.sum(st) + iat[0])/len(iat)
    else:
        avg_time = (np.sum(iat) + st[-1])/len(iat)
   





