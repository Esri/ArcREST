"""
   Contains all the information regarding the layers that can be created in
   the ArcGIS Webmap JSON
"""
import base
import json
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
        return json.dumps(self.__dict__())
    #----------------------------------------------------------------------
    def __dict__(self):
        """ returns the object as a dictionary """
        template = {
            "type" : self._type,
            "id" : self._id,
            "url" : self._url,
            "title" : self._title,
            "opacity" : self._opacity,
            "visibility" : self._visibility,
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

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
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

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class AGSFeatureServiceLayer(base.BaseOperationalLayer):
    """
       Represents a AGS Feature Service operational layer
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
                 title, opacity=1,
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
    def __str__(self):
        """ string representation of the class """
        return json.dumps(self.__dict__())
    #----------------------------------------------------------------------
    def __dict__(self):
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
        return json.dumps(self.__dict__())
    #----------------------------------------------------------------------
    def __dict__(self):
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

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
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
        return json.dumps(self.__dict__())
    #----------------------------------------------------------------------
    def __dict__(self):
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
if __name__ == "__main__":
    pass



