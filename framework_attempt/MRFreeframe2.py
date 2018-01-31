import nibabel as nib
from nibabel import freesurfer
import numpy as np

class Region(object):
    def __init__(self, source):
        self._source = source

    def __add__(self):
        pass

    def __sub__(self):
        pass

    def __setattr__(self, item, value):
        object.__setattr__(self, item, value)

    def __getattr__(self, item):
        if item not in self.__dict__:
 	    return None

    def __call__(self, layer = 1, hemi = None, space_name = 'MNI'):
        self.layer = layer
        self.space = space_name
        self.set_hemi(hemi)
        self.load_data()
        if self.morphdata is not None:
            self.morphshape = self.morphdata.shape
        if self.funcdata is not None:
            self.funcshape = self.funcdata.shape
        if self.labeldata is not None:
            self.labelshape = self.labeldata.shape 

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, layer_value):
        if not isinstance(layer_value, int):
            raise ValueError('Layer value must be an integer!')
        if layer_value < 1 | layer_value > 7:
            raise ValueError('Layer value must be in range of 1-7')        
        self._layer = value 
  
    @property 
    def space(self):
        return self._space
    
    @space.setter
    def space(self, space_type):
        if not isinstance(space_type, str):
            raise ValueError('space_type must be a string')
        self._space = space

    def set_hemi(self, hemi = None):
        if ('lh' in self._source.lower()) & ('rh' in self._source.lower()):
            self.hemi = 'both'
        elif ('lh' in self._source.lower()) & ('rh' not in self._source.lower()):
            self.hemi = 'lh'
        elif ('lh' not in self._source.lower()) & ('rh' in self._source.lower()):
            self.hemi = 'rh'
        else:
            self.hemi = hemi
        

    def load_data(self):
        # Geometry
        if self._source.endswith(('.inflated', '.pial', '.white', '.orig', '.surf.gii2')):
            self.coordinate, self.face = get_geometry_data(self._source)

        # Morphology
        elif self._source.endswith(('.curv', '.sulc', '.volume', '.thickness', '.area', '.shape.gii', '.func.gii')):
            self.morphdata = get_morph_data(self._source)

        # Function
        elif self._source.endswith(('.dscalar.nii', 'dseries.nii', '.mgz', '.mgh', '.nii.gz', '.nii')):
            self.img, self.funcdata, self.funcheader  = get_func_data(self._source)

        # Label
        elif self._source.endswith(('.label', '.annot', '.dlabel.nii', '.label.gii')):
            self.labeldata = get_label_data(self._source) 

    def save_data(self):
        pass

def get_geometry_data(source):
    """
    Method to load geometry data
    
    Parameters:
    -----------
    source: source path

    Returns: 
    --------
    coordinate: coordinate
    face: face
    """
    if source.endswith(('.inflated', '.pial', '.white', '.orig')):
        coordinate, face = freesurfer.read_geometry(source)
    elif source.endswith('.surf.gii'):
        coordinate = nib.load(source).darrays[0].data
        face = nib.load(source).darrays[1].data
    else:
        raise Exception('Wrong data formats')
    return coordinate, face

def get_morph_data(source):
    """
    """
    if source.endswith(('.curv', '.sulc', '.volume', '.thickness', '.area')):
        data = np.expand_dims(freesurfer.read_morph_data(source), axis=-1)
    elif source.endswith(('.shape.gii', '.func.gii')):
        data = np.expand_dims(nib.load(source).darrays[0].data, axis=-1)
    else:
        raise Exception('Wrong data format')
    return data 

def get_func_data():
    """
    """
    img = nib.load(source)
    data = img.get_data()
    header = img.get_header()
    if source.endswith(('.mgz', '.mgh')):
        data = data.reshape((data.shape[0], data.shape[-1]))
    elif source.endswith(('.dscalar.nii', '.dseries.nii')):
        data = data.T
    elif source.endswith(('.nii.gz', '.nii')):
        pass
    else:
        raise Exception('Wrong data format')
    return img, data, header     

def get_label_data():
    """
    """
    if source.endswith('.label.gii'):
        data = nib.load(source).darrays[0].data
    elif source.endswith('.dlabel.nii'):
        data = nib.load(source).get_data().T
    elif source.endswith('.label'):
        data = freesurfer.read_label(source)
    elif source.endswith('.annot'):
        data, _, _ = freesurfer.read_annot(souce)
    else:
        raise Exception('Wrong data format')
    return data
