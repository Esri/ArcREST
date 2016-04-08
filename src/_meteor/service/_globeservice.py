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