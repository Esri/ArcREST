from base import BaseAGSServer
########################################################################
class GeoDataService(BaseAGSServer):
    """
       The GeoData Service resource represents a geodata service that
       you've published with ArcGIS for Server. This resource provides
       basic information associated with the geodata service, such as the
       service description, workspace type, default working version,
       versions, and replicas.
    """
    _defaultWorkingVersion = None
    _workspaceType = None
    _replicas = None
    _serviceDescription = None
    _versions = None
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
                print k, " - attribute not implmented for GeoData Service."
    #----------------------------------------------------------------------
    @property
    def defaultWorkingVersion(self):
        """ returns the default working version """
        if self._defaultWorkingVersion is None:
            self.__init()
        return self._defaultWorkingVersion
    #----------------------------------------------------------------------
    @property
    def workspaceType(self):
        """ returns the workspace type """
        if self._workspaceType is None:
            self.__init()
        return self._workspaceType
    #----------------------------------------------------------------------
    @property
    def replicas(self):
        """ returns a list of replicas """
        if self._replicas is None:
            self.__init()
        return self._replicas
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the service description """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def versions(self):
        """ returns the versions """
        if self._versions is None:
            self.__init()
        return self._versions