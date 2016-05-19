"""

.. module:: services.py
   :platform: Windows, Linux
   :synopsis: Represents functions/classes used to control Feature Services,
              Feature Service Layer, Map Service, etc...

.. moduleauthor:: Esri

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import os
import uuid
import json
import types
from re import search
from ..common.general import create_uid
from ..packages.six.moves import urllib_parse as urlparse
from ..packages import six
from ._uploads import Uploads
from ..security import security
from .._abstract import abstract
from ..common.filters import LayerDefinitionFilter, GeometryFilter, TimeFilter
from ..common.general import FeatureSet
from ..common import filters
from ..common.geometry import SpatialReference
from ..common.general import _date_handler, Feature
from ..common.spatial import scratchFolder, scratchGDB, json_to_featureclass
from ..common.spatial import get_OID_field, get_records_with_attachments
from ..common.spatial import create_feature_layer, merge_feature_class
from ..common.spatial import featureclass_to_json, create_feature_class
from ..common.spatial import get_attachment_data
from ..common import geometry
from ..hostedservice import AdminFeatureService, AdminFeatureServiceLayer
from .._abstract.abstract import BaseSecurityHandler, BaseAGOLClass

########################################################################
class FeatureService(abstract.BaseAGOLClass):
    """ contains information about a feature service """
    _url = None
    _currentVersion = None
    _serviceDescription = None
    _hasVersionedData = None
    _supportsDisconnectedEditing = None
    _hasStaticData = None
    _maxRecordCount = None
    _supportedQueryFormats = None
    _capabilities = None
    _description = None
    _copyrightText = None
    _spatialReference = None
    _initialExtent = None
    _fullExtent = None
    _allowGeometryUpdates = None
    _units = None
    _syncEnabled = None
    _syncCapabilities = None
    _editorTrackingInfo = None
    _documentInfo = None
    _layers = None
    _tables = None
    _enableZDefaults = None
    _zDefault = None
    _size = None
    _xssPreventionInfo = None
    _editingInfo = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _serverURL = None
    _json = None
    _json_dict = None
    _supportsApplyEditsWithGlobalIds = None
    _serviceItemId = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler=None,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._url = url

        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if isinstance(securityHandler, BaseSecurityHandler):
            if hasattr(securityHandler, 'is_portal'):
                if securityHandler.is_portal:
                    if hasattr(securityHandler, 'portalServerHandler'):
                        self._securityHandler = securityHandler.portalServerHandler(serverUrl=url)
                    else:
                        self._securityHandler = securityHandler
                else:
                    self._securityHandler = securityHandler

            else:
                self._securityHandler = securityHandler


        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ loads the data into the class """
        params = {"f": "json"}

        json_dict = self._get(self._url, params,
                              securityHandler=self._securityHandler,
                              proxy_url=self._proxy_url,
                              proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict,
                                default=_date_handler)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.items():
            if k == 'layers':
                self._getLayers()
            elif k == 'tables':
                self._getTables()
            elif k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print("%s - attribute not implemented in Feature Service." % k)
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        if self._json is None:
            self.__init()
        return self._json
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
    def securityHandler(self):
        """ returns the security handler """
        return self._securityHandler
    #----------------------------------------------------------------------
    @securityHandler.setter
    def securityHandler(self, value):
        """ sets the security handler """
        if isinstance(value, abstract.BaseSecurityHandler):
            if isinstance(value, security.AGOLTokenSecurityHandler):
                self._securityHandler = value
                self._username = value.username
                self._password = value._password
                self._token_url = value.token_url
            elif isinstance(value, security.OAuthSecurityHandler):
                self._securityHandler = value
            else:
                pass
    #----------------------------------------------------------------------
    @property
    def editingInfo(self):
        """  returns the editing information """
        if self._editingInfo is None:
            self.__init()
        return self._editingInfo

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
    def refresh_service(self):
        """ repopulates the properties of the service """
        self._tables = None
        self._layers = None
        self.__init()
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
        """ returns the supported query formats """
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
    def supportsApplyEditsWithGlobalIds(self):
        """returns the supportsApplyEditsWithGlobalIds property"""
        if self._supportsApplyEditsWithGlobalIds is None:
            self.__init()
        return self._supportsApplyEditsWithGlobalIds
    #----------------------------------------------------------------------
    @property
    def serviceItemId(self):
        """ returns the serviceItemId"""
        if self._serviceItemId is None:
            self.__init()
        return self._serviceItemId
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
    def uploads(self):
        """returns the class to perform the upload function.  it will
        only return the uploads class if syncEnabled is True.
        """
        if self.syncEnabled == True:
            return Uploads(url=self._url + "/uploads",
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
        return None
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
        """ returns the editor tracking information """
        if self._editorTrackingInfo is None:
            self.__init()
        return self._editorTrackingInfo
    #----------------------------------------------------------------------
    @property
    def documentInfo(self):
        """ returns the document information """
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
    #----------------------------------------------------------------------
    def _getLayers(self):
        """ gets layers for the featuer service """
        if self._layers is None:
            self._layers = []
            params = {"f": "json"}
            json_dict = self._get(self._url, params,
                                  securityHandler=self._securityHandler,
                                  proxy_url=self._proxy_url,
                                  proxy_port=self._proxy_port)
            if isinstance(json_dict, dict) and \
               'layers' in json_dict:
                for l in json_dict['layers']:
                    self._layers.append(FeatureLayer(url=self._url + "/%s" % l['id'],
                                                     securityHandler=self._securityHandler,
                                                     proxy_port=self._proxy_port,
                                                     proxy_url=self._proxy_url))
                    del l
        return self._layers
    #----------------------------------------------------------------------
    def _getTables(self):
        """ gets layers for the featuer service """
        if self._tables is None:
            self._tables = []
            params = {"f": "json"}
            json_dict = self._get(self._url, params,
                                     securityHandler=self._securityHandler,
                                     proxy_url=self._proxy_url,
                                     proxy_port=self._proxy_port)
            if isinstance(json_dict, dict) and \
               'tables' in json_dict:
                for l in json_dict['tables']:
                    self._tables.append(FeatureLayer(url=self._url + "/%s" % l['id'],
                                                     securityHandler=self._securityHandler,
                                                     proxy_port=self._proxy_port,
                                                     proxy_url=self._proxy_url))
                    del l
        return self._tables
    @property
    def url(self):
        """ returns the url for the feature service"""
        return self._url
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """ returns a list of layer objects """
        if self._layers is None:
            self._getLayers()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def tables(self):
        """ returns the tables  """
        if self._tables is None:
            self._getTables()
        return self._tables
    #----------------------------------------------------------------------
    @property
    def enableZDefaults(self):
        """ returns the enable Z defaults value """
        if self._enableZDefaults is None:
            self.__init()
        return self._enableZDefaults
    #----------------------------------------------------------------------
    @property
    def zDefault(self):
        """ returns the Z default value """
        if self._zDefault is None:
            self.__init()
        return self._zDefault
    #----------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """ returns boolean for has statistic data """
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
    def administration(self):
        """returns the hostservice object to manage the back-end functions"""
        url = self._url
        res = search("/rest/", url).span()
        addText = "admin/"
        part1 = url[:res[1]]
        part2 = url[res[1]:]
        adminURL = "%s%s%s" % (part1, addText, part2)

        res = AdminFeatureService(url=url,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port,
                            initialize=False)
        return res
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
           isinstance(layerDefsFilter, LayerDefinitionFilter):
            params['layerDefs'] = layerDefsFilter.filter
        if not geometryFilter is None and \
           isinstance(geometryFilter, GeometryFilter):
            gf = geometryFilter.filter
            params['geometryType'] = gf['geometryType']
            params['spatialRel'] = gf['spatialRel']
            params['geometry'] = gf['geometry']
            params['inSR'] = gf['inSR']
        if not outSR is None and \
           isinstance(outSR, geometry.SpatialReference):
            params['outSR'] = outSR.asDictionary
        if not timeFilter is None and \
           isinstance(timeFilter, TimeFilter):
            params['time'] = timeFilter.filter
        res =  self._get(url=qurl,
                         param_dict=params,
                         securityHandler=self._securityHandler,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
        if returnIdsOnly == False and returnCountOnly == False:
            if isinstance(res, str):
                jd = json.loads(res)
                return [FeatureSet.fromJSON(json.dumps(lyr)) for lyr in jd['layers']]
            elif isinstance(res, dict):
                return [FeatureSet.fromJSON(json.dumps(lyr)) for lyr in res['layers']]
            else:
                return res
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
        if outWKID is not None:
            params['outSR'] =geometry.SpatialReference(outWKID).asDictionary
        if maxAllowableOffset is not None:
            params['maxAllowableOffset'] = maxAllowableOffset
        if geometryPrecision is not None:
            params['geometryPrecision'] = geometryPrecision
        quURL = self._url + "/queryRelatedRecords"
        res = self._get(url=quURL, param_dict=params,
                        securityHandler=self._securityHandler,
                        proxy_url=self._proxy_url, proxy_port=self._proxy_port)
        return res
    #----------------------------------------------------------------------
    @property
    def replicas(self):
        """ returns all the replicas for a feature service """
        params = {
            "f" : "json",

        }
        url = self._url + "/replicas"
        return self._get(url, params,
                         securityHandler=self._securityHandler,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
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
        return self._post(url, params,
                          securityHandler=self._securityHandler,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port)
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
        return self._get(url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
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
        if self.syncEnabled == False and "Extract" not in self.capabilities:
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
           isinstance(geometryFilter, GeometryFilter):
            params.update(geometryFilter.filter)
        if replicaSR is not None:
            params['replicaSR'] = replicaSR
        if replicaOptions is not None:
            params['replicaOptions'] = replicaOptions
        if transportType is not None:
            params['transportType'] = transportType

        if async:
            if wait:
                exportJob = self._post(url=url,
                                          param_dict=params,
                                          securityHandler=self._securityHandler,
                                          proxy_url=self._proxy_url,
                                          proxy_port=self._proxy_port)
                status = self.replicaStatus(url=exportJob['statusUrl'])
                while status['status'].lower() != "completed":
                    status = self.replicaStatus(url=exportJob['statusUrl'])
                    if status['status'].lower() == "failed":
                        return status

                res = status

            else:
                res = self._post(url=url,
                                     param_dict=params,
                                     securityHandler=self._securityHandler,
                                     proxy_url=self._proxy_url,
                                     proxy_port=self._proxy_port)
        else:
            res = self._post(url=url,
                                param_dict=params,
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)


        if out_path is not None and \
           os.path.isdir(out_path):
            dlURL = None
            if 'resultUrl' in res:

                dlURL = res["resultUrl"]
            elif 'responseUrl' in res:
                dlURL = res["responseUrl"]
            if dlURL is not None:
                return self._get(url=dlURL,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port,
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
        params = {
            "f" : "json",
            "replicaID" : replicaID,
            "transportType" : transportType,
            "dataFormat" : dataFormat,
            "rollbackOnFailure" : rollbackOnFailure,
            "async" : async,
            "returnIdsForAdds": returnIdsForAdds,
            "syncDirection" : syncDirection,
            "returnAttachmentDatabyURL" : returnAttachmentDatabyURL
        }
        return
    #----------------------------------------------------------------------
    def replicaStatus(self, url):
        """gets the replica status when exported async set to True"""
        params = {"f" : "json"}
        url = url + "/status"
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
########################################################################
class FeatureLayer(abstract.BaseAGOLClass):
    """
       This contains information about a feature service's layer.
    """
    _supportsValidateSQL = None
    _syncCanReturnChanges = None
    _dateFieldsTimeReference = None
    _enableZDefaults = None
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
    _supportsValidateSql = None
    _supportsCoordinatesQuantization = None
    _supportsApplyEditsWithGlobalIds = None
    _serviceItemId = None
    _json = None
    _json_dict = None
    _standardMaxRecordCount = None
    _tileMaxRecordCount = None
    _maxRecordCountFactor = None
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
        if isinstance(securityHandler, BaseSecurityHandler):
            if hasattr(securityHandler, 'is_portal'):
                if securityHandler.is_portal:
                    if hasattr(securityHandler, 'portalServerHandler'):
                        self._securityHandler = securityHandler.portalServerHandler(serverUrl=url)
                    else:
                        self._securityHandler = securityHandler
                else:
                    self._securityHandler = securityHandler

            else:
                self._securityHandler = securityHandler

        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the service """
        params = {
            "f" : "json",
        }
        json_dict = self._get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict, default=self._date_handler)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print("%s - attribute not implemented in Feature Layer." % k)
        if self._parentLayer is None:
            self._parentLayer = FeatureService(
                url=os.path.dirname(self._url),
                securityHandler=self._securityHandler,
                proxy_port=self._proxy_port,
                proxy_url=self._proxy_url, initialize=False)
    #----------------------------------------------------------------------
    def refresh(self):
        """refreshes all the properties of the service"""
        self.__init()
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        if self._json is None:
            self.refresh()
        return self._json
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
    def standardMaxRecordCount(self):
        """ returns the standardMaxRecordCount for the feature layer"""
        if self._standardMaxRecordCount is None:
            self.__init()
        return self._standardMaxRecordCount
    #----------------------------------------------------------------------
    @property
    def tileMaxRecordCount(self):
        """ returns the tileMaxRecordCount for the feature layer"""
        if self._tileMaxRecordCount is None:
            self.__init()
        return self._tileMaxRecordCount
    #----------------------------------------------------------------------
    @property
    def maxRecordCountFactor(self):
        """ returns the maxRecordCountFactor for the feature layer"""
        if self._maxRecordCountFactor is None:
            self.__init()
        return self._maxRecordCountFactor

    #----------------------------------------------------------------------
    @property
    def url(self):
        """ returns the url for the feature layer"""
        return self._url
    #----------------------------------------------------------------------
    @property
    def supportsApplyEditsWithGlobalIds(self):
        """ returns the url for the feature layer"""
        if self._supportsApplyEditsWithGlobalIds is None:
            self.__init()
        return self._supportsApplyEditsWithGlobalIds
    #----------------------------------------------------------------------
    @property
    def serviceItemId(self):
        """returns the service item id"""
        if self._serviceItemId is None:
            self.__init()
        return self._serviceItemId
    #----------------------------------------------------------------------
    @property
    def administration(self):
        """returns the hostservice object to manage the back-end functions"""
        url = self._url
        res = search("/rest/", url).span()
        addText = "admin/"
        part1 = url[:res[1]]
        part2 = url[res[1]:]
        adminURL = "%s%s%s" % (part1, addText, part2)

        res = AdminFeatureServiceLayer(url=adminURL,
                                       securityHandler=self._securityHandler,
                                       proxy_url=self._proxy_url,
                                       proxy_port=self._proxy_port,
                                       initialize=True)
        return res
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
            url = os.path.dirname(self._url)
            self._parentLayer = FeatureService(url=url,
                                               securityHandler=self._securityHandler,
                                               proxy_url=self._proxy_url,
                                               proxy_port=self._proxy_port)
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
    def supportsValidateSQL(self):
        """ returns the boolean value """
        if self._supportsValidateSQL is None:
            self.__init()
        return self._supportsValidateSQL
    #----------------------------------------------------------------------
    @property
    def syncCanReturnChanges(self):
        """ returns the syncCanReturnChanges value"""
        if self._syncCanReturnChanges is None:
            self.__init()
        return self._syncCanReturnChanges
    #----------------------------------------------------------------------
    @property
    def dateFieldsTimeReference(self):
        """returns the dateFieldsTimeReference value"""
        if self._dateFieldsTimeReference is None:
            self.__init()
        return self._dateFieldsTimeReference
    #----------------------------------------------------------------------
    @property
    def enableZDefaults(self):
        if self._enableZDefaults is None:
            self.__init()
        return self._enableZDefaults
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
            parsed = urlparse.urlparse(attachURL)

            files = {'attachment': file_path}
            res = self._post(url=attachURL,
                             param_dict=params,
                             files=files,
                             securityHandler=self._securityHandler,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
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
        return self._post(url, params,
                             securityHandler=self._securityHandler,
                             proxy_port=self._proxy_port,
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
        files = {'attachment': file_path }
        res = self._post(url=url,
                             param_dict=params,
                             files=files,
                             securityHandler=self._securityHandler,
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
        return self._get(url, params,
                            securityHandler=self._securityHandler,
                            proxy_port=self._proxy_port,
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
           isinstance(statisticFilter, filters.StatisticFilter):
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
        
        result = self._post(url=url,
                            securityHandler=self._securityHandler,
                            param_dict=params, 
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
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
        if outWKID is not None:
            params['outSR'] = SpatialReference(outWKID).asDictionary
        if maxAllowableOffset is not None:
            params['maxAllowableOffset'] = maxAllowableOffset
        if geometryPrecision is not None:
            params['geometryPrecision'] = geometryPrecision
        quURL = self._url + "/queryRelatedRecords"
        res = self._get(url=quURL, param_dict=params,
                           securityHandler=self._securityHandler,
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

            return self._get(url=popURL, param_dict=params,
                                securityHandler=self._securityHandler,
                                proxy_port=self._proxy_port,
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
                                                  attachmentsSyncDirection="upload",
                                                  async=True,
                                                  wait=True,
                                                  returnAttachments=includeAttachments,
                                                  out_path=out_path)[0]
        elif self.hasAttachments == False and \
             self.parentLayer.syncEnabled:
            return self.parentLayer.createReplica(replicaName="fgdb_dump",
                                                  layers="%s" % self.id,
                                                  attachmentsSyncDirection="upload",
                                                  async=True,
                                                  wait=True,
                                                  returnAttachments=includeAttachments,
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
        if isinstance(features, Feature):
            params['features'] = json.dumps([features.asDictionary],
                                            default=_date_handler
                                            )
        elif isinstance(features, list):
            vals = []
            for feature in features:
                if isinstance(feature, Feature):
                    vals.append(feature.asDictionary)
            params['features'] = json.dumps(vals,
                                            default=_date_handler
                                            )
        elif isinstance(features, FeatureSet):
            params['features'] = json.dumps(
                [feature.asDictionary for feature in features.features],
                default=_date_handler
            )
        else:
            return {'message' : "invalid inputs"}
        updateURL = self._url + "/updateFeatures"
        res = self._post(url=updateURL,
                            securityHandler=self._securityHandler,
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
            "rollbackOnFailure" : rollbackOnFailure
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
        result = self._post(url=dURL, param_dict=params,
                               securityHandler=self._securityHandler,
                               proxy_port=self._proxy_port,
                               proxy_url=self._proxy_url)

        return result
    #----------------------------------------------------------------------
    def applyEdits(self,
                   addFeatures=None,
                   updateFeatures=None,
                   deleteFeatures=None,
                   gdbVersion=None,
                   useGlobalIds=False,
                   rollbackOnFailure=True,
                   attachments=None):
        """
           This operation adds, updates, and deletes features to the
           associated feature layer or table in a single call.
           Inputs:
              addFeatures - The array of features to be added.  These
                            features should be common.Feature objects, or
                            they should be a list of dictionary features.
              updateFeatures - The array of features to be updateded.
                               These features should be common.Feature
                               objects or a list of dictionary formed 
                               features.
              deleteFeatures - string of OIDs to remove from service or a 
                               list of values.  
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
              attachments - Optional parameter which requires the layer's 
                            supportsApplyEditsWithGlobalIds property to be 
                            true.
                            Use the attachments parameter to add, update or
                            delete attachments. Applies only when the 
                            useGlobalIds parameter is set to true. For 
                            adds, the globalIds of the attachments provided
                            by the client are preserved. When useGlobalIds 
                            is true, updates and deletes are identified by 
                            each feature or attachment globalId rather than
                            their objectId or attachmentId.
                            
                            Dictionary Format:
                            {
                            "adds": [<attachment1>, <attachment2>],
                            "updates": [<attachment1>, <attachment2>],
                            "deletes": ["<attachmentGlobalId1>", 
                                        "<attachmentGlobalId2>"]
                            }
           Output:
              dictionary of messages
        """
        editURL = self._url + "/applyEdits"
        params = {"f": "json",
                  "useGlobalIds" : useGlobalIds,
                  "rollbackOnFailure" : rollbackOnFailure
                  }
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion
        if addFeatures is None:
            addFeatures = []
        if updateFeatures is None:
            updateFeatures = []
        if len(addFeatures) > 0 and \
           isinstance(addFeatures[0], Feature):
            params['adds'] = json.dumps([f.asDictionary for f in addFeatures],
                                        default=_date_handler)
        elif len(addFeatures) > 0 and \
             isinstance(addFeatures[0], dict):
            params['adds'] = json.dumps(addFeatures, default=_date_handler)
        elif len(addFeatures) == 0:
            params['adds'] = json.dumps(addFeatures)
        if len(updateFeatures) > 0 and \
           isinstance(updateFeatures[0], Feature):
            params['updates'] = json.dumps([f.asDictionary for f in updateFeatures],
                                           default=_date_handler)
        elif len(updateFeatures) > 0 and \
             isinstance(updateFeatures[0], dict):
            params['updates'] = json.dumps(updateFeatures, 
                                           default=_date_handler)
        elif updateFeatures is None or \
             len(updateFeatures) == 0:
            updateFeatures = json.dumps([])
        if deleteFeatures is not None and \
           isinstance(deleteFeatures, str):
            params['deletes'] = deleteFeatures
        elif deleteFeatures is not None and \
             isinstance(deleteFeatures, list):
            params['deletes'] = ",".join([str(f) for f in deleteFeatures])
        else:
            params['deletes'] = ""
        if attachments is None:
            params['attachments'] = ""
        else:
            params['attachments'] = attachments
        res = self._post(url=editURL, 
                          param_dict=params,
                          securityHandler=self._securityHandler,
                          proxy_port=self._proxy_port,
                          proxy_url=self._proxy_url)
        return res
    #----------------------------------------------------------------------
    def addFeature(self, features,
                   gdbVersion=None,
                   rollbackOnFailure=True):
        """ Adds a single feature to the service
           Inputs:
              feature - list of common.Feature object or a single
                        common.Feature Object, a FeatureSet object, or a
                        list of dictionary objects
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
        if isinstance(features, list) and \
           len(features) > 0:
            if isinstance(features[0], Feature):
                params['features'] = json.dumps([feature.asDictionary for feature in features],
                                                default=_date_handler)
            elif isinstance(features[0], dict):
                params['features'] = json.dumps(features, 
                                                default=_date_handler)
        elif isinstance(features, Feature):
            params['features'] = json.dumps([features.asDictionary],
                                            default=_date_handler)
        elif isinstance(features, FeatureSet):
            params['features'] = json.dumps([feature.asDictionary for feature in features.features],
                                            default=_date_handler)
        else:
            return None
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def addFeatures(self, fc, attachmentTable=None,
                    nameField="ATT_NAME", blobField="DATA",
                    contentTypeField="CONTENT_TYPE",
                    rel_object_field="REL_OBJECTID",
                    lowerCaseFieldNames=False):
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
        messages = {'addResults':[]}

        if attachmentTable is None:
            count = 0
            bins = 1
            uURL = self._url + "/addFeatures"
            max_chunk = 250
            js = json.loads(self._unicode_convert(
                 featureclass_to_json(fc)))
            js = js['features']
            if lowerCaseFieldNames == True:
                for feat in js:
                    feat['attributes'] = dict((k.lower(), v) for k,v in feat['attributes'].items())
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
                                             default=_date_handler)
                }

                result = self._post(url=uURL, param_dict=params,
                                       securityHandler=self._securityHandler,
                                       proxy_port=self._proxy_port,
                                       proxy_url=self._proxy_url)
                if messages is None:
                    messages = result
                else:
                    if 'addResults' in result:
                        if 'addResults' in messages:
                            messages['addResults'] = messages['addResults'] + result['addResults']
                        else:
                            messages['addResults'] = result['addResults']
                    else:
                        messages['errors'] = result

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
                        del s
                    del sends
                    del result
                messages.update( msgs)
                del fl
                del oid
            del OIDs
            return messages

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
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
########################################################################
class TableLayer(FeatureLayer):
    """Table object is exactly like FeatureLayer object"""
    pass
########################################################################
class TiledService(BaseAGOLClass):
    """
       AGOL Tiled Map Service
    """
    _mapName = None
    _documentInfo = None
    _copyrightText = None
    _id = None
    _layers = None
    _tables = None
    _supportedImageFormatTypes = None
    _storageFormat = None
    _capabilities = None
    _access = None
    _currentVersion = None
    _units = None
    _type = None
    _serviceDescription = None
    _status = None
    _tileInfo = None
    _description = None
    _fullExtent = None
    _singleFusedMapCache = None
    _name = None
    _created = None
    _maxScale = None
    _modified = None
    _spatialReference = None
    _minScale = None
    _server = None
    _tileServers = None
    _securityHandler = None
    _exportTilesAllowed = None
    _maxExportTilesCount = None
    _initialExtent = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler,
                 initialize=False,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._url = url
        if isinstance(securityHandler, BaseSecurityHandler):
            self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ loads the data into the class """
        params = {"f": "json"}
        json_dict = self._get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url, proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print("%s - attribute not implemented in tiled service." % k)
    #----------------------------------------------------------------------
    @property
    def maxExportTilesCount(self):
        """ returns the max export tiles count"""
        if self._maxExportTilesCount is None:
            self.__init()
        return self._maxExportTilesCount
    #----------------------------------------------------------------------
    @property
    def exportTilesAllowed(self):
        """ export tiles allowed """
        if self._exportTilesAllowed is None:
            self.__init()
        return self._exportTilesAllowed
    #----------------------------------------------------------------------
    @property
    def securityHandler(self):
        """ gets the security handler """
        return self._securityHandler
    #----------------------------------------------------------------------
    @securityHandler.setter
    def securityHandler(self, value):
        """ sets the security handler """
        if isinstance(value, BaseSecurityHandler):
            if isinstance(value, security.AGOLTokenSecurityHandler):
                self._securityHandler = value
            elif isinstance(value, security.OAuthSecurityHandler):
                self._securityHandler = value
            else:
                pass
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        return json.dumps(dict(self),
                          default=_date_handler)
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
    def initialExtent(self):
        """ initial extent of tile service """
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def mapName(self):
        """ returns the map name """
        if self._mapName is None:
            self.__init()
        return self._mapName
    #----------------------------------------------------------------------
    @property
    def documentInfo(self):
        """ returns the document information """
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """ returns the copyright information """
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def id(self):
        """ returns the ID """
        if self._id is None:
            self.__init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """ returns the layers """
        if self._layers is None:
            self.__init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def tables(self):
        """ returns the tables in the map service """
        if self._tables is None:
            self.__init()
        return self._tables
    #----------------------------------------------------------------------
    @property
    def supportedImageFormatTypes(self):
        """ returns the supported image format types """
        if self._supportedImageFormatTypes is None:
            self.__init()
        return self._supportedImageFormatTypes
    #----------------------------------------------------------------------
    @property
    def storageFormat(self):
        """ returns the storage format """
        if self._storageFormat is None:
            self.__init()
        return self._storageFormat
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """ returns the capabilities """
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def access(self):
        """ returns the access value """
        if self._access is None:
            self.__init()
        return self._access
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the current version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def units(self):
        """ returns the units """
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the type """
        if self._type is None:
            self.__init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the service description """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def status(self):
        """ returns the status """
        if self._status is None:
            self.__init()
        return self._status
    #----------------------------------------------------------------------
    @property
    def tileInfo(self):
        """ returns the tile information """
        if self._tileInfo is None:
            self.__init()
        return self._tileInfo
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the description """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """ returns the full extent """
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def singleFusedMapCache(self):
        """ information about the single fused map cache """
        if self._singleFusedMapCache is None:
            self.__init()
        return self._singleFusedMapCache
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ returns the service name """
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def created(self):
        """ returns the created value """
        if self._created is None:
            self.__init()
        return self._created
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """ returns the maximum scale """
        if self._maxScale is None:
            self.__init()
        return self._maxScale
    #----------------------------------------------------------------------
    @property
    def modified(self):
        """ returns the modified value """
        if self._modified is None:
            self.__init()
        return self._modified
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """ returns the spatial reference value """
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ returns the minimum scale """
        if self._minScale is None:
            self.__init()
        return self._minScale
    #----------------------------------------------------------------------
    @property
    def server(self):
        """ returns the server information """
        if self._server is None:
            self.__init()
        return self._server
    #----------------------------------------------------------------------
    @property
    def tileServers(self):
        """ returns the tile services value """
        if self._tileServers is None:
            self.__init()
        return self._tileServers
