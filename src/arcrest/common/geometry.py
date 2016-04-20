from __future__ import absolute_import
from __future__ import print_function
import json
try:
    import arcpy
    arcpyFound = True
except:
    arcpyFound = False
import types


from .._abstract import abstract
#----------------------------------------------------------------------
def _date_handler(obj):
    if isinstance(obj, datetime.datetime):
        return local_time_to_online(obj)
    else:
        return obj
########################################################################
class SpatialReference(abstract.AbstractGeometry):
    """ creates a spatial reference instance """
    _wkid = None
    _wkt = None
    #----------------------------------------------------------------------
    def __init__(self, wkid=None,wkt=None):
        """Constructor"""
        self._wkid = wkid
        self._wkt = wkt
    #----------------------------------------------------------------------
    @property
    def wkid(self):
        """ get/set the wkid """
        return self._wkid
    @wkid.setter
    def wkid(self, wkid):
        """ get/set the wkid """
        self._wkid = wkid
    #----------------------------------------------------------------------
    @property
    def wkt(self):
        """ get/set the wkt """
        return self._wkt
    @wkt.setter
    def wkt(self, wkt):
        """ get/set the wkt """
        self._wkt = wkt
    @property
    def asDictionary(self):
        """returns the wkid id for use in json calls"""
        if self._wkid == None and self._wkt is not None:
            return {"wkt": self._wkt}
        else:
            return {"wkid": self._wkid}
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the wkid id for use in json calls"""
        if self._wkid == None and self._wkt is not None:
            return {"wkt": self._wkt}
        else:
            return {"wkid": self._wkid}

########################################################################
class Point(abstract.AbstractGeometry):
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
    _wkt = None
    _json = None
    _geom = None
    _dict = None
    #----------------------------------------------------------------------
    def __init__(self, coord, wkid=None, wkt=None, z=None, m=None):
        """Constructor"""
        if isinstance(coord, list):
            self._x = float(coord[0])
            self._y = float(coord[1])
        elif arcpyFound and isinstance(coord, arcpy.Geometry):
            self._x = coord.centroid.X
            self._y = coord.centroid.Y
            self._z = coord.centroid.Z
            self._m = coord.centroid.M
            self._geom = coord.centroid

        self._wkid = wkid
        self._wkt = wkt
        if not z is None:
            self._z = float(z)
        if not m is None:
            self._m = m
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the object as a string """
        return json.dumps(self.asDictionary,
                          default=_date_handler)
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        if self._wkid == None and self._wkt is not None:
            return {"wkt": self._wkt}
        else:
            return {"wkid": self._wkid}
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
        if arcpyFound == False:
            raise Exception("ArcPy is required to use this function")
        return arcpy.AsShape(self.asDictionary, True)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a python dictionary """
        #
        template = {"x" : self._x,
                    "y" : self._y,
                    "spatialReference" : self.spatialReference
                    }
        if not self._z is None:
            template['z'] = self._z
        if not self._m is None:
            template['z'] = self._m
        return template
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
    #----------------------------------------------------------------------
    @property
    def X(self):
        """ gets the X coordinate """
        return self._x
    #----------------------------------------------------------------------
    @X.setter
    def X(self, value):
        """sets the X coordinate"""
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._x = value
    #----------------------------------------------------------------------
    @property
    def Y(self):
        """ gets the Y Coordinate """
        return self._y
    #----------------------------------------------------------------------
    @Y.setter
    def Y(self, value):
        """ sets the Y coordinate """
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._y = value
    #----------------------------------------------------------------------
    @property
    def Z(self):
        """ gets the Z Coordinate """
        return self._z
    #----------------------------------------------------------------------
    @Z.setter
    def Z(self, value):
        """ sets the Z coordinate """
        if isinstance(value, (int, float,
                              long, types.NoneType)):
            self._z = value
    #----------------------------------------------------------------------
    @property
    def wkid(self):
        """ gets the wkid """
        return self._wkid
    #----------------------------------------------------------------------
    @wkid.setter
    def wkid(self, value):
        """ sets the wkid """
        if isinstance(value, (int,
                              long)):
            self._wkid = value
    #----------------------------------------------------------------------
    @property
    def wkt(self):
        """ get/set the wkt """
        return self._wkt
    @wkt.setter
    def wkt(self, wkt):
        """ get/set the wkt """
        self._wkt = wkt
########################################################################
class MultiPoint(abstract.AbstractGeometry):
    """ Implements the ArcGIS JSON MultiPoint Geometry Object """
    _geom = None
    _json = None
    _dict = None
    _wkid = None
    _wkt = None
    _points = None
    _hasZ = False
    _hasM = False
    #----------------------------------------------------------------------
    def __init__(self, points, wkid=None, wkt=None, hasZ=False, hasM=False):
        """Constructor"""
        if isinstance(points, list):
            self._points = points
        elif arcpyFound and isinstance(points, arcpy.Geometry):
            self._points = self.__geomToPointList(points)
        self._wkid = wkid
        self._wkt = wkt
        self._hasZ = hasZ
        self._hasM = hasM
    #----------------------------------------------------------------------
    def __geomToPointList(self, geom):
        """ converts a geometry object to a common.Geometry object """
        if arcpyFound and isinstance(geom, arcpy.Multipoint):
            feature_geom = []
            fPart = []
            for part in geom:
                fPart = []
                for pnt in part:
                    fPart.append(Point(coord=[pnt.X, pnt.Y],
                          wkid=geom.spatialReference.factoryCode,
                          z=pnt.Z, m=pnt.M))
                feature_geom.append(fPart)
            return feature_geom
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        if self._wkid == None and self._wkt is not None:
            return {"wkt": self._wkt}
        else:
            return {"wkid": self._wkid}
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
        if arcpyFound == False:
            raise Exception("ArcPy is required to use this function")
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
                "spatialReference" : self.spatialReference
            }
            for pt in self._points:
                template['points'].append(pt.asList)
            self._dict = template
        return self._dict
########################################################################
class Polyline(abstract.AbstractGeometry):
    """ Implements the ArcGIS REST API Polyline Object
        Inputs:
           paths - list - list of lists of Point objects
           wkid - integer - well know spatial reference id
           hasZ - boolean -
           hasM - boolean -
    """
    _paths = None
    _wkid = None
    _wkt = None
    _json = None
    _dict = None
    _geom = None
    _hasZ = None
    _hasM = None
    #----------------------------------------------------------------------
    def __init__(self, paths, wkid=None,wkt=None, hasZ=False, hasM=False):
        """Constructor"""
        if isinstance(paths, list):
            self._paths = paths
        elif arcpyFound and isinstance(paths, arcpy.Geometry):
            self._paths = self.__geomToPointList(paths)
        self._wkid = wkid
        self._wkt = wkt
        self._hasM = hasM
        self._hasZ = hasZ
    #----------------------------------------------------------------------
    def __geomToPointList(self, geom):
        """ converts a geometry object to a common.Geometry object """
        if arcpyFound and isinstance(geom, arcpy.Polyline):
            feature_geom = []
            fPart = []
            wkt = None
            wkid = None
            for part in geom:
                fPart = []
                for pnt in part:
                    if geom.spatialReference is None:
                        if self._wkid is None and self._wkt is not None:
                            wkt = self._wkt
                        else:
                            wkid = self._wkid
                    else:
                        wkid = geom.spatialReference.factoryCode
                    fPart.append(Point(coord=[pnt.X, pnt.Y],
                          wkid=wkid,
                          wkt=wkt,
                          z=pnt.Z, m=pnt.M))
                feature_geom.append(fPart)
            return feature_geom
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        if self._wkid == None and self._wkt is not None:
            return {"wkt": self._wkt}
        else:
            return {"wkid": self._wkid}
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
        if arcpyFound == False:
            raise Exception("ArcPy is required to use this function")
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
                "spatialReference" : self.spatialReference
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
class Polygon(abstract.AbstractGeometry):
    """ Implements the ArcGIS REST JSON for Polygon Object """
    _rings = None
    _wkid = None
    _wkt = None
    _json = None
    _dict = None
    _geom = None
    _hasZ = None
    _hasM = None
    #----------------------------------------------------------------------
    def __init__(self, rings, wkid=None,wkt=None, hasZ=False, hasM=False):
        """Constructor"""
        if isinstance(rings, list):
            self._rings = rings
        elif arcpyFound and isinstance(rings, arcpy.Geometry):
            self._rings = self.__geomToPointList(rings)
##            self._json = rings.JSON
##            self._dict = _unicode_convert(json.loads(self._json))
        self._wkid = wkid
        self._wkt = wkt
        self._hasM = hasM
        self._hasZ = hasZ
    #----------------------------------------------------------------------
    def __geomToPointList(self, geom):
        """ converts a geometry object to a common.Geometry object """
        sr = geom.spatialReference
        wkid = None
        wkt = None
        if sr is None:
            if self._wkid is None and self._wkt is not None:
                wkt = self._wkt
            else:
                wkid = self._wkid
        else:
            wkid = sr.factoryCode
        g = json.loads(geom.JSON)
        top = []
        for gring in g['rings']:
            ring = []
            for g in gring:
                ring.append(Point(coord=g, wkid=wkid, wkt=wkt, z=None, m=None))
            top.append(ring)
        return top
        #if isinstance(geom, arcpy.Polygon):
            #feature_geom = []
            #fPart = []
            #for part in geom:
                #fPart = []
                #for pnt in part:
                    #if geom.spatialReference is None:
                        #wkid = self._wkid
                    #else:
                        #wkid = geom.spatialReference.factoryCode
                    #fPart.append(Point(coord=[pnt.X, pnt.Y],
                          #wkid=wkid,
                          #z=pnt.Z, m=pnt.M))
                #feature_geom.append(fPart)
            #return feature_geom
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        if self._wkid == None and self._wkt is not None:
            return {"wkt": self._wkt}
        else:
            return {"wkid": self._wkid}
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
        if arcpyFound == False:
            raise Exception("ArcPy is required to use this function")
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
                "spatialReference" : self.spatialReference
            }
            for part in self._rings:
                lpart = []
                for pt in part:
                    if isinstance(pt, list):
                        lpart.append(pt)
                    elif isinstance(pt, Point):
                        lpart.append(pt.asList)
                template['rings'].append(lpart)
                del lpart
            self._dict = template
        return self._dict
########################################################################
class Envelope(abstract.AbstractGeometry):
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
    _wkt = None
    #----------------------------------------------------------------------
    def __init__(self, xmin, ymin, xmax, ymax, wkid=None, wkt=None,
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
        self._wkt = wkt
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        if self._wkid == None and self._wkt is not None:
            return {"wkt": self._wkt}
        else:
            return {"wkid": self._wkid}
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
            "spatialReference" : self.spatialReference
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
    def value(self):
        """ returns the envelope as a dictionary """
        template = {
            "xmin" : self._xmin,
            "ymin" : self._ymin,
            "xmax" : self._xmax,
            "ymax" : self._ymax,
            "spatialReference" : self.spatialReference
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
    def __str__(self):
        """returns object as string"""
        return self.asJSON
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
        return Polygon(rings=ring,
                       wkid=self._wkid,
                       wkt=self._wkid,
                       hasZ=False,
                       hasM=False).asArcPyObject