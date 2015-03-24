from .._abstract.abstract import BaseSecurityHandler, BaseAGSServer
from ..security.security import AGSTokenSecurityHandler
import json, types
########################################################################
class GeoDataService(BaseAGSServer):
    """
    Represents a single mobile service layer
    """
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None

    _defaultWorkingVersion = None
    _workspaceType = None
    _replicas = None
    _serviceDescription = None
    _versions = None
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
                print k, " - attribute not implmented for GeoData Service"
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
    def defaultWorkingVersion(self):
        """returns the default working version name"""
        if self._defaultWorkingVersion is None:
            self.__init()
        return self._defaultWorkingVersion
    #----------------------------------------------------------------------
    @property
    def workspaceType(self):
        """returns the workspace type"""
        if self._workspaceType is None:
            self.__init()
        return self._workspaceType
    #----------------------------------------------------------------------
    @property
    def replicas(self):
        """returns a list of replices"""
        if self._replicas is None:
            self.__init()
        return self._replicas
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """returns the service description"""
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def versions(self):
        """returns a list of the versions"""
        if self._versions is None:
            self.__init()
        return self._versions
