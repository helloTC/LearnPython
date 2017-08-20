import nibabel as nib
from surfer import Brain
from os.path import join as pjoin

def show_img(sessid, actpath, roipath):
    """
    """
    actdata = nib.load(actpath).get_data()
    roidata = nib.load(roipath).get_data()
    actbrain = Brain(sessid, 'lh', 'inflated')
    try:
        actbrain.add_data(actdata[:,0,0], thresh = 6.0)
    except:
        actbrain.close()
    raw_input('waiting...')
    roibrain = Brain(sessid, 'lh', 'inflated')
    try:
        roibrain.add_data(roidata[:,0,0],thresh = 0.0001)
    except:
        roibrain.close()
    raw_input('waiting...')

def loop_imaging(sessid, all_sid, all_actpath, all_roipath):
    """
    """
    init_i = all_sid.index(sessid)
    final_i = len(all_sid)
    for i in range(init_i, final_i):
        print('showing {}'.format(all_sid[i]))
        show_img(all_sid[i], all_actpath[i], all_roipath[i])
    print('Finish')

if __name__ == '__main__':
    sidpath = '/nfs/h2/fmricenter/doc/mt/sessid_all/mt_sessid'
    with open(sidpath, 'r') as f:
        all_sid = f.read().splitlines()
    sessid = input('Input sessid as initial keyword:')
    actparpath = '/nfs/t1/nsppara/surface_proc/'
    all_actpath = [pjoin(actparpath, sid, 'mt', 'mt.sm0.self.lh', 'mt_fix', 'sig.mgz') for sid in all_sid]
    roiparpath = '/nfs/j3/userhome/huangtaicheng/hworkingshop/try_htc/freeroi_outdata/'
    all_roipath = [pjoin(roiparpath, sid+'.mgz') for sid in all_sid]
    loop_imaging(sessid, all_sid, all_actpath, all_roipath) 
    
