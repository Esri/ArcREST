from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseParameters
from ..common.geometry import SpatialReference, Envelope
import os
import json
########################################################################
class InvitationList(object):
    """Used for Inviting users to a site"""
    _invites = []
    _value = {}
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._invites = []
    #----------------------------------------------------------------------
    def addUser(self, username, password,
                firstname, lastname,
                email, role):
        """adds a user to the invitation list"""
        self._invites.append({
            "username":username,
            "password":password,
            "firstname":firstname,
            "lastname":lastname,
            "fullname":"%s %s" % (firstname, lastname),
            "email":email,
            "role":role
        })
    #----------------------------------------------------------------------
    def removeByIndex(self, index):
        """removes a user from the invitation list by position"""
        if index < len(self._invites) -1 and \
           index >=0:
            self._invites.remove(index)
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self._value)
    #----------------------------------------------------------------------
    def value(self):
        """returns object as dictionary"""
        return {"invitations": self._invites}
########################################################################
class AnalyzeParameters(BaseParameters):
    """
    The analyzeParameters JSON object used to analyze a CSV file are
    described below.

    Inputs:
       sourcelocale - The locale used for the geocoding service source.
       geocodeServiceUrl - The URL of the geocoding service that supports
                           batch geocoding.
                           Note: ArcGIS for Portal 10.3 supports
                           configuring multiple geocoding services. If the
                           client application requires a specific locator,
                           the URL of this service should be specified in
                           this parameter.
       sourcecountry - The two character country code associated with the
                       geocoding service, default is "world".
       sourcecountryhint - If first time analyzing, the hint is used. If
                           source country is already specified than
                           sourcecountry is used.
    """
    _sourcelocale = None
    _geocodeServiceUrl = None
    _sourcecountry = None
    _sourcecountryhint = None

    #----------------------------------------------------------------------
    def __init__(self,
                 sourcelocale="en",
                 geocodeServiceUrl=None,
                 sourcecountry="world",
                 sourcecountryhint=None):
        """Constructor"""
        self._sourcelocale = sourcelocale
        self._geocodeServiceUrl = geocodeServiceUrl
        self._sourcecountry = sourcecountry
        self._sourcecountryhint = sourcecountryhint
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns object as a dictionary"""
        val = {}
        if self.sourcelocale is not None:
            val['sourcelocale'] = self.sourcelocale
        if self.geocodeServiceUrl is not None:
            val['geocodeServiceUrl'] = self.geocodeServiceUrl
        if self.sourcecountry is not None:
            val['sourcecountry'] = self.sourcecountry
        if self.sourcecountryhint is not None:
            val['sourcecountryhint'] = self.sourcecountryhint
        return val
    #----------------------------------------------------------------------
    @property
    def sourcelocale(self):
        """gets/sets the locale for geocoding serouce source"""
        return self._sourcelocale
    #----------------------------------------------------------------------
    @sourcelocale.setter
    def sourcelocale(self, value):
        """gets/sets the locale for geocoding serouce source"""
        if self._sourcelocale != value:
            self._sourcelocale = value
    #----------------------------------------------------------------------
    @property
    def geocodeServiceUrl(self):
        """gets/sets the geocodeServiceUrl"""
        return self._geocodeServiceUrl
    #----------------------------------------------------------------------
    @geocodeServiceUrl.setter
    def geocodeServiceUrl(self, value):
        """gets/sets the geocodeServiceUrl"""
        if self._geocodeServiceUrl != value:
            self._geocodeServiceUrl = value
    #----------------------------------------------------------------------
    @property
    def sourcecountry(self):
        """gets/sets the sourcecountry"""
        return self._sourcecountry
    #----------------------------------------------------------------------
    @sourcecountry.setter
    def sourcecountry(self, value):
        """gets/sets the sourcecountry"""
        if self._sourcecountry != value:
            self._sourcecountry = value
    #----------------------------------------------------------------------
    @property
    def sourcecountryhint(self):
        """gets/sets the sourcecountryhint"""
        return self._sourcecountryhint
    #----------------------------------------------------------------------
    @sourcecountryhint.setter
    def sourcecountryhint(self, value):
        """gets/sets the sourcecountryhint"""
        if self._sourcecountryhint != value:
            self._sourcecountryhint = value
########################################################################
class CreateServiceParameters(BaseParameters):
    """
    The createParameters JSON object

    name (Required) Name of the service to be created. This name must be
                    unique. If the name already exists, the operation will
                    fail.
    serviceDescription	- Description given to the service.
    hasStaticData - Boolean value indicating whether the data changes.
    maxRecordCount - A double value indicating any constraints enforced on
                     query operations.
    supportedQueryFormats - The formats in which query results are returned
    capabilities - Specify feature service editing capabilities for Create,
                   Delete, Query, Update, and Sync.
    description	- A user-friendly description for the published dataset.
    copyrightText - Copyright information associated with the dataset.
    spatialReference - All layers added to a hosted feature service need to
                       have the same spatial reference defined for the
                       feature service. When creating a new empty service
                       without specifying its spatial reference, the
                       spatial reference of the hosted feature service is
                       set to the first layer added to that feature service
    initialExtent - The initial extent set for the service.
    allowGeometryUpdates - Boolean value indicating if updating the
                           geometry of the service is permitted.
    units - Units used by the feature service
    xssPreventionEnabled - Boolean value indicating whether cross-site
                           scripting prevention is enabled.
    xssPreventionRule - Either InputOnly | InputOutput
    xssInputRule - Either rejectInvalid | sanitizeInvalid


    """
    _name = None
    _spatialReference = None
    _serviceDescription = None
    _hasStaticData = None
    _maxRecordCount=None
    _supportedQueryFormats=None
    _capabilities=None
    _description=None
    _copyrightText=None
    _initialExtent=None
    _allowGeometryUpdates=None
    _units=None
    _xssPreventionEnabled=None
    _xssPreventionRule=None
    _xssInputRule=None
    _currentVersion = 10.3
    _enableEditorTracking = False,
    _enableOwnershipAccessControl = False,
    _allowOthersToUpdate = True,
    _allowOthersToDelete = True,
    _supportsAsync = True,
    _supportsRegisteringExistingData = True,
    _supportsSyncDirectionControl = True,
    _supportsPerLayerSync = True,
    _supportsPerReplicaSync = True,
    _supportsRollbackOnFailure = True,
    _hasVersionedData = False,
    _supportsDisconnectedEditing = False,
    _size =49152,
    _syncEnabled =True
    #----------------------------------------------------------------------
    def __init__(self,
                 name,
                 spatialReference,
                 serviceDescription="",
                 hasStaticData=False,
                 maxRecordCount=1000,
                 supportedQueryFormats="JSON",
                 capabilities="Query",
                 description="",
                 copyrightText="",
                 initialExtent=None,
                 allowGeometryUpdates=False,
                 units="esriDecimalDegrees",
                 xssPreventionEnabled=False,
                 xssPreventionRule="InputOnly",
                 xssInputRule="sanitizeInvalid",
                 currentVersion="10.3",
                 enableEditorTracking = False,
                 enableOwnershipAccessControl = False,
                 allowOthersToUpdate = True,
                 allowOthersToDelete = True,
                 supportsAsync = True,
                 supportsRegisteringExistingData = True,
                 supportsSyncDirectionControl = True,
                 supportsPerLayerSync = True,
                 supportsPerReplicaSync = True,
                 supportsRollbackOnFailure = True,
                 hasVersionedData = False,
                 supportsDisconnectedEditing = False,
                 size =49152,
                 syncEnabled =True
                 ):
        """Constructor"""


        self._name = name
        if isinstance(spatialReference, SpatialReference):
            self._spatialReference = spatialReference.value
        else:
            raise AttributeError('spatialReference must be of type geometry.SpatialReference')
        self._serviceDescription= serviceDescription
        self._hasStaticData= hasStaticData
        self._maxRecordCount=maxRecordCount
        self._supportedQueryFormats= supportedQueryFormats
        self._capabilities = capabilities
        self._description= description
        self._copyrightText= copyrightText
        if initialExtent is not None:
            if isinstance(initialExtent, Envelope):
                self._initialExtent= initialExtent.value
            else:
                raise AttributeError('initialExtent must be of type geometry.Envelope')
        self._allowGeometryUpdates=allowGeometryUpdates
        self._units=units
        self._xssPreventionEnabled=xssPreventionEnabled
        self._xssPreventionRule=xssPreventionRule
        self._xssInputRule=xssInputRule
        self._currentVersion=currentVersion
        self._enableEditorTracking = enableEditorTracking
        self._enableOwnershipAccessControl = enableOwnershipAccessControl
        self._allowOthersToUpdate = allowOthersToUpdate
        self._allowOthersToDelete = allowOthersToDelete
        self._supportsAsync = supportsAsync
        self._supportsRegisteringExistingData = supportsRegisteringExistingData
        self._supportsSyncDirectionControl = supportsSyncDirectionControl
        self._supportsPerLayerSync = supportsPerLayerSync
        self._supportsPerReplicaSync = supportsPerReplicaSync
        self._supportsRollbackOnFailure = supportsRollbackOnFailure
        self._hasVersionedData = hasVersionedData
        self._supportsDisconnectedEditing = supportsDisconnectedEditing
        self._size =size
        self._syncEnabled =syncEnabled




    #----------------------------------------------------------------------
    @property
    def value(self):
        """"""
        val = {
            "name" : self._name,
            "spatialReference" : self._spatialReference,
            'maxRecordCount' : self._maxRecordCount,
            'serviceDescription' : self._serviceDescription,
            'description' : self._description,
            'hasStaticData' : self._hasStaticData,
            'units' : self._units,
            'allowGeometryUpdates' : self._allowGeometryUpdates,
            'capabilities' : self._capabilities,
            "currentVersion" : self._currentVersion,
            "hasVersionedData" : self._hasStaticData,
            "supportsDisconnectedEditing": self._supportsDisconnectedEditing,
            "size":self._size,
            "syncEnabled":self._syncEnabled,
            "syncCapabilities":{"supportsAsync":self._supportsAsync,
                                "supportsRegisteringExistingData":self._supportsRegisteringExistingData,
                                "supportsSyncDirectionControl":self._supportsSyncDirectionControl,
                                "supportsPerLayerSync":self._supportsPerLayerSync,
                                "supportsPerReplicaSync":self._supportsPerReplicaSync,
                                "supportsRollbackOnFailure":self._supportsRollbackOnFailure},
            "editorTrackingInfo":{"enableEditorTracking":self._enableEditorTracking,
                                  "enableOwnershipAccessControl":self._enableOwnershipAccessControl,
                                  "allowOthersToUpdate":self._allowOthersToUpdate,
                                  "allowOthersToDelete":self._allowOthersToDelete},
            "tables":[],
            "_ssl":False

        }
        if self._initialExtent is not None:
            val['initialExtent'] = self._initialExtent
        if self._supportedQueryFormats is not None:
            val['supportedQueryFormats'] = self._supportedQueryFormats

        if self._xssPreventionEnabled:
            val['xssPreventionInfo'] = {}
            val['xssPreventionInfo']['xssPreventionEnabled'] = self._xssPreventionEnabled
            val['xssPreventionInfo']['xssPreventionRule'] = self._xssPreventionRule
            val['xssPreventionInfo']['xssInputRule'] = self._xssInputRule
        return val
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)
########################################################################
class PortalParameters(BaseParameters):
    """
    The following parameters represent the properties of a portal
    """
    _contacts = None
    _authorizedCrossOriginDomains = None
    _canSharePublic = None
    _subscriptionInfo = None
    _defaultExtent = None
    _supportsHostedServices = None
    _homePageFeaturedContentCount = None
    _supportsOAuth = None
    _portalName = None
    _urlKey = None
    _databaseUsage = None
    _culture = None
    _helpBase = None
    _galleryTemplatesGroupQuery = None
    _commentsEnabled = None
    _metadataEditable = None
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
    _useStandardizedQuery = None
    _canListData = None
    _rotatorPanels = None
    _description = None
    _homePageFeaturedContent = None
    _canProvisionDirectPurchase = None
    _metadataFormats = None
    _stylesGroupQuery = None
    _ipCntryCode = None
    _user = None
    _helpMap = None
    _colorSetsGroupQuery = None
    _canListApps = None
    _portalProperties = None
    _portalHostname = None
    _livingAtlasGroupQuery = None
    _symbolSetsGroupQuery = None
    _name = None
    _storageQuota = None
    _canShareBingPublic = None
    _maxTokenExpirationMinutes = None
    _layerTemplatesGroupQuery = None
    _staticImagesUrl = None
    _modified = None
    _showHomePageDescription = None
    _availableCredits = None
    _helperServices = None
    _storageUsage = None
    _templatesGroupQuery = None
    _mfaAdmins = None
    _basemapGalleryGroupQuery = None
    _region = None
    _portalMode = None
    _creditAssignments = None
    __allowed_keys = ["creditAssignments", "contacts", "canSharePublic",
                      "subscriptionInfo","defaultExtent",
                      "supportsHostedServices", "authorizedCrossOriginDomains",
                      "homePageFeaturedContentCount","supportsOAuth","portalName","urlKey",
                      "databaseUsage","culture","helpBase","galleryTemplatesGroupQuery",
                      "commentsEnabled","metadataEditable","databaseQuota","id","canSearchPublic",
                      "customBaseUrl","allSSL","featuredGroupsId","defaultBasemap","created",
                      "access","httpPort","isPortal","canSignInArcGIS","portalThumbnail",
                      "httpsPort","units","canListPreProvisionedItems","mfaEnabled",
                      "featuredGroups","thumbnail","featuredItemsGroupQuery","canSignInIDP",
                      "useStandardizedQuery","canListData","rotatorPanels","description",
                      "homePageFeaturedContent","canProvisionDirectPurchase","metadataFormats",
                      "stylesGroupQuery","ipCntryCode","user","helpMap","colorSetsGroupQuery",
                      "canListApps","portalProperties","portalHostname","livingAtlasGroupQuery",
                      "symbolSetsGroupQuery","name","storageQuota","canShareBingPublic",
                      "maxTokenExpirationMinutes","layerTemplatesGroupQuery","staticImagesUrl",
                      "modified","showHomePageDescription","availableCredits","helperServices",
                      "storageUsage","templatesGroupQuery","mfaAdmins",
                      "basemapGalleryGroupQuery","region","portalMode"]
    #----------------------------------------------------------------------
    def __init__(self, **kwargv):
        """Constructor"""
        for key, value in kwargv:
            if key in self.__allowed_keys:
                setattr(self, "_"+ key, value)
    @staticmethod
    def fromDictionary(value):
        """creates the portal properties object from a dictionary"""
        if isinstance(value, dict):
            pp = PortalParameters()
            for k,v in value.items():
                setattr(pp, "_%s" % k, v)
            return pp
        else:
            raise AttributeError("Invalid input.")
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the class as a dictionary """
        val = {}
        for k in self.__allowed_keys:
            v = getattr(self, "_" + k)
            if v is not None:
                val[k] = v
        return val
    @property
    def canSharePublic(self):
        """gets/sets the property value canSharePublic"""
        return self._canSharePublic
    #----------------------------------------------------
    @canSharePublic.setter
    def canSharePublic(self,value):
        """gets/sets the property value canSharePublic"""
        if value is not None:
            self._canSharePublic = value
    #----------------------------------------------------
    @property
    def subscriptionInfo(self):
        """gets/sets the property value subscriptionInfo"""
        return self._subscriptionInfo
    #----------------------------------------------------
    @subscriptionInfo.setter
    def subscriptionInfo(self,value):
        """gets/sets the property value subscriptionInfo"""
        if value is not None:
            self._subscriptionInfo = value
    #----------------------------------------------------
    @property
    def contacts(self):
        """gets/sets the property value contacts"""
        return self._contacts
    #----------------------------------------------------
    @contacts.setter
    def contacts(self,value):
        """gets/sets the property value contacts"""
        if value is not None:
            self._contacts = value
    #----------------------------------------------------
    @property
    def authorizedCrossOriginDomains(self):
        """gets/sets the property value authorizedCrossOriginDomains"""
        return self._contacts
    #----------------------------------------------------
    @authorizedCrossOriginDomains.setter
    def authorizedCrossOriginDomains(self,value):
        """gets/sets the property value authorizedCrossOriginDomains"""
        if value is not None:
            self._contacts = value
    #----------------------------------------------------
    @property
    def defaultExtent(self):
        """gets/sets the property value defaultExtent"""
        return self._defaultExtent
    #----------------------------------------------------
    @defaultExtent.setter
    def defaultExtent(self,value):
        """gets/sets the property value defaultExtent"""
        if value is not None:
            self._defaultExtent = value
    #----------------------------------------------------
    @property
    def supportsHostedServices(self):
        """gets/sets the property value supportsHostedServices"""
        return self._supportsHostedServices
    #----------------------------------------------------
    @supportsHostedServices.setter
    def supportsHostedServices(self,value):
        """gets/sets the property value supportsHostedServices"""
        if value is not None:
            self._supportsHostedServices = value
    #----------------------------------------------------
    @property
    def homePageFeaturedContentCount(self):
        """gets/sets the property value homePageFeaturedContentCount"""
        return self._homePageFeaturedContentCount
    #----------------------------------------------------
    @homePageFeaturedContentCount.setter
    def homePageFeaturedContentCount(self,value):
        """gets/sets the property value homePageFeaturedContentCount"""
        if value is not None:
            self._homePageFeaturedContentCount = value
    #----------------------------------------------------
    @property
    def supportsOAuth(self):
        """gets/sets the property value supportsOAuth"""
        return self._supportsOAuth
    #----------------------------------------------------
    @supportsOAuth.setter
    def supportsOAuth(self,value):
        """gets/sets the property value supportsOAuth"""
        if value is not None:
            self._supportsOAuth = value
    #----------------------------------------------------
    @property
    def portalName(self):
        """gets/sets the property value portalName"""
        return self._portalName
    #----------------------------------------------------
    @portalName.setter
    def portalName(self,value):
        """gets/sets the property value portalName"""
        if value is not None:
            self._portalName = value
    #----------------------------------------------------
    @property
    def urlKey(self):
        """gets/sets the property value urlKey"""
        return self._urlKey
    #----------------------------------------------------
    @urlKey.setter
    def urlKey(self,value):
        """gets/sets the property value urlKey"""
        if value is not None:
            self._urlKey = value
    #----------------------------------------------------
    @property
    def databaseUsage(self):
        """gets/sets the property value databaseUsage"""
        return self._databaseUsage
    #----------------------------------------------------
    @databaseUsage.setter
    def databaseUsage(self,value):
        """gets/sets the property value databaseUsage"""
        if value is not None:
            self._databaseUsage = value
    #----------------------------------------------------
    @property
    def culture(self):
        """gets/sets the property value culture"""
        return self._culture
    #----------------------------------------------------
    @culture.setter
    def culture(self,value):
        """gets/sets the property value culture"""
        if value is not None:
            self._culture = value
    #----------------------------------------------------
    @property
    def helpBase(self):
        """gets/sets the property value helpBase"""
        return self._helpBase
    #----------------------------------------------------
    @helpBase.setter
    def helpBase(self,value):
        """gets/sets the property value helpBase"""
        if value is not None:
            self._helpBase = value
    #----------------------------------------------------
    @property
    def galleryTemplatesGroupQuery(self):
        """gets/sets the property value galleryTemplatesGroupQuery"""
        return self._galleryTemplatesGroupQuery
    #----------------------------------------------------
    @galleryTemplatesGroupQuery.setter
    def galleryTemplatesGroupQuery(self,value):
        """gets/sets the property value galleryTemplatesGroupQuery"""
        if value is not None:
            self._galleryTemplatesGroupQuery = value
    #----------------------------------------------------
    @property
    def commentsEnabled(self):
        """gets/sets the property value commentsEnabled"""
        return self._commentsEnabled
    #----------------------------------------------------
    @commentsEnabled.setter
    def commentsEnabled(self,value):
        """gets/sets the property value commentsEnabled"""
        if value is not None:
            self._commentsEnabled = value
    #----------------------------------------------------
    @property
    def metadataEditable(self):
        """gets/sets the property value metadataEditable"""
        return self._metadataEditable
    #----------------------------------------------------
    @metadataEditable.setter
    def metadataEditable(self,value):
        """gets/sets the property value metadataEditable"""
        if value is not None:
            self._metadataEditable = value
    #----------------------------------------------------
    @property
    def databaseQuota(self):
        """gets/sets the property value databaseQuota"""
        return self._databaseQuota
    #----------------------------------------------------
    @databaseQuota.setter
    def databaseQuota(self,value):
        """gets/sets the property value databaseQuota"""
        if value is not None:
            self._databaseQuota = value
    #----------------------------------------------------
    @property
    def id(self):
        """gets/sets the property value id"""
        return self._id
    #----------------------------------------------------
    @id.setter
    def id(self,value):
        """gets/sets the property value id"""
        if value is not None:
            self._id = value
    #----------------------------------------------------
    @property
    def canSearchPublic(self):
        """gets/sets the property value canSearchPublic"""
        return self._canSearchPublic
    #----------------------------------------------------
    @canSearchPublic.setter
    def canSearchPublic(self,value):
        """gets/sets the property value canSearchPublic"""
        if value is not None:
            self._canSearchPublic = value
    #----------------------------------------------------
    @property
    def customBaseUrl(self):
        """gets/sets the property value customBaseUrl"""
        return self._customBaseUrl
    #----------------------------------------------------
    @customBaseUrl.setter
    def customBaseUrl(self,value):
        """gets/sets the property value customBaseUrl"""
        if value is not None:
            self._customBaseUrl = value
    #----------------------------------------------------
    @property
    def allSSL(self):
        """gets/sets the property value allSSL"""
        return self._allSSL
    #----------------------------------------------------
    @allSSL.setter
    def allSSL(self,value):
        """gets/sets the property value allSSL"""
        if value is not None:
            self._allSSL = value
    #----------------------------------------------------
    @property
    def featuredGroupsId(self):
        """gets/sets the property value featuredGroupsId"""
        return self._featuredGroupsId
    #----------------------------------------------------
    @featuredGroupsId.setter
    def featuredGroupsId(self,value):
        """gets/sets the property value featuredGroupsId"""
        if value is not None:
            self._featuredGroupsId = value
    #----------------------------------------------------
    @property
    def defaultBasemap(self):
        """gets/sets the property value defaultBasemap"""
        return self._defaultBasemap
    #----------------------------------------------------
    @defaultBasemap.setter
    def defaultBasemap(self,value):
        """gets/sets the property value defaultBasemap"""
        if value is not None:
            self._defaultBasemap = value
    #----------------------------------------------------
    @property
    def created(self):
        """gets/sets the property value created"""
        return self._created
    #----------------------------------------------------
    @created.setter
    def created(self,value):
        """gets/sets the property value created"""
        if value is not None:
            self._created = value
    #----------------------------------------------------
    @property
    def access(self):
        """gets/sets the property value access"""
        return self._access
    #----------------------------------------------------
    @access.setter
    def access(self,value):
        """gets/sets the property value access"""
        if value is not None:
            self._access = value
    #----------------------------------------------------
    @property
    def httpPort(self):
        """gets/sets the property value httpPort"""
        return self._httpPort
    #----------------------------------------------------
    @httpPort.setter
    def httpPort(self,value):
        """gets/sets the property value httpPort"""
        if value is not None:
            self._httpPort = value
    #----------------------------------------------------
    @property
    def isPortal(self):
        """gets/sets the property value isPortal"""
        return self._isPortal
    #----------------------------------------------------
    @isPortal.setter
    def isPortal(self,value):
        """gets/sets the property value isPortal"""
        if value is not None:
            self._isPortal = value
    #----------------------------------------------------
    @property
    def canSignInArcGIS(self):
        """gets/sets the property value canSignInArcGIS"""
        return self._canSignInArcGIS
    #----------------------------------------------------
    @canSignInArcGIS.setter
    def canSignInArcGIS(self,value):
        """gets/sets the property value canSignInArcGIS"""
        if value is not None:
            self._canSignInArcGIS = value
    #----------------------------------------------------
    @property
    def portalThumbnail(self):
        """gets/sets the property value portalThumbnail"""
        return self._portalThumbnail
    #----------------------------------------------------
    @portalThumbnail.setter
    def portalThumbnail(self,value):
        """gets/sets the property value portalThumbnail"""
        if value is not None:
            self._portalThumbnail = value
    #----------------------------------------------------
    @property
    def httpsPort(self):
        """gets/sets the property value httpsPort"""
        return self._httpsPort
    #----------------------------------------------------
    @httpsPort.setter
    def httpsPort(self,value):
        """gets/sets the property value httpsPort"""
        if value is not None:
            self._httpsPort = value
    #----------------------------------------------------
    @property
    def units(self):
        """gets/sets the property value units"""
        return self._units
    #----------------------------------------------------
    @units.setter
    def units(self,value):
        """gets/sets the property value units"""
        if value is not None:
            self._units = value
    #----------------------------------------------------
    @property
    def canListPreProvisionedItems(self):
        """gets/sets the property value canListPreProvisionedItems"""
        return self._canListPreProvisionedItems
    #----------------------------------------------------
    @canListPreProvisionedItems.setter
    def canListPreProvisionedItems(self,value):
        """gets/sets the property value canListPreProvisionedItems"""
        if value is not None:
            self._canListPreProvisionedItems = value
    #----------------------------------------------------
    @property
    def mfaEnabled(self):
        """gets/sets the property value mfaEnabled"""
        return self._mfaEnabled
    #----------------------------------------------------
    @mfaEnabled.setter
    def mfaEnabled(self,value):
        """gets/sets the property value mfaEnabled"""
        if value is not None:
            self._mfaEnabled = value
    #----------------------------------------------------
    @property
    def featuredGroups(self):
        """gets/sets the property value featuredGroups"""
        return self._featuredGroups
    #----------------------------------------------------
    @featuredGroups.setter
    def featuredGroups(self,value):
        """gets/sets the property value featuredGroups"""
        if value is not None:
            self._featuredGroups = value
    #----------------------------------------------------
    @property
    def thumbnail(self):
        """gets/sets the property value thumbnail"""
        return self._thumbnail
    #----------------------------------------------------
    @thumbnail.setter
    def thumbnail(self,value):
        """gets/sets the property value thumbnail"""
        if value is not None:
            self._thumbnail = value
    #----------------------------------------------------
    @property
    def featuredItemsGroupQuery(self):
        """gets/sets the property value featuredItemsGroupQuery"""
        return self._featuredItemsGroupQuery
    #----------------------------------------------------
    @featuredItemsGroupQuery.setter
    def featuredItemsGroupQuery(self,value):
        """gets/sets the property value featuredItemsGroupQuery"""
        if value is not None:
            self._featuredItemsGroupQuery = value
    #----------------------------------------------------
    @property
    def canSignInIDP(self):
        """gets/sets the property value canSignInIDP"""
        return self._canSignInIDP
    #----------------------------------------------------
    @canSignInIDP.setter
    def canSignInIDP(self,value):
        """gets/sets the property value canSignInIDP"""
        if value is not None:
            self._canSignInIDP = value
    #----------------------------------------------------
    @property
    def useStandardizedQuery(self):
        """gets/sets the property value useStandardizedQuery"""
        return self._useStandardizedQuery
    #----------------------------------------------------
    @useStandardizedQuery.setter
    def useStandardizedQuery(self,value):
        """gets/sets the property value useStandardizedQuery"""
        if value is not None:
            self._useStandardizedQuery = value
    #----------------------------------------------------
    @property
    def canListData(self):
        """gets/sets the property value canListData"""
        return self._canListData
    #----------------------------------------------------
    @canListData.setter
    def canListData(self,value):
        """gets/sets the property value canListData"""
        if value is not None:
            self._canListData = value
    #----------------------------------------------------
    @property
    def rotatorPanels(self):
        """gets/sets the property value rotatorPanels"""
        return self._rotatorPanels
    #----------------------------------------------------
    @rotatorPanels.setter
    def rotatorPanels(self,value):
        """gets/sets the property value rotatorPanels"""
        if value is not None:
            self._rotatorPanels = value
    #----------------------------------------------------
    @property
    def description(self):
        """gets/sets the property value description"""
        return self._description
    #----------------------------------------------------
    @description.setter
    def description(self,value):
        """gets/sets the property value description"""
        if value is not None:
            self._description = value
    #----------------------------------------------------
    @property
    def homePageFeaturedContent(self):
        """gets/sets the property value homePageFeaturedContent"""
        return self._homePageFeaturedContent
    #----------------------------------------------------
    @homePageFeaturedContent.setter
    def homePageFeaturedContent(self,value):
        """gets/sets the property value homePageFeaturedContent"""
        if value is not None:
            self._homePageFeaturedContent = value
    #----------------------------------------------------
    @property
    def canProvisionDirectPurchase(self):
        """gets/sets the property value canProvisionDirectPurchase"""
        return self._canProvisionDirectPurchase
    #----------------------------------------------------
    @canProvisionDirectPurchase.setter
    def canProvisionDirectPurchase(self,value):
        """gets/sets the property value canProvisionDirectPurchase"""
        if value is not None:
            self._canProvisionDirectPurchase = value
    #----------------------------------------------------
    @property
    def metadataFormats(self):
        """gets/sets the property value metadataFormats"""
        return self._metadataFormats
    #----------------------------------------------------
    @metadataFormats.setter
    def metadataFormats(self,value):
        """gets/sets the property value metadataFormats"""
        if value is not None:
            self._metadataFormats = value
    #----------------------------------------------------
    @property
    def stylesGroupQuery(self):
        """gets/sets the property value stylesGroupQuery"""
        return self._stylesGroupQuery
    #----------------------------------------------------
    @stylesGroupQuery.setter
    def stylesGroupQuery(self,value):
        """gets/sets the property value stylesGroupQuery"""
        if value is not None:
            self._stylesGroupQuery = value
    #----------------------------------------------------
    @property
    def ipCntryCode(self):
        """gets/sets the property value ipCntryCode"""
        return self._ipCntryCode
    #----------------------------------------------------
    @ipCntryCode.setter
    def ipCntryCode(self,value):
        """gets/sets the property value ipCntryCode"""
        if value is not None:
            self._ipCntryCode = value
    #----------------------------------------------------
    @property
    def user(self):
        """gets/sets the property value user"""
        return self._user
    #----------------------------------------------------
    @user.setter
    def user(self,value):
        """gets/sets the property value user"""
        if value is not None:
            self._user = value
    #----------------------------------------------------
    @property
    def helpMap(self):
        """gets/sets the property value helpMap"""
        return self._helpMap
    #----------------------------------------------------
    @helpMap.setter
    def helpMap(self,value):
        """gets/sets the property value helpMap"""
        if value is not None:
            self._helpMap = value
    #----------------------------------------------------
    @property
    def colorSetsGroupQuery(self):
        """gets/sets the property value colorSetsGroupQuery"""
        return self._colorSetsGroupQuery
    #----------------------------------------------------
    @colorSetsGroupQuery.setter
    def colorSetsGroupQuery(self,value):
        """gets/sets the property value colorSetsGroupQuery"""
        if value is not None:
            self._colorSetsGroupQuery = value
    #----------------------------------------------------
    @property
    def canListApps(self):
        """gets/sets the property value canListApps"""
        return self._canListApps
    #----------------------------------------------------
    @canListApps.setter
    def canListApps(self,value):
        """gets/sets the property value canListApps"""
        if value is not None:
            self._canListApps = value
    #----------------------------------------------------
    @property
    def portalProperties(self):
        """gets/sets the property value portalProperties"""
        return self._portalProperties
    #----------------------------------------------------
    @portalProperties.setter
    def portalProperties(self,value):
        """gets/sets the property value portalProperties"""
        if value is not None:
            self._portalProperties = value
    #----------------------------------------------------
    @property
    def portalHostname(self):
        """gets/sets the property value portalHostname"""
        return self._portalHostname
    #----------------------------------------------------
    @portalHostname.setter
    def portalHostname(self,value):
        """gets/sets the property value portalHostname"""
        if value is not None:
            self._portalHostname = value
    #----------------------------------------------------
    @property
    def livingAtlasGroupQuery(self):
        """gets/sets the property value livingAtlasGroupQuery"""
        return self._livingAtlasGroupQuery
    #----------------------------------------------------
    @livingAtlasGroupQuery.setter
    def livingAtlasGroupQuery(self,value):
        """gets/sets the property value livingAtlasGroupQuery"""
        if value is not None:
            self._livingAtlasGroupQuery = value
    #----------------------------------------------------
    @property
    def symbolSetsGroupQuery(self):
        """gets/sets the property value symbolSetsGroupQuery"""
        return self._symbolSetsGroupQuery
    #----------------------------------------------------
    @symbolSetsGroupQuery.setter
    def symbolSetsGroupQuery(self,value):
        """gets/sets the property value symbolSetsGroupQuery"""
        if value is not None:
            self._symbolSetsGroupQuery = value
    #----------------------------------------------------
    @property
    def name(self):
        """gets/sets the property value name"""
        return self._name
    #----------------------------------------------------
    @name.setter
    def name(self,value):
        """gets/sets the property value name"""
        if value is not None:
            self._name = value
    #----------------------------------------------------
    @property
    def storageQuota(self):
        """gets/sets the property value storageQuota"""
        return self._storageQuota
    #----------------------------------------------------
    @storageQuota.setter
    def storageQuota(self,value):
        """gets/sets the property value storageQuota"""
        if value is not None:
            self._storageQuota = value
    #----------------------------------------------------
    @property
    def canShareBingPublic(self):
        """gets/sets the property value canShareBingPublic"""
        return self._canShareBingPublic
    #----------------------------------------------------
    @canShareBingPublic.setter
    def canShareBingPublic(self,value):
        """gets/sets the property value canShareBingPublic"""
        if value is not None:
            self._canShareBingPublic = value
    #----------------------------------------------------
    @property
    def maxTokenExpirationMinutes(self):
        """gets/sets the property value maxTokenExpirationMinutes"""
        return self._maxTokenExpirationMinutes
    #----------------------------------------------------
    @maxTokenExpirationMinutes.setter
    def maxTokenExpirationMinutes(self,value):
        """gets/sets the property value maxTokenExpirationMinutes"""
        if value is not None:
            self._maxTokenExpirationMinutes = value
    #----------------------------------------------------
    @property
    def layerTemplatesGroupQuery(self):
        """gets/sets the property value layerTemplatesGroupQuery"""
        return self._layerTemplatesGroupQuery
    #----------------------------------------------------
    @layerTemplatesGroupQuery.setter
    def layerTemplatesGroupQuery(self,value):
        """gets/sets the property value layerTemplatesGroupQuery"""
        if value is not None:
            self._layerTemplatesGroupQuery = value
    #----------------------------------------------------
    @property
    def staticImagesUrl(self):
        """gets/sets the property value staticImagesUrl"""
        return self._staticImagesUrl
    #----------------------------------------------------
    @staticImagesUrl.setter
    def staticImagesUrl(self,value):
        """gets/sets the property value staticImagesUrl"""
        if value is not None:
            self._staticImagesUrl = value
    #----------------------------------------------------
    @property
    def modified(self):
        """gets/sets the property value modified"""
        return self._modified
    #----------------------------------------------------
    @modified.setter
    def modified(self,value):
        """gets/sets the property value modified"""
        if value is not None:
            self._modified = value
    #----------------------------------------------------
    @property
    def showHomePageDescription(self):
        """gets/sets the property value showHomePageDescription"""
        return self._showHomePageDescription
    #----------------------------------------------------
    @showHomePageDescription.setter
    def showHomePageDescription(self,value):
        """gets/sets the property value showHomePageDescription"""
        if value is not None:
            self._showHomePageDescription = value
    #----------------------------------------------------
    @property
    def availableCredits(self):
        """gets/sets the property value availableCredits"""
        return self._availableCredits
    #----------------------------------------------------
    @availableCredits.setter
    def availableCredits(self,value):
        """gets/sets the property value availableCredits"""
        if value is not None:
            self._availableCredits = value
    #----------------------------------------------------
    @property
    def helperServices(self):
        """gets/sets the property value helperServices"""
        return self._helperServices
    #----------------------------------------------------
    @helperServices.setter
    def helperServices(self,value):
        """gets/sets the property value helperServices"""
        if value is not None:
            self._helperServices = value
    #----------------------------------------------------
    @property
    def storageUsage(self):
        """gets/sets the property value storageUsage"""
        return self._storageUsage
    #----------------------------------------------------
    @storageUsage.setter
    def storageUsage(self,value):
        """gets/sets the property value storageUsage"""
        if value is not None:
            self._storageUsage = value
    #----------------------------------------------------
    @property
    def templatesGroupQuery(self):
        """gets/sets the property value templatesGroupQuery"""
        return self._templatesGroupQuery
    #----------------------------------------------------
    @templatesGroupQuery.setter
    def templatesGroupQuery(self,value):
        """gets/sets the property value templatesGroupQuery"""
        if value is not None:
            self._templatesGroupQuery = value
    #----------------------------------------------------
    @property
    def mfaAdmins(self):
        """gets/sets the property value mfaAdmins"""
        return self._mfaAdmins
    #----------------------------------------------------
    @mfaAdmins.setter
    def mfaAdmins(self,value):
        """gets/sets the property value mfaAdmins"""
        if value is not None:
            self._mfaAdmins = value
    #----------------------------------------------------
    @property
    def basemapGalleryGroupQuery(self):
        """gets/sets the property value basemapGalleryGroupQuery"""
        return self._basemapGalleryGroupQuery
    #----------------------------------------------------
    @basemapGalleryGroupQuery.setter
    def basemapGalleryGroupQuery(self,value):
        """gets/sets the property value basemapGalleryGroupQuery"""
        if value is not None:
            self._basemapGalleryGroupQuery = value
    #----------------------------------------------------
    @property
    def region(self):
        """gets/sets the property value region"""
        return self._region
    #----------------------------------------------------
    @region.setter
    def region(self,value):
        """gets/sets the property value region"""
        if value is not None:
            self._region = value
    #----------------------------------------------------
    @property
    def portalMode(self):
        """gets/sets the property value portalMode"""
        return self._portalMode
    #----------------------------------------------------
    @portalMode.setter
    def portalMode(self,value):
        """gets/sets the property value portalMode"""
        if value is not None:
            self._portalMode = value
    #----------------------------------------------------
    @property
    def creditAssignments(self):
        """gets/sets the property value creditAssignments"""
        return self._creditAssignments
    #----------------------------------------------------
    @creditAssignments.setter
    def creditAssignments(self,value):
        """gets/sets the property value creditAssignments"""
        if value is not None:
            self._creditAssignments = value
########################################################################
class ItemParameter(BaseParameters):
    """
    Item parameters correspond to properties of an item that are available
    to update on the Add Item and Update Item operations.

    Allowed Parameters:
       title - The title of the item. This is the only name that users and
               applications use for the item. There is no concept of
               display names or aliases in the ArcGIS Portal API.
       thumbnail - Enter the pathname to the thumbnail image to be used for
                   the item. The recommended image size is 200 pixels wide
                   by 133 pixels high. Acceptable image formats are PNG,
                   GIF, and JPEG. The maximum file size for an image is 1
                   MB. This is not a reference to the file but the file
                   itself, which will be stored on the sharing servers.
       thumbnailurl - Enter the URL to the thumbnail image to be used for
                      the item. The recommended image size is 200 pixels
                      wide by 133 pixels high. Acceptable image formats are
                      PNG, GIF, and JPEG. The maximum file size for an
                      image is 1 MB.
       metadata - The file that stores the metadata information on an item.
                  It's stored in the metadata folder under esriinfo, e.g.,
                  /sharing/content/items/<itemid>/info/metadata/metadata.xml.
       type - The type of the item. Must be drawn from the list of
              supported types. See Items and item types for a list of the
              supported types.
       typeKeywords - Type keywords describe the type and should logically
                      apply to all items of that type. See Items and item
                      types for a list of the different predefined type
                      keywords that will be automatically added based on
                      the supplied type. Use this parameter only if you
                      want to add additional type keywords. typeKeywords
                      can be applied to any type of item, in addition to
                      hosted feature services.
       description - An item description can be of any length.
       tags - Tags are words or short phrases that describe the specific
              item. Separate with commas.
       snippet - Snippet or summary for the item. Limit this brief
                 descriptive text to 250 characters.
       extent - boudning box as Syntax: extent=<xmin>, <ymin>, <xmax>, <ymax>
       spatialReference - coordinate system of the item
       accessInformation - credits the source of the item
       licenseInfo - includes any license information or restrictions
       culture -The item locale (language and country) information.
       serviceUsername - Set the username on a secure on-premise ArcGIS
                         Server service. It is valid on Map Services,
                         Feature Services and Image Services only.
       servicePassword - Set the password on a secure on-premise ArcGIS
                         Server service. It is valid on Map Services,
                         Feature Services, and Image Services only.
       fileName - name of the file updating (optional)
       archiveSelect - type of archive. Values: filegeodatabase
    """
    _archiveSelect = None
    _title = None
    _thumbnail = None
    _thumbnailurl = None
    _metadata = None
    _type = None
    _typeKeywords = None
    _description = None
    _tags = None
    _snippet = None
    _overwrite = False
    _extent = None
    _spatialReference = None
    _accessInformation = None
    _licenseInfo = None
    _culture = None
    _serviceUsername = None
    _servicePassword = None
    _filename = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the class as a dictionary """
        r = {}
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for a in attributes:
            if a != "value":
                val = getattr(self, a)
                if val is not None:
                    r[a] = val
        return r
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def title(self):
        """gets/set the title"""
        return self._title
    #----------------------------------------------------------------------
    @title.setter
    def title(self, value):
        """ gets/sets the title """
        if self._title != value:
            self._title = value
    #----------------------------------------------------------------------
    @property
    def thumbnail(self):
        """
        gets/sets the thumbnail
        Enter the pathname to the thumbnail image to be used for the item.
        The recommended image size is 200 pixels wide by 133 pixels high.
        Acceptable image formats are PNG, GIF, and JPEG. The maximum file
        size for an image is 1 MB. This is not a reference to the file but
        the file itself, which will be stored on the sharing servers.
        """
        return self._thumbnail
    #----------------------------------------------------------------------
    @thumbnail.setter
    def thumbnail(self, value):
        """
        gets/sets the thumbnail
        Enter the pathname to the thumbnail image to be used for the item.
        The recommended image size is 200 pixels wide by 133 pixels high.
        Acceptable image formats are PNG, GIF, and JPEG. The maximum file
        size for an image is 1 MB. This is not a reference to the file but
        the file itself, which will be stored on the sharing servers.
        """
        if os.path.isfile(value) and \
           self._thumbnail != value:
            self._thumbnail = value
        elif value is None:
            self._thumbnail = None
    #----------------------------------------------------------------------
    @property
    def thumbnailurl(self):
        """
        gets/sets the thumbnail url
        Enter the URL to the thumbnail image to be used for the item. The
        recommended image size is 200 pixels wide by 133 pixels high.
        Acceptable image formats are PNG, GIF, and JPEG. The maximum file
        size for an image is 1 MB
        """
        return self._thumbnailurl
    #----------------------------------------------------------------------
    @thumbnailurl.setter
    def thumbnailurl(self, value):
        """
        gets/sets the thumbnail url
        Enter the URL to the thumbnail image to be used for the item. The
        recommended image size is 200 pixels wide by 133 pixels high.
        Acceptable image formats are PNG, GIF, and JPEG. The maximum file
        size for an image is 1 MB
        """
        if self._thumbnailurl != value:
            self._thumbnailurl = value
    #----------------------------------------------------------------------
    @property
    def metadata(self):
        """
        gets/sets the metadata file
        The file that stores the metadata information on an item. It's
        stored in the metadata folder under esriinfo, e.g.,
        /sharing/content/items/<itemid>/info/metadata/metadata.xml
        """
        return self._metadata
    #----------------------------------------------------------------------
    @metadata.setter
    def metadata(self, value):
        """
        gets/sets the metadata file
        The file that stores the metadata information on an item. It's
        stored in the metadata folder under esriinfo, e.g.,
        /sharing/content/items/<itemid>/info/metadata/metadata.xml
        """
        if self._metadata != value:
            self._metadata = value
    #----------------------------------------------------------------------
    @property
    def type(self):
        """
        gets/sets the type
        The type of the item. Must be drawn from the list of supported types.
        """
        return self._type
    #----------------------------------------------------------------------
    @type.setter
    def type(self, value):
        """
        gets/sets the type
        The type of the item. Must be drawn from the list of supported types.
        """
        if self._type != value:
            self._type = value
    #----------------------------------------------------------------------
    @property
    def typeKeywords(self):
        """
        gets/sets the typeKeywords
        Type keywords describe the type and should logically apply to all
        items of that type. See Items and item types for a list of the
        different predefined type keywords that will be automatically added
        based on the supplied type. Use this parameter only if you want to
        add additional type keywords. typeKeywords can be applied to any
        type of item, in addition to hosted feature services.
        """
        return self._typeKeywords
    #----------------------------------------------------------------------
    @typeKeywords.setter
    def typeKeywords(self, value):
        """
        gets/sets the typeKeywords
        Type keywords describe the type and should logically apply to all
        items of that type. See Items and item types for a list of the
        different predefined type keywords that will be automatically added
        based on the supplied type. Use this parameter only if you want to
        add additional type keywords. typeKeywords can be applied to any
        type of item, in addition to hosted feature services.
        """
        if self._typeKeywords != value:
            self._typeKeywords = value
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets/sets an item description of any length"""
        return self._description
    #----------------------------------------------------------------------
    @description.setter
    def description(self, value):
        """gets/sets an item description of any length"""
        if self._description != value:
            self._description = value
    @property
    def archiveSelect(self):
        """ gets/sets an item archiveSelect value"""
        return self._archiveSelect
    #----------------------------------------------------------------------
    @archiveSelect.setter
    def archiveSelect(self, value):
        """gets/sets an item description of any length"""
        if self._archiveSelect != value:
            self._archiveSelect = value
    #----------------------------------------------------------------------
    @property
    def tags(self):
        """gets/sets the tags that describe the item"""
        return self._tags
    #----------------------------------------------------------------------
    @tags.setter
    def tags(self, value):
        """gets/sets the tags that describe the item"""
        if self._tags != value:
            self._tags = value
    #----------------------------------------------------------------------
    @property
    def snippet(self):
        """
        Snippet or summary for the item. Limit this brief descriptive text
        to 250 characters.
        """
        return self._snippet
    #----------------------------------------------------------------------
    @snippet.setter
    def snippet(self, value):
        """
        Snippet or summary for the item. Limit this brief descriptive text
        to 250 characters.
        """
        if self._snippet != value:
            self._snippet = value
    #----------------------------------------------------------------------
    @property
    def overwrite(self):
        """
        overwrites an existing item.
        """
        return self._overwrite
    #----------------------------------------------------------------------
    @overwrite.setter
    def overwrite(self, value):
        """
        overwrites an existing item (depricated)
        """
        if self._overwrite != value:
            self._overwrite = value
    #----------------------------------------------------------------------
    @property
    def extent(self):
        """gets/sets the bounding rectangle of the item"""
        return self._extent
    #----------------------------------------------------------------------
    @extent.setter
    def extent(self, value):
        """gets/sets the bounding rectangle of the item"""
        if self._extent != value:
            self._extent = value
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """gets/sets the coordinate system of the item """
        return self._spatialReference
    #----------------------------------------------------------------------
    @spatialReference.setter
    def spatialReference(self, value):
        """gets/sets the coordinate system of the item """
        if self._spatialReference != value:
            self._spatialReference = value
    #----------------------------------------------------------------------
    @property
    def accessInformation(self):
        """gets/sets for the credits of the source of the item."""
        return self._accessInformation
    #----------------------------------------------------------------------
    @accessInformation.setter
    def accessInformation(self, value):
        """gets/sets for the credits of the source of the item."""
        if self._accessInformation != value:
            self._accessInformation = value
    #----------------------------------------------------------------------
    @property
    def licenseInfo(self):
        """gets/sets the license information or restrictions"""
        return self._licenseInfo
    #----------------------------------------------------------------------
    @licenseInfo.setter
    def licenseInfo(self, value):
        """gets/sets the license information or restrictions"""
        if self._licenseInfo != value:
            self._licenseInfo = value
    #----------------------------------------------------------------------
    @property
    def culture(self):
        """gets/sets the item locale"""
        return self._culture
    #----------------------------------------------------------------------
    @culture.setter
    def culture(self, value):
        """gets/sets the item locale"""
        if self._culture != value:
            self._culture = value
    #----------------------------------------------------------------------
    @property
    def serviceUsername(self):
        """
        gets/Set the username on a secure on-premise ArcGIS Server service.
        It is valid on Map Services, Feature Services and Image Services
        only
        """
        return self._serviceUsername
    #----------------------------------------------------------------------
    @serviceUsername.setter
    def serviceUsername(self, value):
        """
        gets/Set the username on a secure on-premise ArcGIS Server service.
        It is valid on Map Services, Feature Services and Image Services
        only
        """
        if self._serviceUsername != value:
            self._serviceUsername = value
    #----------------------------------------------------------------------
    @property
    def servicePassword(self):
        """
        gets/sets - Set the password on a secure on-premise ArcGIS Server
        service. It is valid on Map Services, Feature Services, and Image
        Services only.
        """
        return self._servicePassword
    #----------------------------------------------------------------------
    @servicePassword.setter
    def servicePassword(self, value):
        """
        gets/sets - Set the password on a secure on-premise ArcGIS Server
        service. It is valid on Map Services, Feature Services, and Image
        Services only.
        """
        if self._servicePassword != value:
            self._servicePassword = value
    #----------------------------------------------------------------------
    @property
    def filename(self):
        """gets/sets the file name"""
        return self._filename
    #----------------------------------------------------------------------
    @filename.setter
    def filename(self, value):
        """"""
        if value != self._filename:
            self._filename = value


########################################################################
class PublishCSVParameters(BaseParameters):
    """
    The publishParameters JSON object used to publish a CSV file

    name - (Required) - Name of the service to be created. The same name is
           reused as the name for the single layer within the service if
           the layerInfo parameter is not provided.

    locationType - (Required) - coordinates | address | lookup | none
                   -When locationType == coordinates, the CSV data contains
                   X,Y information.
                   -When locationType == address, the CSV data contains
                   address fields that will be geocoded to a single point.
                   -When locationType == lookup, the CSV data contains
                   fields that can be mapped to well-known sets of
                   geographies.
                   -When locationType == none, the CSV data contains no
                   spatial content and data will be loaded and subsequently
                   queried as tabular data.

                   Based on this parameter, additional parameters will be
                   required, e.g., when specifying locationType ==
                   coordinates, the latitude and longitude field names must
                   be specified.
    latitudeFieldName - (Required if locationType = coordinates) - If
                        locationType = coordinates, the name of the field
                        that contains the Y coordinate.
    longitudeFieldName - (Required if locationType = coordinates) - If
                         locationType = coordinates, the name of the field
                         that contains the X coordinate.
    addressTemplate - (Required if locationType = address) - A string value
                      that defines the address to find based on CSV field
                      values.
                      Example: "{Address} {City}, {State} {Zip}"
    lookupType - (Required if locationType == lookup) - The type of place
                 to look up. To be supported in a follow on phase.
    lookupFields (Required if locationType == lookup) - A JSON object with
                 name value pairs that define the fields used to look up
                 the location.
    layerInfo - (Required) - A JSON object that provides additional
                information about the dataset. The JSON format resembles
                the layerDescriptor used in publishing feature services to
                an on-premise spatial data server or ArcGIS Server. All
                parameters except fields are optional.
    description - A user-friendly description for the published dataset.
    maxRecordCount - A double value indicating any constraints enforced on
                     query operations.
                     Default is -1 or int.MaxValue indicating no constraint.
    copyrightText - Copyright information associated with the dataset.
    columnNames - [<array of column names], overridden if layerInfo fields
                  is specified.
                  If columnNames are omitted, the field names are inferred
                  from the first line in source CSV.
    columnDelimiter - A delimiter between data fields in each row of text.
                      Default is the comma character.
    sourceSR - Spatial reference of the input coordinates.
               Default is WKID 4326.
    targetSR - Target spatial reference of the coordinates as stored in the
               database.
               Default is WKID 102100.
    """
    _name = None
    _locationType = None
    _latitudeFieldName = None
    _longitudeFieldName = None
    _addressTemplate = None
    _lookupType = None
    _lookupField = None
    _layerInfo = None
    _description = None
    _maxRecordCount = None
    _copyrightText = None
    _columnNames = None
    _columnDelimiter = None
    _sourceSR = 4326
    _targetSR = 102100
    _allowed_locationType = ["coordinates", "address", "lookup", "none"]
    __allowed_keys = ['name', "locationType", "layerInfo",
                      "latitudeFieldName", "longitudeFieldName",
                      "addressTemplate", "lookupType", "lookupFields",
                      "description", "maxRecordCount", "copyrightText",
                      "columnNames", "columnDelimiter", "sourceSR",
                      "targetSR"]
    #----------------------------------------------------------------------
    def __init__(self,
                 name,
                 locationType,
                 layerInfo,
                 latitudeFieldName=None,
                 longitudeFieldName=None,
                 addressTemplate=None,
                 lookupType=None,
                 lookupFields=None,
                 description="",
                 maxRecordCount=-1,
                 copyrightText="",
                 columnNames=None,
                 columnDelimiter=",",
                 sourceSR=4326,
                 targetSR=102100):
        """Constructor"""
        self._name = name
        self._layerInfo = layerInfo
        if locationType.lower() in self._allowed_locationType:
            self._locationType = locationType
        else:
            raise AttributeError("Invalid locationType %s." % locationType)
        #["coordinates", "address", "lookup", "none"]
        if locationType.lower() == "none":
            pass
        elif locationType.lower() == "address":
            if addressTemplate is None:
                raise AttributeError("addressTemplate must be provide for this location type")
        elif locationType.lower() == "coordinates":
            if latitudeFieldName is None or \
               longitudeFieldName is None:
                raise AttributeError("Latitude and Longitude fields must be provided with this location type.")
        elif locationType.lower() == "lookup":
            if lookupFields is None or \
               lookupType is None:
                raise AttributeError("lookupFields and lookupType must be provide with this location type.")
        self._latitudeFieldName = latitudeFieldName
        self._longitudeFieldName = longitudeFieldName
        self._addressTemplate = addressTemplate
        self._lookupType = lookupType
        self._lookupFields = lookupFields
        self._description = description
        self._maxRecordCount = maxRecordCount
        self._copyrightText = copyrightText
        self._columnNames = columnNames
        self._columnDelimiter = columnDelimiter
        self._sourceSR = sourceSR
        self._targetSR = targetSR
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the values as a dictionary"""
        val = {}
        for k in self.__allowed_keys:
            value = getattr(self, "_" + k)
            if value is not None:
                val[k] = value
        return val
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def name(self):
        """
        gets/sets the name property
        """
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """ gets/sets the name property """
        if self._name != value and value is not None:
            self._name = value
    #----------------------------------------------------------------------
    @property
    def locationType(self):
        """
        gets/sets the location type
        """
        return self._locationType
    #----------------------------------------------------------------------
    @locationType.setter
    def locationType(self, value):
        """
        gets/sets the location type
        """
        if value.lower() in self._allowed_locationType and \
           self._locationType.lower() != value.lower():
            self._locationType = value.lower()
    #----------------------------------------------------------------------
    @property
    def latitudeFieldName(self):
        """ gets/sets the latitude field name """
        return self._latitudeFieldName
    #----------------------------------------------------------------------
    @latitudeFieldName.setter
    def latitudeFieldName(self, value):
        """ gets/sets the latitude field name """
        if self._latitudeFieldName != value:
            self._latitudeFieldName = value
    #----------------------------------------------------------------------
    @property
    def longitudeFieldName(self):
        """ gets/sets the longitude field name """
        return self._longitudeFieldName
    #----------------------------------------------------------------------
    @longitudeFieldName.setter
    def longitudeFieldName(self, value):
        """ gets/sets the longitude field name """
        if self._longitudeFieldName != value:
            self._longitudeFieldName = value
    #----------------------------------------------------------------------
    @property
    def addressTemplate(self):
        """ gets/sets the address tempalte value """
        return self._addressTemplate
    #----------------------------------------------------------------------
    @addressTemplate.setter
    def addressTemplate(self, value):
        """ gets/sets the address template value """
        if self._addressTemplate != value:
            self._addressTemplate = value
    #----------------------------------------------------------------------
    @property
    def lookupField(self):
        """ gets/sets the lookup field """
        return self._lookupField
    #----------------------------------------------------------------------
    @lookupField.setter
    def lookupField(self, value):
        """ gets/sets the lookup field """
        if self._lookupField != value:
            self._lookupField = value
    #----------------------------------------------------------------------
    @property
    def layerInfo(self):
        """ gets/sets the layer info """
        return self._layerInfo
    #----------------------------------------------------------------------
    @layerInfo.setter
    def layerInfo(self, value):
        """ gets/sets the layer info """
        if self._layerInfo != value:
            self._layerInfo = value
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets/set the decription"""
        return self._description
    #----------------------------------------------------------------------
    @description.setter
    def description(self, value):
        """ gets/sets the description """
        if self._description != value:
            self._description = value
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """gets/set the max record count"""
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @maxRecordCount.setter
    def maxRecordCount(self, value):
        """gets/sets the max record count"""
        if self._maxRecordCount != value:
            self._maxRecordCount = value
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """gets/sets the copyright text"""
        return self._copyrightText
    #----------------------------------------------------------------------
    @copyrightText.setter
    def copyrightText(self, value):
        """gets/sets the copyright text"""
        if self._copyrightText != value:
            self._copyrightText = value
    #----------------------------------------------------------------------
    @property
    def columnNames(self):
        """gets/sets the columnNames"""
        return self._columnNames
    #----------------------------------------------------------------------
    @columnNames.setter
    def columnNames(self, value):
        """gets/sets the columnNames"""
        if self._columnNames != value:
            self._columnNames = value
    #----------------------------------------------------------------------
    @property
    def columnDelimiter(self):
        """gets/sets the columnDelimiter"""
        return self._columnDelimiter
    #----------------------------------------------------------------------
    @columnDelimiter.setter
    def columnDelimiter(self, value):
        """gets/sets the columnDelimiter"""
        if self._columnDelimiter != value:
            self._columnDelimiter = value
    #----------------------------------------------------------------------
    @property
    def targetSR(self):
        """gets/sets the target spatial reference"""
        return self._targetSR
    #----------------------------------------------------------------------
    @targetSR.setter
    def targetSR(self, value):
        """gets/sets the target spatial reference"""
        if self._targetSR != value:
            self._targetSR = value
    #----------------------------------------------------------------------
    @property
    def sourceSR(self):
        """gets/set the source spatialreference"""
        return self._sourceSR
    #----------------------------------------------------------------------
    @sourceSR.setter
    def sourceSR(self, value):
        """gets/sets the source spatial reference"""
        if self._sourceSR != value:
            self._sourceSR = value
########################################################################
class PublishShapefileParameter(BaseParameters):
    """
    The publishParameters JSON object used to publish shapefiles
    """
    _name = None
    _layerInfo = None
    _description = None
    _maxRecordCount = None
    _copyrightText = None
    _targetSR = None
    _hasStaticData = True
    __allowed_keys = ['name', "description",
                      "maxRecordCount", "copyrightText",
                      "layerInfo", "targetSR", "hasStaticData"]
    #----------------------------------------------------------------------
    def __init__(self,
                 name,
                 layerInfo,
                 description="",
                 maxRecordCount=-1,
                 copyrightText="",
                 targetSR=102100
                 ):
        """Constructor"""
        self._name = name
        self._layerInfo = layerInfo
        self._description = description
        self._maxRecordCount = maxRecordCount
        self._copyrightText = copyrightText
        self._targetSR = targetSR
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets/sets the name"""
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """gets/sets the name"""
        if self._name != value:
            self._name = value
    #----------------------------------------------------------------------
    @property
    def layerInfo(self):
        """gets/sets the layer info"""
        return self._layerInfo
    #----------------------------------------------------------------------
    @layerInfo.setter
    def layerInfo(self, value):
        """gets/sets the layer info"""
        if self._layerInfo != value:
            self._layerInfo = value
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets/sets the description"""
        return self._description
    #----------------------------------------------------------------------
    @description.setter
    def description(self, value):
        """gets/sets the description"""
        if self._description != value:
            self._description = value
    #----------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """gets/sets hasStaticData"""
        return self._hasStaticData
    #----------------------------------------------------------------------
    @hasStaticData.setter
    def hasStaticData(self, value):
        """gets/sets the hasStaticData"""
        if self._hasStaticData != value and \
           isinstance(value, bool):
            self._hasStaticData = value
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """gets/sets the max record count"""
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @maxRecordCount.setter
    def maxRecordCount(self, value):
        """gets/sets the max record count"""
        if self._maxRecordCount != value:
            self._maxRecordCount = value
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """gets/sets the copyrightText"""
        return self._copyrightText
    #----------------------------------------------------------------------
    @copyrightText.setter
    def copyrightText(self, value):
        """gets/sets the copyrightText"""
        if self._copyrightText != value:
            self._copyrightText = value
    #----------------------------------------------------------------------
    @property
    def targetSR(self):
        """gets/sets the targetSR"""
        return self._targetSR
    #----------------------------------------------------------------------
    @targetSR.setter
    def targetSR(self, value):
        """gets/sets the targetSR"""
        if self._targetSR != value:
            self._targetSR = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the object as a dictionary"""
        val = {}
        for k in self.__allowed_keys:
            value = getattr(self, "_" + k)
            if value is not None:
                val[k] = value
        return val
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as string"""
        return json.dumps(self.value)
########################################################################
class PublishFeatureCollectionParameter(BaseParameters):
    """
    The publishParameters JSON object used to publish feature collections
    """
    _name = None
    _layerInfo = None
    _description = None
    _maxRecordCount = None
    _copyrightText = None
    _targetSR = None
    __allowed_keys = ['name', "description",
                      "maxRecordCount", "copyrightText",
                      "layerInfo", "targetSR"]
    #----------------------------------------------------------------------
    def __init__(self,
                 name,
                 layerInfo,
                 description="",
                 maxRecordCount=-1,
                 copyrightText="",
                 targetSR=102100
                 ):
        """Constructor"""
        self._name = name
        self._layerInfo = layerInfo
        self._description = description
        self._maxRecordCount = maxRecordCount
        self._copyrightText = copyrightText
        self._targetSR = targetSR
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets/sets the name"""
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """gets/sets the name"""
        if self._name != value:
            self._name = value
    #----------------------------------------------------------------------
    @property
    def layerInfo(self):
        """gets/sets the layer info"""
        return self._layerInfo
    #----------------------------------------------------------------------
    @layerInfo.setter
    def layerInfo(self, value):
        """gets/sets the layer info"""
        if self._layerInfo != value:
            self._layerInfo = value
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets/sets the description"""
        return self._description
    #----------------------------------------------------------------------
    @description.setter
    def description(self, value):
        """gets/sets the description"""
        if self._description != value:
            self._description = value
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """gets/sets the max record count"""
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @maxRecordCount.setter
    def maxRecordCount(self, value):
        """gets/sets the max record count"""
        if self._maxRecordCount != value:
            self._maxRecordCount = value
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """gets/sets the copyrightText"""
        return self._copyrightText
    #----------------------------------------------------------------------
    @copyrightText.setter
    def copyrightText(self, value):
        """gets/sets the copyrightText"""
        if self._copyrightText != value:
            self._copyrightText = value
    #----------------------------------------------------------------------
    @property
    def targetSR(self):
        """gets/sets the targetSR"""
        return self._targetSR
    #----------------------------------------------------------------------
    @targetSR.setter
    def targetSR(self, value):
        """gets/sets the targetSR"""
        if self._targetSR != value:
            self._targetSR = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the object as a dictionary"""
        val = {}
        for k in self.__allowed_keys:
            value = getattr(self, "_" + k)
            if value is not None:
                val[k] = value
        return val
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as a string"""
        return json.dumps(self.value)
########################################################################
class GenerateParameter(BaseParameters):
    """
    The publishParameters JSON object used to create feature collections
    Mike: This may be the same as PublishFeatureCollectionParameters
    """
    _name = None
    _maxRecordCount = None
    _copyrightText = None
    _targetSR = None
    _enforceOutputJsonSizeLimit = None
    _enforceInputFileSizeLimit = None
    _generalize = None
    _maxAllowableOffset = None
    _reducePrecision = None
    _numberOfDigitsAfterDecimal = None
    _locationType = None
    __allowed_keys = ['name', "numberOfDigitsAfterDecimal",
                      "maxRecordCount", "locationType",
                      "enforceInputFileSizeLimit", "generalize",
                      "maxAllowableOffset", "reducePrecision",
                      "enforceOutputJsonSizeLimit", "targetSR"]
    #----------------------------------------------------------------------
    def __init__(self,
                 name,
                 maxRecordCount=-1,
                 targetSR={'wkid':102100},
                 enforceOutputJsonSizeLimit = True,
                 enforceInputFileSizeLimit = True,
                 generalize = None,
                 maxAllowableOffset = None,
                 reducePrecision = True,
                 numberOfDigitsAfterDecimal = 1,
                 locationType = 'none'
                 ):
        """Constructor"""
        self._name = name
        self._maxRecordCount = maxRecordCount
        self._targetSR = targetSR

        self._enforceOutputJsonSizeLimit = enforceOutputJsonSizeLimit
        self._enforceInputFileSizeLimit = enforceInputFileSizeLimit
        self._generalize = generalize
        self._maxAllowableOffset = maxAllowableOffset
        self._reducePrecision = reducePrecision
        self._numberOfDigitsAfterDecimal = numberOfDigitsAfterDecimal
        self._locationType = locationType

    #----------------------------------------------------------------------
    def generalizeDefaults(self):
        self._maxAllowableOffset = 10.58335450004355
        self._reducePrecision = True
        self._numberOfDigitsAfterDecimal = 0
    #----------------------------------------------------------------------
    @property
    def enforceOutputJsonSizeLimit(self):
        """gets/sets the enforceOutputJsonSizeLimit"""
        return self._enforceOutputJsonSizeLimit
    #----------------------------------------------------------------------
    @enforceOutputJsonSizeLimit.setter
    def enforceOutputJsonSizeLimit(self, value):
        """gets/sets the enforceOutputJsonSizeLimit"""
        if self._enforceOutputJsonSizeLimit != value:
            self._enforceOutputJsonSizeLimit = value
    #----------------------------------------------------------------------
    @property
    def locationType(self):
        """gets/sets the locationType"""
        return self._locationType
    #----------------------------------------------------------------------
    @locationType.setter
    def locationType(self, value):
        """gets/sets the enforceOutputJsonSizeLimit"""
        if self._locationType != value:
            self._locationType = value

    #----------------------------------------------------------------------
    @property
    def enforceInputFileSizeLimit(self):
        """gets/sets the enforceInputFileSizeLimit"""
        return self._enforceInputFileSizeLimit
    #----------------------------------------------------------------------
    @enforceInputFileSizeLimit.setter
    def enforceInputFileSizeLimit(self, value):
        """gets/sets the enforceInputFileSizeLimit"""
        if self._enforceInputFileSizeLimit != value:
            self._enforceInputFileSizeLimit = value
    #----------------------------------------------------------------------
    @property
    def generalize(self):
        """gets/sets the generalize"""
        return self._generalize
    #----------------------------------------------------------------------
    @generalize.setter
    def generalize(self, value):
        """gets/sets the generalize"""
        if self._generalize != value:
            self._generalize = value

    #----------------------------------------------------------------------
    @property
    def maxAllowableOffset(self):
        """gets/sets the maxAllowableOffset"""
        return self._maxAllowableOffset
    #----------------------------------------------------------------------
    @maxAllowableOffset.setter
    def maxAllowableOffset(self, value):
        """gets/sets the maxAllowableOffset"""
        if self._maxAllowableOffset != value:
            self._maxAllowableOffset = value


    #----------------------------------------------------------------------
    @property
    def reducePrecision(self):
        """gets/sets the reducePrecision"""
        return self._reducePrecision
    #----------------------------------------------------------------------
    @reducePrecision.setter
    def reducePrecision(self, value):
        """gets/sets the reducePrecision"""
        if self._reducePrecision != value:
            self._reducePrecision = value

    #----------------------------------------------------------------------
    @property
    def numberOfDigitsAfterDecimal(self):
        """gets/sets the numberOfDigitsAfterDecimal"""
        return self._numberOfDigitsAfterDecimal
    #----------------------------------------------------------------------
    @numberOfDigitsAfterDecimal.setter
    def numberOfDigitsAfterDecimal(self, value):
        """gets/sets the numberOfDigitsAfterDecimal"""
        if self._numberOfDigitsAfterDecimal != value:
            self._numberOfDigitsAfterDecimal = value
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets/sets the name"""
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """gets/sets the name"""
        if self._name != value:
            self._name = value

    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """gets/sets the max record count"""
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @maxRecordCount.setter
    def maxRecordCount(self, value):
        """gets/sets the max record count"""
        if self._maxRecordCount != value:
            self._maxRecordCount = value
    #----------------------------------------------------------------------
    @property
    def targetSR(self):
        """gets/sets the targetSR"""
        return self._targetSR
    #----------------------------------------------------------------------
    @targetSR.setter
    def targetSR(self, value):
        """gets/sets the targetSR"""
        if self._targetSR != value:
            self._targetSR = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the object as a dictionary"""
        val = {}
        for k in self.__allowed_keys:
            value = getattr(self, "_" + k)
            if value is not None:
                val[k] = value
        return val
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as a string"""
        return json.dumps(self.value)
########################################################################
class PublishGeoJSONParameter(BaseParameters):
    """Allows users to provide the required information to
    publish a geojson file.
    """
    _hasStaticData = True
    _name = None
    _maxRecordCount = 2000
    _layerInfo = {"capabilities":"Query"}
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the object as a dictionary"""
        return {
            "hasStaticData":self._hasStaticData,
            "name":self._name,
            "maxRecordCount":self._maxRecordCount,
            "layerInfo":self._layerInfo
        }
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets/sets the name"""
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """gets/sets the name"""
        self._name = value
    #----------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """gets/set the hasStaticData value"""
        return self._hasStaticData
    #----------------------------------------------------------------------
    @hasStaticData.setter
    def hasStaticData(self, value):
        """gets/sets the hasStaticData value"""
        if self._hasStaticData != value:
            self._hasStaticData = value
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """gets/sets the maxRecordCount to return to user on request"""
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @maxRecordCount.setter
    def maxRecordCount(self, value):
        """gets/sets the maxRecordCount to return to user on request"""
        if value != self._maxRecordCount:
            self._maxRecordCount = value
    #----------------------------------------------------------------------
    @property
    def layerInfo(self):
        """gets/sets the layerInfo"""
        return self._layerInfo
    #----------------------------------------------------------------------
    @layerInfo.setter
    def layerInfo(self, value):
        """gets/sets the layerInfo"""
        if self._layerInfo != value:
            self._layerInfo = value
########################################################################
class PublishFGDBParameter(BaseParameters):
    """
    The publishParameters JSON object used to publish file geodatabase
    """
    _name = None
    _layerInfo = None
    _description = None
    _maxRecordCount = None
    _copyrightText = None
    _targetSR = None
    _overwrite = False
    __allowed_keys = ['name', "description",
                      "maxRecordCount", "copyrightText",
                      "layerInfo", "targetSR", "overwrite"]
    #----------------------------------------------------------------------
    def __init__(self,
                 name,
                 layerInfo,
                 description="",
                 maxRecordCount=-1,
                 copyrightText="",
                 targetSR=102100,
                 overwrite=False
                 ):
        """Constructor"""
        self._name = name
        self._layerInfo = layerInfo
        self._description = description
        self._maxRecordCount = maxRecordCount
        self._copyrightText = copyrightText
        self._targetSR = targetSR
        self._overwrite = overwrite
    #----------------------------------------------------------------------
    @property
    def overwrite(self):
        """gets/sets the overwrite value"""

        return self._overwrite
    #----------------------------------------------------------------------
    @overwrite.setter
    def overwrite(self, value):
        """gets/sets the overwrite value"""

        if isinstance(value, bool):
            self._overwrite = value
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets/sets the name"""
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """gets/sets the name"""
        if self._name != value:
            self._name = value
    #----------------------------------------------------------------------
    @property
    def layerInfo(self):
        """gets/sets the layer info"""
        return self._layerInfo
    #----------------------------------------------------------------------
    @layerInfo.setter
    def layerInfo(self, value):
        """gets/sets the layer info"""
        if self._layerInfo != value:
            self._layerInfo = value
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets/sets the description"""
        return self._description
    #----------------------------------------------------------------------
    @description.setter
    def description(self, value):
        """gets/sets the description"""
        if self._description != value:
            self._description = value
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """gets/sets the max record count"""
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @maxRecordCount.setter
    def maxRecordCount(self, value):
        """gets/sets the max record count"""
        if self._maxRecordCount != value:
            self._maxRecordCount = value
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """gets/sets the copyrightText"""
        return self._copyrightText
    #----------------------------------------------------------------------
    @copyrightText.setter
    def copyrightText(self, value):
        """gets/sets the copyrightText"""
        if self._copyrightText != value:
            self._copyrightText = value
    #----------------------------------------------------------------------
    @property
    def targetSR(self):
        """gets/sets the targetSR"""
        return self._targetSR
    #----------------------------------------------------------------------
    @targetSR.setter
    def targetSR(self, value):
        """gets/sets the targetSR"""
        if self._targetSR != value:
            self._targetSR = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the object as a dictionary"""
        val = {}
        for k in self.__allowed_keys:
            value = getattr(self, "_" + k)
            if value is not None:
                val[k] = value
        return val
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)

########################################################################
class PublishSDParameters(BaseParameters):
    """
    Required parameters to publish SD Parameters
    """
    _tags = None
    _overwrite = False
    #----------------------------------------------------------------------
    def __init__(self, tags,overwrite=False):
        """Constructor"""
        self._tags = tags
        self._overwrite = overwrite
    #----------------------------------------------------------------------
    @property
    def tags(self):
        """gets/sets the tags value"""
        return self._tags
    #----------------------------------------------------------------------
    @tags.setter
    def tags(self, value):
        """gets/sets the tags value"""
        if self._tags != value:
            self._tags = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the parameter value """
        r = {}
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for a in attributes:
            if a != "value":
                val = getattr(self, a)
                if val is not None:
                    r[a] = val
        return r
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as string"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def overwrite(self):
        """
        overwrites an item
        """
        return self._overwrite
    #----------------------------------------------------------------------
    @overwrite.setter
    def overwrite(self, value):
        """
        overwrites an item
        """
        if self._overwrite != value:
            self._overwrite = value