from ..security.security import AGOLTokenSecurityHandler, PortalTokenSecurityHandler
from .._abstract.abstract import BaseAGOLClass
import json
from urllib import quote_plus
import _community, _content, _marketplace, _portals, _oauth2
from ..hostedservice import Services
########################################################################
class Administration(BaseAGOLClass):
    """  Administers the AGOL/Portal Site """
    _securityHandler = None
    _url = None
    _proxy_url = None
    _proxy_port = None
    _token = None
    _currentVersion = None
    _json = None
    _json_dict = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url=None,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._securityHandler = securityHandler
        if url is None and not securityHandler is None:
            url = securityHandler.org_url
        if proxy_url is None and not securityHandler is None:
            self._proxy_url = securityHandler.proxy_url
        if proxy_port is None and not securityHandler is None:
            self._proxy_url = securityHandler.proxy_port

        if url is None or url == '':
            raise AttributeError("URL or Security Hanlder needs to be specified")

        if url.lower().find("/sharing") > -1:
            pass
        else:
            url = url + "/sharing"

        if url.lower().find("/rest") > -1:
            self._url = url
        else:
            self._url = url + "/rest"

        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if securityHandler is not None:
            if isinstance(securityHandler, AGOLTokenSecurityHandler) or \
               isinstance(securityHandler, PortalTokenSecurityHandler):
                self._token = securityHandler.token
                self._referer_url = securityHandler.referer_url
            else:
                raise AttributeError("Security Handler Must be AGOLTokenSecurityHandler or PortalTokenSecurityHandler")
        if initialize:
            self.__init(url=url)
    #----------------------------------------------------------------------
    def __init(self, url):
        """ initializes the site properties """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._securityHandler.token
        json_dict = self._do_get(url, params,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented in Administration class."
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init(url=self._url)
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns object as key/value pairs"""
        if self._json_dict is None:
            self.__init(url=self._url)
        for k,v in self._json_dict.iteritems():
            yield (k,v)
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the current version of the site """
        if self._currentVersion is None:
            self.__init(self._url)
        return self._currentVersion
    #----------------------------------------------------------------------
    def query(self,
              q,
              bbox=None,
              start=1,
              num=10,
              sortField=None,
              sortOrder="asc"):
        """
        This operation searches for content items in the portal. The
        searches are performed against a high performance index that
        indexes the most popular fields of an item. See the Search
        reference page for information on the fields and the syntax of the
        query.
        The search index is updated whenever users add, update, or delete
        content. There can be a lag between the time that the content is
        updated and the time when it's reflected in the search results.
        The results of a search only contain items that the user has
        permission to access.

        Inputs:
           q - The query string used to search
           bbox - The bounding box for a spatial search defined as minx,
                  miny, maxx, or maxy. Search requires q, bbox, or both.
                  Spatial search is an overlaps/intersects function of the
                  query bbox and the extent of the document.
                  Documents that have no extent (e.g., mxds, 3dds, lyr)
                  will not be found when doing a bbox search.
                  Document extent is assumed to be in the WGS84 geographic
                  coordinate system.
           start -  The number of the first entry in the result set
                    response. The index number is 1-based.
                    The default value of start is 1 (that is, the first
                    search result).
                    The start parameter, along with the num parameter, can
                    be used to paginate the search results.
           num - The maximum number of results to be included in the result
                 set response.
                 The default value is 10, and the maximum allowed value is
                 100.
                 The start parameter, along with the num parameter, can be
                 used to paginate the search results.
           sortField - Field to sort by. You can also sort by multiple
                       fields (comma separated) for an item.
                       The allowed sort field names are title, created,
                       type, owner, modified, avgRating, numRatings,
                       numComments, and numViews.
           sortOrder - Describes whether the results return in ascending or
                       descending order. Default is ascending.
                       Values: asc | desc
        """
        if self._url.endswith("/rest"):
            url = self._url + "/search"
        else:
            url = self._url + "/rest/search"

        params = {
            "f" : "json",
            "q" : q,
            "sortOrder" : sortOrder,
            "num" : num,
            "start" : start
        }
        if self._securityHandler is not None:
            params["token"] = self._securityHandler.token
        if sortField is not None:
            params['sortField'] = sortField
        if bbox is not None:
            params['bbox'] = bbox
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def query_without_creds(self,q,
              bbox=None,
              start=1,
              num=10,
              sortField=None,
              sortOrder="asc"):
        """
        This operation searches for content items in the portal. The
        searches are performed against a high performance index that
        indexes the most popular fields of an item. See the Search
        reference page for information on the fields and the syntax of the
        query.
        The search index is updated whenever users add, update, or delete
        content. There can be a lag between the time that the content is
        updated and the time when it's reflected in the search results.
        The results of a search only contain items that the user has
        permission to access.

        Inputs:
           q - The query string used to search
           bbox - The bounding box for a spatial search defined as minx,
                  miny, maxx, or maxy. Search requires q, bbox, or both.
                  Spatial search is an overlaps/intersects function of the
                  query bbox and the extent of the document.
                  Documents that have no extent (e.g., mxds, 3dds, lyr)
                  will not be found when doing a bbox search.
                  Document extent is assumed to be in the WGS84 geographic
                  coordinate system.
           start -  The number of the first entry in the result set
                    response. The index number is 1-based.
                    The default value of start is 1 (that is, the first
                    search result).
                    The start parameter, along with the num parameter, can
                    be used to paginate the search results.
           num - The maximum number of results to be included in the result
                 set response.
                 The default value is 10, and the maximum allowed value is
                 100.
                 The start parameter, along with the num parameter, can be
                 used to paginate the search results.
           sortField - Field to sort by. You can also sort by multiple
                       fields (comma separated) for an item.
                       The allowed sort field names are title, created,
                       type, owner, modified, avgRating, numRatings,
                       numComments, and numViews.
           sortOrder - Describes whether the results return in ascending or
                       descending order. Default is ascending.
                       Values: asc | desc
        """
        if self._url.endswith("/rest"):
            url = self._url + "/search"
        else:
            url = self._url + "/rest/search"
        params = {
            "f" : "json",
            "q" : q,
            "sortOrder" : sortOrder,
            "num" : num,
            "start" : start,
            "focus" : "layers"
        }
        if sortField is not None:
            params['sortField'] = sortField
        if bbox is not None:
            params['bbox'] = bbox
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port,
                            compress=False)
    #----------------------------------------------------------------------
    @property
    def community(self):
        """ return the community class to allow community modifications"""
        return _community.Community(url=self._url + "/community",
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def content(self):
        """
        returns the content class to allow content modifications
        """
        if self._url.endswith("/rest"):
            url = self._url
        else:
            url = self._url + "/rest"
        return _content.Content(url=url + "/content",
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def oauth2(self):
        """
        returns the oauth2 class
        """
        if self._url.endswith("/oauth2"):
            url = self._url
        else:
            url = self._url + "/oauth2"
        return _oauth2.oauth2(oauth_url=url,
                              securityHandler=self._securityHandler,
                              proxy_url=self._proxy_url,
                              proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def portals(self, portalId=None):
        """
        returns the portals class to allow portals mofications
        """
        if self._url.endswith("/rest"):
            url = self._url
        else:
            url = self._url + "/rest"
        url += "/portals"
        return _portals.Portals(url,
                                portalId,
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def hostedServices(self, portalId=None):
        """gets the object to manage site's hosted services"""
        portal = self.portals()
        url = "https://%s/%s/ArcGIS/rest/admin" % (portal.featureServers['https'][0], portal.portalId)
        return Services(url=url,
                        securityHandler=self._securityHandler,
                        proxy_url=self._proxy_url,
                        proxy_port=self._proxy_port)

