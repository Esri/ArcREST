from __future__ import absolute_import
import json
from ._spatialreference import SpatialReference
from ._point import Point
from ._abstract import AbstractGeometry
try:
    import arcpy
    arcpyFound = True
except ImportError:
    arcpyFound = False

__version__ = "1.0.0"
__all__ = ['Polyline']

########################################################################
class Polyline(AbstractGeometry):
    """
    A polyline contains an array of paths or curvePaths and a spatialReference

    JSON Syntax

    {
      "hasZ" : true | false,
      "hasM" : true | false,
      "paths" : [[[<x11>, <y11>, <z11>, <m11>],...,[<x1N>, <y1N>, <z1N>, <m1N>]],
                ,...,[[<xk1>, <yk1>, <zk1>, <mk1>],...,[<xkM>, <ykM>, <zkM>, <mkM>]]],
      "spatialReference" : {<spatialReference>}
    }

    JSON Syntax Examples:

    A 2D polyline
    {
      "paths" : [[[-97.06138,32.837],[-97.06133,32.836],[-97.06124,32.834],[-97.06127,32.832]],
                 [[-97.06326,32.759],[-97.06298,32.755]]],
      "spatialReference" : {"wkid" : 4326}
    }

    A 2D polyline with m-values (note that the 2nd path does not have m-values defined)
    {
      "hasM" : true,
      "paths" : [[[-97.06138,32.837,5],[-97.06133,32.836,6],[-97.06124,32.834,7],[-97.06127,32.832,8]],
                 [[-97.06326,32.759],[-97.06298,32.755]]],
      "spatialReference" : {"wkid" : 4326}
    }

    An empty polyline
    {
      "paths" : [ ]
    }
    """
    _paths = None
    _sr = None
    _hasZ = None
    _hasM = None
    #----------------------------------------------------------------------
    def __init__(self, paths=None, spatialreference=None,
                 hasM=False, hasZ=False, **kwargs):
        self._hasM = hasM
        self._hasZ = hasZ
        self._paths = []
        self._parts = {}
        if isinstance(spatialreference, SpatialReference):
            self._sr = spatialreference
        self._paths.append(self._validate_paths(paths))
    #----------------------------------------------------------------------
    def _validate_paths(self, paths):
        _geoms = []
        if isinstance(paths, (list, tuple)):
            for path in paths:
                if isinstance(path, (list, tuple)):
                    _geoms.append(self._validate_paths(paths=path))
                elif isinstance(path, Point):
                    _geoms.append(path)
                else:
                    _geoms.append(self._pl_to_paths(geom=path))
                del path
        elif arcpyFound and \
             isinstance(paths, arcpy.Polyline):
            print 'arcpy.Polyline'
        elif isinstance(paths, Point):
            return paths
        return _geoms
    #----------------------------------------------------------------------
    def _pl_to_paths(self, geom):
        """ converts a geometry object to a common.Geometry object """
        if arcpyFound and isinstance(geom, arcpy.Polyline):
            feature_geom = []
            fPart = []
            for part in geom:
                fPart = []
                for pnt in part:
                    fPart.append(Point(coord=[pnt.X, pnt.Y, pnt.Z],
                          spatialreference=SpatialReference.from_json(
                              geom.spatialReference.JSON),
                          m=pnt.M))
                feature_geom.append(fPart)
            return feature_geom
        return None
    #----------------------------------------------------------------------
    def __iter__(self):
        """iterates the paths"""
        for path in self._paths:
            yield [p.as_list for p in path]
    #----------------------------------------------------------------------
    def clear(self):
        """removes all points from the Multipoint geometry"""
        self._paths = []
    #----------------------------------------------------------------------
    def append(self, path):
        """adds a new line to the path"""
        self._paths.append(path)
    #----------------------------------------------------------------------
    def __len__(self):
        """returns the point count"""
        return len(self._paths)
    #----------------------------------------------------------------------
    def __eq__(self, value):
        """determines if two objects are equal"""
        if isinstance(value, Polyline):
            return len(value) == len(self)
        return False
    #----------------------------------------------------------------------
    def __ne__(self, value):
        """determines if two valuesare not equal"""
        return not self.__eq__(value)
    #----------------------------------------------------------------------
    def __lt__(self, value):
        if isinstance(value, Polyline):
            return self.distance < value.distance
        return False
    #----------------------------------------------------------------------
    def __le__(self, value):
        if isinstance(value, Polyline):
            return self.distance <= value.distance
        return False
    #----------------------------------------------------------------------
    def __gt__(self, value):
        if isinstance(value, Polyline):
            return self.distance > value.distance
        return False
    #----------------------------------------------------------------------
    def __ge__(self, value):
        if isinstance(value, Polyline):
            return self.distance >= value.distance
        return False
    #----------------------------------------------------------------------
    @property
    def distance(self):
        def calculateDistance(x1,y1,x2,y2):
            import math
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return dist
        distance = 0
        for part in self._paths:
            for path in part:
                path = [p.as_list for p in path]
                if len(path) == 2:
                    distance += calculateDistance(x1=path[0][0], y1=path[0][1],
                                                  x2=path[1][0], y2=path[1][1])
                else:
                    for pt in range(len(path)):
                        print pt, pt+1, len(path)
                        if pt + 1 < len(path):
                            distance += calculateDistance(
                                x1=path[pt][0], y1=path[pt][1],
                                x2=path[pt+1][0], y2=path[pt+1][1])
                        del pt
                del path
        return distance
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the point count"""
        return json.dumps(self.as_dict)
    #----------------------------------------------------------------------
    def __geo_interface__(self):
        return self.as_dict
    #----------------------------------------------------------------------
    def __getitem__(self, index):
        """slicing operation"""
        if len(self) == 0:
            return []

        if isinstance(index, slice):
            return self._paths[index]
        else:
            if index <= len(self) -1:
                return self._paths[index]
            else:
                raise ValueError("Invalid index")
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return self._sr
    #----------------------------------------------------------------------
    @spatialReference.setter
    def spatialReference(self, value):
        """returns the geometry spatial reference"""
        if isinstance(value, SpatialReference):
            self._sr = value
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryPolyline"
    #----------------------------------------------------------------------
    @staticmethod
    def from_json(value):
        if isinstance(value, str):
            sr = None
            j = json.loads(value.strip())
            if "spatialReference" in j:
                sr = SpatialReference.from_json(j['spatialReference'])
                del j['spatialReference']
            return Polyline(spatialreference=sr, **j)
        elif isinstance(value, dict):
            if "spatialReference" in j:
                sr = SpatialReference.from_json(value['spatialReference'])
                del value['spatialReference']
            return Polyline(spatialreference=sr, **value)
        else:
            raise ValueError("Invalid input of type: {}. Check the item's format.".format(type(value)))
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        return json.dumps(self.as_dict)
    #----------------------------------------------------------------------
    @property
    def as_arcpy(self):
        """ returns the Point as an ESRI arcpy.MultiPoint object """
        if arcpyFound == False:
            raise Exception("ArcPy is required to use this function")
        return arcpy.AsShape(self.__str__(), True)
    #----------------------------------------------------------------------
    @property
    def as_list(self):
        """ returns the MultiPoint Geometry Objects """
        return self.as_dict['paths']
    #----------------------------------------------------------------------
    @property
    def as_dict(self):
        """ returns the object as a python dictionary """

        template = {
                "hasM" : self._hasM,
                "hasZ" : self._hasZ,
                "paths" : [],
                "spatialReference" : None
            }
        if self._sr:
            template['spatialReference'] = self._sr.as_dict
        for part in self._paths:
            for pt in part:
                if isinstance(pt, (list, tuple)):
                    template['paths'].append([p.as_list for p in pt])
                else:
                    template['paths'].append(pt.as_list)
        return template
