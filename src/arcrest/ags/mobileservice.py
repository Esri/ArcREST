from base import BaseAGSServer
########################################################################
class MobileService(BaseAGSServer):
    """
       The mobile service resource represents a mobile service published
       with ArcGIS Server. The resource provides information about the
       service such as the service description, spatial reference, initial
       and full extents, and the various layers contained in the published
       map document.
    """
    _serviceDescription = None
    _layers = None
    _description = None
    _initialExtent = None
    _spatialReference = None
    _mapName = None
    _currentVersion = None
    _units = None
    _fullExtent = None
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
                print k, " - attribute not implmented for Mobile Service. "
    @property
    def serviceDescription(self):
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    @property
    def layers(self):
        if self._layers is None:
            self.__init()
        return self._layers
    @property
    def description(self):
        if self._description is None:
            self.__init()
        return self._description
    @property
    def initialExtent(self):
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    @property
    def spatialReference(self):
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    @property
    def mapName(self):
        if self._mapName is None:
            self.__init()
        return self._mapName
    @property
    def currentVersion(self):
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    @property
    def units(self):
        if self._units is None:
            self.__init()
        return self._units
    @property
    def fullExtent(self):
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent