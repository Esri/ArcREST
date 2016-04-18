from __future__ import absolute_import
from ._base import BaseService
from ..connection import SiteConnection
import json

########################################################################
class MobileService(BaseService):
    """
    Represents a mobile service
    """
    _url = None
    _json_dict = None
    _con = None
    _layers = None
    _description = None
    _initialExtent = None
    _spatialReference = None
    _mapName = None
    _currentVersion = None
    _units = None
    _fullExtent = None
    _serviceDescription = None
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
        """gets the layers value"""
        if self._layers is None:
            self.__init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets the description value"""
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """gets the initialExtent value"""
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """gets the spatialReference value"""
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def mapName(self):
        """gets the mapName value"""
        if self._mapName is None:
            self.__init()
        return self._mapName
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the currentVersion value"""
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def units(self):
        """gets the units value"""
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """gets the fullExtent value"""
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """gets the serviceDescription value"""
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription