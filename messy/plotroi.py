import nibabel as nib
from ATT.algorithm import surf_tools
import numpy as np
from os.path import join as pjoin
import copy

class RG_ROI(object):

    def __init__(self, actpath='/nfs/h1/workingshop/huangtaicheng/parcellation_MT/BAA/surface_proc/'):
        """
        """
        self._facepath = '/nfs/t1/nsppara/corticalsurface'
        self._actpath = actpath

    def genRG_roi(self, vertx, sessid, hemi = 'lh', thr = 6.0):
        """
        """
        self._sessid = sessid
        self._hemi = hemi
        # Prepare data
        # Activation data
        actimg = nib.load(pjoin(self._actpath, sessid, 'mt', 'mt.sm0.self.'+hemi, 'mt_fix', 'sig.mgz'))
        actdata = actimg.get_data()
        actmask = copy.copy(actdata)
        actmask[actmask<thr] = 0
        actmask[actmask!=0] = 1
        self._actmask = actmask
        actheader = actimg.get_header()
        actshape = actimg.get_shape()
        self._actheader = actheader
        # faces
        _, faces = nib.freesurfer.read_geometry(pjoin(self._facepath, sessid, 'surf', hemi+'.sphere'))

        if isinstance(vertx, int):
            vertx = [vertx]

        # Initialization
        outdata_shape = list(actshape)
        outdata_shape.append(len(vertx))
        outdata = np.zeros(outdata_shape)
        
        for idx,vx in enumerate(vertx):
            outlbl = surf_tools.get_connvex(vx, faces, actmask) 
            outdata[...,idx][list(outlbl)] = 1
        self._outdata = outdata
        self.show_roi()

    def show_roi(self, idx = None):
        """
        """
        from surfer import Brain
        try:
           brain = Brain(self._sessid, self._hemi, 'inflated')
           if idx is not None:
               brain.add_data(self._outdata[:,0,0,idx], thresh = 0.0001)
           else:
               outdata = np.mean(self._outdata,axis=-1)
               outdata[outdata!=0] = 1
               brain.add_data(outdata[:,0,0], thresh = 0.0001) 
        except NameError as e:
           print('Run genRG_roi first please') 

    def save_roi(self, savelist = None, savepath = '/nfs/j3/userhome/huangtaicheng/hworkingshop/try_htc/freeroi_outdata'):
        """
        """
        if savelist is None:
            savelist = range(self._outdata.shape[-1])
        chsdata = self._outdata[...,savelist]
        savedata = np.mean(chsdata,axis=3)
        savedata[savedata!=0] = 1
        img = nib.MGHImage(savedata, None, self._actheader)
        nib.save(img, pjoin(savepath, self._sessid+'.mgz'))

def all_save(sessid, thr = 6.0, actpath='/nfs/j3/userhome/huangtaicheng/hworkingshop/parcellation_MT/BAA/surface_proc', hemi = 'lh', savepath = '/nfs/j3/userhome/huangtaicheng/hworkingshop/try_htc/freeroi_outdata'):
    """
    """
    from surfer import Brain
    img = nib.load(pjoin(actpath, sessid, 'mt', 'mt.sm0.self.'+hemi, 'mt_fix', 'sig.mgz'))
    header = img.get_header()
    actmask = img.get_data()
    actmask[actmask<thr] = 0
    actmask[actmask!=0] = 1
    outimg = nib.MGHImage(actmask, None, header)
    nib.save(outimg, pjoin(savepath, sessid+'.mgz'))

    brain = Brain(sessid, hemi, 'inflated')
    brain.add_data(actmask[:,0,0],thresh = 0.0001)
    return 0


def show_act(sessid, actpath = '/nfs/j3/userhome/huangtaicheng/hworkingshop/parcellation_MT/BAA/surface_proc', hemi = 'lh', thr = 6.0):
    """
    A function to show activation
    """
    from surfer import Brain
    img = nib.load(pjoin(actpath, sessid, 'mt', 'mt.sm0.self.'+hemi, 'mt_fix', 'sig.mgz'))
    data = img.get_data()
    try:
        assert np.max(data)>6.0, ""
    except AssertionError as e:
        save_zeros(sessid, img)
        return 0
    brain = Brain(sessid, hemi, 'inflated')
    brain.add_data(data[:,0,0],thresh = thr)               
    return brain

def save_zeros(sessid, img, save_path = '/nfs/j3/userhome/huangtaicheng/hworkingshop/try_htc/freeroi_outdata/'):
    """
    """
    datashape = img.get_shape()
    header = img.get_header()
    outdata = np.zeros(datashape)
    img = nib.MGHImage(outdata, None, header)
    nib.save(img, pjoin(save_path, sessid+'.mgz'))
    
