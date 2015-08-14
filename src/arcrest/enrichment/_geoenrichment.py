from ..common.geometry import Point, Polygon, Envelope, SpatialReference
from .. import AGOLTokenSecurityHandler
from .._abstract.abstract import BaseGeoEnrichment
from ..manageorg import Administration
import json
import csv
import os
import numpy as np
########################################################################
class GeoEnrichment(BaseGeoEnrichment):
    """"""
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _countryCodeFile = None
    _dataCollectionNames = None
    _countrycodes = None
    _datacollectionnames = None
    _dataCollectionFile = None
    _base_url = "http://geoenrich.arcgis.com/arcgis/rest/services/World/geoenrichmentserver"
    _url_standard_geography_query = "/StandardGeographyLevels" # returns boundaries
    _url_standard_geography_query_execute = "/StandardGeographyQuery/execute" # returns report
    _url_getVariables = "/GetVariables/execute" # returns report
    _url_create_report = "/GeoEnrichment/createreport" # generates a report
    _url_list_reports = "/Geoenrichment/Reports" # return report types for a country
    _url_data_collection = "/Geoenrichment/dataCollections"
    #----------------------------------------------------------------------
    def __init__(self,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        else:
            raise Exception("A SecurityHandler object is required for this object.")
        admin = Administration(securityHandler=securityHandler,
                               proxy_url=proxy_url,
                               proxy_port=proxy_port)
        self._base_url = admin.portals.portalSelf.helperServices['geoenrichment']['url']
        del admin
        self._securityHandler = securityHandler
        self._countryCodeFile = os.path.join(os.path.dirname(__file__),
                                             "__countrycodes.csv")
        self._dataCollectionFile = os.path.join(os.path.dirname(__file__),
                                             "__datacollectionnames.csv")
        self._countrycodes = self._readcsv(self._countryCodeFile)
        self._dataCollectionCodes = self._readcsv(path_to_csv=self._dataCollectionFile)
    #----------------------------------------------------------------------
    def _readcsv(self, path_to_csv):
        """reads a csv column"""
        import numpy as np
        return np.genfromtxt(path_to_csv,
                             dtype=None,
                             delimiter=',',
                             names=True)
    #----------------------------------------------------------------------
    @property
    def allowedTwoDigitCountryCodes(self):
        """returns a list of accepted two digit country codes"""
        return self._countrycodes['Two_Digit_Country_Code']
    #----------------------------------------------------------------------
    @property
    def allowedCountryNames(self):
        """returns a list of accepted country names"""
        return self._countrycodes['Country_Name']
    #----------------------------------------------------------------------
    @property
    def allowedThreeDigitNames(self):
        """returns a list of accepted three digit country codes"""
        return self._countrycodes['Three_Digit_Country_Code']
    #----------------------------------------------------------------------
    @property
    def dataCollectionNames(self):
        """returns a list of data collection names"""
        return self._dataCollectionCodes['Data_Collection_Name']
    #----------------------------------------------------------------------
    def queryDataCollectionByName(self, countryName):
        """
        returns a list of available data collections for a given country
        name.

        Inputs:
           countryName - name of the country to file the data collection.
        Output:
           list or None. None implies could not find the countryName
        """
        var = self._dataCollectionCodes
        try:
            return [x[0] for x in var[var['Countries'] == countryName]]
        except:
            return None
    #----------------------------------------------------------------------
    def findCountryTwoDigitCode(self, countryName):
        """
        Returns the two digit code based on a country name

        Inputs:
           countryName - name of the country to file the data collection.
        Output:
           list or None. None implies could not find the countryName
        """
        var = self._countrycodes
        try:
            return var[var['Country_Name'] == countryName][0][1]
        except:
            return None
    #----------------------------------------------------------------------
    def findCountryThreeDigitCode(self, countryName):
        """
        Returns the three digit code based on a country name

        Inputs:
           countryName - name of the country to file the data collection.
        Output:
           list or None. None implies could not find the countryName
        """
        var = self._countrycodes
        try:
            return var[var['Country_Name'] == countryName][0][2]
        except:
            return None
    #----------------------------------------------------------------------
    def __geometryToDict(self, geom):
        """converts a geometry object to a dictionary"""
        if isinstance(geom, dict):
            return geom
        elif isinstance(geom, Point):
            pt = geom.asDictionary
            return {"geometry": {"x" : pt['x'], "y" : pt['y']}}
        elif isinstance(geom, Polygon):
            poly = geom.asDictionary
            return {
                "geometry" : {
                    "rings" : poly['rings'],
                    'spatialReference' : poly['spatialReference']
                }
            }
        elif isinstance(geom, list):
            return [self.__geometryToDict(g) for g in geom]
    #----------------------------------------------------------------------
    def lookUpReportsByCountry(self, countryName):
        """
        looks up a country by it's name
        Inputs
           countryName - name of the country to get reports list.
        """

        code = self.findCountryTwoDigitCode(countryName)

        if code is None:
            raise Exception("Invalid country name.")
        url = self._base_url + self._url_list_reports + "/%s" % code
        params = {
            "f" : "json",
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def createReport(self,
                     out_file_path,
                     studyAreas,
                     report=None,
                     format="PDF",
                     reportFields=None,
                     studyAreasOptions=None,
                     useData=None,
                     inSR=4326,
                     ):
        """
        The GeoEnrichment Create Report method uses the concept of a study
        area to define the location of the point or area that you want to
        enrich with generated reports. This method allows you to create
        many types of high-quality reports for a variety of use cases
        describing the input area. If a point is used as a study area, the
        service will create a 1-mile ring buffer around the point to
        collect and append enrichment data. Optionally, you can create a
        buffer ring or drive-time service area around the points to prepare
        PDF or Excel reports for the study areas.

        Note:
          For full examples for each input, please review the following:
          http://resources.arcgis.com/en/help/arcgis-rest-api/#/Create_report/02r30000022q000000/

        Inputs:
          out_file_path - save location of the report
          studyAreas - Required parameter to specify a list of input
            features to be enriched. The input can be a Point, Polygon,
            Adress, or named administrative boundary.  The locations can be
            passed in as a single object or as a list of objects.
          report - Default report to generate.
          format - specify the generated report. Options are: XLSX or PDF
          reportFields - Optional parameter specifies additional choices to
            customize reports.  See the URL above to see all the options.
          studyAreasOptions - Optional parameter to specify enrichment
            behavior. For points described as map coordinates, a 1-mile
            ring area centered on each site will be used by default. You
            can use this parameter to change these default settings.
            With this parameter, the caller can override the default
            behavior describing how the enrichment attributes are appended
            to the input features described in studyAreas. For example,
            you can change the output ring buffer to 5 miles, change the
            number of output buffers created around each point, and also
            change the output buffer type to a drive-time service area
            rather than a simple ring buffer.
          useData - By default, the service will automatically determine
            the country or dataset that is associated with each location or
            area submitted in the studyAreas parameter; however, there is
            an associated computational cost which may lengthen the time it
            takes to return a response. To skip this intermediate step and
            potentially improve the speed and performance of the service,
            the caller can specify the country or dataset information up
            front through this parameter.
          inSR - parameter to define the input geometries in the studyAreas
            parameter in a specified spatial reference system.
        """
        url = self._base_url + self._url_create_report
        if isinstance(studyAreas, list) == False:
            studyAreas = [studyAreas]
        studyAreas = self.__geometryToDict(studyAreas)

        params = {
            "f" : "bin",
            "studyAreas" : studyAreas,
            "inSR" : inSR,
        }
        if not report is None:
            params['report'] = report
        if format is None:
            format = "pdf"
        elif format.lower() in ['pdf', 'xlsx']:
            params['format'] = format.lower()
        else:
            raise AttributeError("Invalid format value.")
        if not reportFields is None:
            params['reportFields'] = reportFields
        if not studyAreasOptions is None:
            params['studyAreasOptions'] = studyAreasOptions
        if not useData is None:
            params['useData'] = useData
        return self._download_file(url=url,
                                   save_path=os.path.dirname(out_file_path),
                                   file_name=None,
                                   param_dict=params,
                                   securityHandler=self._securityHandler,
                                   proxy_url=self._proxy_url,
                                   proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def dataCollections(self,
                        countryName=None,
                        addDerivativeVariables=["*"],
                        outFields=["*"],
                        suppressNullValues=False):
        """
        The GeoEnrichment service uses the concept of a data collection to
        define the data attributes returned by the enrichment service. Each
        data collection has a unique name that acts as an ID that is passed
        in the dataCollections parameter of the GeoEnrichment service.
        Some data collections (such as default) can be used in all
        supported countries. Other data collections may only be available
        in one or a collection of countries. Data collections may only be
        available in a subset of countries because of differences in the
        demographic data that is available for each country. A list of data
        collections for all available countries can be generated with the
        data collection discover method.

        For full help please go here:
        http://resources.arcgis.com/en/help/arcgis-rest-api/#/Data_collections/02r30000021t000000/

        Inputs:
           countryName - lets the user supply and optional name of a
             country in order to get information about the data collections
             in that given country.
           addDerivativeVariables - Optional parameter to specify a list of
             field names that include variables for the derivative
             statistics.
           outFields - Optional parameter to specify a list of output
             fields in the response.
           suppressNullValues - Optional parameter to return only values
             that are not NULL in the output response. Adding the optional
             suppressNullValues parameter to any data collections discovery
             method will reduce the size of the output that is returned
        """
        if countryName is None:
            url = self._base_url + self._url_data_collection
        else:
            url = self._base_url + self._url_data_collection + "/%s" % countryName
        params = {
            "f" : "token"
        }
        _addDerivVals = ["percent","index","average","all","*"]
        if addDerivativeVariables in _addDerivVals:
            params['addDerivativeVariables'] = addDerivativeVariables
        if not outFields is None:
            params['outFields'] = outFields
        if not suppressNullValues is None and \
           isinstance(suppressNullValues, bool):
            if suppressNullValues:
                params['suppressNullValues'] = "true"
            else:
                params['suppressNullValues'] = "false"
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def getVariables(self,
                     sourceCountry,
                     optionalCountryDataset=None,
                     searchText=None):
        r"""
        The GeoEnrichment GetVariables helper method allows you to search
        the data collections for variables that contain specific keywords.

        To see the comprehensive set of global Esri Demographics data that
        are available, use the interactive data browser:
        http://resources.arcgis.com/en/help/arcgis-rest-api/02r3/02r300000266000000.htm#GUID-2D66F7F8-83A9-4EAA-B5E2-F09D629939CE

        Inputs:
        sourceCountry - specify the source country for the search. Use this
         parameter to limit the search and query of standard geographic
         features to one country. This parameter supports both the
         two-digit and three-digit country codes illustrated in the
         coverage table.
            Examples
                    Example 1 - Set source country to the United States:
                    sourceCountry=US

            Example 2 - Set source country to the Canada:
                    sourceCountry=CA

            Additional notes
                    Currently, the service is available for Canada, the
                    United States and a number of European countries. Other
                    countries will be added in the near future.
                    The list of available countries and their associated
                    IDS are listed in the coverage section.
        optionalCountryDataset - Optional parameter to specify a specific
         dataset within a defined country. This parameter will not be used
         in the Beta release. In the future, some countries may have two or
         more datasets that may have different vintages and standard
         geography areas. For example, in the United States, there may be
         an optional dataset with historic census data from previous years.
            Examples
                    optionalCountryDataset=USA_ESRI_2013
            Additional notes
                    Most countries only have a single dataset.
                    The United States has multiple datasets.
        searchText - Optional parameter to specify the text to query and
         search the data collections for the country and datasets
         specified. You can use this parameter to query and find specific
         keywords that are contained in a data collection.
            Default value
                    (null or empty)
            Examples
                    Example 1 - Return all the data collections and variabels that contain the word furniture:
                    searchText=furniture
            Search terms
                    A query is broken up into terms and operators. There are two types of terms: Single Terms and Phrases.
                    A Single Term is a single word such as "Income" or "Households".
                    A Phrase is a group of words surrounded by double quotes such as "Household Income".
                    Multiple terms can be combined together with Boolean operators to form a more complex query (see below).
            Fields
                    Geography search supports fielded data. When performing a search, you can either specify a field or use search through all fields.
                    You can search any field by typing the field name followed by a colon ":" then the term you are looking for.
                    For example, to search for "Income" in the Alias field:
                            Alias:Income
                    The search supports single and multiple character wildcard searches within single terms (not within phrase queries).
                    To perform a single character wildcard search, use the "?" symbol.
                    To perform a multiple character wildcard search, use the "*" symbol.
                    The single character wildcard search looks for terms that match that with the single character replaced. For example, to search for "San" or "Sen" you can use the search:
            Fuzzy searches
                    Fuzzy searches are based on the Levenshtein Distance or Edit Distance algorithm. To perform a fuzzy search, you can explicitly set a fuzzy search by using the tilde symbol "~" at the end of a Single Term.
                    For example, a term similar in spelling to "Hous" uses the fuzzy search:
                            Hous~
                    An additional (optional) numeric parameter can be specified after the tilde symbol ("~") to set the similarity tolerance. The value is between 0 and 1; with a value closer to 1, only terms with a higher similarity will be matched.
                    For example, if you only want to match terms with a similarity of 0.0 or higher, you can set the fuzzy search as follows:
                            hous~0.8
                    The default that is used if the optional similarity number is not provided is 0.5.
            Boolean operators
                    Boolean operators allow terms to be combined through logic operators. The search supports AND, "+", OR, NOT and "-" as Boolean operators. Boolean operators must be ALL CAPS.
                    In searchText , the AND operator is the default conjunction operator. This means that if there is no Boolean operator between two or more terms, the AND operator is used. The AND operator matches items where both terms exist anywhere in the list of standard geography features. The symbol "&" can be used in place of the word AND.
                    The OR operator links two terms and finds a matching variable if either of the terms exist. This is equivalent to a union with using sets. The symbol "||" can be used in place of the word OR.
                    To search for features that contain either "Income" or "Wealth" use the following query:
                            Income OR Wealth
                    The "+" or required operator requires that the term after the "+" symbol exist somewhere in the attributes of a variable.
                    To search for features that must contain "Income" and may contain "Household" use the following query:
                            +Income OR Household
                    Escaping Special Characters
                            Search supports escaping special characters that are part of the query syntax. The available special characters are as follows:
                            + - && || ! ( ) { } [ ] ^ " ~ * ? : \
                            To escape these characters, use the \ before the character.

        """
        url = self._base_url + self._url_getVariables
        params = {
            "f" : "json",
            "sourceCountry" : sourceCountry
        }
        if not searchText is None:
            params["searchText"] = searchText
        if not optionalCountryDataset is None:
            params['optionalCountryDataset'] = optionalCountryDataset
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def standardGeographyQuery(self,
                               sourceCountry=None,
                               optionalCountryDataset=None,
                               geographyLayers=None,
                               geographyIDs=None,
                               geographyQuery=None,
                               returnSubGeographyLayer=False,
                               subGeographyLayer=None,
                               subGeographyQuery=None,
                               outSR=4326,
                               returnGeometry=False,
                               returnCentroids=False,
                               generalizationLevel=0,
                               useFuzzySearch=False,
                               featureLimit=1000):
        """
        The GeoEnrichment service provides a helper method that returns
        standard geography IDs and features for the supported geographic
        levels in the United States and Canada.
        As indicated throughout this documentation guide, the GeoEnrichment
        service uses the concept of a study area to define the location of
        the point or area that you want to enrich with additional
        information. Locations can also be passed as one or many named
        statistical areas. This form of a study area lets you define an
        area by the ID of a standard geographic statistical feature, such
        as a census or postal area. For example, to obtain enrichment
        information for a U.S. state, county or ZIP Code or a Canadian
        province or postal code, the Standard Geography Query helper method
        allows you to search and query standard geography areas so that
        they can be used in the GeoEnrichment method to obtain facts about
        the location.
        The most common workflow for this service is to find a FIPS
        (standard geography ID) for a geographic name. For example, you can
        use this service to find the FIPS for the county of San Diego which
        is 06073. You can then use this FIPS ID within the GeoEnrichment
        service study area definition to get geometry and optional
        demographic data for the county. This study area definition is
        passed as a parameter to the GeoEnrichment service to return data
        defined in the enrichment pack and optionally return geometry for
        the feature.

        For examples and more help with this function see:
        http://resources.arcgis.com/en/help/arcgis-rest-api/#/Standard_geography_query/02r30000000q000000/

        Inputs:
           sourceCountry - Optional parameter to specify the source country
            for the search. Use this parameter to limit the search and
            query of standard geographic features to one country. This
            parameter supports both the two-digit and three-digit country
            codes illustrated in the coverage table.
           optionalCountryDataset - Optional parameter to specify a
            specific dataset within a defined country.
           geographyLayers - Optional parameter to specify which standard
            geography layers are being queried or searched. If this
            parameter is not provided, all layers within the defined
            country will be queried.
           geographyIDs - Optional parameter to specify which IDs for the
            standard geography layers are being queried or searched. You
            can use this parameter to return attributes and/or geometry for
            standard geographic areas for administrative areas where you
            already know the ID, for example, if you know the Federal
            Information Processing Standard (FIPS) Codes for a U.S. state
            or county; or, in Canada, to return the geometry and attributes
            for a Forward Sortation Area (FSA).
           geographyQuery - Optional parameter to specify the text to query
            and search the standard geography layers specified. You can use
            this parameter to query and find standard geography features
            that meet an input term, for example, for a list of all the
            U.S. counties that contain the word "orange". The
            geographyQuery parameter can be a string that contains one or
            more words.
           returnSubGeographyLayer - Use this optional parameter to return
            all the subgeographic areas that are within a parent geography.
            For example, you could return all the U.S. counties for a given
            U.S. state or you could return all the Canadian postal areas
            (FSAs) within a Census Metropolitan Area (city).
            When this parameter is set to true, the output features will be
            defined in the subGeographyLayer. The output geometries will be
            in the spatial reference system defined by outSR.
           subGeographyLayer - Use this optional parameter to return all
            the subgeographic areas that are within a parent geography. For
            example, you could return all the U.S. counties within a given
            U.S. state or you could return all the Canadian postal areas
            (FSAs) within a Census Metropolitan Areas (city).
            When this parameter is set to true, the output features will be
            defined in the subGeographyLayer. The output geometries will be
            in the spatial reference system defined by outSR.
           subGeographyQuery - Optional parameter to filter the results of
            the subgeography features that are returned by a search term.
            You can use this parameter to query and find subgeography
            features that meet an input term. This parameter is used to
            filter the list of subgeography features that are within a
            parent geography. For example, you may want a list of all the
            ZIP Codes that are within "San Diego County" and filter the
            results so that only ZIP Codes that start with "921" are
            included in the output response. The subgeography query is a
            string that contains one or more words.
           outSR - Optional parameter to request the output geometries in a
            specified spatial reference system.
           returnGeometry - Optional parameter to request the output
            geometries in the response.
           returnCentroids - Optional Boolean parameter to request the
            output geometry to return the center point for each feature.
            Use this parameter to return all the geometries as points. For
            example, you could return all U.S. ZIP Code centroids (points)
            rather than providing the boundaries.
           generalizationLevel - Optional integer that specifies the level
            of generalization or detail in the area representations of the
            administrative boundary or standard geographic data layers.
            Values must be whole integers from 0 through 6, where 0 is most
            detailed and 6 is most generalized.
           useFuzzySearch - Optional Boolean parameter to define if text
            provided in the geographyQuery parameter should utilize fuzzy
            search logic. Fuzzy searches are based on the Levenshtein
            Distance or Edit Distance algorithm.
           featureLimit - Optional integer value where you can limit the
            number of features that are returned from the geographyQuery.
        """
        url = self._base_url + self._url_standard_geography_query_execute
        params = {
            "f" : "json"
        }
        if not sourceCountry is None:
            params['sourceCountry'] = sourceCountry
        if not optionalCountryDataset is None:
            params['optionalCountryDataset'] = optionalCountryDataset
        if not geographyLayers is None:
            params['geographylayers'] = geographyLayers
        if not geographyIDs is None:
            params['geographyids'] = json.dumps(geographyIDs)
        if not geographyQuery is None:
            params['geographyQuery'] = geographyQuery
        if not returnSubGeographyLayer is None and \
           isinstance(returnSubGeographyLayer, bool):
            params['returnSubGeographyLayer'] = returnSubGeographyLayer
        if not subGeographyLayer is None:
            params['subGeographyLayer'] = json.dumps(subGeographyLayer)
        if not subGeographyQuery is None:
            params['subGeographyQuery'] = subGeographyQuery
        if not outSR is None and \
           isinstance(outSR, int):
            params['outSR'] = outSR
        if not returnGeometry is None and \
           isinstance(returnGeometry, bool):
            params['returnGeometry']  = returnGeometry
        if not returnCentroids is None and \
           isinstance(returnCentroids, bool):
            params['returnCentroids'] = returnCentroids
        if not generalizationLevel is None and \
           isinstance(generalizationLevel, int):
            params['generalizationLevel'] = generalizationLevel
        if not useFuzzySearch is None and \
           isinstance(useFuzzySearch, bool):
            params['useFuzzySearch'] = json.dumps(useFuzzySearch)
        if featureLimit is None:
            featureLimit = 1000
        elif isinstance(featureLimit, int):
            params['featureLimit'] = featureLimit
        else:
            params['featureLimit'] = 1000
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
