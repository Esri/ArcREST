from __future__ import absolute_import
from __future__ import print_function
import json
from .._abstract.abstract import BaseAGSServer

########################################################################
class Info(BaseAGSServer):
    """
       A read-only resource that returns meta information about the server.
    """
    _url = None
    _securityHandler = None
    _timezone = None
    _loggedInUser = None
    _loggedInUserPrivilege = None
    _currentBuild = None
    _currentVersion = None
    _fullVersion = None
    _proxy_port = None
    _proxy_url = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor
            Inputs:
               url - admin url
               token_url - url to generate token
               username - admin username
               password - admin password
        """
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        self._securityHandler = securityHandler
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in Info.")
            del k
            del v
    #----------------------------------------------------------------------
    @property
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    @property
    def fullVersion(self):
        """ returns the full version """
        if self._fullVersion is None:
            self.__init()
        return self._fullVersion
    #----------------------------------------------------------------------
    @property
    def currentversion(self):
        """ returns the current vesrion """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def loggedInUser(self):
        """ get the logged in user """
        if self._loggedInUser is None:
            self.__init()
        return self._loggedInUser
    #----------------------------------------------------------------------
    @property
    def currentbuild(self):
        """ returns the current build """
        if self._currentBuild is None:
            self.__init()
        return self._currentBuild
    #----------------------------------------------------------------------
    @property
    def timezone(self):
        """ returns the server's defined time zone """
        if self._timezone is None:
            self.__init()
        return self._timezone
    #----------------------------------------------------------------------
    @property
    def loggedInUserPrivilege(self):
        """ gets the logged in user's privileges """
        if self._loggedInUserPrivilege is None:
            self.__init()
        return self._loggedInUserPrivilege
    #----------------------------------------------------------------------
    def healthCheck(self):
        """
        The health check reports if the ArcGIS Server site is able to
        receive requests. For example, during site creation, this URL
        reports the site is unhealthy because it can't take requests at
        that time. This endpoint is useful if you're setting up a
        third-party load balancer or other monitoring software that
        supports a health check function.
        A healthy (available) site will return an HTTP 200 response code
        along with a message indicating "success": true (noted below). An
        unhealthy (unavailable) site will return messaging other than HTTP
        200.
        """
        url = self._url + "/healthCheck"
        params = {
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getAvailableTimeZones(self):
        """
           Returns an enumeration of all the time zones of which the server
           is aware. This is used by the GIS service publishing tools
        """
        url = self._url + "/getAvailableTimeZones"
        params = {
            "f" : "json"
        }
        return self._do_get(url, params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
