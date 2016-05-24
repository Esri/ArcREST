"""
   OpenData Operations
"""
from __future__ import absolute_import
import json
import time
from ._base import BaseOpenData
########################################################################
class OpenData(BaseOpenData):
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
                 connection,
                 url=None):
        """Constructor"""
        if url is None:
            url = "http://opendata.arcgis.com/"
        self._url = url

        self._con = connection
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
        ds_data =  self._con.get(path_or_url=url,
                                 params=param_dict)
        return ds_data
    #----------------------------------------------------------------------
    def getDataset(self, itemId):
        """gets a dataset class"""
        if self._url.lower().find('datasets') > -1:
            url = self._url
        else:
            url = self._url + "/datasets"
        return OpenDataItem(url=url,
                            connection=self._con,
                            itemId=itemId)
########################################################################
class OpenDataItem(BaseOpenData):
    """represents a single data object"""
    _url = None
    _con = None
    _itemId = None
    _json = None
    _json_dict = None
    _related_items = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 connection,
                 itemId,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._itemId = itemId
        self._con = connection
        if initialize:
            self.__init(connection)
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
    def __init(self, connection=None):
        """gets the properties for the site"""
        if connection is None:
            connection = self._con
        url = "%s/%s.json" % (self._url, self._itemId)
        params = {"f": "json"}
        json_dict = self._con.get(path_or_url=url, params=params)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        setattr(self, "data", json_dict['data'])
        if 'data' in json_dict:
            for k,v in json_dict['data'].items():
                setattr(self, k, v)
                del k,v
        if isinstance(json_dict, dict):
            self.__dict__.update(json_dict)
    #----------------------------------------------------------------------
    def export(self, outFormat="shp", outFolder=None):
        """exports a dataset t"""
        export_formats = {'shp':".zip", 'kml':'.kml', 'geojson':".geojson",'csv': '.csv'}
        url = "%s/%s%s" % (self._url, self._itemId, export_formats[outFormat])
        results =  self._con.get(path_or_url=url,
                                 out_folder=outFolder)
        if 'status' in results:
            time.sleep(7)
            results = self.export(outFormat=outFormat, outFolder=outFolder)
        return results
