import models
import numpy as np

cancel_command = 150
t_list = []
m_list = []
is_success_canceled_list = []
is_success_canceled = False
t0 = 0
for i in range(100):
    t, m, is_success_canceled= models.microsaccades(150, last_success_canceled = is_success_canceled)
    t = [j + t0 for j in t]
    t0 = np.max(t)
    t_list = t_list + t
    m_list = m_list + m
    is_success_canceled_list.append(is_success_canceled)
