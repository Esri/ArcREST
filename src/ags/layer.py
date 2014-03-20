from base import BaseAGSServer
import json
import base
########################################################################
class FeatureLayer(BaseAGSServer):
    """
       This contains information about a feature service's layer.
    """
    _currentVersion = None
    _id = None
    _name = None
    _type = None
    _description = None
    _definitionExpression = None
    _geometryType = None
    _hasZ = None
    _hasM = None
    _copyrightText = None
    _parentLayer = None
    _subLayers = None
    _minScale = None
    _maxScale = None
    _effectiveMinScale = None
    _effectiveMaxScale = None
    _defaultVisibility = None
    _extent = None
    _timeInfo = None
    _drawingInfo = None
    _hasAttachments = None
    _htmlPopupType = None
    _displayField = None
    _typeIdField = None
    _fields = None
    _types = None # sub-types
    _relationships = None
    _maxRecordCount = None
    _canModifyLayer = None
    _supportsStatistics = None
    _supportsAdvancedQueries = None
    _hasLabels = None
    _canScaleSymbols = None
    _capabilities = None
    _supportedQueryFormats =  None
    _isDataVersioned = None
    _ownershipBasedAccessControlForFeatures = None
    _useStandardizedQueries = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url=None,
                 username=None, password=None):
        """Constructor"""
        self._url = url
        self_token_url = token_url
        self._username = username
        self._password = password
        if not username is None and\
           not password is None:
            if not token_url is None:
                self._token = self.generate_token()
        self.__init()
    def __init(self):
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(self._url, params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implmented."
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the current version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def id(self):
        """ returns the id """
        if self._id is None:
            self.__init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ returns the name """
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the type """
        if self._type is None:
            self.__init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the layer's description """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def definitionExpression(self):
        """returns the definitionExpression"""
        if self._definitionExpression is None:
            self.__init()
        return self._definitionExpression
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """returns the geometry type"""
        if self._geometryType is None:
            self.__init()
        return self._geometryType
    #----------------------------------------------------------------------
    @property
    def hasZ(self):
        """ returns if it has a Z value or not """
        if self._hasZ is None:
            self.__init()
        return self._hasZ
    #----------------------------------------------------------------------
    @property
    def hasM(self):
        """ returns if it has a m value or not """
        if self._hasM is None:
            self.__init()
        return self._hasM
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """ returns the copyright text """
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def parentLayer(self):
        """ returns information about the parent """
        if self._parentLayer is None:
            self.__init()
        return self._parentLayer
    #----------------------------------------------------------------------
    @property
    def subLayers(self):
        """ returns sublayers for layer """
        if self._subLayers is None:
            self.__init()
        return self._subLayers
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ minimum scale layer will show """
        if self._minScale is None:
            self.__init()
        return self._minScale
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """ sets the max scale """
        if self._maxScale is None:
            self.__init()
        return self._maxScale
    #----------------------------------------------------------------------
    @property
    def effectiveMinScale(self):
        if self._effectiveMinScale is None:
            self.__init()
        return self._effectiveMinScale
    #----------------------------------------------------------------------
    @property
    def effectiveMaxScale(self):
        if self._effectiveMaxScale is None:
            self.__init()
        return self._effectiveMaxScale
    #----------------------------------------------------------------------
    @property
    def defaultVisibility(self):
        if self._defaultVisibility is None:
            self.__init()
        return self._defaultVisibility
    #----------------------------------------------------------------------
    @property
    def extent(self):
        if self._extent is None:
            self.__init()
        return self._extent
    #----------------------------------------------------------------------
    @property
    def timeInfo(self):
        if self._timeInfo is None:
            self.__init()
        return self._timeInfo
    @property
    def drawingInfo(self):
        if self._drawingInfo is None:
            self.__init()
        return self._drawingInfo
    @property
    def hasAttachments(self):
        if self._hasAttachments is None:
            self.__init()
        return self._hasAttachments
    @property
    def htmlPopupType(self):
        if self._htmlPopupType is None:
            self.__init()
        return self._htmlPopupType
    @property
    def displayField(self):
        if self._displayField is None:
            self.__init()
        return self._displayField
    @property
    def typeIdField(self):
        if self._typeIdField is None:
            self.__init()
        return self._typeIdField
    @property
    def fields(self):
        if self._fields is None:
            self.__init()
        return self._fields
    @property
    def types(self):
        if self._types is None:
            self.__init()
        return self._types
    @property
    def relationships(self):
        if self._relationships is None:
            self.__init()
        return self._relationships
    @property
    def maxRecordCount(self):
        if self._maxRecordCount is None:
            self.__init()
            if self._maxRecordCount is None:
                self._maxRecordCount = 1000
        return self._maxRecordCount
    @property
    def canModifyLayer(self):
        if self._canModifyLayer is None:
            self.__init()
        return self._canModifyLayer
    @property
    def supportsStatistics(self):
        if self._supportsStatistics is None:
            self.__init()
        return self._supportsStatistics
    @property
    def supportsAdvancedQueries(self):
        if self._supportsAdvancedQueries is None:
            self.__init()
        return self._supportsAdvancedQueries
    @property
    def hasLabels(self):
        if self._hasLabels is None:
            self.__init()
        return self._hasLabels
    @property
    def canScaleSymbols(self):
        if self._canScaleSymbols is None:
            self.__init()
        return self._canScaleSymbols
    @property
    def capabilities(self):
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    @property
    def supportedQueryFormats(self):
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    @property
    def isDataVersioned(self):
        if self._isDataVersioned is None:
            self.__init()
        return self._isDataVersioned
    @property
    def ownershipBasedAccessControlForFeatures(self):
        if self._ownershipBasedAccessControlForFeatures is None:
            self.__init()
        return self._ownershipBasedAccessControlForFeatures
    @property
    def useStandardizedQueries(self):
        if self._useStandardizedQueries is None:
            self.__init()
        return self._useStandardizedQueries
########################################################################
class TableLayer(FeatureLayer):
    """Table object is exactly like FeatureLayer object"""
    pass
########################################################################
class RasterLayer(FeatureLayer):
    """Raster Layer is exactly like FeatureLayer object"""
    pass
########################################################################
class DynamicMapLayer(base.DynamicData):
    """ creates a dynamic map layer object
        A dynamic map layer refers to a layer in the current map service.
        If supported, use gdbVersion to specify an alternate geodatabase
        version.
    """
    _type = "mapLayer"
    _mapLayerId = None
    _gdbVersion = ""
    #----------------------------------------------------------------------
    def __init__(self, mapLayerId, gdbVersion=""):
        """Constructor"""
        self._mapLayerId = mapLayerId
        self._gdbVersion = gdbVersion
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """converts the dynamic object to a string"""
        return json.dumps(self.asDictionary)
    @property
    def asDictionary(self):
        """ converts the object to a dictionary """
        template = {"type" : self._type,
                    "mapLayerId" : self._mapLayerId}
        if not self._gdbVersion is None and\
           self._gdbVersion != "":
            template['gdbVersion'] = self._gdbVersion
        return template
########################################################################
#TODO DYNAMICDATALAYER CLASS
#http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Layer_source_object/02r30000019v000000/
class DynamicDataLayer(base.DynamicData):
    """

    """
    _type = "dataLayer"
    _dataSource = None
    _fields = None
    #----------------------------------------------------------------------
    def __init__(self, dataSource, fields=None):
        """Constructor"""
        if isinstance(dataSource, base.DataSource):
            self._dataSource = dataSource
        else:
            raise TypeError("Invalid datasource object")
        if fields is not None and \
           type(fields) is list:
            self._fields = fields
        elif not type(fields) is list:
            raise TypeError("Invalid fields object, must be a list")
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the value as a dictionary """
        template =  {
            "type": "dataLayer",
            "dataSource": self._dataSource
        }
        if not self._fields is None:
            template['fields'] = self._fields
        return template

    #----------------------------------------------------------------------
    @property
    def dataSource(self):
        """ returns the data source object """
        return self._dataSource
    #----------------------------------------------------------------------
    @dataSource.setter
    def dataSource(self, value):
        """ sets the datasource object """
        if isinstance(value, base.DataSource):
            self._dataSource = value
        else:
            raise TypeError("value must be a DataSource object")
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """ returns the fields """
        return self._fields
    #----------------------------------------------------------------------
    @fields.setter
    def fields(self, value):
        """sets the fields variable"""
        if type(value) is list:
            self._fields = value
        else:
            raise TypeError("Input must be a list")
########################################################################
class TableDataSource(base.DataSource):
    """Table data source is a table, feature class, or raster that
       resides in a registered workspace (either a folder or geodatabase).
       In the case of a geodatabase, if versioned, use version to switch
       to an alternate geodatabase version. If version is empty or
       missing, the registered geodatabase version will be used.
    """
    _type = "table"
    _workspaceId = None
    _dataSourceName = None
    _gdbVersion = None
    _dict = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, workspaceId, dataSourceName, gdbVersion=""):
        """Constructor"""
        self._workspaceId = workspaceId
        self._dataSourceName = dataSourceName
        self._gdbVersion = gdbVersion
    #----------------------------------------------------------------------
    @property
    def datatype(self):
        """returns the type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def workspaceId(self):
        """ returns the workspace id """
        return self._workspaceId
    #----------------------------------------------------------------------
    @workspaceId.setter
    def workspaceId(self, value):
        """sets the workspace Id"""
        self._workspaceId = value
    #----------------------------------------------------------------------
    @property
    def dataSourceName(self):
        """ returns the dataSourceName """
        return self._dataSourceName
    #----------------------------------------------------------------------
    @dataSourceName.setter
    def dataSourceName(self, value):
        """sets the dataSourceName"""
        self._dataSourceName = value
    #----------------------------------------------------------------------
    @property
    def gdbVersion(self):
        """ gets the gdbVersion """
        return self._gdbVersion
    #----------------------------------------------------------------------
    @gdbVersion.setter
    def gdbVersion(self,value):
        """ sets the GDB version """
        self._gdbVersion = value
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns the data source as JSON """
        self._json = json.dumps(self.asDictionary)
        return self._json
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the data source as JSON """
        self._dict = {
            "type" : self._type,
            "workspaceId" : self._workspaceId,
            "dataSourceName": self._dataSourceName,
            "gdbVersion" : self._gdbVersion
        }
        return self._dict
########################################################################
class RasterDataSource(base.DataSource):
    """
       Raster data source is a file-based raster that resides in a
       registered raster workspace.
    """
    _type = "raster"
    _workspaceId = None
    _dataSourceName = None
    _gdbVersion = None
    _dict = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, workspaceId, dataSourceName):
        """Constructor"""
        self._workspaceId = workspaceId
        self._dataSourceName = dataSourceName
    #----------------------------------------------------------------------
    @property
    def datatype(self):
        """returns the type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def workspaceId(self):
        """ returns the workspace id """
        return self._workspaceId
    #----------------------------------------------------------------------
    @workspaceId.setter
    def workspaceId(self, value):
        """sets the workspace Id"""
        self._workspaceId = value
    #----------------------------------------------------------------------
    @property
    def dataSourceName(self):
        """ returns the dataSourceName """
        return self._dataSourceName
    #----------------------------------------------------------------------
    @dataSourceName.setter
    def dataSourceName(self, value):
        """sets the dataSourceName"""
        self._dataSourceName = value
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns the data source as JSON """
        self._json = json.dumps(self.asDictionary)
        return self._json
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the data source as JSON """
        self._dict = {
            "type" : self._type,
            "workspaceId" : self._workspaceId,
            "dataSourceName": self._dataSourceName
        }
        return self._dict
########################################################################
class QueryTableDataSource(base.DataSource):
    """"""
    _type = "queryTable"
    _workspaceId = None
    _query = None
    _oidFields = None
    _geometryType = None
    _wkid = None
    _allowedTypes = ["esriGeometryPoint", "esriGeometryMultipoint",
                     'esriGeometryPolyline', 'esriGeometryPolygon']
    _spatialReference = None
    _dict = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, workspaceId, query, oidFields, wkid, geometryType=""):
        """Constructor"""
        self._workspaceId = workspaceId
        self._query = query
        self._oidFields = oidFields
        self._wkid = wkid
        if geometryType != "" and \
           geometryType in self._allowedTypes:
            self._geometryType = geometryType
        elif geometryType != "" and \
             not geometryType in self._allowedTypes:
            raise TypeError("geometryType is invalid")
    #----------------------------------------------------------------------
    @property
    def datatype(self):
        """returns the type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def workspaceId(self):
        """ returns the workspace id """
        return self._workspaceId
    #----------------------------------------------------------------------
    @workspaceId.setter
    def workspaceId(self, value):
        """sets the workspace Id"""
        self._workspaceId = value
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """ returns the geometry type of the query table """
        return self._geometryType
    #----------------------------------------------------------------------
    @geometryType.setter
    def geometryType(self, value):
        """ sets the geometry type """
        if value in self._allowedTypes:
            self._geometryType = value
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns the data source as JSON """
        self._json = json.dumps(self.asDictionary)
        return self._json
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the data source as a dictionary """
        self._dict = {
            "type": "queryTable",
            "workspaceId": self._workspaceId,
            "query": self._query,
            "oidFields": self._oidFields,
            "spatialReference": {"wkid" : self._wkid}
        }
        if self._geometryType != "":
            self._dict["geometryType"] = self._geometryType
        return self._dict
########################################################################
class JoinTableDataSource(base.DataSource):
    """
        joinTable data source is the result of a join operation. Nested
        joins are supported. To use nested joins, set either
        leftTableSource or rightTableSource to be a joinTable.
    """
    _type = "joinTable"
    _leftTableSource = None
    _rightTableSource = None
    _leftTableKey = None
    _rightTableKey = None
    _joinType = None
    _json = None
    joinTypes = ["esriLeftOuterJoin", "esriLeftInnerJoin"]
    #----------------------------------------------------------------------
    def __init__(self, leftTableSource, rightTableSource, leftTableKey,
                 rightTableKey, joinType):
        """Constructor"""
        if joinType in self.joinTypes:
            self._type = "joinTable"
            self._leftTableSource = leftTableSource
            self._rightTableSource = rightTableSource
            self._leftTableKey = leftTableKey
            self._rightTableKey = rightTableKey
            self._joinType = joinType
        else:
            raise TypeError("joinType is invalid")
    #----------------------------------------------------------------------
    @property
    def datatype(self):
        """returns the type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns the object as JSON string """
        self._json = json.dumps(self.asDictionary)
        return self._json
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the data source as a dictionary """
        return {
            "type": "joinTable",
            "leftTableSource": self._leftTableSource,
            "rightTableSource": self._rightTableSource,
            "leftTableKey": self._leftTableKey,
            "rightTableKey": self._rightTableKey,
            "joinType": self._joinType
        }

