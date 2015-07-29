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

    _platform = None
    _disableSignup = None
    _portalLocalHttpPort = None
    _isWindows = None
    _samlEnabled = None
    _portalLocalHttpsPort = None
    _hostedServerHostedFolder = None
    _portalLocalHostname = None
    _supportsSceneServices = None

    _metadataEditable = None
    _backgroundImage = None
    _metadataFormats = None
    _livingAtlasGroupQuery = None

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
            "f" : "json"
        }
        if not self._culture is None:
            params['culture'] = self._culture
        if not self._region is None:
            params['region'] = self._region

        json_dict = self._do_get(url=self._url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implemented in Portals."
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
    def platform(self):
        """gets the platform info"""
        if self._platform is None:
            self.__init()
        return self._platform
    #----------------------------------------------------------------------
    @property
    def disableSignup(self):
        """returns the disableSignup value"""
        if self._disableSignup is None:
            self.__init()
        return self._disableSignup
    #----------------------------------------------------------------------
    @property
    def portalLocalHttpPort(self):
        """gets the portalLocalHttpPort value"""
        if self._portalLocalHttpPort is None:
            self.__init()
        return self._portalLocalHttpPort
    #----------------------------------------------------------------------
    @property
    def isWindows(self):
        """determines if the OS is windows or not"""
        if self._isWindows is None:
            self.__init()
        return self._isWindows
    #----------------------------------------------------------------------
    @property
    def samlEnabled(self):
        """boolean values determines if saml is used on services"""
        if self._samlEnabled is None:
            self.__init()
        return self._samlEnabled
    #----------------------------------------------------------------------
    @property
    def portalLocalHttpsPort(self):
        """gets the portalLocalHttpsPort value"""
        if self._portalLocalHttpsPort is None:
            self.__init()
        return self._portalLocalHttpsPort
    #----------------------------------------------------------------------
    @property
    def hostedServerHostedFolder(self):
        """returns the folder containing the hosted folder"""
        if self._hostedServerHostedFolder is None:
            self.__init()
        return self._hostedServerHostedFolder
    #----------------------------------------------------------------------
    @property
    def portalLocalHostname(self):
        """returns the portal local hostname"""
        if self._portalLocalHostname is None:
            self.__init()
        return self._portalLocalHostname
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
        if self._canSearchPublic is None:
            self.__init()
        return self._canSharePublic
    #----------------------------------------------------------------------
    @property
    def subscriptionInfo(self):
        """returns the subscription information"""
        if self._subscriptionInfo is None:
            self.__init()
        return self._subscriptionInfo
    #----------------------------------------------------------------------
    @property
    def defaultExtent(self):
        """returns the default extent"""
        if self._defaultExtent is None:
            self.__init()
        return self._defaultExtent
    #----------------------------------------------------------------------
    @property
    def supportsHostedServices(self):
        """returns the support of hosted services"""
        if self._supportsHostedServices is None:
            self.__init()
        return self._supportsHostedServices
    #----------------------------------------------------------------------
    @property
    def homePageFeaturedContentCount(self):
        """returns the homePageFeaturedContentCount value"""
        if self._homePageFeaturedContentCount is None:
            self.__init()
        return self._homePageFeaturedContentCount
    #----------------------------------------------------------------------
    @property
    def supportsOAuth(self):
        """returns the supports OAuth value"""
        if self._supportsOAuth is None:
            self.__init()
        return self._supportsOAuth
    #----------------------------------------------------------------------
    @property
    def portalName(self):
        """returns the portal name"""
        if self._portalName is None:
            self.__init()
        return self._portalName
    #----------------------------------------------------------------------
    @property
    def urlKey(self):
        """returns the url key"""
        if self._urlKey is None:
            self.__init()
        return self._urlKey
    #----------------------------------------------------------------------
    @property
    def modified(self):
        """returns the modified value"""
        if self._modified is None:
            self.__init()
        return self._modified
    #----------------------------------------------------------------------
    @property
    def culture(self):
        """returns the culture value"""
        if self._culture is None:
            self.__init()
        return self._culture
    #----------------------------------------------------------------------
    @property
    def helpBase(self):
        """returns the helpBase value"""
        if self._helpBase is None:
            self.__init()
        return self._helpBase
    #----------------------------------------------------------------------
    @property
    def galleryTemplatesGroupQuery(self):
        """returns the value"""
        if self._galleryTemplatesGroupQuery is None:
            self.__init()
        return self._galleryTemplatesGroupQuery
    #----------------------------------------------------------------------
    @property
    def commentsEnabled(self):
        """returns the comments enable value"""
        if self._commentsEnabled is None:
            self.__init()
        return self._commentsEnabled
    #----------------------------------------------------------------------
    @property
    def databaseQuota(self):
        """returns the database quota"""
        if self._databaseQuota is None:
            self.__init()
        return self._databaseQuota
    #----------------------------------------------------------------------
    @property
    def id(self):
        """returns the portal id"""
        if self._id is None:
            self.__init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def canSearchPublic(self):
        """returns the can search public value"""
        if self._canSearchPublic is None:
            self.__init()
        return self._canSearchPublic
    #----------------------------------------------------------------------
    @property
    def customBaseUrl(self):
        """returns the base url"""
        if self._customBaseUrl is None:
            self.__init()
        return self._customBaseUrl
    #----------------------------------------------------------------------
    @property
    def allSSL(self):
        """gets the all SSL value"""
        if self._allSSL is None:
            self.__init()
        return self._allSSL
    #----------------------------------------------------------------------
    @property
    def featuredGroupsId(self):
        """returns the feature groups id"""
        if self._featuredGroupsId is None:
            self.__init()
        return self._featuredGroupsId
    #----------------------------------------------------------------------
    @property
    def defaultBasemap(self):
        """returns the default basemap"""
        if self._defaultBasemap is None:
            self.__init()
        return self._defaultBasemap
    #----------------------------------------------------------------------
    @property
    def created(self):
        """returns the created date"""
        if self._created is None:
            self.__init()
        return self._created
    #----------------------------------------------------------------------
    @property
    def access(self):
        """returns the access value"""
        if self._access is None:
            self.__init()
        return self._access
    #----------------------------------------------------------------------
    @property
    def httpPort(self):
        """returns the http Port"""
        if self._httpPort is None:
            self.__init()
        return self._httpPort
    #----------------------------------------------------------------------
    @property
    def isPortal(self):
        """returns the isPortal value"""
        if self._isPortal is None:
            self.__init()
        return self._isPortal
    #----------------------------------------------------------------------
    @property
    def canSignInArcGIS(self):
        """returns the value"""
        if self._canSignInArcGIS is None:
            self.__init()
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
        if self._httpsPort is None:
            self.__init()
        return self._httpsPort
    #----------------------------------------------------------------------
    @property
    def units(self):
        """returns the default units"""
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def canListPreProvisionedItems(self):
        """returns the value"""
        if self._canListPreProvisionedItems is None:
            self.__init()
        return self._canListPreProvisionedItems
    #----------------------------------------------------------------------
    @property
    def mfaEnabled(self):
        """returns the mfe enabled value"""
        if self._mfaEnabled is None:
            self.__init()
        return self._mfaEnabled
    #----------------------------------------------------------------------
    @property
    def featureGroups(self):
        """returns feature groups value"""
        if self._featuredGroups is None:
            self.__init()
        return self._featuredGroups
    #----------------------------------------------------------------------
    @property
    def thumbnail(self):
        """returns the thumbnail value"""
        if self._thumbnail is None:
            self.__init()
        return self._thumbnail
    #----------------------------------------------------------------------
    @property
    def featuredItemsGroupQuery(self):
        """returns the feature Items group query"""
        if self._galleryTemplatesGroupQuery is None:
            self.__init()
        return self._featuredItemsGroupQuery
    #----------------------------------------------------------------------
    @property
    def canSignInIDP(self):
        """return can signin IDP"""
        if self._canSignInIDP is None:
            self.__init()
        return self._canSignInIDP
    #----------------------------------------------------------------------
    @property
    def storageUsage(self):
        """returns the storage usage"""
        if self._storageUsage is None:
            self.__init()
        return self._storageUsage
    #----------------------------------------------------------------------
    @property
    def rotatorPanels(self):
        """returns the rotator panels"""
        if self._rotatorPanels is None:
            self.__init()
        return self._rotatorPanels
    #----------------------------------------------------------------------
    @property
    def description(self):
        """returns the portal description"""
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def homePageFeatureContent(self):
        """return home page feature content"""
        if self._homePageFeaturedContent is None:
            self.__init()
        return self._homePageFeaturedContent
    #----------------------------------------------------------------------
    @property
    def canProvisionDirectPurchase(self):
        """returns the provision direct purchase"""
        if self._canProvisionDirectPurchase is None:
            self.__init()
        return self._canProvisionDirectPurchase
    #----------------------------------------------------------------------
    @property
    def canListData(self):
        """returns the canListData value"""
        if self._canListData is None:
            self.__init()
        return self._canListData
    #----------------------------------------------------------------------
    @property
    def ipCntryCode(self):
        """returns the ip cntrycode"""
        if self._ipCntryCode is None:
            self.__init()
        return self._ipCntryCode
    #----------------------------------------------------------------------
    @property
    def user(self):
        """returns the user value"""
        if self._user is None:
            self.__init()
        return self._user
    #----------------------------------------------------------------------
    @property
    def helpMap(self):
        """returns the helpmap value"""
        if self._helpMap is None:
            self.__init()
        return self._helpMap
    #----------------------------------------------------------------------
    @property
    def colorSetsGroupQuery(self):
        """returns the colorsets group query"""
        if self._colorSetsGroupQuery is None:
            self.__init()
        return self._colorSetsGroupQuery
    #----------------------------------------------------------------------
    @property
    def canListApps(self):
        """returns the can list apps value"""
        if self._canListApps is None:
            self.__init()
        return self._canListApps
    #----------------------------------------------------------------------
    @property
    def portalProperties(self):
        """returns the portal properties"""
        if self._portalProperties is None:
            self.__init()
        return self._portalProperties
    #----------------------------------------------------------------------
    @property
    def portalHostname(self):
        """returns the portal hostname"""
        if self._portalHostname is None:
            self.__init()
        return self._portalHostname
    #----------------------------------------------------------------------
    @property
    def useStandardizedQuery(self):
        """returns the user standardized query value"""
        if self._useStandardizedQuery is None:
            self.__init()
        return self._useStandardizedQuery
    #----------------------------------------------------------------------
    @property
    def stylesGroupQuery(self):
        """returns the styles group query"""
        if self._stylesGroupQuery is None:
            self.__init()
        return self._stylesGroupQuery
    #----------------------------------------------------------------------
    @property
    def symbolSetsGroupQuery(self):
        """returns the symbolsets group query"""
        if self._symbolSetsGroupQuery is None:
            self.__init()
        return self._symbolSetsGroupQuery
    #----------------------------------------------------------------------
    @property
    def name(self):
        """returns the portal name"""
        if self._name is None:
            self.__init()
        return  self._name
    #----------------------------------------------------------------------
    @property
    def storageQuota(self):
        """returns the storageQuota value"""
        if self._storageQuota is None:
            self.__init()
        return self._storageQuota
    #----------------------------------------------------------------------
    @property
    def canShareBingPublic(self):
        """returns the canShareBingPublic value"""
        if self._canShareBingPublic is None:
            self.__init()
        return self._canShareBingPublic
    #----------------------------------------------------------------------
    @property
    def maxTokenExpirationMinutes(self):
        """returns the maxTokenExpirationMinutes value"""
        if self._maxTokenExpirationMinutes is None:
            self.__init()
        return self._maxTokenExpirationMinutes
    #----------------------------------------------------------------------
    @property
    def layerTemplatesGroupQuery(self):
        """returns the layerTemplatesGroupQuery value"""
        if self._layerTemplatesGroupQuery is None:
            self.__init()
        return self._layerTemplatesGroupQuery
    #----------------------------------------------------------------------
    @property
    def staticImagesUrl(self):
        """returns the staticImagesUrl value"""
        if self._staticImagesUrl is None:
            self.__init()
        return self._staticImagesUrl
    #----------------------------------------------------------------------
    @property
    def databaseUsage(self):
        """returns the databaseUsage value"""
        if self._databaseUsage is None:
            self.__init()
        return self._databaseUsage
    #----------------------------------------------------------------------
    @property
    def showHomePageDescription(self):
        """returns the show home page description value"""
        if self._showHomePageDescription is None:
            self.__init()
        return self._showHomePageDescription
    #----------------------------------------------------------------------
    @property
    def availableCredits(self):
        """returns the available credits"""
        if self._availableCredits is None:
            self.__init()
        return self._availableCredits
    #----------------------------------------------------------------------
    @property
    def helperServices(self):
        """returns the helper services"""
        if self._helperServices is None:
            self.__init()
        return self._helperServices
    #----------------------------------------------------------------------
    @property
    def templatesGroupQuery(self):
        """returns the templates group query"""
        if self._templatesGroupQuery is None:
            self.__init()
        return self._templatesGroupQuery
    #----------------------------------------------------------------------
    @property
    def mfaAdmins(self):
        """returns the mfaAdmins value"""
        if self._mfaAdmins is None:
            self.__init()
        return self._mfaAdmins
    #----------------------------------------------------------------------
    @property
    def basemapGalleryGroupQuery(self):
        """returns the basemap gallery group query"""
        if self._basemapGalleryGroupQuery is None:
            self.__init()
        return self._basemapGalleryGroupQuery
    #----------------------------------------------------------------------
    @property
    def region(self):
        """returns the portal region value"""
        if self._region is None:
            self.__init()
        return self._region
    #----------------------------------------------------------------------
    @property
    def portalMode(self):
        """returns the portal's mode"""
        if self._portalMode is None:
            self.__init()
        return self._portalMode
    #----------------------------------------------------------------------
    @property
    def supportsSceneServices(self):
        """returns the portal's mode"""
        if self._supportsSceneServices is None:
            self.__init()
        return self._supportsSceneServices




    #----------------------------------------------------------------------
    @property
    def metadataEditable(self):
        """returns the metadataEditable"""
        if self._metadataEditable is None:
            self.__init()
        return self._metadataEditable

    #----------------------------------------------------------------------
    @property
    def backgroundImage(self):
        """returns the backgroundImage"""
        if self._backgroundImage is None:
            self.__init()
        return self._backgroundImage

    #----------------------------------------------------------------------
    @property
    def metadataFormats(self):
        """returns the metadataFormats"""
        if self._metadataFormats is None:
            self.__init()
        return self._metadataFormats

    #----------------------------------------------------------------------
    @property
    def livingAtlasGroupQuery(self):
        """returns the livingAtlasGroupQuery"""
        if self._livingAtlasGroupQuery is None:
            self.__init()
        return self._livingAtlasGroupQuery


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
    _json = None
    _json_dict = None
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

    def __init(self):
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """class iterator"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.iteritems():
            yield (k,v)
    #----------------------------------------------------------------------
    def _findPortalId(self):
        """gets the portal id for a site if not known."""
        url = self._baseURL + "/self"
        params = {
            "f" : "json"
        }
        res = self._do_get(url=url, param_dict=params,
                           securityHandler=self._securityHandler,
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
        }
        return self._do_get(url=url, param_dict=params, proxy_url=self._proxy_url,
                            securityHandler=self._securityHandler,
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
            "name" : name,
            "type" : serviceType
        }
        return self._do_get(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
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
            "html" : html,
            "subject" : subject
        }
        if isinstance(invitationList, UserInvite):
            params['invitationList'] = {"invitations":[invitationList.value]}
        elif isinstance(invitationList, list) and \
             isinstance(invitationList[0], UserInvite):
            params['invitationList'] = {"invitations":[iL.value for iL in invitationList]}
        return self._do_post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def languages(self):
        """ list of available languages """
        url = self._url + "/languages"
        params = {
            "f" : "json"

        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
        return ps
    #----------------------------------------------------------------------
    @property
    def regions(self):
        """
        Lists the available regions
        """
        url = self._url + "/regions"
        params = {
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "url" : url,
            "adminUrl" : adminUrl,
            "isHosted" : isHosted,
            "name" : name,
            "serverType" : serverType
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "users" : users
        }
        return self._do_post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
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
            "start" : start,
            "num" : num
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "f" : "json"
        }
        return self._do_post(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
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
            "clearEmptyFields" : clearEmptyFields
        }
        if isinstance(updatePortalParameters, parameters.PortalParameters):
            params.update(updatePortalParameters.value)
        else:
            raise AttributeError("updatePortalParameters must be of type parameter.PortalParameters")
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
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
                             securityHandler=self._securityHandler,
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
            "user" : user,
            "role" : role
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
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
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getRoles(self,
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
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def roles(self):
        """returns a class to work with the site's roles"""
        return Roles(url=self._url + "/roles",
                     securityHandler=self._securityHandler,
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
        endTime = int(local_time_to_online(dt=endTime) /1000)
        params = {
            "f" : "json",
            "vars" : vars,
            "startTime" : "%s000" % startTime,
            "endTime" : "%s000" % endTime,
            "period" : period
        }
        if not groupby is None:
            params['groupby'] = groupby
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
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
        }
        url = self._url + "/cost"
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
########################################################################
class Roles(BaseAGOLClass):
    """Handles the searching, creation, deletion and updating of roles on
    AGOL or Portal.
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        if url.find('/roles') < 0:
            url = url + "/roles"
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the roles as a string"""
        nextCount = 0
        start = 0
        num = 100
        results = []
        while nextCount != -1:
            res = self.roles(start=start + nextCount, num=num)
            results = results + res['roles']
            nextCount = int(res['nextStart'])
        return json.dumps(results)
    #----------------------------------------------------------------------
    def __iter__(self):
        """iterator to loop through role entries"""
        nextCount = 0
        start = 0
        num = 100
        results = []
        while nextCount != -1:
            res = self.roles(start=start + nextCount, num=num)
            for r in res['roles']:
                yield r
            nextCount = int(res['nextStart'])
    #----------------------------------------------------------------------
    def roles(self, start, num):
        """
           lists the custom roles on the AGOL/Portal site

           Input:
              start - default 1
              num - 100 - number of roles to return
        """
        url = self._url
        params = {
            "f" : "json",
            "start" : start,
            "num" : num
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def createRole(self, name, description):
        """
        creates a role for a portal/agol site.
        Inputs:
           names - name of the role
           description - brief text string stating the nature of this
            role.
        Ouput:
           dictionary
        """
        params = {
            "name" : name,
            "description" : description,
            "f" : "json"
        }
        url = self._url + "/createRole"
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def deleteRole(self, roleID):
        """
        deletes a role by ID

        """
        url = self._url + "/%s/delete" % roleID
        params = {
            "f" : "json"
        }
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_post)
    #----------------------------------------------------------------------
    def updateRole(self, roleID, name, description):
        """allows for the role name or description to be modified"""
        params = {
            "name" : name,
            "description" : description,
            "f" : "json"
        }
        url = url + "/%s/update"
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def info(self, roleID):
        """"""
        url = self._url + "/%s" % roleID
        params = {"f" : "json"}
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def findRoleID(self, name):
        """searches the roles by name and returns the role's ID"""
        for r in self:
            if r['name'].lower == name.lower():
                return r['id']
            del r
        return None
    #----------------------------------------------------------------------
    def privileges(self, roleID):
        """returns the assigned priveleges for a given custom role"""
        url = self._url + "/%s/privileges" % roleID
        params = {"f" : "json"}
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def setPrivileges(self, roleID, privileges):
        """
        assigns a role a set of actions that the role can perform on the
        AGOL or Portal site.

        Input:
           roleID - unique id of the role
           privileges - list of privileges to assign to role.
        """
        params = {
            "f" : "json",
            "privileges" : {"privileges": privileges}
        }
        url = self._url + "/%s/setPrivileges" % roleID
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
