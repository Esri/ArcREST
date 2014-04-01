from base import BaseAGSServer

########################################################################
class GlobeService(BaseAGSServer):
    """
       The Globe Service resource represents a globe service published with
       ArcGIS for Server. The resource provides information about the
       service such as the service description and the various layers
       contained in the published globe document.
    """
    _layers = None
    _currentVersion = None
    _serviceDescription = None
    _documentInfo = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url=None,
                 username=None, password=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self_token_url = token_url
        self._username = username
        self._password = password
        if not username is None and\
           not password is None:
            if not token_url is None:
                self._token = self.generate_token()
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(self._url, params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k == "layers":
                self._layers = []
                for gl in v:
                    self._layers.append(
                        GlobeLayer(url=self._url + "/%s" % gl['id'],
                                   username=self._username,
                                   password=self._password,
                                   token_url=self._token_url,
                                   initialize=False
                                   )
                    )
            elif k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implmented for Globe Service. "
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """ returns the globe layers """
        if self._layers is None:
            self.__init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the current version of the service """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the service description """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def documentInfo(self):
        """ returns the document information """
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
########################################################################
class GlobeLayer(BaseAGSServer):
    """
       The Globe Layer resource represents a single layer in a globe
       service published by ArcGIS for Server. It provides basic
       information about the layer, such as its ID, name, type, parent and
       sub-layers, fields, extent, data type, sampling mode, and extrusion
       type.
    """
    _extent = None
    _displayField = None
    _baseOption = None
    _name = None
    _baseID = None
    _dataType = None
    _fields = None
    _cullMode = None
    _defaultVisibility = None
    _copyrightText = None
    _extrusionExpression = None
    _currentVersion = None
    _subLayers = None
    _minDistance = None
    _type = None
    _samplingMode = None
    _maxDistance = None
    _id = None
    _layerFolderName = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url=None,
                 username=None, password=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self_token_url = token_url
        self._username = username
        self._password = password
        if not username is None and\
           not password is None:
            if not token_url is None:
                self._token = self.generate_token()
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(self._url, params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print "%s = None" % k#k, " - attribute not implmented for Globe Layer. "
    #----------------------------------------------------------------------
    @property
    def extent(self):
        """ returns the extent of the data """
        if self._extent is None:
            self.__init()
        return self._extent
    #----------------------------------------------------------------------
    @property
    def displayField(self):
        """ returns the display field for labels """
        if self._displayField is None:
            self.__init()
        return self._displayField
    #----------------------------------------------------------------------
    @property
    def baseOption(self):
        """ returns the base option """
        if self._baseOption is None:
            self.__init()
        return self._baseOption
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ returns the service name """
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def baseID(self):
        """ returns the baseID """
        if self._baseID is None:
            self.__init()
        return self._baseID
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """ returns the data type """
        if self._dataType is None:
            self.__init()
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """ returns the data's fields """
        if self._fields is None:
            self.__init()
        return self._fields
    #----------------------------------------------------------------------
    @property
    def cullMode(self):
        """ returns cullMode """
        if self._cullMode is None:
            self.__init()
        return self._cullMode
    #----------------------------------------------------------------------
    @property
    def id(self):
        """ returns the id """
        if self._id is None:
            self.__init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def layerFolderName(self):
        """ returns the layer's folder name """
        if self._layerFolderName is None:
            self.__init()
        return self._layerFolderName
    #----------------------------------------------------------------------
    @property
    def maxDistance(self):
        """ returns the max distance """
        if self._maxDistance is None:
            self.__init()
        return self._maxDistance
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the type """
        if self._type is None:
            self.__init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def minDistance(self):
        """ returns the minimum distance """
        if self._minDistance is None:
            self.__init()
        return self._minDistance
    #----------------------------------------------------------------------
    @property
    def samplingMode(self):
        """ returns the sampling mode """
        if self._samplingMode is None:
            self.__init()
        return self._samplingMode
    #----------------------------------------------------------------------
    @property
    def subLayers(self):
        """ returns all the sublayers """
        if self._subLayers is None:
            self.__init()
        return self._subLayers
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the service's version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def extrusionExpression(self):
        """ returns the extrusion expression """
        if self._extrusionExpression is None:
            self.__init()
        return self._extrusionExpression
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """ returns the copyright text """
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def defaultVisibility(self):
        """ returns the default Visibility """
        if self._defaultVisibility is None:
            self.__init()
        return self._defaultVisibility