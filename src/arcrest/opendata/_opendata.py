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
    _last_search = None
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
    def search(self,
               q=None,
               bbox=None,
               keyword=None,
               sort_by='relevance',
               page=1,
               per_page=100,
               quality=None,
               group_id=None):
        """
        searches the opendata site and returns the data results

        Inputs:
           q - query term
           bbox - takes input as pair of lat/long
           keyword - filter for tags
           sort_by - criteria for sorting:
                     Supported Criteria:
                       name
                       relevance
                       updated_at
                       created_at
                       quality
           page - page number of the search results
           per_page - how many results are returned (max 100)
           quality - metadata quality. Number you pass is the lowest
            'quality' score you want.
           group_id - filter for returning datasets that are only in
            the group with the specified id.
        """
        params = {}
        results = []
        get_all = False
        if q is not None:
            params['q'] = q
        if bbox is not None:
            params['bbox'] = bbox
        if keyword is not None:
            params['keyword'] = keyword

        params['sort_by'] = sort_by
        if isinstance(page, int):
            params['page'] = page
        params['per_page'] = per_page
        if quality is not None:
            params['quality'] = quality
        if group_id is not None:
            params['group_id'] = group_id
        self._last_search =  self._do_get(url=self._url + ".json",
                                           param_dict=params,
                                           securityHandler=None,
                                           proxy_url=self._proxy_url,
                                           proxy_port=self._proxy_port)
        return self._last_search  # TODO: merge searches? or how to better handle search for all?
    #----------------------------------------------------------------------
    def metadata(self):
        """gets the metadata """
        return self._metadata
    #----------------------------------------------------------------------
    @property
    def data(self):
        """returns the data objects from the last search"""
        if self._last_search is None:
            self.search()
        for d in self._last_search['data']:
            yield OpenDataItem(url=self._url + "/%s" % d['id'],
                               proxy_url=self._proxy_url,
                               proxy_port=self._proxy_port,
                               initialize=True)

#http://opendata.arcgis.com/datasets/4d83e90db45e48a688376c431ceec81f_0/related.json
#http://opendata.arcgis.com/datasets/4d83e90db45e48a688376c431ceec81f_0.json
########################################################################
class OpenDataItem(BaseOpenData):
    # TODO: add functions to export item?
    # TODO: some results return 404, how do you handle this without raising a show
    #       stopping error?
    """represents a single data object"""
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _json = None
    _json_dict = None
    _related_items = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __delattr__(self,name):
        raise AttributeError,"Attribute '%s' of '%s' object cannot be deleted"%(name,self.__class__.__name__)
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as a string"""
        return self._json
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
        setattr(self, "data", json_dict['data'])
        if 'data' in json_dict:
            for k,v in json_dict['data'].items():
                setattr(self, k, v)
                del k,v
    def asShapefile(self, outfolder, outSR=None):
        """
        exports the dataset as a shapefile

        Inputs:
           outfolder - save location of the file.
           outSR - export spatial reference (optional)
        Output:
           full path to downloaded file
        """
        params = {}
        url = self._url + ".zip"
        if outSR is not None:
            params['outSR'] = outSR
        return self._download_file(url=url,
                                   securityHandler=self._securityHandler,
                                   save_path=outfolder,
                                   param_dict=params,
                                   proxy_url=self._proxy_url,
                                   proxy_port=self._proxy_port)
