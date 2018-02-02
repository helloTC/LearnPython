import nibabel as nib
from nibabel import freesurfer
import numpy as np

class Region(object):
    def __init__(self, name, layer = None, space_name = None, hemisphere = None):
        self.name = name
        self.layer = layer
        self.space = space_name
        self.hemisphere = hemisphere

    def __add__(self):
        pass

    def __sub__(self):
        pass

    def __setattr__(self, item, value):
        object.__setattr__(self, item, value)

    def __getattr__(self, item):
        if item not in self.__dict__:
 	    return None

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, layer_value):
        if layer_value is not None:
            if not isinstance(layer_value, int):
                raise ValueError('Layer value must be an integer!')
            if layer_value < 1 | layer_value > 7:
                raise ValueError('Layer value must be in range of 1-7')
        else:
            pass
        self._layer = layer_value

    def load_geometry(self, source, surf_type):
        """
        """
        if self.geometry is None:
            self.geometry = {}
        coordinate, face = _load_geometry_data(source)
        self.geometry['coordinate'] = coordinate
        self.geometry['face'] = face
        self.geometry['surf_type'] = surf_type

    def set_geometry(self, coordinate, face, surf_type):
        """
        """
        self.geometry['coordinate'] = coordinate
        self.geometry['face'] = face
        self.geometry['surf_type'] = surf_type

    def get_geometry(self, surf_type):
        """
        """
        if self.geometry is not None:
             return self.geometry['coordinate'], self.geometry['face'], self.geometry[surf_type]

    def get_geometry_key(self):
        try:
            return self.geometry.keys()
        except AttributeError:
            raise Exception('Load geometry data first!')

    def mask_geometry(self,mask):
        pass

    def load_scalar(self, source, key):
        if self.scalar is None:
             self.scalar = {}
        # whether to load header or not?     
        if self.scalar.has_key(key):
            raise Exception('')
        if isinstance(source, str):
            scalar_data = _load_scalar_data(source)
            if self.geometry is not None:
                if scalar_data.shape[0] != self.geometry['coordinate'].shape[0]:
                    raise Exception('Mismatch between geometry and scalar data')
            self.scalar[key] = scalar_data     
        elif isinstance(source, np.ndarray):
            self.scalar[key] = source
        else:
            raise Exception('')
        
    def get_scalar(self, key):
        try:
            return self.scalar[key]  
        except TypeError:
            raise Exception('Load scalar data first!')                         
   
    def get_scalar_key(self):
        try:
            return  self.scalar.keys()
        except AttributeError:
            raise Exception('Load scalar data first!')

def _load_scalar_data(source):
    """
    """
    if source.endswith(('.curv', '.sulc', '.volume', '.thickness', '.area')):
        data = np.expand_dims(freesurfer.read_morph_data(source), axis=-1)
    elif source.endswith(('.shape.gii', '.func.gii')):
        data = np.expand_dims(nib.load(source).darrays[0].data, axis=-1)
    elif source.endswith(('.mgz', '.mgh')):
        data = nib.load(source).get_data()
        data = data.reshape((data.shape[0], data.shape[-1]))
    elif source.endswith(('.dscalar.nii', '.dseries.nii')):
        data = nib.load(source).get_data()
        data = data.T
    elif (source.endswith('.nii.gz')) | (source.endswith('.nii') & source.count('.') == 1):
        data = nib.load(source).get_data()
    elif source.endswith('.label.gii'):
        data = np.expand_dims(nib.load(source).darrays[0].data,axis=-1)
    elif source.endswith('.dlabel.nii'):
        data = nib.load(source).get_data().T
    elif source.endswith('.label'):
        data = np.expand_dims(freesurfer.read_label(source),axis=-1)
    elif source.endswith('.annot'):
        data, _, _ = freesurfer.read_annot(source) 
    else:
        raise Exception('Wrong data format')
    return data   

def _load_geometry_data(source):
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
