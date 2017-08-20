import nibabel as nib
import numpy as np
from ATT.algorithm import surf_tools

_, faces = nib.freesurfer.read_geometry('/nfs/t1/nsppara/corticalsurface/fsaverage/surf/lh.sphere')

# data = nib.load('../fsfast_surf_mt_lh.mgz').get_data()
# data = data[...,0]
data = nib.load('/nfs/j3/userhome/huangtaicheng/hworkingshop/parcellation_MT/BAA/surface_proc/S0001/mt/mt.sm0.lh/mt_fix/t.mgz').get_data()

mask = nib.load('../mask_lh_thr7_mt.mgz').get_data()

vxall = np.where(data*mask>0)[0]

localmax = []
for i,vx in enumerate(vxall):
    print('{0} start'.format(i))
    neigh = surf_tools.get_n_ring_neighbor(vx, faces, n=2, ordinal = True)
    neigh_mag = data[list(neigh[0]),0,0]
    if np.all(data[vx,0,0]>neigh_mag):
        localmax.append(vx)
mag = data[list(localmax),0,0]
locmax_sort = [localmax[i] for i in np.argsort(mag)[::-1]]




