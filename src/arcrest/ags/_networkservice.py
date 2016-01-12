from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseAGSServer
import json

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

                elif k == "closestFacilityLayers" and json_dict[k]:
                    self._closestFacilityLayers = []
                    for cf in v:
                        self._closestFacilityLayers.append(
                            ClosestFacilityNetworkLayer(url=self._url + "/%s" % cf,
                                                    securityHandler=self._securityHandler,
                                                    proxy_url=self._proxy_url,
                                                    proxy_port=self._proxy_port,
                                                    initialize=False))
                else:
                    setattr(self, "_"+ k, v)
            else:
                print ("attribute %s is not implemented." % k)
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

        # TODO handle spaces in the url, 'Service Area' should be 'Service+Area'
        self._url = self._url.replace(' ','+')

        json_dict = self._get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print (k, " - attribute not implemented in NetworkLayer.")
            del k,v
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
    The Route Network Layer which has common properties of Network Layer
    as well as some attributes unique to Route Network Layer only.
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
        json_dict = self._get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in RouteNetworkLayer.")
            del k,v

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
        route operation as query parameters.
        Inputs:
            stops - The set of stops loaded as network locations during analysis.
                    Stops can be specified using a simple comma / semi-colon
                    based syntax or as a JSON structure. If stops are not
                    specified, preloaded stops from the map document are used in
                    the analysis.
            barriers - The set of barriers loaded as network locations during
                       analysis. Barriers can be specified using a simple comma
                       / semi-colon based syntax or as a JSON structure. If
                       barriers are not specified, preloaded barriers from the
                       map document are used in the analysis. If an empty json
                       object is passed ('{}') preloaded barriers are ignored.
            polylineBarriers - The set of polyline barriers loaded as network
                               locations during analysis. If polyline barriers
                               are not specified, preloaded polyline barriers
                               from the map document are used in the analysis.
                               If an empty json object is passed ('{}')
                               preloaded polyline barriers are ignored.
            polygonBarriers - The set of polygon barriers loaded as network
                              locations during analysis. If polygon barriers
                              are not specified, preloaded polygon barriers
                              from the map document are used in the analysis.
                              If an empty json object is passed ('{}') preloaded
                              polygon barriers are ignored.

            travelMode - Travel modes provide override values that help you
                         quickly and consistently model a vehicle or mode of
                         transportation. The chosen travel mode must be
                         preconfigured on the network dataset that the routing
                         service references.
            attributeParameterValues - A set of attribute parameter values that
                                       can be parameterized to determine which
                                       network elements can be used by a vehicle.
            returnDirections - If true, directions will be generated and returned
                               with the analysis results. Default is true.
            returnRoutes - If true, routes will be returned with the analysis
                           results. Default is true.
            returnStops -  If true, stops will be returned with the analysis
                           results. Default is false.
            returnBarriers -  If true, barriers will be returned with the analysis
                              results. Default is false.
            returnPolylineBarriers -  If true, polyline barriers will be returned
                                      with the analysis results. Default is false.
            returnPolygonBarriers - If true, polygon barriers will be returned with
                                    the analysis results. Default is false.
            outSR - The spatial reference of the geometries returned with the
                    analysis results.
            ignoreInvalidLocations - If true, the solver will ignore invalid
                                     locations. Otherwise, it will raise an error.
                                     The default is as defined in the network layer.
            outputLines - The type of output lines to be generated in the result.
                          The default is as defined in the network layer.
            findBestSequence - If true, the solver should re-sequence the route in
                               the optimal order. The default is as defined in the
                               network layer.
            preserveFirstStop - If true, the solver should keep the first stop
                                fixed in the sequence. The default is as defined
                                in the network layer.
            preserveLastStop - If true, the solver should keep the last stop fixed
                               in the sequence. The default is as defined in the
                               network layer.
            useTimeWindows - If true, the solver should consider time windows.
                             The default is as defined in the network layer.
            startTime - The time the route begins. If not specified, the solver
                        will use the default as defined in the network layer.
            startTimeIsUTC - The time zone of the startTime parameter.
            accumulateAttributeNames - The list of network attribute names to be
                                       accumulated with the analysis. The default is
                                       as defined in the network layer. The value
                                       should be specified as a comma separated list
                                       of attribute names. You can also specify a
                                       value of none to indicate that no network
                                       attributes should be accumulated.
            impedanceAttributeName - The network attribute name to be used as the
                                     impedance attribute in analysis. The default is
                                     as defined in the network layer.
            restrictionAttributeNames -The list of network attribute names to be
                                       used as restrictions with the analysis. The
                                       default is as defined in the network layer.
                                       The value should be specified as a comma
                                       separated list of attribute names. You can
                                       also specify a value of none to indicate that
                                       no network attributes should be used as
                                       restrictions.
            restrictUTurns -  Specifies how U-Turns should be restricted in the
                              analysis. The default is as defined in the network
                              layer. Values: esriNFSBAllowBacktrack |
                              esriNFSBAtDeadEndsOnly | esriNFSBNoBacktrack |
                              esriNFSBAtDeadEndsAndIntersections
            useHierarchy -  If true, the hierarchy attribute for the network should
                            be used in analysis. The default is as defined in the
                            network layer.
            directionsLanguage - The language to be used when computing directions.
                                 The default is as defined in the network layer. The
                                 list of supported languages can be found in REST
                                 layer description.
            directionsOutputType -  Defines content, verbosity of returned
                                    directions. The default is esriDOTStandard.
                                    Values: esriDOTComplete | esriDOTCompleteNoEvents
                                    | esriDOTInstructionsOnly | esriDOTStandard |
                                    esriDOTSummaryOnly
            directionsStyleName - The style to be used when returning the directions.
                                  The default is as defined in the network layer. The
                                  list of supported styles can be found in REST
                                  layer description.
            directionsLengthUnits - The length units to use when computing directions.
                                    The default is as defined in the network layer.
                                    Values: esriNAUFeet | esriNAUKilometers |
                                    esriNAUMeters | esriNAUMiles |
                                    esriNAUNauticalMiles | esriNAUYards |
                                    esriNAUUnknown
            directionsTimeAttributeName - The name of network attribute to use for
                                          the drive time when computing directions.
                                          The default is as defined in the network
                                          layer.
            outputGeometryPrecision -  The precision of the output geometry after
                                       generalization. If 0, no generalization of
                                       output geometry is performed. The default is
                                       as defined in the network service
                                       configuration.
            outputGeometryPrecisionUnits - The units of the output geometry
                                           precision. The default value is
                                           esriUnknownUnits. Values: esriUnknownUnits
                                           | esriCentimeters | esriDecimalDegrees |
                                           esriDecimeters | esriFeet | esriInches |
                                           esriKilometers | esriMeters | esriMiles |
                                           esriMillimeters | esriNauticalMiles |
                                           esriPoints | esriYards
            returnZ - If true, Z values will be included in the returned routes and
                       compressed geometry if the network dataset is Z-aware.
                       The default is false.
        """

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
            return self._post(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        else:
            return self._get(url=url,
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
        json_dict = self._get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in ServiceAreaNetworkLayer.")
            del k,v

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

    #----------------------------------------------------------------------
    def solveServiceArea(self,facilities,method="POST",
                         barriers=None,
                         polylineBarriers=None,
                         polygonBarriers=None,
                         travelMode=None,
                         attributeParameterValues=None,
                         defaultBreaks=None,
                         excludeSourcesFromPolygons=None,
                         mergeSimilarPolygonRanges=None,
                         outputLines=None,
                         outputPolygons=None,
                         overlapLines=None,
                         overlapPolygons=None,
                         splitLinesAtBreaks=None,
                         splitPolygonsAtBreaks=None,
                         trimOuterPolygon=None,
                         trimPolygonDistance=None,
                         trimPolygonDistanceUnits=None,
                         returnFacilities=False,
                         returnBarriers=False,
                         returnPolylineBarriers=False,
                         returnPolygonBarriers=False,
                         outSR=None,
                         accumulateAttributeNames=None,
                         impedanceAttributeName=None,
                         restrictionAttributeNames=None,
                         restrictUTurns=None,
                         outputGeometryPrecision=None,
                         outputGeometryPrecisionUnits='esriUnknownUnits',
                         useHierarchy=None,
                         timeOfDay=None,
                         timeOfDayIsUTC=None,
                         travelDirection=None,
                         returnZ=False):
        """ The solve service area operation is performed on a network layer
        resource of type service area (layerType is esriNAServerServiceArea).
        You can provide arguments to the solve service area operation as
        query parameters.
        Inputs:
            facilities - The set of facilities loaded as network locations
                         during analysis. Facilities can be specified using
                         a simple comma / semi-colon based syntax or as a
                         JSON structure. If facilities are not specified,
                         preloaded facilities from the map document are used
                         in the analysis. If an empty json object is passed
                         ('{}') preloaded facilities are ignored.
            barriers - The set of barriers loaded as network locations during
                       analysis. Barriers can be specified using a simple
                       comma/semicolon-based syntax or as a JSON structure.
                       If barriers are not specified, preloaded barriers from
                       the map document are used in the analysis. If an empty
                       json object is passed ('{}'), preloaded barriers are
                       ignored.
            polylineBarriers - The set of polyline barriers loaded as network
                               locations during analysis. If polyline barriers
                               are not specified, preloaded polyline barriers
                               from the map document are used in the analysis.
                               If an empty json object is passed ('{}'),
                               preloaded polyline barriers are ignored.
            polygonBarriers - The set of polygon barriers loaded as network
                              locations during analysis. If polygon barriers
                              are not specified, preloaded polygon barriers
                              from the map document are used in the analysis.
                              If an empty json object is passed ('{}'),
                              preloaded polygon barriers are ignored.
            travelMode - Travel modes provide override values that help you
                         quickly and consistently model a vehicle or mode of
                         transportation. The chosen travel mode must be
                         preconfigured on the network dataset that the
                         service area service references.
            attributeParameterValues - A set of attribute parameter values that
                                       can be parameterized to determine which
                                       network elements can be used by a vehicle.
            defaultBreaks - A comma-separated list of doubles. The default is
                            defined in the network analysis layer.
            excludeSourcesFromPolygons - A comma-separated list of string names.
                                         The default is defined in the network
                                         analysis layer.

            mergeSimilarPolygonRanges - If true, similar ranges will be merged
                                        in the result polygons. The default is
                                        defined in the network analysis layer.
            outputLines - The type of lines(s) generated. The default is as
                          defined in the network analysis layer.
            outputPolygons - The type of polygon(s) generated. The default is
                             as defined in the network analysis layer.
            overlapLines - Indicates if the lines should overlap from multiple
                           facilities. The default is defined in the network
                           analysis layer.
            overlapPolygons - Indicates if the polygons for all facilities
                              should overlap. The default is defined in the
                              network analysis layer.
            splitLinesAtBreaks - If true, lines will be split at breaks. The
                                 default is defined in the network analysis
                                 layer.
            splitPolygonsAtBreaks - If true, polygons will be split at breaks.
                                    The default is defined in the network
                                    analysis layer.
            trimOuterPolygon -  If true, the outermost polygon (at the maximum
                                break value) will be trimmed. The default is
                                defined in the network analysis layer.
            trimPolygonDistance -  If polygons are being trimmed, provides the
                                   distance to trim. The default is defined in
                                   the network analysis layer.
            trimPolygonDistanceUnits - If polygons are being trimmed, specifies
                                       the units of the trimPolygonDistance. The
                                       default is defined in the network analysis
                                       layer.
            returnFacilities - If true, facilities will be returned with the
                               analysis results. Default is false.
            returnBarriers - If true, barriers will be returned with the analysis
                             results. Default is false.
            returnPolylineBarriers - If true, polyline barriers will be returned
                                     with the analysis results. Default is false.
            returnPolygonBarriers - If true, polygon barriers will be returned
                                    with the analysis results. Default is false.
            outSR - The well-known ID of the spatial reference for the geometries
                    returned with the analysis results. If outSR is not specified,
                    the geometries are returned in the spatial reference of the map.
            accumulateAttributeNames - The list of network attribute names to be
                                       accumulated with the analysis. The default
                                       is as defined in the network analysis layer.
                                       The value should be specified as a comma
                                       separated list of attribute names. You can
                                       also specify a value of none to indicate that
                                       no network attributes should be accumulated.
            impedanceAttributeName - The network attribute name to be used as the
                                     impedance attribute in analysis. The default
                                     is as defined in the network analysis layer.
            restrictionAttributeNames - The list of network attribute names to be
                                        used as restrictions with the analysis. The
                                        default is as defined in the network analysis
                                        layer. The value should be specified as a
                                        comma separated list of attribute names.
                                        You can also specify a value of none to
                                        indicate that no network attributes should
                                        be used as restrictions.
            restrictUTurns - Specifies how U-Turns should be restricted in the
                             analysis. The default is as defined in the network
                             analysis layer. Values: esriNFSBAllowBacktrack |
                             esriNFSBAtDeadEndsOnly | esriNFSBNoBacktrack |
                             esriNFSBAtDeadEndsAndIntersections
            outputGeometryPrecision - The precision of the output geometry after
                                      generalization. If 0, no generalization of
                                      output geometry is performed. The default is
                                      as defined in the network service configuration.
            outputGeometryPrecisionUnits - The units of the output geometry precision.
                                           The default value is esriUnknownUnits.
                                           Values: esriUnknownUnits | esriCentimeters |
                                           esriDecimalDegrees | esriDecimeters |
                                           esriFeet | esriInches | esriKilometers |
                                           esriMeters | esriMiles | esriMillimeters |
                                           esriNauticalMiles | esriPoints | esriYards
            useHierarchy - If true, the hierarchy attribute for the network should be
                           used in analysis. The default is as defined in the network
                           layer. This cannot be used in conjunction with outputLines.
            timeOfDay - The date and time at the facility. If travelDirection is set
                        to esriNATravelDirectionToFacility, the timeOfDay value
                        specifies the arrival time at the facility. if travelDirection
                        is set to esriNATravelDirectionFromFacility, the timeOfDay
                        value is the departure time from the facility. The time zone
                        for timeOfDay is specified by timeOfDayIsUTC.
            timeOfDayIsUTC - The time zone or zones of the timeOfDay parameter. When
                             set to false, which is the default value, the timeOfDay
                             parameter refers to the time zone or zones in which the
                             facilities are located. Therefore, the start or end times
                             of the service areas are staggered by time zone.
            travelDirection - Options for traveling to or from the facility. The
                              default is defined in the network analysis layer.
            returnZ - If true, Z values will be included in saPolygons and saPolylines
                      geometry if the network dataset is Z-aware.
    """
        if not self.layerType == "esriNAServerServiceAreaLayer":
            raise ValueError("The solveServiceArea operation is supported on a network "
                             "layer of Service Area type only")

        url = self._url + "/solveServiceArea"
        params = {
                "f" : "json",
                "facilities": facilities
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
        if not defaultBreaks is None:
            params['defaultBreaks'] = defaultBreaks
        if not excludeSourcesFromPolygons is None:
            params['excludeSourcesFromPolygons'] = excludeSourcesFromPolygons
        if not mergeSimilarPolygonRanges is None:
            params['mergeSimilarPolygonRanges'] = mergeSimilarPolygonRanges
        if not outputLines is None:
            params['outputLines'] = outputLines
        if not outputPolygons is None:
            params['outputPolygons'] = outputPolygons
        if not overlapLines is None:
            params['overlapLines'] = overlapLines
        if not overlapPolygons is None:
            params['overlapPolygons'] = overlapPolygons
        if not splitLinesAtBreaks is None:
            params['splitLinesAtBreaks'] = splitLinesAtBreaks
        if not splitPolygonsAtBreaks is None:
            params['splitPolygonsAtBreaks'] = splitPolygonsAtBreaks
        if not trimOuterPolygon is None:
            params['trimOuterPolygon'] = trimOuterPolygon
        if not trimPolygonDistance is None:
            params['trimPolygonDistance'] = trimPolygonDistance
        if not trimPolygonDistanceUnits is None:
            params['trimPolygonDistanceUnits'] = trimPolygonDistanceUnits
        if not returnFacilities is None:
            params['returnFacilities'] = returnFacilities
        if not returnBarriers is None:
            params['returnBarriers'] = returnBarriers
        if not returnPolylineBarriers is None:
            params['returnPolylineBarriers'] = returnPolylineBarriers
        if not returnPolygonBarriers is None:
            params['returnPolygonBarriers'] = returnPolygonBarriers
        if not outSR is None:
            params['outSR'] = outSR
        if not accumulateAttributeNames is None:
            params['accumulateAttributeNames'] = accumulateAttributeNames
        if not impedanceAttributeName is None:
            params['impedanceAttributeName'] = impedanceAttributeName
        if not restrictionAttributeNames is None:
            params['restrictionAttributeNames'] = restrictionAttributeNames
        if not restrictUTurns is None:
            params['restrictUTurns'] = restrictUTurns
        if not outputGeometryPrecision is None:
            params['outputGeometryPrecision'] = outputGeometryPrecision
        if not outputGeometryPrecisionUnits is None:
            params['outputGeometryPrecisionUnits'] = outputGeometryPrecisionUnits
        if not useHierarchy is None:
            params['useHierarchy'] = useHierarchy
        if not timeOfDay is None:
            params['timeOfDay'] = timeOfDay
        if not timeOfDayIsUTC is None:
            params['timeOfDayIsUTC'] = timeOfDayIsUTC
        if not travelDirection is None:
            params['travelDirection'] = travelDirection
        if not returnZ is None:
            params['returnZ'] = returnZ

        if method.lower() == "post":
            return self._post(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        else:
            return self._get(url=url,
                                param_dict=params,
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)


########################################################################
class ClosestFacilityNetworkLayer(NetworkLayer):
    """
    The Closest Facility Network Layer which has common properties of Network
    Layer as well as some attributes unique to Closest Facility Network Layer
    only.
    """

    #specific to Closest Facility
    _directionsLanguage = None
    _directionsLengthUnits = None
    _outputLineType = None
    _timeOfDayIsUTC = None
    _travelDirection = None
    _defaultCutoffValue = None
    _facilityCount = None
    _directionsTimeAttribute = None
    _timeOfDayUsage = None
    _directionsSupportedLanguages = None
    _directionsStyleNames = None
    _timeOfDay = None

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

        # TODO handle spaces in the url, 'Closest Facility' should be 'Closest+Facility'
        self._url = self._url.replace(' ','+')
        json_dict = self._get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print (k, " - attribute not implemented in ClosestFacilityNetworkLayer.")
            del k,v

    #----------------------------------------------------------------------
    @property
    def directionsLanguage(self):
        if self._directionsLanguage is None:
            self.__init()
        return self._directionsLanguage
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
    def defaultCutoffValue(self):
        if self._defaultCutoffValue is None:
            self.__init()
        return self._defaultCutoffValue
    #----------------------------------------------------------------------
    @property
    def facilityCount(self):
        if self._facilityCount is None:
            self.__init()
        return self._facilityCount
    #----------------------------------------------------------------------
    @property
    def directionsTimeAttribute(self):
        if self._directionsTimeAttribute is None:
            self.__init()
        return self._directionsTimeAttribute
    #----------------------------------------------------------------------
    @property
    def timeOfDayUsage(self):
        if self._timeOfDayUsage is None:
            self.__init()
        return self._timeOfDayUsage
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
    def timeOfDay(self):
        if self._timeOfDay is None:
            self.__init()
        return self._timeOfDay

    #----------------------------------------------------------------------
    def solveClosestFacility(self,incidents,facilities,method="POST",
                             barriers=None,
                             polylineBarriers=None,
                             polygonBarriers=None,
                             travelMode=None,
                             attributeParameterValues=None,
                             returnDirections=None,
                             directionsLanguage=None,
                             directionsStyleName=None,
                             directionsLengthUnits=None,
                             directionsTimeAttributeName=None,
                             returnCFRoutes=True,
                             returnFacilities=False,
                             returnIncidents=False,
                             returnBarriers=False,
                             returnPolylineBarriers=False,
                             returnPolygonBarriers=False,
                             outputLines=None,
                             defaultCutoff=None,
                             defaultTargetFacilityCount=None,
                             travelDirection=None,
                             outSR=None,
                             accumulateAttributeNames=None,
                             impedanceAttributeName=None,
                             restrictionAttributeNames=None,
                             restrictUTurns=None,
                             useHierarchy=True,
                             outputGeometryPrecision=None,
                             outputGeometryPrecisionUnits=None,
                             timeOfDay=None,
                             timeOfDayIsUTC=None,
                             timeOfDayUsage=None,
                             returnZ=False):
        """The solve operation is performed on a network layer resource of
        type closest facility (layerType is esriNAServerClosestFacilityLayer).
        You can provide arguments to the solve route operation as query
        parameters.
        Inputs:
            facilities  - The set of facilities loaded as network locations
                          during analysis. Facilities can be specified using
                          a simple comma / semi-colon based syntax or as a
                          JSON structure. If facilities are not specified,
                          preloaded facilities from the map document are used
                          in the analysis.
            incidents - The set of incidents loaded as network locations
                        during analysis. Incidents can be specified using
                        a simple comma / semi-colon based syntax or as a
                        JSON structure. If incidents are not specified,
                        preloaded incidents from the map document are used
                        in the analysis.
            barriers - The set of barriers loaded as network locations during
                       analysis. Barriers can be specified using a simple comma
                       / semi-colon based syntax or as a JSON structure. If
                       barriers are not specified, preloaded barriers from the
                       map document are used in the analysis. If an empty json
                       object is passed ('{}') preloaded barriers are ignored.
            polylineBarriers - The set of polyline barriers loaded as network
                               locations during analysis. If polyline barriers
                               are not specified, preloaded polyline barriers
                               from the map document are used in the analysis.
                               If an empty json object is passed ('{}')
                               preloaded polyline barriers are ignored.
            polygonBarriers - The set of polygon barriers loaded as network
                              locations during analysis. If polygon barriers
                              are not specified, preloaded polygon barriers
                              from the map document are used in the analysis.
                              If an empty json object is passed ('{}') preloaded
                              polygon barriers are ignored.
            travelMode - Travel modes provide override values that help you
                         quickly and consistently model a vehicle or mode of
                         transportation. The chosen travel mode must be
                         preconfigured on the network dataset that the routing
                         service references.
            attributeParameterValues - A set of attribute parameter values that
                                       can be parameterized to determine which
                                       network elements can be used by a vehicle.
            returnDirections - If true, directions will be generated and returned
                               with the analysis results. Default is true.
            directionsLanguage - The language to be used when computing directions.
                                 The default is as defined in the network layer. The
                                 list of supported languages can be found in REST
                                 layer description.
            directionsOutputType -  Defines content, verbosity of returned
                                    directions. The default is esriDOTStandard.
                                    Values: esriDOTComplete | esriDOTCompleteNoEvents
                                    | esriDOTInstructionsOnly | esriDOTStandard |
                                    esriDOTSummaryOnly
            directionsStyleName - The style to be used when returning the directions.
                                  The default is as defined in the network layer. The
                                  list of supported styles can be found in REST
                                  layer description.
            directionsLengthUnits - The length units to use when computing directions.
                                    The default is as defined in the network layer.
                                    Values: esriNAUFeet | esriNAUKilometers |
                                    esriNAUMeters | esriNAUMiles |
                                    esriNAUNauticalMiles | esriNAUYards |
                                    esriNAUUnknown
            directionsTimeAttributeName - The name of network attribute to use for
                                          the drive time when computing directions.
                                          The default is as defined in the network
                                          layer.
            returnCFRoutes - If true, closest facilities routes will be returned
                             with the analysis results. Default is true.
            returnFacilities -  If true, facilities  will be returned with the
                                analysis results. Default is false.
            returnIncidents - If true, incidents will be returned with the
                              analysis results. Default is false.
            returnBarriers -  If true, barriers will be returned with the analysis
                              results. Default is false.
            returnPolylineBarriers -  If true, polyline barriers will be returned
                                      with the analysis results. Default is false.
            returnPolygonBarriers - If true, polygon barriers will be returned with
                                    the analysis results. Default is false.
            outputLines - The type of output lines to be generated in the result.
                          The default is as defined in the network layer.
            defaultCutoff - The default cutoff value to stop traversing.
            defaultTargetFacilityCount - The default number of facilities to find.
            travelDirection - Options for traveling to or from the facility.
                              The default is defined in the network layer.
                              Values: esriNATravelDirectionFromFacility |
                              esriNATravelDirectionToFacility
            outSR - The spatial reference of the geometries returned with the
                    analysis results.
            accumulateAttributeNames - The list of network attribute names to be
                                       accumulated with the analysis. The default is
                                       as defined in the network layer. The value
                                       should be specified as a comma separated list
                                       of attribute names. You can also specify a
                                       value of none to indicate that no network
                                       attributes should be accumulated.
            impedanceAttributeName - The network attribute name to be used as the
                                     impedance attribute in analysis. The default is
                                     as defined in the network layer.
            restrictionAttributeNames -The list of network attribute names to be
                                       used as restrictions with the analysis. The
                                       default is as defined in the network layer.
                                       The value should be specified as a comma
                                       separated list of attribute names. You can
                                       also specify a value of none to indicate that
                                       no network attributes should be used as
                                       restrictions.
            restrictUTurns -  Specifies how U-Turns should be restricted in the
                              analysis. The default is as defined in the network
                              layer. Values: esriNFSBAllowBacktrack |
                              esriNFSBAtDeadEndsOnly | esriNFSBNoBacktrack |
                              esriNFSBAtDeadEndsAndIntersections
            useHierarchy -  If true, the hierarchy attribute for the network should
                            be used in analysis. The default is as defined in the
                            network layer.
            outputGeometryPrecision -  The precision of the output geometry after
                                       generalization. If 0, no generalization of
                                       output geometry is performed. The default is
                                       as defined in the network service
                                       configuration.
            outputGeometryPrecisionUnits - The units of the output geometry
                                           precision. The default value is
                                           esriUnknownUnits. Values: esriUnknownUnits
                                           | esriCentimeters | esriDecimalDegrees |
                                           esriDecimeters | esriFeet | esriInches |
                                           esriKilometers | esriMeters | esriMiles |
                                           esriMillimeters | esriNauticalMiles |
                                           esriPoints | esriYards
            timeOfDay - Arrival or departure date and time. Values: specified by
                        number of milliseconds since midnight Jan 1st, 1970, UTC.
            timeOfDayIsUTC - The time zone of the timeOfDay parameter. By setting
                             timeOfDayIsUTC to true, the timeOfDay parameter refers
                             to Coordinated Universal Time (UTC). Choose this option
                             if you want to find what's nearest for a specific time,
                             such as now, but aren't certain in which time zone the
                             facilities or incidents will be located.
            timeOfDayUsage - Defines the way timeOfDay value is used. The default
                             is as defined in the network layer.
                             Values: esriNATimeOfDayUseAsStartTime |
                             esriNATimeOfDayUseAsEndTime
            returnZ - If true, Z values will be included in the returned routes and
                       compressed geometry if the network dataset is Z-aware.
                       The default is false.
    """

        if not self.layerType == "esriNAServerClosestFacilityLayer":
            raise ValueError("The solveClosestFacility operation is supported on a network "
                             "layer of Closest Facility type only")

        url = self._url + "/solveClosestFacility"
        params = {
                "f" : "json",
                "facilities": facilities,
                "incidents": incidents
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
        if not directionsLanguage is None:
            params['directionsLanguage'] = directionsLanguage
        if not directionsStyleName is None:
            params['directionsStyleName'] = directionsStyleName
        if not directionsLengthUnits is None:
            params['directionsLengthUnits'] = directionsLengthUnits
        if not directionsTimeAttributeName is None:
            params['directionsTimeAttributeName'] = directionsTimeAttributeName
        if not returnCFRoutes is None:
            params['returnCFRoutes'] = returnCFRoutes
        if not returnFacilities is None:
            params['returnFacilities'] = returnFacilities
        if not returnIncidents is None:
            params['returnIncidents'] = returnIncidents
        if not returnBarriers is None:
            params['returnBarriers'] = returnBarriers
        if not returnPolylineBarriers is None:
            params['returnPolylineBarriers'] = returnPolylineBarriers
        if not returnPolygonBarriers is None:
            params['returnPolygonBarriers'] = returnPolygonBarriers
        if not outputLines is None:
            params['outputLines'] = outputLines
        if not defaultCutoff is None:
            params['defaultCutoff'] = defaultCutoff
        if not defaultTargetFacilityCount is None:
            params['defaultTargetFacilityCount'] = defaultTargetFacilityCount
        if not travelDirection is None:
            params['travelDirection'] = travelDirection
        if not outSR is None:
            params['outSR'] = outSR
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
        if not outputGeometryPrecision is None:
            params['outputGeometryPrecision'] = outputGeometryPrecision
        if not outputGeometryPrecisionUnits is None:
            params['outputGeometryPrecisionUnits'] = outputGeometryPrecisionUnits
        if not timeOfDay is None:
            params['timeOfDay'] = timeOfDay
        if not timeOfDayIsUTC is None:
            params['timeOfDayIsUTC'] = timeOfDayIsUTC
        if not timeOfDayUsage is None:
            params['timeOfDayUsage'] = timeOfDayUsage
        if not returnZ is None:
            params['returnZ'] = returnZ

        if method.lower() == "post":
            return self._post(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        else:
            return self._get(url=url,
                                param_dict=params,
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
