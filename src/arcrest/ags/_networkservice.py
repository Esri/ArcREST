from .._abstract.abstract import BaseSecurityHandler, BaseAGSServer
from ..security.security import AGSTokenSecurityHandler
import json, types

########################################################################
class NetworkService(BaseAGSServer):
    """
    The network service resource represents a network analysis service
    published with ArcGIS Server. The resource provides information about
    the service such as the service description and the various network
    layers (route, closest facility, and service area layers) contained in
    the network analysis service.
    """
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None
    _routeLayers = None
    _currentVersion = None
    _serviceDescription = None
    _serviceAreaLayers = None
    _closestFacilityLayers = None
    _serviceLimits = None

    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if self._securityHandler is not None:
            self._referer_url = self._securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()

    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the properties """
        params = {
            "f" : "json",
        }
        json_dict = self._do_get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]

        for k,v in json_dict.iteritems():
            if k in attributes:
                if k == "routeLayers" and json_dict[k]:
                    self._routeLayers = []
                    for rl in v:
                        self._routeLayers.append(
                            RouteNetworkLayer(url=self._url + "/%s" % rl,
                                              securityHandler=self._securityHandler,
                                              proxy_url=self._proxy_url,
                                              proxy_port=self._proxy_port,
                                              initialize=False))

                elif k == "serviceAreaLayers" and json_dict[k]:
                    self._serviceAreaLayers = []
                    for sal in v:
                        self._serviceAreaLayers.append(
                            ServiceAreaNetworkLayer(url=self._url + "/%s" % sal,
                                                    securityHandler=self._securityHandler,
                                                    proxy_url=self._proxy_url,
                                                    proxy_port=self._proxy_port,
                                                    initialize=False))
                else:
                    setattr(self, "_"+ k, v)
            else:
                print "attribute %s is not implemented." % k
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """
        returns key/value pair
        """
        attributes = json.loads(str(self))
        for att in attributes.keys():
            yield [att, getattr(self, att)]

    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def routeLayers(self):
        if self._routeLayers is None:
            self.__init()
        return self._routeLayers
    #----------------------------------------------------------------------
    @property
    def serviceAreaLayers(self):
        if self._serviceAreaLayers is None:
            self.__init()
        return self._serviceAreaLayers
    #----------------------------------------------------------------------
    @property
    def closestFacilityLayers(self):
        if self._closestFacilityLayers is None:
            self.__init()
        return self._closestFacilityLayers
    #----------------------------------------------------------------------
    @property
    def serviceLimits(self):
        if self._serviceLimits is None:
            self.__init()
        return self._serviceLimits



########################################################################
class NetworkLayer(BaseAGSServer):
    """
    The network layer resource represents a single network layer in
    a network analysis service published by ArcGIS Server. It provides basic
    information about the network layer such as its name, type, and network
    classes. Additionally, depending on the layer type, it provides different
    pieces of information.

    It is a base class for RouteNetworkLayer, ServiceAreaNetworkLayer, and
    ClosestFacilityNetworkLayer.
    """
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None

    #common attrs for all Network Layer types
    _currentVersion = None
    _layerName = None
    _layerType = None
    _impedance = None
    _restrictions = None
    _snapTolerance = None
    _maxSnapTolerance = None
    _snapToleranceUnits = None
    _ignoreInvalidLocations = None
    _restrictUTurns = None
    _accumulateAttributeNames = None
    _attributeParameterValues = None
    _outputSpatialReference = None
    _useHierarchy = None
    _hierarchyAttributeName = None
    _hierarchyLevelCount = None
    _hierarchyMaxValues = None
    _hierarchyNumTransitions = None
    _networkClasses = None
    _networkDataset = None
    _hasM = None
    _hasZ = None
    _supportedTravelModes = None
    _serviceLimits = None

    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implemented in NetworkLayer."
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def layerName(self):
        if self._layerName is None:
            self.__init()
        return self._layerName
    #----------------------------------------------------------------------
    @property
    def layerType(self):
        if self._layerType is None:
            self.__init()
        return self._layerType
    #----------------------------------------------------------------------
    @property
    def impedance(self):
        if self._impedance is None:
            self.__init()
        return self._impedance
    #----------------------------------------------------------------------
    @property
    def restrictions(self):
        if self._restrictions is None:
            self.__init()
        return self._restrictions
    #----------------------------------------------------------------------
    @property
    def snapTolerance(self):
        if self._snapTolerance is None:
            self.__init()
        return self._snapTolerance
    #----------------------------------------------------------------------
    @property
    def maxSnapTolerance(self):
        if self._maxSnapTolerance is None:
            self.__init()
        return self._maxSnapTolerance
    #----------------------------------------------------------------------
    @property
    def snapToleranceUnits(self):
        if self._snapToleranceUnits is None:
            self.__init()
        return self._snapToleranceUnits
    #----------------------------------------------------------------------
    @property
    def ignoreInvalidLocations(self):
        if self._ignoreInvalidLocations is None:
            self.__init()
        return self._ignoreInvalidLocations
    #----------------------------------------------------------------------
    @property
    def restrictUTurns(self):
        if self._restrictUTurns is None:
            self.__init()
        return self._restrictUTurns
    #----------------------------------------------------------------------
    @property
    def accumulateAttributeNames(self):
        if self._accumulateAttributeNames is None:
            self.__init()
        return self._accumulateAttributeNames
    #----------------------------------------------------------------------
    @property
    def attributeParameterValues(self):
        if self._attributeParameterValues is None:
            self.__init()
        return self._attributeParameterValues
    #----------------------------------------------------------------------
    @property
    def outputSpatialReference(self):
        if self._outputSpatialReference is None:
            self.__init()
        return self._outputSpatialReference
    #----------------------------------------------------------------------
    @property
    def useHierarchy(self):
        if self._useHierarchy is None:
            self.__init()
        return self._useHierarchy
    #----------------------------------------------------------------------
    @property
    def hierarchyAttributeName(self):
        if self._hierarchyAttributeName is None:
            self.__init()
        return self._hierarchyAttributeName
    #----------------------------------------------------------------------
    @property
    def hierarchyLevelCount(self):
        if self._hierarchyLevelCount is None:
            self.__init()
        return self._hierarchyLevelCount
    #----------------------------------------------------------------------
    @property
    def hierarchyMaxValues(self):
        if self._hierarchyMaxValues is None:
            self.__init()
        return self._hierarchyMaxValues
    #----------------------------------------------------------------------
    @property
    def hierarchyNumTransitions(self):
        if self._hierarchyNumTransitions is None:
            self.__init()
        return self._hierarchyNumTransitions
    #----------------------------------------------------------------------
    @property
    def networkClasses(self):
        if self._networkClasses is None:
            self.__init()
        return self._networkClasses
    #----------------------------------------------------------------------
    @property
    def networkDataset(self):
        if self._networkDataset is None:
            self.__init()
        return self._networkDataset
    #----------------------------------------------------------------------
    @property
    def hasM(self):
        if self._hasM is None:
            self.__init()
        return self._hasM
    #----------------------------------------------------------------------
    @property
    def hasZ(self):
        if self._hasZ is None:
            self.__init()
        return self._hasZ
    #----------------------------------------------------------------------
    @property
    def supportedTravelModes(self):
        if self._supportedTravelModes is None:
            self.__init()
        return self._supportedTravelModes
    #----------------------------------------------------------------------
    @property
    def serviceLimits(self):
        if self._serviceLimits is None:
            self.__init()
        return self._serviceLimits


########################################################################
class RouteNetworkLayer(NetworkLayer):
    """
    The Route Network Layer which has common properties of any Network
    Layer as well as some attributes unique to Route Network Layer only.
    """

    #specific to Route
    _findBestSequence = None
    _useStartTime = None
    _startTime = None
    _startTimeIsUTC = None
    _useTimeWindows = None
    _preserveFirstStop = None
    _preserveLastStop = None
    _outputLineType = None
    _directionsLanguage = None
    _directionsSupportedLanguages = None
    _directionsStyleNames = None
    _directionsLengthUnits = None
    _directionsTimeAttribute = None

    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """ initializes all properties """
        NetworkLayer.__init__(self,url)

    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implemented in RouteNetworkLayer."

    #----------------------------------------------------------------------
    @property
    def directionsTimeAttribute(self):
        if self._directionsTimeAttribute is None:
            self.__init()
        return self._directionsTimeAttribute
    #----------------------------------------------------------------------
    @property
    def directionsLengthUnits(self):
        if self._directionsLengthUnits is None:
            self.__init()
        return self._directionsLengthUnits
    #----------------------------------------------------------------------
    @property
    def outputLineType(self):
        if self._outputLineType is None:
            self.__init()
        return self._outputLineType
    #----------------------------------------------------------------------
    @property
    def directionsLanguage(self):
        if self._directionsLanguage is None:
            self.__init()
        return self._directionsLanguage
    #----------------------------------------------------------------------
    @property
    def directionsSupportedLanguages(self):
        if self._directionsSupportedLanguages is None:
            self.__init()
        return self._directionsSupportedLanguages
    #----------------------------------------------------------------------
    @property
    def directionsStyleNames(self):
        if self._directionsStyleNames is None:
            self.__init()
        return self._directionsStyleNames
    #----------------------------------------------------------------------
    @property
    def useStartTime(self):
        if self._useStartTime is None:
            self.__init()
        return self._useStartTime
    #----------------------------------------------------------------------
    @property
    def startTime(self):
        if self._startTime is None:
            self.__init()
        return self._startTime
    #----------------------------------------------------------------------
    @property
    def startTimeIsUTC(self):
        if self._startTimeIsUTC is None:
            self.__init()
        return self._startTimeIsUTC
    #----------------------------------------------------------------------
    @property
    def useTimeWindows(self):
        if self._useTimeWindows is None:
            self.__init()
        return self._useTimeWindows
    #----------------------------------------------------------------------
    @property
    def preserveFirstStop(self):
        if self._preserveFirstStop is None:
            self.__init()
        return self._preserveFirstStop
    #----------------------------------------------------------------------
    @property
    def preserveLastStop(self):
        if self._preserveLastStop is None:
            self.__init()
        return self._preserveLastStop
    #----------------------------------------------------------------------
    @property
    def findBestSequence(self):
        if self._findBestSequence is None:
            self.__init()
        return self._findBestSequence

    #----------------------------------------------------------------------
    def solve(self,stops,
              method="POST",
              barriers=None,
              polylineBarriers=None,
              polygonBarriers=None,
              travelMode=None,
              attributeParameterValues=None,
              returnDirections=None,
              returnRoutes=True,
              returnStops=False,
              returnBarriers=False,
              returnPolylineBarriers=True,
              returnPolygonBarriers=True,
              outSR=None,
              ignoreInvalidLocations=True,
              outputLines=None,
              findBestSequence=False,
              preserveFirstStop=True,
              preserveLastStop=True,
              useTimeWindows=False,
              startTime=None,
              startTimeIsUTC=False,
              accumulateAttributeNames=None,
              impedanceAttributeName=None,
              restrictionAttributeNames=None,
              restrictUTurns=None,
              useHierarchy=True,
              directionsLanguage=None,
              directionsOutputType=None,
              directionsStyleName=None,
              directionsLengthUnits=None,
              directionsTimeAttributeName=None,
              outputGeometryPrecision=None,
              outputGeometryPrecisionUnits=None,
              returnZ=False
              ):
        """The solve operation is performed on a network layer resource.
        The solve operation is supported on a network layer whose layerType
        is esriNAServerRouteLayer. You can provide arguments to the solve
        route operation as query parameters"""

        if not self.layerType == "esriNAServerRouteLayer":
            raise ValueError("The solve operation is supported on a network "
                             "layer of Route type only")

        url = self._url + "/solve"
        params = {
                    "f" : "json",
                    "stops": stops
                 }

        if not barriers is None:
            params['barriers'] = barriers
        if not polylineBarriers is None:
            params['polylineBarriers'] = polylineBarriers
        if not polygonBarriers is None:
            params['polygonBarriers'] = polygonBarriers
        if not travelMode is None:
            params['travelMode'] = travelMode
        if not attributeParameterValues is None:
            params['attributeParameterValues'] = attributeParameterValues
        if not returnDirections is None:
            params['returnDirections'] = returnDirections
        if not returnRoutes is None:
            params['returnRoutes'] = returnRoutes
        if not returnStops is None:
            params['returnStops'] = returnStops
        if not returnBarriers is None:
            params['returnBarriers'] = returnBarriers
        if not returnPolylineBarriers is None:
            params['returnPolylineBarriers'] = returnPolylineBarriers
        if not returnPolygonBarriers is None:
            params['returnPolygonBarriers'] = returnPolygonBarriers
        if not outSR is None:
            params['outSR'] = outSR
        if not ignoreInvalidLocations is None:
            params['ignoreInvalidLocations'] = ignoreInvalidLocations
        if not outputLines is None:
            params['outputLines'] = outputLines
        if not findBestSequence is None:
            params['findBestSequence'] = findBestSequence
        if not preserveFirstStop is None:
            params['preserveFirstStop'] = preserveFirstStop
        if not preserveLastStop is None:
            params['preserveLastStop'] = preserveLastStop
        if not useTimeWindows is None:
            params['useTimeWindows'] = useTimeWindows
        if not startTime is None:
            params['startTime'] = startTime
        if not startTimeIsUTC is None:
            params['startTimeIsUTC'] = startTimeIsUTC
        if not accumulateAttributeNames is None:
            params['accumulateAttributeNames'] = accumulateAttributeNames
        if not impedanceAttributeName is None:
            params['impedanceAttributeName'] = impedanceAttributeName
        if not restrictionAttributeNames is None:
            params['restrictionAttributeNames'] = restrictionAttributeNames
        if not restrictUTurns is None:
            params['restrictUTurns'] = restrictUTurns
        if not useHierarchy is None:
            params['useHierarchy'] = useHierarchy
        if not directionsLanguage is None:
            params['directionsLanguage'] = directionsLanguage
        if not directionsOutputType is None:
            params['directionsOutputType'] = directionsOutputType
        if not directionsStyleName is None:
            params['directionsStyleName'] = directionsStyleName
        if not directionsLengthUnits is None:
            params['directionsLengthUnits'] = directionsLengthUnits
        if not directionsTimeAttributeName is None:
            params['directionsTimeAttributeName'] = directionsTimeAttributeName
        if not outputGeometryPrecision is None:
            params['outputGeometryPrecision'] = outputGeometryPrecision
        if not outputGeometryPrecisionUnits is None:
            params['outputGeometryPrecisionUnits'] = outputGeometryPrecisionUnits
        if not returnZ is None:
            params['returnZ'] = returnZ

        if method.lower() == "post":
            return self._do_post(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        else:
            return self._do_get(url=url,
                                param_dict=params,
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)


########################################################################
class ServiceAreaNetworkLayer(NetworkLayer):
    """
    The Service Area Network Layer which has common properties of Network
    Layer as well as some attributes unique to Service Area Network Layer
    only.
    """

    #specific to Service Area
    _outputLines = None
    _timeOfDayIsUTC = None
    _travelDirection = None
    _trimOuterPolygon = None
    _trimPolygonDistanceUnits = None
    _defaultBreaks = None
    _includeSourceInformationOnLines = None
    _overlapPolygons = None
    _timeOfDay = None
    _excludeSourcesFromPolygons = None
    _splitPolygonsAtBreaks = None
    _outputPolygons = None
    _overlapLines = None
    _trimPolygonDistance = None
    _splitLinesAtBreaks = None
    _timeOfDayUsage = None
    _mergeSimilarPolygonRanges = None

    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """initializes all properties"""
        NetworkLayer.__init__(self, url)

    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }

        # TODO handle spaces in the url, 'Service Area' should be 'Service+Area'
        self._url = self._url.replace(' ','+')
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implemented in ServiceAreaNetworkLayer."

    #----------------------------------------------------------------------
    @property
    def outputLines(self):
        if self._outputLines is None:
            self.__init()
        return self._outputLines
    #----------------------------------------------------------------------
    @property
    def timeOfDayIsUTC(self):
        if self._timeOfDayIsUTC is None:
            self.__init()
        return self._timeOfDayIsUTC
    #----------------------------------------------------------------------
    @property
    def travelDirection(self):
        if self._travelDirection is None:
            self.__init()
        return self._travelDirection
    #----------------------------------------------------------------------
    @property
    def trimOuterPolygon(self):
        if self._trimOuterPolygon is None:
            self.__init()
        return self._trimOuterPolygon
    #----------------------------------------------------------------------
    @property
    def trimPolygonDistanceUnits(self):
        if self._trimPolygonDistanceUnits is None:
            self.__init()
        return self._trimPolygonDistanceUnits
    #----------------------------------------------------------------------
    @property
    def defaultBreaks(self):
        if self._defaultBreaks is None:
            self.__init()
        return self._defaultBreaks
    #----------------------------------------------------------------------
    @property
    def includeSourceInformationOnLines(self):
        if self._includeSourceInformationOnLines is None:
            self.__init()
        return self._includeSourceInformationOnLines
    #----------------------------------------------------------------------
    @property
    def overlapPolygons(self):
        if self._overlapPolygons is None:
            self.__init()
        return self._overlapPolygons
    #----------------------------------------------------------------------
    @property
    def timeOfDay(self):
        if self._timeOfDay is None:
            self.__init()
        return self._timeOfDay
    #----------------------------------------------------------------------
    @property
    def excludeSourcesFromPolygons(self):
        if self._excludeSourcesFromPolygons is None:
            self.__init()
        return self._excludeSourcesFromPolygons
    #----------------------------------------------------------------------
    @property
    def splitPolygonsAtBreaks(self):
        if self._splitPolygonsAtBreaks is None:
            self.__init()
        return self._splitPolygonsAtBreaks
    #----------------------------------------------------------------------
    @property
    def outputPolygons(self):
        if self._outputPolygons is None:
            self.__init()
        return self._outputPolygons
    #----------------------------------------------------------------------
    @property
    def overlapLines(self):
        if self._overlapLines is None:
            self.__init()
        return self._overlapLines
    #----------------------------------------------------------------------
    @property
    def trimPolygonDistance(self):
        if self._trimPolygonDistance is None:
            self.__init()
        return self._trimPolygonDistance
    #----------------------------------------------------------------------
    @property
    def splitLinesAtBreaks(self):
        if self._splitLinesAtBreaks is None:
            self.__init()
        return self._splitLinesAtBreaks
    #----------------------------------------------------------------------
    @property
    def timeOfDayUsage(self):
        if self._timeOfDayUsage is None:
            self.__init()
        return self._timeOfDayUsage
    #----------------------------------------------------------------------
    @property
    def mergeSimilarPolygonRanges(self):
        if self._mergeSimilarPolygonRanges is None:
            self.__init()
        return self._mergeSimilarPolygonRanges
