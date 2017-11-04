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

def microsaccades(AfferentDelay_mean = 95, AfferentDelay_std = 40, rb_mean = 8, rb_std = 2, efferent_delay = 20, thr_M = 1000, decay = 7, t_step = 1):
    """
    """
    afferent_delay = np.random.normal(AfferentDelay_mean, AfferentDelay_std)
    rb = np.random.normal(rb_mean, rb_std)
    m_point = 0
    M = []
    M.append(m_point)
    t = []
    t.append(afferent_delay)
    t1 = t[0]
    # linear increment
    while np.max(M)<1000:
       t1, m_point = linear_y(t1, t_step, rb, m_point) 
       M.append(m_point)
       t.append(t1)
    # After arriving at 1000, after an efferent delay to trigger a microsaccade
    for i in range(efferent_delay/t_step):
        t1, m_point = linear_y(t1, t_step, rb, m_point)
        M.append(m_point)
        t.append(t1)
    # exponential decrease
    while m_point>1:
        slope = -1.0*m_point/decay
        t1, m_point = linear_y(t1, t_step, slope, m_point)
        M.append(m_point)
        t.append(t1)
    return t, M







