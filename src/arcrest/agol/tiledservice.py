"""

.. module:: admin
   :platform: Windows, Linux
   :synopsis: Class to help managing Tiled Services

.. moduleauthor:: Esri


"""
import json
from base import BaseAGOLClass
import urlparse
import urllib
import os
import json

########################################################################
class TiledService(BaseAGOLClass):
    """
       AGOL Tiled Map Service
    """
    _mapName = None
    _documentInfo = None
    _copyrightText = None
    _id = None
    _layers = None
    _tables = None
    _supportedImageFormatTypes = None
    _storageFormat = None
    _capabilities = None
    _access = None
    _currentVersion = None
    _units = None
    _type = None
    _serviceDescription = None
    _status = None
    _tileInfo = None
    _description = None
    _fullExtent = None
    _singleFusedMapCache = None
    _name = None
    _created = None
    _maxScale = None
    _modified = None
    _spatialReference = None
    _minScale = None
    _server = None
    _tileServers = None
    #----------------------------------------------------------------------
    def __init__(self, url,  token_url=None,
                 username=None, password=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._username = username
        self._password = password
        self._token_url = token_url
        if not username is None and \
           not password is None:
            self.generate_token(tokenURL=token_url)
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ loads the data into the class """
        if self._token is None:
            param_dict = {"f": "json"}
        else:
            param_dict = {"f": "json",
                          "token" : self._token
                          }
        json_dict = self._do_get(self._url, param_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print "_%s = None" % k#k, " - attribute not implmented in tiled service."
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """ initial extent of tile service """
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def mapName(self):
        """ returns the map name """
        if self._mapName is None:
            self.__init()
        return self._mapName
    #----------------------------------------------------------------------
    @property
    def documentInfo(self):
        """ returns the document information """
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """ returns the copyright information """
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def id(self):
        """ returns the ID """
        if self._id is None:
            self.__init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """ returns the layers """
        if self._layers is None:
            self.__init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def tables(self):
        """ returns the tables in the map service """
        if self._tables is None:
            self.__init()
        return self._tables
    #----------------------------------------------------------------------
    @property
    def supportedImageFormatTypes(self):
        """ returns the supported image format types """
        if self._supportedImageFormatTypes is None:
            self.__init()
        return self._supportedImageFormatTypes
    #----------------------------------------------------------------------
    @property
    def storageFormat(self):
        """ returns the storage format """
        if self._storageFormat is None:
            self.__init()
        return self._storageFormat
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """ returns the capabilities """
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def access(self):
        """ returns the access value """
        if self._access is None:
            self.__init()
        return self._access
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the current version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def units(self):
        """ returns the units """
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the type """
        if self._type is None:
            self.__init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the service description """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def status(self):
        """ returns the status """
        if self._status is None:
            self.__init()
        return self._status
    #----------------------------------------------------------------------
    @property
    def tileInfo(self):
        """ returns the tile information """
        if self._tileInfo is None:
            self.__init()
        return self._tileInfo
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the description """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """ returns the full extent """
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def singleFusedMapCache(self):
        """ information about the single fused map cache """
        if self._singleFusedMapCache is None:
            self.__init()
        return self._singleFusedMapCache
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ returns the service name """
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def created(self):
        """ returns the created value """
        if self._created is None:
            self.__init()
        return self._created
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """ returns the maximum scale """
        if self._maxScale is None:
            self.__init()
        return self._maxScale
    #----------------------------------------------------------------------
    @property
    def modified(self):
        """ returns the modified value """
        if self._modified is None:
            self.__init()
        return self._modified
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """ returns the spatial reference value """
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ returns the minimum scale """
        if self._minScale is None:
            self.__init()
        return self._minScale
    #----------------------------------------------------------------------
    @property
    def server(self):
        """ returns the server information """
        if self._server is None:
            self.__init()
        return self._server
    #----------------------------------------------------------------------
    @property
    def tileServers(self):
        """ returns the tile services value """
        if self._tileServers is None:
            self.__init()
        return self._tileServers