# Tim Cornwell <realtimcornwell@gmail.com>
#
# Definition of structures needed by the function interface. These are mostly
# subclasses of astropy classes.
#

from astropy.table import Table
import numpy

class Configuration:
    """ Describe a Configuration
    
    """
    
    def __init__(self, name='', data=None, location=None,
                 names="%s", xyz=None, mount="alt-az"):

        # Defaults
        if data is None and not xyz is None:
            nants = xyz.shape[0]
            if isinstance(names, str):
                names = [names % ant for ant in range(nants)]
            if isinstance(mount, str):
                mount = numpy.repeat(mount, nants)
            data = Table(      [ names,   xyz,   mount],
                         names=['names', 'xyz', 'mount'])

        self.name = name
        self.data = data
        self.location = location

    @property
    def names(self): return self.data['names']
    @property
    def xyz(self): return self.data['xyz']
    @property
    def mount(self): return self.data['mount']

class GainTable:
    """ Gain table with data: time, antenna, gain[:,chan,pol] columns
    """
    
    # TODO: Implement gaintables with Jones and Mueller matrices
    
    def __init__(self):
        self.data = None
        self.frequency = None


class Image:
    """Image class with Image data (as a numpy.array) and optionally the AstroPy WCS.

    Many operations can be done conveniently using numpy arl on Image.data.

    Most of the imaging arl require an image in canonical format:
    - 4 axes: RA, DEC, POL, FREQ

    The conventions for indexing in WCS and numpy are opposite.
    - In astropy.wcs, the order is (longitude, latitude, polarisation, frequency)
    - in numpy, the order is (frequency, polarisation, latitude, longitude)

    """
    
    def __init__(self):
        self.data = None
        self.wcs = None


class SkyComponent:
    """ A single SkyComponent with direction, flux, shape, and params for the shape
    
    """
    # TODO: fill out SkyComponent
    def __init__(self):
        self.direction = None   # SkyCoord
        self.frequency = None   # numpy.array [nchan]
        self.name = None        # user friendly name
        self.flux = None        # numpy.array [nchan, npol]
        self.shape = None       # str e.g. 'Point' 'Gaussian'
        self.params = None      # numpy.array shape dependent parameters


class SkyModel:
    """ A skymodel consisting of a list of images and a list of skycomponents
    
    """
    # TODO: Fill out SkyModel

    def __init__(self):
        self.images = []    # collection of numpy arrays
        self.components = []    # collection of SkyComponents


class Visibility:
    """ Visibility table class

    Visibility with uvw, time, a1, a2, vis, weight Columns in
    an astropy Table along with an attribute to hold the frequencies
    and an attribute to hold the direction.

    Visibility is defined to hold an observation with one set of frequencies and one
    direction.

    The data column has vis:[row,nchan,npol], uvw:[row,3]
    """

    def __init__(self, data=None, frequency=None, phasecentre=None, configuration=None,
                 uvw=None, time=None, a1=None, a2=None, vis=None, weight=None):

        if data is None and not vis is None:
            data = Table(      [ uvw,   time,   a1,   a2,   vis,   weight],
                         names=['uvw', 'time', 'a1', 'a2', 'vis', 'weight'])

        self.data = data            # Astropy.table with columns uvw, time, a1, a2, vis, weight
        self.frequency = frequency  # numpy.array [nchan]
        self.phasecentre = phasecentre # Phase centre of observation
        self.configuration = configuration # Antenna/station configuration

    @property
    def uvw(self): return self.data['uvw']
    @property
    def u(self):   return self.data['uvw'][:,0]
    @property
    def v(self):   return self.data['uvw'][:,1]
    @property
    def w(self):   return self.data['uvw'][:,2]
    @property
    def time(self): return self.data['time']
    @property
    def a1(self):  return self.data['a1']
    @property
    def a2(self):  return self.data['a2']
    @property
    def vis(self): return self.data['vis']
    @property
    def weight(self): return self.data['weight']

class QA:
    """
    Quality assessment
    """
    
    # TODO: Implement some form of QA receipt and bundling
    
    def __init__(self):
        self.origin = None      # Name of function originating QA assessment
        self.data = None        # Dictionary containing standard fields
        self.context = None     # Context string (TBD)
