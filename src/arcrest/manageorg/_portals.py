from ..security.security import OAuthSecurityHandler, AGOLTokenSecurityHandler, PortalServerSecurityHandler
from ..manageags import AGSAdministration
from ..hostedservice import Services
from ..common.general import local_time_to_online,online_time_to_string
from .._abstract.abstract import BaseAGOLClass
import os
import urlparse
import _parameters as parameters
import json
import types
########################################################################
class Portals(BaseAGOLClass):
    """
    A multitenant portal contains multiple portals, each one of which is
    owned by and represents an organization. Each user in the multitenant
    portal belongs to one of these organizational portals or to a default
    portal that includes all users who do not belong to an organization.
    The Portals Root resource is a root placeholder resource that covers
    all the portals contained in the multitenant portal.
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _culture = None
    _region = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        if url.lower().endswith("/portals"):
            self._url = url
        else:
            self._url = "%s/portals" % url
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
    #----------------------------------------------------------------------
    @property
    def root(self):
        """gets the classes url"""
        return self._url
    #----------------------------------------------------------------------
    @property
    def regions(self):
        """gets the regions value"""
        url = "%s/regions" % self.root
        params = {"f": "json"}
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def languages(self):
        """returns the site's languages"""
        url = "%s/languages" % self.root
        params = {'f': "json"}
        return self._do_get(url=url,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def info(self):
        """gets the sharing api information"""
        url = "%s/info" % self.root
        params = {"f": "json"}
        return self._do_get(url=url,
                    param_dict=params,
                    proxy_url=self._proxy_url,
                    proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def portalSelf(self):
        """The portal to which the current user belongs. This is an
        organizational portal if the user belongs to an organization or the
        default portal if the user does not belong to one"""
        url = "%s/self" % self.root
        return Portal(url=url,
                      securityHandler=self._securityHandler,
                      proxy_url=self._proxy_url,
                      proxy_port=self._proxy_port,
                      )
    #----------------------------------------------------------------------
    def portal(self, portalID=None):
        """returns a specific reference to a portal"""
        if portalID is None:
            portalID = self.portalSelf.id
        url = "%s/%s" % (self.root, portalID)
        return Portal(url=url,
                  securityHandler=self._securityHandler,
                  proxy_url=self._proxy_url,
                  proxy_port=self._proxy_port,
                  initalize=True)
    #----------------------------------------------------------------------
    @property
    def portalId(self):
        """gets the portal Id"""
        return self.portalSelf.id
########################################################################
class Portal(BaseAGOLClass):
    """
    Portal returns information on your organization and is accessible to
    administrators. Publishers and information workers can view users and
    resources of the organization.
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _json = None
    _json_dict = None
    _canSharePublic = None
    _defaultExtent = None
    _supportsHostedServices = None
    _homePageFeaturedContentCount = None
    _supportsOAuth = None
    _portalName = None
    _databaseUsage = None
    _culture = None
    _helpBase = None
    _galleryTemplatesGroupQuery = None
    _commentsEnabled = None
    _databaseQuota = None
    _id = None
    _canSearchPublic = None
    _customBaseUrl = None
    _allSSL = None
    _httpPort = None
    _featuredGroupsId = None
    _defaultBasemap = None
    _created = None
    _access = None
    _platform = None
    _isPortal = None
    _canSignInArcGIS = None
    _disableSignup = None
    _httpsPort = None
    _units = None
    _backgroundImage = None
    _mfaEnabled = None
    _featuredGroups = None
    _thumbnail = None
    _featuredItemsGroupQuery = None
    _canSignInIDP = None
    _useStandardizedQuery = None
    _rotatorPanels = None
    _description = None
    _homePageFeaturedContent = None
    _helperServices = None
    _canProvisionDirectPurchase = None
    _canListData = None
    _user = None
    _helpMap = None
    _canListPreProvisionedItems = None
    _colorSetsGroupQuery = None
    _canListApps = None
    _portalProperties = None
    _isWindows = None
    _name = None
    _supportsSceneServices = None
    _stylesGroupQuery = None
    _samlEnabled = None
    _symbolSetsGroupQuery = None
    _portalLocalHttpPort = None
    _storageQuota = None
    _canShareBingPublic = None
    _maxTokenExpirationMinutes = None
    _layerTemplatesGroupQuery = None
    _staticImagesUrl = None
    _modified = None
    _portalHostname = None
    _showHomePageDescription = None
    _availableCredits = None
    _portalMode = None
    _portalLocalHttpsPort = None
    _hostedServerHostedFolder = None
    _storageUsage = None
    _templatesGroupQuery = None
    _portalLocalHostname = None
    _basemapGalleryGroupQuery = None
    _mfaAdmins = None
    _portalId = None
    _subscriptionInfo = None
    _urlKey = None
    _metadataEditable = None
    _portalThumbnail = None
    _metadataFormats = None
    _ipCntryCode = None
    _livingAtlasGroupQuery = None
    _region = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initalize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initalize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """loads the property data into the class"""
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self.root,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
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
                print k, " - attribute not implemented in Portal class."
    #----------------------------------------------------------------------
    def _findPortalId(self):
        """gets the portal id for a site if not known."""
        if not self.root.lower().endswith("/self"):
            url = self.root + "/self"
        else:
            url = self.root
        params = {
            "f" : "json"
        }
        res = self._do_get(url=url, param_dict=params,
                           securityHandler=self._securityHandler,
                           proxy_port=self._proxy_port,
                           proxy_url=self._proxy_url)
        if res.has_key('id'):
            return res['id']
        return None
    ##----------------------------------------------------------------------
    #@property
    #def hostingServers(self):
        #"""returns a list of servers that host non-tile based content for a
        #site."""
        #return
    ##----------------------------------------------------------------------
    #@property
    #def tileServers(self):
        #""""""
        #return
    #----------------------------------------------------------------------
    @property
    def subscriptionInfo(self):
        '''gets the property value for subscriptionInfo'''
        if self._subscriptionInfo is None:
            self.__init()
        return self._subscriptionInfo

    #----------------------------------------------------------------------
    @property
    def urlKey(self):
        '''gets the property value for urlKey'''
        if self._urlKey is None:
            self.__init()
        return self._urlKey

    #----------------------------------------------------------------------
    @property
    def metadataEditable(self):
        '''gets the property value for metadataEditable'''
        if self._metadataEditable is None:
            self.__init()
        return self._metadataEditable

    #----------------------------------------------------------------------
    @property
    def portalThumbnail(self):
        '''gets the property value for portalThumbnail'''
        if self._portalThumbnail is None:
            self.__init()
        return self._portalThumbnail

    #----------------------------------------------------------------------
    @property
    def metadataFormats(self):
        '''gets the property value for metadataFormats'''
        if self._metadataFormats is None:
            self.__init()
        return self._metadataFormats

    #----------------------------------------------------------------------
    @property
    def ipCntryCode(self):
        '''gets the property value for ipCntryCode'''
        if self._ipCntryCode is None:
            self.__init()
        return self._ipCntryCode

    #----------------------------------------------------------------------
    @property
    def livingAtlasGroupQuery(self):
        '''gets the property value for livingAtlasGroupQuery'''
        if self._livingAtlasGroupQuery is None:
            self.__init()
        return self._livingAtlasGroupQuery

    #----------------------------------------------------------------------
    @property
    def region(self):
        '''gets the property value for region'''
        if self._region is None:
            self.__init()
        return self._region

    #----------------------------------------------------------------------
    @property
    def portalId(self):
        """gets the portal Id"""
        if self._portalId is None:
            self._portalId = self._findPortalId()
        return self._portalId
    #----------------------------------------------------------------------
    def __str__(self):
        """returns class as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """iterates through raw JSON"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.iteritems():
            yield [k,v]
    #----------------------------------------------------------------------
    @property
    def root(self):
        """returns classes URL"""
        return self._url
    #----------------------------------------------------------------------
    @property
    def canSharePublic(self):
        '''gets the property value for canSharePublic'''
        if self._canSharePublic is None:
            self.__init()
        return self._canSharePublic

    #----------------------------------------------------------------------
    @property
    def defaultExtent(self):
        '''gets the property value for defaultExtent'''
        if self._defaultExtent is None:
            self.__init()
        return self._defaultExtent

    #----------------------------------------------------------------------
    @property
    def supportsHostedServices(self):
        '''gets the property value for supportsHostedServices'''
        if self._supportsHostedServices is None:
            self.__init()
        return self._supportsHostedServices

    #----------------------------------------------------------------------
    @property
    def homePageFeaturedContentCount(self):
        '''gets the property value for homePageFeaturedContentCount'''
        if self._homePageFeaturedContentCount is None:
            self.__init()
        return self._homePageFeaturedContentCount

    #----------------------------------------------------------------------
    @property
    def supportsOAuth(self):
        '''gets the property value for supportsOAuth'''
        if self._supportsOAuth is None:
            self.__init()
        return self._supportsOAuth

    #----------------------------------------------------------------------
    @property
    def portalName(self):
        '''gets the property value for portalName'''
        if self._portalName is None:
            self.__init()
        return self._portalName

    #----------------------------------------------------------------------
    @property
    def databaseUsage(self):
        '''gets the property value for databaseUsage'''
        if self._databaseUsage is None:
            self.__init()
        return self._databaseUsage

    #----------------------------------------------------------------------
    @property
    def culture(self):
        '''gets the property value for culture'''
        if self._culture is None:
            self.__init()
        return self._culture

    #----------------------------------------------------------------------
    @property
    def helpBase(self):
        '''gets the property value for helpBase'''
        if self._helpBase is None:
            self.__init()
        return self._helpBase

    #----------------------------------------------------------------------
    @property
    def galleryTemplatesGroupQuery(self):
        '''gets the property value for galleryTemplatesGroupQuery'''
        if self._galleryTemplatesGroupQuery is None:
            self.__init()
        return self._galleryTemplatesGroupQuery

    #----------------------------------------------------------------------
    @property
    def commentsEnabled(self):
        '''gets the property value for commentsEnabled'''
        if self._commentsEnabled is None:
            self.__init()
        return self._commentsEnabled

    #----------------------------------------------------------------------
    @property
    def databaseQuota(self):
        '''gets the property value for databaseQuota'''
        if self._databaseQuota is None:
            self.__init()
        return self._databaseQuota

    #----------------------------------------------------------------------
    @property
    def id(self):
        '''gets the property value for id'''
        if self._id is None:
            self.__init()
        return self._id

    #----------------------------------------------------------------------
    @property
    def canSearchPublic(self):
        '''gets the property value for canSearchPublic'''
        if self._canSearchPublic is None:
            self.__init()
        return self._canSearchPublic

    #----------------------------------------------------------------------
    @property
    def customBaseUrl(self):
        '''gets the property value for customBaseUrl'''
        if self._customBaseUrl is None:
            self.__init()
        return self._customBaseUrl

    #----------------------------------------------------------------------
    @property
    def allSSL(self):
        '''gets the property value for allSSL'''
        if self._allSSL is None:
            self.__init()
        return self._allSSL

    #----------------------------------------------------------------------
    @property
    def httpPort(self):
        '''gets the property value for httpPort'''
        if self._httpPort is None:
            self.__init()
        return self._httpPort

    #----------------------------------------------------------------------
    @property
    def featuredGroupsId(self):
        '''gets the property value for featuredGroupsId'''
        if self._featuredGroupsId is None:
            self.__init()
        return self._featuredGroupsId

    #----------------------------------------------------------------------
    @property
    def defaultBasemap(self):
        '''gets the property value for defaultBasemap'''
        if self._defaultBasemap is None:
            self.__init()
        return self._defaultBasemap

    #----------------------------------------------------------------------
    @property
    def created(self):
        '''gets the property value for created'''
        if self._created is None:
            self.__init()
        return self._created

    #----------------------------------------------------------------------
    @property
    def access(self):
        '''gets the property value for access'''
        if self._access is None:
            self.__init()
        return self._access

    #----------------------------------------------------------------------
    @property
    def platform(self):
        '''gets the property value for platform'''
        if self._platform is None:
            self.__init()
        return self._platform

    #----------------------------------------------------------------------
    @property
    def isPortal(self):
        '''gets the property value for isPortal'''
        if self._isPortal is None:
            self.__init()
        return self._isPortal

    #----------------------------------------------------------------------
    @property
    def canSignInArcGIS(self):
        '''gets the property value for canSignInArcGIS'''
        if self._canSignInArcGIS is None:
            self.__init()
        return self._canSignInArcGIS

    #----------------------------------------------------------------------
    @property
    def disableSignup(self):
        '''gets the property value for disableSignup'''
        if self._disableSignup is None:
            self.__init()
        return self._disableSignup

    #----------------------------------------------------------------------
    @property
    def httpsPort(self):
        '''gets the property value for httpsPort'''
        if self._httpsPort is None:
            self.__init()
        return self._httpsPort

    #----------------------------------------------------------------------
    @property
    def units(self):
        '''gets the property value for units'''
        if self._units is None:
            self.__init()
        return self._units

    #----------------------------------------------------------------------
    @property
    def backgroundImage(self):
        '''gets the property value for backgroundImage'''
        if self._backgroundImage is None:
            self.__init()
        return self._backgroundImage

    #----------------------------------------------------------------------
    @property
    def mfaEnabled(self):
        '''gets the property value for mfaEnabled'''
        if self._mfaEnabled is None:
            self.__init()
        return self._mfaEnabled

    #----------------------------------------------------------------------
    @property
    def featuredGroups(self):
        '''gets the property value for featuredGroups'''
        if self._featuredGroups is None:
            self.__init()
        return self._featuredGroups

    #----------------------------------------------------------------------
    @property
    def thumbnail(self):
        '''gets the property value for thumbnail'''
        if self._thumbnail is None:
            self.__init()
        return self._thumbnail

    #----------------------------------------------------------------------
    @property
    def featuredItemsGroupQuery(self):
        '''gets the property value for featuredItemsGroupQuery'''
        if self._featuredItemsGroupQuery is None:
            self.__init()
        return self._featuredItemsGroupQuery

    #----------------------------------------------------------------------
    @property
    def canSignInIDP(self):
        '''gets the property value for canSignInIDP'''
        if self._canSignInIDP is None:
            self.__init()
        return self._canSignInIDP

    #----------------------------------------------------------------------
    @property
    def useStandardizedQuery(self):
        '''gets the property value for useStandardizedQuery'''
        if self._useStandardizedQuery is None:
            self.__init()
        return self._useStandardizedQuery

    #----------------------------------------------------------------------
    @property
    def rotatorPanels(self):
        '''gets the property value for rotatorPanels'''
        if self._rotatorPanels is None:
            self.__init()
        return self._rotatorPanels

    #----------------------------------------------------------------------
    @property
    def description(self):
        '''gets the property value for description'''
        if self._description is None:
            self.__init()
        return self._description

    #----------------------------------------------------------------------
    @property
    def homePageFeaturedContent(self):
        '''gets the property value for homePageFeaturedContent'''
        if self._homePageFeaturedContent is None:
            self.__init()
        return self._homePageFeaturedContent

    #----------------------------------------------------------------------
    @property
    def helperServices(self):
        '''gets the property value for helperServices'''
        if self._helperServices is None:
            self.__init()
        return self._helperServices

    #----------------------------------------------------------------------
    @property
    def canProvisionDirectPurchase(self):
        '''gets the property value for canProvisionDirectPurchase'''
        if self._canProvisionDirectPurchase is None:
            self.__init()
        return self._canProvisionDirectPurchase

    #----------------------------------------------------------------------
    @property
    def canListData(self):
        '''gets the property value for canListData'''
        if self._canListData is None:
            self.__init()
        return self._canListData

    #----------------------------------------------------------------------
    @property
    def user(self):
        '''gets the property value for user'''
        if self._user is None:
            self.__init()
        return self._user
    #----------------------------------------------------------------------
    @property
    def helpMap(self):
        '''gets the property value for helpMap'''
        if self._helpMap is None:
            self.__init()
        return self._helpMap

    #----------------------------------------------------------------------
    @property
    def canListPreProvisionedItems(self):
        '''gets the property value for canListPreProvisionedItems'''
        if self._canListPreProvisionedItems is None:
            self.__init()
        return self._canListPreProvisionedItems

    #----------------------------------------------------------------------
    @property
    def colorSetsGroupQuery(self):
        '''gets the property value for colorSetsGroupQuery'''
        if self._colorSetsGroupQuery is None:
            self.__init()
        return self._colorSetsGroupQuery

    #----------------------------------------------------------------------
    @property
    def canListApps(self):
        '''gets the property value for canListApps'''
        if self._canListApps is None:
            self.__init()
        return self._canListApps

    #----------------------------------------------------------------------
    @property
    def portalProperties(self):
        '''gets the property value for portalProperties'''
        if self._portalProperties is None:
            self.__init()
        return self._portalProperties

    #----------------------------------------------------------------------
    @property
    def isWindows(self):
        '''gets the property value for isWindows'''
        if self._isWindows is None:
            self.__init()
        return self._isWindows

    #----------------------------------------------------------------------
    @property
    def name(self):
        '''gets the property value for name'''
        if self._name is None:
            self.__init()
        return self._name

    #----------------------------------------------------------------------
    @property
    def supportsSceneServices(self):
        '''gets the property value for supportsSceneServices'''
        if self._supportsSceneServices is None:
            self.__init()
        return self._supportsSceneServices

    #----------------------------------------------------------------------
    @property
    def stylesGroupQuery(self):
        '''gets the property value for stylesGroupQuery'''
        if self._stylesGroupQuery is None:
            self.__init()
        return self._stylesGroupQuery

    #----------------------------------------------------------------------
    @property
    def samlEnabled(self):
        '''gets the property value for samlEnabled'''
        if self._samlEnabled is None:
            self.__init()
        return self._samlEnabled

    #----------------------------------------------------------------------
    @property
    def symbolSetsGroupQuery(self):
        '''gets the property value for symbolSetsGroupQuery'''
        if self._symbolSetsGroupQuery is None:
            self.__init()
        return self._symbolSetsGroupQuery

    #----------------------------------------------------------------------
    @property
    def portalLocalHttpPort(self):
        '''gets the property value for portalLocalHttpPort'''
        if self._portalLocalHttpPort is None:
            self.__init()
        return self._portalLocalHttpPort

    #----------------------------------------------------------------------
    @property
    def storageQuota(self):
        '''gets the property value for storageQuota'''
        if self._storageQuota is None:
            self.__init()
        return self._storageQuota

    #----------------------------------------------------------------------
    @property
    def canShareBingPublic(self):
        '''gets the property value for canShareBingPublic'''
        if self._canShareBingPublic is None:
            self.__init()
        return self._canShareBingPublic

    #----------------------------------------------------------------------
    @property
    def maxTokenExpirationMinutes(self):
        '''gets the property value for maxTokenExpirationMinutes'''
        if self._maxTokenExpirationMinutes is None:
            self.__init()
        return self._maxTokenExpirationMinutes

    #----------------------------------------------------------------------
    @property
    def layerTemplatesGroupQuery(self):
        '''gets the property value for layerTemplatesGroupQuery'''
        if self._layerTemplatesGroupQuery is None:
            self.__init()
        return self._layerTemplatesGroupQuery

    #----------------------------------------------------------------------
    @property
    def staticImagesUrl(self):
        '''gets the property value for staticImagesUrl'''
        if self._staticImagesUrl is None:
            self.__init()
        return self._staticImagesUrl

    #----------------------------------------------------------------------
    @property
    def modified(self):
        '''gets the property value for modified'''
        if self._modified is None:
            self.__init()
        return self._modified

    #----------------------------------------------------------------------
    @property
    def portalHostname(self):
        '''gets the property value for portalHostname'''
        if self._portalHostname is None:
            self.__init()
        return self._portalHostname

    #----------------------------------------------------------------------
    @property
    def showHomePageDescription(self):
        '''gets the property value for showHomePageDescription'''
        if self._showHomePageDescription is None:
            self.__init()
        return self._showHomePageDescription

    #----------------------------------------------------------------------
    @property
    def availableCredits(self):
        '''gets the property value for availableCredits'''
        if self._availableCredits is None:
            self.__init()
        return self._availableCredits

    #----------------------------------------------------------------------
    @property
    def portalMode(self):
        '''gets the property value for portalMode'''
        if self._portalMode is None:
            self.__init()
        return self._portalMode

    #----------------------------------------------------------------------
    @property
    def portalLocalHttpsPort(self):
        '''gets the property value for portalLocalHttpsPort'''
        if self._portalLocalHttpsPort is None:
            self.__init()
        return self._portalLocalHttpsPort

    #----------------------------------------------------------------------
    @property
    def hostedServerHostedFolder(self):
        '''gets the property value for hostedServerHostedFolder'''
        if self._hostedServerHostedFolder is None:
            self.__init()
        return self._hostedServerHostedFolder

    #----------------------------------------------------------------------
    @property
    def storageUsage(self):
        '''gets the property value for storageUsage'''
        if self._storageUsage is None:
            self.__init()
        return self._storageUsage

    #----------------------------------------------------------------------
    @property
    def templatesGroupQuery(self):
        '''gets the property value for templatesGroupQuery'''
        if self._templatesGroupQuery is None:
            self.__init()
        return self._templatesGroupQuery

    #----------------------------------------------------------------------
    @property
    def portalLocalHostname(self):
        '''gets the property value for portalLocalHostname'''
        if self._portalLocalHostname is None:
            self.__init()
        return self._portalLocalHostname

    #----------------------------------------------------------------------
    @property
    def basemapGalleryGroupQuery(self):
        '''gets the property value for basemapGalleryGroupQuery'''
        if self._basemapGalleryGroupQuery is None:
            self.__init()
        return self._basemapGalleryGroupQuery

    #----------------------------------------------------------------------
    @property
    def mfaAdmins(self):
        '''gets the property value for mfaAdmins'''
        if self._mfaAdmins is None:
            self.__init()
        return self._mfaAdmins
    #----------------------------------------------------------------------
    @property
    def urls(self):
        """gets the urls for a portal"""
        url = "%s/urls" % self.root
        params = {"f":"json"}
        return self._do_get(url=url,
                     param_dict=params,
                     securityHandler=self._securityHandler,
                     proxy_url=self._proxy_url,
                     proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def featureServers(self):
        """gets the hosting feature AGS Server"""
        services = []
        if self.urls == {}:
            return {}
        urls = self.urls
        if 'https' in urls['urls']['features']:
            res = urls['urls']['features']['https']
        else:
            res = urls['urls']['features']['http']
        for https in res:
            if self.isPortal:
                url = "%s/admin" % https
                services.append(AGSAdministration(url=url,
                                                  securityHandler=self._securityHandler,
                                                  proxy_url=self._proxy_url,
                                                  proxy_port=self._proxy_port)
                                )
            else:
                url = "https://%s/%s/ArcGIS/admin" % (https, self.portalId)
                services.append(Services(url=url,
                                         securityHandler=self._securityHandler,
                                         proxy_url=self._proxy_url,
                                         proxy_port=self._proxy_port))
        return services
    #----------------------------------------------------------------------
    @property
    def tileServers(self):
        """
          Returns the objects to manage site's tile hosted services/servers. It returns
          AGSAdministration object if the site is Portal and it returns a
          hostedservice.Services object if it is AGOL.
        """
        services = []
        ishttps = False
        if self.urls == {}:
            return {}
        urls = self.urls["urls"]['tiles']
        if 'https' in urls:
            res = urls['https']
            ishttps = True
        else:
            res = urls['http']
        for https in res:
            if ishttps:
                scheme = "https"
            else:
                scheme = "http"
            if self.isPortal == False:
                url = "%s://%s/tiles/%s/arcgis/admin/services" % (scheme, https, self.portalId)
                services.append(Services(url=url,
                    securityHandler=self._securityHandler,
                    proxy_url=self._proxy_url,
                    proxy_port=self._proxy_port))
            else:
                url = "%s/admin" % https
                servers = self.servers
                for server in servers.servers:
                    url = server.adminUrl
                    sh = PortalServerSecurityHandler(tokenHandler=self._securityHandler,
                                                     serverUrl=url,
                                                     referer=server.name.split(":")[0]
                                                     )
                    services.append(
                        AGSAdministration(url=url,
                                          securityHandler=sh,
                                          proxy_url=self._proxy_url,
                                          proxy_port=self._proxy_port,
                                          initialize=True)
                    )
        return services
    #----------------------------------------------------------------------
    @property
    def purchases(self):
        """gets the portal's purchases"""
        url = "%s/purchases" % self.root
        params = {"f":"json"}
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def customers(self):
        """gets the site's customers"""
        url = "%s/customers" % self.root
        params = {"f":"json"}
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def exportCustomers(self, outPath):
        """exports customer list to a csv file
        Input:
         outPath - save location of the customer list
        """
        url = "%s/customers/export" % self.root
        params = {"f":"csv"}
        return self._download_file(url=url, save_path=outPath,
                                   securityHandler=self._securityHandler,
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
        url = self.root + "/update"
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
    def isServiceNameAvailable(self,
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
    @property
    def servers(self):
        """gets the federated or registered servers for Portal"""
        url = "%s/servers" % self.root
        return Servers(url=url,
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
        Output:
         list of User classes
        """
        users = []
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
        from _community import Community
        res = self._do_post(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)

        if "users" in res:
            if len(res['users']) > 0:
                cURL = "https://%s/sharing/rest/community" % self.portalHostname
                com = Community(url=cURL,
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
                for r in res['users']:
                    users.append(
                        com.users.user(r["username"])
                    )
        res['users'] = users
        return res
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
        url = self.root + "/createRole"
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def roles(self):
        """gets the roles class that allows admins to manage custom roles
        on portal"""
        return Roles(url="%s/roles" % self.root,
                     securityHandler=self._securityHandler,
                     proxy_url=self._proxy_url,
                     proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def cost(self,
             tileStorage=0,
             fileStorage=0,
             featureStorage=0,
             generatedTileCount=0,
             loadedTileCount=0,
             enrichVariableCount=0,
             enrichReportCount=0,
             serviceAreaCount=0,
             geocodeCount=0):
        """
        returns the cost values for a given portal
        Inputs:
         tileStorage - int - numbe of tiles to store in MBs
         fileStorage - int - size of file to store in MBs
         featureStorage - int - size in MBs
         generateTileCount - int - number of tiles to genearte on site
         loadedTileCount -int- cost to host a certian number of tiles
         enrichVariableCount - int - cost to enrich data
         enrichReportCount - int - cost to generate an enrichment report
         serviceAreaCount - int - cost to generate x number of service
          areas
         geocodeCount - int - cost to generate x number of addresses
        """
        params = {
            "f" : "json",
            "tileStorage": tileStorage,
            "fileStorage": fileStorage,
            "featureStorage": featureStorage,
            "generatedTileCount": generatedTileCount,
            "loadedTileCount":loadedTileCount,
            "enrichVariableCount": enrichVariableCount,
            "enrichReportCount" : enrichReportCount,
            "serviceAreaCount" : serviceAreaCount,
            "geocodeCount" : geocodeCount
        }
        url = self._url + "/cost"
        return self._do_post(url=url,
                             param_dict=params,
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
        url = self.root + "/addresource"
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
        return self._do_post(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def securityPolicy(self):
        """gets the object to manage the portal's security policy"""
        url = "%s/securityPolicy" % self.root
        params = {'f': 'json'}
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def resetSecurityPolicy(self):
        """resets the security policy to default install"""
        params = {"f" : "json"}
        url = "%s/securityPolicy/reset" % self.root
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateSecurityPolicy(self,
                             minLength=8,
                             minUpper=None,
                             minLower=None,
                             minLetter=None,
                             minDigit=None,
                             minOther=None,
                             expirationInDays=None,
                             historySize=None):
        """updates the Portals security policy"""
        params = {
            "f" : "json",
            "minLength" : minLength,
            "minUpper": minUpper,
            "minLower": minLower,
            "minLetter": minLetter,
            "minDigit": minDigit,
            "minOther": minOther,
            "expirationInDays" : expirationInDays,
            "historySize": historySize
        }
        url = "%s/securityPolicy/update" % self.root
        return self._do_post(url=url,
                     param_dict=params,
                     securityHandler=self._securityHandler,
                     proxy_url=self._proxy_url,
                     proxy_port=self._proxy_port)

    #----------------------------------------------------------------------
    @property
    def portalAdmin(self):
        """gets a reference to a portal administration class"""
        from ..manageportal import PortalAdministration
        return PortalAdministration(admin_url="https://%s/portaladmin" % self.portalHostname,
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port,
                                    initalize=False)
    #----------------------------------------------------------------------
    def addUser(self, invitationList,
                subject, html):
        """
        adds a user without sending an invitation email

        Inputs:
           invitationList - InvitationList class used to add users without
            sending an email
           subject - email subject
           html - email message sent to users in invitation list object
        """
        url = self._url + "/invite"
        params = {"f" : "json"}
        if isinstance(invitationList, parameters.InvitationList):
            params['invitationList'] = invitationList.value()
        params['html'] = html
        params['subject'] = subject
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def inviteByEmail(self,
                   emails,
                   subject,
                   text,
                   html,
                   role="org_user",
                   mustApprove=True,
                   expiration=1440):
        """Invites a user or users to a site.

        Inputs:
           emails - comma seperated list of emails
           subject - title of email
           text - email text
           html - email text in html
           role - site role (can't be administrator)
           mustApprove - verifies if user that is join must be approved by
            an administrator
           expiration - time in seconds. Default is 1 day 1440
        """
        url = self.root + "/inviteByEmail"
        params = {
            "f" : "json",
            "emails": emails,
            "subject": subject,
            "text": text,
            "html" : html,
            "role" : role,
            "mustApprove": mustApprove,
            "expiration" : expiration
        }
        return self._do_post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def invitations(self):
        """gets all the invitations to the current portal"""
        params = {"f": "json"}
        url = "%s/invitations" % self.root
        return self._do_get(url=url,
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
        url = self.root + "/usage"
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
    def IDP(self):
        """gets the IDP information for the portal/agol"""
        url = "%s/idp" % self.root
        params = {"f": "json"}
        return self._do_get(url=url,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
########################################################################
class Servers(BaseAGOLClass):
    """This resource lists the ArcGIS Server sites that have been federated
    with the portal.This resource is not applicable to ArcGIS Online; it is
    only applicable to Portal for ArcGIS.
    """
    _servers = None
    _surl = None
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _json = None
    _json_dict = None
    ########################################################################
    class Server(BaseAGOLClass):
        _surl = None
        _url = None
        _id = None
        _name = None
        _adminUrl = None
        _url = None
        _isHosted = None
        _serverKey = None
        _serverType = None
        _surl = None
        _url = None
        _securityHandler = None
        _proxy_url = None
        _proxy_port = None
        _json = None
        _json_dict = None
        """represents a single server instance registers with portal"""
        #----------------------------------------------------------------------
        def __init__(self,
                     url,
                     securityHandler,
                     proxy_url=None,
                     proxy_port=None,
                     initalize=False):
            """Constructor"""
            self._surl = url
            self._securityHandler = securityHandler
            if not securityHandler is None:
                self._referer_url = securityHandler.referer_url
            self._proxy_port = proxy_port
            self._proxy_url = proxy_url
            if initalize:
                self.__init()
        #----------------------------------------------------------------------
        def __init(self):
            """loads the property data into the class"""
            params = {
                "f" : "pjson"
            }
            json_dict = self._do_get(url=self._surl,
                                     param_dict=params,
                                     securityHandler=self._securityHandler,
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
                    print k, " - attribute not implemented in Servers.Server class."
        #----------------------------------------------------------------------
        def __str__(self):
            """returns class as string"""
            if self._json is None:
                self.__init()
            return self._json
        #----------------------------------------------------------------------
        def __iter__(self):
            """iterates through raw JSON"""
            if self._json_dict is None:
                self.__init()
            for k,v in self._json_dict.iteritems():
                yield [k,v]
        #----------------------------------------------------------------------
        @property
        def root(self):
            """returns classes URL"""
            return self._url
        #----------------------------------------------------------------------
        @property
        def id(self):
            """gets the server id"""
            if self._id is None:
                self.__init()
            return self._id
        #----------------------------------------------------------------------
        @property
        def name(self):
            """gets the server name"""
            if self._name is None:
                self.__init()
            return self._name
        #----------------------------------------------------------------------
        @property
        def adminUrl(self):
            """gets the adminURL for the server"""
            if self._adminUrl is None:
                self.__init()
            return self._adminUrl
        #----------------------------------------------------------------------
        @property
        def url(self):
            """gets the url for the server"""
            if self._url is None:
                self.__init()
            return self._url
        #----------------------------------------------------------------------
        @property
        def isHosted(self):
            """gets the isHosted value"""
            if self._isHosted is None:
                self.__init()
            return self._isHosted
        #----------------------------------------------------------------------
        @property
        def serverKey(self):
            """gets the server key"""
            if self._serverKey is None:
                self.__init()
            return self._serverKey
        #----------------------------------------------------------------------
        @property
        def serverType(self):
            """gets the server type"""
            if self._serverType is None:
                self.__init()
            return self._serverType
        #----------------------------------------------------------------------
        def unregister(self):
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
            url = self._url + "/unregister"
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
            url = self._url + "/update"
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
    def __init__(self,
                 url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initalize=False):
        """Constructor"""
        if url.lower().endswith('/servers') == False:
            url = url + "/servers"
        self._surl = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initalize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """loads the property data into the class"""
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._surl,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
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
                print k, " - attribute not implemented in Servers class."
    #----------------------------------------------------------------------
    def __str__(self):
        """returns class as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """iterates through raw JSON"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.iteritems():
            yield [k,v]
    #----------------------------------------------------------------------
    @property
    def root(self):
        """returns classes URL"""
        return self._surl
    #----------------------------------------------------------------------
    def register(self,
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
        url = self.root + "/register"
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
    @property
    def servers(self):
        """gets all the server resources"""
        self.__init()
        items = []
        for k,v in self._json_dict.iteritems():
            if k == "servers":
                for s in v:
                    if 'id' in s:
                        url = "%s/%s" % (self.root, s['id'])
                        items.append(
                            self.Server(url=url,
                                        securityHandler=self._securityHandler,
                                        proxy_url=self._proxy_url,
                                        proxy_port=self._proxy_port))
            del k,v
        return items
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
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateRole(self, roleID, name, description):
        """allows for the role name or description to be modified"""
        params = {
            "name" : name,
            "description" : description,
            "f" : "json"
        }
        url = self._url + "/%s/update"
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
