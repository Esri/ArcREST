from ..security.security import OAuthSecurityHandler, AGOLTokenSecurityHandler
from ..common.general import local_time_to_online,online_time_to_string
from .._abstract.abstract import BaseAGOLClass
import os
import urlparse
import parameters
import json
import types
########################################################################
class PortalSelf(BaseAGOLClass):
    """
    represents the basic portal information from the portalSelf()
    """
    _json = None
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _culture = None
    _region = None
    #
    _portalSelfDict = None
    _canSharePublic = None
    _subscriptionInfo = None
    _defaultExtent = None
    _supportsHostedServices = None
    _homePageFeaturedContentCount = None
    _supportsOAuth = None
    _portalName = None
    _urlKey = None
    _modified = None
    _culture = None
    _helpBase = None
    _galleryTemplatesGroupQuery = None
    _commentsEnabled = None
    _databaseQuota = None
    _id = None
    _canSearchPublic = None
    _customBaseUrl = None
    _allSSL = None
    _featuredGroupsId = None
    _defaultBasemap = None
    _created = None
    _access = None
    _httpPort = None
    _isPortal = None
    _canSignInArcGIS = None
    _portalThumbnail = None
    _httpsPort = None
    _units = None
    _canListPreProvisionedItems = None
    _mfaEnabled = None
    _featuredGroups = None
    _thumbnail = None
    _featuredItemsGroupQuery = None
    _canSignInIDP = None
    _storageUsage = None
    _rotatorPanels = None
    _description = None
    _homePageFeaturedContent = None
    _canProvisionDirectPurchase = None
    _canListData = None
    _ipCntryCode = None
    _user = None
    _helpMap = None
    _colorSetsGroupQuery = None
    _canListApps = None
    _portalProperties = None
    _portalHostname = None
    _useStandardizedQuery = None
    _stylesGroupQuery = None
    _symbolSetsGroupQuery = None
    _name = None
    _storageQuota = None
    _canShareBingPublic = None
    _maxTokenExpirationMinutes = None
    _layerTemplatesGroupQuery = None
    _staticImagesUrl = None
    _databaseUsage = None
    _homePageFeaturedContent = None
    _showHomePageDescription = None
    _availableCredits = None
    _helperServices = None
    _templatesGroupQuery = None
    _mfaAdmins = None
    _basemapGalleryGroupQuery = None
    _region = None
    _portalMode = None
    _json_dict = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, culture,
                 region,
                 url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._culture = culture
        self._region = region
        self._url = url
        if not securityHandler is None:
            self._securityHandler = securityHandler
            self._referer_url = securityHandler.referer_url
        proxy_url = self._proxy_url
        proxy_port = self._proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates the object information """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        if not self._culture is None:
            params['culture'] = self._culture
        if not self._region is None:
            params['region'] = self._region

        json_dict = self._do_get(url=self._url,
                                 param_dict=params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
            del k
            del v
    #----------------------------------------------------------------------
    def __iter__(self):
        """"""
        attributes = [attr for attr in dir(self)
              if not attr.startswith('__') and \
              not attr.startswith('_') and \
              not isinstance(getattr(self, attr), (types.MethodType,
                                                   types.BuiltinFunctionType,
                                                   types.BuiltinMethodType)
                             )
              ]
        for att in attributes:
            yield (att, getattr(self, att))
    #----------------------------------------------------------------------
    def __str__(self):
        """gets the object as a string"""
        if self._json_dict is not None:
            return json.dumps(self._json_dict)
        return "{}"
    #----------------------------------------------------------------------
    @property
    def featuredGroups(self):
        """returns the featured groups property"""
        if self._featuredGroups is None:
            self.__init()
        return self._featuredGroups
    #----------------------------------------------------------------------
    @property
    def homePageFeaturedContent(self):
        """returns the homePageFeaturedContent property"""
        if self._homePageFeaturedContent is None:
            self.__init()
        return self._homePageFeaturedContent
    #----------------------------------------------------------------------
    @property
    def canSharePublic(self):
        """gets the can share public value"""
        return self._canSharePublic
    #----------------------------------------------------------------------
    @property
    def subscriptionInfo(self):
        """returns the subscription information"""
        return self._subscriptionInfo
    #----------------------------------------------------------------------
    @property
    def defaultExtent(self):
        """returns the default extent"""
        return self._defaultExtent
    #----------------------------------------------------------------------
    @property
    def supportsHostedServices(self):
        """returns the support of hosted services"""
        return self._supportsHostedServices
    #----------------------------------------------------------------------
    @property
    def homePageFeaturedContentCount(self):
        """returns the homePageFeaturedContentCount value"""
        return self._homePageFeaturedContentCount
    #----------------------------------------------------------------------
    @property
    def supportsOAuth(self):
        """returns the supports OAuth value"""
        return self._supportsOAuth
    #----------------------------------------------------------------------
    @property
    def portalName(self):
        """returns the portal name"""
        return self._portalName
    #----------------------------------------------------------------------
    @property
    def urlKey(self):
        """returns the url key"""
        return self._urlKey
    #----------------------------------------------------------------------
    @property
    def modified(self):
        """returns the modified value"""
        return self._modified
    #----------------------------------------------------------------------
    @property
    def culture(self):
        """returns the culture value"""
        return self._culture
    #----------------------------------------------------------------------
    @property
    def helpBase(self):
        """returns the helpBase value"""
        return self._helpBase
    #----------------------------------------------------------------------
    @property
    def galleryTemplatesGroupQuery(self):
        """returns the value"""
        return self._galleryTemplatesGroupQuery
    #----------------------------------------------------------------------
    @property
    def commentsEnabled(self):
        """returns the comments enable value"""
        return self._commentsEnabled
    #----------------------------------------------------------------------
    @property
    def databaseQuota(self):
        """returns the database quota"""
        return self._databaseQuota
    #----------------------------------------------------------------------
    @property
    def id(self):
        """returns the portal id"""
        return self._id
    #----------------------------------------------------------------------
    @property
    def canSearchPublic(self):
        """returns the can search public value"""
        return self._canSearchPublic
    #----------------------------------------------------------------------
    @property
    def customBaseUrl(self):
        """returns the base url"""
        return self._customBaseUrl
    #----------------------------------------------------------------------
    @property
    def allSSL(self):
        """gets the all SSL value"""
        return self._allSSL
    #----------------------------------------------------------------------
    @property
    def featuredGroupsId(self):
        """returns the feature groups id"""
        return self._featuredGroupsId
    #----------------------------------------------------------------------
    @property
    def defaultBasemap(self):
        """returns the default basemap"""
        return self._defaultBasemap
    #----------------------------------------------------------------------
    @property
    def created(self):
        """returns the created date"""
        return self._created
    #----------------------------------------------------------------------
    @property
    def access(self):
        """returns the access value"""
        return self._access
    #----------------------------------------------------------------------
    @property
    def httpPort(self):
        """returns the http Port"""
        return self._httpPort
    #----------------------------------------------------------------------
    @property
    def isPortal(self):
        """returns the isPortal value"""
        return self._isPortal
    #----------------------------------------------------------------------
    @property
    def canSignInArcGIS(self):
        """returns the value"""
        return self._canSignInArcGIS
    #----------------------------------------------------------------------
    @property
    def portalThumbnail(self):
        """returns the portal thumbnail"""
        return self._portalThumbnail
    #----------------------------------------------------------------------
    @property
    def httpsPort(self):
        """returns the https port"""
        return self._httpsPort
    #----------------------------------------------------------------------
    @property
    def units(self):
        """returns the default units"""
        return self._units
    #----------------------------------------------------------------------
    @property
    def canListPreProvisionedItems(self):
        """returns the value"""
        return self._canListPreProvisionedItems
    #----------------------------------------------------------------------
    @property
    def mfaEnabled(self):
        """returns the mfe enabled value"""
        return self._mfaEnabled
    #----------------------------------------------------------------------
    @property
    def featureGroups(self):
        """returns feature groups value"""
        return self._featuredGroups
    #----------------------------------------------------------------------
    @property
    def thumbnail(self):
        """returns the thumbnail value"""
        return self._thumbnail
    #----------------------------------------------------------------------
    @property
    def featuredItemsGroupQuery(self):
        """returns the feature Items group query"""
        return self._featuredItemsGroupQuery
    #----------------------------------------------------------------------
    @property
    def canSignInIDP(self):
        """return can signin IDP"""
        return self._canSignInIDP
    #----------------------------------------------------------------------
    @property
    def storageUsage(self):
        """returns the storage usage"""
        return self._storageUsage
    #----------------------------------------------------------------------
    @property
    def rotatorPanels(self):
        """returns the rotator panels"""
        return self._rotatorPanels
    #----------------------------------------------------------------------
    @property
    def description(self):
        """returns the portal description"""
        return self._description
    #----------------------------------------------------------------------
    @property
    def homePageFeatureContent(self):
        """return home page feature content"""
        return self._homePageFeaturedContent
    #----------------------------------------------------------------------
    @property
    def canProvisionDirectPurchase(self):
        """returns the provision direct purchase"""
        return self._canProvisionDirectPurchase
    #----------------------------------------------------------------------
    @property
    def canListData(self):
        """returns the canListData value"""
        return self._canListData
    #----------------------------------------------------------------------
    @property
    def ipCntryCode(self):
        """returns the ip cntrycode"""
        return self._ipCntryCode
    #----------------------------------------------------------------------
    @property
    def user(self):
        """returns the user value"""
        return self._user
    #----------------------------------------------------------------------
    @property
    def helpMap(self):
        """returns the helpmap value"""
        return self._helpMap
    #----------------------------------------------------------------------
    @property
    def colorSetsGroupQuery(self):
        """returns the colorsets group query"""
        return self._colorSetsGroupQuery
    #----------------------------------------------------------------------
    @property
    def canListApps(self):
        """returns the can list apps value"""
        return self._canListApps
    #----------------------------------------------------------------------
    @property
    def portalProperties(self):
        """returns the portal properties"""
        return self._portalProperties
    #----------------------------------------------------------------------
    @property
    def portalHostname(self):
        """returns the portal hostname"""
        return self._portalHostname
    #----------------------------------------------------------------------
    @property
    def useStandardizedQuery(self):
        """returns the user standardized query value"""
        return self._useStandardizedQuery
    #----------------------------------------------------------------------
    @property
    def stylesGroupQuery(self):
        """returns the styles group query"""
        return self._stylesGroupQuery
    #----------------------------------------------------------------------
    @property
    def symbolSetsGroupQuery(self):
        """returns the symbolsets group query"""
        return self._symbolSetsGroupQuery
    #----------------------------------------------------------------------
    @property
    def name(self):
        """returns the portal name"""
        return  self._name
    #----------------------------------------------------------------------
    @property
    def storageQuota(self):
        """returns the storageQuota value"""
        return self._storageQuota
    #----------------------------------------------------------------------
    @property
    def canShareBingPublic(self):
        """returns the canShareBingPublic value"""
        return self._canShareBingPublic
    #----------------------------------------------------------------------
    @property
    def maxTokenExpirationMinutes(self):
        """returns the maxTokenExpirationMinutes value"""
        return self._maxTokenExpirationMinutes
    #----------------------------------------------------------------------
    @property
    def layerTemplatesGroupQuery(self):
        """returns the layerTemplatesGroupQuery value"""
        return self._layerTemplatesGroupQuery
    #----------------------------------------------------------------------
    @property
    def staticImagesUrl(self):
        """returns the staticImagesUrl value"""
        return self._staticImagesUrl
    #----------------------------------------------------------------------
    @property
    def databaseUsage(self):
        """returns the databaseUsage value"""
        return self._databaseUsage
    #----------------------------------------------------------------------
    @property
    def showHomePageDescription(self):
        """returns the show home page description value"""
        return self._showHomePageDescription
    #----------------------------------------------------------------------
    @property
    def availableCredits(self):
        """returns the available credits"""
        return self._availableCredits
    #----------------------------------------------------------------------
    @property
    def helperServices(self):
        """returns the helper services"""
        return self._helperServices
    #----------------------------------------------------------------------
    @property
    def templatesGroupQuery(self):
        """returns the templates group query"""
        return self._templatesGroupQuery
    #----------------------------------------------------------------------
    @property
    def mfaAdmins(self):
        """returns the mfaAdmins value"""
        return self._mfaAdmins
    #----------------------------------------------------------------------
    @property
    def basemapGalleryGroupQuery(self):
        """returns the basemap gallery group query"""
        return self._basemapGalleryGroupQuery
    #----------------------------------------------------------------------
    @property
    def region(self):
        """returns the portal region value"""
        return self._region
    #----------------------------------------------------------------------
    @property
    def portalMode(self):
        """returns the portal's mode"""
        return self._portalMode
########################################################################
class UserInvite(object):
    """
    represents a user to invite to a user
    """
    _username = None
    _password = None
    _firstName = None
    _lastName = None
    _fullName = None
    _email = None
    _role = None
    _allowedRole = ["account_publisher", "account_user", "account_admin"]
    #----------------------------------------------------------------------
    def __init__(self, username, password, firstName, lastName,
                 email, role="account_user"):
        """Constructor"""
        self._username = username
        self._password = password
        self._firstName = firstName
        self._lastName = lastName
        self._fullName = firstName + " " + lastName
        self._email = email
        if role.lower() in self._allowedRole:
            self._role = role
        else:
            raise AttributeError("Invalid Role: %s" % role)
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns object as dictionary"""
        return {
            "username": self._username,
            "password": self._password,
            "firstname": self._firstName,
            "lastname": self._lastName,
            "fullname":self.fullName,
            "email":self._email,
            "role":self.role
        }
    #----------------------------------------------------------------------
    def __str__(self):
        """object as a string"""
        return json.dumps(self.value)

    #----------------------------------------------------------------------
    @property
    def firstName(self):
        """gets/sets the first name"""
        return self._firstName
    #----------------------------------------------------------------------
    @firstName.setter
    def firstName(self, value):
        """gets/sets the first name"""
        if self._firstName != value:
            self._firstName = value
    #----------------------------------------------------------------------
    @property
    def lastName(self):
        """gets/sets the last name"""
        return self._lastName
    #----------------------------------------------------------------------
    @lastName.setter
    def lastName(self, value):
        """gets/sets the last name"""
        if self._lastName != value:
            self._lastName = value
    #----------------------------------------------------------------------
    @property
    def email(self):
        """gets/sets the email"""
        return self._email
    #----------------------------------------------------------------------
    @email.setter
    def email(self, value):
        """gets/sets the email"""
        if self._email != value:
            self._email = value
    #----------------------------------------------------------------------
    @property
    def password(self):
        """gets/sets the password"""
        return self._password
    #----------------------------------------------------------------------
    @password.setter
    def password(self, value):
        """gets/sets the password"""
        if self._password != value:
            self._password = value
    #----------------------------------------------------------------------
    @property
    def username(self):
        """gets/sets the user name"""
        return self._username
    #----------------------------------------------------------------------
    @username.setter
    def username(self, value):
        """gets/sets the user name"""
        if self._username != value:
            self._username = value
    #----------------------------------------------------------------------
    @property
    def role(self):
        """gets/sets the role name"""
        return self._role
    #----------------------------------------------------------------------
    @role.setter
    def role(self, value):
        """gets/sets the role name"""
        if self._role != value and \
           self._role.lower() in self._allowedRole:
            self._role = value
    #----------------------------------------------------------------------
    @property
    def fullName(self):
        """gets the full name of the user"""
        return self._firstName + " " + self._lastName


########################################################################
class Portals(BaseAGOLClass):
    """
    provides access to the portals' child resources.
    """
    _baseURL = None
    _url = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _portalId = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 portalId=None,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        if url.lower().find("/portals") < 0:
            url = url + "/portals"
        self._baseURL = url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        if portalId is not None:
            self._portalId = portalId
            self._url = url + "/%s" % portalId
            self._referer_url = securityHandler.referer_url
        else:
            portalId = self._findPortalId()
            self._portalId = portalId
            self._url = url + "/%s" % portalId
            self._referer_url = securityHandler.referer_url
    #----------------------------------------------------------------------
    def _findPortalId(self):
        """gets the portal id for a site if not known."""
        url = self._baseURL + "/self"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        res = self._do_get(url=url, param_dict=params,
                           proxy_port=self._proxy_port,
                           proxy_url=self._proxy_url)
        if res.has_key('id'):
            return res['id']
        else:
            raise AttributeError("Invalid URL or token")
    #----------------------------------------------------------------------
    @property
    def portalId(self):
        """gets the portal Id"""
        if self._portalId is None:
            self._findPortalId()
        return self._portalId
    #----------------------------------------------------------------------
    @property
    def urls(self):
        """gets the hosting server information"""
        if self._portalId is None:
            self._findPortalId()
        url = self._baseURL + "/%s/urls" % self._portalId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url, param_dict=params, proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def featureServers(self):
        """gets the hosting feature AGS Server"""
        if self.urls == {}:
            return {}
        return self.urls["urls"]['features']
    #----------------------------------------------------------------------
    @property
    def tileServers(self):
        """gets the tile server base urls"""
        if self.urls == {}:
            return {}
        return self.urls["urls"]['tiles']
    #----------------------------------------------------------------------
    @property
    def portalRoot(self):
        """ returns the base url without the portal id """
        return self._baseURL
    #----------------------------------------------------------------------
    def addResource(self, key, filePath, text):
        """
        The add resource operation allows the administrator to add a file
        resource, for example, the organization's logo or custom banner.
        The resource can be used by any member of the organization. File
        resources use storage space from your quota and are scanned for
        viruses.

        Inputs:
           key - The name the resource should be stored under.
           filePath - path of file to upload
           text - Some text to be written (for example, JSON or JavaScript)
                  directly to the resource from a web client.
        """
        url = self._url + "/addresource"
        params = {
        "f": "json",
        "token" : self._securityHandler.token,
        "key" : key,
        "text" : text
        }
        parsed = urlparse.urlparse(url)
        files = []
        files.append(('file', filePath, os.path.basename(filePath)))
        res = self._post_multipart(host=parsed.hostname,
                                           selector=parsed.path,
                                           files = files,
                                           fields=params,
                                           port=parsed.port,
                                           ssl=parsed.scheme.lower() == 'https',
                                           proxy_port=self._proxy_port,
                                           proxy_url=self._proxy_url)
        return res
    #----------------------------------------------------------------------
    def checkServiceName(self,
                         name,
                         serviceType):
        """
        Checks to see if a given service name and type are available for
        publishing a new service. true indicates that the name and type is
        not found in the organization's services and is available for
        publishing. false means the requested name and type are not available.

        Inputs:
           name - requested name of service
           serviceType - type of service allowed values: Feature Service or
                         Map Service
        """
        _allowedTypes = ['Feature Service', "Map Service"]
        url = self._url + "/isServiceNameAvailable"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "name" : name,
            "type" : serviceType
        }
        return self._do_get(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def inviteUser(self, invitationList, html, subject):
        """Invites a user or users to a site.

        Inputs:
           invitationList - either an UserInvite object or a list of
                            UserInvite object.
           html - text of invite email with HTML formatting
           subject - subject of email to send
        """
        url = self._baseURL + "/self/invite"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "html" : html,
            "subject" : subject
        }
        if isinstance(invitationList, UserInvite):
            params['invitationList'] = {"invitations":[invitationList.value]}
        elif isinstance(invitationList, list) and \
             isinstance(invitationList[0], UserInvite):
            params['invitationList'] = {"invitations":[iL.value for iL in invitationList]}
        return self._do_post(url=url, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def languages(self):
        """ list of available languages """
        url = self._url + "/languages"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,

        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def portalProperties(self):
        """
        Portal returns information on your organization and is accessible
        to administrators. Publishers and information workers can view
        users and resources of the organization.
        """
        url = self._url
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def portalSelf(self, usePortalId=True, culture=None, region=None):
        """
        The Portal Self resource is used to return the view of the portal
        as seen by the current user, anonymous or logged in. It includes
        information such as the name, logo, featured items, and supported
        protocols (HTTP vs. HTTPS) for this portal. If the user is not
        logged in, this call will return the default view of the portal. If
        the user is logged in, the view of the returned portal will be
        specific to the organization to which the user belongs. The default
        view of the portal is dependent on the culture of the user, which
        is obtained from the user's profile. A parameter to pass in the
        locale/culture is available for anonymous users.

        Inputs:
           culture - the culture code of the calling client output is
                     customized for this culture if settings are available
           region - the region code of the calling client.
        """
        if usePortalId == False:
            url = self._url + "/self"
        else:
            url = self._baseURL + "/self"

        ps = PortalSelf(culture=culture,
                        region=region,
                        url=url,
                        securityHandler=self._securityHandler,
                        proxy_url=self._proxy_url,
                        proxy_port=self._proxy_port)
        #ps._referer_url = self._referer_url
        return ps
    #----------------------------------------------------------------------
    @property
    def regions(self):
        """
        Lists the available regions
        """
        url = self._url + "/regions"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def registerServer(self,
                       name,
                       url,
                       adminUrl,
                       isHosted,
                       serverType):
        """
        You can optionally register (or "federate") an ArcGIS Server site
        with your Portal for ArcGIS deployment. This provides the
        following benefits:
             The server and the portal share the same user store (that of
             the portal). This results in a convenient single sign-on
             experience.

             Any items you publish to the server are automatically shared
             on the portal.

             You can optionally allow the server to host tiled map services
             and feature services published by portal users.

        After you register a server with your portal, you must invoke the
        Update Security Configuration operation on the ArcGIS Server site
        and configure the site's security store to take advantage of users
        and roles from the portal.

        This operation is only applicable to Portal for ArcGIS; it is not
        supported with ArcGIS Online.

        Inputs:
           name - The fully qualified name of the machine hosting the
                  ArcGIS Server site, followed by the port.
           url - The externally visible URL of the ArcGIS Server site,
                 using the fully qualified name of the machine.
           adminUrl - The administrative URL of your ArcGIS Server site,
                      using the fully qualified name of the machine.
           isHosted - A Boolean property denoting whether the ArcGIS Server
                      site will be allowed to host services for the portal
                      (true) or not be allowed to host services (false).
           serverType - The type of server being registered with the portal
                        For example: ArcGIS.
        """
        url = self._url + "/register"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "url" : url,
            "adminUrl" : adminUrl,
            "isHosted" : isHosted,
            "name" : name,
            "serverType" : serverType
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeResource(self, key):
        """
        The Remove Resource operation allows the administrator to remove a
        file resource.

        Input:
           key - name of resource to delete
        """
        url = self._url + "/removeresource"
        params = {
            "key" : key,
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def removeUser(self, users):
        """
        The Remove Users operation allows the administrator to remove users
        from a portal. Before the administrator can remove the user, all of
        the user's content and groups must be reassigned or deleted.

        Inputs:
           users - Comma-separated list of usernames to remove.
        """
        url = self._url + "/removeusers"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "users" : users
        }
        return self._do_post(url=url, param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def resources(self,
                  start=1,
                  num=10):
        """
        Resources lists all file resources for the organization. The start
        and num paging parameters are supported.

        Inputs:
           start - the number of the first entry in the result set response
                   The index number is 1-based and the default is 1
           num - the maximum number of results to be returned as a whole #
        """
        url = self._url + "/resources"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "start" : start,
            "num" : num
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def server(self, serverId):
        """
        This resource represents an ArcGIS Server site that has been
        federated with the portal.
        This resource is not applicable to ArcGIS Online; it is only
        applicable to Portal for ArcGIS.
        """
        url = self._url + "/servers/%s" % serverId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def servers(self):
        """
        This resource lists the ArcGIS Server sites that have been
        federated with the portal. This resource is not applicable to
        ArcGIS Online; it is only applicable to Portal for ArcGIS.
        """
        url = self._url + "/servers"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def unregisterServer(self, serverId):
        """
        This operation unregisters an ArcGIS Server site from the portal.
        The server is no longer federated with the portal after this
        operation completes.
        After this operation completes, you must invoke the Update Security
        Configuration operation on your ArcGIS Server site to specify how
        you want the server to work with users and roles.

        Inputs:
           serverId - unique identifier of the server
        """
        url = self._url + "/servers/%s/unregister" % serverId
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        return self._do_post(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def update(self,
               updatePortalParameters,
               clearEmptyFields=False):
        """
        The Update operation allows administrators only to update the
        organization information such as name, description, thumbnail, and
        featured groups.

        Inputs:
           updatePortalParamters - parameter.PortalParameters object that holds information to update
           clearEmptyFields - boolean that clears all whitespace from fields
        """
        url = self._url + "/update"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "clearEmptyFields" : clearEmptyFields
        }
        if isinstance(updatePortalParameters, parameters.PortalParameters):
            params.update(updatePortalParameters.value)
        else:
            raise AttributeError("updatePortalParameters must be of type parameter.PortalParameters")
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateServer(self,
                     serverId,
                     name,
                     url,
                     adminUrl,
                     isHosted,
                     serverType):
        """
        This operation updates the properties of an ArcGIS Server site that
        has been registered, or federated, with the portal. For example,
        you can use this operation to change the federated site that acts
        as the portal's hosting server.

        Inputs:
           serverId - identifier of server to update.
           name - The fully qualified name of the machine hosting the
                  ArcGIS Server site, followed by the port.
           url - The externally visible URL of the ArcGIS Server site,
                 using the fully qualified name of the machine.
           adminUrl - The administrative URL of the ArcGIS Server site,
                      using the fully qualified name of the machine.
           isHosted - A Boolean property denoting whether the ArcGIS Server
                      site will be allowed to host services for the portal
                      (true) or will not be allowed to host services
                      (false).
           serverType - The type of server being registered with the portal
                        For example: ArcGIS.
        """
        url = self._url + "/%s/update" % serverId
        params = {
            "name" : name,
            "url" : url,
            "adminUrl" : adminUrl,
            "isHosted" : isHosted,
            "serverType" : serverType
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateUserRole(self,
                       user,
                       role):
        """
        The Update User Role operation allows the administrator of an org
        anization to update the role of a user within a portal.

        Inputs:
           role - Sets the user's role.
                  Roles are the following:
                      org_user - Ability to add items, create groups, and
                        share in the organization.
                      org_publisher - Same privileges as org_user plus the
                        ability to publish hosted services from ArcGIS for
                        Desktop and ArcGIS Online.
                      org_admin - In addition to add, create, share, and publish
                        capabilities, an org_admin administers and customizes
                        the organization.
                  Example: role=org_publisher
           user - The username whose role you want to change.

        """
        url = self._url + "/updateuserrole"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "user" : user,
            "role" : role
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def users(self,
              start=1,
              num=10,
              sortField="fullName",
              sortOrder="asc",
              role=None):
        """
        Lists all the members of the organization. The start and num paging
        parameters are supported.

        Inputs:
           start - The number of the first entry in the result set response.
                   The index number is 1-based.
                   The default value of start is 1 (that is, the first
                   search result).
                   The start parameter, along with the num parameter, can
                   be used to paginate the search results.
           num - The maximum number of results to be included in the result
                 set response.
                 The default value is 10, and the maximum allowed value is
                 100.The start parameter, along with the num parameter, can
                 be used to paginate the search results.
           sortField - field to sort on
           sortOrder - asc or desc on the sortField
           role - name of the role or role id to search
        """
        url = self._url + "/users"
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "start" : start,
            "num" : num
        }
        if not role is None:
            params['role'] = role
        if not sortField is None:
            params['sortField'] = sortField
        if not sortOrder is None:
            params['sortOrder'] = sortOrder
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def roles(self,
              start=1,
              num=100):
        """
           lists the custom roles on the AGOL/Portal site

           Input:
              start - default 1
              num - 100 - number of roles to return
        """
        url = self._url.replace(self._portalId, "") + "self/roles"
        params = {
            "f" : "json",
            "start" : start,
            "num" : num
        }
        if not self._securityHandler is None:
            params['token'] = self._securityHandler.token
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def usage(self,
              startTime,
              endTime,
              vars,
              period="1d",
              groupby=None
              ):
        """
        returns the usage statistics value
        """
        url = self._url + "/usage"
        startTime = int(local_time_to_online(dt=startTime)/ 1000)
        print startTime
        print "1429660800000"
        endTime = int(local_time_to_online(dt=endTime) /1000)
        params = {
            "f" : "json",
            "token" : self._securityHandler.token,
            "vars" : vars,
            "startTime" : "%s000" % startTime,
            "endTime" : "%s000" % endTime,
            "period" : period
        }
        if not groupby is None:
            params['groupby'] = groupby
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def cost(self):
        """
        returns the cost values for a given portal
        """
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        url = self._url + "/cost" #% (self.portalId, )
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)