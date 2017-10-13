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

class compute_avg_time(object):
    def __init__(self, iat, st):
        """
        A class to compute varied average time
        Initialization
        
        Parameters:
        -----------
        iat: interarrival time series
        st: service time series  (of each customer)
        """
        self._iat = iat
        self._st = st
        self._custom_num = len(iat)

    def avg_queue_time(self):
        """
        Compute the average queue time
        To each customer (the ith), their queue time will be
        sigma(st:st from 1 to i-1) - sigma(iat:iat from 2 to i)
        if queue time smaller than 0, that means to that customer, he/she needn't wait for a serve
        For example, guess we have list as:

        iat 4 3 2 2
        st  2 6 4 1

        the queue time of each subject will be
        0 0 3 5

        This function has been simplified

        Returns:
        --------
        avg_queue_time: the average queue time
        """
        queue_time_series = []
        queue_time_series.append(0)
        if self._custom_num < 2:
            return 0
        else:
            for i in np.arange(1, self._custom_num):
                queue_time_series.append(np.sum(self._st[:i]) - np.sum(self._iat[1:(i+1)]))
            queue_time_series[queue_time_series<0] = 0
            return np.mean(queue_time_series)

    def avg_service_time(self):
        """
        Compute the average service time

        the average service time is the mean of service time

        Returns:
        --------
        avg_service_time: the average service time
        """
        return np.mean(self._st)

    def avg_system_time(self):
        """
        Compute the average system time

        if there's larger summation of interarrival time than service time except the last one, whole system time will be all of the interarrival time + service time of the last customer(System must wait for the last one)
        if there's smaller summation of interarrival time than service time except the last one, whole system time will be all of the service time + interarrival time of the first customer(System must wait for the first one to come)

        Returns:
        --------
        avg_sys_time: average system time  
        """
        if self._custom_num == 1:
            avg_sys_time = self._st[0] + self._iat[0]
        else:
            if np.sum(self._iat) < np.sum(self._st[:-2]):
                avg_sys_time = (np.sum(self._st) + self._iat[0])/self._custom_num
            else:
                avg_sys_time = (np.sum(self._iat) + st[-1])/self._custom_num
            return avg_sys_time


if __name__ == '__main__':

    customer_count = 50

    x0_iat = 1155192169
    # interarrival time series
    iat_gen = lcm(16807, 0, 2147483647, x0_iat)
    # generate first 50 random numbers and Xn (Xn will contains 51 numbers)
    iat_rd = [iat_gen.next() for i in range(customer_count-1)]

    xn_iat = [j for i, j in iat_rd]
    u0_iat = 1.0*x0_iat/2147483647
    un_iat = [1.0*x/2147483647 for x in xn_iat]
    un_iat = [u0_iat] + un_iat

    iat = neg_exp_distribute(5, un_iat)
        
    x0_st = 1806794933
    # serice time series
    st_gen = lcm(16807, 0, 2147483647, 1806794933)
    # generate first 50 random numbers and Xn (Xn will contains 51 numbers) 
    st_rd = [st_gen.next() for i in range(customer_count-1)]
    
    xn_st = [j for i, j in st_rd]
    u0_st = 1.0*x0_st/2147483647
    un_st = [1.0*x/2147483647 for x in xn_st]
    un_st = [u0_st] + un_st

    st = neg_exp_distribute(8, un_st)
   
    avg_queue_time = []
    avg_service_time = []
    avg_system_time = []
    for i in np.arange(0, customer_count):
        # the average time
        cat_cls = compute_avg_time(iat[:(i+1)], st[:(i+1)])
        avg_queue_time.append(cat_cls.avg_queue_time())
        avg_service_time.append(cat_cls.avg_service_time())
        avg_system_time.append(cat_cls.avg_system_time())

