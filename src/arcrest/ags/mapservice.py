from .._abstract.abstract import BaseAGSServer, DynamicData, BaseSecurityHandler
import layer
from ..common.general import Feature
from layer import FeatureLayer, TableLayer, RasterLayer
from ..common import filters, geometry
from ..security import security
import json
import time
from ..common.geometry import Polygon
import tempfile
from geoprocessing import GPJob
########################################################################
class MapService(BaseAGSServer):
    """ contains information about a map service """
    _json = None
    _json_dict = None
    _tileInfo = None
    _url = None
    _username = None
    _password = None
    _token = None
    _token_url = None
    _currentVersion = None
    _serviceDescription = None
    _mapName = None
    _description = None
    _copyrightText = None
    _supportsDynamicLayers = None
    _layers = None
    _tables = None
    _spatialReference = None
    _singleFusedMapCache = None
    _initialExtent = None
    _fullExtent = None
    _minScale = None
    _maxScale = None
    _units = None
    _supportedImageFormatTypes = None
    _documentInfo = None
    _capabilities = None
    _supportedQueryFormats = None
    _exportTilesAllowed = None
    _maxRecordCount = None
    _maxImageHeight = None
    _maxImageWidth = None
    _supportedExtensions = None
    _timeInfo = None
    _maxExportTilesCount = None
    _hasVersionedData = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 initialize=False, proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._proxy_url= proxy_url
        self._proxy_port = proxy_port
        self._url = url
        if securityHandler is not None and \
           isinstance(securityHandler, (security.AGSTokenSecurityHandler,
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
    @property
    def itemInfo(self):
        """gets the item's info"""
        params = {
            "f" : "json"
        }
        if not self._securityHandler is None:
            params['token'] = self._securityHandler.token
        url = self._url + "/info/iteminfo"
        return self._do_get(url=url, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def downloadThumbnail(self, outPath):
        """downloads the items's thumbnail"""
        url = self._url + "/info/thumbnail"
        params = {

        }
        if not self._securityHandler is None:
            params['token']  = self._securityHandler.token
        return self._download_file(url=url,
                            save_path=outPath,
                            file_name=None,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def downloadMetadataFile(self, outPath):
        """downloads the metadata file to a given path"""
        fileName = "metadata.xml"
        url = self._url + "/info/metadata"
        params = {}
        if not self._securityHandler is None:
            params['token']  = self._securityHandler.token
        return self._download_file(url=url,
                                   save_path=outPath,
                                   file_name=fileName,
                                   param_dict=params,
                                   proxy_url=self._proxy_url,
                                   proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def __str__(self):
        """gets the object as as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    @property
    def json_dict(self):
        """returns object as a dictionary"""
        if self._json_dict is None:
            self.__init()
        return self._json_dict
    #----------------------------------------------------------------------
    def __init(self):
        """ populates all the properties for the map service """
        if self._token is None:
            param_dict = {"f": "json"}
        else:
            param_dict = {"f": "json",
                          "token" : self._token
                          }
        json_dict = self._do_get(self._url, param_dict,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json = json.dumps(json_dict)
        self._json_dict = json_dict
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k == "tables":
                self._tables = []
                for tbl in v:
                    url = self._url + "/%s" % tbl['id']
                    self._tables.append(
                        layer.TableLayer(url,
                                         securityHandler=self._securityHandler,
                                         proxy_port=self._proxy_port,
                                         proxy_url=self._proxy_url)
                    )
            elif k == "layers":
                self._layers = []
                for lyr in v:
                    url = self._url + "/%s" % lyr['id']
                    layer_type = self._getLayerType(url)
                    if layer_type == "Feature Layer":
                        self._layers.append(
                            layer.FeatureLayer(url,
                                               securityHandler=self._securityHandler,
                                               proxy_port=self._proxy_port,
                                               proxy_url=self._proxy_url)
                        )
                    elif layer_type == "Raster Layer":
                        self._layers.append(
                            layer.RasterLayer(url,
                                         securityHandler=self._securityHandler,
                                         proxy_port=self._proxy_port,
                                         proxy_url=self._proxy_url)
                        )
                    elif layer_type == "Group Layer":
                        self._layers.append(
                            layer.GroupLayer(url,
                                             securityHandler=self._securityHandler,
                                             proxy_port=self._proxy_port,
                                             proxy_url=self._proxy_url)
                        )
                    else:
                        print 'Type %s is not implemented' % layer_type
            elif k in attributes:
                setattr(self, "_"+ k, json_dict[k])

            else:
                print k, " is not implemented for mapservice."
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
            if isinstance(value, security.AGSTokenSecurityHandler):
                self._securityHandler = value
                self._token = value.token
            else:
                pass
        elif value is None:
            self._securityHandler = None
            self._token = None
    #----------------------------------------------------------------------
    @property
    def maxExportTilesCount(self):
        """ returns the maximum export tiles count """
        if self._maxExportTilesCount is None:
            self.__init()
        return self._maxExportTilesCount
    @property
    def hasVersionedData(self):
        """ reutrn boolean if has versioned data """
        if self._hasVersionedData is None:
            self.__init()
        return self._hasVersionedData
    #----------------------------------------------------------------------
    @property
    def tileInfo(self):
        """ Returns tile info for cached services """
        if self._tileInfo is None:
            self.__init()
        return self._tileInfo
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
    def mapName(self):
        """ returns the map name value """
        if self._mapName is None:
            self.__init()
        return self._mapName
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the map service description """
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
    def supportsDynamicLayers(self):
        """ returns boolean (True/False) if it support dynamic layers"""
        if self._supportsDynamicLayers is None:
            self.__init()
        return self._supportsDynamicLayers
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """ returns all the layers in the map service """
        if self._layers is None:
            self.__init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def tables(self):
        """ returns all tables in the map service """
        if self._tables is None:
            self.__init()
        return self._tables
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """ returns the spatialreference information for the map service """
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def singleFusedMapCache(self):
        """ returns boolean for this property """
        if self._singleFusedMapCache is None:
            self.__init()
        return self._singleFusedMapCache
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """ returns the initial extent of the map service """
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """ returns the full extent of the map service """
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ returns the map service minimum scale """
        if self._minScale is None:
            self.__init()
        return self._minScale
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """ returns the max scale for a map service """
        if self._maxScale is None:
            self.__init()
        return self._maxScale
    #----------------------------------------------------------------------
    @property
    def units(self):
        """ returns the map service's measurement units """
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def supportedImageFormatTypes(self):
        """ returns the supported image format types """
        if self._supportedImageFormatTypes is None:
            self.__init()
        return self._supportedImageFormatTypes
    #----------------------------------------------------------------------
    @property
    def timeInfo(self):
        """ returns the timeInformation for a given service """
        if self._timeInfo is None:
            self.__init()
        return self._timeInfo

    #----------------------------------------------------------------------
    @property
    def documentInfo(self):
        """ returns the document information as a dictionary """
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """ returns the service's capabilities """
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def supportedQueryFormats(self):
        """ returns the supported query formats """
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    #----------------------------------------------------------------------
    @property
    def exportTilesAllowed(self):
        """ Boolean if export tiles is allowed """
        if self._exportTilesAllowed is None:
            self.__init()
        return self._exportTilesAllowed
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """ returns the max number of records returned by a query/display ect. """
        if self._maxRecordCount is None:
            self.__init()
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @property
    def maxImageHeight(self):
        """ returns the max image height """
        if self._maxImageHeight is None:
            self.__init()
        return self._maxImageHeight
    #----------------------------------------------------------------------
    @property
    def maxImageWidth(self):
        """ returns the max image width """
        if self._maxImageWidth is None:
            self.__init()
        return self._maxImageWidth
    #----------------------------------------------------------------------
    @property
    def supportedExtensions(self):
        """ returns the supported extensions """
        if self._supportedExtensions is None:
            self.__init()
        return self._supportedExtensions
    #----------------------------------------------------------------------
    @property
    def allLayers(self):
        """ returns all layers for the service """
        url = self._url + "/layers"
        params = {
            "f" : "json"
        }
        if self._token is not None:
            params['token'] = self._token
        res = self._do_get(url, param_dict=params)
        return_dict = {
            "layers" : [],
            "tables" : []
        }
        for k, v in res.iteritems():
            if k == "layers":
                for val in v:
                    return_dict['layers'].append(
                        layer.FeatureLayer(url=self._url + "/%s" % val['id'],
                                           token_url=self._token_url,
                                           username=self._username,
                                           password=self._password)
                    )
            elif k == "tables":
                for val in v:
                    return_dict['tables'].append(
                        layer.TableLayer(url=self._url + "/%s" % val['id'],
                                           token_url=self._token_url,
                                           username=self._username,
                                           password=self._password)
                    )
            del k,v
        return return_dict
    #----------------------------------------------------------------------
    def find(self, searchText, layers,
             contains=True, searchFields="",
             sr="", layerDefs="",
             returnGeometry=True, maxAllowableOffset="",
             geometryPrecision="", dynamicLayers="",
             returnZ=False, returnM=False, gdbVersion=""):
        """ performs the map service find operation """
        url = self._url + "/find"
        #print url
        params = {
            "f" : "json",
            "searchText" : searchText,
            "contains" : self._convert_boolean(contains),
            "searchFields": searchFields,
            "sr" : sr,
            "layerDefs" : layerDefs,
            "returnGeometry" : self._convert_boolean(returnGeometry),
            "maxAllowableOffset" : maxAllowableOffset,
            "geometryPrecision" : geometryPrecision,
            "dynamicLayers" : dynamicLayers,
            "returnZ" : self._convert_boolean(returnZ),
            "returnM" : self._convert_boolean(returnM),
            "gdbVersion" : gdbVersion,
            "layers" : layers
        }
        if not self._token is None and \
           self._token != "":
            params['token'] = self._token
        res = self._do_get(url, params)
        qResults = []
        for r in res['results']:
            qResults.append(Feature(r))
        print 'stop'
        return qResults
    #----------------------------------------------------------------------
    def _getLayerType(self, url):
        """ returns a layer type """
        params={
            "f" : "json"
        }
        if self._token is not None:
            params['token'] = self._token
        res = self._do_get(url=url, param_dict=params)
        return res['type']
    #----------------------------------------------------------------------
    def getFeatureDynamicLayer(self, oid, dynamicLayer,
                               returnZ=False, returnM=False):
        """ The feature resource represents a single feature in a dynamic
            layer in a map service
        """
        url = self._url + "/dynamicLayer/%s" % oid
        params = {
            "f": "json",
            "returnZ": returnZ,
            "returnM" : returnM,
            "layer": {
                "id": 101,
                "source" : dynamicLayer.asDictionary
            }
        }
        return Feature(
            json_string=self._do_get(url=url,
                                     param_dict=params,
                                     proxy_port=self._proxy_port,
                                     proxy_url=self._proxy_url)
        )
    #----------------------------------------------------------------------
    def identify(self,
                 geometryFilter,
                 mapExtent,
                 imageDisplay,
                 layerDefs=None,
                 timeFilter=None,
                 layerTimeOptions=None,
                 layers="top",
                 tolerance=None,
                 returnGeometry=True,
                 maxAllowableOffset=None,
                 geometryPrecision=None,
                 dynamicLayers=None,
                 returnZ=False,
                 returnM=False,
                 gdbVersion=None
                 ):
        """ performs the map service's identify operation """
        pass
    #----------------------------------------------------------------------
    def _convert_boolean(self, value):
        """ converts a boolean value to json value """
        if value == True:
            return 'true'
        else:
            return 'false'
    #----------------------------------------------------------------------
    def generateKML(self, save_location, docName, layers, layerOptions="composite"):
        """
           The generateKml operation is performed on a map service resource.
           The result of this operation is a KML document wrapped in a KMZ
           file. The document contains a network link to the KML Service
           endpoint with properties and parameters you specify.
           Inputs:
              docName - The name of the resulting KML document. This is the
                        name that appears in the Places panel of Google
                        Earth.
              layers - the layers to perform the generateKML operation on.
                       The layers are specified as a comma-separated list
                       of layer ids.
              layerOptions - The layer drawing options. Based on the option
                             chosen, the layers are drawn as one composite
                             image, as separate images, or as vectors. When
                             the KML capability is enabled, the ArcGIS
                             Server administrator has the option of setting
                             the layer operations allowed. If vectors are
                             not allowed, then the caller will not be able
                             to get vectors. Instead, the caller receives a
                             single composite image.
                             values: composite | separateImage |
                                     nonComposite
        """
        kmlURL = self._url + "/generateKml"
        params= {'f': 'json',
                 'docName' : docName,
                 'layers' : layers,
                 'layerOptions': layerOptions
                 }
        if self._token is not None:
            params['token'] = self._token
        import urllib
        url = kmlURL + "?%s" % urllib.urlencode(params)
        return self._download_file(url, save_location, docName + ".kmz")
    #----------------------------------------------------------------------
    def exportMap(self,
                  bbox,
                  size="600,550",
                  dpi=200,
                  imageSR=None,
                  image_format="png",
                  layerDefFilter=None,
                  layers=None,
                  transparent=False,
                  timeFilter=None,
                  layerTimeOptions=None,
                  dynamicLayers=None,
                  mapScale=None
                  ):
        """
           The export operation is performed on a map service resource.
           The result of this operation is a map image resource. This
           resource provides information about the exported map image such
           as its URL, its width and height, extent and scale.
           Inputs:
            bbox - envelope geometry object
            size - size of image in pixels
            dpi - dots per inch
            imageSR - spatial reference of the output image
            image_format - Description: The format of the exported image.
                             The default format is .png.
                             Values: png | png8 | png24 | jpg | pdf | bmp | gif
                                     | svg | svgz | emf | ps | png32
            layerDefFilter - Description: Allows you to filter the
                             features of individual layers in the exported
                             map by specifying definition expressions for
                             those layers. Definition expression for a
                             layer that is published with the service will
                             be always honored.
            layers - Determines which layers appear on the exported map.
                     There are four ways to specify which layers are shown:
                        show: Only the layers specified in this list will
                              be exported.
                        hide: All layers except those specified in this
                              list will be exported.
                        include: In addition to the layers exported by
                                 default, the layers specified in this list
                                 will be exported.
                        exclude: The layers exported by default excluding
                                 those specified in this list will be
                                 exported.
            transparent - If true, the image will be exported with the
                          background color of the map set as its
                          transparent color. The default is false. Only
                          the .png and .gif formats support transparency.
                          Internet Explorer 6 does not display transparency
                          correctly for png24 image formats.
            timeFilter - The time instant or time extent of the exported
                         map image.
            layerTimeOptions - The time options per layer. Users can
                               indicate whether or not the layer should use
                               the time extent specified by the time
                               parameter or not, whether to draw the layer
                               features cumulatively or not and the time
                               offsets for the layer.
                               see: http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Export_Map/02r3000000v7000000/
            dynamicLayers - Use dynamicLayers parameter to modify the layer
                            drawing order, change layer drawing info, and
                            change layer data source version for this request.
                            New layers (dataLayer) can also be added to the
                            dynamicLayers based on the map service registered
                            workspaces.
            mapScale - Use this parameter to export a map image at a specific
                       scale, with the map centered around the center of the
                       specified bounding box (bbox).

        """
        params = {
            "f" : "json"
        }
        if self._token is not None:
            params['token'] = self._token
        if isinstance(bbox, geometry.Envelope):
            vals = bbox.asDictionary
            params['bbox'] = "%s,%s,%s,%s" % (vals['xmin'], vals['ymin'],
                                              vals['xmax'], vals['ymax'])
            params['bboxSR'] = vals['spatialReference']
            if dpi is not None:
                params['dpi'] = dpi
            if size is not None:
                params['size'] = size
            if imageSR is not None and \
               isinstance(imageSR, geometry.SpatialReference):
                params['imageSR'] = {'wkid': imageSR.wkid}
            if image_format is not None:
                params['format'] = image_format
            if layerDefFilter is not None and \
               isinstance(layerDefFilter,
                          filters.LayerDefinitionFilter):
                params['layerDefs'] = layerDefFilter.filter
            if layers is not None:
                params['layers'] = layers
            if transparent is not None:
                params['transparent'] = transparent
            if timeFilter is not None and \
               isinstance(timeFilter, filters.TimeFilter):
                params['time'] = timeFilter.filter
            if layerTimeOptions is not None:
                params['layerTimeOptions'] = layerTimeOptions
            if dynamicLayers is not None and \
               isinstance(dynamicLayers, DynamicData):
                params['dynamicLayers'] = dynamicLayers.asDictionary
            if mapScale is not None:
                params['mapScale'] = mapScale
            exportURL = self._url + "/export"
            return self._do_get(url=exportURL,
                                param_dict=params)
        else:
            return None
    #----------------------------------------------------------------------
    def estimateExportTilesSize(self,
                                exportBy,
                                levels,
                                tilePackage=False,
                                exportExtent="DEFAULTEXTENT",
                                areaOfInterest=None,
                                async=True):
        """
        The estimateExportTilesSize operation is an asynchronous task that
        allows estimation of the size of the tile package or the cache data
        set that you download using the Export Tiles operation. This
        operation can also be used to estimate the tile count in a tile
        package and determine if it will exceced the maxExportTileCount
        limit set by the administrator of the service. The result of this
        operation is Map Service Job. This job response contains reference
        to Map Service Result resource that returns the total size of the
        cache to be exported (in bytes) and the number of tiles that will
        be exported.

        Inputs:

        tilePackage - Allows estimating the size for either a tile package
         or a cache raster data set. Specify the value true for tile
         packages format and false for Cache Raster data set. The default
         value is False
           Values: True | False
        exportExtent - The extent (bounding box) of the tile package or the
         cache dataset to be exported. If extent does not include a spatial
         reference, the extent values are assumed to be in the spatial
         reference of the map. The default value is full extent of the
         tiled map service.
	   Syntax: <xmin>, <ymin>, <xmax>, <ymax>
           Example 1: -104,35.6,-94.32,41
        exportBy - The criteria that will be used to select the tile
         service levels to export. The values can be Level IDs, cache scales
         or the Resolution (in the case of image services).
	   Values: LevelID | Resolution | Scale
        levels - Specify the tiled service levels for which you want to get
         the estimates. The values should correspond to Level IDs, cache
         scales or the Resolution as specified in exportBy parameter. The
         values can be comma separated values or a range.
	   Example 1: 1,2,3,4,5,6,7,8,9
	   Example 2: 1-4,7-9
        areaOfInterest - (Optional) The areaOfInterest polygon allows
         exporting tiles within the specified polygon areas. This parameter
         supersedes exportExtent parameter. Also excepts geometry.Polygon.
	   Example: { "features": [{"geometry":{"rings":[[[-100,35],
             [-100,45],[-90,45],[-90,35],[-100,35]]],
             "spatialReference":{"wkid":4326}}}]}
        async - (optional) the estimate function is run asynchronously
         requiring the tool status to be checked manually to force it to
         run synchronously the tool will check the status until the
         estimation completes.  The default is True, which means the status
         of the job and results need to be checked manually.  If the value
         is set to False, the function will wait until the task completes.
           Values: True | False
        """
        url = self._url + "/estimateExportTilesSize"
        params = {
            "f" : "json",
            "levels" : levels,
            "exportBy" : exportBy,
            "tilePackage" : tilePackage,
            "exportExtent" : exportExtent
        }
        if not self._securityHandler is None:
            params['token'] = self._securityHandler.token
        params["levels"] = levels
        if not areaOfInterest is None:
            if isinstance(areaOfInterest, Polygon):
                template = { "features": [areaOfInterest.asDictionary]}
                params['areaOfInterest'] = template
            else:
                params['areaOfInterest'] = areaOfInterest
        if async == True:
            return self._do_get(url=url,
                                param_dict=params,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
        else:
            exportJob = self._do_get(url=url,
                                     param_dict=params,
                                     proxy_url=self._proxy_url,
                                     proxy_port=self._proxy_port)
            jobUrl = "%s/jobs/%s" % (url, exportJob['jobId'])
            gpJob = GPJob(url=jobUrl,
                          securityHandler=self._securityHandler,
                          proxy_port=self._proxy_port,
                          proxy_url=self._proxy_url)
            status = gpJob.jobStatus
            while status != "esriJobSucceeded":
                if status in ['esriJobFailed',
                              'esriJobCancelling',
                              'esriJobCancelled']:
                    return None
                else:
                    time.sleep(5)
                    status = gpJob.jobStatus
            return gpJob.getAllResults['out_service_url']['value']
    #----------------------------------------------------------------------
    def exportTiles(self,
                    levels,
                    exportBy="LevelID",
                    tilePackage=False,
                    exportExtent="DEFAULT",
                    optimizeTilesForSize=True,
                    compressionQuality=0,
                    areaOfInterest=None,
                    async=False
                    ):
        """
        The exportTiles operation is performed as an asynchronous task and
        allows client applications to download map tiles from a server for
        offline use. This operation is performed on a Map Service that
        allows clients to export cache tiles. The result of this operation
        is Map Service Job. This job response contains a reference to the
        Map Service Result resource, which returns a URL to the resulting
        tile package (.tpk) or a cache raster dataset.
        exportTiles can be enabled in a service by using ArcGIS for Desktop
        or the ArcGIS Server Administrator Directory. In ArcGIS for Desktop
        make an admin or publisher connection to the server, go to service
        properties, and enable Allow Clients to Export Cache Tiles in the
        advanced caching page of the Service Editor. You can also specify
        the maximum tiles clients will be allowed to download. The default
        maximum allowed tile count is 100,000. To enable this capability
        using the Administrator Directory, edit the service, and set the
        properties exportTilesAllowed=true and maxExportTilesCount=100000.

        At 10.2.2 and later versions, exportTiles is supported as an
        operation of the Map Server. The use of the
        http://Map Service/exportTiles/submitJob operation is deprecated.
        You can provide arguments to the exportTiles operation as defined
        in the following parameters table:

        Inputs:
         exportBy - The criteria that will be used to select the tile
           service levels to export. The values can be Level IDs, cache
           scales. or the resolution (in the case of image services).
	   Values: LevelID | Resolution | Scale
        levels - Specifies the tiled service levels to export. The values
          should correspond to Level IDs, cache scales. or the resolution
          as specified in exportBy parameter. The values can be comma
          separated values or a range. Make sure tiles are present at the
          levels where you attempt to export tiles.
	   Example 1: 1,2,3,4,5,6,7,8,9
	   Example 2: 1-4,7-9
        tilePackage - Allows exporting either a tile package or a cache
          raster data set. If the value is true, output will be in tile
          package format, and if the value is false, a cache raster data
          set is returned. The default value is false
	   Values: true | false
        exportExtent - The extent (bounding box) of the tile package or the
          cache dataset to be exported. If extent does not include a
          spatial reference, the extent values are assumed to be in the
          spatial reference of the map. The default value is full extent of
          the tiled map service.
                       Syntax: <xmin>, <ymin>, <xmax>, <ymax>
                       Example 1: -104,35.6,-94.32,41
                       Example 2: {"xmin" : -109.55, "ymin" : 25.76,
                        "xmax" : -86.39, "ymax" : 49.94,
                        "spatialReference" : {"wkid" : 4326}}
        optimizeTilesForSize - (Optional) Use this parameter to enable
          compression of JPEG tiles and reduce the size of the downloaded
          tile package or the cache raster data set. Compressing tiles
          slightly compromises the quality of tiles but helps reduce the
          size of the download. Try sample compressions to determine the
          optimal compression before using this feature.
	   Values: true | false
        compressionQuality - (Optional) When optimizeTilesForSize=true, you
         can specify a compression factor. The value must be between 0 and
         100. The value cannot be greater than the default compression
         already set on the original tile. For example, if the default
         value is 75, the value of compressionQuality must be between 0 and
         75. A value greater than 75 in this example will attempt to up
         sample an already compressed tile and will further degrade the
         quality of tiles.
        areaOfInterest - (Optional) The areaOfInterest polygon allows
         exporting tiles within the specified polygon areas. This parameter
         supersedes the exportExtent parameter. Must be geometry.Polygon
         object.
        Example: { "features": [{"geometry":{"rings":[[[-100,35],
         [-100,45],[-90,45],[-90,35],[-100,35]]],
         "spatialReference":{"wkid":4326}}}]}
        async - default True, this value ensures the returns are returned
         to the user instead of the user having the check the job status
         manually.
        """
        params = {
            "f" : "json",
            "tilePackage" : tilePackage,
            "exportExtent" : exportExtent,
            "optimizeTilesForSize" : optimizeTilesForSize,
            "compressionQuality" : compressionQuality,
            "exportBy" : exportBy,
            "levels" : levels
        }
        url = self._url + "/exportTiles"
        if not self._securityHandler is None:
            params['token'] = self._securityHandler.token
        if isinstance(areaOfInterest, Polygon):
            geom = areaOfInterest.asDictionary()
            feature_template = {
                "geometry" :geom,

                "attributes" : {
                  "OID" : 1,
                }
              }
            template = {
                "displayFieldName": "",
                "geometryType": "esriGeometryPolygon",
                "spatialReference": {
                 "wkid": 4326,
                 "latestWkid": 4326
                },
                "fields": [
                 {
                  "name": "OID",
                  "type": "esriFieldTypeOID",
                  "alias": "OID"
                 },
                 {
                  "name": "updateGeom_Length",
                  "type": "esriFieldTypeDouble",
                  "alias": "updateGeom_Length"
                 },
                 {
                  "name": "updateGeom_Area",
                  "type": "esriFieldTypeDouble",
                  "alias": "updateGeom_Area"
                 }
                ],
                "features": [feature_template],
                "exceededTransferLimit": false
               }
            params["areaOfInterest"] = template
        if async == True:
            return self._do_get(url=url, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
        else:
            exportJob = self._do_get(url=url, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
            jobUrl = "%s/jobs/%s" % (url, exportJob['jobId'])
            gpJob = GPJob(url=jobUrl,
                          securityHandler=self._securityHandler,
                          proxy_port=self._proxy_port,
                          proxy_url=self._proxy_url)
            status = gpJob.jobStatus
            while status != "esriJobSucceeded":
                if status in ['esriJobFailed',
                                       'esriJobCancelling',
                                       'esriJobCancelled']:
                    return None
                else:
                    time.sleep(5)
                    status = gpJob.jobStatus
            allResults = gpJob.getAllResults
            for k,v in allResults.iteritems():
                if k == "out_service_url":
                    value = v['value']
                    params = {
                        "f" : "json"
                    }
                    if not self._securityHandler is None:
                        params['token'] = self._securityHandler.token
                    gpRes = self._do_get(url=v['value'],
                                         param_dict=params,
                                         proxy_url=self._proxy_url,
                                         proxy_port=self._proxy_port)
                    if tilePackage == True:
                        files = []
                        for f in gpRes['files']:
                            name = f['name']
                            dlURL = f['url']
                            files.append(
                                self._download_file(url=dlURL,
                                                    save_path=tempfile.gettempdir(),
                                                    file_name=name,
                                                    param_dict=params,
                                                    proxy_url=self._proxy_url,
                                                    proxy_port=self._proxy_port)
                            )
                        return files
                    else:
                        return gpRes['folders']
                else:
                    return None






