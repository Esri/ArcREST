from __future__ import absolute_import
from __future__ import print_function
from ...common._base import BaseServer

########################################################################
class KML(BaseServer):
    """
       This resource is a container for all the KMZ files created on the
       server.
    """
    _con = None
    _url = None
    _json_dict = None
    _items = None
    #----------------------------------------------------------------------
    def __init__(self, url, connection,
                 initialize=False):
        """Constructor
            Inputs:
               url - admin url
               connection - SiteConnection object
               initialize - boolean - if true, information loaded at object
                creation
        """
        super(KML, self).__init__(url=url,
              connection=connection,
              initialize=initialize)
        self._con = connection
        self._url = url
        if initialize:
            self.init(connection)
    #----------------------------------------------------------------------
    def createKMZ(self, kmz_as_json):
        """
           Creates a KMZ file from json.
           See http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Create_Kmz/02r3000001tm000000/
           for more information.
        """
        url = self._url + "/createKmz"
        params = {
            "f" : "json",
            "kml" : kmz_as_json
        }
        return self._con.post(path_or_url=url, postdata=params)
    #----------------------------------------------------------------------
    @property
    def items(self):
        """ returns list of KMZ/KML on server """
        if self._items is None:
            self.init()
        return self._items
