"""

.. module:: featureservice
   :platform: Windows, Linux
   :synopsis: Represents functions/classes used to control Feature Services

.. moduleauthor:: Esri


"""
import types
import layer as servicelayers
import urlparse
import urllib
import os
import json
import mimetypes
from urlparse import urlparse
from re import search
from _uploads import Uploads
from ..security import security
from .._abstract import abstract
from ..common.filters import LayerDefinitionFilter, GeometryFilter, TimeFilter
from ..common.general import _date_handler
from ..common.general import FeatureSet
from ..common import geometry
from ..hostedservice import AdminFeatureService

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
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler=None,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._url = url

        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._securityHandler = securityHandler
        
        #if securityHandler is not None and \
           #isinstance(securityHandler, abstract.BaseSecurityHandler):
            #if isinstance(securityHandler, security.AGOLTokenSecurityHandler):
                #self._username = securityHandler.username
                #self._password = securityHandler._password
                #self._token_url = securityHandler.token_url

                #self._securityHandler = securityHandler

                #self._referer_url = securityHandler.referer_url
            #elif isinstance(securityHandler, security.ArcGISTokenSecurityHandler):
                #self._username = securityHandler.username
                #self._securityHandler = securityHandler
                #self._referer_url = securityHandler.referer_url
            #elif isinstance(securityHandler, security.PortalTokenSecurityHandler):
                #parsedURL = urlparse(url=url)
                #pathParts = parsedURL.path.split('/')
                #self._serverURL = parsedURL.scheme + '://' + parsedURL.netloc + '/' + pathParts[1]

                #self._username = securityHandler.username
                #self._password = securityHandler.password
                #self._token_url = securityHandler.token_url
                #self._securityHandler = securityHandler
                #self._referer_url = securityHandler.referer_url
            #elif isinstance(securityHandler, security.OAuthSecurityHandler):

                #self._securityHandler = securityHandler
                #self._referer_url = securityHandler.referer_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ loads the data into the class """
        params = {"f": "json"}

        json_dict = self._do_get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict,
                                default=_date_handler)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implemented in Feature Service."
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

        params = {"f": "json"}
        json_dict = self._do_get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._layers = []
        if json_dict.has_key("layers"):
            for l in json_dict["layers"]:
                self._layers.append(
                    servicelayers.FeatureLayer(url=self._url + "/%s" % l['id'],
                                               securityHandler=self._securityHandler,
                                               proxy_port=self._proxy_port,
                                               proxy_url=self._proxy_url)
                )
    #----------------------------------------------------------------------
    def _getTables(self):
        """ gets layers for the featuer service """

        params = {"f": "json"}
        json_dict = self._do_get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url, proxy_port=self._proxy_port)
        self._tables = []
        if json_dict.has_key("tables"):
            for l in json_dict["tables"]:
                self._tables.append(
                    servicelayers.TableLayer(url=self._url + "/%s" % l['id'],
                                               securityHandler=self._securityHandler,
                                               proxy_port=self._proxy_port,
                                               proxy_url=self._proxy_url)
                )
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
        res =  self._do_get(url=qurl,
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
        res = self._do_get(url=quURL, param_dict=params,
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
        return self._do_get(url, params,
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
        return self._do_post(url, params,
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
        return self._do_get(url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def createReplica(self,
                      replicaName,
                      layers,
                      keep_replica=False,
                      layerQueries=None,
                      geometryFilter=None,
                      returnAttachments=False,
                      returnAttachmentDatabyURL=True,
                      returnAsFeatureClass=False,
                      out_path=None
                      ):
        """ generates a replica
            Inputs:
               replicaName - string of replica name
               layers - layer id # as comma seperated string
               keep_replica - if the replica does not have returnAsFeatureClass set to true,
                              the feature service creates a permanent copy of the replica.
                              If this is just a pull, then erase the replica in order to prevent
                              build up of replicas.
               layerQueries - In addition to the layers and geometry parameters, the layerQueries
                              parameter can be used to further define what is replicated. This
                              parameter allows you to set properties on a per layer or per table
                              basis. Only the properties for the layers and tables that you want
                              changed from the default are required.
                                Example:
                                  layerQueries = {"0":{"queryOption": "useFilter", "useGeometry": true,
                                                 "where": "requires_inspection = Yes"}}
               geometryFilter - Geospatial filter applied to the replica to parse down data output.
               returnAttachments - If true, attachments are added to the replica and returned in the
                                   response. Otherwise, attachments are not included.
               returnAttachmentDatabyURL -  If true, a reference to a URL will be provided for each
                                            attachment returned from createReplica. Otherwise,
                                            attachments are embedded in the response.
               returnAsFeatureClass - If a local copy is desired, set this parameter to True, else
                                      the service will return information on how to download the
                                      json file.
               out_path - Path where the FGDB will be saved.  Only used with returnAsFeatureClass is
                          True.
        """
        if self.syncEnabled:
            url = self._url + "/createReplica"
            params = {
                "f" : "json",
                "replicaName": replicaName,
                "layers": layers,
                "returnAttachmentDatabyURL" : returnAttachmentDatabyURL,
                "returnAttachments" : returnAttachments,
                "async" : False
            }
            if not geometryFilter is None and \
               isinstance(geometryFilter, GeometryFilter):
                gf = geometryFilter.filter
                params['geometryType'] = gf['geometryType']
                params['geometry'] = gf['geometry']
                params['inSR'] = gf['inSR']
            if returnAsFeatureClass and \
               out_path is not None:
                if os.path.isdir(out_path) == False:
                    os.makedirs(out_path)
                params['dataFormat'] = "filegdb"
                params['syncModel'] = 'none'
                res = self._do_post(url=url, param_dict=params,
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port)
                if res.has_key("responseUrl"):
                    zipURL = res["responseUrl"]
                    dl_file = self._download_file(url=zipURL,
                                        save_path=out_path,
                                        securityHandler=self._securityHandler,
                                        file_name=os.path.basename(zipURL)
                                        )
                    self._unzip_file(zip_file=dl_file, out_folder=out_path)
                    os.remove(dl_file)
                    return self._list_files(path=out_path + os.sep + "*.gdb")
                else:
                    return None
            else:
                res = self._do_post(url=url, param_dict=params,
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url, proxy_port=self._proxy_port)
                return res

        return "Not Supported"
