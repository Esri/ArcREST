from .._abstract.abstract import BaseSecurityHandler, BaseAGSServer
from ..security.security import AGSTokenSecurityHandler
import json, types
########################################################################
class MobileServiceLayer(BaseAGSServer):
    """
    Represents a single mobile service layer
    """
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None

    _drawingInfo = None
    _extent = None
    _canModifyLayer = None
    _advancedQueryCapabilities = None
    _hasLabels = None
    _supportsAdvancedQueries = None
    _id = None
    _currentVersion = None
    _geometryType = None
    _ownershipBasedAccessControlForFeatures = None
    _type = None
    _useStandardizedQueries = None
    _supportedQueryFormats = None
    _maxRecordCount = None
    _description = None
    _defaultVisibility = None
    _typeIdField = None
    _displayField = None
    _name = None
    _supportsStatistics = None
    _hasAttachments = None
    _fields = None
    _maxScale = None
    _copyrightText = None
    _canScaleSymbols = None
    _minScale = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token
        json_dict = self._do_get(self._url, params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implmented for Mobile Service Layer."
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """
        returns key/value pair
        """
        attributes = json.loads(str(self))
        for att in attributes.keys():
            yield (att, getattr(self, att))
    #----------------------------------------------------------------------
    @property
    def drawingInfo(self):
        """gets the services drawing information"""
        if self._drawingInfo is None:
            self.__init()
        return self._drawingInfo
    #----------------------------------------------------------------------
    @property
    def extent(self):
        """returns the service layer extent"""
        if self._extent is None:
            self.__init()
        return self._extent
    #----------------------------------------------------------------------
    @property
    def canModifyLayer(self):
        """returns value for can modify layer"""
        if self._canModifyLayer is None:
            self.__init()
        return self._canModifyLayer
    #----------------------------------------------------------------------
    @property
    def advancedQueryCapabilities(self):
        """gets the advancedQueryCapabilities value"""
        if self._advancedQueryCapabilities is None:
            self.__init()
        return self._advancedQueryCapabilities
    #----------------------------------------------------------------------
    @property
    def hasLabels(self):
        """returns the has labels value"""
        if self._hasLabels is None:
            self.__init()
        return self._hasLabels
    #----------------------------------------------------------------------
    @property
    def supportsAdvancedQueries(self):
        """returns the supportsAdvancedQueries value"""
        if self._supportsAdvancedQueries is None:
            self.__init()
        return self._supportsAdvancedQueries
    #----------------------------------------------------------------------
    @property
    def id(self):
        """returns the layers' id"""
        if self._id is None:
            self.__init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the layers current version"""
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """retusn the layers geometry type"""
        if self._geometryType is None:
            self.__init()
        return self._geometryType
    #----------------------------------------------------------------------
    @property
    def ownershipBasedAccessControlForFeatures(self):
        """returns the ownershipBasedAccessControlForFeatures value"""
        if self._ownershipBasedAccessControlForFeatures is None:
            self.__init()
        return self._ownershipBasedAccessControlForFeatures
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the layer type"""
        if self._type is None:
            self.__init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def useStandardizedQueries(self):
        """gets the useStandardizedQueries value"""
        if self._useStandardizedQueries is None:
            self.__init()
        return self._useStandardizedQueries
    #----------------------------------------------------------------------
    @property
    def hasAttachments(self):
        """returns if the layer has attachments enabled"""
        if self._hasAttachments is None:
            self.__init()
        return self._hasAttachments
    #----------------------------------------------------------------------
    @property
    def supportedQueryFormats(self):
        """returns the supportedQueryFormats value"""
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """returns the max record count"""
        if self._maxRecordCount is None:
            self.__init()
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @property
    def description(self):
        """returns the service layer description"""
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def defaultVisibility(self):
        """returns the defaultVisibility value"""
        if self._defaultVisibility is None:
            self.__init()
        return self._defaultVisibility
    #----------------------------------------------------------------------
    @property
    def typeIdField(self):
        """returns the type id field"""
        if self._typeIdField is None:
            self.__init()
        return self._typeIdField
    #----------------------------------------------------------------------
    @property
    def displayField(self):
        """returns the display field"""
        if self._displayField is None:
            self.__init()
        return self._display
    #----------------------------------------------------------------------
    @property
    def name(self):
        """returns the layers name"""
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def supportsStatistics(self):
        """returns the supports statistics value"""
        if self._supportsStatistics is None:
            self.__init()
        return self._supportsStatistics
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """gets the fields for the layer"""
        if self._fields is None:
            self.__init()
        return self._fields
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """gets the copy right text"""
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def canScaleSymbols(self):
        """returns the can scale symbols value"""
        if self._canScaleSymbols is None:
            self.__init()
        return self._canScaleSymbols
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """returns the minScale value"""
        if self._minScale is None:
            self.__init()
        return self._minScale
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """gets the max scale for the layer"""
        if self._maxScale is None:
            self.__init()
        return self._maxScale
########################################################################
class MobileService(BaseAGSServer):
    """
    Represents a single globe layer
    """
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None

    _layers = None
    _description = None
    _initialExtent = None
    _spatialReference = None
    _mapName = None
    _currentVersion = None
    _units = None
    _fullExtent = None
    _serviceDescription = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token
        json_dict = self._do_get(self._url, params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implmented for Mobile Service."
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """
        returns key/value pair
        """
        attributes = json.loads(str(self))
        for att in attributes.keys():
            yield (att, getattr(self, att))
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """gets the service layers"""
        if self._layers is None:
            self.__init()
        lyrs = []
        for lyr in self._layers:
            url = self._url + "/%s" % lyr['id']
            lyr['object'] = MobileServiceLayer(url=url,
                                               securityHandler=self._securityHandler,
                                               proxy_url=self._proxy_url,
                                               proxy_port=self._proxy_port,
                                               initialize=True)#TODO change to false
        return self._layers
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets the service description"""
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """gets the service initial extent"""
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """gets the spatial reference"""
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def mapName(self):
        """gets the map name"""
        if self._mapName is None:
            self._mapName
        return self._mapName
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the current version"""
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def units(self):
        """gets the units for the service"""
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """returns the service full extent"""
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """returns the service description"""
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription









