
import arcrest
_url = None
_securityHandler = None

class search():
    def __init__(self, url=None, securityHandler=None, proxy_url=None, proxy_port=None):
        """Constructor"""
        
        if url is None and not securityHandler is None:
            url = securityHandler.org_url
        if proxy_url is None and not securityHandler is None:
            self._proxy_url = securityHandler.proxy_url             
        if proxy_port is None and not securityHandler is None:
            self._proxy_url = securityHandler.proxy_port                         
            
        if url is None or url == '':
            raise AttributeError("URL or Security Hanlder needs to be specified")
          
        if url.lower().find("/home") > -1:
            pass
        else:
            url = url + "/home"
        
        if url.lower().find("/search") > -1:
            self._url = url
        else:
            self._url = url + "/search"

        self._securityHandler = securityHandler 
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
    #----------------------------------------------------------------------
    def findItem(self, title, itemType,username=None):
        #
        # Find the itemID of whats being updated
        #        
        url = self._url + "/search"
        #http://arcgissolutions.maps.arcgis.com/home/search.html?q=qwrwq&t=content&focus=maps
        
        if username is None:
            username = self._securityHandler.username
            
        params = {'f': 'json',
                'token': self._securityHandler.token,
                'q': "title:\""+ title + "\"AND owner:\"" + username + "\" AND type:\"" + itemType + "\""}    
        
        jsonResponse = self._do_get(url=url,
                                   param_dict=params,
                                   proxy_url=self._proxy_url,
                                   proxy_port=self._proxy_port)        
        
        if jsonResponse['total'] == 0:
           # print "\nCould not find a service to update. Check the service name in the settings.ini"
            return None
        else:
            return jsonResponse['results'][0]["id"]