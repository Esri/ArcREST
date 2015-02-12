from .._abstract.abstract import BaseSecurityHandler, BaseAGSServer
from ..security.security import AGSTokenSecurityHandler
import json, types
########################################################################
class GeocodeService(BaseAGSServer):
    """
    Represents a single mobile service layer
    """
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None

    _candidateFields = None
    _intersectionCandidateFields = None
    _capabilities = None
    _spatialReference = None
    _singleLineAddressField = None
    _addressFields = None
    _currentVersion = None
    _locatorProperties = None
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
                print k, " - attribute not implmented for Geocode Service"
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
    def candidateFields(self):
        """get candidate fields"""
        if self._candidateFields is None:
            self.__init()
        return self._candidateFields
    #----------------------------------------------------------------------
    @property
    def intersectionCandidateFields(self):
        """gets the intersectionCandidateFields value"""
        if self._intersectionCandidateFields is None:
            self.__init()
        return self._intersectionCandidateFields
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """gets the capabilities value"""
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """gets the spatialReference for the service"""
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def singleLineAddressField(self):
        """returns single line support field"""
        if self._singleLineAddressField is None:
            self.__init()
        return self._singleLineAddressField
    #----------------------------------------------------------------------
    @property
    def addressFields(self):
        """gets the address fields"""
        if self._addressFields is None:
            self.__init()
        return self._addressFields
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the current version"""
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def locatorProperties(self):
        """gets the locator properties"""
        if self._locatorProperties is None:
            self.__init()
        return self._locatorProperties
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """gets the service description"""
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription









