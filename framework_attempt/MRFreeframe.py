import nibabel as nib
from nibabel import freesurfer
import numpy as np

class Region(object):
    
    _defaults = ['_name', '_layer', 'hemi', 'header', 'space']

    def __init__(self, source):
        self._source = source
        for key in self._defaults:
            if key not in self.__dict__:
                self.__dict__.update({key:None})

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, namestr):
        self._name = namestr

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, layernum):
        self._layer = layernum    

    def setspace(self, space_name = 'MNI'):
        self.space = space_name
        if space_name == 'MNI':
            self.shape = (91,109,91)
        elif space_name == 'fsaverage':
            self.shape = (163842,1)
        elif space_name == 'fsaverage5':
            self.shape = (10242,1)
        else:
            self.shape = None
        if 'data' in self.__dict__:
            self.shape = self.data.shape
            self.space = None

    def get_data(self):
        self.img = nib.load(self._source)
        self.data = self.img.get_data()
        self.shape = self.data.shape
        self.sethemi()

    def sethemi(self, hemi=None):
        if ('lh' in self._source) & ('rh' in self._source):
            self.hemi = 'both'
        elif ('lh' in self._source) & ('rh' not in self._source):
            self.hemi = 'lh'
        elif ('lh' not in self._source) & ('rh' in self._source):
            self.hemi = 'rh'
        else:
            self.hemi = hemi

    def get_header(self):
        self.header = self.img.get_header()

    def regionsize(self):
        pass

class Geometry(Region):
    def __init__(self):
        super(Geometry, self).__init__()       

    def get_data(self, source):
        if source.endswith(('.inflated', '.pial', '.white', '.orig')):
            self.coordinate, self.face = freesurfer.read_geometry(source)
        elif source.endswith('.surf.gii'):
            self.coordinate = nib.load(source).darrays[0].data
            self.face = nib.load(source).darrays[1].data
        else:
            raise Exception('Wrong data formats')

    def calc_distance(self):
        pass

class Morphology(Region):
    def __init__(self, source):
        super(Morphology, self).__init__(source)       

    def get_data(self):
        if self._source.endswith(('.curv', '.sulc', '.volume', '.thickness', '.area')):
            self.data = np.expand_dims(freesurfer.read_morph_data(self._source),axis=-1)
        elif self._source.endswith('.shape.gii'):
            self.data = np.expand_dims(nib.load(self._source).darrays[0],axis=-1)
        else:
            raise Exception('Wrong data format')            

    def data_type(self):
        if self._source.endswith(('.curv', '.sulc', '.volume', '.thickness', '.area')):
            self.datatype = self._source.split('.')[-1]
        elif self._source.endswith('.shape.gii'):
            self.datatype = self._source.split('.')[2]
        else:
            raise Exception('wrong data format')  

    def get_signals(self):
        pass
     
class Function(Region):
    def __init__(self, source):
        super(Function, self).__init__(source)      
    
    def get_signals(self):
        pass

class Parcellation(Region):
    def __init__(self, source):
        super(Parcellation, self).__init__(source)

    def get_signals(self):
        pass


class Fiber(object):
    pass

class Participants(object):
    def __init__(self, source):
        geocls = Geometry(source)
        morphcls = Morpohology(source)
        funcls = Function(source)
        parcls = Parcellation(source)
        fibcls = Fiber(source)

    def methods(self):
        pass


