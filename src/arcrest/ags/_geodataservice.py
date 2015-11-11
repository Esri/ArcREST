from .._abstract.abstract import BaseSecurityHandler, BaseAGSServer
from ..security.security import AGSTokenSecurityHandler, PortalServerSecurityHandler
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
        json_dict = self._do_get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                if k == "versions" and json_dict[k]:
                    self._versions = []
                    for version in v:
                        self._versions.append(
                            Version(url=self._url + "/versions/%s" % version,
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port,
                                    initialize=False))
                else:
                    setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implemented for GeoData Service"
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
            yield [att, getattr(self, att)]
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

########################################################################
class Version(BaseAGSServer):
    """represents a version in a geodata service"""

    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _url = None

    _name = None
    _description = None
    _created = None
    _modified = None
    _access = None
    _parentVersion = None
    _childVersions = None
    _ancestorVersions = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implemented in Version."

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
            yield [att, getattr(self, att)]

    #----------------------------------------------------------------------
    @property
    def name(self):
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def description(self):
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def created(self):
        if self._created is None:
            self.__init()
        return self._created
    #----------------------------------------------------------------------
    @property
    def modified(self):
        if self._modified is None:
            self.__init()
        return self._modified
    #----------------------------------------------------------------------
    @property
    def access(self):
        if self._access is None:
            self.__init()
        return self._access
    #----------------------------------------------------------------------
    @property
    def parentVersion(self):
        if self._parentVersion is None:
            self.__init()
        return self._parentVersion
    #----------------------------------------------------------------------
    @property
    def childVersions(self):
        if self._childVersions is None:
            self.__init()
        return self._childVersions
    #----------------------------------------------------------------------
    @property
    def ancestorVersions(self):
        if self._ancestorVersions is None:
            self.__init()
        return self._ancestorVersions
