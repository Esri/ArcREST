from __future__ import absolute_import
from __future__ import division
import json
import math
from ._spatialreference import SpatialReference
from ._point import Point
from ._abstract import AbstractGeometry
try:
    import arcpy
    arcpyFound = True
except ImportError:
    arcpyFound = False

_version_ = "1.0.0"
_all_ = ['Polygon']








def ring_area(coordinates):
    """
    Calculate the approximate _area of the polygon were it projected onto
        the earth.  Note that this _area will be positive if ring is oriented
        clockwise, otherwise it will be negative.

    Reference:
        Robert. G. Chamberlain and William H. Duquette, "Some Algorithms for
        Polygons on a Sphere", JPL Publication 07-03, Jet Propulsion
        Laboratory, Pasadena, CA, June 2007 http://trs-new.jpl.nasa.gov/dspace/handle/2014/40409

    @Returns

    {float} The approximate signed geodesic _area of the polygon in square meters.
    """

    assert isinstance(coordinates, list)

    _area = 0
    coordinates_length = len(coordinates)
    if coordinates_length > 2:
        for i in range(0, coordinates_length):
            if i == (coordinates_length - 2):
                lower_index = coordinates_length - 2
                middle_index = coordinates_length - 1
                upper_index = 0
            elif i == (coordinates_length - 1):
                lower_index = coordinates_length - 1
                middle_index = 0
                upper_index = 1
            else:
                lower_index = i
                middle_index = i + 1
                upper_index = i + 2
            p1 = coordinates[lower_index]
            p2 = coordinates[middle_index]
            p3 = coordinates[upper_index]
            _area += (rad(p3[0]) - rad(p1[0])) * math.sin(rad(p2[1]))
        _area = _area * WGS84_RADIUS * WGS84_RADIUS / 2
    return _area


def polygon_area(coordinates):
    assert isinstance(coordinates, list)
    _area = 0
    if len(coordinates) > 0:
        _area += abs(ring_area(coordinates[0]))
        for i in range(1, len(coordinates)):
            _area -= abs(ring_area(coordinates[i]))
    return _area

def area(geometry):
    if isinstance(geometry, str):
        geometry = json.loads(geometry)
    assert isinstance(geometry, dict)
    _area = 0
    if geometry['type'] == 'Polygon':
        return polygon_area(geometry['coordinates'])
    elif geometry['type'] == 'MultiPolygon':
        for i in range(0, len(geometry['coordinates'])):
            _area += polygon_area(geometry['coordinates'][i])
    elif geometry['type'] == 'GeometryCollection':
        for i in range(0, len(geometry['geometries'])):
            _area += area(geometry['geometries'][i])
    return _area

###########################################################################
class Polygon(AbstractGeometry):
    _rings = None
    _sr = None
    _hasZ = None
    _hasM = None
    _planear = None
    _perim = None
    _WGS84_RADIUS = 6378137
    def __init__(self, rings=None, spatialreference=None,
                 hasM=False, hasZ=False, **kwargs):
        self._hasM = hasM
        self._hasZ = hasZ
        self._rings = []
        if isinstance(spatialreference, SpatialReference):
            self._sr = spatialreference
        if rings:
            self._rings = self._validate_rings(rings)
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryPolygon"
    #----------------------------------------------------------------------
    @staticmethod
    def from_json(value):
        if isinstance(value, str):
            sr = None
            j = json.loads(value.strip())
            return Polygon.from_json(value=j)
        elif isinstance(value, dict):
            if "spatialReference" in value:
                sr = SpatialReference.from_json(value['spatialReference'])
                del value['spatialReference']
            container = []
            if "rings" in value:
                _rings = []
                for geom in value['rings']:
                    _geom = []
                    for part in geom:
                        pt = Point(coord=part, spatialreference=sr)
                        _geom.append(pt)
                        del pt
                        del part
                    if len(_geom) > 0:
                        _rings.append(_geom)
                    del geom
                container.append(_rings)
            return Polygon(rings=container, spatialreference=sr)
        else:
            raise ValueError("Invalid input of type: {}. Check the item's format.".format(type(value)))
    #----------------------------------------------------------------------
    def _validate_rings(self, rings):
        """ensures the rings are in the proper form"""
        return rings
    #----------------------------------------------------------------------
    def _poly_to_rings(self, geom):
        """ converts a geometry object to a common.Geometry object """
        if arcpyFound and isinstance(geom, arcpy.Polygon):
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
    def _rad(value):
        """converts degrees to radians"""
        return value * math.pi / 180
    #----------------------------------------------------------------------
    @property
    def area(self):
        """calculates the area"""
        return self._find_area_perim(array=self._rings)[0]
    #----------------------------------------------------------------------
    @property
    def perimeter(self):
        """calculates the perimeter of a polygon"""
        self._find_area_perim(array=self._rings)
        return self._perim
    #----------------------------------------------------------------------
    def _find_area_perim(self, array):
        """finds the perimeter and area of a polygon"""
        self._planear = 0
        self._perim = 0
        for array in self._rings:
            ox,oy = array[0]
            for x,y in array[1:]:
                self._planear += (x*oy-y*ox)
                self._perim += abs((x-ox)+(y-oy)*1j)
                ox,oy = x,y
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.as_dict)
    #----------------------------------------------------------------------
    def __getitem__(self, index):
        """slicing operation"""
        if len(self) == 0:
            return []

        if isinstance(index, slice):
            return self._rings[index]
        else:
            if index <= len(self) -1:
                return self._rings[index]
            else:
                raise ValueError("Invalid index")
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns iterable over rings"""
        yield None
    #----------------------------------------------------------------------
    def __geo_interface__(self):
        return {}
    #----------------------------------------------------------------------
    def __eq__(self, value):
        return False
    #----------------------------------------------------------------------
    def __ne__(self, value):
        return False
    #----------------------------------------------------------------------
    def __gt__(self, value):
        return False
    #----------------------------------------------------------------------
    def __ge__(self, value):
        return False
    #----------------------------------------------------------------------
    def __lt__(self, value):
        return False
    #----------------------------------------------------------------------
    def __le__(self, value):
        return False
    #----------------------------------------------------------------------
    def __len__(self):
        if self._rings:
            return len(self._rings)
        return 0
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
                "rings" : [],
                "spatialReference" : None
            }
        if self._sr:
            template['spatialReference'] = self._sr.as_dict
        for part in self._rings:
            for pt in part:
                if isinstance(pt, (list, tuple)):
                    template['rings'].append([p.as_list for p in pt])
                else:
                    template['rings'].append(pt.as_list)
        return template
