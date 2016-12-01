from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseSecurityHandler, BaseAGSServer
from ..security import AGSTokenSecurityHandler, PortalServerSecurityHandler
from ..common.general import MosaicRuleObject, local_time_to_online
import datetime, urllib
import json
from ..common import filters
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
    _json = None
    _json_dict = None
    _advancedQueryCapabilities = None
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
        if securityHandler is not None:
            self._securityHandler = securityHandler
            self._referer_url = securityHandler.referer_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        json_dict = self._get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print (k, " - attribute not implemented for Image Service.")
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns the JSON response in key/value pairs"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.items():
            yield [k,v]
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
            else:
                pass
        elif value is None:
            self._securityHandler = None
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
    @property
    def advancedQueryCapabilities(self):
        if self._advancedQueryCapabilities is None:
            self.__init()
        return self._advancedQueryCapabilities
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
        params["f" ] = f
        if f == "json":
            return self._get(url=url,
                                param_dict=params,
                                securityHandler=self._securityHandler,
                                proxy_port=self._proxy_port,
                                proxy_url=self._proxy_url)
        elif f == "image":
            result = self._get(url=url,
                               param_dict=params,
                               securityHandler=self._securityHandler,
                               proxy_url=self._proxy_url,
                               proxy_port=self._proxy_port,
                               out_folder=saveFolder,
                               file_name=saveFile)
            return result
        elif f == "kmz":
            return self._get(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port,
                             out_folder=saveFolder,
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
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
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
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def identify(self,geometry,geometryType="esriGeometryPoint",mosaicRule=None,
                 renderingRule=None,renderingRules=None,pixelSize=None,time=None,
                 returnGeometry="false",returnCatalogItems="false"):
        """
        The identify operation is performed on an image service resource.
        It identifies the content of an image service for a given location
        and a given mosaic rule. The location can be a point or a polygon.
        The identify operation is supported by both mosaic dataset and raster
        dataset image services.
        The result of this operation includes the pixel value of the mosaic
        for a given mosaic rule, a resolution (pixel size), and a set of
        catalog items that overlap the given geometry. The single pixel value
        is that of the mosaic at the centroid of the specified location. If
        there are multiple rasters overlapping the location, the visibility
        of a raster is determined by the order of the rasters defined in the
        mosaic rule. It also contains a set of catalog items that overlap the
        given geometry. The catalog items are ordered based on the mosaic rule.
        A list of catalog item visibilities gives the percentage contribution
        of the item to overall mosaic.

        Inputs:

        geometry - A geometry that defines the location to be identified.
         The location can be a point or polygon. The structure of the geometry
         is the same as the structure of the JSON geometry objects returned by
         the ArcGIS REST API. In addition to the JSON structures, for points,
         you can specify the geometry with a simple comma-separated syntax.

         This is a required parameter. The default geometry type is a point.
         By default, the geometry is assumed to be in the spatial reference of
         the image service. You can specify a different spatial reference by
         using the JSON structure syntax for geometries.

        geometryType - The type of geometry specified by the geometry parameter.
         The geometry type can be a point or polygon. Values:
         esriGeometryPoint | esriGeometryPolygon

        mosaicRule - Specifies the mosaic rule when defining how individual images
         should be mosaicked. When a mosaic rule is not specified, the default
         mosaic rule of the image service will be used (as advertised in the root
         resource: defaultMosaicMethod, mosaicOperator, sortField, sortValue).

        renderingRule - Specifies the rendering rule for how the requested image
         should be rendered.

        renderingRules - Specifies an array of rendering rules. Use this parameter
         to get multiple processed values from different raster functions in one
         single request.

        pixelSize - The pixel level being identified (or the resolution being
         looked at). If pixel size is not specified, then pixelSize will default to
         the base resolution of the dataset. The raster at the specified pixel size
         in the mosaic dataset will be used for identify.
         The structure of the pixelSize parameter is the same as the structure of
         the point object returned by the ArcGIS REST API. In addition to the JSON
         structure, you can specify the pixel size with a simple comma-separated
         syntax.

        time - The time instant or time extent of the raster to be identified.
         This parameter is only valid if the image service supports time.

        returnGeometry - Indicates whether or not to return the raster catalog
         item's footprint. Set it to false when the catalog item's footprint is
         not needed to improve the identify operation's response time.

        returnCatalogItems - Indicates whether or not to return raster catalog
         items. Set it to false when catalog items are not needed to improve the
         identify operation's performance significantly. When set to false, neither
         the geometry nor attributes of catalog items will be returned.
        """

        url = self._url + "/identify"
        params = {
            "f" : "json",
            "geometry" : geometry,
            "geometryType": geometryType
        }
        if not mosaicRule is None:
            params["mosaicRule"] = mosaicRule
        if not renderingRule is None:
            params["renderingRule"] = renderingRule
        if not renderingRules is None:
            params["renderingRules"] = renderingRules
        if not pixelSize is None:
            params["pixelSize"] = pixelSize
        if not time is None:
            params["time"] = time
        if not returnGeometry is None:
            params["returnGeometry"] = returnGeometry
        if not returnCatalogItems is None:
            params["returnCatalogItems"] = returnCatalogItems

        return self._get(url=url,
                         param_dict=params,
                         securityHandler=self._securityHandler,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def measure(self,fromGeometry,toGeometry,measureOperation,
                geometryType="esriGeometryPoint",pixelSize=None,mosaicRule=None,
                linearUnit=None,angularUnit=None,areaUnit=None):
        """
        The measure operation is performed on an image service resource. It
        lets a user measure distance, direction, area, perimeter, and height
        from an image service. The result of this operation includes the name
        of the raster dataset being used, sensor name, and measured values.

        The measure operation can be supported by image services from raster
        datasets and mosaic datasets. Spatial reference is required to perform
        basic measurement (distance, area, and so on). Sensor metadata (geodata
        transformation) needs to be present in the data source used by an image
        service to enable height measurement (for example, imagery with RPCs).
        The mosaic dataset or service needs to include DEM to perform 3D measure.

        Users can provide arguments to the measure operation as query parameters.

        Inputs:

        fromGeometry - A geometry that defines the "from" location of the
         measurement. The structure of the geometry is the same as the structure
         of the JSON geometry objects returned by the ArcGIS REST API. In addition
         to the JSON structures, for points, you can specify the geometry with a
         simple comma-separated syntax.
         By default, the geometry is assumed to be in the spatial reference of
         the image service. You can specify a different spatial reference by
         using the JSON structure syntax for geometries.

         toGeometry - A geometry that defines the "to" location of the measurement.
         The type of geometry must be the same as fromGeometry. The structure of
         the geometry is the same as the structure of the JSON geometry objects
         returned by the ArcGIS REST API. In addition to the JSON structures, for
         points, you can specify the geometry with a simple comma-separated syntax.

         By default, the geometry is assumed to be in the spatial reference of
         the image service. You can specify a different spatial reference by
         using the JSON structure syntax for geometries.

        geometryType - The type of geometry specified by the fromGeometry and
         toGeometry parameters. The geometry type can be a point, polygon, or
         envelope. The default geometry type is point.
         Values: esriGeometryPoint | esriGeometryPolygon | esriGeometryEnvelope

        measureOperation - Specifies the type of measure being performed.
         Values: esriMensurationPoint | esriMensurationDistanceAndAngle |
         esriMensurationAreaAndPerimeter | esriMensurationHeightFromBaseAndTop |
         esriMensurationHeightFromBaseAndTopShadow |
         esriMensurationHeightFromTopAndTopShadow | esriMensurationCentroid |
         esriMensurationPoint3D | esriMensurationDistanceAndAngle3D |
         esriMensurationAreaAndPerimeter3D | esriMensurationCentroid3D

        pixelSize - The pixel level (resolution) being measured. If pixel size
         is not specified, pixelSize will default to the base resolution of the
         image service. The raster at the specified pixel size in the mosaic
         dataset will be used for measurement.
         The structure of the pixelSize parameter is the same as the structure
         of the point object returned by the ArcGIS REST API. In addition to the
         JSON structure, you can specify the pixel size with a simple
         comma-separated syntax.

        mosaicRule - Specifies the mosaic rule when defining how individual
         images should be mosaicked. When a mosaic rule is not specified, the
         default mosaic rule of the image service will be used (as advertised
         in the root resource: defaultMosaicMethod, mosaicOperator, sortField,
         sortValue). The first visible image is used by measure.

        linearUnit - The linear unit in which height, length, or perimeters
         will be calculated. It can be any of the following esriUnits constant.
         If the unit is not specified, the default is esriMeters. The list of
         valid esriUnits constants include:
         esriInches | esriFeet | esriYards | esriMiles | esriNauticalMiles |
         esriMillimeters | esriCentimeters | esriDecimeters | esriMeters |
         esriKilometers

        angularUnit - The angular unit in which directions of line segments
         will be calculated. It can be one of the following esriDirectionUnits
         constants: esriDURadians | esriDUDecimalDegrees
         If the unit is not specified, the default is esriDUDecimalDegrees.

        areaUnit - The area unit in which areas of polygons will be calculated.
         It can be any esriAreaUnits constant. If the unit is not specified, the
         default is esriSquareMeters. The list of valid esriAreaUnits constants
         include:
         esriSquareInches | esriSquareFeet | esriSquareYards | esriAcres |
         esriSquareMiles | esriSquareMillimeters | esriSquareCentimeters |
         esriSquareDecimeters | esriSquareMeters | esriAres | esriHectares |
         esriSquareKilometers
        """

        url = self._url + "/measure"
        params = {
            "f" : "json",
            "fromGeometry" : fromGeometry,
            "toGeometry": toGeometry,
            "geometryType": geometryType,
            "measureOperation": measureOperation
            }

        if not pixelSize is None:
            params["pixelSize"] = pixelSize
        if not mosaicRule is None:
            params["mosaicRule"] = mosaicRule
        if not linearUnit is None:
            params["linearUnit"] = linearUnit
        if not angularUnit is None:
            params["angularUnit"] = angularUnit
        if not areaUnit is None:
            params["areaUnit"] = areaUnit

        return self._get(url=url,
                         param_dict=params,
                         securityHandler=self._securityHandler,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def computeHistograms(self,geometry,geometryType,mosaicRule=None,
                          renderingRule=None,pixelSize=None):
        """
        The computeHistograms operation is performed on an image service resource.
        This operation is supported by any image service published with mosaic
        datasets or a raster dataset. The result of this operation is an array of
        histograms for all raster bands computed from the given extent.

        Inputs:

        geometry - A geometry that defines the geometry within which the histogram
         is computed. The geometry can be an envelope or a polygon. The structure of
         the geometry is the same as the structure of the JSON geometry objects
         returned by the ArcGIS REST API.

        geometryType - The type of geometry specified by the geometry parameter.
         The geometry type can be an envelope or polygon.
         Values: esriGeometryEnvelope | esriGeometryPolygon

        mosaicRule - Specifies the mosaic rule when defining how individual
         images should be mosaicked. When a mosaic rule is not specified, the
         default mosaic rule of the image service will be used (as advertised
         in the root resource: defaultMosaicMethod, mosaicOperator, sortField,
         sortValue).

        renderingRule - Specifies the rendering rule for how the requested
         image should be rendered.

        pixelSize - The pixel level being used (or the resolution being looked at).
         If pixel size is not specified, then pixelSize will default to the base
         resolution of the dataset. The raster at the specified pixel size in the
         mosaic dataset will be used for histogram calculation.
         The structure of the pixelSize parameter is the same as the structure of
         the point object returned by the ArcGIS REST API. In addition to the JSON
         structure, you can specify the pixel size with a simple comma-separated syntax.
        """

        url = self._url + "/computeHistograms"
        params = {
            "f" : "json",
            "geometry" : geometry,
            "geometryType": geometryType
            }

        if not mosaicRule is None:
            params["mosaicRule"] = mosaicRule
        if not renderingRule is None:
            params["renderingRule"] = renderingRule
        if not pixelSize is None:
            params["pixelSize"] = pixelSize

        return self._get(url=url,
                         param_dict=params,
                         securityHandler=self._securityHandler,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def computeStatisticsHistograms(self,geometry,geometryType,mosaicRule=None,
                                    renderingRule=None,pixelSize=None):
        """
        The computeStatisticsHistograms operation is performed on an image service
        resource. This operation is supported by any image service published with
        mosaic datasets or a raster dataset. The result of this operation contains
        both statistics and histograms computed from the given extent.

        Inputs:

        geometry - A geometry that defines the geometry within which the histogram
         is computed. The geometry can be an envelope or a polygon. The structure of
         the geometry is the same as the structure of the JSON geometry objects
         returned by the ArcGIS REST API.

        geometryType - The type of geometry specified by the geometry parameter.
         The geometry type can be an envelope or polygon.
         Values: esriGeometryEnvelope | esriGeometryPolygon

        mosaicRule - Specifies the mosaic rule when defining how individual
         images should be mosaicked. When a mosaic rule is not specified, the
         default mosaic rule of the image service will be used (as advertised
         in the root resource: defaultMosaicMethod, mosaicOperator, sortField,
         sortValue).

        renderingRule - Specifies the rendering rule for how the requested
         image should be rendered.

        pixelSize - The pixel level being used (or the resolution being looked at).
         If pixel size is not specified, then pixelSize will default to the base
         resolution of the dataset. The raster at the specified pixel size in the
         mosaic dataset will be used for histogram calculation.
         The structure of the pixelSize parameter is the same as the structure of
         the point object returned by the ArcGIS REST API. In addition to the JSON
         structure, you can specify the pixel size with a simple comma-separated syntax.
        """

        url = self._url + "/computeStatisticsHistograms"
        params = {
            "f" : "json",
            "geometry" : geometry,
            "geometryType": geometryType
        }

        if not mosaicRule is None:
            params["mosaicRule"] = mosaicRule
        if not renderingRule is None:
            params["renderingRule"] = renderingRule
        if not pixelSize is None:
            params["pixelSize"] = pixelSize

        return self._get(url=url,
                         param_dict=params,
                         securityHandler=self._securityHandler,
                         proxy_url=self._proxy_url,
                         proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getSamples(self,geometry,geometryType="esriGeometryPoint",
                   sampleDistance=None,sampleCount=None,mosaicRule=None,
                   pixelSize=None,returnFirstValueOnly=None,interpolation=None,
                   outFields=None):
        """
        The getSamples operation is performed on an image service resource.
        The getSamples operation is supported by both mosaic dataset and raster
        dataset image services.
        The result of this operation includes sample point locations, pixel
        values, and corresponding spatial resolutions of the source data for a
        given geometry. When the input geometry is a polyline, envelope, or
        polygon, sampling is based on sampleCount or sampleDistance; when the
        input geometry is a point or multipoint, the point or points are used
        directly.
        The number of sample locations in the response is based on the
        sampleDistance or sampleCount parameter and cannot exceed the limit of
        the image service (the default is 1000, which is an approximate limit).

        Inputs:

        geometry - A geometry that defines the location(s) to be sampled. The
         structure of the geometry is the same as the structure of the JSON
         geometry objects returned by the ArcGIS REST API. Applicable geometry
         types are point, multipoint, polyline, polygon, and envelope. When
         spatialReference is omitted in the input geometry, it will be assumed
         to be the spatial reference of the image service.

        geometryType - The type of geometry specified by the geometry parameter.
         The geometry type can be point, multipoint, polyline, polygon, or envelope.
         Values: esriGeometryPoint | esriGeometryMultipoint | esriGeometryPolyline |
         esriGeometryPolygon | esriGeometryEnvelope

        sampleDistance - The distance interval used to sample points from the
         provided path. The unit is the same as the input geometry. If neither
         sampleCount nor sampleDistance is provided, no densification can be done
         for paths (polylines), and a default sampleCount (100) is used for areas
         (polygons or envelopes).

        sampleCount - The approximate number of sample locations from the provided
         path. If neither sampleCount nor sampleDistance is provided, no
         densification can be done for paths (polylines), and a default
         sampleCount (100) is used for areas (polygons or envelopes).

        mosaicRule - Specifies the mosaic rule defining the image sort order.
         Additional filtering can be applied to the where clause and FIDs of a
         mosaic rule.

        pixelSize - The raster that is visible at the specified pixel size in the
         mosaic dataset will be used for sampling. If pixelSize is not specified,
         the service's pixel size is used.
         The structure of the esri_codephpixelSize parameter is the same as the
         structure of the point object returned by the ArcGIS REST API. In addition
         to the JSON structure, you can specify the pixel size with a simple
         comma-separated syntax.

        returnFirstValueOnly - Indicates whether to return all values at a point,
         or return the first non-NoData value based on the current mosaic rule.
         The default is true.

        interpolation - This parameter was added at 10.3. The resampling method.
         Default is nearest neighbor.

        outFields - This parameter was added at 10.3. The list of fields to be
         included in the response. This list is a comma-delimited list of field
         names. You can also specify the wildcard character (*) as the value of
         this parameter to include all the field values in the results.
        """

        url = self._url + "/getSamples"
        params = {
            "f" : "json",
            "geometry" : geometry,
            "geometryType": geometryType
        }

        if not sampleDistance is None:
            params["sampleDistance"] = sampleDistance
        if not sampleCount is None:
            params["sampleCount"] = sampleCount
        if not mosaicRule is None:
            params["mosaicRule"] = mosaicRule
        if not pixelSize is None:
            params["pixelSize"] = pixelSize
        if not returnFirstValueOnly is None:
            params["returnFirstValueOnly"] = returnFirstValueOnly
        if not interpolation is None:
            params["interpolation"] = interpolation
        if not outFields is None:
            params["outFields"] = outFields

        return self._get(url=url,
                         param_dict=params,
                         securityHandler=self._securityHandler,
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
            return self._get(url=url,
                                param_dict=params,
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
        else:
            return None
