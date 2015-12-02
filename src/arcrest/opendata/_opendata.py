from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseOpenData
import json
########################################################################
class OpenData(BaseOpenData):
    """allows simple access to the open datasite."""
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json_dict = None
    _json = None
    _metadata = None
    _results = None
    #----------------------------------------------------------------------
    def __init__(self, url="http://opendata.arcgis.com/datasets",
                 securityHandler=None,
                 proxy_port=None,
                 proxy_url=None,
                 initialize=False
                 ):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """gets the properties for the site"""
        url = self._url + ".json"
        params = {"f": "json"}
        json_dict = self._do_get(url, params,
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
                print("%s - attribute not implemented for OpenData class." % k)
    #----------------------------------------------------------------------
    def search(self, q=None, bbox=None,
               page=1, per_page=255,
               sort_by='relevance',
               sort_order='desc'):
        """searches the opendata site and returns the data results"""
        params = {}
        results = []
        get_all = False
        if q is not None:
            params['q'] = q
        if bbox is not None:
            params['bbox'] = bbox
        if isinstance(page, int):
            params['page'] = page
        elif page.lower() == "all":
            get_all = True
        params['per_page'] = per_page
        params['sort_by'] = sort_by
        params['sort_order'] = sort_order
        if get_all:
            pass
        else:
            results = []



        pass
    #----------------------------------------------------------------------
    def metadata(self):
        """gets the metadata """
        return self._metadata
    #----------------------------------------------------------------------
    def data(self):
        """returns the data objects from the last search"""
        return self._results

#http://opendata.arcgis.com/datasets/4d83e90db45e48a688376c431ceec81f_0/related.json
#http://opendata.arcgis.com/datasets/4d83e90db45e48a688376c431ceec81f_0.json
########################################################################
class OpenDataItem(object):
    """represents a single data object"""
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _json = None
    _json_dict = None
    _related_items = None
    #----------------------------------------------------------------------
    def __init__(self,\
                 url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        if not url.lower().endswith('.json'):
            self._url = url + ".json"
        else:
            self._url = url
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """gets the properties for the site"""
        url = self._url
        params = {"f": "json"}
        json_dict = self._do_get(url, params,
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
                print("%s - attribute not implemented for OpenData class." % k)






