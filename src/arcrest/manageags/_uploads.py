from .._abstract.abstract import BaseAGSServer
########################################################################
class Uploads(BaseAGSServer):
    """
    This resource is a collection of all the items that have been uploaded
    to the server.
    See: http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Uploads/02r3000001qr000000/
    """
    _uploads = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _url = None

    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor"""
        if url.lower().find("uploads") < -1:
            self._url = url + "/uploads"
        else:
            self._url = url
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url

    #----------------------------------------------------------------------
    @property
    def uploads(self):
        """
        returns a collection of all the items that have been uploaded to
        the server.
        """
        params = {
            "f" :"json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=self._url,
                            param_dict=params,
                            header={},
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)

    #----------------------------------------------------------------------
    def deleteItem(self, itemId):
        """
           Deletes the uploaded item and its configuration.
           Inputs:
              itemId - unique ID of the item
        """
        url = self._url + "/%s/delete" % itemId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=url, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def item(self, itemId):
        """
        This resource represents an item that has been uploaded to the
        server. Various workflows upload items and then process them on the
        server. For example, when publishing a GIS service from ArcGIS for
        Desktop or ArcGIS Server Manager, the application first uploads the
        service definition (.SD) to the server and then invokes the
        publishing geoprocessing tool to publish the service.
        Each uploaded item is identified by a unique name (itemID). The
        pathOnServer property locates the specific item in the ArcGIS
        Server system directory.
        The committed parameter is set to true once the upload of
        individual parts is complete.
        """
        url = self._url + "/%s" % itemId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def uploadItem(self, filePath, description):
        """"""
        import urlparse
        url = self._url + "/upload"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        files = []
        files.append(('itemFile', filePath, os.path.basename(filePath)))
        parsed = urlparse.urlparse(url)
        return self._post_multipart(host=parsed.hostname,
                                       selector=parsed.path,
                                       files = files,
                                       fields=params,
                                       port=parsed.port,
                                       ssl=parsed.scheme.lower() == 'https',
                                       proxy_port=self._proxy_port,
                                       proxy_url=self._proxy_url)

