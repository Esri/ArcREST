from __future__ import absolute_import
import json
from collections import OrderedDict
from ..connection import SiteConnection
###########################################################################
class BaseService(OrderedDict):
    _con = None
    _url = None
    _json_dict = None
    _json = None
    def __init__(self, url, connection=None, initialize=True, **kwargs):
        super(BaseService, self).__init__()
        self._url = url
        if isinstance(connection, SiteConnection):
            self._con = connection
        else:
            raise ValueError("connection must be of type SiteConnection")
        if initialize:
            self.init(connection)
    #----------------------------------------------------------------------
    def init(self, connection=None):
        if connection is None:
            connection = self._con
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        params = {"f":"json"}
        result = connection.get(path_or_url=self._url,
                                params=params)
        self._json_dict = result
        for k,v in result.items():
            if k in attributes:
                setattr(self, "_"+ k, v)
                self[k] = v
            else:
                self[k] = v
        self.__dict__.update(result)
    #----------------------------------------------------------------------
    @property
    def connection(self):
        return self._con
    #----------------------------------------------------------------------
    @connection.setter
    def connection(self, value):
        if isinstance(value, SiteConnection):
            self._con = value
            self.refresh()
        else:
            raise ValueError("connection must be of type SiteConnection")
    #----------------------------------------------------------------------
    @property
    def url(self):
        return self._url
    #----------------------------------------------------------------------
    @url.setter
    def url(self, value):
        """"""
        self._url = value
        self.refresh()
    #----------------------------------------------------------------------
    def __str__(self):
        return json.dumps(self)
    #----------------------------------------------------------------------
    def __repr__(self):
        return self.__str__()
    #----------------------------------------------------------------------
    def refresh(self):
        self.init()
###########################################################################
class BaseServiceOld(object):
    _url = None
    _con = None
    _json_dict = None
    #----------------------------------------------------------------------
    def __str__(self):
        return json.dumps(self._json_dict)
    #----------------------------------------------------------------------
    @property
    def as_dict(self):
        return self._json_dict
    #----------------------------------------------------------------------
    def __repr__(self):
        return self.__str__()
    #----------------------------------------------------------------------
    def __iter__(self):
        """iterator"""
        if self._json_dict is None:
            yield None
        else:
            for k,v in self._json_dict.items():
                yield k,v

