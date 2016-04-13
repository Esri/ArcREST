from __future__ import absolute_import
import json
from .administration import Administration as Portal
#from ..common.packages.six.moves.urllib_parse import urlparse, urlunparse
#from .administration.administration import Administration
#from .localportal import PortalAdministration
#from ..connection import SiteConnection
#from ..common._base import BaseDict
#class Portal(BasePortal):
    #"""

    #"""
    #_con = None
    #_root = None
    #_generateToken = None
    #_admin = None
    #_community = None
    #def __init__(self, url, connection):
        #"""initializer"""
        #self._con = connection
        #self._root = self._validate_url(url)
        #self._url = self._root
        #self._generateToken = "{root}/generateToken".format(root=self._root)
        #self.__init() # loads properties @ runtime
    ##----------------------------------------------------------------------
    #def _validate_url(self, url):
        #"""ensures proper URL validation"""
        #parsed = urlparse(url)
        #path = parsed.path
        #if parsed.scheme == "":
            #url = "https://{}".format(url)
            #parsed = urlparse(url)
        #if path[0] == "/":
            #path = parsed.path[1:]
        #if path.strip() == '':
            #return "{}/sharing/rest".format(url)
        #elif path.strip().lower().find('/sharing/rest') > -1:
            #return url
        #if path.strip().lower().find('/sharing') == -1:
            #url = "{scheme}://{netloc}/{path}/sharing".format(scheme=parsed.scheme,
                                                             #netloc=parsed.netloc, path=path)
            #return self._validate_url(url)
        #if path.strip().lower().find('/rest') == -1:
            #url = "{netloc}/{path}/rest".format(netloc=parsed.netloc, path=path)
        #url = "{scheme}://{url}".format(scheme=parsed.scheme, url=url)
        #return url
    ##----------------------------------------------------------------------
    #def __init(self):
        #result = self._con.get(path_or_url=self._root, params={"f":"json"})
        #if isinstance(result, dict):
            #for k,v in result.items():
                #setattr(self, k, v)
                #del k,v
        #elif isinstance(result, str):
            #setattr(self, "error", result)
    ##----------------------------------------------------------------------
    #def search(self,
               #q,
               #t=None,
               #focus=None,
               #bbox=None,
               #start=1,
               #num=10,
               #sortField=None,
               #sortOrder="asc"):
        #"""
        #This operation searches for content items in the portal. The
        #searches are performed against a high performance index that
        #indexes the most popular fields of an item. See the Search
        #reference page for information on the fields and the syntax of the
        #query.
        #The search index is updated whenever users add, update, or delete
        #content. There can be a lag between the time that the content is
        #updated and the time when it's reflected in the search results.
        #The results of a search only contain items that the user has
        #permission to access.

        #Inputs:
           #q - The query string used to search
           #t - type of content to search for.
           #focus - another content filter. Ex: files
           #bbox - The bounding box for a spatial search defined as minx,
                  #miny, maxx, or maxy. Search requires q, bbox, or both.
                  #Spatial search is an overlaps/intersects function of the
                  #query bbox and the extent of the document.
                  #Documents that have no extent (e.g., mxds, 3dds, lyr)
                  #will not be found when doing a bbox search.
                  #Document extent is assumed to be in the WGS84 geographic
                  #coordinate system.
           #start -  The number of the first entry in the result set
                    #response. The index number is 1-based.
                    #The default value of start is 1 (that is, the first
                    #search result).
                    #The start parameter, along with the num parameter, can
                    #be used to paginate the search results.
           #num - The maximum number of results to be included in the result
                 #set response.
                 #The default value is 10, and the maximum allowed value is
                 #100.
                 #The start parameter, along with the num parameter, can be
                 #used to paginate the search results.
           #sortField - Field to sort by. You can also sort by multiple
                       #fields (comma separated) for an item.
                       #The allowed sort field names are title, created,
                       #type, owner, modified, avgRating, numRatings,
                       #numComments, and numViews.
           #sortOrder - Describes whether the results return in ascending or
                       #descending order. Default is ascending.
                       #Values: asc | desc
           #Output:
             #returns a list of dictionary
        #"""
        #return self.administration.search(q=q,
                                          #t=t,
                                          #focus=focus,
                                          #bbox=bbox,
                                          #start=start,
                                          #num=num,
                                          #sortField=sortField,
                                          #sortOrder=sortOrder)
    ##----------------------------------------------------------------------
    #@property
    #def connection(self):
        #"""gets/sets the connection class"""
        #return self._con
    ##----------------------------------------------------------------------
    #@connection.setter
    #def connection(self, value):
        #self._lp = None
        #self._admin = None
        #self._community = None
        #self._content = None
        #self._portals = None
        #if not value is None and \
           #self._con != value:
            #self._con = value
            #self.__init()
        #elif value is None:
            #self._con = SiteConnection(baseurl=self.root)
            #self.__init()
    ##----------------------------------------------------------------------
    #@property
    #def administration(self):
        #"""
        #Creates the hooks into the content/user/item management side of
        #portal.  This gives full access to all the functions of portal
        #and requrires extensive knowledge of the REST API structure.

        #Gives access to all parts of the portal:
         #- community
         #- content
         #- portals
        #"""
        #if self._admin is None:
            #self._admin = Administration(url=self._url,
                                         #connection=self._con)
        #return self._admin
    ###----------------------------------------------------------------------
    ##def community(self):
        ##"""
        ##This set of resources contains operations related to users and groups.
        ##This property provides access via authentacated user to do the
        ##following:
         ##- Accept/Delete/Deny invitations
         ##- Create/Update/Manage/Delete/leave groups
         ##- Assign users to groups
         ##- Delete/Update users
         ##- Find a user
         ##- Enable/Disable accounts
         ##- Manage group applications
         ##- Manage Notifications
         ##- see http://resources.arcgis.com/en/help/arcgis-rest-api/#/Community_Root/02r3000000mq000000/
           ##for full details
        ##Inputs:
         ##None
        ##Ouput:
          ##community class
        ##"""
        ##if self._community is None:
            ##self._community = self.administration.community
        ##return  self._community
    ###----------------------------------------------------------------------
    ##@property
    ##def content(self):
        ##"""
        ##The Portal Content Root operation consists of items, user and group
        ##content, and feature operations. It is a placeholder URI in that
        ##there is no response available at this URI. It acts as a root to its
        ##child resources and operations. All resources and operations (other
        ##than publicly accessible items) under this URI require an
        ##authenticated user (or a user token).

        ##Common tasks under content:
         ##- Add/Remove/Update Items
         ##- Add/Delete relationships
         ##- Export items
         ##- Register applications
         ##- Modify item sharing
         ##- share/move item(s)
         ##- protect/unprotect items
         ##- create services
        ##"""
        ##if self._content is None:
            ##self._content = self.administration.content
        ##return self._content
    ###----------------------------------------------------------------------
    ##@property
    ##def portals(self):
        ##"""
        ##Provides information that describes the portal site.

        ##"""
        ##return self.administration.portals
    ###----------------------------------------------------------------------
    ##@property
    ##def local_portal(self):
        ##"""
        ##This is for local portal sites only.  It provides details local
        ##site administration not used with ArcGIS Online
        ##"""
        ##if self._lp is None and \
           ##self.portals.portalSelf.isPortal == True:
            ##url = self.root.replace("/sharing/rest", "/portaladmin")
            ##admin = self.administration.portals
            ##self._lp = PortalAdministration(connection=self._con, url=url)
            ##return self._lp
        ##elif not self._lp is None:
            ##return self._lp
        ##else:
            ##return None
    ###----------------------------------------------------------------------
    ##@property
    ##def hosted_services(self):
        ##"""provides the class to manage hosted feature services"""
        ##return
    ###----------------------------------------------------------------------
    ##@property
    ##def hosting_server(self):
        ##"""
        ##returns the urls for the hosting servers.  These URLs can then be
        ##used with the manage ArcGIS server functions to control the local
        ##or hosted services on a Portal or ArcGIS Online site.
        ##"""
        ##return []


