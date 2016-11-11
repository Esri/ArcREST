from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseAGSServer
import json

########################################################################
class StreamService(BaseAGSServer):
    """
    A stream service is a type of ArcGIS GeoEvent Server service that emphasizes
    low latency, real-time data dissemination for client and server data flows.

    ArcGIS GeoEvent Server must be licensed and installed in your enterprise GIS
    in order to leverage stream services. In the initial release (10.3), stream
    service content can be incorporated into ArcGIS Online web maps as well as
    exposed through clients developed using the ArcGIS API for JavaScript. Future
    releases will support a wider variety of client subscriptions.

    Hosting a stream service on ArcGIS GeoEvent Server enables administrators to
    broadcast event data over the stream service and enables clients to subscribe
    to a stream service and immediately begin receiving data. The REST API stream
    service resource provides basic information about the service including event
    attribute fields, geometry type, and WebSocket resources used by the service.
    """
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None
    _drawingInfo = None
    _displayField = None
    _description = None
    _fields = None
    _capabilities = None
    _spatialReference = None
    _currentVersion = None
    _timeInfo = None
    _geometryType = None
    _objectIdField = None
    _streamUrls = None
    _geometryField = None
    _relatedFeatures = None

    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if self._securityHandler is not None:
            self._referer_url = self._securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()

    #----------------------------------------------------------------------
    def __init(self):
        """initializes the properties"""
        params = {
            "f" : "json",
        }
        json_dict = self._get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print (k, " - attribute not implemented for Stream Service")
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
    def drawingInfo(self):
        if self._drawingInfo is None:
            self.__init()
        return self._drawingInfo
    #----------------------------------------------------------------------
    @property
    def displayField(self):
        if self._displayField is None:
            self.__init()
        return self._displayField
    #----------------------------------------------------------------------
    @property
    def description(self):
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def fields(self):
        if self._fields is None:
            self.__init()
        return self._fields
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def timeInfo(self):
        if self._timeInfo  is None:
            self.__init()
        return self._timeInfo
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        if self._geometryType  is None:
            self.__init()
        return self._geometryType
    #----------------------------------------------------------------------
    @property
    def objectIdField(self):
        if self._objectIdField  is None:
            self.__init()
        return self._objectIdField
    #----------------------------------------------------------------------
    @property
    def streamUrls(self):
        if self._streamUrls  is None:
            self.__init()
        return self._streamUrls
    #----------------------------------------------------------------------
    @property
    def geometryField(self):
        if self._geometryField  is None:
            self.__init()
        return self._geometryField
    #----------------------------------------------------------------------
    @property
    def relatedFeatures(self):
        if self._relatedFeatures  is None:
            self.__init()
        return self._relatedFeatures
