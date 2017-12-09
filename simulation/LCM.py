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

def list_reshape_bywindow(longlist, windowlen, step=1):
    """
    A function to use window intercept long list into several component

    A list could like below,
    [a, b, c, d, e]
    Output could be
    [[a,b], [c,d]]
    where windowlen as 2, 
          step as 2

    Parameters:
    ------------
    longlist: original long list
    windowlen: window length
    step: by default is 1, to use overlapping batch method, step as 1,
                           to use non-overlapping batch method, step as windowlen

    Returns:
    --------
    ic_list: intercept list

    Example:
    --------
    >>> ic_list = list_reshape_bywindow(longlist, windowlen = 3)
    """
    ic_list = []
    i = 0
    while len(longlist)>=(windowlen+step*i): 
        ic_list.append(longlist[(step*i):(windowlen+step*i)]) 
        i+=1
    return ic_list

def system_time(mean_time, a, c, m, X0, customer_count = 100):
    """
    Generate system time
    """
    r_gen = lcm(a, c, m, X0)
    rd = [r_gen.next() for i in range(customer_count)]
    un = [i for i, j in rd]
    time = neg_exp_distribute(mean_time, un)
    return time

class MM1_system(object):
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

    def queue_time(self):
        """
        Compute the queue time series

        The idea for queue time computation is relate to an iteration analysis
        the queue time is equal to summation of the interarrival time of last one, and the service time of last one, and queue time of last one minus the interarrival time of present one.
        if queue time smaller than 0, that means to that customer, he/she needn't wait for a serve

        For example, guess we have list as:

        iat 4 3 2 2
        st  2 6 4 1

        the queue time of each subject will be
        0 0 4 6

        This function has been simplified

        Returns:
        --------
        queue_time: the average queue time
        """
        queue_time_series = []
        if self._custom_num < 2:
            return 0
        else:
            for i in range(self._custom_num):
                if i==0:
                    queue_time_tmp = 0
                    queue_time_series.append(queue_time_tmp)
                else:
                    iat_now = np.sum(self._iat[:(i+1)])
                    iat_lastperson = np.sum(self._iat[:i])
                    st_lastperson = self._st[i-1]
                    queue_time_tmp = st_lastperson + iat_lastperson + queue_time_tmp - iat_now
                    if queue_time_tmp < 0:
                        queue_time_tmp = 0
                    queue_time_series.append(queue_time_tmp)
        return queue_time_series

    def queue_time_by_idol_method(self):
        """
        A new solution to compute queue time using vision of machine idol time.
        Same results to queue_time_series
        """
        idolmach_time = 0
        mach_isidol = True
        arr_time = [sum(self._iat[:(i+1)]) for i in range(self._custom_num)]
        queue_time_series = []
	for i in range(self._custom_num):
            if mach_isidol:
                idolmach_time = arr_time[i] + self._st[i]
                mach_isidol = False
                queue_time_series.append(0)
            else:
                if arr_time[i] > idolmach_time:
                    queue_time_series.append(0)
                    idolmach_time = arr_time[i] + self._st[i]
                else:
                    queue_time_series.append(idolmach_time - arr_time[i])
                    idolmach_time = idolmach_time + self._st[i]
                print('{}'.format(idolmach_time))
        return queue_time_series, idolmach_time

 
    def avg_queue_time(self):
        """
        Return series of queue time of each customer on average
        """
        queue_time_series = self.queue_time()
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

class MM2_system(object):
    def __init__(self, iat, st):
        """
        Initialization of MM2 system
        """
        self._iat = iat
        self._st = st
        self._custom_num = len(iat)
    
    def queue_time(self):
        """
        Computation of queue time

        To solve problems of queue time in MM2 system, 
        machine idol time was set to instruct when machine will be idol
        If it exists machine to be idol, queue time should be 0, or queue time should be idolmach_time - arrive_time
        """
        idolmach_time = [0, 0]
        mach_isidol = [True, True]
        arr_time = [sum(self._iat[:(i+1)]) for i in range(self._custom_num)]
        queue_time_series = []
        for i in range(self._custom_num):
            if np.any(mach_isidol):
                idolmach_time[mach_isidol.index(True)] = arr_time[i] + self._st[i] 
                mach_isidol[mach_isidol.index(True)] = False
                queue_time_series.append(0)
            else:
                if arr_time[i] > np.min(idolmach_time):
                    queue_time_series.append(0)
                    idolmach_time[idolmach_time.index(np.min(idolmach_time))] = arr_time[i] + self._st[i]
                else:
                    queue_time_series.append(np.min(idolmach_time) - arr_time[i])
                    idolmach_time[idolmach_time.index(np.min(idolmach_time))] = np.min(idolmach_time) + self._st[i]
            print('{}'.format(idolmach_time))
        return queue_time_series, idolmach_time

if __name__ == '__main__':

    customer_count = 100
    x0_iat = 1155192169
    iat = system_time(5, 16807, 0, 2147483647, x0_iat, customer_count)
    x0_st = 1806794933
    st = system_time(8, 16807, 0, 2147483637, x0_st, customer_count)
        
   
    avg_queue_time = []
    avg_service_time = []
    avg_system_time = []
    for i in np.arange(0, customer_count):
        # the average time
        cat_cls = MM1_system(iat[:(i+1)], st[:(i+1)])
        avg_queue_time.append(cat_cls.avg_queue_time())
        avg_service_time.append(cat_cls.avg_service_time())
        avg_system_time.append(cat_cls.avg_system_time())

    # estimate average time in queue and its corresponding variance, and its confidence interval using NBM (non-overlapping batch method) and OBM (overlapping batch method)
    # Batch size = 100
    # Batch number = 100
    # window size = 100, to NBM, list size = 100*100 = 10,000
    #                    to OBM, list size = 199
    iat_gen = lcm(16807, 0, 2147483647, 1155192169)
    st_gen = lcm(16807, 0, 2147483647, 1806794933)
    iat_nbm_rd = [iat_gen.next() for i in range(10000-1)]
    st_nbm_rd = [st_gen.next() for i in range(10000-1)]
    iat_obm_rd = [iat_gen.next() for i in range(199-1)]
    st_obm_rd = [iat_gen.next() for i in range(199-1)]

    xn_nbm_iat = [j for i,j in iat_nbm_rd]
    u0_nbm_iat = 1.0*x0_iat/2147483647
    un_nbm_iat = [1.0*x/2147483647 for x in xn_nbm_iat]
    un_nbm_iat = [u0_nbm_iat] + un_nbm_iat
    nbm_iat = neg_exp_distribute(5, un_nbm_iat)

    xn_nbm_st = [j for i,j in st_nbm_rd]
    u0_nbm_st = 1.0*x0_st/2147483647
    un_nbm_st = [1.0*x/2147483647 for x in xn_nbm_st]
    un_nbm_st = [u0_nbm_st] + un_nbm_st
    nbm_st = neg_exp_distribute(8, un_nbm_st)

    xn_obm_iat = [j for i,j in iat_obm_rd]
    u0_obm_iat = 1.0*x0_iat/2147483647
    un_obm_iat = [1.0*x/2147483647 for x in xn_obm_iat]
    un_obm_iat = [u0_obm_iat] + un_obm_iat
    obm_iat = neg_exp_distribute(5, un_obm_iat)

    xn_obm_st = [j for i,j in st_obm_rd]
    u0_obm_st = 1.0*x0_st/2147483647
    un_obm_st = [1.0*x/2147483647 for x in xn_obm_st]
    un_obm_st = [u0_obm_st] + un_obm_st
    obm_st = neg_exp_distribute(8, un_obm_st)

    sep_nbm_iat = list_reshape_bywindow(nbm_iat, 100, 100)
    sep_nbm_st = list_reshape_bywindow(nbm_st, 100, 100)
    sep_obm_iat = list_reshape_bywindow(obm_iat, 100, 1)
    sep_obm_st = list_reshape_bywindow(obm_st, 100, 1)

    queue_nbm_time = []
    queue_obm_time = []
    for i in range(100):
        cat_cls_nbm = MM1_system(sep_nbm_iat[i], sep_nbm_st[i])
        cat_cls_obm = MM1_system(sep_obm_iat[i], sep_obm_st[i])
        queue_nbm_time.append(cat_cls_nbm.queue_time())
        queue_obm_time.append(cat_cls_obm.queue_time())

    # nbm variance
    xn_avg_nbm = np.mean(queue_nbm_time)
    yn_avg_nbm = [np.mean(qnt) for qnt in queue_nbm_time]
    dif_avg_nbm = [(yan - xn_avg_nbm)**2 for yan in yn_avg_nbm]
    vb_nbm = (1.0*100/(100-1))*np.sum(dif_avg_nbm)

    # nbm confidence interval
    # t99,0.975 = 1.984
    # xn_avg_nbm +- 1.984*np.sqrt(vb_nbm/100)
    
    # obm variance
    xn_avg_obm = np.mean(queue_obm_time)
    yn_avg_obm = [np.mean(qot) for qot in queue_obm_time]
    dif_avg_obm = [(yao - xn_avg_obm)**2 for yao in yn_avg_obm]
    vb_obm = (1.0*199*100/((199-100+1)*(199-100)))*np.sum(dif_avg_nbm)

    # obm confidence interval
    # t199,0.975 ~= 1.984
