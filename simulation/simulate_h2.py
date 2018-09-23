# Code for simulating calculation of heritability

# Variance(p) = Variance(A) + Variance(E) + Noise
# To MZ twins, they have same variance of A and E
# To DZ twins, their variance of A shared only 50%

import numpy as np

nsubj = 1000
# Set variance of environment and errors

vE = np.random.normal(0,1,nsubj)
# No enviornment
# vE = np.zeros((nsubj))


# First DZ
# We seperate Variance(A) = Variance(AS) + Variance(AD)
# Where AS means their same variance and AD means their different variance
# Thus
vAS = np.random.normal(0,np.sqrt(0.5),nsubj)
vAD1 = np.random.normal(0,np.sqrt(0.5),nsubj)
vAD2 = np.random.normal(0,np.sqrt(0.5),nsubj)

DZ_A1 = vAS + vAD1
DZ_A2 = vAS + vAD2
# Verification
shared_pct_DZ1 = np.var(vAS)/np.var(DZ_A1)
shared_pct_DZ2 = np.var(vAS)/np.var(DZ_A2)
print('DZ twin1 and twin2 seperately shared 50% variance of genome: {0},{1}'.format(shared_pct_DZ1, shared_pct_DZ2))
# Thus, Variance of DZ
vDZ1 = DZ_A1 + vE + np.random.normal(0,0.1,nsubj)
vDZ2 = DZ_A2 + vE + np.random.normal(0,0.1,nsubj)

# Variance of 50% addictive genetic contribution
spD1_dist = []
spD2_dist = []
for i in range(1000):
    vAS_dist = np.random.normal(0,np.sqrt(0.5),nsubj)
    vAD1_dist = np.random.normal(0,np.sqrt(0.5),nsubj)
    vAD2_dist = np.random.normal(0,np.sqrt(0.5),nsubj)
    DZ_A1_dist = vAS_dist + vAD1_dist
    DZ_A2_dist = vAS_dist + vAD2_dist
    spD1_dist.append(np.var(vAS_dist)/np.var(DZ_A1_dist))
    spD2_dist.append(np.var(vAS_dist)/np.var(DZ_A2_dist))

# Similar, MZ
MZ_A = np.random.normal(0,1,nsubj)
# Verification
# Same environment
vMZ1 = MZ_A + vE + np.random.normal(0,0.1,nsubj)
vMZ2 = MZ_A + vE + np.random.normal(0,0.1,nsubj)


# Different environment
vE1 = np.random.normal(0,1,nsubj)
vE2 = np.random.normal(0,1,nsubj)
vMZ1_varE = MZ_A + vE1 + np.random.normal(0,0.1,nsubj)
vMZ2_varE = MZ_A + vE2 + np.random.normal(0,0.1,nsubj)
vDZ1_varE = DZ_A1 + vE1 + np.random.normal(0,0.1,nsubj)
vDZ2_varE = DZ_A2 + vE2 + np.random.normal(0,0.1,nsubj)
# Larger noise
vMZ1_noise = MZ_A + vE + np.random.normal(0,0.5,nsubj)
vMZ2_noise = MZ_A + vE + np.random.normal(0,0.5,nsubj)
vDZ1_noise = DZ_A1 + vE + np.random.normal(0,0.5,nsubj)
vDZ2_noise = DZ_A2 + vE + np.random.normal(0,0.5,nsubj)



