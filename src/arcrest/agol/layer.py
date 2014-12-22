"""

.. module:: layer
   :platform: Windows, Linux
   :synopsis: Class that contians feature service layer information.

.. moduleauthor:: Esri


"""
from .._abstract import abstract
from ..security import security
import types
from ..common import filters
from ..common.geometry import SpatialReference
from ..common.general import _date_handler, _unicode_convert, Feature
from ..common.spatial import scratchFolder, scratchGDB, json_to_featureclass
from ..common.spatial import get_OID_field, get_records_with_attachments
from ..common.spatial import create_feature_layer, merge_feature_class
from ..common.spatial import featureclass_to_json, create_feature_class
from ..common.spatial import get_attachment_data
import featureservice
import os
import json
import math
import urlparse
import mimetypes
import uuid
from urlparse import urlparse
########################################################################
class FeatureLayer(abstract.BaseAGOLClass):
    """
       This contains information about a feature service's layer.
    """
    _objectIdField = None
    _allowGeometryUpdates = None
    _globalIdField = None
    _token_url = None
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
    _supportsValidateSql = None
    _supportsCoordinatesQuantization = None
    _supportsStatistics = None
    _supportsAdvancedQueries = None
    _hasLabels = None
    _canScaleSymbols = None
    _capabilities = None
    _supportedQueryFormats =  None
    _isDataVersioned = None
    _ownershipBasedAccessControlForFeatures = None
    _useStandardizedQueries = None
    _templates = None
    _indexes = None
    _hasStaticData = None
    _supportsRollbackOnFailureParameter = None
    _advancedQueryCapabilities = None
    _editingInfo = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _supportsCalculate = None
    _supportsAttachmentsByUploadId = None
    _editFieldsInfo = None
    _serverURL = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler=None,
                 initialize=False,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._url = url

        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if securityHandler is not None and \
           isinstance(securityHandler, abstract.BaseSecurityHandler):
            if isinstance(securityHandler, security.AGOLTokenSecurityHandler):
                self._token = securityHandler.token
                self._username = securityHandler.username
                self._password = securityHandler.password
                self._token_url = securityHandler.token_url
                self._securityHandler = securityHandler
                self._referer_url = securityHandler.referer_url  
            elif isinstance(securityHandler, security.PortalTokenSecurityHandler):
                parsedURL = urlparse(url=url)
                pathParts = parsedURL.path.split('/')
                self._serverURL = parsedURL.scheme + '://' + parsedURL.netloc + '/' + pathParts[1]
                
                self._token = securityHandler.servertoken(serverURL=self._serverURL,referer=parsedURL.netloc)
                self._username = securityHandler.username
                self._password = securityHandler.password
                self._token_url = securityHandler.token_url
                self._securityHandler = securityHandler
                self._referer_url = securityHandler.referer_url
                
            elif isinstance(securityHandler, security.OAuthSecurityHandler):
                self._token = securityHandler.token
                self._securityHandler = securityHandler
            else:
                pass
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
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented in Feature Layer."
        self._parentLayer = featureservice.FeatureService(
            url=os.path.dirname(self._url),
            securityHandler=self._securityHandler,
            proxy_port=self._proxy_port,
            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        return json.dumps(dict(self), default=_date_handler)
    #----------------------------------------------------------------------
    def __iter__(self):
        """ iterator generator for public values/properties
            It only returns the properties that are public.
        """
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_') and \
                      not isinstance(getattr(self, attr), (types.MethodType,
                                                           types.BuiltinFunctionType,
                                                           types.BuiltinMethodType))
                      ]
        for att in attributes:
            yield (att, getattr(self, att))
    #----------------------------------------------------------------------
    @property
    def url(self):
        """ returns the url for the feature layer"""
        return self._url      
    
    #----------------------------------------------------------------------
    @property
    def supportsValidateSql(self):
        """ returns the supports calculate values """
        if self._supportsValidateSql is None:
            self.__init()
        return self._supportsValidateSql    

    #----------------------------------------------------------------------
    @property
    def supportsCoordinatesQuantization(self):
        """ returns the supports calculate values """
        if self._supportsCoordinatesQuantization is None:
            self.__init()
        return self._supportsCoordinatesQuantization   
    #----------------------------------------------------------------------
    @property
    def supportsCalculate(self):
        """ returns the supports calculate values """
        if self._supportsCalculate is None:
            self.__init()
        return self._supportsCalculate
    #----------------------------------------------------------------------
    
    @property
    def editFieldsInfo(self):
        """ returns edit field info """
        if self._editFieldsInfo is None:
            self.__init()
        return self._editFieldsInfo
        #----------------------------------------------------------------------    
    @property
    def supportsAttachmentsByUploadId(self):
        """ returns is supports attachments by uploads id """
        if self._supportsAttachmentsByUploadId is None:
            self.__init()
        return self._supportsAttachmentsByUploadId
    #----------------------------------------------------------------------
    @property
    def editingInfo(self):
        """ returns the edit information """
        if self._editingInfo is None:
            self.__init()
        return self._editingInfo
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
    @property
    def maxScale(self):
        """ sets the max scale """
        if self._maxScale is None:
            self.__init()
        return self._maxScale
    @property
    def effectiveMinScale(self):
        """ returns the effective minimum scale value """
        if self._effectiveMinScale is None:
            self.__init()
        return self._effectiveMinScale
    @property
    def effectiveMaxScale(self):
        """ returns the effective maximum scale value """
        if self._effectiveMaxScale is None:
            self.__init()
        return self._effectiveMaxScale
    @property
    def defaultVisibility(self):
        """ returns the default visibility of the layer """
        if self._defaultVisibility is None:
            self.__init()
        return self._defaultVisibility
    @property
    def extent(self):
        """ returns the extent """
        if self._extent is None:
            self.__init()
        return self._extent
    @property
    def timeInfo(self):
        """ returns the time information about the layer """
        if self._timeInfo is None:
            self.__init()
        return self._timeInfo
    @property
    def drawingInfo(self):
        """ returns the symbol information about the layer """
        if self._drawingInfo is None:
            self.__init()
        return self._drawingInfo
    @property
    def hasAttachments(self):
        """ boolean that tells if attachments are associated with layer """
        if self._hasAttachments is None:
            self.__init()
        return self._hasAttachments
    @property
    def htmlPopupType(self):
        """ returns the popup type  """
        if self._htmlPopupType is None:
            self.__init()
        return self._htmlPopupType
    @property
    def displayField(self):
        """ returns the primary display field """
        if self._displayField is None:
            self.__init()
        return self._displayField
    @property
    def typeIdField(self):
        """ returns the type Id field """
        if self._typeIdField is None:
            self.__init()
        return self._typeIdField
    @property
    def fields(self):
        """ returns the layer's fields """
        if self._fields is None:
            self.__init()
        return self._fields
    @property
    def types(self):
        """ returns the types """
        if self._types is None:
            self.__init()
        return self._types
    @property
    def relationships(self):
        """ returns the relationships for the layer """
        if self._relationships is None:
            self.__init()
        return self._relationships
    @property
    def maxRecordCount(self):
        """ returns the maximum returned records """
        if self._maxRecordCount is None:
            self.__init()
            if self._maxRecordCount is None:
                self._maxRecordCount = 1000
        return self._maxRecordCount
    @property
    def canModifyLayer(self):
        """ returns boolean to say if layer can be modified """
        if self._canModifyLayer is None:
            self.__init()
        return self._canModifyLayer
    @property
    def supportsStatistics(self):
        """  boolean to if supports statistics """
        if self._supportsStatistics is None:
            self.__init()
        return self._supportsStatistics
    @property
    def supportsAdvancedQueries(self):
        """ boolean value if advanced queries is supported """
        if self._supportsAdvancedQueries is None:
            self.__init()
        return self._supportsAdvancedQueries
    @property
    def hasLabels(self):
        """ returns if layer has labels on or not """
        if self._hasLabels is None:
            self.__init()
        return self._hasLabels
    @property
    def canScaleSymbols(self):
        """ states if symbols can scale """
        if self._canScaleSymbols is None:
            self.__init()
        return self._canScaleSymbols
    @property
    def capabilities(self):
        """ operations that can be performed on layer """
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    @property
    def supportedQueryFormats(self):
        """ returns supported query formats """
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    @property
    def isDataVersioned(self):
        """ returns boolean if data is in version control """
        if self._isDataVersioned is None:
            self.__init()
        return self._isDataVersioned
    @property
    def ownershipBasedAccessControlForFeatures(self):
        """ returns value for owernship based access control """
        if self._ownershipBasedAccessControlForFeatures is None:
            self.__init()
        return self._ownershipBasedAccessControlForFeatures
    @property
    def useStandardizedQueries(self):
        """ returns value if standardized queries can be used """
        if self._useStandardizedQueries is None:
            self.__init()
        return self._useStandardizedQueries
    #----------------------------------------------------------------------
    @property
    def securityHandler(self):
        """ gets the security handler """
        return self._securityHandler
    #----------------------------------------------------------------------
    @securityHandler.setter
    def securityHandler(self, value):
        """ sets the security handler """
        if isinstance(value, abstract.BaseSecurityHandler):
            if isinstance(value, security.AGOLTokenSecurityHandler):
                self._securityHandler = value
                self._token = value.token
                self._username = value.username
                self._password = value._password
                self._token_url = value.token_url
            elif isinstance(value, security.OAuthSecurityHandler):
                self._token = value.token
                self._securityHandler = value
            else:
                pass
    #----------------------------------------------------------------------
    def addAttachment(self, oid, file_path):
        """ Adds an attachment to a feature service
            Input:
              oid - string - OBJECTID value to add attachment to
              file_path - string - path to file
            Output:
              JSON Repsonse
        """
        if self.hasAttachments == True:
            attachURL = self._url + "/%s/addAttachment" % oid
            params = {'f':'json'}
            if not self._token is None:
                params['token'] = self._token
            parsed = urlparse(attachURL)

            files = []
            files.append(('attachment', file_path, os.path.basename(file_path)))
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
    def deleteAttachment(self, oid, attachment_id):
        """ removes an attachment from a feature service feature
            Input:
              oid - integer or string - id of feature
              attachment_id - integer - id of attachment to erase
            Output:
               JSON response
        """
        url = self._url + "/%s/deleteAttachments" % oid
        params = {
            "f":"json",
            "attachmentIds" : "%s" % attachment_id
        }
        if not self._token is None:
            params['token'] = self._token
        return self._do_post(url, params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def updateAttachment(self, oid, attachment_id, file_path):
        """ updates an existing attachment with a new file
            Inputs:
               oid - string/integer - Unique record ID
               attachment_id - integer - Unique attachment identifier
               file_path - string - path to new attachment
            Output:
               JSON response
        """
        url = self._url + "/%s/updateAttachment" % oid
        params = {
            "f":"json",
            "attachmentId" : "%s" % attachment_id
        }
        if not self._token is None:
            params['token'] = self._token
        parsed = urlparse(url)
        port = parsed.port
        files = []
        files.append(('attachment', file_path, os.path.basename(file_path)))
        res = self._post_multipart(host=parsed.hostname,
                                   selector=parsed.path,
                                   files=files,
                                   port=port,
                                   fields=params,
                                   ssl=parsed.scheme.lower() == 'https',
                                   proxy_port=self._proxy_port,
                                   proxy_url=self._proxy_url)
        return self._unicode_convert(res)
    #----------------------------------------------------------------------
    def listAttachments(self, oid):
        """ list attachements for a given OBJECT ID """
        url = self._url + "/%s/attachments" % oid
        params = {
            "f":"json"
        }
        if not self._token is None:
            params['token'] = self._token
        return self._do_get(url, params, proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def create_fc_template(self, out_path, out_name):
        """creates a featureclass template on local disk"""
        fields = self.fields
        objectIdField = self.objectIdField
        geomType = self.geometryType
        wkid = self.parentLayer.spatialReference['wkid']
        return create_feature_class(out_path,
                                    out_name,
                                    geomType,
                                    wkid,
                                    fields,
                                    objectIdField)
    def create_feature_template(self):
        """creates a feature template"""
        fields = self.fields
        feat_schema = {}

        att = {}
        for fld in fields:
            self._globalIdField
            if not fld['name'] == self._objectIdField and not fld['name'] == self._globalIdField:
                att[fld['name']] = ''

        feat_schema['attributes'] = att
        feat_schema['geometry'] = ''
        return Feature(feat_schema)

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
                feats = []
                for res in results['features']:
                    feats.append(Feature(res))
                return feats
        else:
            return results
        return
    #----------------------------------------------------------------------
    def query_related_records(self,
                              objectIds,
                              relationshipId,
                              outFields="*",
                              definitionExpression=None,
                              returnGeometry=True,
                              maxAllowableOffset=None,
                              geometryPrecision=None,
                              outWKID=None,
                              gdbVersion=None,
                              returnZ=False,
                              returnM=False):
        """
           The Query operation is performed on a feature service layer
           resource. The result of this operation are feature sets grouped
           by source layer/table object IDs. Each feature set contains
           Feature objects including the values for the fields requested by
           the user. For related layers, if you request geometry
           information, the geometry of each feature is also returned in
           the feature set. For related tables, the feature set does not
           include geometries.
           Inputs:
              objectIds - the object IDs of the table/layer to be queried
              relationshipId - The ID of the relationship to be queried.
              outFields - the list of fields from the related table/layer
                          to be included in the returned feature set. This
                          list is a comma delimited list of field names. If
                          you specify the shape field in the list of return
                          fields, it is ignored. To request geometry, set
                          returnGeometry to true.
                          You can also specify the wildcard "*" as the
                          value of this parameter. In this case, the result
                          s will include all the field values.
              definitionExpression - The definition expression to be
                                     applied to the related table/layer.
                                     From the list of objectIds, only those
                                     records that conform to this
                                     expression are queried for related
                                     records.
              returnGeometry - If true, the feature set includes the
                               geometry associated with each feature. The
                               default is true.
              maxAllowableOffset - This option can be used to specify the
                                   maxAllowableOffset to be used for
                                   generalizing geometries returned by the
                                   query operation. The maxAllowableOffset
                                   is in the units of the outSR. If outSR
                                   is not specified, then
                                   maxAllowableOffset is assumed to be in
                                   the unit of the spatial reference of the
                                   map.
              geometryPrecision - This option can be used to specify the
                                  number of decimal places in the response
                                  geometries.
              outWKID - The spatial reference of the returned geometry.
              gdbVersion - The geodatabase version to query. This parameter
                           applies only if the isDataVersioned property of
                           the layer queried is true.
              returnZ - If true, Z values are included in the results if
                        the features have Z values. Otherwise, Z values are
                        not returned. The default is false.
              returnM - If true, M values are included in the results if
                        the features have M values. Otherwise, M values are
                        not returned. The default is false.
        """
        params = {
            "f" : "json",
            "objectIds" : objectIds,
            "relationshipId" : relationshipId,
            "outFields" : outFields,
            "returnGeometry" : returnGeometry,
            "returnM" : returnM,
            "returnZ" : returnZ
        }
        if self._token is not None:
            params['token'] = self._token
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if definitionExpression is not None:
            params['definitionExpression'] = definitionExpression
        if outWKID is not None:
            params['outSR'] = SpatialReference(outWKID).asDictionary
        if maxAllowableOffset is not None:
            params['maxAllowableOffset'] = maxAllowableOffset
        if geometryPrecision is not None:
            params['geometryPrecision'] = geometryPrecision
        quURL = self._url + "/queryRelatedRecords"
        res = self._do_get(url=quURL, param_dict=params,
                           proxy_port=self._proxy_port,
                           proxy_url=self._proxy_url)
        return res
    #----------------------------------------------------------------------
    def getHTMLPopup(self, oid):
        """
           The htmlPopup resource provides details about the HTML pop-up
           authored by the user using ArcGIS for Desktop.
           Input:
              oid - object id of the feature where the HTML pop-up
           Output:

        """
        if self.htmlPopupType != "esriServerHTMLPopupTypeNone":
            popURL = self._url + "/%s/htmlPopup" % oid
            params = {
                'f' : "json"
            }
            if self._token is not None:
                params['token'] = self._token
            return self._do_get(url=popURL, param_dict=params, proxy_port=self._proxy_port,
                                proxy_url=self._proxy_url)
        return ""
    #----------------------------------------------------------------------
    def _chunks(self, l, n):
        """ Yield n successive chunks from a list l.
        """
        l.sort()
        newn = int(1.0 * len(l) / n + 0.5)
        for i in xrange(0, n-1):
            yield l[i*newn:i*newn+newn]
        yield l[n*newn-newn:]
    #----------------------------------------------------------------------
    def get_local_copy(self, out_path, includeAttachments=False):
        """ exports the whole feature service to a feature class
            Input:
               out_path - path to where the data will be placed
               includeAttachments - default False. If sync is not supported
                                    then the paramter is ignored.
            Output:
               path to exported feature class or fgdb (as list)
        """
        if self.hasAttachments and \
           self.parentLayer.syncEnabled:
            return self.parentLayer.createReplica(replicaName="fgdb_dump",
                                                  layers="%s" % self.id,
                                                  returnAsFeatureClass=True,
                                                  returnAttachments=includeAttachments,
                                                  out_path=out_path)[0]
        elif self.hasAttachments == False and \
             self.parentLayer.syncEnabled:
            return self.parentLayer.createReplica(replicaName="fgdb_dump",
                                                  layers="%s" % self.id,
                                                  returnAsFeatureClass=True,
                                                  out_path=out_path)[0]
        else:
            result_features = []
            res = self.query(returnIDsOnly=True)
            OIDS = res['objectIds']
            OIDS.sort()
            OIDField = res['objectIdFieldName']
            count = len(OIDS)
            if count <= self.maxRecordCount:
                bins = 1
            else:
                bins = count / self.maxRecordCount
                v = count % self.maxRecordCount
                if v > 0:
                    bins += 1
            chunks = self._chunks(OIDS, bins)
            for chunk in chunks:
                chunk.sort()
                sql = "%s >= %s and %s <= %s" % (OIDField, chunk[0],
                                                 OIDField, chunk[len(chunk) -1])
                temp_base = "a" + uuid.uuid4().get_hex()[:6] + "a"
                temp_fc = r"%s\%s" % (scratchGDB(), temp_base)
                temp_fc = self.query(where=sql,
                                     returnFeatureClass=True,
                                     out_fc=temp_fc)
                result_features.append(temp_fc)
            return merge_feature_class(merges=result_features,
                                       out_fc=out_path)
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
        if self._token is not None:
            params['token'] = self._token
        if isinstance(features, Feature):
            params['features'] = json.dumps([features.asDictionary])
        elif isinstance(features, list):
            vals = []
            for feature in features:
                if isinstance(feature, Feature):
                    vals.append(feature.asDictionary)
            params['features'] = json.dumps(vals)
        else:
            return {'message' : "invalid inputs"}
        updateURL = self._url + "/updateFeatures"
        res = self._do_post(url=updateURL,
                            param_dict=params, proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
        return res
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
        if not self._token is None:
            params['token'] = self._token
           
        result = self._do_post(url=dURL, param_dict=params, proxy_port=self._proxy_port,
                               proxy_url=self._proxy_url)
        
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
                            features should be common.Feature objects
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
        if self._token is not None:
            params['token'] = self._token
        if len(addFeatures) > 0 and \
           isinstance(addFeatures[0], Feature):
            params['adds'] = json.dumps([f.asDictionary for f in addFeatures],
                                        default=_date_handler)
        if len(updateFeatures) > 0 and \
           isinstance(updateFeatures[0], Feature):
            params['updates'] = json.dumps([f.asDictionary for f in updateFeatures],
                                           default=_date_handler)
        if deleteFeatures is not None and \
           isinstance(deleteFeatures, str):
            params['deletes'] = deleteFeatures
        return self._do_post(url=editURL, param_dict=params, proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
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
        if self._token is not None:
            params['token'] = self._token
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if isinstance(rollbackOnFailure, bool):
            params['rollbackOnFailure'] = rollbackOnFailure
        if isinstance(features, list):
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
    def addFeatures(self, fc, attachmentTable=None,
                    nameField="ATT_NAME", blobField="DATA",
                    contentTypeField="CONTENT_TYPE",
                    rel_object_field="REL_OBJECTID"):
        """ adds a feature to the feature service
           Inputs:
              fc - string - path to feature class data to add.
              attachmentTable - string - (optional) path to attachment table
              nameField - string - (optional) name of file field in attachment table
              blobField - string - (optional) name field containing blob data
              contentTypeField - string - (optional) name of field containing content type
              rel_object_field - string - (optional) name of field with OID of feature class
           Output:
              boolean, add results message as list of dictionaries

        """
        messages = {'addResults':None}
        if attachmentTable is None:
            count = 0
            bins = 1
            uURL = self._url + "/addFeatures"
            max_chunk = 250
            js = json.loads(self._unicode_convert(
                 featureclass_to_json(fc)))
           
            js = js['features']
            if len(js) == 0:
                return {'addResults':None}
            if len(js) <= max_chunk:
                bins = 1
            else:
                bins = int(len(js)/max_chunk)
                if len(js) % max_chunk > 0:
                    bins += 1
            chunks = self._chunks(l=js, n=bins)
            for chunk in chunks:
                params = {
                    "f" : 'json',
                    "features"  : json.dumps(chunk,
                                             default=self._date_handler)
                }
                if not self._token is None:
                    params['token'] = self._token
                result = self._do_post(url=uURL, param_dict=params, proxy_port=self._proxy_port,
                                       proxy_url=self._proxy_url)
                messages.update(result)
                
                del params
                del result
            return messages
        else:
            oid_field = get_OID_field(fc)
            OIDs = get_records_with_attachments(attachment_table=attachmentTable)
            fl = create_feature_layer(fc, "%s not in ( %s )" % (oid_field, ",".join(OIDs)))
            result = self.addFeatures(fl)
            if result is not None:
                messages.update(result)
            #messages.append(msgs)
            del fl
            for oid in OIDs:
                fl = create_feature_layer(fc, "%s = %s" % (oid_field, oid), name="layer%s" % oid)
                msgs = self.addFeatures(fl)
                for result in msgs['addResults']:
                    oid_fs = result['objectId']
                    sends = get_attachment_data(attachmentTable, sql="%s = %s" % (rel_object_field, oid))
                    result['addAttachmentResults'] = []
                    for s in sends:
                        attRes = self.addAttachment(oid_fs, s['blob'])
                     
                        if 'addAttachmentResult' in attRes:
                            attRes['addAttachmentResult']['AttachmentName'] = s['name']
                            result['addAttachmentResults'].append(attRes['addAttachmentResult'])
                        else:
                            attRes['AttachmentName'] = s['name']
                            result['addAttachmentResults'].append(attRes)                            
                        #messages.append(self.addAttachment(oid_fs, s['blob']))
                        del s
                    del sends
                    del result
                messages.update( msgs)
                del fl
                del oid
            del OIDs
            return messages


########################################################################
class TableLayer(FeatureLayer):
    """Table object is exactly like FeatureLayer object"""
    pass