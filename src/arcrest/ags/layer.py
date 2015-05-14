from .._abstract.abstract import BaseAGSServer
import json
import os
from urlparse import urlparse
import uuid
from ..security import security
from .._abstract.abstract import DynamicData, DataSource
from ..common.spatial import scratchGDB, scratchFolder, featureclass_to_json, json_to_featureclass
from ..common import filters
from ..common.general import _date_handler, _unicode_convert, Feature, FeatureSet
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
    _securityHandler = None
    _supportsRollbackOnFailureParameter = None
    _globalIdField = None
    _syncCanReturnChanges = None
    _allowGeometryUpdates = None
    _objectIdField = None
    _templates = None
    _editFieldsInfo = None
    _proxy_url = None
    _proxy_port = None
    _json = None
    _advancedQueryCapabilities = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 initialize=False,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._url = url
        if securityHandler is not None and \
           isinstance(securityHandler,
                      (security.AGSTokenSecurityHandler,
                       security.PortalServerSecurityHandler)):
            self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
            self._token = securityHandler.token
        elif securityHandler is None:
            pass
        else:
            raise AttributeError("Security Handler must type of security.AGSTokenSecurityHandler")
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __init(self):
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token   
        json_dict = self._do_get(self._url, params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implmented for layer.FeatureLayer."
    #----------------------------------------------------------------------
    @property
    def advancedQueryCapabilities(self):
        """returns the advancedQueryCapabilities property"""
        if self._advancedQueryCapabilities is None:
            self.__init()
        return self._advancedQueryCapabilities
    #----------------------------------------------------------------------
    @property
    def supportsRollbackOnFailureParameter(self):
        """ returns the value for the supportsRollbackOnFailureParameter """
        if self._supportsRollbackOnFailureParameter is None:
            self.__init()
        return self._supportsRollbackOnFailureParameter
    #----------------------------------------------------------------------
    @property
    def globalIdField(self):
        """returns the global id field"""
        if self._globalIdField is None:
            self.__init()
        return self._globalIdField
    #----------------------------------------------------------------------
    @property
    def syncCanReturnChanges(self):
        """ returns the sync can return changes """
        if self._syncCanReturnChanges  is None:
            self.__init()
        return self._syncCanReturnChanges
    #----------------------------------------------------------------------
    @property
    def allowGeometryUpdates(self):
        """ returns the boolean value """
        if self._allowGeometryUpdates is None:
            self.__init()
        return self._allowGeometryUpdates
    #----------------------------------------------------------------------
    @property
    def objectIdField(self):
        """ returns the object id field """
        if self._objectIdField is None:
            self.__init()
        return self._objectIdField
    #----------------------------------------------------------------------
    @property
    def templates(self):
        """ returns the templates """
        if self._templates is None:
            self.__init()
        return self._templates
    #----------------------------------------------------------------------
    @property
    def editFieldsInfo(self):
        """ returns the edit field information """
        if self._editFieldsInfo is None:
            self.__init()
        return self._editFieldsInfo
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
    #----------------------------------------------------------------------
    def addFeature(self, features,
                   gdbVersion=None,
                   rollbackOnFailure=True):
        """ Adds a single feature to the service
           Inputs:
              feature - list of common.Feature object or a single
                        common.Feature Object
              gdbVersion - Geodatabase version to apply the edits
              rollbackOnFailure - Optional parameter to specify if the
                                  edits should be applied only if all
                                  submitted edits succeed. If false, the
                                  server will apply the edits that succeed
                                  even if some of the submitted edits fail.
                                  If true, the server will apply the edits
                                  only if all edits succeed. The default
                                  value is true.
           Output:
              JSON message as dictionary
        """
        url = self._url + "/addFeatures"
        params = {
            "f" : "json"
        }
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token   
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if isinstance(rollbackOnFailure, bool):
            params['rollbackOnFailure'] = rollbackOnFailure
        if isinstance(features, list) or \
           isinstance(features, FeatureSet):
            params['features'] = json.dumps([feature.asDictionary for feature in features],
                                            default=_date_handler)
        elif isinstance(features, Feature):
            params['features'] = json.dumps([features.asDictionary],
                                            default=_date_handler)
        else:
            return None
        return self._do_post(url=url,
                             param_dict=params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def addAttachments(self,
                       featureId,
                       attachment,
                       gdbVersion=None,
                       uploadId=None):
        """
        This operation adds an attachment to the associated feature (POST
        only). The addAttachment operation is performed on a feature
        service feature resource.
        Since this request uploads a file, it must be a multipart request
        pursuant to IETF RFC1867.
        This operation is available only if the layer has advertised that
        it has attachments. A layer has attachments if its hasAttachments
        property is true.
        See the Limiting upload file size and file types section under
        Uploads to learn more about default file size and file type
        limitations imposed on attachments.
        The result of this operation is an array of edit result objects.
        Each edit result indicates whether or not the edit was successful.
        If successful, the objectId of the result is the ID of the new
        attachment. If unsuccessful, it also includes an error code and
        error description.
        You can provide arguments to the addAttachment operation as defined
        in the following parameters table:

        Inputs:
           attachment - The file to be uploaded as a new feature
             attachment. The content type, size, and name of the attachment
             will be derived from the uploaded file.
           gdbVersion - Geodatabase version to apply the edits. This
             parameter applies only if the isDataVersioned property of the
             layer is true. If the gdbVersion parameter is not specified,
             edits are made to the published map's version.
           uploadId - This option was added to the July 2014 of ArcGIS
             Online. It is not available with ArcGIS Server. The ID of the
             attachment that has already been uploaded to the server. This
             parameter only applies if the supportsAttachmentsByUploadId
             property of the layer is true.
        """
        if self.hasAttachments == True:
            url = self._url + "/%s/addAttachment" % featureId
            params = {'f':'json'}
            if self._securityHandler is not None:
                params['token'] = self._securityHandler.token   
            parsed = urlparse(url)
            files = []
            files.append(('attachment', attachment, os.path.basename(attachment)))
            res = self._post_multipart(host=parsed.hostname,
                                       selector=parsed.path,
                                       files=files,
                                       fields=params,
                                       port=parsed.port,
                                       ssl=parsed.scheme.lower() == 'https',
                                       proxy_url=self._proxy_url,
                                       proxy_port=self._proxy_port)
            return self._unicode_convert(res)
        else:
            return "Attachments are not supported for this feature service."
    #----------------------------------------------------------------------
    def deleteFeatures(self,
                       objectIds="",
                       where="",
                       geometryFilter=None,
                       gdbVersion=None,
                       rollbackOnFailure=True
                       ):
        """ removes 1:n features based on a sql statement
            Input:
              objectIds - The object IDs of this layer/table to be deleted
              where - A where clause for the query filter. Any legal SQL
                      where clause operating on the fields in the layer is
                      allowed. Features conforming to the specified where
                      clause will be deleted.
              geometryFilter - a filters.GeometryFilter object to limit
                               deletion by a geometry.
              gdbVersion - Geodatabase version to apply the edits. This
                           parameter applies only if the isDataVersioned
                           property of the layer is true
              rollbackOnFailure - parameter to specify if the edits should
                                  be applied only if all submitted edits
                                  succeed. If false, the server will apply
                                  the edits that succeed even if some of
                                  the submitted edits fail. If true, the
                                  server will apply the edits only if all
                                  edits succeed. The default value is true.
            Output:
               JSON response as dictionary
        """
        dURL = self._url + "/deleteFeatures"
        params = {
            "f": "json",
        }
        if geometryFilter is not None and \
           isinstance(geometryFilter, filters.GeometryFilter):
            gfilter = geometryFilter.filter
            params['geometry'] = gfilter['geometry']
            params['geometryType'] = gfilter['geometryType']
            params['inSR'] = gfilter['inSR']
            params['spatialRel'] = gfilter['spatialRel']
        if where is not None and \
           where != "":
            params['where'] = where
        if objectIds is not None and \
           objectIds != "":
            params['objectIds'] = objectIds
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token   
        result = self._do_post(url=dURL, param_dict=params, proxy_port=self._proxy_port,
                               proxy_url=self._proxy_url)
        self.__init()
        return result
    #----------------------------------------------------------------------
    def applyEdits(self,
                   addFeatures=[],
                   updateFeatures=[],
                   deleteFeatures=None,
                   gdbVersion=None,
                   rollbackOnFailure=True):
        """
           This operation adds, updates, and deletes features to the
           associated feature layer or table in a single call.
           Inputs:
              addFeatures - The array of features to be added.  These
                            features should be common.general.Feature
                            objects, or they should be a
                            common.general.FeatureSet object.
              updateFeatures - The array of features to be updateded.
                               These features should be common.Feature
                               objects
              deleteFeatures - string of OIDs to remove from service
              gdbVersion - Geodatabase version to apply the edits.
              rollbackOnFailure - Optional parameter to specify if the
                                  edits should be applied only if all
                                  submitted edits succeed. If false, the
                                  server will apply the edits that succeed
                                  even if some of the submitted edits fail.
                                  If true, the server will apply the edits
                                  only if all edits succeed. The default
                                  value is true.
           Output:
              dictionary of messages
        """
        editURL = self._url + "/applyEdits"
        params = {"f": "json"
                  }
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token   
        if len(addFeatures) > 0 and \
           isinstance(addFeatures[0], Feature):
            params['adds'] = json.dumps([f.asDictionary for f in addFeatures],
                                        default=_date_handler)
        elif isinstance(addFeatures, FeatureSet):
            params['adds'] = json.dumps([f.asDictionary for f in addFeatures],
                                        default=_date_handler)
        if len(updateFeatures) > 0 and \
           isinstance(updateFeatures[0], Feature):
            params['updates'] = json.dumps([f.asDictionary for f in updateFeatures],
                                           default=_date_handler)
        if deleteFeatures is not None and \
           isinstance(deleteFeatures, str):
            params['deletes'] = deleteFeatures
        return self._do_post(url=editURL, param_dict=params,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateFeature(self,
                      features,
                      gdbVersion=None,
                      rollbackOnFailure=True):
        """
           updates an existing feature in a feature service layer
           Input:
              feature - feature object(s) to get updated.  A single feature
                        or a list of feature objects can be passed
           Output:
              dictionary of result messages
        """
        params = {
            "f" : "json",
            "rollbackOnFailure" : rollbackOnFailure
        }
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token           
        if isinstance(features, Feature):
            params['features'] = json.dumps([features.asDictionary])
        elif isinstance(features, list):
            vals = []
            for feature in features:
                if isinstance(feature, Feature):
                    vals.append(feature.asDictionary)
            params['features'] = json.dumps(vals)
        elif isinstance(features, FeatureSet):
            params['features'] = json.dumps([f.asDictionary for f in features],
                                            default=_date_handler)
        else:
            return {'message' : "invalid inputs"}
        updateURL = self._url + "/updateFeatures"
        res = self._do_post(url=updateURL,
                            param_dict=params, proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
        return res
    #----------------------------------------------------------------------
    def query(self,
              where="1=1",
              out_fields="*",
              timeFilter=None,
              geometryFilter=None,
              returnGeometry=True,
              returnIDsOnly=False,
              returnCountOnly=False,
              returnFeatureClass=False,
              out_fc=None):
        """ queries a feature service based on a sql statement
            Inputs:
               where - the selection sql statement
               out_fields - the attribute fields to return
               timeFilter - a TimeFilter object where either the start time
                            or start and end time are defined to limit the
                            search results for a given time.  The values in
                            the timeFilter should be as UTC timestampes in
                            milliseconds.  No checking occurs to see if they
                            are in the right format.
               geometryFilter - a GeometryFilter object to parse down a given
                               query by another spatial dataset.
               returnGeometry - true means a geometry will be returned,
                                else just the attributes
               returnIDsOnly - false is default.  True means only OBJECTIDs
                               will be returned
               returnCountOnly - if True, then an integer is returned only
                                 based on the sql statement
               returnFeatureClass - Default False. If true, query will be
                                    returned as feature class
               out_fc - only valid if returnFeatureClass is set to True.
                        Output location of query.
            Output:
               A list of Feature Objects (default) or a path to the output featureclass if
               returnFeatureClass is set to True.
         """
        params = {"f": "json",
                  "where": where,
                  "outFields": out_fields,
                  "returnGeometry" : returnGeometry,
                  "returnIdsOnly" : returnIDsOnly,
                  "returnCountOnly" : returnCountOnly,
                  }
        if not self._token is None:
            params["token"] = self._token
        if not timeFilter is None and \
           isinstance(timeFilter, filters.TimeFilter):
            params['time'] = timeFilter.filter
        if not geometryFilter is None and \
           isinstance(geometryFilter, filters.GeometryFilter):
            gf = geometryFilter.filter
            params['geometry'] = gf['geometry']
            params['geometryType'] = gf['geometryType']
            params['spatialRelationship'] = gf['spatialRel']
            params['inSR'] = gf['inSR']
        fURL = self._url + "/query"
        results = self._do_get(fURL, params, proxy_port=self._proxy_port,
                               proxy_url=self._proxy_url)
        if 'error' in results:
            raise ValueError (results)
        if not returnCountOnly and not returnIDsOnly:
            if returnFeatureClass:
                json_text = json.dumps(results)
                temp = scratchFolder() + os.sep + uuid.uuid4().get_hex() + ".json"
                with open(temp, 'wb') as writer:
                    writer.write(json_text)
                    writer.flush()
                del writer
                fc = json_to_featureclass(json_file=temp,
                                          out_fc=out_fc)
                os.remove(temp)
                return fc
            else:
                return FeatureSet.fromJSON(json.dumps(results))
        else:
            return results
        return
    #----------------------------------------------------------------------
    def calculate(self, where, calcExpression, sqlFormat="standard"):
        """
        The calculate operation is performed on a feature service layer
        resource. It updates the values of one or more fields in an
        existing feature service layer based on SQL expressions or scalar
        values. The calculate operation can only be used if the
        supportsCalculate property of the layer is true.
        Neither the Shape field nor system fields can be updated using
        calculate. System fields include ObjectId and GlobalId.
        See Calculate a field for more information on supported expressions

        Inputs:
           where - A where clause can be used to limit the updated records.
                   Any legal SQL where clause operating on the fields in
                   the layer is allowed.
           calcExpression - The array of field/value info objects that
                            contain the field or fields to update and their
                            scalar values or SQL expression.  Allowed types
                            are dictionary and list.  List must be a list
                            of dictionary objects.
                            Calculation Format is as follows:
                               {"field" : "<field name>",
                               "value" : "<value>"}
           sqlFormat - The SQL format for the calcExpression. It can be
                       either standard SQL92 (standard) or native SQL
                       (native). The default is standard.
                       Values: standard, native
        Output:
           JSON as string
        Usage:
        >>>sh = arcrest.AGOLTokenSecurityHandler("user", "pw")
        >>>fl = arcrest.agol.FeatureLayer(url="someurl",
                                     securityHandler=sh, initialize=True)
        >>>print fl.calculate(where="OBJECTID < 2",
                              calcExpression={"field": "ZONE",
                                              "value" : "R1"})
        {'updatedFeatureCount': 1, 'success': True}
        """
        url = self._url + "/calculate"
        params = {
            "f" : "json",
            "where" : where,

        }
        if isinstance(calcExpression, dict):
            params["calcExpression"] = json.dumps([calcExpression],
                                                  default=_date_handler)
        elif isinstance(calcExpression, list):
            params["calcExpression"] = json.dumps(calcExpression,
                                                  default=_date_handler)
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token   
        if sqlFormat.lower() in ['native', 'standard']:
            params['sqlFormat'] = sqlFormat.lower()
        else:
            params['sqlFormat'] = "standard"
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
########################################################################
class GroupLayer(FeatureLayer):
    """ represents a group layer  """
    _securityHandler = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None):
        """Constructor"""
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._url = url
        if securityHandler is not None and \
           isinstance(securityHandler,
                      security.AGSTokenSecurityHandler):
            self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
            self._token = securityHandler.token
        elif securityHandler is None:
            pass
        else:
            raise AttributeError("Security Handler must type of security.AGSTokenSecurityHandler")
        self.__init()
    def __init(self):
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token   
        json_dict = json.loads(self._do_get(self._url, params,
                                            proxy_url=self._proxy_url,
                                            proxy_port=self._proxy_port))
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implmented."
########################################################################
class TableLayer(FeatureLayer):
    """Table object is exactly like FeatureLayer object"""
    pass
########################################################################
class RasterLayer(FeatureLayer):
    """Raster Layer is exactly like FeatureLayer object"""
    pass
########################################################################
class DynamicMapLayer(DynamicData):
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
class DynamicDataLayer(DynamicData):
    """

    """
    _type = "dataLayer"
    _dataSource = None
    _fields = None
    #----------------------------------------------------------------------
    def __init__(self, dataSource, fields=None):
        """Constructor"""
        if isinstance(dataSource, DataSource):
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
        if isinstance(value, DataSource):
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
class TableDataSource(DataSource):
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
class RasterDataSource(DataSource):
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
class QueryTableDataSource(DataSource):
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
class JoinTableDataSource(DataSource):
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