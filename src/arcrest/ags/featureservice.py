"""
   Contains information regarding an ArcGIS Server Feature Server
"""
from __future__ import absolute_import
from __future__ import print_function
from re import search
from .._abstract.abstract import BaseAGSServer, BaseSecurityHandler
from ..security import security
from . import layer
import json
from ..common.geometry import SpatialReference
from ..common.general import FeatureSet
from ..common.filters import LayerDefinitionFilter, GeometryFilter, TimeFilter
########################################################################
class FeatureService(BaseAGSServer):
    """ contains information about a feature service """
    _url = None
    _currentVersion = None
    _serviceDescription = None
    _hasVersionedData = None
    _supportsDisconnectedEditing = None
    _hasStaticData = None
    _maxRecordCount = None
    _supportedQueryFormats = None
    _capabilities = None
    _description = None
    _copyrightText = None
    _spatialReference = None
    _initialExtent = None
    _fullExtent = None
    _allowGeometryUpdates = None
    _units = None
    _syncEnabled = None
    _syncCapabilities = None
    _editorTrackingInfo = None
    _documentInfo = None
    _layers = None
    _tables = None
    _enableZDefaults = None
    _zDefault = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        if securityHandler is not None:
            self._securityHandler = securityHandler

        elif securityHandler is None:
            pass
        else:
            raise AttributeError("Invalid Security Handler")
        if not securityHandler is None and \
           hasattr(securityHandler, 'referer_url'):
            self._referer_url = securityHandler.referer_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ loads the data into the class """
        params = {"f": "json"}
        json_dict = self._get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print("%s - attribute not implemented for Feature Service." % k)
    #----------------------------------------------------------------------
    @property
    def administration(self):
        """returns the service admin object (if accessible)"""
        from ..manageags._services import AGSService
        url = self._url
        res = search("/rest/", url).span()
        addText = "/admin/"
        part1 = url[:res[1]].lower().replace('/rest/', '')
        part2 = url[res[1]:].lower().replace('/featureserver', ".mapserver")
        adminURL = "%s%s%s" % (part1, addText, part2)
        return AGSService(url=adminURL,
                          securityHandler=self._securityHandler,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port,
                          initialize=False)
    #----------------------------------------------------------------------
    @property
    def itemInfo(self):
        """gets the item's info"""
        params = {"f" : "json"}
        url = self._url + "/info/iteminfo"
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def downloadThumbnail(self, outPath):
        """downloads the items's thumbnail"""
        url = self._url + "/info/thumbnail"
        params = {}
        return self._get(url=url,
                         out_folder=outPath,
                         securityHandler=self._securityHandler,
                         file_name=None,
                         param_dict=params,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def downloadMetadataFile(self, outPath):
        """downloads the metadata file to a given path"""
        fileName = "metadata.xml"
        url = self._url + "/info/metadata"
        params = {}
        return self._get(url=url,
                         out_folder=outPath,
                         file_name=fileName,
                         param_dict=params,
                         securityHandler=self._securityHandler,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as a string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns the JSON response in key/value pairs"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.items():
            yield [k,v]
    #----------------------------------------------------------------------
    @property
    def securityHandler(self):
        """ gets the security handler """
        return self._securityHandler
    #----------------------------------------------------------------------
    @securityHandler.setter
    def securityHandler(self, value):
        """ sets the security handler """
        if isinstance(value, BaseSecurityHandler):
            if isinstance(value, security.AGSTokenSecurityHandler):
                self._securityHandler = value
            else:
                pass
        elif value is None:
            self._securityHandler = None
            self._token = None
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """returns the max record count"""
        if self._maxRecordCount is None:
            self.__init()
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @property
    def supportedQueryFormats(self):
        """"""
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """ returns a list of capabilities """
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the service description """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """ returns the copyright text """
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """ returns the spatial reference """
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """ returns the initial extent of the feature service """
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """ returns the full extent of the feature service """
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def allowGeometryUpdates(self):
        """ informs the user if the data allows geometry updates """
        if self._allowGeometryUpdates is None:
            self.__init()
        return self._allowGeometryUpdates
    #----------------------------------------------------------------------
    @property
    def units(self):
        """ returns the measurement unit """
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def syncEnabled(self):
        """ informs the user if sync of data can be performed """
        if self._syncEnabled is None:
            self.__init()
        return self._syncEnabled
    #----------------------------------------------------------------------
    @property
    def syncCapabilities(self):
        """ type of sync that can be performed """
        if self._syncCapabilities is None:
            self.__init()
        return self._syncCapabilities
    #----------------------------------------------------------------------
    @property
    def editorTrackingInfo(self):
        """"""
        if self._editorTrackingInfo is None:
            self.__init()
        return self._editorTrackingInfo
    #----------------------------------------------------------------------
    @property
    def documentInfo(self):
        """"""
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """ gets the layers for the feature service """
        if self._layers is None:
            self.__init()
        self._getLayers()
        return self._layers
    #----------------------------------------------------------------------
    def _getLayers(self):
        """ gets layers for the featuer service """
        params = {"f": "json"}

        json_dict = self._get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._layers = []
        if json_dict.has_key("layers"):
            for l in json_dict["layers"]:
                self._layers.append(
                    layer.FeatureLayer(url=self._url + "/%s" % l['id'],
                                       securityHandler=self._securityHandler,
                                       proxy_port=self._proxy_port,
                                       proxy_url=self._proxy_url)
                )
    #----------------------------------------------------------------------
    @property
    def tables(self):
        """lists the tables on the feature service"""
        if self._tables is None:
            self.__init()
        return self._tables
    #----------------------------------------------------------------------
    @property
    def enableZDefaults(self):
        """"""
        if self._enableZDefaults is None:
            self.__init()
        return self._enableZDefaults
    #----------------------------------------------------------------------
    @property
    def zDefault(self):
        """"""
        if self._zDefault is None:
            self.__init()
        return self._zDefault
    #----------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """"""
        if self._hasStaticData is None:
            self.__init()
        return self._hasStaticData

    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the map service current version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the serviceDescription of the map service """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def hasVersionedData(self):
        """ returns boolean for versioned data """
        if self._hasVersionedData is None:
            self.__init()
        return self._hasVersionedData
    #----------------------------------------------------------------------
    @property
    def supportsDisconnectedEditing(self):
        """ returns boolean is disconnecting editted supported """
        if self._supportsDisconnectedEditing is None:
            self.__init()
        return self._supportsDisconnectedEditing
    #----------------------------------------------------------------------
    def query(self,
              layerDefsFilter=None,
              geometryFilter=None,
              timeFilter=None,
              returnGeometry=True,
              returnIdsOnly=False,
              returnCountOnly=False,
              returnZ=False,
              returnM=False,
              outSR=None
              ):
        """
           The Query operation is performed on a feature service resource
        """
        qurl = self._url + "/query"
        params = {"f": "json",
                  "returnGeometry": returnGeometry,
                  "returnIdsOnly": returnIdsOnly,
                  "returnCountOnly": returnCountOnly,
                  "returnZ": returnZ,
                  "returnM" : returnM}
        if not layerDefsFilter is None and \
           isinstance(layerDefsFilter, LayerDefinitionFilter):
            params['layerDefs'] = layerDefsFilter.filter
        if not geometryFilter is None and \
           isinstance(geometryFilter, GeometryFilter):
            gf = geometryFilter.filter
            params['geometryType'] = gf['geometryType']
            params['spatialRel'] = gf['spatialRel']
            params['geometry'] = gf['geometry']
            params['inSR'] = gf['inSR']
        if not outSR is None and \
           isinstance(outSR, SpatialReference):
            params['outSR'] = outSR.asDictionary
        if not timeFilter is None and \
           isinstance(timeFilter, TimeFilter):
            params['time'] = timeFilter.filter

        res = self._post(url=qurl,
                           param_dict=params,
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
        if returnIdsOnly == False and returnCountOnly == False:
            if isinstance(res, str):
                jd = json.loads(res)
                return [FeatureSet.fromJSON(json.dumps(lyr)) for lyr in jd['layers']]
            elif isinstance(res, dict):
                return [FeatureSet.fromJSON(json.dumps(lyr)) for lyr in res['layers']]
            else:
                return res
        return res
