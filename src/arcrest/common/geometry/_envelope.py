from __future__ import absolute_import
import json
from ._abstract import AbstractGeometry
from . import SpatialReference
########################################################################
class Envelope(AbstractGeometry):
    """
       An envelope is a rectangle defined by a range of values for each
       coordinate and attribute. It also has a spatialReference field.
       The fields for the z and m ranges are optional.
    """
    _json = None
    _dict = None
    _geom = None
    _xmin = None
    _ymin = None
    _zmin = None
    _mmin = None
    _xmax = None
    _ymax = None
    _zmax = None
    _mmax = None
    _sr = None
    #----------------------------------------------------------------------
    def __init__(self, xmin, ymin, xmax, ymax, sr=None,
                 zmin=None, zmax=None, mmin=None, mmax=None):
        """Constructor"""
        self._xmin = xmin
        self._ymin = ymin
        self._zmin = zmin
        self._mmin = mmin
        self._xmax = xmax
        self._ymax = ymax
        self._zmax = zmax
        self._mmax = mmax
        if isinstance(sr, SpatialReference):
            self._sr = sr
        elif isinstance(sr, dict):
            self._sr = SpatialReference.from_json(value=json.dumps(sr))
        else:
            self._sr = None
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return self._sr
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryEnvelope"
    #----------------------------------------------------------------------
    @property
    def as_dict(self):
        """ returns the envelope as a dictionary """
        template = {
            "xmin" : self._xmin,
            "ymin" : self._ymin,
            "xmax" : self._xmax,
            "ymax" : self._ymax,
            "spatialReference" : self._sr.as_dict
        }
        if self._zmax is not None and \
           self._zmin is not None:
            template['zmin'] = self._zmin
            template['zmax'] = self._zmax

        if self._mmin is not None and \
           self._mmax is not None:
            template['mmax'] = self._mmax
            template['mmin'] = self._mmin

        return template
    #----------------------------------------------------------------------
    @property
    def xmin(self):
        """ gets the xmin coordinate """
        return self._xmin
    #----------------------------------------------------------------------
    @xmin.setter
    def xmin(self, value):
        """sets the xmin coordinate"""
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._xmin = value
    #----------------------------------------------------------------------
    @property
    def ymin(self):
        """ gets the ymin Coordinate """
        return self._ymin
    #----------------------------------------------------------------------
    @ymin.setter
    def ymin(self, value):
        """ sets the y coordinate """
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._ymin = value
    #----------------------------------------------------------------------
    @property
    def xmax(self):
        """ gets the xmax coordinate """
        return self._xmax
    #----------------------------------------------------------------------
    @xmax.setter
    def xmax(self, value):
        """sets the xmax coordinate"""
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._xmax = value
    #----------------------------------------------------------------------
    @property
    def ymax(self):
        """ gets the ymax Coordinate """
        return self._ymax
    #----------------------------------------------------------------------
    @ymax.setter
    def ymax(self, value):
        """ sets the ymax coordinate """
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._ymax = value

    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return self.as_json
    #----------------------------------------------------------------------
    @property
    def as_json(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.as_dict,
                               default=_date_handler)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    def __lt__(self, value):
        """determines if the values is less than another object"""
        if isinstance(value, Envelope):
            return self.value < value.area
        return False
    #----------------------------------------------------------------------
    def __le__(self, value):
        """determines if the values is less than or equal to another object"""
        if isinstance(value, Envelope):
            return self.area <= value.area
        return False
    #----------------------------------------------------------------------
    def __gt__(self, value):
        """determines if the value object is greater than another object"""
        if isinstance(value, Envelope):
            return self.area > value.area
        return False
    #---------------------------------------------------------------------
    def _distance(self, x1,y1,x2,y2):
        """calculates simple distance"""
        import math
        return math.sqrt((math.pow((x2-x1), 2) + math.pow((y2-y1), 2)))
    #---------------------------------------------------------------------
    @property
    def area(self):
        """returns value in square units of the envelope"""
        xmin = value.as_dict['xmin']
        ymin = value.as_dict['ymin']
        xmax = value.as_dict['xmax']
        ymax = value.as_dict['ymax']
        vertical_distance = self._distance(x1=xmin, y1=ymin,
                                           x2=xmin, y2=ymax)
        horizontal_distance = self._distance(x1=xmin, y1=ymin,
                                             x2=xmax, y2=ymin)
        return vertical_distance * horizontal_distance
    #---------------------------------------------------------------------
    def __ge__(self, value):
        """determines if the value object is greater than or equal to another object"""
        if isinstance(value, Envelope):
            return self.area >= value.area
        return False
    #----------------------------------------------------------------------
    def __eq__(self, value):
        """determines if the values is equal to other object"""
        return (self.as_dict == value.as_dict)
    #----------------------------------------------------------------------
    def __ne__(self, value):
        """determines if the values is not equal to other object"""
        if isinstance(value, Envelope):
            return not (self.as_dict == value.as_dict)
        return False
    #----------------------------------------------------------------------
    def __iter__(self):
        for k,v in self.as_dict.items():
            yield k,v
    #----------------------------------------------------------------------
    def __geo_interface__(self):
        return self.as_json
    #----------------------------------------------------------------------
    @classmethod
    def from_json(value):
        """creates object from JSON string"""
        raise NotImplementedError()