from __future__ import absolute_import
from __future__ import print_function
from .._abstract import abstract
from ..common.geometry import Point, Polyline, Polygon, MultiPoint, Envelope
import json


########################################################################
class GeometryService(abstract.BaseAGSServer):
    """
    A geometry service contains utility methods that provide access to
    sophisticated and frequently used geometric operations. An ArcGIS
    Server web site can only expose one geometry service with the static
    name "Geometry".
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _json_dict = None
    _json_string = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """loads the json values"""
        res = self._get(url=self._url,
                           param_dict={"f": "json"},
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
        self._json_dict = res
        self._json_string = json.dumps(self._json_dict)
        for k,v in self._json_dict.items():
            setattr(self, k, v)
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as a string"""
        if self._json_string is None:
            self.__init()
        return self._json_string
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns the JSON response in key/value pairs"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.items():
            yield [k,v]
    #----------------------------------------------------------------------
    def areasAndLengths(self,
                        polygons,
                        lengthUnit,
                        areaUnit,
                        calculationType,
                        ):
        """
           The areasAndLengths operation is performed on a geometry service
           resource. This operation calculates areas and perimeter lengths
           for each polygon specified in the input array.

           Inputs:
              polygons - The array of polygons whose areas and lengths are
                         to be computed.
              lengthUnit - The length unit in which the perimeters of
                           polygons will be calculated. If calculationType
                           is planar, then lengthUnit can be any esriUnits
                           constant. If lengthUnit is not specified, the
                           units are derived from sr. If calculationType is
                           not planar, then lengthUnit must be a linear
                           esriUnits constant, such as esriSRUnit_Meter or
                           esriSRUnit_SurveyMile. If lengthUnit is not
                           specified, the units are meters. For a list of
                           valid units, see esriSRUnitType Constants and
                           esriSRUnit2Type Constant.
              areaUnit - The area unit in which areas of polygons will be
                         calculated. If calculationType is planar, then
                         areaUnit can be any esriUnits constant. If
                         areaUnit is not specified, the units are derived
                         from sr. If calculationType is not planar, then
                         areaUnit must be a linear esriUnits constant such
                         as esriSRUnit_Meter or esriSRUnit_SurveyMile. If
                         areaUnit is not specified, then the units are
                         meters. For a list of valid units, see
                         esriSRUnitType Constants and esriSRUnit2Type
                         constant.
                         The list of valid esriAreaUnits constants include,
                         esriSquareInches | esriSquareFeet |
                         esriSquareYards | esriAcres | esriSquareMiles |
                         esriSquareMillimeters | esriSquareCentimeters |
                         esriSquareDecimeters | esriSquareMeters | esriAres
                         | esriHectares | esriSquareKilometers.
              calculationType -  The type defined for the area and length
                                 calculation of the input geometries. The
                                 type can be one of the following values:
                                 planar - Planar measurements use 2D
                                          Euclidean distance to calculate
                                          area and length. Th- should
                                          only be used if the area or
                                          length needs to be calculated in
                                          the given spatial reference.
                                          Otherwise, use preserveShape.
                                 geodesic - Use this type if you want to
                                          calculate an area or length using
                                          only the vertices of the polygon
                                          and define the lines between the
                                          points as geodesic segments
                                          independent of the actual shape
                                          of the polygon. A geodesic
                                          segment is the shortest path
                                          between two points on an ellipsoid.
                                 preserveShape - This type calculates the
                                          area or length of the geometry on
                                          the surface of the Earth
                                          ellipsoid. The shape of the
                                          geometry in its coordinate system
                                          is preserved.
           Output:
              JSON as dictionary
        """
        url = self._url + "/areasAndLengths"
        params = {
            "f" : "json",
            "lengthUnit" : lengthUnit,
            "areaUnit" : {"areaUnit" : areaUnit},
            "calculationType" : calculationType
        }
        if isinstance(polygons, list) and len(polygons) > 0:
            p = polygons[0]
            if isinstance(p, Polygon):
                params['sr'] = p.spatialReference['wkid']
                params['polygons'] = [poly.asDictionary for poly in polygons]
            del p
        else:
            return "No polygons provided, please submit a list of polygon geometries"
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def __geometryListToGeomTemplate(self, geometries):
        """
            converts a list of common.Geometry objects to the geometry
            template value
            Input:
               geometries - list of common.Geometry objects
            Output:
               Dictionary in geometry service template
        """
        template = {"geometryType": None,
                    "geometries" : []}
        if isinstance(geometries, list) and len(geometries) > 0:
            for g in geometries:
                if isinstance(g, Polyline):
                    template['geometryType'] = "esriGeometryPolyline"
                elif isinstance(g, Polygon):
                    template['geometryType'] = "esriGeometryPolygon"
                elif isinstance(g, Point):
                    template['geometryType'] = "esriGeometryPoint"
                elif isinstance(g, MultiPoint):
                    template['geometryType'] = "esriGeometryMultipoint"
                elif isinstance(g, Envelope):
                    template['geometryType'] = "esriGeometryEnvelope"
                else:
                    raise AttributeError("Invalid geometry type")
                template['geometries'].append(g.asDictionary)
                del g
            return template
        return template
    #----------------------------------------------------------------------
    def __geometryToGeomTemplate(self, geometry):
        """
           Converts a single geometry object to a geometry service geometry
           template value.

           Input:
              geometry - ArcREST geometry object
           Output:
              python dictionary of geometry template
        """
        template = {"geometryType": None,
                    "geometry" : None}
        if isinstance(geometry, Polyline):
            template['geometryType'] = "esriGeometryPolyline"
        elif isinstance(geometry, Polygon):
            template['geometryType'] = "esriGeometryPolygon"
        elif isinstance(geometry, Point):
            template['geometryType'] = "esriGeometryPoint"
        elif isinstance(geometry, MultiPoint):
            template['geometryType'] = "esriGeometryMultipoint"
        elif isinstance(geometry, Envelope):
            template['geometryType'] = "esriGeometryEnvelope"
        else:
            raise AttributeError("Invalid geometry type")
        template['geometry'] = geometry.asDictionary
        return template
    #----------------------------------------------------------------------
    def __geomToStringArray(self, geometries, returnType="str"):
        """ function to convert the geomtries to strings """
        listGeoms = []
        for g in geometries:
            if isinstance(g, Point):
                listGeoms.append(g.asDictionary)
            elif isinstance(g, Polygon):
                listGeoms.append(g.asDictionary) #json.dumps(
            elif isinstance(g, Polyline):
                listGeoms.append({'paths' : g.asDictionary['paths']})
        if returnType == "str":
            return json.dumps(listGeoms)
        elif returnType == "list":
            return listGeoms
        else:
            return json.dumps(listGeoms)
    #----------------------------------------------------------------------
    def autoComplete(self,
                     polygons=[],
                     polylines=[],
                     sr=None
                     ):
        """
           The autoComplete operation simplifies the process of
           constructing new polygons that are adjacent to other polygons.
           It constructs polygons that fill in the gaps between existing
           polygons and a set of polylines.

           Inputs:
              polygons - array of Polygon objects
              polylines - list of Polyline objects
              sr - spatial reference of the input geometries WKID
        """
        url = self._url + "/autoComplete"
        params = {"f":"json"}
        if sr is not None:
            params['sr'] = sr
        params['polygons'] = self.__geomToStringArray(polygons)
        params['polylines'] = self.__geomToStringArray(polylines)
        return self._get(url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def buffer(self,
               geometries,
               inSR,
               distances,
               units,
               outSR=None,
               bufferSR=None,
               unionResults=True,
               geodesic=True
               ):
        """
           The buffer operation is performed on a geometry service resource
           The result of this operation is buffered polygons at the
           specified distances for the input geometry array. Options are
           available to union buffers and to use geodesic distance.

           Inputs:
             geometries - array of geometries (structured as JSON geometry 
                          objects returned by the ArcGIS REST API)
             inSR - spatial reference of the input geometries WKID
             outSR - spatial reference for the returned geometries
             bufferSR - WKID or a spatial reference JSON object in 
                        which the geometries are buffered
             distances - distances that each of the input geometries is buffered
             unit - units for calculating each buffer distance
             unionResults - if true, all geometries buffered at a given distance 
                            are unioned into a single (possibly multipart) polygon, 
                            and the unioned geometry is placed in the output array.
             geodesic - set geodesic to true to buffer the using geodesic distance.
        """
        url = self._url + "/buffer"
        params = {
            "f" : "json",
            "inSR" : inSR,
            "geodesic" : geodesic,
            "unionResults" : unionResults
        }
        if isinstance(geometries, list) and len(geometries) > 0:
            g = geometries[0]
            if isinstance(g, Polygon):
                params['geometries'] = {"geometryType": "esriGeometryPolygon",
                                        "geometries" : self.__geomToStringArray(geometries, "list")}
            elif isinstance(g, Point):
                params['geometries'] = {"geometryType": "esriGeometryPoint",
                                        "geometries" : self.__geomToStringArray(geometries, "list")}
            elif isinstance(g, Polyline):
                params['geometries'] = {"geometryType": "esriGeometryPolyline",
                                                        "geometries" : self.__geomToStringArray(geometries, "list")}
        else:
            return None
        if isinstance(distances, list):
            distances = [str(d) for d in distances]

            params['distances'] = ",".join(distances)
        else:
            params['distances'] = str(distances)
        params['units'] = units
        if bufferSR is not None:
            params['bufferSR'] = bufferSR
        if outSR is not None:
            params['outSR'] = outSR
        return self._get(url, param_dict=params,
                            proxy_port=self._proxy_port,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def convexHull(self,
                   geometries,
                   sr=None):
        """
        The convexHull operation is performed on a geometry service resource. 
        It returns the convex hull of the input geometry. The input geometry can 
        be a point, multipoint, polyline, or polygon. The convex hull is typically 
        a polygon but can also be a polyline or point in degenerate cases.
        
        Inputs:
            geometries - array of geometries (structured as JSON geometry 
                         objects returned by the ArcGIS REST API)
            sr - spatial reference of the input geometries WKID
        """
        url = self._url + "/convexHull"
        params = {
            "f" : "json"
        }

        if isinstance(geometries, list) and len(geometries) > 0:
            g = geometries[0]
            if sr is not None:
                params['sr'] = sr
            else:
                params['sr'] = g._wkid
            if isinstance(g, Polygon):
                params['geometries'] = {"geometryType": "esriGeometryPolygon",
                                        "geometries" : self.__geomToStringArray(geometries, "list")}
            elif isinstance(g, Point):
                params['geometries'] = {"geometryType": "esriGeometryPoint",
                                        "geometries" : self.__geomToStringArray(geometries, "list")}
            elif isinstance(g, Polyline):
                params['geometries'] = {"geometryType": "esriGeometryPolyline",
                                                        "geometries" : self.__geomToStringArray(geometries, "list")}
        else:
            return None
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def cut(self,
            cutter,
            target,
            sr=None):
        """
        The cut operation is performed on a geometry service resource. 
        This operation splits the target polyline or polygon where it's 
        crossed by the cutter polyline.
        Inputs:
            cutter - polyline that will be used to divide the target into 
                     pieces where it crosses the target (structured as 
                     JSON polyline objects returned by the ArcGIS REST API)
            target - array of polylines/polygons to be cut (structured as 
                     JSON geometry objects returned by the ArcGIS REST API)
            sr - spatial reference of the input geometries WKID
        """
        url = self._url + "/cut"
        params = {
            "f" : "json"
        }
        if sr is not None:
            params['sr'] = sr
        if isinstance(cutter, Polyline):
            params['cutter'] = cutter.asDictionary
        else:
            raise AttributeError("Input must be type Polyline")
        if isinstance(target, list) and len(target) > 0:
            geoms = []
            template = {"geometryType": "",
                        "geometries" : []}
            for g in target:
                if isinstance(g, Polygon):
                    template['geometryType'] = "esriGeometryPolygon"
                    template['geometries'].append(g.asDictionary)
                if isinstance(g, Polyline):
                    template['geometryType'] = "esriGeometryPolyline"
                    template['geometries'].append(g.asDictionary)
                else:
                    AttributeError("Invalid geometry in target, entries can only be Polygon or Polyline")
                del g
            params['target'] = template
        else:
            AttributeError("You must provide at least 1 Polygon/Polyline geometry in a list")
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def density(self,
                geometries,
                sr,
                maxSegmentLength,
                lengthUnit,
                geodesic=False,
                ):
        """"""
        url = self._url + "/densify"
        params = {
            "f" : "json",
            "sr" : sr,
            "maxSegmentLength" : maxSegmentLength,
            "lengthUnit" : lengthUnit,
            "geodesic" : geodesic
        }
        if isinstance(geometries, list) and len(geometries) > 0:
            template = {"geometryType": None,
                        "geometries" : []}
            for g in geometries:
                if isinstance(g, Polyline):
                    template['geometryType'] = "esriGeometryPolyline"
                elif isinstance(g, Polygon):
                    template['geometryType'] = "esriGeometryPolygon"
                else:
                    raise AttributeError("Invalid geometry type")
                template['geometries'].append(g.asDictionary)
            params['geometries'] = template
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port = self._proxy_port)
    #----------------------------------------------------------------------
    def difference(self,
                   geometries,
                   sr,
                   geometry
                   ):
        """"""
        url = self._url + "/difference"
        params = {
            "f" : "json",
            "sr" : sr

        }
        if isinstance(geometries, list) and len(geometries) > 0:
            template = {"geometryType": None,
                        "geometries" : []}
            for g in geometries:
                if isinstance(g, Polyline):
                    template['geometryType'] = "esriGeometryPolyline"
                elif isinstance(g, Polygon):
                    template['geometryType'] = "esriGeometryPolygon"
                elif isinstance(g, Point):
                    template['geometryType'] = "esriGeometryPoint"
                elif isinstance(g, Point):
                    template['geometryType'] = "esriGeometryMultipoint"
                else:
                    raise AttributeError("Invalid geometry type")
                template['geometries'].append(g.asDictionary)
            del g
            params['geometries'] = template
        geomTemplate = {"geometryType": None,
                        "geometries" : []
                        }
        if isinstance(geometry, Polyline):
            geomTemplate['geometryType'] = "esriGeometryPolyline"
        elif isinstance(geometry, Polygon):
            geomTemplate['geometryType'] = "esriGeometryPolygon"
        elif isinstance(geometry, Point):
            geomTemplate['geometryType'] = "esriGeometryPoint"
        elif isinstance(geometry, Point):
            geomTemplate['geometryType'] = "esriGeometryMultipoint"
        else:
            raise AttributeError("Invalid geometry type")
        geomTemplate['geometry'] = geometry.asDictionary
        params['geometry'] = geomTemplate
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def distance(self,
                 sr,
                 geometry1,
                 geometry2,
                 distanceUnit="",
                 geodesic=False
                 ):
        """"""
        url = self._url + "/distance"
        params = {
            "f" : "json",
            "sr" : sr,
            "distanceUnit" : distanceUnit,
            "geodesic" : geodesic
        }
        geometry1 = self.__geometryToGeomTemplate(geometry=geometry1)
        geometry2 = self.__geometryToGeomTemplate(geometry=geometry2)
        params['geometry1'] = geometry1
        params['geometry2'] = geometry2
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def findTransformation(self, inSR, outSR, extentOfInterest=None, numOfResults=1):
        """
        The findTransformations operation is performed on a geometry
        service resource. This operation returns a list of applicable
        geographic transformations you should use when projecting
        geometries from the input spatial reference to the output spatial
        reference. The transformations are in JSON format and are returned
        in order of most applicable to least applicable. Recall that a
        geographic transformation is not needed when the input and output
        spatial references have the same underlying geographic coordinate
        systems. In this case, findTransformations returns an empty list.
        Every returned geographic transformation is a forward
        transformation meaning that it can be used as-is to project from
        the input spatial reference to the output spatial reference. In the
        case where a predefined transformation needs to be applied in the
        reverse direction, it is returned as a forward composite
        transformation containing one transformation and a transformForward
        element with a value of false.

        Inputs:
           inSR - The well-known ID (WKID) of the spatial reference or a
             spatial reference JSON object for the input geometries
           outSR - The well-known ID (WKID) of the spatial reference or a
             spatial reference JSON object for the input geometries
           extentOfInterest -  The bounding box of the area of interest
             specified as a JSON envelope. If provided, the extent of
             interest is used to return the most applicable geographic
             transformations for the area. If a spatial reference is not
             included in the JSON envelope, the inSR is used for the
             envelope.
           numOfResults - The number of geographic transformations to
             return. The default value is 1. If numOfResults has a value of
             -1, all applicable transformations are returned.
        """
        params = {
            "f" : "json",
            "inSR" : inSR,
            "outSR" : outSR
        }
        url = self._url + "/findTransformations"
        if isinstance(numOfResults, int):
            params['numOfResults'] = numOfResults
        if isinstance(extentOfInterest, Envelope):
            params['extentOfInterest'] = extentOfInterest.asDictionary
        return self._post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def fromGeoCoordinateString(self, sr, strings,
                                conversionType, conversionMode=None):
        """
        The fromGeoCoordinateString operation is performed on a geometry
        service resource. The operation converts an array of well-known
        strings into xy-coordinates based on the conversion type and
        spatial reference supplied by the user. An optional conversion mode
        parameter is available for some conversion types.

        Inputs:
         sr - The well-known ID of the spatial reference or a spatial
          reference json object.
         strings - An array of strings formatted as specified by
          conversionType.
          Syntax: [<string1>,...,<stringN>]
          Example: ["01N AA 66021 00000","11S NT 00000 62155",
                    "31U BT 94071 65288"]
         conversionType - The conversion type of the input strings.
          Valid conversion types are:
           MGRS - Military Grid Reference System
           USNG - United States National Grid
           UTM - Universal Transverse Mercator
           GeoRef - World Geographic Reference System
           GARS - Global Area Reference System
           DMS - Degree Minute Second
           DDM - Degree Decimal Minute
           DD - Decimal Degree
         conversionMode - Conversion options for MGRS, UTM and GARS
          conversion types.
          Conversion options for MGRS and UTM conversion types.
          Valid conversion modes for MGRS are:
           mgrsDefault - Default. Uses the spheroid from the given spatial
            reference.
           mgrsNewStyle - Treats all spheroids as new, like WGS 1984. The
            180 degree longitude falls into Zone 60.
           mgrsOldStyle - Treats all spheroids as old, like Bessel 1841.
            The 180 degree longitude falls into Zone 60.
           mgrsNewWith180InZone01 - Same as mgrsNewStyle except the 180
            degree longitude falls into Zone 01.
           mgrsOldWith180InZone01 - Same as mgrsOldStyle except the 180
            degree longitude falls into Zone 01.
          Valid conversion modes for UTM are:
           utmDefault - Default. No options.
           utmNorthSouth - Uses north/south latitude indicators instead of
            zone numbers. Non-standard. Default is recommended
        """
        url = self._url + "/fromGeoCoordinateString"
        params = {
            "f" : "json",
            "sr" : sr,
            "strings" : strings,
            "conversionType" : conversionType
        }
        if not conversionMode is None:
            params['conversionMode'] = conversionMode
        return self._post(url=url, param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def generalize(self,
                   sr,
                   geometries,
                   maxDeviation,
                   deviationUnit):
        """"""
        url = self._url + "/generalize"
        params = {
            "f" : "json",
            "sr" : sr,
            "deviationUnit" : deviationUnit,
            "maxDeviation": maxDeviation
        }
        params['geometries'] = self.__geometryListToGeomTemplate(geometries=geometries)
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_port=self._proxy_port,
                            proxy_url=self._proxy_url)
    #----------------------------------------------------------------------
    def intersect(self,
                  sr,
                  geometries,
                  geometry
                  ):
        """"""
        url = self._url + "/intersect"
        params = {
            "f" : "json",
            "sr" : sr,
            "geometries" : self.__geometryListToGeomTemplate(geometries=geometries),
            "geometry" : self.__geometryToGeomTemplate(geometry=geometry)
        }
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def labelPoints(self,
                    sr,
                    polygons,
                    ):
        """"""
        url = self._url + "/labelPoints"
        params = {
            "f" : "json",
            "sr" : sr,
            "polygons": self.__geomToStringArray(geometries=polygons,
                                                 returnType="list")
        }
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def lengths(self,
                sr,
                polylines,
                lengthUnit,
                calculationType
                ):
        """"""
        allowedCalcTypes = ['planar', 'geodesic', 'preserveShape']
        if calculationType not in allowedCalcTypes:
            raise AttributeError("Invalid calculation Type")
        url = self._url + "/lengths"
        params = {
            "f" : "json",
            "sr" : sr,
            "polylines": self.__geomToStringArray(geometries=polylines,
                                                 returnType="list"),
            "lengthUnit" : lengthUnit,
            "calculationType" : calculationType
        }

        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def offset(self,
               geometries,
               offsetDistance,
               offsetUnit,
               offsetHow="esriGeometryOffsetRounded",
               bevelRatio=10,
               simplifyResult=False,
               sr=None,
               ):
        """"""
        allowedHow = ["esriGeometryOffsetRounded",
                      "esriGeometryOffsetBevelled",
                      "esriGeometryOffsetMitered"]
        if offsetHow not in allowedHow:
            raise AttributeError("Invalid Offset How value")
        url = self._url + "/offset"
        params = {
            "f" : "json",
            "sr" : sr,
            "geometries": self.__geometryListToGeomTemplate(geometries=geometries),
            "offsetDistance": offsetDistance,
            "offsetUnit" : offsetUnit,
            "offsetHow" : offsetHow,
            "bevelRatio" : bevelRatio,
            "simplifyResult" : simplifyResult
        }
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def project(self,
                geometries,
                inSR,
                outSR,
                transformation="",
                transformFoward=False):
        """"""
        url = self._url + "/project"
        params = {
            "f" : "json",
            "inSR" : inSR,
            "geometries": self.__geometryListToGeomTemplate(geometries=geometries),
            "outSR" : outSR,
            "transformation" : transformation,
            "transformFoward": transformFoward
        }
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def relation(self,
                 geometries1,
                 geometries2,
                 sr,
                 relation="esriGeometryRelationIntersection",
                 relationParam=""):
        """"""
        relationType = [
            "esriGeometryRelationCross",
            "esriGeometryRelationDisjoint",
            "esriGeometryRelationIn",
            "esriGeometryRelationInteriorIntersection",
            "esriGeometryRelationIntersection",
            "esriGeometryRelationLineCoincidence",
            "esriGeometryRelationLineTouch",
            "esriGeometryRelationOverlap",
            "esriGeometryRelationPointTouch",
            "esriGeometryRelationTouch",
            "esriGeometryRelationWithin",
            "esriGeometryRelationRelation"
        ]
        if relation not in relationType:
            raise AttributeError("Invalid relation type")
        url = self._url + "/relation"
        params = {
            "f" : "json",
            "sr" : sr,
            "geometries1": self.__geometryListToGeomTemplate(geometries=geometries1),
            "geometries2": self.__geometryListToGeomTemplate(geometries=geometries2),
            "relation" : relation,
            "relationParam" : relationParam
        }
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def reshape(self,
                sr,
                target,
                reshaper
                ):
        """calls the reshape command on a geometry service"""
        url = self._url + "/reshape"
        params = {
            "f" : "json",
            "sr" : sr,
            "target" : self.__geometryToGeomTemplate(geometry=target)
        }
        if isinstance(reshaper, Polyline):
            params["reshaper"] = reshaper.asDictionary
        else:
            raise AttributeError("Invalid reshaper object, must be Polyline")
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def simplify(self,
                 sr,
                 geometries
                 ):
        """returns a simplied geometry object"""
        url = self._url + "/simplify"
        params = {
            "f" : "json",
            "sr" : sr,
            "geometries" : self.__geometryListToGeomTemplate(geometries=geometries)
        }
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def toGeoCoordinateString(self,
                              sr,
                              coordinates,
                              conversionType,
                              conversionMode="mgrsDefault",
                              numOfDigits=None,
                              rounding=True,
                              addSpaces=True
                              ):
        """
        The toGeoCoordinateString operation is performed on a geometry
        service resource. The operation converts an array of
        xy-coordinates into well-known strings based on the conversion type
        and spatial reference supplied by the user. Optional parameters are
        available for some conversion types. Note that if an optional
        parameter is not applicable for a particular conversion type, but a
        value is supplied for that parameter, the value will be ignored.

        Inputs:
          sr -  The well-known ID of the spatial reference or a spatial
           reference json object.
          coordinates - An array of xy-coordinates in JSON format to be
           converted. Syntax: [[x1,y2],...[xN,yN]]
          conversionType - The conversion type of the input strings.
           Allowed Values:
            MGRS - Military Grid Reference System
            USNG - United States National Grid
            UTM - Universal Transverse Mercator
            GeoRef - World Geographic Reference System
            GARS - Global Area Reference System
            DMS - Degree Minute Second
            DDM - Degree Decimal Minute
            DD - Decimal Degree
          conversionMode - Conversion options for MGRS and UTM conversion
           types.
           Valid conversion modes for MGRS are:
            mgrsDefault - Default. Uses the spheroid from the given spatial
             reference.
            mgrsNewStyle - Treats all spheroids as new, like WGS 1984. The
             180 degree longitude falls into Zone 60.
            mgrsOldStyle - Treats all spheroids as old, like Bessel 1841.
             The 180 degree longitude falls into Zone 60.
            mgrsNewWith180InZone01 - Same as mgrsNewStyle except the 180
             degree longitude falls into Zone 01.
            mgrsOldWith180InZone01 - Same as mgrsOldStyle except the 180
             degree longitude falls into Zone 01.
           Valid conversion modes for UTM are:
            utmDefault - Default. No options.
            utmNorthSouth - Uses north/south latitude indicators instead of
             zone numbers. Non-standard. Default is recommended.
          numOfDigits - The number of digits to output for each of the
           numerical portions in the string. The default value for
           numOfDigits varies depending on conversionType.
          rounding - If true, then numeric portions of the string are
           rounded to the nearest whole magnitude as specified by
           numOfDigits. Otherwise, numeric portions of the string are
           truncated. The rounding parameter applies only to conversion
           types MGRS, USNG and GeoRef. The default value is true.
          addSpaces - If true, then spaces are added between components of
           the string. The addSpaces parameter applies only to conversion
           types MGRS, USNG and UTM. The default value for MGRS is false,
           while the default value for both USNG and UTM is true.
        """
        params = {
            "f": "json",
            "sr" : sr,
            "coordinates" : coordinates,
            "conversionType": conversionType
        }
        url = self._url + "/toGeoCoordinateString"
        if not conversionMode is None:
            params['conversionMode'] = conversionMode
        if isinstance(numOfDigits, int):
            params['numOfDigits'] = numOfDigits
        if isinstance(rounding, int):
            params['rounding'] = rounding
        if isinstance(addSpaces, bool):
            params['addSpaces'] = addSpaces
        return self._post(url=url,
                             param_dict=params,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port,
                             securityHandler=self._securityHandler)
    #----------------------------------------------------------------------
    def trimExtend(self,
                   sr,
                   polylines,
                   trimExtendTo,
                   extendHow=0):
        """"""
        allowedHow = [0,1,2,4,8,16]
        if extendHow not in allowedHow:
            raise AttributeError("Invalid extend How value.")
        url = self._url + "/trimExtend"
        params = {
            "f" : "json",
            "sr" : sr,
            "polylines" : self.__geomToStringArray(geometries=polylines, returnType="list"),
            "extendHow": extendHow,
            "trimExtendTo" : trimExtendTo.asDictionary

        }

        return self._get(url=url, param_dict=params,
                            proxy_url=self._proxy_url,
                            securityHandler=self._securityHandler,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def union(self,
              sr,
              geometries):
        """"""
        url = self._url + "/union"
        params = {
            "f" : "json",
            "sr" : sr,
            "geometries" : self.__geometryListToGeomTemplate(geometries=geometries)
        }
        return self._get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
