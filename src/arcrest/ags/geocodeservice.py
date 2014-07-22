from base import BaseAGSServer

########################################################################
class GeocodeService(BaseAGSServer):
    """
       A geometry service contains utility methods that provide access to
       sophisticated and frequently used geometric operations. An ArcGIS
       Server web site can only expose one geometry service with the static
       name "Geometry".
    """
    _serviceDescription = None
    _candidateFields = None
    _spatialReference = None
    _singleLineAddressField = None
    _addressFields = None
    _currentVersion = None
    _locatorProperties = None
    _locators = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url=None, username=None, password=None,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._url = url
        self_token_url = token_url
        self._username = username
        self._password = password
        if not username is None and \
           not password is None and \
           not username is "" and \
           not password is "":
            if not token_url is None:
                res = self.generate_token(tokenURL=token_url,
                                              proxy_port=proxy_port,
                                            proxy_url=proxy_url)
            else:   
                res = self.generate_token(proxy_port=self._proxy_port,
                                                       proxy_url=self._proxy_url)                
            if res is None:
                print "Token was not generated"
            elif 'error' in res:
                print res
            else:
                self._token = res[0]
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
                print k, " - attribute not implmented for Geocoding Service."
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the service description """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def locators(self):
        """ returns the locators """
        if self._locators is None:
            self.__init()
        return self.locators
    #----------------------------------------------------------------------
    @property
    def locatorProperties(self):
        """ returns the locator's properties """
        if self._locatorProperties is None:
            self.__init()
        return self._locatorProperties
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the version of locator """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def addressFields(self):
        """ returns the address fields """
        if self._addressFields is None:
            self.__init()
        return self._addressFields
    #----------------------------------------------------------------------
    @property
    def singleLineAddressField(self):
        """ information about the single line address field """
        if self._singleLineAddressField is None:
            self.__init()
        return self._singleLineAddressField
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """ returns the spatial reference """
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def candidateFields(self):
        """ returns the candidate's fields """
        if self._candidateFields is None:
            self.__init()
        return self._candidateFields
