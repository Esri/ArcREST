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

__version__ = "5.0.0"
__all__ = ['MultiPoint']

########################################################################
class MultiPoint(AbstractGeometry):
    """ Implements the ArcGIS JSON MultiPoint Geometry Object
    A multipoint contains an array of points, along with a spatialReference
    field. A multipoint can also have boolean-valued hasZ and hasM fields.
    These fields control the interpretation of elements of the points array.
    Omitting an hasZ or hasM field is equivalent to setting it to false.
    Each element of the points array is itself an array of two, three, or
    four numbers. It will have two elements for 2D points, two or three
    elements for 2D points with Ms, three elements for 3D points, and three
    or four elements for 3D points with Ms. In all cases, the x coordinate
    is at index 0 of a point's array, and the y coordinate is at index 1.
    For 2D points with Ms, the m coordinate, if present, is at index 2. For
    3D points, the Z coordinate is required and is at index 2. For 3D
    points with Ms, the Z coordinate is at index 2, and the M coordinate,
    if present, is at index 3.
    An empty multipoint has a points field with no elements. Empty points
    are ignored.

    JSON Structure:

    {
        "hasM" : true | false,
        "hasZ" : true | false,
        "points" : [[ <x1>, <y1>, <z1>, <m1> ] , [ <x2>, <y2>, <z2>, <m2> ], ... ],
        "spatialReference" : {<spatialReference>}
    }


    """
    _geoms = None
    _sr = None
    _hasZ = None
    _hasM = None
    #----------------------------------------------------------------------
    def __init__(self, points=None, spatialreference=None,
                 hasM=False, hasZ=False, **kwargs):
        """Constructor"""
        self._geoms = []
        self._validate_points(points=points)
        if isinstance(spatialreference, SpatialReference):
            self._sr = spatialreference
        if isinstance(points, list):
            self._points = points
        elif arcpyFound and isinstance(points, arcpy.Geometry):
            self._points = self._validate_points(points)
        self._hasZ = hasZ
        self._hasM = hasM
    #----------------------------------------------------------------------
    def _validate_points(self, points):
        _geoms = []
        if isinstance(points, list):
            for g in points:
                if arcpyFound and isinstance(g, arcpy.Multipoint):
                    _geoms = _geoms + self._mp_to_points(points)
                elif arcpyFound and isinstance(g, arcpy.Geometry):
                    _geoms.append(Point.from_json(g.centroid.JSON))
                elif isinstance(g, Point):
                    _geoms.append(g)
                del g
        elif arcpyFound and isinstance(points, arcpy.Multipoint):
            _geoms = self._mp_to_points(points)
        else:
            raise ValueError("Points must be a list of Point objects or arcpy.MultiPoint object")
        self._geoms = _geoms
    #----------------------------------------------------------------------
    def _mp_to_points(self, geom):
        """ converts a geometry object to a common.Geometry object """
        if arcpyFound and isinstance(geom, arcpy.Multipoint):
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
    @staticmethod
    def from_json(value):
        if isinstance(value, str):
            sr = None
            j = json.loads(value.strip())
            if "spatialReference" in j:
                sr = SpatialReference.from_json(j['spatialReference'])
                del j['spatialReference']
            return MultiPoint(spatialreference=sr, **j)
        elif isinstance(value, dict):
            if "spatialReference" in j:
                sr = SpatialReference.from_json(value['spatialReference'])
                del value['spatialReference']
            return MultiPoint(spatialreference=sr, **value)
        else:
            raise ValueError("Invalid input of type: {}. Check the item's format.".format(type(value)))
    #----------------------------------------------------------------------
    def append(self, value):
        """adds a point to the multipart object"""
        if isinstance(value, Point):
            self._geoms.append(value)
        elif arcpyFound and \
             isinstance(value, arcpy.Geometry):
            self._geoms.append(Point.from_json(value.centroid.JSON))
    #----------------------------------------------------------------------
    def clear(self):
        """removes all points from the Multipoint geometry"""
        self._geoms = []
    #----------------------------------------------------------------------
    def __len__(self):
        """returns the point count"""
        return len(self._geoms)
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the point count"""
        return json.dumps(self.as_dict)
    #----------------------------------------------------------------------
    def __geo_interface__(self):
        return self.as_dict
    #----------------------------------------------------------------------
    def __iter__(self):
        for pt in self.as_list:
            yield pt
    #----------------------------------------------------------------------
    def __eq__(self, value):
        """determines if the multipoint object is equal"""
        if isinstance(value, MultiPoint) == False:
            return False
        elif len(self) != len(value):
            return False
        elif value.as_list == self.as_list:
            return True
        return False
    #----------------------------------------------------------------------
    def __ne__(self, value):
        """determines if the multipoint object is not equal to the other object"""
        return not self.__eq__(value=value)
    #----------------------------------------------------------------------
    def __gt__(self, value):
        """compares the number of points in the object to see if it is greater than"""
        if isinstance(value, MultiPoint):
            return len(self) > len(value)
        return False
    #----------------------------------------------------------------------
    def __ge__(self, value):
        """compares the number of points in the object to see if it is greater than
        or equal to the other object"""
        if isinstance(value, MultiPoint):
            return len(self) >= len(value)
        return False
    #----------------------------------------------------------------------
    def __lt__(self, value):
        """compares the number of points in the object  to see if it is less
        than the other object"""
        if isinstance(value, MultiPoint):
            return len(self) < len(value)
        return False
    #----------------------------------------------------------------------
    def __le__(self, value):
        """compares the number of points in the object  to see if it is less than
        or equal to the other object"""
        if isinstance(value, MultiPoint):
            return len(self) <= len(value)
        return False
    #----------------------------------------------------------------------
    def __getitem__(self, index):
        """slicing operation"""
        if len(self) == 0:
            return []

        if isinstance(index, slice):
            return self._geoms[index]
        else:
            if index <= len(self) -1:
                return self._geoms[index]
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
        return "esriGeometryMultipoint"
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
        return [geom.as_list for geom in self._geoms]
    #----------------------------------------------------------------------
    @property
    def as_dict(self):
        """ returns the object as a python dictionary """
        template = {
            "hasM" : self._hasM,
            "hasZ" : self._hasZ,
            "points" : [],
            "spatialReference" : self._sr.as_dict
        }
        for pt in self.as_list:
            template['points'].append(pt)
        return template