"""
"""
from __future__ import absolute_import
from ._base import BasePortal
from .administration import *
class Portal(BasePortal):
    """
    Class that allows users to manage, content, site or users on ArcGIS
    Online or ArcGIS for Portal
    """
    _con = None
    _json_dict = None
    _url = None
    _admin = None
    _localportal = None
    _hosted = None
    #----------------------------------------------------------------------
    def __init(self, connection):
        """loads the properties"""
        self._url = self._validate_url(self._url)
        params = {"f" : "json"}
        result = connection.get(path_or_url=self._url, params=params)
        if isinstance(result, dict):
            self._json_dict = result
            for k,v in result.items():
                setattr(self, k, v)
                del k,v
        else:
            raise RuntimeError("Could not connect to the service: %s" % result)
    #----------------------------------------------------------------------
    def _validate_url(self, url):
        """ensures the url has the sharing/rest appended to it"""
        if url.lower().find("/sharing/rest") > -1:
            return url
        if url.lower().find("/sharing") == -1:
            url = "{url}/sharing".format(url=url)
        if url.lower().find("/rest") == -1:
            url = "{url}/rest".format(url=url)
        return url
    #----------------------------------------------------------------------
    @property
    def is_agol(self):
        url = "{url}/portals/self".format(url=self._url)
        return False
    #----------------------------------------------------------------------
    @property
    def portals(self):
        """returns the Portals class that provides administration access
        into a given organization"""
        url = "%s/portals" % self.root
        return _portals.Portals(url=url,
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
    @property
    def community(self):
        """The portal community root covers user and group resources and
        operations.
        """
        return _community.Community(url=self._url + "/community",
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def content(self):
        """returns access into the site's content"""
        return _content.Content(url=self._url + "/content",
                                connection=self._con)
    #----------------------------------------------------------------------
    def find_item_by_id(self, itemID):
        """locates an item by item ID for a given site"""
        pass
    #----------------------------------------------------------------------
    def search(self,
              q,
              t=None,
              focus=None,
              bbox=None,
              start=1,
              num=10,
              sortField=None,
              sortOrder="asc",
              useSecurity=True):
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
           t - type of content to search for.
           focus - another content filter. Ex: files
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
           useSecurity - boolean value that determines if the security
                         handler object's token will be appended on the
                         search call.  If the value is set to False, then
                         the search will be performed without
                         authentication.  This means only items that have
                         been shared with everyone on AGOL or portal site
                         will be found.  If it is set to True, then all
                         items the user has permission to see based on the
                         query passed will be returned.
           Output:
             returns a list of dictionary
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
        if not focus is None:
            params['focus'] = focus
        if not t is None:
            params['t'] = t
        if useSecurity and \
           self._securityHandler is not None and \
           self._securityHandler.method == "token":
            params["token"] = self._securityHandler.token
        if sortField is not None:
            params['sortField'] = sortField
        if bbox is not None:
            params['bbox'] = bbox

        return self._con.get(path_or_url=url,
                        params=params)

