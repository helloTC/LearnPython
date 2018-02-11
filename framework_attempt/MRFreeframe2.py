import nibabel as nib
from nibabel import freesurfer
import numpy as np

class Region(object):
    def __init__(self):
        pass

    def __add__(self):
        pass

    def __sub__(self):
        pass

    def __setattr__(self, item, value):
        object.__setattr__(self, item, value)

    def __getattr__(self, item):
        if item not in self.__dict__:
 	    return None

    def __call__(self, source, hemisphere = None, layer = 1, space_name = None):
        self.layer = layer
        self.space = space_name
        self.hemi = hemisphere
        self.load_data(source)
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
        self._layer = layer_value 
  
    @property 
    def space(self):
        return self._space
    
    @space.setter
    def space(self, space_type):
        if self._space is None:
            if not isinstance(space_type, str):
                raise ValueError('space_type must be a string')
            self._space = space_type
        else:
            if space_type is None:
                pass

    @property
    def hemi(self):
        return self._hemi

    @hemi.setter
    def hemi(self, hemisphere):
        if self._hemi is None:
            if (hemisphere not in ['left', 'right', 'both']):
                raise ValueError('Parameter of hemisphere should be left, right or both')
            self._hemi = hemisphere
        else:
            if hemisphere is None:
                pass

    def load_data(self, source):
        # Geometry
        if source.endswith(('.inflated', '.pial', '.white', '.orig', '.surf.gii')):
            self.coordinate, self.face = _get_geometry_data(source)

        # Morphology
        elif source.endswith(('.curv', '.sulc', '.volume', '.thickness', '.area', '.shape.gii', '.func.gii')):
            self.morphdata = _get_morph_data(source)

        # Function
        elif (source.endswith(('.dscalar.nii', 'dseries.nii', '.mgz', '.mgh', '.nii.gz'))) | (source.endswith('.nii')&(source.count('.')==1)):
            self.img, self.funcdata, self.funcheader  = _get_func_data(source)

        # Label
        elif source.endswith(('.label', '.annot', '.dlabel.nii', '.label.gii')):
            self.labeldata = _get_label_data(source) 

    def save_data(self):
        pass

def _get_geometry_data(source):
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

def _get_morph_data(source):
    """
    """
    if source.endswith(('.curv', '.sulc', '.volume', '.thickness', '.area')):
        data = np.expand_dims(freesurfer.read_morph_data(source), axis=-1)
    elif source.endswith(('.shape.gii', '.func.gii')):
        data = np.expand_dims(nib.load(source).darrays[0].data, axis=-1)
    else:
        raise Exception('Wrong data format')
    return data 

def _get_func_data(source):
    """
    """
    img = nib.load(source)
    data = img.get_data()
    header = img.get_header()
    if source.endswith(('.mgz', '.mgh')):
        data = data.reshape((data.shape[0], data.shape[-1]))
    elif source.endswith(('.dscalar.nii', '.dseries.nii')):
        data = data.T
    elif (source.endswith('.nii.gz')) | (source.endswith('.nii') & source.count('.') == 1):
        pass
    else:
        raise Exception('Wrong data format')
    return img, data, header     

def _get_label_data(source):
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
