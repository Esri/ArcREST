from base import BaseAGOLClass
import layer as servicelayers
from common import SpatialReference
from filters import LayerDefinitionFilter, GeometryFilter, TimeFilter
from base import Geometry
import urlparse
import urllib
import os
import json
import mimetypes

########################################################################
class FeatureService(BaseAGOLClass):
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
    #----------------------------------------------------------------------
    def __init__(self, url,  token_url=None, username=None, password=None):
        """Constructor"""
        self._url = url
        self._username = username
        self._password = password
        self._token_url = token_url        
        if not username is None and \
           not password is None:
            self._token = self.generate_token(tokenURL=token_url)[0]
    #----------------------------------------------------------------------
    def __init(self):
        """ loads the data into the class """
        if self._token is None:
            param_dict = {"f": "json"}
        else:
            param_dict = {"f": "json",
                          "token" : self._token
                          }            
        json_dict = self._do_get(self._url, param_dict) 
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
    def documentInfo(self):
        """"""
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
    #----------------------------------------------------------------------
    def _getLayers(self):
        """ gets layers for the featuer service """
        if self._token is None:
            param_dict = {"f": "json"}
        else:
            param_dict = {"f": "json",
                          "token" : self._token
                          }            
        json_dict = self._do_get(self._url, param_dict)
        self._layers = []
        if json_dict.has_key("layers"):
            for l in json_dict["layers"]:
                self._layers.append(
                    servicelayers.FeatureLayer(url=self._url + "/%s" % l['id'],
                                               username=self._username,
                                               password=self._password,
                                               token_url=self._token_url)
                )
    #----------------------------------------------------------------------
    def _getTables(self):
        """ gets layers for the featuer service """
        if self._token is None:
            param_dict = {"f": "json"}
        else:
            param_dict = {"f": "json",
                          "token" : self._token
                          }            
        json_dict = self._do_get(self._url, param_dict)
        self._tables = []
        if json_dict.has_key("tables"):
            for l in json_dict["tables"]:
                self._tables.append(
                    servicelayers.TableLayer(url=self._url + "/%s" % l['id'],
                                               username=self._username,
                                               password=self._password,
                                               token_url=self._token_url)
                )
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
        """"""
        if self._tables is None:
            self._getTables()
        return self._tables
    #----------------------------------------------------------------------
    @property
    def enableZDefaults(self):
        """"""
        if self._enableZDefaults is None:
            self.__init()
        return self._enableZDefaults
    #----------------------------------------------------------------------
    @property
    def zDefault(self):
        """"""
        if self._zDefault is None:
            self.__init()
        return self._zDefault
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
        if not self._token is None:
            params["token"] = self._token
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
           isinstance(outSR, SpatialReference):
            params['outSR'] = outSR.asDictionary
        if not timeFilter is None and \
           isinstance(timeFilter, TimeFilter):
            params['time'] = timeFilter.filter
        return self._do_get(url=qurl, param_dict=params)
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
            params['outSR'] = common.SpatialReference(outWKID).asDictionary
        if maxAllowableOffset is not None:
            params['maxAllowableOffset'] = maxAllowableOffset
        if geometryPrecision is not None:
            params['geometryPrecision'] = geometryPrecision
        quURL = self._url + "/queryRelatedRecords"
        res = self._do_get(url=quURL, param_dict=params)
        return res
    #----------------------------------------------------------------------
    @property
    def replicas(self):
        """ returns all the replicas for a feature service """
        params = {
            "f" : "json",
            
        }
        if not self._token is None:
            params["token"] = self._token        
        url = self._url + "/replicas"
        return self._do_get(url, params)
    #----------------------------------------------------------------------
    def unRegisterReplica(self, replica_id):
        """"""
        params = {
            "f" : "json",
            "replicaID" : replica_id
        }
        if not self._token is None:
            params["token"] = self._token        
        url = self._url + "/unRegisterReplica"
        return self._do_post(url, params)       
    #----------------------------------------------------------------------
    def replicaInfo(self, replica_id):
        """
           The replica info resources lists replica metadata for a specific replica.
        """
        params = {
            "f" : "json"
        }
        if not self._token is None:
            params["token"] = self._token        
        url = self._url + "/replicas/%s" + replica_id
        return self._do_get(url, param_dict=params)
    #----------------------------------------------------------------------
    def createReplica(self, 
                      replicaName, 
                      layers, 
                      keep_replica=False,
                      layerQueries=None,
                      geometryFilter=None,
                      #geometry=None, geometryType=None,
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
            if not self._token is None:
                params["token"] = self._token            
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
                res = self._do_post(url=url, param_dict=params)
                if res.has_key("responseUrl"):
                    zipURL = res["responseUrl"]
                    dl_file = self._download_file(url=zipURL, 
                                        save_path=out_path, 
                                        file_name=os.path.basename(zipURL)
                                        )
                    self._unzip_file(zip_file=dl_file, out_folder=out_path)
                    os.remove(dl_file)
                    return self._list_files(path=out_path + os.sep + "*.gdb")
                else:
                    return None
            else:
                res = self._do_post(url=url, param_dict=params)                
                return res
            
        return "Not Supported"
        
