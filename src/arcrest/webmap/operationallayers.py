from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseOperationalLayer
from ..common.general import _date_handler, _unicode_convert
import json


########################################################################
class MapGraphicLayer(BaseOperationalLayer):
    """
       Represents a graphic in the map.  There are no attributes for this
       data, only geometries.
    """
    _id = None
    _minScale = None
    _maxScale = None
    _storedFeatures = {}
    _layers = []
    _featureCollection = {}
    #----------------------------------------------------------------------
    def __init__(self, id, minScale=0, maxScale=0):
        """Constructor"""
        self._id = id
        self._minScale = minScale
        self._maxScale = maxScale
        self._featureCollection = {"featureCollection":{"layers":[]}}
        self._layers = []
        self._storedFeatures = {}
    #----------------------------------------------------------------------
    def __str__(self):
        return json.dumps(self.asDictionary, default=_date_handler)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        self._layers = []
        for key in self._featureCollection:
            self._layers.append(self._featureCollection[key])
            del key
        template = {"id":self._id,
                    "minScale":self._minScale,
                    "maxScale":self._maxScale,
                    "featureCollection":{"layers":[self._storedFeatures[x] \
                                                   for x in self._storedFeatures] }
                    }
        return template
    #----------------------------------------------------------------------
    def addGraphic(self, layerName, geometry, symbol):
        """ loads a geometry (ArcPy Geometry Object) into Graphic Layer"""
        allowed_geomtypes = ['polygon', 'polyline', 'point', 'multipoint']
        if not (geometry.type.lower() in allowed_geomtypes):
            return False, layerName
        geom = _unicode_convert(json.loads(geometry.JSON))
        geomType = self.__look_up_geom(geometry.type.lower())
        if layerName in self._storedFeatures:
            self._storedFeatures[layerName]['featureSet']['features'].append({"geometry":geom,
                                                                               "symbol":symbol.asDictionary})
        else:
            template_ld = {
                "layerDefinition":{
                    "name":layerName,
                    "geometryType":geomType
                    },
                "featureSet":{
                    "geometryType":geomType,
                    "features":[{"geometry":geom,
                                 "symbol":symbol.asDictionary}]
                }
            }
            self._storedFeatures[layerName] = template_ld
        return True, layerName
    #----------------------------------------------------------------------
    def __look_up_geom(self, geomType):
        """ compares the geometry object's type verse the JSOn
            specs for geometry types
            Inputs:
              geomType - string - geometry object's type
            Returns:
               string JSON geometry type or None if not an allowed type
        """

        if geomType.lower() == "point":
            return "esriGeometryPoint"
        elif geomType.lower() == "polyline":
            return "esriGeometryPolyline"
        elif geomType.lower() == "polygon":
            return "esriGeometryPolygon"
        elif geomType.lower() == "multipoint":
            return "esriGeometryMultipoint"
        else:
            return None