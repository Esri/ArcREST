"""
   Manages Portal/AGOL content, users, items, etc..
"""
from __future__ import absolute_import
from __future__ import print_function
from ..security import PortalServerSecurityHandler
from .._abstract.abstract import BaseAGOLClass
import json
from . import _community, _content, _portals, _oauth2
from ..hostedservice import Services
from ..manageags import AGSAdministration
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
        if url is None or url == '':
            raise AttributeError("URL or Security Handler needs to be specified")

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

            self._referer_url = securityHandler.referer_url
        else:
            raise AttributeError("Security Handler is required for the administration function")
        if initialize:
            self.__init(url=url)
    #----------------------------------------------------------------------
    def __init(self, url):
        """ initializes the site properties """
        params = {
            "f" : "json"
        }
        json_dict = self._get(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in Administration class.")
            del k, v
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """returns object as a dictionary"""
        if self._json_dict is None:
            self.__init(url=self._url)
        return self._json_dict
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as a string"""
        if self._json is None:
            self.__init(url=self._url)
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """iterates over raw json and returns the values"""
        for k,v in self._json_dict.items():
            yield k,v
    #----------------------------------------------------------------------
    @property
    def root(self):
        """gets the base url"""
        return self._url
    #----------------------------------------------------------------------
    @property
    def tokenURL(self):
        """gets the token url"""
        return self._url + "/generateToken"
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the current version of the site """
        if self._currentVersion is None:
            self.__init(self._url)
        return self._currentVersion
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
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)

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

        return self._get(url=url,
                        param_dict=params,
                        securityHandler=self._securityHandler,
                        proxy_url=self._proxy_url,
                        proxy_port=self._proxy_port)

    #----------------------------------------------------------------------
    def hostingServers(self):
        """
          Returns the objects to manage site's hosted services. It returns
          AGSAdministration object if the site is Portal and it returns a
          hostedservice.Services object if it is AGOL.

        """
        portals = self.portals
        portal = portals.portalSelf
        urls = portal.urls
        if 'error' in urls:
            print( urls)
            return

        services = []
        if urls != {}:
            if 'urls' in urls:
                if 'features' in urls['urls']:
                    if 'https' in urls['urls']['features']:
                        for https in urls['urls']['features']['https']:
                            if portal.isPortal == True:

                                url = "%s/admin" % https
                                #url = https
                                services.append(AGSAdministration(url=url,
                                             securityHandler=self._securityHandler,
                                             proxy_url=self._proxy_url,
                                             proxy_port=self._proxy_port))

                            else:
                                url = "https://%s/%s/ArcGIS/rest/admin" % (https, portal.portalId)
                                services.append(Services(url=url,
                                             securityHandler=self._securityHandler,
                                             proxy_url=self._proxy_url,
                                             proxy_port=self._proxy_port))
                    elif 'http' in urls['urls']['features']:
                        for http in urls['urls']['features']['http']:

                            if (portal.isPortal == True):
                                url = "%s/admin" % http
                                services.append(AGSAdministration(url=url,
                                                                  securityHandler=self._securityHandler,
                                                                  proxy_url=self._proxy_url,
                                                                  proxy_port=self._proxy_port,
                                                                  initialize=True))

                            else:
                                url = "http://%s/%s/ArcGIS/rest/admin" % (http, portal.portalId)
                                services.append(Services(url=url,
                                                          securityHandler=self._securityHandler,
                                                          proxy_url=self._proxy_url,
                                                          proxy_port=self._proxy_port))

                    else:
                        print( "Publishing servers not found")
                else:
                    print ("Publishing servers not found")
            else:
                print( "Publishing servers not found")
            return services
        else:
            for server in portal.servers['servers']:
                url = server['adminUrl'] + "/admin"
                sh = PortalServerSecurityHandler(tokenHandler=self._securityHandler,
                                                   serverUrl=url,
                                                   referer=server['name'].replace(":6080", ":6443")
                                                   )
                services.append(
                    AGSAdministration(url=url,
                                      securityHandler=sh,
                                      proxy_url=self._proxy_url,
                                      proxy_port=self._proxy_port,
                                      initialize=False)
                    )
            return services
