import models
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cancel_command = 150
perm_t_list = []
perm_m_list = []
for n_perm in range(1000):
    t_list = []
    m_list = []
    is_success_canceled = False
    is_success_canceled_list = []
    t0 = 0
    for i in range(1):
        t, m, is_success_canceled= models.microsaccades(cancel_command, last_success_canceled = is_success_canceled, t_step = 1)
        t = [j + t0 for j in t]
        t0 = np.max(t)
        t_list += t
        m_list += m
        is_success_canceled_list.append(is_success_canceled)
    print('permutation times: {}'.format(n_perm))
    t_list = np.array(t_list)
    m_list = np.array(m_list)
    pt_t_list = t_list[m_list>1000]
    pt_m_list = m_list[m_list>1000]
    perm_t_list.append([int(m) for m in pt_t_list])
    perm_m_list.append(pt_m_list)
plt.figure()
plt.plot(t_list, m_list)
plt.plot(pt_t_list.tolist(), pt_m_list.tolist(), marker = 'o', color='r', ls='')
plt.show()
flat_perm_t_list = [item for sublist in perm_t_list for item in sublist]
flat_perm_m_list = [item for sublist in perm_m_list for item in sublist]

plt.figure()
bin_perm_t_list = np.bincount(flat_perm_t_list)
p_perm_t_list = 1.0*bin_perm_t_list/bin_perm_t_list.sum()
plt.plot(p_perm_t_list)
plt.show()

