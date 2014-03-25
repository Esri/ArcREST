from base import BaseAGSServer
from mapservice import MapService
########################################################################
class NAService(BaseAGSServer):
    """
       A geometry service contains utility methods that provide access to
       sophisticated and frequently used geometric operations. An ArcGIS
       Server web site can only expose one geometry service with the static
       name "Geometry".
    """
    _serviceDescription = None
    _serviceLimits = None
    _serviceAreaLayers = None
    _currentVersion = None
    _closestFacilityLayers = None
    _routeLayers = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url=None, username=None, password=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self_token_url = token_url
        self._username = username
        self._password = password
        if not username is None and\
           not password is None:
            if not token_url is None:
                self.generate_token()
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
                print k, " - attribute not implmented for NA Service."
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the service description """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the current version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def serviceLimits(self):
        """ information about service analysis """
        if self._serviceLimits is None:
            self.__init()
        return self._serviceLimits
    #----------------------------------------------------------------------
    @property
    def serviceAreaLayers(self):
        """ returns the service layer names """
        if self._serviceAreaLayers is None:
            self.__init()
        return self._serviceAreaLayers
    #----------------------------------------------------------------------
    @property
    def closestFacilityLayers(self):
        """ returns the closest facility layer names """
        if self._closestFacilityLayers is None:
            self.__init()
        return self._closestFacilityLayers
    #----------------------------------------------------------------------
    @property
    def routeLayers(self):
        """ returns the route layer names """
        if self._routeLayers is None:
            self.__init()
        return self._routeLayers
