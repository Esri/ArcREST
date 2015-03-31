import os
import json
import time
import calendar
import datetime
from ..common.geometry import Polygon, Polyline, Point, MultiPoint
from .._abstract.abstract import AbstractGeometry, BaseFilter
import arcpy
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
    #----------------------------------------------------------------------
    def __init__(self, geomObject, spatialFilter="esriSpatialRelIntersects"):
        """Constructor"""
        self.geometry = geomObject
        if spatialFilter in self._allowedFilters:
            self._spatialAction = spatialFilter
            self._spatialReference = self.geometry.spatialReference
        else:
            raise AttributeError("geomObject must be a geometry object and "+ \
                                 "spatialFilter must be of value: " + \
                                 "%s" % ", ".join(self._allowedFilters))
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
        elif isinstance(geometry, arcpy.Polygon):
            self._geomObject = Polygon(geometry, wkid=geometry.spatialReference.factoryCode)
            self._geomType = "esriGeometryPolygon"
        elif isinstance(geometry, arcpy.Point):
            self._geomObject = Point(geometry, wkid=geometry.spatialReference.factoryCode)
            self._geomType = "esriGeometryPoint"
        elif isinstance(geometry, arcpy.Polyline):
            self._geomObject = Polyline(geometry, wkid=geometry.spatialReference.factoryCode)
            self._geomType = "esriGeometryPolyline"
        elif isinstance(geometry, arcpy.Multipoint):
            self._geomObject = MultiPoint(geometry, wkid=geometry.spatialReference.factoryCode)
            self._geomType = "esriGeometryMultipoint"
        else:
            raise AttributeError("geometry must be a common.Geometry or arcpy.Geometry type.")
    #----------------------------------------------------------------------
    @property
    def filter(self):
        """ returns the key/value pair of a geometry filter """
        return {"geometryType":self.geometryType,
                "geometry": json.dumps(self._geomObject.asDictionary),
                "spatialRel": self.spatialRelation,
                "inSR" : self._geomObject.spatialReference['wkid']}
    #----------------------------------------------------------------------

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