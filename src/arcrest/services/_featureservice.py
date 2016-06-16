"""

.. module:: _featureservice.py
   :platform: Windows, Linux
   :synopsis: Represents functions/classes used to control Feature Services
              and Feature Layer

.. moduleauthor:: Esri

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import os
import json
from re import search
from ._uploads import Uploads
from ..common.util import _date_handler
from ..common.geometry import SpatialReference
from ..common._filters import *
from ..common.packages import six
from ..common._spatial import scratchFolder, scratchGDB, json_to_featureclass
from ..common.util import create_uid
from ..common.packages.six.moves.urllib_parse import urlparse
from ..common._base import BaseService
from ..common._featureset import FeatureSet
from ..portalmanager.hostedservice import AdminFeatureService, AdminFeatureServiceLayer
########################################################################
class FeatureService(BaseService):
    """ contains information about a feature service """
    _url = None
    _con = None
    _json_dict = None
    _layers = None
    _tables = None
    _initialExtent = None
    _supportsApplyEditsWithGlobalIds = None
    _spatialReference = None
    _capabilities = None
    _currentVersion = None
    _hasStaticData = None
    _units = None
    _xssPreventionInfo = None
    _supportedQueryFormats = None
    _maxRecordCount = None
    _allowGeometryUpdates = None
    _description = None
    _hasVersionedData = None
    _fullExtent = None
    _serviceDescription = None
    _editorTrackingInfo = None
    _supportsDisconnectedEditing = None
    _copyrightText = None
    _syncEnabled = None
    _serviceItemId = None
    #----------------------------------------------------------------------
    @property
    def administration(self):
        """accesses the administration service"""
        url = self._url
        res = search("/rest/", url).span()
        addText = "admin/"
        part1 = url[:res[1]]
        part2 = url[res[1]:]
        adminURL = "%s%s%s" % (part1, addText, part2)

        res = AdminFeatureService(url=adminURL,
                                  connection=self._con,
                                  initialize=True)
        return res
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """gets the initialExtent value"""
        if self._initialExtent is None:
            self.init()
        return self._initialExtent
    #--------------------------------------------------------------------------
    @property
    def supportsApplyEditsWithGlobalIds(self):
        """gets the supportsApplyEditsWithGlobalIds value"""
        if self._supportsApplyEditsWithGlobalIds is None:
            self.init()
        return self._supportsApplyEditsWithGlobalIds
    #--------------------------------------------------------------------------
    @property
    def spatialReference(self):
        """gets the spatialReference value"""
        if self._spatialReference is None:
            self.init()
        return self._spatialReference
    #--------------------------------------------------------------------------
    @property
    def capabilities(self):
        """gets the capabilities value"""
        if self._capabilities is None:
            self.init()
        return self._capabilities
    #--------------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the currentVersion value"""
        if self._currentVersion is None:
            self.init()
        return self._currentVersion
    #--------------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """gets the hasStaticData value"""
        if self._hasStaticData is None:
            self.init()
        return self._hasStaticData
    #--------------------------------------------------------------------------
    @property
    def units(self):
        """gets the units value"""
        if self._units is None:
            self.init()
        return self._units
    #--------------------------------------------------------------------------
    @property
    def xssPreventionInfo(self):
        """gets the xssPreventionInfo value"""
        if self._xssPreventionInfo is None:
            self.init()
        return self._xssPreventionInfo
    #--------------------------------------------------------------------------
    @property
    def supportedQueryFormats(self):
        """gets the supportedQueryFormats value"""
        if self._supportedQueryFormats is None:
            self.init()
        return self._supportedQueryFormats
    #--------------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """gets the maxRecordCount value"""
        if self._maxRecordCount is None:
            self.init()
        return self._maxRecordCount
    #--------------------------------------------------------------------------
    @property
    def allowGeometryUpdates(self):
        """gets the allowGeometryUpdates value"""
        if self._allowGeometryUpdates is None:
            self.init()
        return self._allowGeometryUpdates
    #--------------------------------------------------------------------------
    @property
    def description(self):
        """gets the description value"""
        if self._description is None:
            self.init()
        return self._description
    #--------------------------------------------------------------------------
    @property
    def hasVersionedData(self):
        """gets the hasVersionedData value"""
        if self._hasVersionedData is None:
            self.init()
        return self._hasVersionedData
    #--------------------------------------------------------------------------
    @property
    def fullExtent(self):
        """gets the fullExtent value"""
        if self._fullExtent is None:
            self.init()
        return self._fullExtent
    #--------------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """gets the serviceDescription value"""
        if self._serviceDescription is None:
            self.init()
        return self._serviceDescription
    #--------------------------------------------------------------------------
    @property
    def editorTrackingInfo(self):
        """gets the editorTrackingInfo value"""
        if self._editorTrackingInfo is None:
            self.init()
        return self._editorTrackingInfo
    #--------------------------------------------------------------------------
    @property
    def supportsDisconnectedEditing(self):
        """gets the supportsDisconnectedEditing value"""
        if self._supportsDisconnectedEditing is None:
            self.init()
        return self._supportsDisconnectedEditing
    #--------------------------------------------------------------------------
    @property
    def copyrightText(self):
        """gets the copyrightText value"""
        if self._copyrightText is None:
            self.init()
        return self._copyrightText
    #--------------------------------------------------------------------------
    @property
    def syncEnabled(self):
        """gets the syncEnabled value"""
        if self._syncEnabled is None:
            self.init()
        return self._syncEnabled
    #--------------------------------------------------------------------------
    @property
    def serviceItemId(self):
        """gets the serviceItemId value"""
        if self._serviceItemId is None:
            self.init()
        return self._serviceItemId
    #----------------------------------------------------------------------
    def refresh(self):
        """reloads all the services properties"""
        self.init(connection=self._con)
    #----------------------------------------------------------------------
    def __str__(self):
        """object as string"""
        if self._json_dict is None:
            self.init(connection=self._con)
        return json.dumps(self._json_dict)
    #----------------------------------------------------------------------
    def __repr__(self):
        """representation object"""
        return "{classtype}({data})".format(
            classtype=self.__class__.__name__,
            data=self.__str__())
    #----------------------------------------------------------------------
    def __iter__(self):
        """creates iterable for classes properties"""
        for k,v in self.__dict__.items():
            yield k,v
    #----------------------------------------------------------------------
    def refresh_service(self):
        """ repopulates the properties of the service """
        self._tables = None
        self._layers = None
        self.init()
    #----------------------------------------------------------------------
    @property
    def uploads(self):
        """returns the class to perform the upload function.  it will
        only return the uploads class if syncEnabled is True.
        """
        if self.syncEnabled == True:
            return Uploads(connection=self._con,
                           url=self._url + "/uploads")
        return None
    #----------------------------------------------------------------------
    #def _load_layers(self):
        #""" gets layers for the featuer service """
        #self._layers = []
        #self._tables = []
        #if self._json_dict is None:
            #self.init(connection=self._con)
        #json_dict = self._json_dict
        #if isinstance(json_dict, dict) and \
           #json_dict.has_key("layers"):
            #for l in json_dict['layers']:
                #self._layers.append(FeatureLayer(connection=self._con,
                                                 #url=self._url + "/%s" % l['id'],
                                                 #initialize=True))
                #del l
        #if isinstance(json_dict, dict) and \
           #json_dict.has_key("tables"):
            #for l in json_dict['tables']:
                #self._tables.append(TableLayer(connection=self._con,
                                               #url=self._url + "/%s" % l['id'],
                                               #initialize=True))
                #del l
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """gets the layers value"""
        lyrs = []
        if self._layers is None:
            self.init()
        for layer in self._layers:
            if "id" in layer:
                layer_id = layer['id']
                url = "{url}/{id}".format(url=self._url, id=layer_id)
                layer_type = self._get_layer_type(layer_id=layer['id'])
                if layer_type == "Feature Layer":
                    lyrs.append(FeatureLayer(url=url,connection=self._con))
                elif layer_type == "Raster Layer":
                    lyrs.append(RasterLayer(url=url,connection=self._con))
                elif layer_type == "Group Layer":
                    lyrs.append(GroupLayer(url=url,connection=self._con))
            del layer
        return lyrs
    #----------------------------------------------------------------------
    @property
    def tables(self):
        """gets the tables value"""
        lyrs = []
        if self._tables is None:
            self.init()
        for layer in self._tables:
            url = "{url}/{id}".format(url=self._url, id=layer['id'])
            layer_type = self._get_layer_type(layer_id=layer['id'])
            if layer_type == "Table Layer":
                lyrs.append(TableLayer(url=url, connection=self._con))
            elif layer_type == "Group Layer":
                lyrs.append(GroupLayer(url=url, connection=self._con))
        return lyrs
    #----------------------------------------------------------------------
    def _get_layer_type(self, layer_id):
        url = "{url}/{id}".format(url=self._url, id=layer_id)
        params = {"f": "json"}
        res = self._con.get(path_or_url=url, params=params)
        return res['type']
    #----------------------------------------------------------------------
    def query(self,
              layerDefsFilter=None,
              geometryFilter=None,
              timeFilter=None,
              returnGeometry=True,
              returnIdsOnly=False,
              returnCountOnly=False,
              returnZ=False,
              returnM=False,
              outSR=None
              ):
        """
           The Query operation is performed on a feature service resource
        """
        qurl = self._url + "/query"
        params = {"f": "json",
                  "returnGeometry": returnGeometry,
                  "returnIdsOnly": returnIdsOnly,
                  "returnCountOnly": returnCountOnly,
                  "returnZ": returnZ,
                  "returnM" : returnM}
        if not layerDefsFilter is None and \
           isinstance(layerDefsFilter, dict):
            params['layerDefs'] = layerDefsFilter
        elif not layerDefsFilter is None and \
             isinstance(layerDefsFilter, dict):
            pass
        if not geometryFilter is None and \
           isinstance(geometryFilter, dict):
            gf = geometryFilter
            params['geometryType'] = gf['geometryType']
            params['spatialRel'] = gf['spatialRel']
            params['geometry'] = gf['geometry']
            params['inSR'] = gf['inSR']
        if not outSR is None and \
           isinstance(outSR, SpatialReference):
            params['outSR'] = outSR.as_dict
        elif not outSR is None and \
             isinstance(outSR, dict):
            params['outSR'] = outSR
        if not timeFilter is None and \
           isinstance(timeFilter, dict):
            params['time'] = timeFilter
        res =  self._con.get(path_or_url=qurl,
                             params=params)
        return res
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
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if definitionExpression is not None:
            params['definitionExpression'] = definitionExpression
        if outWKID is not None and \
           isinstance(outWKID, SpatialReference):
            params['outSR'] = outWKID.as_dict
        elif outWKID is not None and \
             isinstance(outWKID, dict):
            params['outSR'] = outWKID
        if maxAllowableOffset is not None:
            params['maxAllowableOffset'] = maxAllowableOffset
        if geometryPrecision is not None:
            params['geometryPrecision'] = geometryPrecision
        quURL = self._url + "/queryRelatedRecords"
        res = self._con.get(path_or_url=quURL, params=params)
        return res
    #----------------------------------------------------------------------
    @property
    def replicas(self):
        """ returns all the replicas for a feature service """
        params = {
            "f" : "json",

        }
        url = self._url + "/replicas"
        return self._con.get(path_or_url=url, params=params)
    #----------------------------------------------------------------------
    def unRegisterReplica(self, replica_id):
        """
           removes a replica from a feature service
           Inputs:
             replica_id - The replicaID returned by the feature service
                          when the replica was created.
        """
        params = {
            "f" : "json",
            "replicaID" : replica_id
        }
        url = self._url + "/unRegisterReplica"
        return self._con.post(path_or_url=url, postdata=params)
    #----------------------------------------------------------------------
    def replicaInfo(self, replica_id):
        """
           The replica info resources lists replica metadata for a specific
           replica.
           Inputs:
              replica_id - The replicaID returned by the feature service
                           when the replica was created.
        """
        params = {
            "f" : "json"
        }
        url = self._url + "/replicas/" + replica_id
        return self._con.get(path_or_url=url, params=params)
    #----------------------------------------------------------------------
    def createReplica(self,
                      replicaName,
                      layers,
                      layerQueries=None,
                      geometryFilter=None,
                      replicaSR=None,
                      transportType="esriTransportTypeUrl",
                      returnAttachments=False,
                      returnAttachmentsDatabyURL=False,
                      async=False,
                      attachmentsSyncDirection="none",
                      syncModel="none",
                      dataFormat="json",
                      replicaOptions=None,
                      wait=False,
                      out_path=None):
        """
        The createReplica operation is performed on a feature service
        resource. This operation creates the replica between the feature
        service and a client based on a client-supplied replica definition.
        It requires the Sync capability. See Sync overview for more
        information on sync. The response for createReplica includes
        replicaID, server generation number, and data similar to the
        response from the feature service query operation.
        The createReplica operation returns a response of type
        esriReplicaResponseTypeData, as the response has data for the
        layers in the replica. If the operation is called to register
        existing data by using replicaOptions, the response type will be
        esriReplicaResponseTypeInfo, and the response will not contain data
        for the layers in the replica.

        Inputs:
           replicaName - name of the replica
           layers - layers to export
           layerQueries - In addition to the layers and geometry parameters, the layerQueries
            parameter can be used to further define what is replicated. This
            parameter allows you to set properties on a per layer or per table
            basis. Only the properties for the layers and tables that you want
            changed from the default are required.
            Example:
             layerQueries = {"0":{"queryOption": "useFilter", "useGeometry": true,
             "where": "requires_inspection = Yes"}}
           geometryFilter - Geospatial filter applied to the replica to
            parse down data output.
           returnAttachments - If true, attachments are added to the replica and returned in the
            response. Otherwise, attachments are not included.
           returnAttachmentDatabyURL -  If true, a reference to a URL will be provided for each
            attachment returned from createReplica. Otherwise,
            attachments are embedded in the response.
           replicaSR - the spatial reference of the replica geometry.
           transportType -  The transportType represents the response format. If the
            transportType is esriTransportTypeUrl, the JSON response is contained in a file,
            and the URL link to the file is returned. Otherwise, the JSON object is returned
            directly. The default is esriTransportTypeUrl.
            If async is true, the results will always be returned as if transportType is
            esriTransportTypeUrl. If dataFormat is sqlite, the transportFormat will always be
            esriTransportTypeUrl regardless of how the parameter is set.
            Values: esriTransportTypeUrl | esriTransportTypeEmbedded
           returnAttachments - If true, attachments are added to the replica and returned in
            the response. Otherwise, attachments are not included. The default is false. This
            parameter is only applicable if the feature service has attachments.
           returnAttachmentsDatabyURL -  If true, a reference to a URL will be provided for
            each attachment returned from createReplica. Otherwise, attachments are embedded
            in the response. The default is true. This parameter is only applicable if the
            feature service has attachments and if returnAttachments is true.
           attachmentsSyncDirection - Client can specify the attachmentsSyncDirection when
            creating a replica. AttachmentsSyncDirection is currently a createReplica property
            and cannot be overridden during sync.
            Values: none, upload, bidirectional
           async - If true, the request is processed as an asynchronous job, and a URL is
            returned that a client can visit to check the status of the job. See the topic on
            asynchronous usage for more information. The default is false.
           syncModel - Client can specify the attachmentsSyncDirection when creating a replica.
            AttachmentsSyncDirection is currently a createReplica property and cannot be
            overridden during sync.
           dataFormat - The format of the replica geodatabase returned in the response. The
            default is json.
            Values: filegdb, json, sqlite, shapefile
           replicaOptions - This parameter instructs the createReplica operation to create a
            new replica based on an existing replica definition (refReplicaId). It can be used
            to specify parameters for registration of existing data for sync. The operation
            will create a replica but will not return data. The responseType returned in the
            createReplica response will be esriReplicaResponseTypeInfo.
           wait - if async, wait to pause the process until the async operation is completed.
           out_path - folder path to save the file
        """
        if hasattr(self, "syncEnabled") and \
           hasattr(self, "capabilities") and \
           getattr(self, "syncEnabled") == False and \
           "Extract" not in getattr(self,"capabilities"):
            return None
        url = self._url + "/createReplica"
        dataformat = ["filegdb", "json", "sqlite", "shapefile"]
        params = {"f" : "json",
                  "replicaName": replicaName,
                  "returnAttachments": returnAttachments,
                  "returnAttachmentsDatabyURL": returnAttachmentsDatabyURL,
                  "attachmentsSyncDirection" : attachmentsSyncDirection,
                  "async" : async,
                  "syncModel" : syncModel,
                  "layers" : layers
                  }
        if dataFormat.lower() in dataformat:
            params['dataFormat'] = dataFormat.lower()
        else:
            raise Exception("Invalid dataFormat")
        if layerQueries is not None:
            params['layerQueries'] = layerQueries
        if geometryFilter is not None and \
           isinstance(geometryFilter, dict):
            params.update(geometryFilter)
        if replicaSR is not None:
            params['replicaSR'] = replicaSR
        if replicaOptions is not None:
            params['replicaOptions'] = replicaOptions
        if transportType is not None:
            params['transportType'] = transportType

        if async:
            if wait:
                exportJob = self._con.post(path_or_url=url,
                                           postdata=params)
                status = self.replicaStatus(url=exportJob['statusUrl'])
                while status['status'].lower() != "completed":
                    status = self.replicaStatus(url=exportJob['statusUrl'])
                    if status['status'].lower() == "failed":
                        return status

                res = status

            else:
                res = self._con.post(path_or_url=url,
                                     postdata=params)
        else:
            res = self._con.post(path_or_url=url,
                                 postdata=params)


        if out_path is not None and \
           os.path.isdir(out_path):
            dlURL = None
            if 'resultUrl' in res:

                dlURL = res["resultUrl"]
            elif 'responseUrl' in res:
                dlURL = res["responseUrl"]
            if dlURL is not None:
                return self._con.get(path_or_url=dlURL,
                                     out_folder=out_path)
            else:
                return res
        elif res is not None:
            return res
        return None
    #----------------------------------------------------------------------
    def synchronizeReplica(self,
                           replicaID,
                           transportType="esriTransportTypeUrl",
                           replicaServerGen=None,
                           returnIdsForAdds=False,
                           edits=None,
                           returnAttachmentDatabyURL=False,
                           async=False,
                           syncDirection="snapshot",
                           syncLayers="perReplica",
                           editsUploadID=None,
                           editsUploadFormat=None,
                           dataFormat="json",
                           rollbackOnFailure=True):
        """
        TODO: implement synchronize replica
        http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#//02r3000000vv000000
        """
        url = "{url}/synchronizeReplica".format(url=self._url)
        params = {
            "f" : "json",
            "replicaID" : replicaID,
        }
        if not transportType is None:
            params['transportType'] = transportType
        if not edits is None:
            params['edits'] = edits
        if not replicaServerGen is None:
            params['replicaServerGen'] = replicaServerGen
        if not returnIdsForAdds is None:
            params['returnIdsForAdds'] = returnIdsForAdds
        if not returnAttachmentDatabyURL is None:
            params['returnAttachmentDatabyURL'] = returnAttachmentDatabyURL
        if not async is None:
            params['async'] = async
        if not syncDirection is None:
            params['syncDirection'] = syncDirection
        if not syncLayers is None:
            params['syncLayers'] = syncLayers
        if not editsUploadFormat is None:
            params['editsUploadFormat'] = editsUploadFormat
        if not editsUploadID is None:
            params['editsUploadID'] = editsUploadID
        if not dataFormat is None:
            params['dataFormat'] = dataFormat
        if not rollbackOnFailure is None:
            params['rollbackOnFailure'] = rollbackOnFailure
        return self._con.post(path_or_url=url, postdata=params)
    #----------------------------------------------------------------------
    def replicaStatus(self, url):
        """gets the replica status when exported async set to True"""
        params = {"f" : "json"}
        url = url + "/status"
        return self._con.get(path_or_url=url,
                             params=params)
########################################################################
class FeatureLayer(BaseService):
    """
       This contains information about a feature service's layer.
    """
    _con = None
    _url = None
    _json_dict = None
    _supportsCalculate = None
    _editingInfo = None
    _typeIdField = None
    _supportsValidateSql = None
    _advancedQueryCapabilities = None
    _supportsCoordinatesQuantization = None
    _supportsRollbackOnFailureParameter = None
    _allowGeometryUpdates = None
    _globalIdField = None
    _supportsAdvancedQueries = None
    _id = None
    _relationships = None
    _drawingInfo = None
    _capabilities = None
    _indexes = None
    _currentVersion = None
    _geometryType = None
    _hasStaticData = None
    _type = None
    _useStandardizedQueries = None
    _supportedQueryFormats = None
    _isDataVersioned = None
    _supportsAttachmentsByUploadId = None
    _supportsApplyEditsWithGlobalIds = None
    _description = None
    _standardMaxRecordCount = None
    _defaultVisibility = None
    _extent = None
    _objectIdField = None
    _tileMaxRecordCount = None
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
    _maxRecordCountFactor = None
    _serviceItemId = None
    def __str__(self):
        """object as string"""
        if self._json_dict is None:
            self.init()
        return json.dumps(self._json_dict)
    #----------------------------------------------------------------------
    @property
    def administration(self):
        """accesses the administration service"""
        url = self._url
        res = search("/rest/", url).span()
        addText = "admin/"
        part1 = url[:res[1]]
        part2 = url[res[1]:]
        adminURL = "%s%s%s" % (part1, addText, part2)

        res = AdminFeatureServiceLayer(url=adminURL,
                                       connection=self._con,
                                       initialize=True)
        return res
    #----------------------------------------------------------------------
    @property
    def supportsCalculate(self):
        """gets the supportsCalculate value"""
        if self._supportsCalculate is None:
            self.init()
        return self._supportsCalculate
    #----------------------------------------------------------------------
    @property
    def editingInfo(self):
        """gets the editingInfo value"""
        if self._editingInfo is None:
            self.init()
        return self._editingInfo
    #----------------------------------------------------------------------
    @property
    def typeIdField(self):
        """gets the typeIdField value"""
        if self._typeIdField is None:
            self.init()
        return self._typeIdField
    #----------------------------------------------------------------------
    @property
    def supportsValidateSql(self):
        """gets the supportsValidateSql value"""
        if self._supportsValidateSql is None:
            self.init()
        return self._supportsValidateSql
    #----------------------------------------------------------------------
    @property
    def advancedQueryCapabilities(self):
        """gets the advancedQueryCapabilities value"""
        if self._advancedQueryCapabilities is None:
            self.init()
        return self._advancedQueryCapabilities
    #----------------------------------------------------------------------
    @property
    def supportsCoordinatesQuantization(self):
        """gets the supportsCoordinatesQuantization value"""
        if self._supportsCoordinatesQuantization is None:
            self.init()
        return self._supportsCoordinatesQuantization
    #----------------------------------------------------------------------
    @property
    def supportsRollbackOnFailureParameter(self):
        """gets the supportsRollbackOnFailureParameter value"""
        if self._supportsRollbackOnFailureParameter is None:
            self.init()
        return self._supportsRollbackOnFailureParameter
    #----------------------------------------------------------------------
    @property
    def allowGeometryUpdates(self):
        """gets the allowGeometryUpdates value"""
        if self._allowGeometryUpdates is None:
            self.init()
        return self._allowGeometryUpdates
    #----------------------------------------------------------------------
    @property
    def globalIdField(self):
        """gets the globalIdField value"""
        if self._globalIdField is None:
            self.init()
        return self._globalIdField
    #----------------------------------------------------------------------
    @property
    def supportsAdvancedQueries(self):
        """gets the supportsAdvancedQueries value"""
        if self._supportsAdvancedQueries is None:
            self.init()
        return self._supportsAdvancedQueries
    #----------------------------------------------------------------------
    @property
    def id(self):
        """gets the id value"""
        if self._id is None:
            self.init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def relationships(self):
        """gets the relationships value"""
        if self._relationships is None:
            self.init()
        return self._relationships
    #----------------------------------------------------------------------
    @property
    def drawingInfo(self):
        """gets the drawingInfo value"""
        if self._drawingInfo is None:
            self.init()
        return self._drawingInfo
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """gets the capabilities value"""
        if self._capabilities is None:
            self.init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def indexes(self):
        """gets the indexes value"""
        if self._indexes is None:
            self.init()
        return self._indexes
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the currentVersion value"""
        if self._currentVersion is None:
            self.init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """gets the geometryType value"""
        if self._geometryType is None:
            self.init()
        return self._geometryType
    #----------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """gets the hasStaticData value"""
        if self._hasStaticData is None:
            self.init()
        return self._hasStaticData
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the type value"""
        if self._type is None:
            self.init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def useStandardizedQueries(self):
        """gets the useStandardizedQueries value"""
        if self._useStandardizedQueries is None:
            self.init()
        return self._useStandardizedQueries
    #----------------------------------------------------------------------
    @property
    def supportedQueryFormats(self):
        """gets the supportedQueryFormats value"""
        if self._supportedQueryFormats is None:
            self.init()
        return self._supportedQueryFormats
    #----------------------------------------------------------------------
    @property
    def isDataVersioned(self):
        """gets the isDataVersioned value"""
        if self._isDataVersioned is None:
            self.init()
        return self._isDataVersioned
    #----------------------------------------------------------------------
    @property
    def supportsAttachmentsByUploadId(self):
        """gets the supportsAttachmentsByUploadId value"""
        if self._supportsAttachmentsByUploadId is None:
            self.init()
        return self._supportsAttachmentsByUploadId
    #----------------------------------------------------------------------
    @property
    def supportsApplyEditsWithGlobalIds(self):
        """gets the supportsApplyEditsWithGlobalIds value"""
        if self._supportsApplyEditsWithGlobalIds is None:
            self.init()
        return self._supportsApplyEditsWithGlobalIds
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets the description value"""
        if self._description is None:
            self.init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def standardMaxRecordCount(self):
        """gets the standardMaxRecordCount value"""
        if self._standardMaxRecordCount is None:
            self.init()
        return self._standardMaxRecordCount
    #----------------------------------------------------------------------
    @property
    def defaultVisibility(self):
        """gets the defaultVisibility value"""
        if self._defaultVisibility is None:
            self.init()
        return self._defaultVisibility
    #----------------------------------------------------------------------
    @property
    def extent(self):
        """gets the extent value"""
        if self._extent is None:
            self.init()
        return self._extent
    #----------------------------------------------------------------------
    @property
    def objectIdField(self):
        """gets the objectIdField value"""
        if self._objectIdField is None:
            self.init()
        return self._objectIdField
    #----------------------------------------------------------------------
    @property
    def tileMaxRecordCount(self):
        """gets the tileMaxRecordCount value"""
        if self._tileMaxRecordCount is None:
            self.init()
        return self._tileMaxRecordCount
    #----------------------------------------------------------------------
    @property
    def htmlPopupType(self):
        """gets the htmlPopupType value"""
        if self._htmlPopupType is None:
            self.init()
        return self._htmlPopupType
    #----------------------------------------------------------------------
    @property
    def types(self):
        """gets the types value"""
        if self._types is None:
            self.init()
        return self._types
    #----------------------------------------------------------------------
    @property
    def hasM(self):
        """gets the hasM value"""
        if self._hasM is None:
            self.init()
        return self._hasM
    #----------------------------------------------------------------------
    @property
    def displayField(self):
        """gets the displayField value"""
        if self._displayField is None:
            self.init()
        return self._displayField
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets the name value"""
        if self._name is None:
            self.init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def templates(self):
        """gets the templates value"""
        if self._templates is None:
            self.init()
        return self._templates
    #----------------------------------------------------------------------
    @property
    def supportsStatistics(self):
        """gets the supportsStatistics value"""
        if self._supportsStatistics is None:
            self.init()
        return self._supportsStatistics
    #----------------------------------------------------------------------
    @property
    def hasAttachments(self):
        """gets the hasAttachments value"""
        if self._hasAttachments is None:
            self.init()
        return self._hasAttachments
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """gets the fields value"""
        if self._fields is None:
            self.init()
        return self._fields
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """gets the maxScale value"""
        if self._maxScale is None:
            self.init()
        return self._maxScale
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """gets the copyrightText value"""
        if self._copyrightText is None:
            self.init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def hasZ(self):
        """gets the hasZ value"""
        if self._hasZ is None:
            self.init()
        return self._hasZ
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """gets the maxRecordCount value"""
        if self._maxRecordCount is None:
            self.init()
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """gets the minScale value"""
        if self._minScale is None:
            self.init()
        return self._minScale
    #----------------------------------------------------------------------
    @property
    def maxRecordCountFactor(self):
        """gets the maxRecordCountFactor value"""
        if self._maxRecordCountFactor is None:
            self.init()
        return self._maxRecordCountFactor
    #----------------------------------------------------------------------
    @property
    def serviceItemId(self):
        """gets the serviceItemId value"""
        if self._serviceItemId is None:
            self.init()
        return self._serviceItemId
    #----------------------------------------------------------------------
    def refresh(self):
        """refreshes all the properties of the service"""
        self._json_dict = None
        self.init(self._con)
    #----------------------------------------------------------------------
    def addAttachment(self, oid, file_path):
        """ Adds an attachment to a feature service
            Input:
              oid - string - OBJECTID value to add attachment to
              file_path - string - path to file
            Output:
              JSON Repsonse
        """
        if hasattr(self, "hasAttachments") and \
           getattr(self, "hasAttachments") == True:
            attachURL = self._url + "/%s/addAttachment" % oid
            params = {'f':'json'}

            files = {'attachment': file_path}
            res = self._con.post(path_or_url=attachURL,
                                 postdata=params,
                                 files=files)
            return res
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
        return self._con.post(url, params)
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
        files = {'attachment': file_path }
        res = self._con.post(path_or_url=url,
                             postdata=params,
                             files=files)
        return res
    #----------------------------------------------------------------------
    def listAttachments(self, oid):
        """ list attachements for a given OBJECT ID """
        url = self._url + "/%s/attachments" % oid
        params = {
            "f":"json"
        }
        return self._con.get(path_or_url=url, params=params)
    #----------------------------------------------------------------------
    def query(self,
              where="1=1",
              out_fields="*",
              timeFilter=None,
              geomtryFilter=None,
              returnGeometry=True,
              returnCountOnly=False,
              returnIDsOnly=False,
              returnFeatureClass=False,
              returnDistinctValues=False,
              returnExtentOnly=False,
              groupByFieldsForStatistics=None,
              statisticFilter=None,
              resultOffset=None,
              resultRecordCount=None,
              out_fc=None,
              objectIds=None,
              distance=None,
              units=None,
              maxAllowableOffset=None,
              outSR=None,
              geometryPrecision=None,
              gdbVersion=None,
              orderByFields=None,
              outStatistics=None,
              returnZ=False,
              returnM=False,
              multipatchOption=None,
              quanitizationParameters=None,
              returnCentroid=False,
              as_json=False,
              **kwargs):
        """ queries a feature service based on a sql statement
            Inputs:
                where - the selection sql statement
                out_fields - the attribute fields to return
                objectIds -  The object IDs of this layer or table to be
                            queried.
                distance - The buffer distance for the input geometries.
                          The distance unit is specified by units. For
                          example, if the distance is 100, the query
                          geometry is a point, units is set to meters, and
                          all points within 100 meters of the point are
                          returned.
                units - The unit for calculating the buffer distance. If
                        unit is not specified, the unit is derived from the
                        geometry spatial reference. If the geometry spatial
                        reference is not specified, the unit is derived
                        from the feature service data spatial reference.
                        This parameter only applies if
                        supportsQueryWithDistance is true.
                        Values: esriSRUnit_Meter | esriSRUnit_StatuteMile |
                        esriSRUnit_Foot | esriSRUnit_Kilometer |
                        esriSRUnit_NauticalMile | esriSRUnit_USNauticalMile
                timeFilter - a TimeFilter object where either the start time
                            or start and end time are defined to limit the
                            search results for a given time.  The values in
                            the timeFilter should be as UTC timestampes in
                            milliseconds.  No checking occurs to see if they
                            are in the right format.
                geometryFilter - a GeometryFilter object to parse down a given
                               query by another spatial dataset.
                maxAllowableOffset - This option can be used to specify the
                                     maxAllowableOffset to be used for
                                     generalizing geometries returned by
                                     the query operation.
                                     The maxAllowableOffset is in the units
                                     of outSR. If outSR is not specified,
                                     maxAllowableOffset is assumed to be in
                                     the unit of the spatial reference of
                                     the map.
                outSR - The spatial reference of the returned geometry.
                geometryPrecision -  This option can be used to specify the
                                     number of decimal places in the
                                     response geometries returned by the
                                     Query operation.
                gdbVersion - Geodatabase version to query
                returnDistinctValues -  If true, it returns distinct values
                                        based on the fields specified in
                                        outFields. This parameter applies
                                        only if the
                                        supportsAdvancedQueries property of
                                        the layer is true.
                returnIDsOnly -  If true, the response only includes an
                                 array of object IDs. Otherwise, the
                                 response is a feature set. The default is
                                 false.
                returnCountOnly -  If true, the response only includes the
                                   count (number of features/records) that
                                   would be returned by a query. Otherwise,
                                   the response is a feature set. The
                                   default is false. This option supersedes
                                   the returnIdsOnly parameter. If
                                   returnCountOnly = true, the response will
                                   return both the count and the extent.
                returnExtentOnly -  If true, the response only includes the
                                    extent of the features that would be
                                    returned by the query. If
                                    returnCountOnly=true, the response will
                                    return both the count and the extent.
                                    The default is false. This parameter
                                    applies only if the
                                    supportsReturningQueryExtent property
                                    of the layer is true.
                orderByFields - One or more field names on which the
                                features/records need to be ordered. Use
                                ASC or DESC for ascending or descending,
                                respectively, following every field to
                                control the ordering.
                groupByFieldsForStatistics - One or more field names on
                                             which the values need to be
                                             grouped for calculating the
                                             statistics.
                outStatistics - The definitions for one or more field-based
                                statistics to be calculated.
                returnZ -  If true, Z values are included in the results if
                           the features have Z values. Otherwise, Z values
                           are not returned. The default is false.
                returnM - If true, M values are included in the results if
                          the features have M values. Otherwise, M values
                          are not returned. The default is false.
                multipatchOption - This option dictates how the geometry of
                                   a multipatch feature will be returned.
                resultOffset -  This option can be used for fetching query
                                results by skipping the specified number of
                                records and starting from the next record
                                (that is, resultOffset + 1th).
                resultRecordCount - This option can be used for fetching
                                    query results up to the
                                    resultRecordCount specified. When
                                    resultOffset is specified but this
                                    parameter is not, the map service
                                    defaults it to maxRecordCount. The
                                    maximum value for this parameter is the
                                    value of the layer's maxRecordCount
                                    property.
                quanitizationParameters - Used to project the geometry onto
                                          a virtual grid, likely
                                          representing pixels on the screen.
                returnCentroid - Used to return the geometry centroid
                                 associated with each feature returned. If
                                 true, the result includes the geometry
                                 centroid. The default is false.
                as_json - If true, the query will return as the raw JSON.
                          The default is False.
                returnFeatureClass - If true and arcpy is installed, the
                                     script will attempt to save the result
                                     of the query to a feature class.
                out_fc - only valid if returnFeatureClass is set to True.
                         Output location of query. If out_fc is set to None,
                         then the feature class will be saved to the scratch
                         File Geodatabase with a random name.
               kwargs - optional parameters that can be passed to the Query
                 function.  This will allow users to pass additional
                 parameters not explicitly implemented on the function. A
                 complete list of functions available is documented on the
                 Query REST API.
            Output:
               A list of Feature Objects (default) or a path to the output featureclass if
               returnFeatureClass is set to True.
         """
        url = self._url + "/query"
        params = {"f" : "json"}
        params['where'] = where
        params['outFields'] = out_fields
        params['returnGeometry'] = returnGeometry
        params['returnDistinctValues'] = returnDistinctValues
        params['returnCentroid'] = returnCentroid
        params['returnCountOnly'] = returnCountOnly
        params['returnExtentOnly'] = returnExtentOnly
        params['returnIdsOnly'] = returnIDsOnly
        params['returnZ'] = returnZ
        params['returnM'] = returnM
        if resultRecordCount:
            params['resultRecordCount'] = resultRecordCount
        if resultOffset:
            params['resultOffset'] = resultOffset
        if quanitizationParameters:
            params['quanitizationParameters'] = quanitizationParameters
        if multipatchOption:
            params['multipatchOption'] = multipatchOption
        if orderByFields:
            params['orderByFields'] = orderByFields
        if groupByFieldsForStatistics:
            params['groupByFieldsForStatistics'] = groupByFieldsForStatistics
        if statisticFilter and \
           isinstance(statisticFilter, StatisticFilter):
            params['outStatistics'] = statisticFilter.filter
        if outStatistics:
            params['outStatistics'] = outStatistics
        if outSR:
            params['outSR'] = outSR
        if maxAllowableOffset:
            params['maxAllowableOffset'] = maxAllowableOffset
        if gdbVersion:
            params['gdbVersion'] = gdbVersion
        if geometryPrecision:
            params['geometryPrecision'] = geometryPrecision
        if objectIds:
            params['objectIds'] = objectIds
        if distance:
            params['distance'] = distance
        if units:
            params['units'] = units
        if timeFilter and \
           isinstance(timeFilter, TimeFilter):
            for k,v in timeFilter.filter:
                params[k] = v
        elif isinstance(timeFilter, dict):
            for k,v in timeFilter.items():
                params[k] = v
        if geomtryFilter and \
           isinstance(geomtryFilter, GeometryFilter):
            for k,v in geomtryFilter.filter:
                params[k] = v
        elif geomtryFilter and \
             isinstance(geomtryFilter, dict):
            for k,v in geomtryFilter.items():
                params[k] = v
        if len(kwargs) > 0:
            for k,v in kwargs.items():
                params[k] = v
                del k,v

        result = self._con.post(path_or_url=url,
                                postdata=params)
        if 'error' in result:
            raise ValueError(result)
        if as_json or \
           returnCountOnly == True or \
           returnIDsOnly == True:
            return result
        elif returnFeatureClass and\
             not returnCountOnly and \
             not returnIDsOnly:
            uid = create_uid()
            if out_fc is None:
                out_fc = os.path.join(scratchGDB(),
                                      "a{fid}".format(fid=uid))
            text = json.dumps(result)
            temp = scratchFolder() + os.sep + uid + ".json"
            with open(temp, 'wb') as writer:
                if six.PY3:
                    text = bytes(text, 'UTF-8')
                writer.write(text)
                writer.flush()
                del writer
            fc = json_to_featureclass(json_file=temp,
                                      out_fc=out_fc)
            os.remove(temp)
            return fc
        else:
            return FeatureSet.fromJSON(jsonValue=json.dumps(result))
        return result
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
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if definitionExpression is not None:
            params['definitionExpression'] = definitionExpression
        if outWKID is not None and \
           isinstance(outWKID, SpatialReference):
            params['outSR'] = outWKID.as_dict
        elif outWKID is not None and \
             isinstance(outWKID, dict):
            params['outSR'] = outWKID
        if maxAllowableOffset is not None:
            params['maxAllowableOffset'] = maxAllowableOffset
        if geometryPrecision is not None:
            params['geometryPrecision'] = geometryPrecision
        quURL = self._url + "/queryRelatedRecords"
        return self._con.get(path_or_url=quURL, params=params)
    #----------------------------------------------------------------------
    def getHTMLPopup(self, oid):
        """
           The htmlPopup resource provides details about the HTML pop-up
           authored by the user using ArcGIS for Desktop.
           Input:
              oid - object id of the feature where the HTML pop-up
           Output:

        """
        if hasattr(self, "htmlPopupType") and \
           getattr(self, "htmlPopupType") != "esriServerHTMLPopupTypeNone":
            popURL = self._url + "/%s/htmlPopup" % oid
            params = {
                'f' : "json"
            }

            return self._con.get(path_or_url=popURL, params=params)
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
    ##----------------------------------------------------------------------
    #def get_local_copy(self, out_path, includeAttachments=False):
        #""" exports the whole feature service to a feature class
            #Input:
                #out_path - path to where the data will be placed
                #includeAttachments - default False. If sync is not supported
                                    #then the paramter is ignored.
            #Output:
                #path to exported feature class or fgdb (as list)
        #"""
        #if self.hasAttachments and \
            #self.parentLayer.syncEnabled:
            #return self.parentLayer.createReplica(replicaName="fgdb_dump",
                                                    #layers="%s" % self.id,
                                                    #attachmentsSyncDirection="upload",
                                                    #async=True,
                                                    #wait=True,
                                                    #returnAttachments=includeAttachments,
                                                    #out_path=out_path)[0]
        #elif self.hasAttachments == False and \
                #self.parentLayer.syncEnabled:
            #return self.parentLayer.createReplica(replicaName="fgdb_dump",
                                                    #layers="%s" % self.id,
                                                    #attachmentsSyncDirection="upload",
                                                    #async=True,
                                                    #wait=True,
                                                    #returnAttachments=includeAttachments,
                                                    #out_path=out_path)[0]
        #else:
            #result_features = []
            #res = self.query(returnIDsOnly=True)
            #OIDS = res['objectIds']
            #OIDS.sort()
            #OIDField = res['objectIdFieldName']
            #count = len(OIDS)
            #if count <= self.maxRecordCount:
                #bins = 1
            #else:
                #bins = count / self.maxRecordCount
                #v = count % self.maxRecordCount
                #if v > 0:
                    #bins += 1
            #chunks = self._chunks(OIDS, bins)
            #for chunk in chunks:
                #chunk.sort()
                #sql = "%s >= %s and %s <= %s" % (OIDField, chunk[0],
                                                    #OIDField, chunk[len(chunk) -1])
                #temp_base = "a" + uuid.uuid4().get_hex()[:6] + "a"
                #temp_fc = r"%s\%s" % (scratchGDB(), temp_base)
                #temp_fc = self.query(where=sql,
                                        #returnFeatureClass=True,
                                        #out_fc=temp_fc)
                #result_features.append(temp_fc)
            #return merge_feature_class(merges=result_features,
                                        #out_fc=out_path)
    #----------------------------------------------------------------------
    def updateFeature(self,
                      features,
                      gdbVersion=None,
                      rollbackOnFailure=True):
        """
           updates an existing feature in a feature service layer
           Input:
              feature - feature object(s) to get updated.  A single
                        feature, a list of feature objects can be passed,
                        or a FeatureSet object.
           Output:
              dictionary of result messages
        """
        params = {
            "f" : "json",
            "rollbackOnFailure" : rollbackOnFailure
        }
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if isinstance(features, dict):
            params['features'] = json.dumps([features])
        elif isinstance(features, list):
            params['features'] = json.dumps(features)
        else:
            raise ValueError( {'message' : "invalid inputs"})
        updateURL = self._url + "/updateFeatures"
        res = self._con.post(path_or_url=updateURL,
                             postdata=params
                             )
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
        if not rollbackOnFailure is None:
            params['rollbackOnFailure'] = rollbackOnFailure
        if not gdbVersion is None:
            params['gdbVersion'] = gdbVersion
        if geometryFilter is not None and \
           isinstance(geometryFilter, dict):
            gfilter = geometryFilter
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
        result = self._con.post(path_or_url=dURL, postdata=params)

        return result
    #----------------------------------------------------------------------
    def applyEdits(self,
                   addFeatures=None,
                   updateFeatures=None,
                   deleteFeatures=None,
                   gdbVersion=None,
                   useGlobalIds=False,
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
              useGlobalIds - instead of referencing the default Object ID
                              field, the service will look at a GUID field
                              to track changes.  This means the GUIDs will
                              be passed instead of OIDs for delete,
                              update or add features.
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
        if addFeatures is None:
            addFeatures = []
        if updateFeatures is None:
            updateFeatures = []
        editURL = self._url + "/applyEdits"
        params = {"f": "json",
                  "useGlobalIds" : useGlobalIds,
                  "rollbackOnFailure" : rollbackOnFailure
                  }
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if len(addFeatures) > 0 and \
           isinstance(addFeatures[0], dict):
            params['adds'] = json.dumps([f for f in addFeatures],
                                        default=_date_handler)
        if len(updateFeatures) > 0 and \
           isinstance(updateFeatures[0], dict):
            params['updates'] = json.dumps([f for f in updateFeatures],
                                           default=_date_handler)
        if deleteFeatures is not None and \
           isinstance(deleteFeatures, str):
            params['deletes'] = deleteFeatures
        return self._con.post(path_or_url=editURL, postdata=params)
    #----------------------------------------------------------------------
    def addFeature(self, features,
                   gdbVersion=None,
                   rollbackOnFailure=True):
        """ Adds a single feature to the service
           Inputs:
              feature - list of common.Feature object or a single
                        common.Feature Object or a FeatureSet object
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
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if isinstance(rollbackOnFailure, bool):
            params['rollbackOnFailure'] = rollbackOnFailure
        if isinstance(features, list):
            params['features'] = json.dumps(features,
                                            default=_date_handler)
        elif isinstance(features, dict):
            params['features'] = json.dumps([features],
                                            default=_date_handler)
        else:
            raise ValueError("features must be of type list of dictionaries or a dictionary")
        return self._con.post(path_or_url=url,
                              postdata=params)
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
        if sqlFormat.lower() in ['native', 'standard']:
            params['sqlFormat'] = sqlFormat.lower()
        else:
            params['sqlFormat'] = "standard"
        return self._con.post(path_or_url=url,
                              postdata=params)
########################################################################
class TableLayer(FeatureLayer):
    """Table object is exactly like FeatureLayer object"""
    pass
########################################################################
class TiledService(object):
    """
       AGOL Tiled Map Service
    """
    _con = None
    _url = None
    _json_dict = None
########################################################################
class SchematicLayer(FeatureLayer):
    pass
########################################################################
class RasterLayer(FeatureLayer):
    pass
########################################################################
class GroupLayer(FeatureLayer):
    pass
########################################################################
