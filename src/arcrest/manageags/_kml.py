from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseAGSServer

########################################################################
class KML(BaseAGSServer):
    """
       This resource is a container for all the KMZ files created on the
       server.
    """
    _securityHandler = None
    _items = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - handles site security
        """
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._url = url
        self._securityHandler = securityHandler
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented for KML")
            del k
            del v
    #----------------------------------------------------------------------
    def createKMZ(self, kmz_as_json):
        """
           Creates a KMZ file from json.
           See http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Create_Kmz/02r3000001tm000000/
           for more information.
        """
        kmlURL = self._url + "/createKmz"
        params = {
            "f" : "json",
            "kml" : kmz_as_json
        }
        return self._do_post(url=kmlURL, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def items(self):
        """ returns list of KMZ/KML on server """
        if self._items is None:
            self.__init()
        return self._items
