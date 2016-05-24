from __future__ import absolute_import
from ..common._base import BaseService
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
    @property
    def layers(self):
        """gets the layers value"""
        if self._layers is None:
            self.init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets the description value"""
        if self._description is None:
            self.init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """gets the initialExtent value"""
        if self._initialExtent is None:
            self.init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """gets the spatialReference value"""
        if self._spatialReference is None:
            self.init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def mapName(self):
        """gets the mapName value"""
        if self._mapName is None:
            self.init()
        return self._mapName
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the currentVersion value"""
        if self._currentVersion is None:
            self.init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def units(self):
        """gets the units value"""
        if self._units is None:
            self.init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """gets the fullExtent value"""
        if self._fullExtent is None:
            self.init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """gets the serviceDescription value"""
        if self._serviceDescription is None:
            self.init()
        return self._serviceDescription