from .._abstract.abstract import BaseSecurityHandler, BaseAGSServer
from ..security.security import AGSTokenSecurityHandler, PortalServerSecurityHandler
from ..common.general import MosaicRuleObject, local_time_to_online
import datetime, urllib
from ..common import filters
from ..security import security
########################################################################
class ImageService(BaseAGSServer):
    """
       An image service provides access to raster data through a web
       service. Multiple rasters can be served as one image service through
       mosaic dataset technology, dynamically processed and mosaicked on
       the fly. An image service supports accessing both the mosaicked
       image and its catalog, as well as individual rasters in the catalog.
    """
    _proxy_url = None
    _proxy_port = None
    _maxDownloadSizeLimit = None
    _meanValues = None
    _initialExtent = None
    _pixelSizeY = None
    _pixelSizeX = None
    _hasColormap = None
    _defaultMosaicMethod = None
    _spatialReference = None
    _supportsAdvancedQueries = None
    _stdvValues = None
    _serviceDataType = None
    _description = None
    _allowComputeTiePoints = None
    _maxDownloadImageCount = None
    _capabilities = None
    _minValues = None
    _ownershipBasedAccessControlForRasters = None
    _currentVersion = None
    _hasRasterAttributeTable = None
    _hasHistograms = None
    _bandCount = None
    _useStandardizedQueries = None
    _serviceDescription = None
    _maxRecordCount = None
    _maxMosaicImageCount = None
    _exportTilesAllowed = None
    _mosaicOperator = None
    _maxImageHeight = None
    _rasterFunctionInfos = None
    _defaultCompressionQuality = None
    _extent = None
    _objectIdField = None
    _fullExtent = None
    _maxPixelSize = None
    _rasterTypeInfos = None
    _mensurationCapabilities = None
    _name = None
    _supportsStatistics = None
    _sortField = None
    _maxImageWidth = None
    _minPixelSize = None
    _maxScale = None
    _sortValue = None
    _defaultResamplingMethod = None
    _maxValues = None
    _copyrightText = None
    _fields = None
    _allowRasterFunction = None
    _minScale = None
    _pixelType = None
    _editFieldsInfo = None
    _allowedMosaicMethods = None
    _tileInfo = None
    _singleFusedMapCache = None
    _securityHandler = None
    _hasMultidimensions = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if securityHandler is not None and \
           isinstance(securityHandler,
                      (security.AGSTokenSecurityHandler,
                       security.PortalServerSecurityHandler)):
            self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        elif securityHandler is None:
            pass
        else:
            raise AttributeError("Security Handler must type of AGSTokenSecurityHandler")
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        if self._securityHandler is not None:
            params['token'] = self.securityHandler.token
        json_dict = self._do_get(self._url, params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implmented for Image Service."
    #----------------------------------------------------------------------
    @property
    def hasMultidimensions(self):
        """returns the hasMultidimensions property"""
        if self._hasMultidimensions is None:
            self.__init()
        return self._hasMultidimensions
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
            if isinstance(value, (AGSTokenSecurityHandler,
                                  PortalServerSecurityHandler)):
                self._securityHandler = value
                self._token = value.token
            else:
                pass
        elif value is None:
            self._securityHandler = None
            self._token = None
    #----------------------------------------------------------------------
    @property
    def tileInfo(self):
        """ returns the tile information """
        if self._tileInfo is None:
            self.__init()
        return self._tileInfo
    #----------------------------------------------------------------------
    @property
    def singleFusedMapCache(self):
        """ returns the single fused map cache info """
        if self._singleFusedMapCache is None:
            self.__init()
        return self._singleFusedMapCache


    @property
    def maxDownloadSizeLimit(self):
        """ reutrns the max download size """
        if self._maxDownloadSizeLimit is None:
            self.__init()
        return self._maxDownloadSizeLimit
    @property
    def meanValues(self):
        if self._meanValues is None:
            self.__init()
        return self._meanValues
    @property
    def initialExtent(self):
        if self._initialExtent is None:
            self.__init()
        return self._initialExtent
    @property
    def pixelSizeY(self):
        if self._pixelSizeY is None:
            self.__init()
        return self._pixelSizeY
    @property
    def pixelSizeX(self):
        if self._pixelSizeX is None:
            self.__init()
        return self._pixelSizeX
    @property
    def hasColormap(self):
        if self._hasColormap is None:
            self.__init()
        return self._hasColormap
    @property
    def defaultMosaicMethod(self):
        if self._defaultMosaicMethod  is None:
            self.__init()
        return self._defaultMosaicMethod
    @property
    def spatialReference(self):
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    @property
    def allowedMosaicMethods(self):
        if self._allowedMosaicMethods is None:
            self.__init()
        return self._allowedMosaicMethods
    @property
    def editFieldsInfo(self):
        if self._editFieldsInfo is None:
            self.__init()
        return self._editFieldsInfo
    @property
    def pixelType(self):
        if self._pixelType is None:
            self.__init()
        return self._pixelType
    @property
    def minScale(self):
        if self._minScale is None:
            self.__init()
        return self._minScale
    @property
    def allowRasterFunction(self):
        if self._allowRasterFunction is None:
            self.__init()
        return self._allowRasterFunction
    @property
    def fields(self):
        if self._fields is None:
            self.__init()
        return self._fields
    @property
    def copyrightText(self):
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    @property
    def maxValues(self):
        if self._maxValues is None:
            self.__init()
        return self._maxValues
    @property
    def defaultResamplingMethod(self):
        if self._defaultResamplingMethod is None:
            self.__init()
        return self._defaultResamplingMethod
    @property
    def sortValue(self):
        if self._sortValue is None:
            self.__init()
        return self._sortValue
    @property
    def maxScale(self):
        if self._maxScale is None:
            self.__init()
        return self._maxScale
    @property
    def minPixelSize(self):
        if self._minPixelSize is None:
            self.__init()
        return self._minPixelSize
    @property
    def maxImageWidth(self):
        if self._maxImageWidth is None:
            self.__init()
        return self._maxImageWidth
    @property
    def sortField(self):
        if self._sortField is None:
            self.__init()
        return self._sortField
    @property
    def supportsStatistics(self):
        if self._supportsStatistics is None:
            self.__init()
        return self._supportsStatistics
    @property
    def name(self):
        if self._name is None:
            self.__init()
        return self._name
    @property
    def mensurationCapabilities(self):
        if self._mensurationCapabilities is None:
            self.__init()
        return self._mensurationCapabilities
    @property
    def rasterTypeInfos(self):
        if self._rasterTypeInfos is None:
            self.__init()
        return self._rasterTypeInfos
    @property
    def maxPixelSize(self):
        if self._maxPixelSize is None:
            self.__init()
        return self._maxPixelSize
    @property
    def objectIdField(self):
        if self._objectIdField is None:
            self.__init()
        return self._objectIdField
    @property
    def fullExtent(self):
        if self._fullExtent is None:
            self.__init()
        return self._fullExtent
    @property
    def extent(self):
        if self._extent is None:
            self.__init()
        return self._extent
    @property
    def defaultCompressionQuality(self):
        if self._defaultCompressionQuality is None:
            self.__init()
        return self._defaultCompressionQuality
    @property
    def rasterFunctionInfos(self):
        if self._rasterFunctionInfos is None:
            self.__init()
        return self._rasterFunctionInfos
    @property
    def maxImageHeight(self):
        if self._maxImageHeight is None:
            self.__init()
        return self._maxImageHeight
    @property
    def exportTilesAllowed(self):
        if self._exportTilesAllowed is None:
            self.__init()
        return self._exportTilesAllowed
    @property
    def mosaicOperator(self):
        if self._mosaicOperator is None:
            self.__init()
        return self._mosaicOperator
    @property
    def maxMosaicImageCount(self):
        if self._maxMosaicImageCount is None:
            self.__init()
        return self._maxMosaicImageCount
    @property
    def maxRecordCount(self):
        if self._maxRecordCount is None:
            self.__init()
        return self._maxRecordCount
    @property
    def serviceDescription(self):
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    @property
    def useStandardizedQueries(self):
        if self._useStandardizedQueries is None:
            self.__init()
        return self._useStandardizedQueries
    @property
    def bandCount(self):
        if self._bandCount is None:
            self.__init()
        return self._bandCount
    @property
    def hasHistograms(self):
        if self._hasHistograms is None:
            self.__init()
        return self._hasHistograms
    @property
    def hasRasterAttributeTable(self):
        if self._hasRasterAttributeTable is None:
            self.__init()
        return self._hasRasterAttributeTable
    @property
    def currentVersion(self):
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    @property
    def ownershipBasedAccessControlForRasters(self):
        if self._ownershipBasedAccessControlForRasters is None:
            self.__init()
        return self._ownershipBasedAccessControlForRasters
    @property
    def minValues(self):
        if self._minValues is None:
            self.__init()
        return self._minValues
    @property
    def capabilities(self):
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    @property
    def maxDownloadImageCount(self):
        if self._maxDownloadImageCount is None:
            self.__init()
        return self._maxDownloadImageCount
    @property
    def allowComputeTiePoints(self):
        if self._allowComputeTiePoints is None:
            self.__init()
        return self._allowComputeTiePoints
    @property
    def description(self):
        if self._description is None:
            self.__init()
        return self._description
    @property
    def serviceDataType(self):
        if self._serviceDataType is None:
            self.__init()
        return self._serviceDataType
    @property
    def stdvValues(self):
        if self._stdvValues is None:
            self.__init()
        return self._stdvValues
    @property
    def supportsAdvancedQueries(self):
        if self._supportsAdvancedQueries is None:
            self.__init()
        return self._supportsAdvancedQueries
    #----------------------------------------------------------------------
    def exportImage(self,
                    bbox,
                    imageSR,
                    bboxSR,
                    size=[400,400],
                    time=None,
                    format="jpgpng",
                    pixelType="UNKNOWN",
                    noData=None,
                    noDataInterpretation="esriNoDataMatchAny",
                    interpolation=None,
                    compression=None,
                    compressionQuality=75,
                    bandIds=None,
                    moasiacRule=None,
                    renderingRule="",
                    f="json",
                    saveFolder=None,
                    saveFile=None
                    ):
        """
        The exportImage operation is performed on an image service resource
        The result of this operation is an image resource. This resource
        provides information about the exported image, such as its URL,
        extent, width, and height.
        In addition to the usual response formats of HTML and JSON, you can
        also request the image format while performing this operation. When
        you perform an export with the image format , the server responds
        by directly streaming the image bytes to the client. With this
        approach, you don't get any information associated with the
        exported image other than the image itself.

        Inputs:
           bbox - The extent (bounding box) of the exported image. Unless
                  the bboxSR parameter has been specified, the bbox is
                  assumed to be in the spatial reference of the image
                  service.
           imageSR - The spatial reference of the exported image.
           bboxSR - The spatial reference of the bbox.
           size - The size (width * height) of the exported image in
                  pixels. If size is not specified, an image with a default
                  size of 400 * 400 will be exported.
           time - The time instant or the time extent of the exported image.
           format - The format of the exported image. The default format is
                    jpgpng.
                    Values: jpgpng | png | png8 | png24 | jpg | bmp | gif |
                            tiff | png32
           pixelType - The pixel type, also known as data type, pertains to
                       the type of values stored in the raster, such as
                       signed integer, unsigned integer, or floating point.
                       Integers are whole numbers, whereas floating points
                       have decimals.
           noDate - The pixel value representing no information.
           noDataInterpretation - Interpretation of the noData setting. The
                               default is esriNoDataMatchAny when noData is
                               a number, and esriNoDataMatchAll when noData
                               is a comma-delimited string:
                               esriNoDataMatchAny | esriNoDataMatchAll.
           interpolation - The resampling process of extrapolating the
                           pixel values while transforming the raster
                           dataset when it undergoes warping or when it
                           changes coordinate space.
           compression - Controls how to compress the image when exporting
                         to TIFF format: None, JPEG, LZ77. It does not
                         control compression on other formats.
           compressionQuality - Controls how much loss the image will be
                                subjected to by the compression algorithm.
                                Valid value ranges of compression quality
                                are from 0 to 100.
           bandIds - If there are multiple bands, you can specify a single
                     band to export, or you can change the band combination
                     (red, green, blue) by specifying the band number. Band
                     number is 0 based.
           mosaicRule - Specifies the mosaic rule when defining how
                        individual images should be mosaicked. When a mosaic
                        rule is not specified, the default mosaic rule of
                        the image service will be used (as advertised in
                        the root resource: defaultMosaicMethod,
                        mosaicOperator, sortField, sortValue).
           renderingRule - Specifies the rendering rule for how the
                           requested image should be rendered.
           f - The response format.  default is json
               Values: json | image | kmz
        """
        params = {
            "bbox" : bbox,
            "imageSR": imageSR,
            "bboxSR": bboxSR,
            "size" : "%s %s" % (size[0], size[1]),
            "pixelType" : pixelType,
            "compressionQuality" : compressionQuality,

        }
        url = self._url + "/exportImage"
        __allowedFormat = ["jpgpng", "png",
                           "png8", "png24",
                           "jpg", "bmp",
                           "gif", "tiff",
                           "png32"]
        __allowedPixelTypes = [
            "C128", "C64", "F32",
            "F64", "S16", "S32",
            "S8", "U1", "U16",
            "U2", "U32", "U4",
            "U8", "UNKNOWN"
        ]
        __allowednoDataInt = [
            "esriNoDataMatchAny",
            "esriNoDataMatchAll"
        ]
        __allowedInterpolation = [
            "RSP_BilinearInterpolation",
            "RSP_CubicConvolution",
            "RSP_Majority",
            "RSP_NearestNeighbor"
        ]
        __allowedCompression = [
            "JPEG", "LZ77"
        ]
        if isinstance(moasiacRule,MosaicRuleObject):
            params["moasiacRule"] = moasiacRule.value
        if format in __allowedFormat:
            params['format'] = format
        if isinstance(time, datetime.datetime):
            params['time'] = local_time_to_online(time)
        if interpolation is not None and \
           interpolation in __allowedInterpolation and \
           isinstance(interpolation, str):
            params['interpolation'] = interpolation
        if pixelType is not None and \
           pixelType in __allowedPixelTypes:
            params['pixelType'] = pixelType
        if noDataInterpretation in __allowedInterpolation:
            params['noDataInterpretation']  = noDataInterpretation
        if noData is not None:
            params['noData'] = noData
        if compression is not None and \
           compression in __allowedCompression:
            params['compression'] = compression
        if bandIds is not None and \
           isinstance(bandIds, list):
            params['bandIds'] = ",".join(bandIds)
        if renderingRule is not None:
            params['renderingRule'] = renderingRule
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token
        params["f" ] = f
        if f == "json":
            return self._do_get(url=url,
                                param_dict=params,
                                proxy_port=self._proxy_port,
                                proxy_url=self._proxy_url)
        elif f == "image":
            url = url + "?%s"  % urllib.urlencode(params)
            print url
            return self._download_file(url=url,
                                       save_path=saveFolder,
                                       file_name=saveFile)
        elif f == "kmz":
            url = url + "?%s"  % urllib.urlencode(params)
            return self._download_file(url=url,
                                       save_path=saveFolder,
                                       file_name=saveFile)
    #----------------------------------------------------------------------
    def query(self,
              where="1=1",
              out_fields="*",
              timeFilter=None,
              geometryFilter=None,
              returnGeometry=True,
              returnIDsOnly=False,
              returnCountOnly=False,
              pixelSize=None,
              orderByFields=None,
              returnDistinctValues=True,
              outStatistics=None,
              groupByFieldsForStatistics=None
              ):
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
               pixelSize-Query visible rasters at a given pixel size. If
                         pixelSize is not specified, rasters at all
                         resolutions can be queried.
               orderByFields-Order results by one or more field names. Use
                             ASC or DESC for ascending or descending order,
                             respectively
               returnDistinctValues-  If true, returns distinct values
                                    based on the fields specified in
                                    outFields. This parameter applies only
                                    if the supportsAdvancedQueries property
                                    of the image service is true.
               outStatistics- the definitions for one or more field-based
                              statistics to be calculated.
               groupByFieldsForStatistics-One or more field names using the
                                         values that need to be grouped for
                                         calculating the statistics.
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
        if not self._securityHandler is None:
            params["token"] = self._securityHandler.token
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
        if pixelSize is not None:
            params['pixelSize'] = pixelSize
        if orderByFields is not None:
            params['orderByFields'] = orderByFields
        if returnDistinctValues is not None:
            params['returnDistinctValues'] = returnDistinctValues

        url = self._url + "/query"
        return self._do_get(url=url, param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def addRasters(self,
            rasterType,
            itemIds=None,
            serviceUrl=None,
            computeStatistics=False,
            buildPyramids=False,
            buildThumbnail=False,
            minimumCellSizeFactor=None,
            maximumCellSizeFactor=None,
            attributes=None,
            geodataTransforms=None,
            geodataTransformApplyMethod="esriGeodataTransformApplyAppend"
            ):
        """
        This operation is supported at 10.1 and later.
        The Add Rasters operation is performed on an image service resource.
        The Add Rasters operation adds new rasters to an image service
        (POST only).
        The added rasters can either be uploaded items, using the itemIds
        parameter, or published services, using the serviceUrl parameter.
        If itemIds is specified, uploaded rasters are copied to the image
        service's dynamic image workspace location; if the serviceUrl is
        specified, the image service adds the URL to the mosaic dataset no
        raster files are copied. The serviceUrl is required input for the
        following raster types: Image Service, Map Service, WCS, and WMS.

        Inputs:

        itemIds - The upload items (raster files) to be added. Either
         itemIds or serviceUrl is needed to perform this operation.
            Syntax: itemIds=<itemId1>,<itemId2>
            Example: itemIds=ib740c7bb-e5d0-4156-9cea-12fa7d3a472c,
                             ib740c7bb-e2d0-4106-9fea-12fa7d3a482c
        serviceUrl - The URL of the service to be added. The image service
         will add this URL to the mosaic dataset. Either itemIds or
         serviceUrl is needed to perform this operation. The service URL is
         required for the following raster types: Image Service, Map
         Service, WCS, and WMS.
            Example: serviceUrl=http://myserver/arcgis/services/Portland/ImageServer
        rasterType - The type of raster files being added. Raster types
         define the metadata and processing template for raster files to be
         added. Allowed values are listed in image service resource.
            Example: Raster Dataset | CADRG/ECRG | CIB | DTED | Image Service | Map Service | NITF | WCS | WMS
        computeStatistics - If true, statistics for the rasters will be
         computed. The default is false.
            Values: false | true
        buildPyramids - If true, builds pyramids for the rasters. The
         default is false.
                Values: false | true
        buildThumbnail	 - If true, generates a thumbnail for the rasters.
         The default is false.
                Values: false | true
        minimumCellSizeFactor - The factor (times raster resolution) used
         to populate the MinPS field (maximum cell size above which the
         raster is visible).
                Syntax: minimumCellSizeFactor=<minimumCellSizeFactor>
                Example: minimumCellSizeFactor=0.1
        maximumCellSizeFactor - The factor (times raster resolution) used
         to populate MaxPS field (maximum cell size below which raster is
         visible).
                Syntax: maximumCellSizeFactor=<maximumCellSizeFactor>
                Example: maximumCellSizeFactor=10
        attributes - Any attribute for the added rasters.
                Syntax:
                {
                  "<name1>" : <value1>,
                  "<name2>" : <value2>
                }
                Example:
                {
                  "MinPS": 0,
                  "MaxPS": 20;
                  "Year" : 2002,
                  "State" : "Florida"
                }
        geodataTransforms - The geodata transformations applied on the
         added rasters. A geodata transformation is a mathematical model
         that performs a geometric transformation on a raster; it defines
         how the pixels will be transformed when displayed or accessed.
         Polynomial, projective, identity, and other transformations are
         available. The geodata transformations are applied to the dataset
         that is added.
                Syntax:
                [
                {
                  "geodataTransform" : "<geodataTransformName1>",
                  "geodataTransformArguments" : {<geodataTransformArguments1>}
                  },
                  {
                  "geodataTransform" : "<geodataTransformName2>",
                  "geodataTransformArguments" : {<geodataTransformArguments2>}
                  }
                ]
         The syntax of the geodataTransformArguments property varies based
         on the specified geodataTransform name. See Geodata Transformations
         documentation for more details.
        geodataTransformApplyMethod - This parameter defines how to apply
         the provided geodataTransform. The default is
         esriGeodataTransformApplyAppend.
                Values: esriGeodataTransformApplyAppend |
                esriGeodataTransformApplyReplace |
                esriGeodataTransformApplyOverwrite
        """
        url = self._url + "/add"
        params = {
            "f" : "json"
        }
        if not self._securityHandler is None:
            params['token'] = self._securityHandler.token
        if itemIds is None and serviceUrl is None:
            raise Exception("An itemId or serviceUrl must be provided")
        if isinstance(itemIds, str):
            itemIds = [itemIds]
        if isinstance(serviceUrl, str):
            serviceUrl = [serviceUrl]
        params['geodataTransformApplyMethod'] = geodataTransformApplyMethod
        params['rasterType'] = rasterType
        params['buildPyramids'] = buildPyramids
        params['buildThumbnail'] = buildThumbnail
        params['minimumCellSizeFactor'] = minimumCellSizeFactor
        params['computeStatistics'] = computeStatistics
        params['maximumCellSizeFactor'] = maximumCellSizeFactor
        params['attributes'] = attributes
        params['geodataTransforms'] = geodataTransforms
        if not itemIds is None:
            params['itemIds'] = itemIds
        if not serviceUrl is None:
            params['serviceUrl'] = serviceUrl
        return self._do_post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def colormap(self):
        """
        The colormap resource returns RGB color representation of pixel
        values. This resource is supported if the hasColormap property of
        the service is true.
        """
        if self.hasColormap:
            url = self._url + "/colormap"
            params = {
                "f" : "json"
            }
            if not self._securityHandler is None:
                params['token'] = self._securityHandler.token
            return self._do_get(url=url,
                                param_dict=params,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
        else:
            return None


