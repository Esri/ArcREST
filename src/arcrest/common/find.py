from ..web import _base
_url = None
_securityHandler = None

class search(_base.BaseWebOperations):
    def __init__(self, url=None, securityHandler=None, proxy_url=None, proxy_port=None):
        """Constructor"""

        if url is None and not securityHandler is None:
            url = securityHandler.org_url + "/sharing/rest"
        if proxy_url is None and not securityHandler is None:
            self._proxy_url = securityHandler.proxy_url
        else:
            self._proxy_url = proxy_url
        if proxy_port is None and not securityHandler is None:
            self.proxy_port = securityHandler.proxy_port
        else:
            self._proxy_port = proxy_port
            
        if url is None or url == '':
            raise AttributeError("URL or Security Hanlder needs to be specified")

        #if url.lower().find("/home") > -1:
            #pass
        #else:
            #url = url + "/home"

        if url.lower().find("/search") > -1:
            self._url = url
        else:
            self._url = url + "/search"

        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        
       
    #----------------------------------------------------------------------
    def findItem(self, title, itemType,username=None,searchorg=False):
        #
        # Find the itemID of whats being updated
        #
        types = ('"ArcPad Package"',
              '"Basemap Package"',
              '"Code Attachment"',
              '"Code Sample"',
              '"Color Set"',
              '"Desktop Add In"',
              '"Desktop Application Template"',
              '"Desktop Style"',
              '"Explorer Add In"',
              '"Explorer Layer"',
              '"Explorer Map"',
              '"Feature Collection Template"',
              '"Feature Collection"',
              '"Feature Service"',
              '"Featured Items"',
              '"File Geodatabase"',
              '"Geodata Service"',
              '"Geoprocessing Package"',
              '"Geoprocessing Sample"',
              '"Globe Document"',
              '"Image"',
              '"Image Service"',
              '"KML"',
              '"Layer Package"',
              '"Layer"',
              '"Layout"',
              '"Locator Package"',
              '"Map Document"',
              '"Map Service"',
              '"Map Template"',
              '"Mobile Basemap Package"',
              '"Mobile Map Package"',
              '"Pro Map"',             
              '"Project Package"',
              '"Project Template"',
              '"Published Map"',
              '"Scene Documen"',
              '"Scene Package"',
              '"Scene Service"',
              '"Stream Service"',
              '"Symbol Set"',
              '"Tile Package"',
              '"Windows Mobile Package"',
              '"Windows Viewer Add In"',
              '"Windows Viewer Configuration"',
              '"WMS"',
              '"Workflow Manager Package"',
              '"web mapping application"',
              '"Web Map"')
        if username is None:
            username = self._securityHandler.username
        if searchorg == True:
            params = {'f': 'json',
               'q': "(title:\""+ title + "\" AND type:\"" + itemType + "\")"}               
        else:
            params = {'f': 'json',
               'q': "(title:\""+ title + "\" AND owner:\"" + username + "\" AND type:\"" + itemType + "\")"}
        typstr = ''
        for ty in types:
            if ty !=  '"' + itemType + '"':
                typstr = typstr + " -type: " + ty
            
        params['q'] = params['q'] + typstr
        jsonResponse = self._do_get(url=self._url,
                                   securityHandler=self._securityHandler,
                                   param_dict=params,
                                   proxy_url=self._proxy_url,
                                   proxy_port=self._proxy_port)   
        return jsonResponse
        