"""
   OpenData Operations
"""
from __future__ import absolute_import
from __future__ import print_function
import json
from ._base import BaseOpenData
from ..web._base import BaseWebOperations
########################################################################
class OpenData(BaseOpenData, BaseWebOperations):
    """Represents an open data site
    Inputs:
       url - web address of the open data site
    """
    _url = None
    _proxy_port = None
    _proxy_url = None
    _securityHandler = None
    _api = "v1"
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
    #----------------------------------------------------------------------
    @property
    def root(self):
        """get/set the base url"""
        return self._url
    #----------------------------------------------------------------------
    @root.setter
    def root(self, value):
        """get/set the base url"""
        self._url = value
    #----------------------------------------------------------------------
    def search(self,
               q=None,
               per_page=None,
               page=None,
               bbox=None,
               sort_by="relavance",
               sort_order="asc"):
        """
        searches the opendata site and returns the dataset results
        """
        url = self._url + "/datasets.json"
        param_dict = {
            "sort_by" : sort_by,
            "f" : "json"
        }
        if q is not None:
            param_dict['q'] = q
        if per_page is not None:
            param_dict['per_page'] = per_page
        if page is not None:
            param_dict['page'] = page
        if bbox is not None:
            param_dict['bbox'] = bbox
        if sort_by is not None:
            param_dict['sort_by'] = sort_by
        if sort_order is not None:
            param_dict['sort_order'] = sort_order
        ds_data =  self._get(url=url,
                    param_dict=param_dict,
                    securityHandler=self._securityHandler,
                    additional_headers=[],
                    proxy_url=self._proxy_url,
                    proxy_port=self._proxy_port)
        return ds_data
    #----------------------------------------------------------------------
    def getDataset(self, itemId):
        """gets a dataset class"""
        if self._url.lower().find('datasets') > -1:
            url = self._url
        else:
            url = self._url + "/datasets"
        return OpenDataItem(url=url,
                            itemId=itemId,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
########################################################################
class OpenDataItem(BaseOpenData, BaseWebOperations):
    """represents a single data object"""
    _url = None
    _itemId = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _json = None
    _json_dict = None
    _related_items = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 itemId,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._itemId = itemId
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __delattr__(self, name):
        raise AttributeError("Attribute '%s' of '%s' object cannot be deleted"%(name,self.__class__.__name__))
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as a string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __init(self):
        """gets the properties for the site"""
        url = "%s/%s.json" % (self._url, self._itemId)
        params = {"f": "json"}
        json_dict = self._get(url, params,
                         securityHandler=self._securityHandler,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        setattr(self, "data", json_dict['data'])
        if 'data' in json_dict:
            for k,v in json_dict['data'].items():
                setattr(self, k, v)
                del k,v
    #----------------------------------------------------------------------
    import time
    def export(self, outFormat="shp", outFolder=None):
        """exports a dataset t"""
        export_formats = {'shp':".zip", 'kml':'.kml', 'geojson':".geojson",'csv': '.csv'}
        url = "%s/%s%s" % (self._url, self._itemId, export_formats[outFormat])
        results =  self._get(url=url,
                    securityHandler=self._securityHandler,
                    out_folder=outFolder)
        if 'status' in results:
            self.time.sleep(7)
            results = self.export(outFormat=outFormat, outFolder=outFolder)
        return results
