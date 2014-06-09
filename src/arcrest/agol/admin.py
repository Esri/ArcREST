"""

.. module:: admin
   :platform: Windows
   :synopsis: Base Class from which AGOL function inherit from.

.. moduleauthor:: test


"""


import httplib
import urlparse
import os
import sys
import shutil
import json
from xml.etree import ElementTree as ET
import arcpy
import mimetypes
from arcpy import mapping
from arcpy import env
from base import BaseAGOLClass
########################################################################
class Admin(BaseAGOLClass):
    """
       The administration resource is the root node and initial entry point
       into a Spatial Data Server adminstrative interface. This resource
       represents a catalog of data sources and services published on the
       host.
       The current version and type of the server is also returned in the
       response. The value of the version is a number such that its value
       at a future release is guaranteed to be greater than its value at a
       previous release.
    """
    _token = None
    _username = None
    _password = None
    _token_url = None
    _url = None
    _currentVersion = None
    _resources = None
    _serverType = None
    _proxy_port = None
    _proxy_url = None
    #----------------------------------------------------------------------
    def __init__(self, url,
             username=None,
             password=None,
             token_url=None,
             initialize=False,
             proxy_url=None,
             proxy_port=None):
        """Constructor"""
        self._url = url
        self._token_url = token_url
        self._username = username
        self._password = password
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if not username is None and\
           not password is None:
            if not token_url is None:
                self._token = self.generate_token(tokenURL=token_url,
                                                  proxy_port=self._proxy_port,
                                                  proxy_url=self._proxy_url)[0]
            else:
                self._token = self.generate_token(proxy_port=self._proxy_port,
                                                  proxy_url=self._proxy_url)[0]
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the service """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._token
        header= {"Referer" : "www.arcgis.com"}
        json_dict = self._do_get(self._url, params,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the software's current version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def resources(self):
        """ list of all resources on the AGOL site """
        if self._resources is None:
            self.__init()
        return self._resources
    #----------------------------------------------------------------------
    @property
    def serverType(self):
        """ returns the server type """
        if self._serverType is None:
            self.__init()
        return self._serverType
    #----------------------------------------------------------------------
    @property
    def services(self):
        """ returns all the service objects in the admin service's page """
        self._services = []
        params = {
            "f" : "json",
            "token" : self._token
        }
        uURL = self._url + "/services"
        res = self._do_get(url=uURL, param_dict=params,
                           proxy_port=self._proxy_port,
                           proxy_url=self._proxy_url)

        for k, v in res.iteritems():
            if k == "services":
                for item in v:
                    self._services.append(
                        AdminFeatureService(url=uURL + "/%s.%s" % (item['adminServiceInfo']['name'],
                                                                        item['adminServiceInfo']['type']),
                                            username=self._username,
                                            password=self._password,
                                            token_url=self._token_url,
                                            proxy_url=self._proxy_url,
                                            proxy_port=self._proxy_port)
                                            )
        return self._services
########################################################################
class AdminMapService(BaseAGOLClass):
    """
       A map service offer access to map and layer content.

       The REST API administrative map service resource represents a map
       service. This resource provides basic information about the map,
       including the layers that it contains, whether the map is cached or
       not, its spatial reference, initial and full extents, etc...  The
       administrative map service resource maintains a set of operations
       that manage the state and contents of the service.
    """
    _token = None
    _username = None
    _password = None
    _token_url = None
    _url = None
    #----------------------------------------------------------------------
    def __init__(self, url,
             username=None,
             password=None,
             token_url=None,
             initialize=False,
             proxy_url=None,
             proxy_port=None):
        """Constructor"""
        self._url = url
        self._token_url = token_url
        self._username = username
        self._password = password
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if not username is None and\
           not password is None:
            if not token_url is None:
                self._token = self.generate_token(tokenURL=token_url,
                                                  proxy_port=self._proxy_port,
                                                  proxy_url=self._proxy_url)[0]
            else:
                self._token = self.generate_token(proxy_url=self._proxy_url,
                                                  proxy_port=self._proxy_port)[0]
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the service """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(self._url, params, proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
    #----------------------------------------------------------------------
    @property
    def status(self):
        """ returns the service status """
        uURL = self._url + "/status"
        params = {
            "token" : self._token,
            "f" : "json"
        }
        return self._do_get(url=uURL, param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def refresh(self):
        """ refreshes a service """
        params = {
            "f" : "json",
            "token" : self._token
        }
        uURL = self._url + "/refresh"
        return self._do_get(url=uURL, param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
########################################################################
class AdminFeatureService(BaseAGOLClass):
    """
       A feature service can contain datasets (e.g. tables, views) with and
       without a spatial column.  Datasets with a spatial column are
       considered layers and without a spatial column are considered
       tables.  A feature service allows clients to query and edit feature
       geometry and attributes.

       This resource provides basic information about the feature service
       including the feature layers and tables that it contains, the
       service description, etc.  The administrative feature service
       resource maintains a set of operations that manage the state and
       contents of the service.  Note, query and edit operations are not
       available via the adminstrative resource.
    """
    _token = None
    _username = None
    _password = None
    _token_url = None
    _url = None
    _xssPreventionInfo = None
    _size = None
    _adminServiceInfo = None
    _initialExtent = None
    _copyrightText = None
    _layers = None
    _syncCapabilities = None
    _capabilities = None
    _currentVersion = None
    _hasVersionedData = None
    _units = None
    _supportedQueryFormats = None
    _maxRecordCount = None
    _allowGeometryUpdates = None
    _description = None
    _hasStaticData = None
    _fullExtent = None
    _serviceDescription = None
    _editorTrackingInfo = None
    _supportsDisconnectedEditing = None
    _spatialReference = None
    _syncEnabled = None
    _dict = None
    #----------------------------------------------------------------------
    def __init__(self, url,
             username=None,
             password=None,
             token_url=None,
             initialize=False,
             proxy_url=None,
             proxy_port=None):
        """Constructor"""
        self._url = url
        self._token_url = token_url
        self._username = username
        self._password = password
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if not username is None and\
           not password is None:
            if not token_url is None:
                self._token = self.generate_token(tokenURL=token_url,
                                                  proxy_url=proxy_url,
                                                  proxy_port=proxy_port)[0]
            else:
                self._token = self.generate_token(proxy_url=proxy_url,
                                                  proxy_port=proxy_port)[0]
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the service """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(self._url, params,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._dict = json_dict
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k == "layers":
                self._layers = []
                for lyr in v:
                    fl = AdminFeatureServiceLayer(url=self._url + "/%s" % lyr['id'],
                                             username=self._username,
                                             password=self._password,
                                             token_url=self._token_url,
                                             proxy_port=self._proxy_port,
                                             proxy_url=self._proxy_url)
                    self._layers.append(fl)
                    del fl
                    del lyr
            elif k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented in AdminFeatureService."
    #----------------------------------------------------------------------
    @property
    def status(self):
        """ returns the service status """
        uURL = self._url + "/status"
        params = {
            "token" : self._token,
            "f" : "json"
        }
        return self._do_get(url=uURL, param_dict=params,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def refresh(self):
        """ refreshes a service """
        params = {
            "f" : "json",
            "token" : self._token
        }
        uURL = self._url + "/refresh"
        return self._do_get(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def xssPreventionInfo(self):
        """returns the xssPreventionInfo information """
        if self._xssPreventionInfo is None:
            self.__init()
        return self._xssPreventionInfo
    #----------------------------------------------------------------------
    @property
    def size(self):
        """returns the size parameter"""
        if self._size is None:
            self.__init()
        return self._size
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """returns the max record count"""
        if self._maxRecordCount is None:
            self.__init()
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @property
    def supportedQueryFormats(self):
        """"""
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """ returns a list of capabilities """
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the service description """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """ returns the copyright text """
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """ returns the spatial reference """
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """ returns the initial extent of the feature service """
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """ returns the full extent of the feature service """
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def allowGeometryUpdates(self):
        """ informs the user if the data allows geometry updates """
        if self._allowGeometryUpdates is None:
            self.__init()
        return self._allowGeometryUpdates
    #----------------------------------------------------------------------
    @property
    def units(self):
        """ returns the measurement unit """
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def syncEnabled(self):
        """ informs the user if sync of data can be performed """
        if self._syncEnabled is None:
            self.__init()
        return self._syncEnabled
    #----------------------------------------------------------------------
    @property
    def syncCapabilities(self):
        """ type of sync that can be performed """
        if self._syncCapabilities is None:
            self.__init()
        return self._syncCapabilities
    #----------------------------------------------------------------------
    @property
    def editorTrackingInfo(self):
        """"""
        if self._editorTrackingInfo is None:
            self.__init()
        return self._editorTrackingInfo
    #----------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """"""
        if self._hasStaticData is None:
            self.__init()
        return self._hasStaticData

    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the map service current version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the serviceDescription of the map service """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def hasVersionedData(self):
        """ returns boolean for versioned data """
        if self._hasVersionedData is None:
            self.__init()
        return self._hasVersionedData
    #----------------------------------------------------------------------
    @property
    def supportsDisconnectedEditing(self):
        """ returns boolean is disconnecting editted supported """
        if self._supportsDisconnectedEditing is None:
            self.__init()
        return self._supportsDisconnectedEditing
    #----------------------------------------------------------------------
    @property
    def adminServiceInfo(self):
        """ returns the admin service information"""
        if self._adminServiceInfo is None:
            self.__init()
        return self._adminServiceInfo
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """ returns the layers for a service """
        if self._layers is None:
            self.__init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the feature service as a dictionary object """
        if self._dict is None:
            self.__init()
        return self._dict
    #----------------------------------------------------------------------
    def addToDefinition(self, json_dict):
        """
           The addToDefinition operation supports adding a definition
           property to a hosted feature service. The result of this
           operation is a response indicating success or failure with error
           code and description.

           This function will allow users to change add additional values
           to an already published service.

           Input:
              json_dict - part to add to host service.  The part format can
                          be derived from the asDictionary property.  For
                          layer level modifications, run updates on each
                          individual feature service layer object.
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._token,
            "addToDefinition" : json_dict,
            "async" : False
        }
        uURL = self._url + "/addToDefinition"
        return self._do_post(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateDefinition(self, json_dict):
        """
           The updateDefinition operation supports updating a definition
           property in a hosted feature service. The result of this
           operation is a response indicating success or failure with error
           code and description.

           Input:
              json_dict - part to add to host service.  The part format can
                          be derived from the asDictionary property.  For
                          layer level modifications, run updates on each
                          individual feature service layer object.
           Output:
              JSON Message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._token,
            "updateDefinition" : json_dict,
            "async" : False
        }
        uURL = self._url + "/updateDefinition"
        return self._do_post(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def deleteFromDefinition(self, json_dict):
        """
           The deleteFromDefinition operation supports deleting a
           definition property from a hosted feature service. The result of
           this operation is a response indicating success or failure with
           error code and description.
           See: http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Delete_From_Definition_Feature_Service/02r30000021w000000/
           for additional information on this function.
           Input:
              json_dict - part to add to host service.  The part format can
                          be derived from the asDictionary property.  For
                          layer level modifications, run updates on each
                          individual feature service layer object.  Only
                          include the items you want to remove from the
                          FeatureService or layer.

           Output:
              JSON Message as dictionary

        """
        params = {
            "f" : "json",
            "token" : self._token,
            "deleteFromDefinition" : json_dict,
            "async" : False
        }
        uURL = self._url + "/deleteFromDefinition"
        return self._do_post(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
########################################################################
class AdminFeatureServiceLayer(BaseAGOLClass):
    """
       The layer resource represents a single feature layer or a non
       spatial table in a feature service.  A feature layer is a table or
       view with at least one spatial column.
       For tables, it provides basic information about the table such as
       its id, name, fields, types and templates.
       For feature layers, in addition to the table information above, it
       provides information such as its geometry type, min and max scales,
       and spatial reference.
       Each type includes information about the type such as the type id,
       name, and definition expression.  Sub-types also include a default
       symbol and a list of feature templates.
       Each feature template includes a template name, description and a
       prototypical feature.
       The property supportsRollbackOnFailures will be true to indicate the
       support for transactional edits.
       The property maxRecordCount returns the maximum number of records
       that will be returned at once for a query.
       The property capabilities returns Query, Create, Delete, Update, and
       Editing capabilities. The Editing capability will be included if
       Create, Delete or Update is enabled for a Feature Service.
       Note, query and edit operations are not available on a layer in the
       adminstrative view.
    """
    _editFieldsInfo = None
    _drawingInfo = None
    _typeIdField = None
    _advancedQueryCapabilities = None
    _supportsRollbackOnFailureParameter = None
    _globalIdField = None
    _supportsAdvancedQueries = None
    _id = None
    _relationships = None
    _capabilities = None
    _indexes = None
    _currentVersion = None
    _geometryType = None
    _hasStaticData = None
    _type = None
    _supportedQueryFormats = None
    _isDataVersioned = None
    _allowGeometryUpdates = None
    _description = None
    _defaultVisibility = None
    _extent = None
    _objectIdField = None
    _htmlPopupType = None
    _types = None
    _hasM = None
    _displayField = None
    _name = None
    _templates = None
    _supportsStatistics = None
    _hasAttachments = None
    _fields = None
    _maxScale = None
    _copyrightText = None
    _hasZ = None
    _maxRecordCount = None
    _minScale = None
    _drawingInfo = None
    _typeIdField = None
    _advancedQueryCapabilities = None
    _supportsRollbackOnFailureParameter = None
    _globalIdField = None
    _supportsAdvancedQueries = None
    _id = None
    _relationships = None
    _capabilities = None
    _indexes = None
    _currentVersion = None
    _geometryType = None
    _hasStaticData = None
    _type = None
    _supportedQueryFormats = None
    _isDataVersioned = None
    _allowGeometryUpdates = None
    _description = None
    _defaultVisibility = None
    _extent = None
    _objectIdField = None
    _htmlPopupType = None
    _types = None
    _hasM = None
    _displayField = None
    _name = None
    _templates = None
    _supportsStatistics = None
    _hasAttachments = None
    _fields = None
    _maxScale = None
    _copyrightText = None
    _hasZ = None
    _maxRecordCount = None
    _minScale = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 username=None,
                 password=None,
                 token_url=None,
                 initialize=False,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._url = url
        self._token_url = token_url
        self._username = username
        self._password = password
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if not username is None and\
           not password is None:
            if not token_url is None:
                self._token = self.generate_token(tokenURL=token_url,
                                                  proxy_port=self._proxy_port,
                                                  proxy_url=self._proxy_url)[0]
            else:
                self._token = self.generate_token(proxy_url=self._proxy_url,
                                                  proxy_port=self._proxy_port)[0]
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the service """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(self._url, params, proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented AdminFeatureServiceLayer."
    #----------------------------------------------------------------------
    def refresh(self):
        """ refreshes a service """
        params = {
            "f" : "json",
            "token" : self._token
        }
        uURL = self._url + "/refresh"
        return self._do_get(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    @property
    def editFieldsInfo(self):
        """ returns the edit fields information """
        if self._editFieldsInfo is None:
            self.__init()
        return self._editFieldsInfo
    #----------------------------------------------------------------------
    @property
    def advancedQueryCapabilities(self):
        """ returns the advanced query capabilities """
        if self._advancedQueryCapabilities is None:
            self.__init()
        return self._advancedQueryCapabilities
    #----------------------------------------------------------------------
    @property
    def supportsRollbackOnFailureParameter(self):
        """ returns if rollback on failure supported """
        if self._supportsRollbackOnFailureParameter is None:
            self.__init()
        return self._supportsRollbackOnFailureParameter
    #----------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """boolean T/F if static data is present """
        if self._hasStaticData is None:
            self.__init()
        return self._hasStaticData
    #----------------------------------------------------------------------
    @property
    def indexes(self):
        """gets the indexes"""
        if self._indexes is None:
            self.__init()
        return self._indexes
    #----------------------------------------------------------------------
    @property
    def templates(self):
        """ gets the template """
        if self._templates is None:
            self.__init()
        return self._templates
    #----------------------------------------------------------------------
    @property
    def allowGeometryUpdates(self):
        """ returns boolean if geometry updates are allowed """
        if self._allowGeometryUpdates is None:
            self.__init()
        return self._allowGeometryUpdates
    #----------------------------------------------------------------------
    @property
    def globalIdField(self):
        """ returns the global id field """
        if self._globalIdField is None:
            self.__init()
        return self._globalIdField
    #----------------------------------------------------------------------
    @property
    def objectIdField(self):
        if self._objectIdField is None:
            self.__init()
        return self._objectIdField
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
    #----------------------------------------------------------------------
    @property
    def drawingInfo(self):
        if self._drawingInfo is None:
            self.__init()
        return self._drawingInfo
    #----------------------------------------------------------------------
    @property
    def hasAttachments(self):
        if self._hasAttachments is None:
            self.__init()
        return self._hasAttachments
    #----------------------------------------------------------------------
    @property
    def htmlPopupType(self):
        if self._htmlPopupType is None:
            self.__init()
        return self._htmlPopupType
    #----------------------------------------------------------------------
    @property
    def displayField(self):
        if self._displayField is None:
            self.__init()
        return self._displayField
    #----------------------------------------------------------------------
    @property
    def typeIdField(self):
        if self._typeIdField is None:
            self.__init()
        return self._typeIdField
    #----------------------------------------------------------------------
    @property
    def fields(self):
        if self._fields is None:
            self.__init()
        return self._fields
    #----------------------------------------------------------------------
    @property
    def types(self):
        if self._types is None:
            self.__init()
        return self._types
    #----------------------------------------------------------------------
    @property
    def relationships(self):
        if self._relationships is None:
            self.__init()
        return self._relationships
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        if self._maxRecordCount is None:
            self.__init()
            if self._maxRecordCount is None:
                self._maxRecordCount = 1000
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @property
    def canModifyLayer(self):
        if self._canModifyLayer is None:
            self.__init()
        return self._canModifyLayer
    #----------------------------------------------------------------------
    @property
    def supportsStatistics(self):
        if self._supportsStatistics is None:
            self.__init()
        return self._supportsStatistics
    #----------------------------------------------------------------------
    @property
    def supportsAdvancedQueries(self):
        if self._supportsAdvancedQueries is None:
            self.__init()
        return self._supportsAdvancedQueries
    #----------------------------------------------------------------------
    @property
    def hasLabels(self):
        if self._hasLabels is None:
            self.__init()
        return self._hasLabels
    #----------------------------------------------------------------------
    @property
    def canScaleSymbols(self):
        if self._canScaleSymbols is None:
            self.__init()
        return self._canScaleSymbols
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def supportedQueryFormats(self):
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    #----------------------------------------------------------------------
    @property
    def isDataVersioned(self):
        if self._isDataVersioned is None:
            self.__init()
        return self._isDataVersioned
    #----------------------------------------------------------------------
    @property
    def ownershipBasedAccessControlForFeatures(self):
        if self._ownershipBasedAccessControlForFeatures is None:
            self.__init()
        return self._ownershipBasedAccessControlForFeatures
    #----------------------------------------------------------------------
    @property
    def useStandardizedQueries(self):
        if self._useStandardizedQueries is None:
            self.__init()
        return self._useStandardizedQueries
    #----------------------------------------------------------------------
    def addToDefinition(self, json_dict):
        """
           The addToDefinition operation supports adding a definition
           property to a hosted feature service. The result of this
           operation is a response indicating success or failure with error
           code and description.

           This function will allow users to change add additional values
           to an already published service.

           Input:
              json_dict - part to add to host service.  The part format can
                          be derived from the asDictionary property.  For
                          layer level modifications, run updates on each
                          individual feature service layer object.
           Output:
              JSON message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._token,
            "addToDefinition" : json.dumps(json_dict),
            #"async" : False
        }
        uURL = self._url + "/addToDefinition"
        return self._do_post(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateDefinition(self, json_dict):
        """
           The updateDefinition operation supports updating a definition
           property in a hosted feature service. The result of this
           operation is a response indicating success or failure with error
           code and description.

           Input:
              json_dict - part to add to host service.  The part format can
                          be derived from the asDictionary property.  For
                          layer level modifications, run updates on each
                          individual feature service layer object.
           Output:
              JSON Message as dictionary
        """
        params = {
            "f" : "json",
            "token" : self._token,
            "updateDefinition" : json.dumps(json_dict),
            "async" : False
        }
        uURL = self._url + "/updateDefinition"
        return self._do_post(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def deleteFromDefinition(self, json_dict):
        """
           The deleteFromDefinition operation supports deleting a
           definition property from a hosted feature service. The result of
           this operation is a response indicating success or failure with
           error code and description.
           See: http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Delete_From_Definition_Feature_Service/02r30000021w000000/
           for additional information on this function.
           Input:
              json_dict - part to add to host service.  The part format can
                          be derived from the asDictionary property.  For
                          layer level modifications, run updates on each
                          individual feature service layer object.  Only
                          include the items you want to remove from the
                          FeatureService or layer.

           Output:
              JSON Message as dictionary

        """
        params = {
            "f" : "json",
            "token" : self._token,
            "deleteFromDefinition" : json.dumps(json_dict),
            #"async" : False
        }
        uURL = self._url + "/deleteFromDefinition"
        return self._do_post(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
########################################################################
class AGOL(BaseAGOLClass):
    """ publishes to AGOL """
    _username = None
    _password = None
    _token = None
    _org_url ="http://www.arcgis.com"
    _url = "http://www.arcgis.com/sharing/rest"
    _token_url = ""

    def __init__(self, username, password, org_url=None,
                 rest_url=None,token_url=None,referer_url=None,
                 proxy_url=None, proxy_port=None):
        """ constructor """
        self._username = username
        self._password = password
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self.initURL(org_url, rest_url,token_url,referer_url)
        result = self.generate_token(proxy_port=proxy_port,
                                          proxy_url=proxy_url)
        if result != None:
            self._token = result[0]

    #----------------------------------------------------------------------
    @property
    def orgURL(self):
        """ returns the Portal's base org url"""
        return self._org_url
    #----------------------------------------------------------------------
    @property
    def contentRootURL(self):
        """ returns the Portal's content root """
        return self._url + "/content"
    #----------------------------------------------------------------------
    def addComment(self, item_id, comment):
        """ adds a comment to a given item.  Must be authenticated """
        url = self.contentRootURL + "/items/%s/addComment" % item_id
        params = {
            "f" : "json",
            "comment" : comment,
            "token" : self._token
        }
        return self._do_post(url, params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def addRating(self, item_id, rating=5.0):
        """Adds a rating to an item between 1.0 and 5.0"""
        if rating > 5.0:
            rating = 5.0
        elif rating < 1.0:
            rating = 1.0
        url = self.contentRootURL + "/items/%s/addRating" % item_id
        params = {
            "f": "json",
            "token" : self._token,
            "rating" : "%s" % rating
        }
        return self._do_post(url, params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def createFolder(self, folder_name):
        """ creats a folder for a user's agol account """
        url = self.contentRootURL + "/users/%s/createFolder" % self._username
        params = {
            "f" : "json",
            "token" : self._token,
            "title" : folder_name
        }
        return self._do_post(url, params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def deleteFolder(self, item_id):
        """ deletes a user's folder """
        url = self.contentRootURL + "/users/%s/%s/delete" % (self._username, item_id)
        params = {
            "f" : "json",
            "token" : self._token
        }
        return self._do_post(url, params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def item(self, item_id):
        """ returns information about an item on agol/portal """
        params = {
            "f" : "json",
            "token" : self._token
        }
        url = self.contentRootURL + "/items/%s" % item_id
        return self._do_get(url, params, proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def itemData(self, item_id):
        """ returns data for an item on agol/portal """
        params = {
            "f" : "json",
            "token" : self._token
        }
        url = self.contentRootURL + "/items/%s/data" % item_id
        return self._do_get(url, params, proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def _prep_mxd(self, mxd):
        """ ensures the requires mxd properties are set to something """
        changed = False
        if mxd.author.strip() == "":
            mxd.author = "NA"
            changed = True
        if mxd.credits.strip() == "":
            mxd.credits = "NA"
            changed = True
        if mxd.description.strip() == "":
            mxd.description = "NA"
            changed = True
        if mxd.summary.strip() == "":
            mxd.summary = "NA"
            changed = True
        if mxd.tags.strip() == "":
            mxd.tags = "NA"
            changed = True
        if mxd.title.strip() == "":
            mxd.title = "NA"
            changed = True
        if changed == True:
            mxd.save()
        return mxd
    #----------------------------------------------------------------------
    def getUserContent(self,folder=None):
        """ gets a user's content on agol """
        data = {"token": self._token,
                "f": "json"}
        url = '{}/content/users/{}'.format(self._url,self._username)

        if folder:
            url += '/' + folder
        jres = self._do_get(url=url,
                            param_dict=data,
                            header={"Accept-Encoding":""},
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
        return jres
    #----------------------------------------------------------------------
    def getUserInfo(self):
        """ gets a user's info on agol """
        data = {"token": self._token,
                "f": "json"}
        url = '{}/content/users/{}'.format(self._url,self._username)

        jres = self._do_get(url=url, param_dict=data,
                            header={"Accept-Encoding":""},
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
        return jres
    #----------------------------------------------------------------------
    def getUserCommunityInfo(self):
        """ gets a user's info on agol """
        data = {"token": self._token,
                "f": "json"}
        url = '{}/community/users/{}'.format(self._url,self._username)

        jres = self._do_get(url=url, param_dict=data,
                            header={"Accept-Encoding":""},
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
        return jres
      #----------------------------------------------------------------------
    def addFile(self, file_path, agol_type, name, tags, description,folder=None):
        """ loads a file to AGOL """
        params = {
            "f" : "json",
            "filename" : os.path.basename(file_path),
            "type" : agol_type,
            "title" : name,
            "tags" : tags,
            "description" : description
        }
        if self._token is not None:
            params['token'] = self._token

        url = "{}/content/users/{}".format(self._url,
                                                   self._username)
        if folder:
            url += '/' + folder
        url += '/addItem'
        parsed = urlparse.urlparse(url)
        files = []
        files.append(('file', file_path, os.path.basename(file_path)))

        res = self._post_multipart(host=parsed.hostname,
                                   selector=parsed.path,
                                   files = files,
                                   fields=params,
                                   port=parsed.port,
                                   ssl=parsed.scheme.lower() == 'https',
                                   proxy_port=self._proxy_port,
                                   proxy_url=self._proxy_url)
        res = self._unicode_convert(json.loads(res))
        return res
    #----------------------------------------------------------------------
    def addItem(self,  name, tags, description,snippet,data,extent,item_type='Web Map',thumbnail='',folder=None,typeKeywords = [
                    "ArcGIS Online",
                    "Collector",
                    "Data Editing",
                    "Explorer Web Map",
                    "Map",
                    "Offline",
                    "Online Map",
                    "Web Map"
                    ]
                ):
            """ loads a file to AGOL """

            params = {
                "f" : "json",
                "text" : json.dumps(data),
                "type" : item_type,
                "title" : name,
                "tags" : tags,
                "description" : description,
                "snippet" : snippet,
                "extent": extent,
                "typeKeywords":typeKeywords,
                "thumbnail": os.path.basename(thumbnail)
            }

            if self._token is not None:
                params['token'] = self._token

            url = "{}/content/users/{}".format(self._url,
                                                       self._username)
            if folder:
                url += '/' + folder
            url += '/addItem'
            parsed = urlparse.urlparse(url)

            files = []
            files.append(('thumbnail', thumbnail, os.path.basename(thumbnail)))

            res = self._post_multipart(host=parsed.hostname,
                                       selector=parsed.path,
                                       fields=params,
                                       files=files,
                                       ssl=parsed.scheme.lower() == 'https',
                                       proxy_port=self._proxy_port,
                                       proxy_url=self._proxy_url,
                                       port=parsed.port)
            res = self._unicode_convert(json.loads(res))
            return res




    #----------------------------------------------------------------------
    #def addWebmap(self,  name, tags, description,snippet,data,extent,agol_type='Web Map',thumbnail='',folder=None):
        #""" loads a file to AGOL """
        #params = {
            #"f" : "json",
            #"text" : json.dumps(data),
            #"type" : agol_type,
            #"title" : name,
            #"tags" : tags,
            #"description" : description,
            #"snippet" : snippet,
            #"extent": extent,
            #"typeKeywords": [
                #"ArcGIS Online",
                #"Collector",
                #"Data Editing",
                #"Explorer Web Map",
                #"Map",
                #"Offline",
                #"Online Map",
                #"Web Map"
            #],
            #"thumbnail": os.path.basename(thumbnail)
        #}

        #if self._token is not None:
            #params['token'] = self._token

        #url = "{}/content/users/{}".format(self._url,
                                                   #self._username)
        #if folder:
            #url += '/' + folder
        #url += '/addItem'
        #parsed = urlparse.urlparse(url)

        #files = []
        #files.append(('thumbnail', thumbnail, os.path.basename(thumbnail)))

        #res = self._post_multipart(host=parsed.hostname,
                                   #selector=parsed.path,
                                   #fields=params,
                                   #files=files,
                                   #ssl=parsed.scheme.lower() == 'https',
                                   #proxy_port=self._proxy_port,
                                   #proxy_url=self._proxy_url,
                                   #port=parsed.port)
        #res = self._unicode_convert(json.loads(res))
        #return res


    #----------------------------------------------------------------------
    def updateItem(self,  agol_id, data,folder=None):

        """ update an items details"""
        update_url = '{}/content/users/{}'.format(self._url,self._username)

        if folder:
            update_url += '/' + folder

        update_url += '/items/{}/update'.format(agol_id)

        params = {
            "f" : "json",
            "text" : json.dumps(data)

        }
        if self._token is not None:
            params['token'] = self._token

        parsed = urlparse.urlparse(update_url)

        files = []

        res = self._post_multipart(host=parsed.hostname,
                                   selector=parsed.path,
                                   fields=params,
                                   files=files,
                                   port=parsed.port,
                                   ssl=parsed.scheme.lower() == 'https',
                                   proxy_port=self._proxy_port,
                                   proxy_url=self._proxy_url)
        res = self._unicode_convert(json.loads(res))
        return self._tostr(res)



    #----------------------------------------------------------------------
    def enableProtect(self, item_id,folder=None):
        """Enables an items protection  """

        url = '{}/content/users/{}'.format(self._url, self._username )
        if folder:
            url += '/' + folder

        url += '/items/{}/protect'.format(item_id)
        query_dict = {'f': 'json',
                      'token': self._token}
        jres = self._do_post(url, query_dict, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
        return jres
    #----------------------------------------------------------------------

    def disableProtect(self, item_id,folder=None):
        """ Disables an items protection """

        url = '{}/content/users/{}'.format(self._url, self._username )
        if folder:
            url += '/' + folder

        url += '/items/{}/unprotect'.format(item_id)
        query_dict = {'f': 'json',
                      'token': self._token}
        jres = self._do_post(url, query_dict, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
        return jres

    #----------------------------------------------------------------------
    def deleteItem(self, item_id,folder=None,force_delete=False):
        """ deletes an agol item by it's ID """

        deleteURL = '{}/content/users/{}'.format(self._url, self._username )
        if folder:
            deleteURL += '/' + folder

        deleteURL += '/items/{}/delete'.format(item_id)
        query_dict = {'f': 'json',
                      'token': self._token}
        jres = self._do_post(deleteURL, query_dict, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
        if 'error' in jres:
            if force_delete:
                dis_res = self.disableProtect(item_id,folder)
                if 'success' in dis_res:
                    return self.deleteItem(item_id=item_id,folder=folder,force_delete=False)
                else:
                    return jres
        return jres
    #----------------------------------------------------------------------
    def _modify_sddraft(self, sddraft,maxRecordCount='1000'):
        """ modifies the sddraft for agol publishing """

        doc = ET.parse(sddraft)

        root_elem = doc.getroot()
        if root_elem.tag != "SVCManifest":
            raise ValueError("Root tag is incorrect. Is {} a .sddraft file?".format(sddraft))

        # The following 6 code pieces modify the SDDraft from a new MapService
        # with caching capabilities to a FeatureService with Query,Create,
        # Update,Delete,Uploads,Editing capabilities as well as the ability to set the max
        # records on the service.
        # The first two lines (commented out) are no longer necessary as the FS
        # is now being deleted and re-published, not truly overwritten as is the
        # case when publishing from Desktop.
        # The last three pieces change Map to Feature Service, disable caching
        # and set appropriate capabilities. You can customize the capabilities by
        # removing items.
        # Note you cannot disable Query from a Feature Service.

        # Change service type from map service to feature service
        for desc in doc.findall('Type'):
            if desc.text == "esriServiceDefinitionType_New":
                desc.text = 'esriServiceDefinitionType_Replacement'

        for config in doc.findall("./Configurations/SVCConfiguration/TypeName"):
            if config.text == "MapServer":
                config.text = "FeatureServer"

        #Turn off caching
        for prop in doc.findall("./Configurations/SVCConfiguration/Definition/" +
                                "ConfigurationProperties/PropertyArray/" +
                                "PropertySetProperty"):
            if prop.find("Key").text == 'isCached':
                prop.find("Value").text = "false"
            if prop.find("Key").text == 'maxRecordCount':
                prop.find("Value").text = maxRecordCount

        for prop in doc.findall("./Configurations/SVCConfiguration/Definition/Extensions/SVCExtension"):
            if prop.find("TypeName").text == 'KmlServer':
                prop.find("Enabled").text = "false"

        # Turn on feature access capabilities
        for prop in doc.findall("./Configurations/SVCConfiguration/Definition/Info/PropertyArray/PropertySetProperty"):
            if prop.find("Key").text == 'WebCapabilities':
                prop.find("Value").text = "Query,Create,Update,Delete,Uploads,Editing,Sync"

        # Add the namespaces which get stripped, back into the .SD
        root_elem.attrib["xmlns:typens"] = 'http://www.esri.com/schemas/ArcGIS/10.1'
        root_elem.attrib["xmlns:xs"] = 'http://www.w3.org/2001/XMLSchema'
        newSDdraft = os.path.dirname(sddraft) + os.sep + "draft_mod.sddraft"
        # Write the new draft to disk
        with open(newSDdraft, 'w') as f:
            doc.write(f, 'utf-8')
        del doc
        return newSDdraft


   #----------------------------------------------------------------------
    def enableSharingUserItem(self, agol_id, everyone='true', orgs='true', groups='None',folder=None):
        """ changes an items sharing permissions """
        share_url = '{}/content/users/{}'.format(self._url,self._username)

        if folder:
            share_url += '/' + folder

        share_url += '/items/{}/share'.format(agol_id)



        if groups == None:
            groups = ''
        query_dict = {'f': 'json',
                      'everyone' : everyone,
                      'org' : orgs,
                      'groups' : groups,
                      'token': self._token}
        vals = self._do_post(share_url, query_dict, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
        return self._tostr(vals)

    #----------------------------------------------------------------------
    def enableSharing(self, agol_id, everyone='true', orgs='true', groups='None',folder=None):
        """ changes an items sharing permissions """
        share_url = '{}/content'.format(self._url)


        share_url += '/items/{}/share'.format(agol_id)



        if groups == None:
            groups = ''
        query_dict = {'f': 'json',
                      'everyone' : everyone,
                      'org' : orgs,
                      'groups' : groups,
                      'token': self._token}
        vals = self._do_post(share_url, query_dict, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
        return self._tostr(vals)

    #----------------------------------------------------------------------
    def updateTitle(self, agol_id, title,folder=None):
        """ changes an items title"""
        update_url = '{}/content/users/{}'.format(self._url,self._username)

        if folder:
            update_url += '/' + folder

        update_url += '/items/{}/update'.format(agol_id)

        query_dict = {'f': 'json',
                      'title' : title,
                      'token': self._token}
        vals = self._do_post(update_url, query_dict, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
        return self._tostr(vals)
    #----------------------------------------------------------------------
    def updateThumbnail(self, agol_id, thumbnail,folder=None):
        """ update an items thumbnail"""
        update_url = '{}/content/users/{}'.format(self._url,self._username)

        if folder:
            update_url += '/' + folder

        update_url += '/items/{}/update'.format(agol_id)

        params  = {'f': 'json',
                      "thumbnail":  os.path.basename(thumbnail)
                      }
        if self._token is not None:
            params['token'] = self._token

        parsed = urlparse.urlparse(update_url)

        files = []
        files.append(('thumbnail', thumbnail, os.path.basename(thumbnail)))

        res = self._post_multipart(host=parsed.hostname,
                                   port=parsed.port,
                                   selector=parsed.path,
                                   fields=params,
                                   files=files,
                                   ssl=parsed.scheme.lower() == 'https',
                                   proxy_url=self._proxy_url,
                                   proxy_port=self._proxy_port)
        res = self._unicode_convert(json.loads(res))
        return self._tostr(res)

    #----------------------------------------------------------------------
    def delete_items(self,items,item_type,folder=None,force_delete=False):
        content = self.getUserContent(folder)
        itemID = None
        #Title, item
        resultList=[]
        if 'items' in content:
            for item in content['items']:
                if item['title'] in items and item['type'] in item_type:

                    result = self.deleteItem(item_id=item['id'],folder=folder,force_delete=force_delete)
                    if 'error' in result:
                        resultList.append(result['error'])

                    else:
                        resultList.append(result)
        return resultList
    #----------------------------------------------------------------------

    def publish_to_agol(self, mxd_path, service_name="None", tags="None", description="None",folder=None):
        """ publishes a service to AGOL """

        if not os.path.isabs(mxd_path):
            sciptPath = os.getcwd()
            mxd_path = os.path.join(sciptPath,mxd_path)

        mxd = mapping.MapDocument(mxd_path)
        sddraftFolder = env.scratchFolder + os.sep + "draft"
        sdFolder = env.scratchFolder + os.sep + "sd"
        sddraft = sddraftFolder + os.sep + service_name + ".sddraft"
        sd = sdFolder + os.sep + "%s.sd" % service_name
        mxd = self._prep_mxd(mxd)

        if service_name == "None":
            service_name = mxd.title.strip().replace(' ','_')
        if tags == "None":
            tags = mxd.tags.strip()
        if description == "None":
            description = mxd.description.strip()

        if os.path.isdir(sddraftFolder) == False:
            os.makedirs(sddraftFolder)
        else:
            shutil.rmtree(sddraftFolder, ignore_errors=True)
            os.makedirs(sddraftFolder)
        if os.path.isfile(sddraft):
            os.remove(sddraft)
        analysis = mapping.CreateMapSDDraft(mxd, sddraft,
                                            service_name,
                                            "MY_HOSTED_SERVICES")
        sddraft = self._modify_sddraft(sddraft)
        analysis = mapping.AnalyzeForSD(sddraft)
        if os.path.isdir(sdFolder):
            shutil.rmtree(sdFolder, ignore_errors=True)
            os.makedirs(sdFolder)
        else:
            os.makedirs(sdFolder)
        if analysis['errors'] == {}:
            # Stage the service
            arcpy.StageService_server(sddraft, sd)

        else:
            # If the sddraft analysis contained errors, display them and quit.
            print analysis['errors']
            sys.exit()
        # POST data to site
        content = self.getUserContent(folder=folder)
        #Title, item
        if 'items' in content:
            for item in content['items']:
                if item['title'] == service_name and \
                   item['item'] == os.path.basename(sd):
                    print "Deleted: " + self._tostr( self.deleteItem(item['id']))
    
                elif item['title'] == service_name:
                    print "Deleted: " + self._tostr( self.deleteItem(item['id']))

        res = self.addFile(sd, agol_type="Service Definition", name=service_name,
                                             tags=tags, description=description,folder=folder)
        if "success" in res:
            self._agol_id =  res['id']
        else:
            return res

        del mxd
        p_vals = self._publish(agol_id=self._agol_id,folder=folder)
        if 'error' in p_vals:
            raise ValueError(p_vals)
        return p_vals

    ##----------------------------------------------------------------------
    #def publishWebMap(self, name,tags,snippet,description,extent,data,thumbnail,share_everyone,share_org,share_groups,folder_name=None,protected=False,delete_existing = False):
        #"""
           #The publishWebMap function publishes a web map, sets the details,
           #and shares it with the organization.

           #Inputs:
              #name - the name for the webmap
              #tags - the tags for the web map
              #snippet - the breif summary for the webmap
              #description - the description for the webmap
              #extent - Extent in the following format: "xmin, ymin, xmax, ymax"
              #data - the json representation of the webmap
              #thumbnail - full path or absolute path to the image for the webmap
                #200x133 is the suggested side.
              #share_everyone - True/False to share map with everyone
               #share_org - True/False to share map with Org
              #share_groups - List of groups to share the map with
              #folderName - optional folder name to store the item in
           #Output:
              #WebMapID - returns the webmap id if created or updated
        #"""
        #if os.path.isfile(thumbnail):
            #if not os.path.isabs(thumbnail):
                #thumbnail = os.path.abspath(thumbnail)


        #folderID = self.get_folder_ID(folder_name=folder_name)
        #if delete_existing:
            #items = [name]
            #self.delete_items(items,folderID,item_type="Web Map",force_delete=delete_existing)



        #item_id = self.get_item_ID(item_name=name,item_type='Web Map', folder=folderID)
        #if item_id is not None:
            #webmapInfo = self.updateItem(agol_id=item_id,data=data,folder=folderID)
            #if 'error' in webmapInfo:
                #raise ValueError(str(webmapInfo))
        #else:
            #webmapInfo = self.addItem(name=name,tags=tags,snippet=snippet,description=description,extent=extent,data=data,thumbnail=thumbnail,folder=folderID,item_type='Web Map')
            #if 'error' in webmapInfo:
                #raise ValueError(str(webmapInfo))

            #item_id = webmapInfo['id']
            #if protected:
                #self.enableProtect(item_id,folderID)

            #group_ids = self.get_group_IDs(share_groups)


            #result= self.enableSharing(agol_id=item_id, everyone=share_everyone.lower()== "true" , orgs= share_org.lower()== "true", groups=','.join(group_ids),folder=folderID)
            #if 'error' in result:
                #raise ValueError(str(result))



        #return item_id
    #----------------------------------------------------------------------
    def publishItem(self, name,tags,snippet,description,extent,data,thumbnail,share_everyone,share_org,share_groups,item_type,typeKeywords,folder_name=None,protected=False,delete_existing = False):
        """
           The publish function publishes a item, sets the details,
           and shares it with the organization.

           Inputs:
              name - the name for the webmap
              tags - the tags for the web map
              snippet - the breif summary for the webmap
              description - the description for the webmap
              extent - Extent in the following format: "xmin, ymin, xmax, ymax"
              data - the json representation of the webmap
              thumbnail - full path or absolute path to the image for the webmap
                200x133 is the suggested side.
              share_everyone - True/False to share map with everyone
               share_org - True/False to share map with Org
              share_groups - List of groups to share the map with
              folderName - optional folder name to store the item in
           Output:
              ItemID - returns the webmap id if created or updated
        """

        if os.path.isfile(thumbnail):
            if not os.path.isabs(thumbnail):
                thumbnail = os.path.abspath(thumbnail)


        folderID = self.get_folder_ID(folder_name=folder_name)

        item_id = self.get_item_ID(item_name=name,item_type=item_type, folder=folderID)

        if delete_existing and item_id != None:
            self.deleteItem(item_id =item_id,folder=folderID,force_delete=delete_existing)
            item_id = None

        if item_id is not None:
            itemInfo = self.updateItem(agol_id=item_id,data=data,folder=folderID)
            if 'error' in itemInfo:
                raise ValueError(str(itemInfo))
        else:
            itemInfo = self.addItem(name=name,tags=tags,snippet=snippet,description=description,extent=extent,item_type=item_type,typeKeywords=typeKeywords,data=data,thumbnail=thumbnail,folder=folderID)
            if 'error' in itemInfo:
                raise ValueError(str(itemInfo))

            item_id = itemInfo['id']
            if protected:
                self.enableProtect(item_id,folderID)

            group_ids = self.get_group_IDs(share_groups)


            result= self.enableSharing(agol_id=item_id, everyone=share_everyone.lower()== "true" , orgs= share_org.lower()== "true", groups=','.join(group_ids),folder=folderID)
            if 'error' in result:
                raise ValueError(str(result))



        return item_id

     #----------------------------------------------------------------------
    def get_group_IDs(self, group_names):
        """
           This function retrieves the group IDs

           Inputs:
              group_names - tuple of group names

           Output:
              dict - list of group IDs
        """
        group_ids=[]
        userInfo = self.getUserCommunityInfo()
        if 'groups' in userInfo:
            for gp in userInfo['groups']:
                if gp['title'] in group_names:
                    group_ids.append(gp['id'])
        del userInfo
        return group_ids
   #----------------------------------------------------------------------
    def get_folder_ID(self, folder_name):
        """
           This function retrieves the folder ID and creates the folder if
           it does not exist

           Inputs:
              folder_name - the name of the folder

           Output:
              string - ID of folder, none if no foldername is specified
        """
        if not folder_name == None and not folder_name == '':
            userContent = self.getUserContent()
            folderID = None
            if 'folders' in userContent:
                folders = userContent['folders']

                for folder in folders:
                    if folder['title'] == folder_name:
                        folderID = folder['id']
                        break
                del folders
                del folder

            if folderID == None:
                res = self.createFolder(folder_name)
                if 'success' in res:
                    folderID = res['folder']['id']
            del userContent
            return folderID

        else:
            return None

    #----------------------------------------------------------------------
    def get_item_ID(self, item_name,item_type,folder=None):
        """
           This function retrieves the item ID if the item exist

           Inputs:
              item_name - the name of the item

           Output:
              string - ID of item, none if item does not exist
        """
        itemID = None
        if not item_name == None and not item_name == '':
            userContent = self.getUserContent(folder=folder)
            if 'items' in userContent:
                items = userContent['items']
                for item in items:
                    if item['title'] == item_name and item['type'] in item_type:
                        itemID = item['id']
                        break
                del items

        return itemID
    #----------------------------------------------------------------------
    def createFeatureService(self, mxd, title, share_everyone,share_org,share_groups,thumbnail=None,folder_name=None):
        """
           The createFeatureService function publishes a service definition,
           publishes a features service, sets the details, and shares it with
           the organization.

           Inputs:
              mxd - the name for the webmap
              title - the tags for the web map
              share_everyone - True/False to share map with everyone
              share_org - True/False to share map with Org
              share_groups - List of groups to share the map with
              thumbnail - optional, full path or absolute path to the image for the webmap
                200x133 is the suggested side.
              folderName - optional, folder name to store the item in
           Output:
              Dict - results from publishing the feature service
        """
        service_name = title
        service_name_safe = service_name.replace(' ','_')
        service_name_safe = service_name_safe.replace(':','-')


        folderID = self.get_folder_ID(folder_name=folder_name)

        items = [service_name,service_name_safe]

        self.delete_items(items=items,item_type=['Feature Service','Service Definition'],folder=folderID)
        itemInfo = self.publish_to_agol(mxd_path=mxd,service_name=service_name_safe,folder=folderID)
        if 'error' in itemInfo:
            return itemInfo
        item_id = ''
        service_url = ''
        
        for service in itemInfo['services']:
            if 'error' in service:
                raise ValueError(str(service))
            item_id = service['serviceItemId']
            service_url = service['serviceurl']
            service['folderId'] = folderID

        group_ids = self.get_group_IDs(share_groups)

        errors = []
        result = self.enableSharing(agol_id=item_id, everyone=share_everyone.lower()== "true" , orgs= share_org.lower()== "true", groups=','.join(group_ids),folder=folderID)
        if 'error' in result:
            errors.append(result['error'])

        result = self.updateTitle(agol_id=item_id,title= service_name,folder=folderID)
        if 'error' in result:
            errors.append(result['error'])

        if not thumbnail is None:
            if os.path.isfile(thumbnail):
                if not os.path.isabs(thumbnail):
                    thumbnail = os.path.abspath(thumbnail)
                result = self.updateThumbnail(agol_id=item_id,thumbnail=thumbnail,folder=folderID)
                if 'error' in result:
                    errors.append(result['error'])
        if len(errors)> 0:

            itemInfo['errors'] =  errors
        return itemInfo
    #----------------------------------------------------------------------
    def get_group_content(self, groupID):
        contentURL = '{}/search'.format(self._url)

        query_dict = {
                      'q':'group:{}'.format(groupID),
                      'num': 100,
                      'f': 'json'
                      }
        if self._token != None:
            query_dict['token'] =  self._token

        return self._do_get(contentURL, query_dict,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)

    #----------------------------------------------------------------------
    def _publish(self, agol_id,folder=None):
        """"""
        publishURL = '{}/content/users/{}'.format(self._url,
                                                          self._username)

        if folder:
            publishURL += '/' + folder

        publishURL += '/publish'

        query_dict = {'itemID': agol_id,
                      'filetype': 'serviceDefinition',
                      'f': 'json',
                      'token': self._token
                      }

        return self._do_post(publishURL, query_dict, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
##    def searchGroups(self,q=None, start='1',num=1000,sortField='',
##               sortOrder='asc'):
##        query_dict = {
##            "f" : "json",
##            "token" : self._token,
##            "q": q,
##            "start": start,
##            "num": num,
##            "sortField": sortField,
##            "sortOrder": sortOrder
##        }
##        groupsURL = self._url + "community/groups"
##        return self._do_post(groupsURL, query_dict)
    #----------------------------------------------------------------------
    def createGroup(self, title, description, tags,
                    snippet=None, phone=None,
                    access="org", sortField=None, sortOrder=None,
                    isViewOnly=False, isInvitationOnly=False,
                    thumbnail=None):
        """
           The Create Group operation creates a new group in the Portal
           community.
           Only authenticated users can create groups. The user who creates
           the group automatically becomes the owner of the group. The
           owner of the group is automatically an administrator of the
           group. The calling user provides the title for the group, while
           the group ID is generated by the system.
           Inputs:
              title - The group title must be unique for the username, and
                      the character limit is 250.
              description - A description of the group that can be any
                            length.
              tags - Tags are words or short phrases that describe the
                     group. Separate terms with commas.
              snippet - Snippet or summary of the group that has a
                        character limit of 250 characters.
              phone - Phone is the group contact information. It can be a
                      combination of letters and numbers. The character
                      limit is 250.
              access - sets the access level for the group. private is the
                       default. Setting to org restricts group access to
                       members of your organization. If public, all users
                       can access the group.
                       Values: private | org |public
              sortField - Sets sort field for group items.
              sortOrder - Sets sort order for group items.
              isViewOnly - Allows the group owner or admin to create
                           view-only groups where members are not able to
                           share items. If members try to share, view-only
                           groups are returned in the notshared response
                           property. false is the default.
              isInvitationOnly - If true, this group will not accept join
                                 requests. If false, this group does not
                                 require an invitation to join. Only group
                                 owners and admins can invite users to the
                                 group. false is the default.
              thumbnail - Enter the pathname to the thumbnail image to be
                          used for the group. The recommended image size is
                          200 pixels wide by 133 pixels high. Acceptable
                          image formats are PNG, GIF, and JPEG. The maximum
                          file size for an image is 1 MB. This is not a
                          reference to the file but the file itself, which
                          will be stored in the Portal.
        """
        params = {
            "f" : "json",
            "token" : self._token,
            "title" : title,
            "description" : description,
            "tags" : tags,
            "access" : access,
            "isViewOnly" : isViewOnly,
            "isInvitationOnly" : isInvitationOnly
        }
        uURL = self._url + "/community/createGroup"
        if snippet is not None:
            params['snippet'] = snippet
        if phone is not None:
            params['phone'] = phone
        if sortField is not None:
            params['sortField'] = sortField
        if sortOrder is not None:
            params['sortOrder'] = sortOrder
        if thumbnail is not None and \
           os.path.isfile(thumbnail):

            params['thumbnail'] = os.path.basename(thumbnail)
            content = open(thumbnail, 'rb').read()
            parsed = urlparse.urlparse(uURL)

            files = []
            files.append(('thumbnail', thumbnail, os.path.basename(thumbnail)))

            return self._post_multipart(host=parsed.hostname,
                                        port=parsed.port,
                                        selector=parsed.path,
                                        fields=params,
                                        files=files,
                                        ssl=parsed.scheme.lower() == 'https',
                                        proxy_port=self._proxy_port,
                                        proxy_url=self._proxy_url)

        else:
            return self._do_post(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)




# This function is a workaround to deal with what's typically described as a
# problem with the web server closing a connection. This is problem
# experienced with www.arcgis.com (first encountered 12/13/2012). The problem
# and workaround is described here:
# http://bobrochel.blogspot.com/2010/11/bad-servers-chunked-encoding-and.html
def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner
httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)
