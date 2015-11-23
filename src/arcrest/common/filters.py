from __future__ import absolute_import
from __future__ import print_function
import json
from ..common.geometry import Polygon, Polyline, Point, MultiPoint
from .._abstract.abstract import AbstractGeometry, BaseFilter
try:
    import arcpy
    arcpyFound = True
except:
    arcpyFound = False
########################################################################
class StatisticFilter(BaseFilter):
    """
    The definitions for one or more field-based statistics to be calculated
    """
    _json = None
    _array = []

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    #----------------------------------------------------------------------
    def add(self, statisticType, onStatisticField, outStatisticFieldName=None):
        """
        Adds the statistics group to the filter.

        outStatistics - is supported on only those layers/tables that
          indicate supportsStatistics is true.
        outStatisticFieldName is empty or missing, the map server assigns a
          field name to the returned statistic field. A valid field name
          can only contain alphanumeric characters and an underscore.
        outStatisticFieldName is a reserved keyword of the underlying DBMS,
          the operation can fail. Try specifying an alternative
          outStatisticFieldName. When using outStatistics, the only other
          parameters that can be used are groupByFieldsForStatistics,
          orderByFields, time, and where.
        """
        val = {
            "statisticType" : statisticType,
            "onStatisticField" : onStatisticField,
            "outStatisticFieldName" : outStatisticFieldName
        }
        if outStatisticFieldName is None:
            del val['outStatisticFieldName']
        self._array.append(val)
    #----------------------------------------------------------------------
    def remove(self, index):
        """removes the filter by index"""
        self._array.remove(index)
    #----------------------------------------------------------------------
    def clear(self):
        """removes all the filters"""
        self._array = []
    #----------------------------------------------------------------------
    @property
    def filter(self):
        """ returns the key/value pair of a geometry filter """
        return self._array
########################################################################
class LayerDefinitionFilter(BaseFilter):
    """
       Allows you to filter the features of individual layers in the
       query by specifying definition expressions for those layers. A
       definition expression for a layer that is published with the
       service will always be honored.
    """
    _ids = []
    _filterTemplate = {"layerId" : "", "where" : "", "outFields" : "*"}
    _filter = []
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    #----------------------------------------------------------------------
    def addFilter(self, layer_id, where=None, outFields="*"):
        """ adds a layer definition filter """
        import copy
        f = copy.deepcopy(self._filterTemplate)
        f['layerId'] = layer_id
        f['outFields'] = outFields
        if where is not None:
            f['where'] = where
        if f not in self._filter:
            self._filter.append(f)
    #----------------------------------------------------------------------
    def removeFilter(self, filter_index):
        """ removes a layer filter based on position in filter list """
        f = self._filter[filter_index]
        self._filter.remove(f)
    #----------------------------------------------------------------------
    def removeAll(self):
        """ removes all items from the filter """
        self._filter = []
    #----------------------------------------------------------------------
    @property
    def filter(self):
        """ returns the filter object as a list of layer defs """
        return self._filter
########################################################################
class GeometryFilter(BaseFilter):
    """ creates a geometry filter for queries
        Inputs:
           geomObject - a common.Geometry or arcpy.Geometry object
           spatialFilter - The spatial relationship to be applied on the
                           input geometry while performing the query. The
                           supported spatial relationships include
                           intersects, contains, envelope intersects,
                           within, etc. The default spatial relationship
                           is intersects (esriSpatialRelIntersects).
           bufferDistance - if filter type esriSpatialRelWithin is selected
                            and the service supports that select type, then
                            the geometry will be buffered at a given.
                            Can be of type integer or float.
           units - the value the distance units represents. Valid values
                   are: "esriSRUnit_Meter", "esriSRUnit_StatuteMile",
                        "esriSRUnit_Foot", "esriSRUnit_Kilometer",
                         "esriSRUnit_NauticalMile", and
                         "esriSRUnit_USNauticalMile"
       Raises:
          AttributeError for invalid inputs
    """
    _allowedFilters = ["esriSpatialRelIntersects",
                       "esriSpatialRelContains",
                       "esriSpatialRelCrosses",
                       "esriSpatialRelEnvelopeIntersects",
                       "esriSpatialRelIndexIntersects",
                       "esriSpatialRelOverlaps",
                       "esriSpatialRelTouches",
                       "esriSpatialRelWithin"]
    _geomObject = None
    _spatialAction = None
    _geomType = None
    _spatialReference = None
    _buffer = None
    _units = None
    _allowed_units = ["esriSRUnit_Meter", "esriSRUnit_StatuteMile",
                      "esriSRUnit_Foot", "esriSRUnit_Kilometer",
                      "esriSRUnit_NauticalMile", "esriSRUnit_USNauticalMile"]
    #----------------------------------------------------------------------
    def __init__(self,
                 geomObject,
                 spatialFilter="esriSpatialRelIntersects",
                 bufferDistance=None,
                 units="esriSRUnit_Meter"
                 ):
        """Constructor"""
        self.geometry = geomObject
        if spatialFilter in self._allowedFilters:
            self._spatialAction = spatialFilter
            self._spatialReference = self.geometry.spatialReference
        else:
            raise AttributeError("geomObject must be a geometry object and "+ \
                                 "spatialFilter must be of value: " + \
                                 "%s" % ", ".join(self._allowedFilters))
        if not bufferDistance is None and \
           isinstance(bufferDistance, (int, float)) and \
           not units is None and \
           units.lower() in [f.lower() for f in self._allowed_units]:
            self._buffer = bufferDistance
            self._units = units

    #----------------------------------------------------------------------
    @property
    def spatialRelation(self):
        """ gets the filter type """
        return self._spatialAction
    #----------------------------------------------------------------------
    @spatialRelation.setter
    def spatialRelation(self, value):
        if value.lower() in \
           [x.lower() for x in self._allowedFilters]:
            self._spatialAction = value
        else:
            raise AttributeError("spatialRelation must be values of " + \
                                 "%s" % ", ".join(self._allowedFilters))
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """ returns the geometry type """
        return self._geomObject.type
    #----------------------------------------------------------------------
    @property
    def geometry(self):
        """ gets the geometry object used by the filter """
        return self._geomObject
    #----------------------------------------------------------------------
    @geometry.setter
    def geometry(self, geometry):
        """ sets the geometry value """

        if isinstance(geometry, AbstractGeometry):
            self._geomObject = geometry
            self._geomType = geometry.type
        elif arcpyFound and isinstance(geometry, arcpy.Polygon):
            self._geomObject = Polygon(geometry, wkid=geometry.spatialReference.factoryCode)
            self._geomType = "esriGeometryPolygon"
        elif arcpyFound and isinstance(geometry, arcpy.Point):
            self._geomObject = Point(geometry, wkid=geometry.spatialReference.factoryCode)
            self._geomType = "esriGeometryPoint"
        elif arcpyFound and isinstance(geometry, arcpy.Polyline):
            self._geomObject = Polyline(geometry, wkid=geometry.spatialReference.factoryCode)
            self._geomType = "esriGeometryPolyline"
        elif arcpyFound and isinstance(geometry, arcpy.Multipoint):
            self._geomObject = MultiPoint(geometry, wkid=geometry.spatialReference.factoryCode)
            self._geomType = "esriGeometryMultipoint"
        else:
            raise AttributeError("geometry must be a common.Geometry or arcpy.Geometry type.")
    #----------------------------------------------------------------------
    @property
    def filter(self):
        """ returns the key/value pair of a geometry filter """

        val = {"geometryType":self.geometryType,
                "geometry": json.dumps(self._geomObject.asDictionary),
                "spatialRel": self.spatialRelation,
                "inSR" : self._geomObject.spatialReference['wkid']}
        if self._buffer is not None and \
           self._units is not None:
            val['buffer'] = self._buffer
            val['units'] = self._units
        return val
########################################################################
class TimeFilter(BaseFilter):
    """ Implements the time filter """
    _startTime = None
    _endTime = None
    #----------------------------------------------------------------------
    def __init__(self, start_time, time_zone="UTC", end_time=None):
        """Constructor"""
        self._startTime = start_time
        self._endTime = end_time
        self._tz = time_zone
    #----------------------------------------------------------------------
    @property
    def filter(self):
        if not self._endTime is None:
            val = "%s, %s" % (self._startTime, self._endTime)
            return val
        else:
            return "%s" % self._startTime