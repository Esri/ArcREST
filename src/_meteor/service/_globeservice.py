from __future__ import absolute_import
from __future__ import print_function
from ._base import BaseService
from ..connection import SiteConnection
import json
########################################################################
class GlobeServiceLayer(BaseService):
    """
    Represents a single globe layer
    """
    _url = None
    _json_dict = None
    _con = None
    _extent = None
    _displayField = None
    _baseOption = None
    _name = None
    _baseID = None
    _dataType = None
    _fields = None
    _cullMode = None
    _defaultVisibility = None
    _copyrightText = None
    _extrusionExpression = None
    _currentVersion = None
    _subLayers = None
    _minDistance = None
    _type = None
    _samplingMode = None
    _maxDistance = None
    _id = None
    _layerFolderName = None
    #----------------------------------------------------------------------
    def __init__(self, connection, url, initialize=False):
        """constructor"""
        self._con = connection
        self._url = url
        self._json_dict = None
        if initialize:
            self.__init(connection)
    #----------------------------------------------------------------------
    def __init(self, connection=None):
        """loads the properties"""
        params = {"f" : "json"}
        missing = {}
        if connection is None:
            connection = self._con
        result = connection.get(path_or_url=self._url, params=params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        if isinstance(result, dict):
            self._json_dict = result
            for k,v in result.items():
                if k in attributes:
                    setattr(self, "_" + k, v)
                else:
                    setattr(self, k, v)
                    missing[k] = v
                del k,v
        else:
            raise RuntimeError("Could not connect to the service: %s" % result)
        self.__dict__.update(missing)
    #----------------------------------------------------------------------
    @property
    def extent(self):
        """returns the globe layer extent"""
        if self._extent is None:
            self.__init()
        return self._extent
    #----------------------------------------------------------------------
    @property
    def displayField(self):
        """returns the layer's display field"""
        if self._displayField is None:
            self.__init()
        return self._displayField
    #----------------------------------------------------------------------
    @property
    def baseOption(self):
        """returns the base option"""
        if self._baseOption is None:
            self.__init()
        return self._baseOption
    #----------------------------------------------------------------------
    @property
    def name(self):
        """returns the layers' name"""
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def baseID(self):
        """returns the layers' base ID"""
        if self._baseID is None:
            self.__init()
        return self._baseID
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type for the layer"""
        if self._dataType is None:
            self.__init()
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """returns the fields"""
        if self._fields is None:
            self.__init()
        return self._fields
    #----------------------------------------------------------------------
    @property
    def cullMode(self):
        """returns cull mode"""
        if self._cullMode is None:
            self.__init()
        return self._cullMode
    #----------------------------------------------------------------------
    @property
    def defaultVisibility(self):
        """returns the defaultVisibility value"""
        if self._defaultVisibility is None:
            self.__init()
        return self._defaultVisibility
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """returns the copyright text"""
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def extrusionExpression(self):
        """returns the extrusionExpression value"""
        if self._extrusionExpression is None:
            self.__init()
        return self._extrusionExpression
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """returns the currentVersion value"""
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def subLayers(self):
        """returns the subLayers value"""
        if self._subLayers is None:
            self.__init()
        return self._subLayers
    #----------------------------------------------------------------------
    @property
    def minDistance(self):
        """returns the min distance value"""
        if self._minDistance is None:
            self.__init()
        return self._minDistance
    #----------------------------------------------------------------------
    @property
    def type(self):
        """returns the type"""
        if self._type is None:
            self.__init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def samplingMode(self):
        """returns the sampling mode"""
        if self._samplingMode is None:
            self.__init()
        return self._samplingMode
    #----------------------------------------------------------------------
    @property
    def maxDistance(self):
        """returns the maximum distance"""
        if self._maxDistance is None:
            self.__init()
        return self._maxDistance
    #----------------------------------------------------------------------
    @property
    def id(self):
        """returns the id value"""
        if self._id is None:
            self.__init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def layerFolderName(self):
        """returns the layer folder name"""
        if self._layerFolderName is None:
            self.__init()
        return self._layerFolderName
########################################################################
class GlobeService(BaseService):
    """
    The Globe Service resource represents a globe service published with
    ArcGIS for Server. The resource provides information about the service
    such as the service description and the various layers contained in the
    published globe document.
    """
    _url = None
    _json_dict = None
    _con = None
    _layers = None
    def __init__(self, connection, url, initialize=False):
        """initializer"""
        self._con = connection
        self._url = url
        if initialize:
            self.__init()
    def __init(self, connection=None):
        """loads the properties"""
        params = {"f" : "json"}
        missing = {}
        if connection is None:
            connection = self._con
        result = connection.get(path_or_url=self._url, params=params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        if isinstance(result, dict):
            self._json_dict = result
            for k,v in result.items():
                if k in ['layers']:
                    pass#setattr(self, "_"+k, v)
                elif k in attributes:
                    setattr(self, "_" + k, v)
                else:
                    missing[k] = v
                    setattr(self, k, v)
                del k,v
        else:
            raise RuntimeError("Could not connect to the service: %s" % result)
        if len(missing.keys()) > 0:
            self.__dict__.update(missing)
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """gets the globe service layers"""
        if self.layers is None:
            self.__init()
        lyrs = []
        for lyr in self.layers:
            lyr['object'] = GlobeServiceLayer(url=self._url + "/%s" % lyr['id'],
                                              connection=self._con)
            lyrs.append(lyr)
        self._layers = lyrs
        return lyrs
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """returns the service current version"""
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """returns the service current version"""
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def documentInfo(self):
        """returns the service document information"""
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
