from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseAGSServer
from ..security import AGOLTokenSecurityHandler, OAuthSecurityHandler
from ..common.geometry import Point
import json
########################################################################
class GeocodeService(BaseAGSServer):
    """
    Geocoding is the process of assigning a location, usually in the form
    of coordinate values (points), to an address by comparing the
    descriptive location elements in the address to those present in the
    reference material. Addresses come in many forms, ranging from the
    common address format of a house number followed by the street name and
    succeeding information, to other location descriptions such as postal
    zone or census tract. An address includes any type of information that
    distinguishes a place.
    """
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None

    _candidateFields = None
    _intersectionCandidateFields = None
    _capabilities = None
    _spatialReference = None
    _singleLineAddressField = None
    _addressFields = None
    _currentVersion = None
    _locatorProperties = None
    _serviceDescription = None
    _countries = None
    _categories = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ inializes the properties """
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
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                print (k, " - attribute not implemented for Geocode Service")
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
    def countries(self):
        """returns the countries property"""
        if self._countries is None:
            self.__init()
        return self._countries
    #----------------------------------------------------------------------
    @property
    def categories(self):
        """returns the categories property"""
        if self._categories is None:
            self.__init()
        return self._categories
    #----------------------------------------------------------------------
    @property
    def candidateFields(self):
        """get candidate fields"""
        if self._candidateFields is None:
            self.__init()
        return self._candidateFields
    #----------------------------------------------------------------------
    @property
    def intersectionCandidateFields(self):
        """gets the intersectionCandidateFields value"""
        if self._intersectionCandidateFields is None:
            self.__init()
        return self._intersectionCandidateFields
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """gets the capabilities value"""
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """gets the spatialReference for the service"""
        if self._spatialReference is None:
            self.__init()
        return self._spatialReference
    #----------------------------------------------------------------------
    @property
    def singleLineAddressField(self):
        """returns single line support field"""
        if self._singleLineAddressField is None:
            self.__init()
        return self._singleLineAddressField
    #----------------------------------------------------------------------
    @property
    def addressFields(self):
        """gets the address fields"""
        if self._addressFields is None:
            self.__init()
        return self._addressFields
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the current version"""
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def locatorProperties(self):
        """gets the locator properties"""
        if self._locatorProperties is None:
            self.__init()
        return self._locatorProperties
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """gets the service description"""
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    def find(self,
             text,
             magicKey=None,
             sourceCountry=None,
             bbox=None,
             location=None,
             distance=3218.69,
             outSR=102100,
             category=None,
             outFields="*",
             maxLocations=20,
             forStorage=False):
        """
        The find operation geocodes one location per request; the input
        address is specified in a single parameter.

        Inputs:
           text - Specifies the location to be geocoded. This can be a
            street address, place name, postal code, or POI.
           magicKey - The find operation retrieves results quicker when you
            pass in valid text and magicKey values than when you don't pass
            in magicKey. However, to get these advantages, you need to make
            a prior request to suggest, which provides a magicKey. This may
            or may not be relevant to your workflow.
           sourceCountry - A value representing the country. Providing this
            value increases geocoding speed. Acceptable values include the
            full country name in English or the official language of the
            country, the ISO 3166-1 2-digit country code, or the
            ISO 3166-1 3-digit country code.
           bbox - A set of bounding box coordinates that limit the search
            area to a specific region. This is especially useful for
            applications in which a user will search for places and
            addresses only within the current map extent.
           location - Defines an origin point location that is used with
            the distance parameter to sort geocoding candidates based upon
            their proximity to the location. The distance parameter
            specifies the radial distance from the location in meters. The
            priority of candidates within this radius is boosted relative
            to those outside the radius.
           distance - Specifies the radius of an area around a point
            location which is used to boost the rank of geocoding
            candidates so that candidates closest to the location are
            returned first. The distance value is in meters.
           outSR - The spatial reference of the x/y coordinates returned by
            a geocode request. This is useful for applications using a map
            with a spatial reference different than that of the geocode
            service.
           category - A place or address type which can be used to filter
            find results. The parameter supports input of single category
            values or multiple comma-separated values. The category
            parameter can be passed in a request with or without the text
            parameter.
           outFields - The list of fields to be returned in the response.
           maxLocation - The maximum number of locations to be returned by
            a search, up to the maximum number allowed by the service. If
            not specified, then one location will be returned.
           forStorage - Specifies whether the results of the operation will
            be persisted. The default value is false, which indicates the
            results of the operation can't be stored, but they can be
            temporarily displayed on a map for instance. If you store the
            results, in a database for example, you need to set this
            parameter to true.
        """
        if isinstance(self._securityHandler, (AGOLTokenSecurityHandler, OAuthSecurityHandler)):
            url = self._url + "/find"
            params = {
                "f" : "json",
            }
            if not magicKey is None:
                params['magicKey'] = magicKey
            if not sourceCountry is None:
                params['sourceCountry'] = sourceCountry
            if not bbox is None:
                params['bbox'] = bbox
            if not location is None and \
               isinstance(location, Point):
                params['location'] = location.asDictionary
            elif not location is None and \
                 isinstance(location, list):
                params['location'] = "%s,%s" % (location[0], location[1])
            if not distance is None:
                params['distance'] = distance
            if not outSR is None:
                params['outSR'] = outSR
            if not category is None:
                params['category'] = category
            if outFields is None:
                params['outFields'] = "*"
            else:
                params['outFields'] = outFields
            if not maxLocations is None:
                params['maxLocations'] = maxLocations
            if not forStorage is None:
                params['forStorage'] = forStorage
            return self._do_post(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        else:
            raise Exception("This function works on the ArcGIS Online World Geocoder")
    #----------------------------------------------------------------------
    def findAddressCandidates(self,
                              addressDict=None,
                              singleLine=None,
                              maxLocations=10,
                              outFields="*",
                              outSR=4326,
                              searchExtent=None,
                              location=None,
                              distance=2000,
                              magicKey=None,
                              category=None):
        """
        The findAddressCandidates operation is performed on a geocode
        service resource. The result of this operation is a resource
        representing the list of address candidates. This resource provides
        information about candidates, including the address, location, and
        match score. Locators published using ArcGIS Server 10 or later
        support the single line address field for the findAddressCandidates
        operation.
        You can provide arguments to the findAddressCandidates operation as
        query parameters defined in the following parameters table:

        Inputs:
            addressDict - The various address fields accepted by the
             corresponding geocode service. These fields are listed in the
             addressFields property of the JSON representation associated
             geocode service resource.
             Example: Suppose that addressFields of a geocode service
             resource includes fields with the following names: Street,
             City, State, and Zone. If you want to perform the
             findAddressCandidates operation by providing values for the
             Street and Zone fields, you'd set the query parameters as
             Street=380+New+York+St&Zone=92373

            singleLine - Specifies the location to be geocoded. The input
             address components are formatted as a single string. The
             singleLine parameter and <addressField> parameters should not
             be passed in the same request.
            maxLocations - The maximum number of locations to be returned
             by a search, up to the maximum number allowed by the geocode
             service. If not specified, the maximum number of candidates
             for which the service is configured will be returned.
            outFields - The list of fields to be included in the returned
             result set. This list is a comma-delimited list of field
             names. If you specify the shape field in the list of return
             fields, it is ignored. For non-intersection addresses, you can
             specify the candidate fields from the geocode service
             resource. For intersection addresses, you can specify the
             intersection candidate fields from the geocode service
             resource.
            outSR - The well-known ID (WKID) of the spatial reference or a
             spatial reference JSON object for the returned address
             candidates. For a list of valid WKID values, see Projected
             coordinate systems and Geographic coordinate systems.
            searchExtent - The spatial extent (bounding box) to be used in
             geocoding. The response will return only the candidates that
             are within this spatial extent. Unless the spatialReference is
             included in the searchExtent, the coordinates are assumed to
             be in the spatial reference of the locator.
             Simple syntax: <xmin>, <ymin>, <xmax>, <ymax>
            location - Defines an origin point location that is used with
             the distance parameter to sort geocoding candidates based on
             their proximity to the location. The distance parameter
             specifies the radial distance from the location in meters. The
             priority of candidates within this radius is boosted relative
             to those outside the radius. This is useful in mobile
             applications where a user searches for places in the vicinity
             of their current GPS location; the location and distance
             parameters can be used in this scenario. The location
             parameter can be specified without specifying a distance. If
             distance is not specified, it defaults to 2000 meters. The
             location can be represented with a simple comma-separated
             syntax (x,y), or as a JSON point object. If the spatial
             reference of the location coordinates is different than that
             of the geocode service, then it must be defined in the JSON
             object. If the comma-separated syntax is used, or if the
             spatial reference is not included in the JSON object, then the
             spatial reference of the location is assumed to be the same as
             that of the geocode service. This parameter was added at 10.3
             and is only supported by geocode services published with
             ArcGIS 10.3 for Server and later versions.
            distance - Specifies the radius of an area around a point
             location that is used to boost the rank of geocoding
             candidates so that candidates closest to the location are
             returned first. The distance value is in meters. If the
             distance parameter is specified, the location parameter must
             be specified as well. Unlike the searchExtent parameter, the
             location and distance parameters allow searches to extend
             beyond the specified search radius. They are not used to
             filter results, but rather to rank resulting candidates based
             on their distance from a location. You must pass a
             searchExtent value in addition to location and distance if you
             want to confine the search results to a specific area.
            magicKey - The findAddressCandidates operation retrieves
             results more quickly when you pass in valid singleLine and
             magicKey values than when you don't pass in magicKey. However,
             to get this advantage, you need to make a prior request to the
             suggest operation, which provides a magicKey. This may or may
             not be relevant to your workflow.
             The suggest operation is often called on to improve the user
             experience of search boxes by analyzing partial text and
             providing complete names of places, addresses, points of
             interest, and so on. For instance, typing Mbu into a search
             box offers Mbuji-Mayi, Democratic Republic of the Congo as a
             suggestion, so the user doesn't need to type the complete
             name.
             Looking at the suggestion process from another perspective, as
             the user types, the suggest operation performs a text search,
             which is a redundant part of the overall search that the
             findAddressCandidates operation can also perform. The user
             chooses a place name or type-narrowing the results to a
             specific record. The results from suggest include text and
             magicKey values that contain the information the user chose;
             passing these values from suggest into findAddressCandidates
             results in faster and more accurate find operations.
             In summary, using the magicKey parameter in
             findAddressCandidates is a two-step process:
              1. Make a request to suggest. The response includes text and
                 magicKey properties.
              2. Make a request to findAddressCandidates and pass in the
                 text and magicKey values returned from suggest as the
                 singleLine and magicKey input parameters respectively.
            category - The category parameter is only supported by geocode
             services published using StreetMap Premium locators.
        """
        url = self._url + "/findAddressCandidates"
        params = {
            "f" : "json",
            "distance" : distance
        }
        if addressDict is None and \
           singleLine is None:
            raise Exception("A singleline address or an address dictionary must be passed into this function")
        if not magicKey is None:
            params['magicKey'] = magicKey
        if not category is None:
            params['category'] = category
        if not addressDict is None:
            params = params.update(addressDict)
        if not singleLine is None:
            params['singleLine'] = singleLine
        if not maxLocations is None:
            params['maxLocations'] = maxLocations
        if not outFields is None:
            params['outFields'] = outFields
        if not outSR is None:
            params['outSR'] = outSR
        if not searchExtent is None:
            params['searchExtent'] = searchExtent
        if isinstance(location, Point):
            params['location'] = location.asDictionary
        elif isinstance(location, list):
            params['location'] = "%s,%s" % (location[0], location[1])
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def geocodeAddresses(self,
                         addresses,
                         outSR=4326,
                         sourceCountry=None,
                         category=None):
        """
        The geocodeAddresses operation is performed on a Geocode Service
        resource. The result of this operation is a resource representing
        the list of geocoded addresses. This resource provides information
        about the addresses including the address, location, score, and
        other geocode service-specific attributes.You can provide arguments
        to the geocodeAddresses operation as query parameters defined in
        the following parameters table.

        Inputs:
           addresses - A record set representing the addresses to be
            geocoded. Each record must include an OBJECTID attribute with a
            unique value, as well as various address fields accepted by the
            corresponding geocode service. The field names that should be
            used can be found in the JSON representation of the geocode
            service resource under the addressFields property, for multiple
            input field geocoding, or the singleLineAddressField property,
            for single input field geocoding. The OBJECTID specified in the
            request is reflected as ResultID in the response.
            The maximum number of addresses that can be geocoded in a
            single request is limited to the SuggestedBatchSize property of
            the locator.
            Syntax:
             {
                "records"  : [
                {
                   "attributes" : {"<OBJECTID>" : "<OID11>",
                                   "<field1>" : "<value11>",
                                   "<field2>" : "<value12>",
                                   "<field3>" : "<value13>"
                                   }
                },
                {
                   "attributes" : {"<OBJECTID>" : "<OID12>",
                                   "<field1>" : "<value11>",
                                   "<field2>" : "<value12>",
                                   "<field3>" : "<value13>"
                                   }
                }
                ]
             }
           outSR - The well-known ID of the spatial reference, or a spatial
            reference json object for the returned addresses. For a list of
            valid WKID values, see Projected coordinate systems and
            Geographic coordinate systems.
           sourceCountry - The sourceCountry parameter is only supported by
            geocode services published using StreetMap Premium locators.
            Added at 10.3 and only supported by geocode services published
            with ArcGIS 10.3 for Server and later versions.
           category - The category parameter is only supported by geocode
            services published using StreetMap Premium locators.
        """
        params = {
            "f" : "json"
        }
        url = self._url + "/geocodeAddresses"
        params['outSR'] = outSR
        params['sourceCountry'] = sourceCountry
        params['category'] = category
        params['addresses'] = addresses
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def reverseGeocode(self, location):
        """
        The reverseGeocode operation determines the address at a particular
        x/y location. You pass the coordinates of a point location to the
        geocoding service, and the service returns the address that is
        closest to the location.

        Input:
           location - either an Point object or a list defined as [X,Y]

        """
        params = {
            "f" : "json"
        }
        url = self._url + "/reverseGeocode"
        if isinstance(location, Point):
            params['location'] = location.asDictionary
        elif isinstance(location, list):
            params['location'] = "%s,%s" % (location[0], location[1])
        else:
            raise Exception("Invalid location")
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def suggest(self,
                text,
                location,
                distance=2000,
                category=None
                ):
        """
        The suggest operation is performed on a geocode service resource.
        The result of this operation is a resource representing a list of
        suggested matches for the input text. This resource provides the
        matching text as well as a unique ID value, which links a
        suggestion to a specific place or address.
        A geocode service must meet the following requirements to support
        the suggest operation:
          The address locator from which the geocode service was published
          must support suggestions. Only address locators created using
          ArcGIS 10.3 for Desktop and later can support suggestions. See
          the Create Address Locator geoprocessing tool help topic for more
          information.
          The geocode service must have the Suggest capability enabled.
          Only geocode services published using ArcGIS 10.3 for Server or
          later support the Suggest capability.
        The suggest operation allows character-by-character auto-complete
        suggestions to be generated for user input in a client application.
        This capability facilitates the interactive search user experience
        by reducing the number of characters that need to be typed before
        a suggested match is obtained. A client application can provide a
        list of suggestions that is updated with each character typed by a
        user until the address they are looking for appears in the list.

        Inputs:
           text - The input text provided by a user that is used by the
            suggest operation to generate a list of possible matches. This
            is a required parameter.
           location -  Defines an origin point location that is used with
            the distance parameter to sort suggested candidates based on
            their proximity to the location. The distance parameter
            specifies the radial distance from the location in meters. The
            priority of candidates within this radius is boosted relative
            to those outside the radius.
            This is useful in mobile applications where a user wants to
            search for places in the vicinity of their current GPS
            location. It is also useful for web mapping applications where
            a user wants to find places within or near the map extent.
            The location parameter can be specified without specifying a
            distance. If distance is not specified, it defaults to 2000
            meters.
            The object can be an common.geometry.Point or X/Y list object
           distance - Specifies the radius around the point defined in the
            location parameter to create an area, which is used to boost
            the rank of suggested candidates so that candidates closest to
            the location are returned first. The distance value is in
            meters.
            If the distance parameter is specified, the location parameter
            must be specified as well.
            It is important to note that the location and distance
            parameters allow searches to extend beyond the specified search
            radius. They are not used to filter results, but rather to rank
            resulting candidates based on their distance from a location.
           category - The category parameter is only supported by geocode
            services published using StreetMap Premium locators.
        """
        params = {
            "f" : "json",
            "text" : text
        }
        url = self._url + "/suggest"
        if isinstance(location, Point):
            params['location'] = location.asDictionary
        elif isinstance(location, list):
            params['location'] = "%s,%s" % (location[0], location[1])
        else:
            raise Exception("Invalid location, please try again")
        if not category is None:
            params['category'] = category
        if not distance is None and \
           isinstance(distance, (int, float)):
            params['distance'] = distance
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)