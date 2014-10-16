from .._abstract.abstract import BaseParameters
from ..common.geometry import SpatialReference, Envelope
import os
import json
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
    _currentVersion = 10.21
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
                 xssInputRule="sanitizeInvalid"
                 ):
        """Constructor"""
        self._name = name
        if isinstance(spatialReference, SpatialReference):
            self._spatialReference = spatialReference.value
        else:
            raise AttributeError('spatialReference must be of type geometry.SpatialReference')
        self._serviceDescription = serviceDescription
        self._hasStaticData = hasStaticData
        self._maxRecordCount=maxRecordCount
        self._supportedQueryFormats= supportedQueryFormats
        self._capabilities= capabilities
        self._description= description
        self._copyrightText= copyrightText
        if initialExtent is not None:
            if isinstance(initialExtent, Envelope):
                self._initialExtent= initialExtent.value
            else:
                raise AttributeError('spatialReference must be of type geometry.Envelope')
        self._allowGeometryUpdates = allowGeometryUpdates
        self._units = units
        self._xssPreventionEnabled =  xssPreventionEnabled
        self._xssPreventionRule = xssPreventionRule
        self._xssInputRule = xssInputRule
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
            "hasVersionedData" : False,
            "supportsDisconnectedEditing": False,
            "size":49152,
            "syncEnabled":True,
            "syncCapabilities":{"supportsAsync":True,
                                "supportsRegisteringExistingData":True,
                                "supportsSyncDirectionControl":True,
                                "supportsPerLayerSync":True,
                                "supportsPerReplicaSync":True,
                                "supportsRollbackOnFailure":True},
            "editorTrackingInfo":{"enableEditorTracking":False,
                                  "enableOwnershipAccessControl":False,
                                  "allowOthersToUpdate":True,
                                  "allowOthersToDelete":True},
            "tables":[],
            "_ssl":False

        }
        if self._initialExtent is not None:
            val['initialExtent'] = self._initialExtent.value
        if self._supportedQueryFormats is not None:
            val['supportedQueryFormats'] = self._supportedQueryFormats

        if self._xssPreventionEnabled:
            val['xssPreventionInfo'] = {}
            val['xssPreventionInfo']['xssPreventionEnabled'] = self._xssPreventionEnabled
            val['xssPreventionInfo']['xssPreventionRule'] = self._xssPreventionRule
            val['xssPreventionInfo']['xssInputRule'] = self._xssInputRule
        return json.dumps(val)
########################################################################
class PortalParameters(BaseParameters):
    """
    The following parameters represent the properties of a portal
    """
    _name = None
    _access = None
    _description = None
    _canSharePublic = None
    _canSearchPublic = None
    _thumbnail = None
    _urlKey = None
    _urlHostName = None
    _culture = None

    __allowed_keys = ['name', 'access', "description",
                      "canSharePublic", "canSearchPublic",
                      "thumbnail", "urlKey", "urlHostName",
                      "culture"]
    #----------------------------------------------------------------------
    def __init__(self, **kwargv):
        """Constructor"""
        for key, value in kwargv:
            if key in self.__allowed_keys:
                setattr(self, "_"+ key, value)

    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the class as a dictionary """
        val = {}
        for k in self.__allowed_keys:
            val = getattr(self, "_" + k)
            val[k] = val
        return val
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ The name of the organization/portal. The character limit is 250 """
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """The name of the organization/portal. The character limit is 250"""
        if self._name != value:
            self._name = value
    #----------------------------------------------------------------------
    @property
    def access(self):
        """
        Determines who can view your organization as an anonymous user.
        Setting to public allows anonymous users to access your
        organization's custom URL. Setting to private restricts access to
        only members of your organization. public is the default.
        Values: private | public
        """
        return self._access
    #----------------------------------------------------------------------
    @access.setter
    def access(self, value):
        """
        Determines who can view your organization as an anonymous user.
        Setting to public allows anonymous users to access your
        organization's custom URL. Setting to private restricts access to
        only members of your organization. public is the default.
        Values: private | public
        """
        if self._access != value:
            self._access = value
    #----------------------------------------------------------------------
    @property
    def description(self):
        """
        A description of the organization/portal and can be of any length
        """
        return self._description
    #----------------------------------------------------------------------
    @description.setter
    def description(self, value):
        """
        A description of the organization/portal and can be of any length
        """
        if self._description != value:
            self._description = value
    #----------------------------------------------------------------------
    #@property
    #def (self):
        #""""""
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
    """
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
        Snippet or summary for the item. Limit this brief descriptive text
        to 250 characters.
        """
        return self._overwrite
    #----------------------------------------------------------------------
    @snippet.setter
    def overwrite(self, value):
        """
        Snippet or summary for the item. Limit this brief descriptive text
        to 250 characters.
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
        return json.dumps(val)
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
        return json.dumps(val)
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
        return json.dumps(val)
########################################################################
class PublishSDParmaeters(BaseParameters):
    """
    Required parameters to publish SD Parameters
    """
    _tags = None
    #----------------------------------------------------------------------
    def __init__(self, tags):
        """Constructor"""
        self._tags = tags
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
        return {
            "tags" : self._tags
        }