from base import BaseAGSServer
from layer import FeatureLayer, TableLayer
import filters
import geometry
import common
import layer
########################################################################
class MapService(BaseAGSServer):
    """ contains information about a map service """
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
    #----------------------------------------------------------------------
    def __init__(self, url, token_url=None, username=None, password=None,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._url = url 
        self._token_url = token_url 
        self._username = username
        self._password = password
        if not username is None and \
           not password is None and \
           not username is "" and \
           not password is "":
            if not token_url is None:
                res = self.generate_token(tokenURL=token_url,
                                              proxy_port=proxy_port,
                                            proxy_url=proxy_url)
            else:   
                res = self.generate_token(proxy_port=self._proxy_port,
                                                       proxy_url=self._proxy_url)                
            if res is None:
                print "Token was not generated"
            elif 'error' in res:
                print res
            else:
                self._token = res[0]
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates all the properties for the map service """
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
            if k == "tables":
                self._tables = []
                for tbl in v:
                    self._tables.append(
                        layer.TableLayer(url,
                                         token_url=self._token_url,
                                         username=self._username,
                                         password=self._password)
                    )
            elif k == "layers":
                self._layers = []
                for lyr in v:
                    url = self._url + "/%s" % lyr['id']
                    layer_type = self._getLayerType(url)
                    if layer_type == "Feature Layer":
                        self._layers.append(
                            layer.FeatureLayer(url,
                                               token_url=self._token_url,
                                               username=self._username,
                                               password=self._password)
                        )
                    elif layer_type == "Raster Layer":
                        self._layers.append(
                            layer.RasterLayer(url,
                                               token_url=self._token_url,
                                               username=self._username,
                                               password=self._password)
                        )
                    elif layer_type == "Group Layer":
                        self._layers.append(
                            layer.GroupLayer(url,
                                             token_url=self._token_url,
                                             username=self._username,
                                             password=self._password)
                        )
                    else:
                        print 'Type %s is not implemented' % layer_type
            elif k in attributes:
                setattr(self, "_"+ k, json_dict[k])

            else:
                print k, " is not implemented for mapservice."
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
            qResults.append(common.Feature(r))
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
        return common.Feature(
            json_string=self._do_get(url=url,
                                     param_dict=params)
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
        #return self._do_get(url, param_dict)
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
               isinstance(dynamicLayers, base.DynamicData):
                params['dynamicLayers'] = dynamicLayers.asDictionary
            if mapScale is not None:
                params['mapScale'] = mapScale
            exportURL = self._url + "/export"
            return self._do_get(url=exportURL,
                                param_dict=params)
        else:
            return None

