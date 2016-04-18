from __future__ import absolute_import
from __future__ import print_function
from ._base import BaseService
import json

########################################################################
class SceneService(BaseService):
    """
    A scene service is an ArcGIS Server web service originating from a 3D
    scene in ArcGIS Pro. Scene services (also known as web scene layers)
    allow you to share 3D content via web scenes to your Portal for ArcGIS
    organization. Web scenes are similar in concept to web maps. However,
    instead of displaying 2D map or feature services, they use 3D scene
    services and give you access to 3D content originally created in ArcGIS
    Pro.
    """
    _url = None
    _con = None
    _json_dict = None
    #----------------------------------------------------------------------
    def __init__(self, connection, url,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._con = connection

        if initialize:
            self.__init(connection)
    #----------------------------------------------------------------------
    def __init(self, connection=None):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        missing = {}
        if connection is None:
            connection = self._con
        self._url = self._url.replace(' ','+')

        json_dict = connection.get(url_or_path=self._url, params=params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                missing[k] = v
                setattr(self, k, v)
            del k,v
        if len(missing.keys()) > 0:
            self.__dict__.update(missing)




