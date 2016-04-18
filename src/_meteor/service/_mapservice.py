"""

.. module:: _mapservice.py
   :platform: Windows, Linux
   :synopsis: Represents functions/classes used to control Map Services
              and map service layer

.. moduleauthor:: Esri

"""
import json
import time
from ..connection import SiteConnection
import tempfile
from ._base import BaseService
from ..common.geometry import Polygon, SpatialReference
from .geoprocessing import GPTask, GPService, GPJob
class MapService(BaseService):
    """
    """
    _con = None
    _json_dict = None
    _json = None
    _url = None
    _tileInfo = None
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
    _tileServers = None
    _supportsDynamicLayers = None
    _initialExtent = None
    _documentInfo = None
    _spatialReference = None
    _description = None
    _layers = None
    _tables = None
    _supportedImageFormatTypes = None
    _capabilities = None
    _mapName = None
    _currentVersion = None
    _units = None
    _supportedQueryFormats = None
    _maxRecordCount = None
    _exportTilesAllowed = None
    _maxImageHeight = None
    _supportedExtensions = None
    _fullExtent = None
    _singleFusedMapCache = None
    _maxImageWidth = None
    _maxScale = None
    _copyrightText = None
    _minScale = None
    _serviceDescription = None
    #----------------------------------------------------------------------
    def __init__(self, connection, url, initialize=False):
        """constructor"""
        self._con = connection
        self._url = url
        self._json_dict = None
        if initialize:
            self.__init(connection)
    #----------------------------------------------------------------------
    def __init(self, connection=None):
        """loads the properties"""
        params = {"f" : "json"}
        missing = {}
        if connection is None:
            connection = self._con
        result = connection.get(path_or_url=self._url, params=params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        if isinstance(result, dict):
            self._json_dict = result
            for k,v in result.items():
                if k in attributes:
                    setattr(self, "_" + k, v)
                else:
                    missing[k] = v
                    setattr(self, k, v)
                del k,v
        else:
            raise RuntimeError("Could not connect to the service: %s" % result)
        if len(missing.keys()) > 0:
            self.__dict__.update(missing)
    #----------------------------------------------------------------------
    @property
    def supportsDynamicLayers(self):
        """gets the supportsDynamicLayers value"""
        if self._supportsDynamicLayers is None:
            self.__init()
        return self._supportsDynamicLayers
    #----------------------------------------------------------------------
    @property
    def initialExtent(self):
        """gets the initialExtent value"""
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    #----------------------------------------------------------------------
    @property
    def documentInfo(self):
        """gets the documentInfo value"""
        if self._documentInfo is None:
            self.__init()
        return self._documentInfo
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """gets the spatialReference value"""
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets the description value"""
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def layers(self):
        """gets the layers value"""
        if self._layers is None:
            self.__init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def tables(self):
        """gets the tables value"""
        if self._tables is None:
            self.__init()
        return self._tables
    #----------------------------------------------------------------------
    @property
    def supportedImageFormatTypes(self):
        """gets the supportedImageFormatTypes value"""
        if self._supportedImageFormatTypes is None:
            self.__init()
        return self._supportedImageFormatTypes
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """gets the capabilities value"""
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def mapName(self):
        """gets the mapName value"""
        if self._mapName is None:
            self.__init()
        return self._mapName
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the currentVersion value"""
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def units(self):
        """gets the units value"""
        if self._units is None:
            self.__init()
        return self._units
    #----------------------------------------------------------------------
    @property
    def supportedQueryFormats(self):
        """gets the supportedQueryFormats value"""
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    #----------------------------------------------------------------------
    @property
    def maxRecordCount(self):
        """gets the maxRecordCount value"""
        if self._maxRecordCount is None:
            self.__init()
        return self._maxRecordCount
    #----------------------------------------------------------------------
    @property
    def exportTilesAllowed(self):
        """gets the exportTilesAllowed value"""
        if self._exportTilesAllowed is None:
            self.__init()
        return self._exportTilesAllowed
    #----------------------------------------------------------------------
    @property
    def maxImageHeight(self):
        """gets the maxImageHeight value"""
        if self._maxImageHeight is None:
            self.__init()
        return self._maxImageHeight
    #----------------------------------------------------------------------
    @property
    def supportedExtensions(self):
        """gets the supportedExtensions value"""
        if self._supportedExtensions is None:
            self.__init()
        return self._supportedExtensions
    #----------------------------------------------------------------------
    @property
    def fullExtent(self):
        """gets the fullExtent value"""
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    #----------------------------------------------------------------------
    @property
    def singleFusedMapCache(self):
        """gets the singleFusedMapCache value"""
        if self._singleFusedMapCache is None:
            self.__init()
        return self._singleFusedMapCache
    #----------------------------------------------------------------------
    @property
    def maxImageWidth(self):
        """gets the maxImageWidth value"""
        if self._maxImageWidth is None:
            self.__init()
        return self._maxImageWidth
    #----------------------------------------------------------------------
    @property
    def maxScale(self):
        """gets the maxScale value"""
        if self._maxScale is None:
            self.__init()
        return self._maxScale
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """gets the copyrightText value"""
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """gets the minScale value"""
        if self._minScale is None:
            self.__init()
        return self._minScale
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """gets the serviceDescription value"""
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def tileServers(self):
        """gets the tileServers value"""
        if self._tileServers is None:
            self.__init()
        return self._tileServers
    #----------------------------------------------------------------------
    @property
    def kml(self):
        url = "{url}/kml/mapImage.kmz".format(url=self._url)
        return self._con.get(path_or_url=url, params={"f" : 'json'},
                             file_name="mapImage.kmz",
                             out_folder=tempfile.gettempdir())
    #----------------------------------------------------------------------
    @property
    def itemInfo(self):
        """returns the service's item's infomation"""
        url = "{url}/info/iteminfo".format(url=self._url)
        params = {"f" : "json"}
        return self._con.get(path_or_url=url, params=params)
    #----------------------------------------------------------------------
    @property
    def metadata(self):
        """returns the service's XML metadata file"""
        url = "{url}/info/metadata".format(url=self._url)
        params = {"f" : "json"}
        return self._con.get(path_or_url=url, params=params)
    #----------------------------------------------------------------------
    def thumbnail(self, out_path=None):
        """"""
        if out_path is None:
            out_path = tempfile.gettempdir()
        url = "{url}/info/thumbnail".format(url=self._url)
        params = {"f" : "json"}
        if isinstance(self._con, SiteConnection): pass
        if out_path is None:
            out_path = tempfile.gettempdir()
        return self._con.get(path_or_url=url,
                             params=params,
                             out_folder=out_path,
                             file_name="thumbnail.png")
    #----------------------------------------------------------------------
    def identify(self,
                 geometry,
                 mapExtent,
                 imageDisplay,
                 tolerance,
                 geometryType="esriGeometryPoint",
                 sr=None,
                 layerDefs=None,
                 time=None,
                 layerTimeOptions=None,
                 layers="top",
                 returnGeometry=True,
                 maxAllowableOffset=None,
                 geometryPrecision=None,
                 dynamicLayers=None,
                 returnZ=False,
                 returnM=False,
                 gdbVersion=None):

        """
            The identify operation is performed on a map service resource
            to discover features at a geographic location. The result of this
            operation is an identify results resource. Each identified result
            includes its name, layer ID, layer name, geometry and geometry type,
            and other attributes of that result as name-value pairs.

            Inputs:
            geometry - The geometry to identify on. The type of the geometry is
                       specified by the geometryType parameter. The structure of
                       the geometries is same as the structure of the JSON geometry
                       objects returned by the ArcGIS REST API. In addition to the
                       JSON structures, for points and envelopes, you can specify
                       the geometries with a simpler comma-separated syntax.
                       Syntax:
                       JSON structures:
                       <geometryType>&geometry={ geometry}
                       Point simple syntax:
                       esriGeometryPoint&geometry=<x>,<y>
                       Envelope simple syntax:
                       esriGeometryEnvelope&geometry=<xmin>,<ymin>,<xmax>,<ymax>

            geometryType - The type of geometry specified by the geometry parameter.
                           The geometry type could be a point, line, polygon, or
                           an envelope.
                           Values:
                           esriGeometryPoint | esriGeometryMultipoint |
                           esriGeometryPolyline | esriGeometryPolygon |
                           esriGeometryEnvelope

            sr - The well-known ID of the spatial reference of the input and
                 output geometries as well as the mapExtent. If sr is not specified,
                 the geometry and the mapExtent are assumed to be in the spatial
                 reference of the map, and the output geometries are also in the
                 spatial reference of the map.

            layerDefs - Allows you to filter the features of individual layers in
                        the exported map by specifying definition expressions for
                        those layers. Definition expression for a layer that is
                        published with the service will be always honored.

            time - The time instant or the time extent of the features to be
            identified.

            layerTimeOptions - The time options per layer. Users can indicate
                               whether or not the layer should use the time extent
                               specified by the time parameter or not, whether to
                               draw the layer features cumulatively or not and the
                               time offsets for the layer.

            layers - The layers to perform the identify operation on. There are
                     three ways to specify which layers to identify on:
                     top: Only the top-most layer at the specified location.
                     visible: All visible layers at the specified location.
                     all: All layers at the specified location.

            tolerance - The distance in screen pixels from the specified geometry
                        within which the identify should be performed. The value for
                        the tolerance is an integer.

            mapExtent - The extent or bounding box of the map currently being viewed.
                        Unless the sr parameter has been specified, the mapExtent is
                        assumed to be in the spatial reference of the map.
                        Syntax: <xmin>, <ymin>, <xmax>, <ymax>
                        The mapExtent and the imageDisplay parameters are used by the
                        server to determine the layers visible in the current extent.
                        They are also used to calculate the distance on the map to
                        search based on the tolerance in screen pixels.

            imageDisplay - The screen image display parameters (width, height, and DPI)
                           of the map being currently viewed. The mapExtent and the
                           imageDisplay parameters are used by the server to determine
                           the layers visible in the current extent. They are also used
                           to calculate the distance on the map to search based on the
                           tolerance in screen pixels.
                           Syntax: <width>, <height>, <dpi>

            returnGeometry - If true, the resultset will include the geometries
                             associated with each result. The default is true.

            maxAllowableOffset - This option can be used to specify the maximum allowable
                                 offset to be used for generalizing geometries returned by
                                 the identify operation. The maxAllowableOffset is in the units
                                 of the sr. If sr is not specified, maxAllowableOffset is
                                 assumed to be in the unit of the spatial reference of the map.

            geometryPrecision - This option can be used to specify the number of decimal places
                                in the response geometries returned by the identify operation.
                                This applies to X and Y values only (not m or z-values).

            dynamicLayers - Use dynamicLayers property to reorder layers and change the layer
                            data source. dynamicLayers can also be used to add new layer that
                            was not defined in the map used to create the map service. The new
                            layer should have its source pointing to one of the registered
                            workspaces that was defined at the time the map service was created.
                            The order of dynamicLayers array defines the layer drawing order.
                            The first element of the dynamicLayers is stacked on top of all
                            other layers. When defining a dynamic layer, source is required.

            returnZ - If true, Z values will be included in the results if the features have
                      Z values. Otherwise, Z values are not returned. The default is false.
                      This parameter only applies if returnGeometry=true.

            returnM - If true, M values will be included in the results if the features have
                      M values. Otherwise, M values are not returned. The default is false.
                      This parameter only applies if returnGeometry=true.

            gdbVersion - Switch map layers to point to an alternate geodatabase version.
        """

        params= {'f': 'json',
                 'geometry': geometry,
                 'geometryType': geometryType,
                 'tolerance': tolerance,
                 'mapExtent': mapExtent,
                 'imageDisplay': imageDisplay
                 }

        if layerDefs is not None:
            params['layerDefs'] = layerDefs
        if layers is not None:
            params['layers'] = layers
        if sr is not None:
            params['sr'] = sr
        if time is not None:
            params['time'] = time
        if layerTimeOptions is not None:
            params['layerTimeOptions'] = layerTimeOptions
        if maxAllowableOffset is not None:
            params['maxAllowableOffset'] = maxAllowableOffset
        if geometryPrecision is not None:
            params['geometryPrecision'] = geometryPrecision
        if dynamicLayers is not None:
            params['dynamicLayers'] = dynamicLayers
        if gdbVersion is not None:
            params['gdbVersion'] = gdbVersion

        identifyURL = "{url}/identify".format(url=self._url)
        return self._con.get(path_or_url=identifyURL,
                         params=params)
    #----------------------------------------------------------------------
    def find(self, searchText, layers,
             contains=True, searchFields="",
             sr="", layerDefs="",
             returnGeometry=True, maxAllowableOffset="",
             geometryPrecision="", dynamicLayers="",
             returnZ=False, returnM=False, gdbVersion=""):
        """ performs the map service find operation """
        url = "{url}/find".format(url=self._url)
        params = {
            "f" : "json",
            "searchText" : searchText,
            "contains" : contains,
            "searchFields": searchFields,
            "sr" : sr,
            "layerDefs" : layerDefs,
            "returnGeometry" : returnGeometry,
            "maxAllowableOffset" : maxAllowableOffset,
            "geometryPrecision" : geometryPrecision,
            "dynamicLayers" : dynamicLayers,
            "returnZ" : returnZ,
            "returnM" : returnM,
            "gdbVersion" : gdbVersion,
            "layers" : layers
        }
        res = self._con.get(path_or_url=url, params=params)
        return res
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
        params= {
            "f" : "json",
            'docName' : docName,
            'layers' : layers,
            'layerOptions': layerOptions}
        return self._con.get(path_or_url=kmlURL,
                             out_folder=save_location,
                             params=params)
    #----------------------------------------------------------------------
    def exportMap(self,
                  bbox,
                  bboxSR=None,
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
            bbox - (Required) The extent (bounding box) of the exported
             image. Unless the bboxSR parameter has been specified, the bbox
             is assumed to be in the spatial reference of the map.
             Example: bbox="-104,35.6,-94.32,41"
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
         Output:
           Image of the map.
        """
        params = {
            "f" : "json"
        }
        params['bbox'] = bbox
        if bboxSR:
            params['bboxSR'] = bboxSR
        if dpi is not None:
            params['dpi'] = dpi
        if size is not None:
            params['size'] = size
        if imageSR is not None and \
           isinstance(imageSR, SpatialReference):
            params['imageSR'] = {'wkid': imageSR.wkid}
        if image_format is not None:
            params['format'] = image_format
        if layerDefFilter is not None:
            params['layerDefs'] = layerDefFilter
        if layers is not None:
            params['layers'] = layers
        if transparent is not None:
            params['transparent'] = transparent
        if timeFilter is not None:
            params['time'] = timeFilter
        if layerTimeOptions is not None:
            params['layerTimeOptions'] = layerTimeOptions
        if dynamicLayers is not None:
            params['dynamicLayers'] = dynamicLayers
        if mapScale is not None:
            params['mapScale'] = mapScale
        exportURL = self._url + "/export"
        return self._con.get(path_or_url=exportURL,
                             params=params)

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
        params["levels"] = levels
        if not areaOfInterest is None:
            params['areaOfInterest'] = areaOfInterest
        if async == True:
            return self._con.get(path_or_url=url,
                             params=params)
        else:
            exportJob = self._con.get(path_or_url=url,
                                  params=params)
            jobUrl = "%s/jobs/%s" % (url, exportJob['jobId'])
            gpJob = GPJob(connection=self._con,
                          url=jobUrl)

            status = gpJob.jobStatus
            while status != "esriJobSucceeded":
                if status in ['esriJobFailed',
                              'esriJobCancelling',
                              'esriJobCancelled']:
                    return gpJob.messages
                else:
                    time.sleep(5)
                    status = gpJob.jobStatus
            return gpJob.results
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
        if isinstance(areaOfInterest, Polygon):
            geom = areaOfInterest.asDictionary()
            template = { "features": [geom]}
            params["areaOfInterest"] = template
        elif isinstance(areaOfInterest, dict):
            params["areaOfInterest"] = { "features": [areaOfInterest]}
        if async == True:
            return self._con.get(path_or_url=url, params=params)
        else:
            exportJob = self._con.get(path_or_url=url, params=params)
            jobUrl = "%s/jobs/%s" % (url, exportJob['jobId'])
            gpJob = GPJob(url=jobUrl,
                          connection=self._con)
            status = gpJob.jobStatus
            while status != "esriJobSucceeded":
                if status in ['esriJobFailed',
                              'esriJobCancelling',
                              'esriJobCancelled']:
                    return None
                else:
                    time.sleep(5)
                    status = gpJob.jobStatus
            allResults = gpJob.results
            for k,v in allResults.items():
                if k == "out_service_url":
                    value = v.value
                    params = {
                        "f" : "json"
                    }
                    gpRes = self._con.get(path_or_url=v.value,
                                      params=params)
                    if tilePackage == True:
                        files = []
                        for f in gpRes['files']:
                            name = f['name']
                            dlURL = f['url']
                            files.append(
                                self._con.get(path_or_url=dlURL,
                                              out_folder=tempfile.gettempdir(),
                                              file_name=name,
                                              params=params))
                        return files
                    else:
                        return gpRes['folders']
                else:
                    return None
