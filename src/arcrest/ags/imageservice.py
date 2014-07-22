from base import BaseAGSServer

########################################################################
class ImageService(BaseAGSServer):
    """
       An image service provides access to raster data through a web
       service. Multiple rasters can be served as one image service through
       mosaic dataset technology, dynamically processed and mosaicked on
       the fly. An image service supports accessing both the mosaicked
       image and its catalog, as well as individual rasters in the catalog.
    """
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
    #----------------------------------------------------------------------
    def __init__(self, url, token_url=None, username=None, password=None,
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._url = url
        self_token_url = token_url
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
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(self._url, params)
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