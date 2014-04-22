import json
import arcpy
from base import Geometry
########################################################################
class SpatialReference(object):
    """ creates a spatial reference instance """
    _wkid = None
    #----------------------------------------------------------------------
    def __init__(self, wkid):
        """Constructor"""
        self._wkid = wkid
    #----------------------------------------------------------------------
    @property
    def wkid(self):
        """ get/set the wkid """
        return self._wkid
    @wkid.setter
    def wkid(self, wkid):
        """ get/set the wkid """
        self._wkid = wkid
    @property
    def asDictionary(self):
        """returns the wkid id for use in json calls"""
        return {"wkid": self._wkid}
########################################################################
class Point(Geometry):
    """ Point Geometry
        Inputs:
           coord - list of [X,Y] pair or arcpy.Point Object
           wkid - well know id of spatial references
           z - is the Z coordinate value
           m - m value
    """
    _x = None
    _y = None
    _z = None
    _m = None
    _wkid = None
    _json = None
    _geom = None
    _dict = None
    #----------------------------------------------------------------------
    def __init__(self, coord, wkid, z=None, m=None):
        """Constructor"""
        if isinstance(coord, list):
            self._x = float(coord[0])
            self._y = float(coord[1])
        elif isinstance(coord, arcpy.Geometry):
            self._x = coord.centroid.X
            self._y = coord.centroid.Y
            self._z = coord.centroid.Z
            self._m = coord.centroid.M
            self._json = coord.JSON
            self._geom = coord.centroid
            self._dict = _unicode_convert(json.loads(self._json))
        self._wkid = wkid
        if not z is None:
            self._z = float(z)
        self._m = m
        self._dict = self.asDictionary
        self._json = self.asJSON
        self._geom = self.asArcPyObject
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryPoint"
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary,
                               default=_date_handler)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Point as an ESRI arcpy.Point object """
        return arcpy.AsShape(self.asDictionary, True)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a python dictionary """
        #
        value = self._dict
        if value is None:
            template = {"x" : self._x,
                        "y" : self._y,
                        "spatialReference" : {"wkid" : self._wkid}
                        }
            if not self._z is None:
                template['z'] = self._z
            if not self._m is None:
                template['z'] = self._m
            self._dict = template
        return self._dict
    #----------------------------------------------------------------------
    @property
    def asList(self):
        """ returns a Point value as a list of [x,y,<z>,<m>] """
        base = [self._x, self._y]
        if not self._z is None:
            base.append(self._z)
        elif not self._m is None:
            base.append(self._m)
        return base

########################################################################
class MultiPoint(Geometry):
    """ Implements the ArcGIS JSON MultiPoint Geometry Object """
    _geom = None
    _json = None
    _dict = None
    _wkid = None
    _points = None
    _hasZ = False
    _hasM = False
    #----------------------------------------------------------------------
    def __init__(self, points, wkid, hasZ=False, hasM=False):
        """Constructor"""
        if isinstance(points, list):
            self._points = points
        elif isinstance(points, arcpy.Geometry):
            self._points = json.loads(points.JSON)['points']
            self._json = points.JSON
            self._dict = _unicode_convert(json.loads(self._json))
        self._wkid = wkid
        self._hasZ = hasZ
        self._hasM = hasM
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryMultipoint"
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary,
                               default=_date_handler)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Point as an ESRI arcpy.MultiPoint object """
        return arcpy.AsShape(self.asDictionary, True)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a python dictionary """
        #
        value = self._dict
        if value is None:
            template = {
                "hasM" : self._hasM,
                "hasZ" : self._hasZ,
                "points" : [],
                "spatialReference" : {"wkid" : self._wkid}
            }
            for pt in self._points:
                template['points'].append(pt.asList)
            self._dict = template
        return self._dict
########################################################################
class Polyline(Geometry):
    """ Implements the ArcGIS REST API Polyline Object
        Inputs:
           paths - list - list of lists of Point objects
           wkid - integer - well know spatial reference id
           hasZ - boolean -
           hasM - boolean -
    """
    _paths = None
    _wkid = None
    _json = None
    _dict = None
    _geom = None
    _hasZ = None
    _hasM = None
    #----------------------------------------------------------------------
    def __init__(self, paths, wkid, hasZ=False, hasM=False):
        """Constructor"""
        if isinstance(paths, list):
            self._paths = paths
        elif isinstance(paths, arcpy.Geometry):
            self._paths = json.loads(paths.JSON)['paths']
            self._json = paths.JSON
            self._dict = _unicode_convert(json.loads(self._json))
        self._wkid = wkid
        self._hasM = hasM
        self._hasZ = hasZ
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryPolyline"
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary,
                               default=_date_handler)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Polyline as an ESRI arcpy.Polyline object """
        return arcpy.AsShape(self.asDictionary, True)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a python dictionary """
        value = self._dict
        if value is None:
            template = {
                "hasM" : self._hasM,
                "hasZ" : self._hasZ,
                "paths" : [],
                "spatialReference" : {"wkid" : self._wkid}
            }
            for part in self._paths:
                lpart = []
                for pt in part:
                    lpart.append(pt.asList)
                template['paths'].append(lpart)
                del lpart
            self._dict = template
        return self._dict
########################################################################
class Polygon(Geometry):
    """ Implements the ArcGIS REST JSON for Polygon Object """
    _rings = None
    _wkid = None
    _json = None
    _dict = None
    _geom = None
    _hasZ = None
    _hasM = None
    #----------------------------------------------------------------------
    def __init__(self, rings, wkid, hasZ=False, hasM=False):
        """Constructor"""
        if isinstance(rings, list):
            self._rings = rings
        elif isinstance(rings, arcpy.Geometry):
            self._rings = json.loads(rings.JSON)['rings']
            self._json = rings.JSON
            self._dict = _unicode_convert(json.loads(self._json))
        self._wkid = wkid
        self._hasM = hasM
        self._hasZ = hasZ
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryPolygon"
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary,
                               default=_date_handler)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Polyline as an ESRI arcpy.Polyline object """
        return arcpy.AsShape(self.asDictionary, True)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a python dictionary """
        value = self._dict
        if value is None:
            template = {
                "hasM" : self._hasM,
                "hasZ" : self._hasZ,
                "rings" : [],
                "spatialReference" : {"wkid" : self._wkid}
            }
            for part in self._rings:
                lpart = []
                for pt in part:
                    lpart.append(pt.asList)
                template['rings'].append(lpart)
                del lpart
            self._dict = template
        return self._dict
########################################################################
class Envelope(Geometry):
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
    _wkid = None
    #----------------------------------------------------------------------
    def __init__(self, xmin, ymin, xmax, ymax, wkid,
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
        self._wkid = wkid
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryEnvelope"
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the envelope as a dictionary """
        template = {
            "xmin" : self._xmin,
            "ymin" : self._ymin,
            "xmax" : self._xmax,
            "ymax" : self._ymax,
            "spatialReference" : {"wkid" : self._wkid}
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
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary,
                               default=_date_handler)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Envelope as an ESRI arcpy.Polygon object """
        env = self.asDictionary
        ring = [[
            Point(env['xmin'], env['ymin'], self._wkid),
            Point(env['xmax'], env['ymin'], self._wkid),
            Point(env['xmax'], env['ymax'], self._wkid),
            Point(env['xmin'], env['ymax'], self._wkid)
            ]]
        return Polygon(ring, self._wkid).asArcPyObject