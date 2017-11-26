import numpy as np

def linear_y(t0, t_step, slope, y0):
    """
    A function to generate y values that satisfied to linear relationship with independent value t_list, slope, and start point of y

    Parameters:
    -----------
    t0: t0, with dependent variable as startpoint_y
    t_step: step of t
    slope: slope
    y0: startpoint of y

    Return:
    -------
    y1: array of dependent variable that satisfied linear relationship with a given slope

    Example:
    --------
    >>> y_list = linear_y(20, 1, 3, 0)
    """
    return t_step+t0, y0+t_step*slope

def varied_rb(t0, t_step, rdn, rb0, tau, y0):
    """
    """
    if rb0 != rdn:
        slope = 1.0*(rdn - rb0)/tau
    else:
        slope = 0
    t, m = linear_y(t0, t_step, slope, y0)
    return t, m

def microsaccades(stop_command_time, deltat_mean = 95, deltat_std = 40, deltas_mean = 30, deltas_std = 7, rb_mean = 8, rb_std = 2, efferent_delay = 20, thr_M = 1000, decay = 7, rdn = -8, tau = 50, t_step = 0.1, last_success_canceled = False):
    """
    A microsaccade model 
    ---------------------
    Parameters:
    stop_command_time: stop command time
    deltat_mean: Mean of afferent delay for ongoing microsaccades, by default is 95ms
    deltat_std: STD of afferent delay for ongoing microsaccades, by default is 40ms
    deltas_mean: Mean of afferent delay for stimulus onset processing, by default is 30ms
    deltas_std: STD of afferent delay for stimulus onset processing, by default is 8ms
    rb_mean: Mean of Buildup rate, by default is 8
    rb_std: STD of Buildup rate, by default is 2
    efferent_delay: After M reaches a threshold of 1000, a microsaccade is triggered as an efferent delay later, by default is 20ms
    thr_M: a threshold of M, by default is 1000
    decay: decay, by default is 7ms
    rdn: the dynamicas of the build-down of a activity after peripheral stimulus onset, by default is -1*rb_mean = -8
    tau: tau, by default is 50ms
    t_step: interval used for counting time, by default is 0.1ms
    last_success_canceled: whether last process is a succeed cancellation 

    Returns:
    --------
    t: list of t
    M: list of M
    is_success_canceled: whether a succeed cancellation
    """
    deltat = np.random.normal(deltat_mean, deltat_std)
    deltas = np.random.normal(deltas_mean, deltas_std)
    rb0 = np.random.normal(rb_mean, rb_std)
    if last_success_canceled is True:
        deltat = 0.5*deltat
        rb0 = 2*rb0
    m_point = 0
    M = []
    t = []
    M.append(m_point)
    t.append(deltat)
    t1 = t[0]
    is_success_canceled = False
    # linear increment
    while np.max(M)<1000:
        if not (0 < np.abs(t1-stop_command_time) < 1):    
            t1, m_point = linear_y(t1, t_step, rb0, m_point) 
            M.append(m_point)
            t.append(t1)
        else:
            # print('afferent start time: {}, m: {}'.format(t1, m_point))
            # Afferent delay for stimulus onset processing: deltas
            for i in range(int(deltas/t_step)):
                t1, m_point = linear_y(t1, t_step, rb0, m_point)
                M.append(m_point)
                t.append(t1)
            break
    # print('linear increment t: {}, m: {}, deltas: {}'.format(t1, m_point, deltas))
    rb = 1.0*rb0
    i = 0
    expo_flag = False
    while m_point > 1:
        if m_point > 1000:
            expo_flag = True
        if (1<m_point<1000) & (expo_flag is False):
            _, rb = varied_rb(t1, t_step, rdn, rb0, tau, rb)
            t1, m_point = linear_y(t1, t_step, rb, m_point)
            M.append(m_point)
            t.append(t1) 
        else:    
            # After arriving at 1000, after an efferent delay to trigger a microsaccade
            # if i<= int(efferent_delay/t_step):
            #     t1, m_point = linear_y(t1, t_step, rb0, m_point)
            #     M.append(m_point)
            #     t.append(t1)
            # else:
            # exponential decrease
            slope = -1.0*m_point/decay
            t1, m_point = linear_y(t1, t_step, slope, m_point)
            M.append(m_point)
            t.append(t1)
    if np.max(M)<1000:
        is_success_canceled = True
    return t, M, is_success_canceled






