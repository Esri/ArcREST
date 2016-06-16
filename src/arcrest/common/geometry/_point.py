"""
A point contains x and y fields along with a spatialReference field. A
point can also contain m and z fields. A point is empty when its x field is
present and has the value null or the string "NaN". An empty point has no
location in space.

Examples:

A 2D point
{"x" : -118.15, "y" : 33.80, "spatialReference" : {"wkid" : 4326}}

A 3D point
{"x" : -118.15, "y" : 33.80, "z" : 10.0, "spatialReference" : {"wkid" : 4326}}

An empty point
{"x" : null, "spatialReference" : {"wkid" : 4326}}

An empty point
{"x" : "NaN", "y" : 22.2, "spatialReference" : {"wkid" : 4326}}
"""

from __future__ import absolute_import
from __future__ import print_function
import json
import types
from six import iteritems
from ._spatialreference import SpatialReference
from ._abstract import AbstractGeometry
try:
    import arcpy
    arcpyFound = True
except ImportError:
    arcpyFound = False
__version__ = "4.0.0"
__all__ = ['Point']
########################################################################
class Point(AbstractGeometry):
    """ Point Geometry
    A point contains x and y fields along with a spatialReference field.
    A point can also contain m and z fields. A point is empty when its x
    field is present and has the value null or the string 'NaN'. An empty
    point has no location in space.
        Inputs:
           :coord: - list of [x,y, [z]] pair or arcpy.Point Object
           :spatialreference:
           :m: - m value
           :kwargs: optional keys that allow user to pass a JSON geomtry
            object into the class to create the object.
    """
    _x = None
    _y = None
    _z = None
    _m = None
    _sr = None
    #----------------------------------------------------------------------
    def __init__(self, coord=None, spatialreference=None, m=None, **kwargs):
        """Constructor"""

        if isinstance(coord, list):
            if len(coord) == 2:
                self._x = float(coord[0])
                self._y = float(coord[1])
                self._z = None
            elif len(coord) == 3:
                self._x = float(coord[0])
                self._y = float(coord[1])
                self._z = float(coord[2])
        elif arcpyFound and isinstance(coord, arcpy.Geometry):
            self._x = coord.centroid.x
            self._y = coord.centroid.y
            self._z = coord.centroid.z
            self._m = coord.centroid.M
            self._geom = coord.centroid
        if spatialreference:
            if arcpyFound and \
               isinstance(spatialreference, arcpy.SpatialReference):
                self._sr = SpatialReference(wkid=spatialreference.factoryCode)
            elif isinstance(spatialreference, SpatialReference):
                self._sr = spatialreference
        if not m is None:
            self._m = m
        if "x" in kwargs:
            self._x = kwargs['x']
        if "y" in kwargs:
            self._y = kwargs['y']
        if "z" in kwargs:
            self._z = kwargs['z']
        if "m" in kwargs:
            self._m = kwargs
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the object as a string """
        return json.dumps(self.as_dict)
    #----------------------------------------------------------------------
    def __geo_interface__(self):
        """returns object as key/value pair"""
        return self.as_dict
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns the key/value items in a Point"""
        for k,v in iteritems(self.as_dict):
            yield k, v
    #----------------------------------------------------------------------
    def __eq__(self, value):
        """compares the Points coordinate to determine if equal"""
        if isinstance(value, Point):
            return [value.x, value.y, value.z, value.m] == \
                   [self.x, self.y, self.z, self.m]
        return False
    #----------------------------------------------------------------------
    def __ne__(self, value):
        """compares the Points coordinate to determine if not equal"""
        if isinstance(value, Point):
            return [value.x, value.y, value.z, value.m] != \
                   [self.x, self.y, self.z, self.m]
        return False
    #----------------------------------------------------------------------
    def __ge__(self, value):
        raise NotImplementedError("Greater Than Equal To Not Implemented")
    #----------------------------------------------------------------------
    def __gt__(self, value):
        raise NotImplementedError("Greater Than Not Implemented")
    #----------------------------------------------------------------------
    def __lt__(self, value):
        raise NotImplementedError("Less Than Not Implemented")
    #----------------------------------------------------------------------
    def __le__(self, value):
        raise NotImplementedError("Less Than Equal To Not Implemented")
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return self._sr
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryPoint"
    #----------------------------------------------------------------------
    @property
    def as_json(self):
        """ returns a geometry as JSON """
        return self.__str__()
    #----------------------------------------------------------------------
    @property
    def as_arcpy(self):
        """ returns the Point as an ESRI arcpy.Point object """
        if arcpyFound == False:
            raise ImportError("ArcPy is required to use this function")
        return arcpy.AsShape(self.as_dict, True)
    #----------------------------------------------------------------------
    @property
    def as_dict(self):
        """ returns the object as a python dictionary """
        template = {"x" : self._x,
                    "y" : self._y}
        if not self._sr is None:
            template["spatialReference"] = self.spatialReference.as_dict
        else:
            template["spatialReference"] = None
        if not self._z is None:
            template['z'] = self._z
        if not self._m is None:
            template['z'] = self._m
        return template
    #----------------------------------------------------------------------
    @property
    def as_list(self):
        """ returns a Point value as a list of [x,y,<z>,<m>] """
        base = [self._x, self._y]
        if not self._z is None:
            base.append(self._z)
        elif not self._m is None:
            base.append(self._m)
        return base
    #----------------------------------------------------------------------
    @property
    def x(self):
        """ gets the x coordinate """
        return self._x
    #----------------------------------------------------------------------
    @x.setter
    def x(self, value):
        """sets the x coordinate"""
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._x = value
    #----------------------------------------------------------------------
    @property
    def y(self):
        """ gets the y Coordinate """
        return self._y
    #----------------------------------------------------------------------
    @y.setter
    def y(self, value):
        """ sets the y coordinate """
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._y = value
    #----------------------------------------------------------------------
    @property
    def z(self):
        """ gets the z Coordinate """
        return self._z
    #----------------------------------------------------------------------
    @z.setter
    def z(self, value):
        """ sets the z coordinate """
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._z = value
    #----------------------------------------------------------------------
    @property
    def m(self):
        """ gets the m Coordinate """
        return self._m
    #----------------------------------------------------------------------
    @m.setter
    def m(self, value):
        """ sets the m coordinate """
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._m = value
    #----------------------------------------------------------------------
    @staticmethod
    def from_json(value):
        if isinstance(value, str):
            sr = None
            j = json.loads(value.strip())
            if "spatialReference" in j:
                sr = SpatialReference.from_json(j['spatialReference'])
                del j['spatialReference']
            return Point(spatialreference=sr, **j)
