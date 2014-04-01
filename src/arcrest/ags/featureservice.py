from base import BaseAGSServer
########################################################################
class FeatureService(BaseAGSServer):
    """ contains information about a feature service """
    _url = None
    _currentVersion = None

    _serviceDescription = None
    _hasVersionedData = None
    _supportsDisconnectedEditing = None
    _hasStaticData = None
    _maxRecordCount = None
    _supportedQueryFormats = None
    _capabilities = None
    _description = None
    _copyrightText = None
    _spatialReference = None
    _initialExtent = None
    _fullExtent = None
    _allowGeometryUpdates = None
    _units = None
    _syncEnabled = None
    _syncCapabilities = None
    _editorTrackingInfo = None
    _documentInfo = None
    _layers = None
    _tables = None
    _enableZDefaults = None
    _zDefault = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url=None, username=None, password=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._token_url = token_url
        if not username is None and \
           not password is None and \
           not token_url is None:
            self._username = username
            self._password = password
            self._token_url = token_url
            self._token = self.generate_token()
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ loads the data into the class """
        if self._token is None:
            param_dict = {"f": "json"}
        else:
            param_dict = {"f": "json",
                          "token" : self._token
                          }
        json_dict = self._do_get(self._url, param_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implmented for Feature Service."
        #if json_dict.has_key("currentVersion"):
            #self._currentVersion = json_dict['currentVersion']
        #else:
            #self._currentVersion = "Not Supported"
        #if json_dict.has_key("serviceDescription"):
            #self._serviceDescription = json_dict['serviceDescription']
        #else:
            #self._serviceDescription = "Not Supported"
        #if json_dict.has_key("hasVersionedData"):
            #self._hasVersionedData = json_dict['hasVersionedData']
        #else:
            #self._hasVersionedData = "Not Supported"
        #if json_dict.has_key('supportsDisconnectedEditing'):
            #self._supportsDisconnectedEditing = json_dict['supportsDisconnectedEditing']
        #else:
            #self._supportsDisconnectedEditing = "Not Supported"
        #if json_dict.has_key("hasStaticData"):
            #self._hasStaticData = json_dict['hasStaticData']
        #else:
            #self._hasStaticData = "Not Supported"
        #if json_dict.has_key("maxRecordCount"):
            #self._maxRecordCount = json_dict['maxRecordCount']
        #else:
            #self._maxRecordCount = "Not Supported"
        #if json_dict.has_key("supportedQueryFormats"):
            #self._supportedQueryFormats = json_dict['supportedQueryFormats']
        #else:
            #self._supportedQueryFormats = "Not Supported"
        #if json_dict.has_key("capabilities"):
            #self._capabilities = json_dict['capabilities']
        #else:
            #self._capabilities = "Not Supported"
        #if json_dict.has_key("description"):
            #self._description = json_dict['description']
        #else:
            #self._description = "Not Supported"
        #if json_dict.has_key("copyrightText"):
            #self._copyrightText = json_dict['copyrightText']
        #else:
            #self._copyrightText = "Not Supported"
        #if json_dict.has_key("spatialReference"):
            #self._spatialReference = json_dict['spatialReference']
        #else:
            #self._spatialReference = "Not Supported"
        #if json_dict.has_key("initialExtent"):
            #self._initialExtent = json_dict['initialExtent']
        #else:
            #self._initialExtent = "Not Supported"
        #if json_dict.has_key("fullExtent"):
            #self._fullExtent = json_dict['fullExtent']
        #else:
            #self._fullExtent = "Not Supported"
        #if json_dict.has_key("allowGeometryUpdates"):
            #self._allowGeometryUpdates = json_dict['allowGeometryUpdates']
        #else:
            #self._allowGeometryUpdates = "Not Supported"
        #if json_dict.has_key("units"):
            #self._units = json_dict['units']
        #else:
            #self._units = "Not Supported"
        #if json_dict.has_key("syncEnabled"):
            #self._syncEnabled = json_dict['syncEnabled']
        #else:
            #self._syncEnabled = False
        #if json_dict.has_key("syncCapabilities"):
            #self._syncCapabilities = json_dict['syncCapabilities']
        #else:
            #self._syncCapabilities = "Not Supported"
        #if json_dict.has_key("editorTrackingInfo"):
            #self._editorTrackingInfo = json_dict['editorTrackingInfo']
        #else:
            #self._editorTrackingInfo = ""
        #if json_dict.has_key("documentInfo"):
            #self._documentInfo = json_dict['documentInfo']
        #else:
            #self._documentInfo = ""
        #if json_dict.has_key("layers"):
            #self._layers = json_dict['layers']
        #else:
            #self._layers = ""
        #if json_dict.has_key("tables"):
            #self._tables = json_dict['tables']
        #else:
            #self._tables = ""
        #if json_dict.has_key("enableZDefaults"):
            #self._enableZDefaults = json_dict['enableZDefaults']
        #else:
            #self._enableZDefaults = False
        #if json_dict.has_key("zDefault"):
            #self._zDefault = json_dict['zDefault']
        #else:
            #self._zDefault = ""
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """returns the max record count"""
        if self._maxRecordCount is None:
            self.__init()
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @property
    def supportedQueryFormats(self):
        """"""
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """ returns a list of capabilities """
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the service description """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """ returns the copyright text """
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """ returns the spatial reference """
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """ returns the initial extent of the feature service """
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """ returns the full extent of the feature service """
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def allowGeometryUpdates(self):
        """ informs the user if the data allows geometry updates """
        if self._allowGeometryUpdates is None:
            self.__init()
        return self._allowGeometryUpdates
    #----------------------------------------------------------------------
    @property
    def units(self):
        """ returns the measurement unit """
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def syncEnabled(self):
        """ informs the user if sync of data can be performed """
        if self._syncEnabled is None:
            self.__init()
        return self._syncEnabled
    #----------------------------------------------------------------------
    @property
    def syncCapabilities(self):
        """ type of sync that can be performed """
        if self._syncCapabilities is None:
            self.__init()
        return self._syncCapabilities
    #----------------------------------------------------------------------
    @property
    def editorTrackingInfo(self):
        """"""
        if self._editorTrackingInfo is None:
            self.__init()
        return self._editorTrackingInfo
    #----------------------------------------------------------------------
    @property
    def documentInfo(self):
        """"""
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """"""
        if self._layers is None:
            self.__init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def tables(self):
        """"""
        if self._tables is None:
            self.__init()
        return self._tables
    #----------------------------------------------------------------------
    @property
    def enableZDefaults(self):
        """"""
        if self._enableZDefaults is None:
            self.__init()
        return self._enableZDefaults
    #----------------------------------------------------------------------
    @property
    def zDefault(self):
        """"""
        if self._zDefault is None:
            self.__init()
        return self._zDefault
    #----------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """"""
        if self._hasStaticData is None:
            self.__init()
        return self._hasStaticData

    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the map service current version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the serviceDescription of the map service """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def hasVersionedData(self):
        """ returns boolean for versioned data """
        if self._hasVersionedData is None:
            self.__init()
        return self._hasVersionedData
    #----------------------------------------------------------------------
    @property
    def supportsDisconnectedEditing(self):
        """ returns boolean is disconnecting editted supported """
        if self._supportsDisconnectedEditing is None:
            self.__init()
        return self._supportsDisconnectedEditing