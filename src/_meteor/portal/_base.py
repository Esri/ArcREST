from __future__ import absolute_import
from ..common._base import BaseDict
import json
###########################################################################
class BasePortal(object):
    _url = None
    _con = None
    _json_dict = None
    _json = None
    def __init__(self, connection, url, initialize=False):
        """constructor"""
        self._con = connection
        self._url = url
        self._json_dict = None
        if initialize:
            self.__init(connection)
    #----------------------------------------------------------------------
    def __init(self, connection):
        """loads the properties"""
        params = {"f" : "json"}
        missing = {}
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        result = connection.get(path_or_url=self._url, params=params)
        self._json_dict = result
        self._json = json.dumps(result)
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
    def refresh(self):
        """reloads all the services properties"""
        self.__init(connection=self._con)
    #----------------------------------------------------------------------
    def __str__(self):
        """object as string"""
        if self._json_dict is None:
            self.__init(connection=self._con)
        return json.dumps(self._json_dict)
    #----------------------------------------------------------------------
    def __repr__(self):
        """representation object"""
        return "{classtype}({data})".format(
            classtype=self.__class__.__name__,
            data=self.__str__())
    #----------------------------------------------------------------------
    def __iter__(self):
        """creates iterable for classes properties"""
        for k,v in self._json_dict.items():
            yield k,v

