"""
   Contains all the information regarding the layers that can be created in
   the ArcGIS Webmap JSON
"""
import base
from common import *
from common import _unicode_convert, _date_handler, featureclassToFeatureSet
import json
import uuid
########################################################################
class MapGraphicLayer(base.BaseOperationalLayer):
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
        if self._storedFeatures.has_key(layerName):
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
########################################################################
class KMZLayer(base.BaseOperationalLayer):
    """
       Reprsents a KMZ/KML operational layer
    """
    _url = None
    _type = "kml"
    _token = None
    _title = None
    _showLabels = None
    _visibleFolders = None
    _opacity = None
    _minScale = None
    _maxScale = None
    _securityHandler = None
    _id = None
    #----------------------------------------------------------------------
    def __init__(self, id, url, title, showLabels=False,
                 visibleFolders=None, opacity=1,
                 minScale=0, maxScale=0,
                 securityHandler=None):
        """Constructor"""
        self._id = id
        self._url = url
        self._title = title
        self._showLabels = showLabels
        self._visibleFolders = visibleFolders
        self._opacity = opacity
        self._minScale = minScale
        self._maxScale = maxScale
        self._securityHandler = securityHandler
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ gets the token for the service """
        if self._securityHandler is not None:
            return self._securityHandler.token
        return None
    #----------------------------------------------------------------------
    @property
    def securityHandler(self):
        """ returns the object that controls the security """
        return self._securityHandler
    #----------------------------------------------------------------------
    @securityHandler.setter
    def securityHandler(self, value):
        """"""
        if isinstance(value, base.BaseSecurityHandler):
            self._securityHandler = value
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """ returns the max scale """
        return self._maxScale
    #----------------------------------------------------------------------
    @maxScale.setter
    def maxScale(self, value):
        """ sets the maximum scale """
        self._maxScale = value
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ returns the minimum scale """
        return self._minScale
    #----------------------------------------------------------------------
    @minScale.setter
    def minScale(self, value):
        """ sets the minimum scale """
        self._minScale = value
    #----------------------------------------------------------------------
    @property
    def showLabels(self):
        """ returns if the values are shown or not """
        return self._showLabels
    #----------------------------------------------------------------------
    @showLabels.setter
    def showLabels(self, value):
        """ sets the show label values (boolean) """
        if isinstance(value, bool):
            self._showLabels = value
    #----------------------------------------------------------------------
    @property
    def url(self):
        """ service url """
        return self._url
    #----------------------------------------------------------------------
    @url.setter
    def url(self, value):
        """ sets the URL """
        self._url = value
    #----------------------------------------------------------------------
    @property
    def visibleFolders(self):
        """ returns the visible folders value """
        return self._visibleFolders
    #----------------------------------------------------------------------
    @visibleFolders.setter
    def visibleFolders(self, value):
        """ sets the visible folders value """
        self._visibleFolders = value
    #----------------------------------------------------------------------
    @property
    def opacity(self):
        """ returns the opacity value """
        return self._opacity
    #----------------------------------------------------------------------
    @opacity.setter
    def opacity(self, value):
        """ sets the opacity value """
        self._opacity = value
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the service type """
        return self._type
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the class as a string (JSON) """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a dictionary """
        template = {
            "type" : self._type,
            "id" : self._id,
            "url" : self._url,
            "title" : self._title,
            "opacity" : self._opacity,
            "minScale" : self._minScale,
            "maxScale" : self._maxScale,
            "showLabels" : self._showLabels,
            "visibleFolders" : self._visibleFolders
        }
        if self._securityHandler is not None:
            template['token'] = self._securityHandler.token
        return template
########################################################################
class WMSLayer(base.BaseOperationalLayer):
    """
       Reprsents a WMS operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class CSVLayer(base.BaseOperationalLayer):
    """
       Reprsents a CSV operational layer
    """
    _columnDelimiter = None
    _id = None
    _layerDefinitions = None
    _locationInfo = None
    _minScale = None
    _maxScale = None
    _opacity = None
    _popupInfo = None
    _title = None
    _type = "CSV"
    _url = None
    _visibility = None
    #----------------------------------------------------------------------
    def __init__(self, url, mapId, title,
                 columnDelimiter,
                 locationInfo,
                 layerDefinitions,
                 popupInfo=None,
                 opacity=1, visibility=True,
                 minScale=0, maxScale=0):
        """Constructor"""
        self._url = url
        self._id = mapId
        self._title = title
        self._columnDelimiter = columnDelimiter
        self._opacity = opacity
        self._visibility = visibility
        self._minScale = minScale
        self._maxScale = maxScale
        self._popupInfo = popupInfo
        if isinstance(locationInfo, LocationInfo):
            self._locationInfo = locationInfo
        else:
            raise AttributeError("Invalid LocationInfo Object")
        if isinstance(layerDefinitions, LayerDefinition):
            self._layerDefinitions = layerDefinitions
        else:
            raise AttributeError("Invalid LayerDefinition Object")
    #----------------------------------------------------------------------
    @property
    def popupInfo(self):
        """ gets the popup information """
        return self._popupInfo
    #----------------------------------------------------------------------
    @property
    def layerDefinition(self):
        """ gets the layer definition """
        return self._layerDefinitions
    #----------------------------------------------------------------------
    @property
    def locationInfo(self):
        """gets the location information"""
        return self._locationInfo
    #----------------------------------------------------------------------
    @property
    def opacity(self):
        """gets the opacity value"""
        return self._opacity
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ gets the minimum scale """
        return self._minScale
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """gets the maximum scale"""
        return self._maxScale
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ gets the layer type """
        return self._type
    #----------------------------------------------------------------------
    @property
    def url(self):
        """ gets the url """
        return self._url
    #----------------------------------------------------------------------
    @property
    def id(self):
        """gets the map id"""
        return self._id
    #----------------------------------------------------------------------
    @property
    def title(self):
        """gets the title"""
        return self._title
    #----------------------------------------------------------------------
    @property
    def columnDelimiter(self):
        """ gets the column delimiter value """
        return self._columnDelimiter
    #----------------------------------------------------------------------
    @property
    def visibility(self):
        """ gets the visibility """
        return self._visibility
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        template = {
            "id" : self._id,
            "title" : self._title,
            "visibility" : self._visibility,
            "opacity" : self._opacity,
            "type" : self._type,
            "url" : self._url,
            "layerDefinition" : self._layerDefinitions.asDictionary,
            "locationInfo" : self._locationInfo.asDictionary,
            "maxScale" : self._maxScale,
            "minScale" : self._minScale
        }
        if self._popupInfo is not None:
            template['popupInfo'] = self._popupInfo
        return template
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        return json.dumps(self.asDictionary, default=_date_handler)
########################################################################
class MapNotesLayer(base.BaseOperationalLayer):
    """
       Reprsents a Map Notes operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class FeatureCollectionLayer(base.BaseOperationalLayer):
    """
       Reprsents a Feature Collection operational layer
    """
    _title = ""
    _visibility = True
    _Opacity = 1
    _minScale = 0
    _maxScale = 0
    _showLegend = True
    _layers = []
    _featureCollection = {}
    #----------------------------------------------------------------------
    def __init__(self, title, visibility=True, opacity=1,
                 minScale=0, maxScale=0, ):
        """Constructor"""
        self._title = title
        self._visibility = visibility
        self._Opacity = opacity
        self._minScale = minScale
        self._maxScale = maxScale
        self._id = uuid.uuid4().get_hex()
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ gets the minimum scale value """
        return self._minScale
    #----------------------------------------------------------------------
    @minScale.setter
    def minScale(self, value):
        """ sets the minimum scale """
        if isinstance(value, (int, float, long)):
            self._minScale = value
    #----------------------------------------------------------------------
    @property
    def visibility(self):
        """ gets the visibility value """
        return self._visibility
    #----------------------------------------------------------------------
    @visibility.setter
    def visibility(self, value):
        """sets the visibility value"""
        if isinstance(value, bool):
            self._visibility = value
    #----------------------------------------------------------------------
    @property
    def title(self):
        """gets the title"""
        return self._title
    #----------------------------------------------------------------------
    @title.setter
    def title(self, value):
        """sets the title value"""
        self._title = value
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """ gets the maximum scale """
        return self._maxScale
    #----------------------------------------------------------------------
    @maxScale.setter
    def maxScale(self, value):
        """ sets the maximum scale """
        if isinstance(value, (int, long, float)):
            self._maxScale = value
    #----------------------------------------------------------------------
    @property
    def opacity(self):
        """ gets the opacity value """
        return self._Opacity
    #----------------------------------------------------------------------
    @opacity.setter
    def opacity(self, value):
        """ sets the opacity value """
        if value >= 0 and value <= 1:
            self._Opacity = value
    #----------------------------------------------------------------------
    @property
    def showLegend(self):
        """gets the show legend value"""
        return self._showLegend
    #----------------------------------------------------------------------
    @showLegend.setter
    def showLegend(self, value):
        """sets the show legend value"""
        if isinstance(value, bool):
            self._showLegend = value
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        return json.dumps(_unicode_convert(self.asDictionary), default=_date_handler)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as a dictionary """
        op_layer_template = {
            "id": self._id,
            "title": self._title,
            "featureCollection": {
                "layers": [],
                "showLegend": self._showLegend
                },
            "visibility": self._visibility,
            "opacity": self._Opacity,
            "minScale" : self._minScale,
            "maxScale" : self._maxScale
        }
        for lyr in self._layers:
            op_layer_template['featureCollection']['layers'].append(lyr)
            del lyr
        return op_layer_template
    #----------------------------------------------------------------------
    def loadFeatures(self, featureClass, layerDefinition):
        """ loads the features from a feature class into the object """
        fs = featureclassToFeatureSet(featureClass)
        dict_json = json.loads(fs.JSON)
        return_template = {
            "layerDefinition": {},
            "featureSet" : {
                "features": [],
                "geometryType": dict_json['geometryType']
            }
        }
        if isinstance(layerDefinition, LayerDefinition):
            return_template['layerDefinition'] = layerDefinition.asDictionary
        else:
            return False, "Invalid layerDefinition"
        # Ensure some required values are populated
        return_template['layerDefinition']['geometryType'] = dict_json['geometryType']
        return_template['layerDefinition']["type"] = "Feature Layer"
        return_template['layerDefinition']["fields"] = dict_json['fields']
        return_template["featureSet"]['features'] = dict_json['features']
        self._layers.append(return_template)
        return True, "Success"
    #----------------------------------------------------------------------
    def removeAllFeatures(self):
        """ removes all features from object """
        self._layers = []
    #----------------------------------------------------------------------
    def removeSingleLayer(self, index):
        """ removes a single layer from the layers list """
        if index <= len(self._layers) - 1:
            self._layers.remove(self._layers[index])
            return True
        return False




########################################################################
class AGSFeatureServiceLayer(base.BaseOperationalLayer):
    """
       Represents a AGS Feature Service operational layer
    """
    _url = None
    _capabilities = None
    _mapId = None
    _opacity = None
    _visibility = None
    _mode = None
    _title = None
    _popupInfo = None
    _minScale = None
    _maxScale = None
    _securityHandler = None
    #----------------------------------------------------------------------
    def __init__(self, url, mapId,
                 title, opacity=1,
                 minScale=0, maxScale=0,
                 capabilities="Query",
                 mode=1,
                 securityHandler=None):
        """Constructor"""
        self._url = url
        self._mapId = mapId
        self._title = title
        self._opacity = opacity
        self._minScale = minScale
        self._maxScale = maxScale
        self._capabilities = capabilities
        self._mode = mode
        self._securityHandler = securityHandler
    #----------------------------------------------------------------------
    @property
    def mode(self):
        """ returns the feature service mode """
        return self._mode
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """ returns the capabilities """
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ gets the token for the service """
        if self._securityHandler is not None:
            return self._securityHandler.token
        return None
    #----------------------------------------------------------------------
    @property
    def securityHandler(self):
        """ returns the object that controls the security """
        return self._securityHandler
    #----------------------------------------------------------------------
    @securityHandler.setter
    def securityHandler(self, value):
        """"""
        if isinstance(value, base.BaseSecurityHandler):
            self._securityHandler = value
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """ returns the max scale """
        return self._maxScale
    #----------------------------------------------------------------------
    @maxScale.setter
    def maxScale(self, value):
        """ sets the maximum scale """
        self._maxScale = value
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ returns the minimum scale """
        return self._minScale
    #----------------------------------------------------------------------
    @minScale.setter
    def minScale(self, value):
        """ sets the minimum scale """
        self._minScale = value
    #----------------------------------------------------------------------
    @property
    def url(self):
        """ service url """
        return self._url
    #----------------------------------------------------------------------
    @url.setter
    def url(self, value):
        """ sets the URL """
        self._url = value
    #----------------------------------------------------------------------
    @property
    def opacity(self):
        """ returns the opacity value """
        return self._opacity
    #----------------------------------------------------------------------
    @opacity.setter
    def opacity(self, value):
        """ sets the opacity value """
        self._opacity = value
    #----------------------------------------------------------------------
    def __str__(self):
        """ string representation of the class """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ dictionary representation of the object """
        value_dict = {
            "id":self._id,
            "title":self._title,
            "opacity":self._opacity,
            "minScale":self._minScale,
            "maxScale":self._maxScale,
            "url":self._url,
            "visible" : self._visibility,
            "capabilities" : self._capabilities,
            "mode" : self._mode
        }
        if self._popupInfo is not None:
            value_dict['popupInfo'] = self._popupInfo
        if self._securityHandler is not None:
            value_dict['token'] = self._securityHandler.token
        return value_dict
########################################################################
class AGSMapServiceLayer(base.BaseOperationalLayer):
    """
       Reprsents a AGS Map Service operational layer
    """
    _url = None
    _mapId = None
    _title = None
    _opacity = None
    _minScale = None
    _maxScale = None
    _securityHandler = None
    _layers = None
    #----------------------------------------------------------------------
    def __init__(self, url, mapId,
                 title, opacity=1, layers=[],
                 minScale=0, maxScale=0,
                 securityHandler=None):
        """Constructor"""
        self._url = url
        self._mapId = mapId
        self._title = title
        self._opacity = opacity
        self._minScale = minScale
        self._maxScale = maxScale
        self._securityHandler = securityHandler
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ gets the token for the service """
        if self._securityHandler is not None:
            return self._securityHandler.token
        return None
    #----------------------------------------------------------------------
    @property
    def securityHandler(self):
        """ returns the object that controls the security """
        return self._securityHandler
    #----------------------------------------------------------------------
    @securityHandler.setter
    def securityHandler(self, value):
        """"""
        if isinstance(value, base.BaseSecurityHandler):
            self._securityHandler = value
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """ returns the max scale """
        return self._maxScale
    #----------------------------------------------------------------------
    @maxScale.setter
    def maxScale(self, value):
        """ sets the maximum scale """
        self._maxScale = value
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ returns the minimum scale """
        return self._minScale
    #----------------------------------------------------------------------
    @minScale.setter
    def minScale(self, value):
        """ sets the minimum scale """
        self._minScale = value
    #----------------------------------------------------------------------
    @property
    def url(self):
        """ service url """
        return self._url
    #----------------------------------------------------------------------
    @url.setter
    def url(self, value):
        """ sets the URL """
        self._url = value
    #----------------------------------------------------------------------
    @property
    def opacity(self):
        """ returns the opacity value """
        return self._opacity
    #----------------------------------------------------------------------
    @opacity.setter
    def opacity(self, value):
        """ sets the opacity value """
        self._opacity = value
    #----------------------------------------------------------------------
    def add_layer(self, layer):
        """ adds a Layer object to the layers """
        if self._layers is None:
            self._layers = []
        self._layers.append(layer)
    #----------------------------------------------------------------------
    def remove_layer(self, index):
        """ removes a layer from the layers """
        if index <= len(self._layers) - 1:
            self._layers.remove(self._layers[index])
            return True
        else:
            return False
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """ returns the optional layers property for map services """
        return self._layers
    #----------------------------------------------------------------------
    def __str__(self):
        """ string representation of the class """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ dictionary representation of the object """
        value_dict = {
            "id":self._id,
            "title":self._title,
            "opacity":self._opacity,
            "minScale":self._minScale,
            "maxScale":self._maxScale,
            "url":self._url,
            "visibleLayers":None,
            "layers":self._layers
        }
        if self._securityHandler is not None:
            value_dict['token'] = self._securityHandler.token
        return value_dict


########################################################################
class AGOLLayer(base.BaseOperationalLayer):
    """
       Reprsents a AGOL service operational layer
    """
    _url = None
    _mapId = None
    _visibility = None
    _opacity = None
    _title = None
    _itemId = None
    _securityHandler = None
    #----------------------------------------------------------------------
    def __init__(self, title, itemId, url,
                 opacity=1, id=1, visibility=True,
                 securityHandler=None):
        """Constructor"""
        self._title = title
        self._itemId = itemId
        self._url = url
        self._opacity = opacity
        self._mapId = id
        self._visibility = visibility
        self._securityHandler = None
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        template = {

            "id": self._mapId,
            "visibility": self._visibility,
            "opacity": self._opacity,
            "title": self._title,
            "itemId": self._itemId
        }
        if self._securityHandler is not None:
            template['url'] = self._url + "?token=%s" % self._securityHandler.token
        else:
            template['url'] = self._url
        return template
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the object as a string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def token(self):
        """ gets the token for the service """
        if self._securityHandler is not None:
            return self._securityHandler.token
        return None
    #----------------------------------------------------------------------
    @property
    def securityHandler(self):
        """ returns the object that controls the security """
        return self._securityHandler
    #----------------------------------------------------------------------
    @securityHandler.setter
    def securityHandler(self, value):
        """"""
        if isinstance(value, base.BaseSecurityHandler):
            self._securityHandler = value
########################################################################
class BaseMapLayer(object):
    """
       A basemap layer is a layer that provides geographic context to the
       map. The web map contains an array of baseMapLayer objects. The
       isReference property determines whether the layer is drawn on top of
       all operational layers (true) or below them (false). Basemap layers
       cannot be drawn between operational layers.
       All basemap layers used in a web map need to have the same spatial
       reference and tiling scheme. All operational layers in the map are
       drawn or requested in the spatial reference of the basemap layers.

       Inputs:
       id - A unique identifying string for the layer.
       isReference - Boolean property determining whether the basemap layer
                     appears on top of all operational layers (true) or
                     beneath all operational layers (false). Typically,
                     this value is set to true on reference layers such as
                     road networks, labels, or boundaries. The default
                     value is false.
       opacity - The degree of transparency applied to the layer, where 0
                 is full transparency and 1 is no transparency.
       type - A special string identifier used when the basemap is from
              Bing Maps or OpenStreetMap. When this property is included,
              the url property is not required. Acceptable values include:
              OpenStreetMap | BingMapsAerial | BingMapsRoad |
              BingMapsHybrid
       url - The URL to the layer.
       visibility - Boolean property determining whether the layer is
                    initially visible in the web map.
    """
    _id = None
    _url = None
    _isReference = None
    _opacity = None
    _type = None
    _visibility = None
    #----------------------------------------------------------------------
    def __init__(self, id, url=None, isReference=False,
                 opacity=1, type=None, visibility=True ):
        """Constructor"""
        self._id = id
        self._url = url
        self._isReference = isReference
        self._opacity = opacity
        self._type = type
        self._visibility = visibility
    #----------------------------------------------------------------------
    @property
    def id(self):
        """ returns the id """
        return self._id
    #----------------------------------------------------------------------
    @id.setter
    def id(self, value):
        """ sets the id """
        self._id = value
    #----------------------------------------------------------------------
    @property
    def url(self):
        """ returns the url """
        return self._url
    #----------------------------------------------------------------------
    @url.setter
    def url(self, value):
        """ sets the basemap url """
        self._url = value
    #----------------------------------------------------------------------
    @property
    def isReference(self):
        """ returns the isReference value """
        return self._isReference
    #----------------------------------------------------------------------
    @isReference.setter
    def isReference(self, value):
        """ sets the isReference value (boolean) """
        self._isReference = value
    #----------------------------------------------------------------------
    @property
    def opacity(self):
        """ returns the opacity value """
        return self._opacity
    #----------------------------------------------------------------------
    @opacity.setter
    def opacity(self, value):
        """ sets the opacity """
        if isinstance(value, [int, float, long]):
            self._opacity = value
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the service type """
        return self.type
    #----------------------------------------------------------------------
    @type.setter
    def type(self, value):
        """ sets the type for the basemap layer """
        allowed_types = ("OpenStreetMap", "BingMapsAerial",
                         "BingMapsRoad", "", "BingMapsHybrid")
        if value in allowed_types:
            self._type = value
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the basemap layer as a string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a dictionary """
        template = {}
        if self._id is not None:
            template['id'] = self._id
        if self._url is not None:
            template['url'] = self._url
        if self._isReference is not None:
            template['isReference'] = self._isReference
        if self._opacity is not None:
            if self._opacity > 1:
                self._opacity = 1
            if self._opacity < 0:
                self._opacity = 0
            template['opacity'] = self._opacity
        if self._type is not None:
            template['type'] = self._type
        if self._visibility is not None:
            template['visibility'] = self._visibility
        return template




