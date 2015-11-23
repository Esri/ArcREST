from __future__ import absolute_import
from __future__ import print_function
import datetime
import time
import json
try:
    import arcpy
    arcpyFound = True
except:
    arcpyFound = False
import copy
import os
import tempfile
import uuid
from .spatial import json_to_featureclass
from .geometry import Point, MultiPoint, Polygon, Polyline, SpatialReference
from .._abstract.abstract import AbstractGeometry
__all__ = ['_unicode_convert', "Feature", "FeatureSet",
           "_date_handler", "local_time_to_online",
           "online_time_to_string", "timestamp_to_datetime",
           "MosaicRuleObject"]
def _unicode_convert(obj):
    """ converts unicode to anscii """
    if isinstance(obj, dict):
        return {_unicode_convert(key): _unicode_convert(value) for key, value in obj.iteritems()}
    elif isinstance(obj, list):
        return [_unicode_convert(element) for element in obj]
    elif isinstance(obj, unicode):
        return obj.encode('utf-8')
    else:
        return obj
#----------------------------------------------------------------------
def _date_handler(obj):
    if isinstance(obj, datetime.datetime):
        return local_time_to_online(obj)
    else:
        return obj
#----------------------------------------------------------------------
def local_time_to_online(dt=None):
    """
       converts datetime object to a UTC timestamp for AGOL
       Inputs:
          dt - datetime object
       Output:
          Long value
    """
    if dt is None:
        dt = datetime.datetime.now()

    is_dst = time.daylight and time.localtime().tm_isdst > 0
    utc_offset =  (time.altzone if is_dst else time.timezone)

    return (time.mktime(dt.timetuple())  * 1000) + (utc_offset *1000)
#----------------------------------------------------------------------
def online_time_to_string(value,timeFormat):
    """
       Converts a timestamp to date/time string
       Inputs:
          value - timestamp as long
          timeFormat - output date/time format
       Output:
          string
    """
    return datetime.datetime.fromtimestamp(value /1000).strftime(timeFormat)
#----------------------------------------------------------------------
def timestamp_to_datetime(timestamp):
    """
       Converts a timestamp to a datetime object
       Inputs:
          timestamp - timestamp value as Long
       output:
          datetime object
    """
    return datetime.datetime.fromtimestamp(timestamp /1000)
########################################################################
class Feature(object):
    """ returns a feature  """
    _geom = None
    _json = None
    _dict = None
    _geom = None
    _geomType = None
    _attributes = None
    _wkid = None
    #----------------------------------------------------------------------
    def __init__(self, json_string, wkid=None):
        """Constructor"""
        self._wkid = wkid
        if type(json_string) is dict:
            if not wkid is None:
                if 'geometry' in json_string and 'spatialReference' in json_string['geometry']:
                    json_string['geometry']['spatialReference']  = {"wkid" : wkid}
            self._json = json.dumps(json_string,
                                    default=_date_handler)
            self._dict = json_string
        elif type(json_string) is str:
            self._dict = json.loads(json_string)
            if not wkid is None:
                self._dict['geometry']['spatialReference']  = {"wkid" : wkid}
            self._json = json.dumps(self._dict,
                                    default=_date_handler)
        else:
            raise TypeError("Invalid Input, only dictionary or string allowed")
    #----------------------------------------------------------------------
    def set_value(self, field_name, value):
        """ sets an attribute value for a given field name """
        if field_name in self.fields:
            if not value is None:
                self._dict['attributes'][field_name] = _unicode_convert(value)
                self._json = json.dumps(self._dict, default=_date_handler)
            else:
                pass
        elif field_name.upper() in ['SHAPE', 'SHAPE@', "GEOMETRY"]:
            if isinstance(value, AbstractGeometry):
                if isinstance(value, Point):
                    self._dict['geometry'] = {
                    "x" : value.asDictionary['x'],
                    "y" : value.asDictionary['y']
                    }
                elif isinstance(value, MultiPoint):
                    self._dict['geometry'] = {
                        "points" : value.asDictionary['points']
                    }
                elif isinstance(value, Polyline):
                    self._dict['geometry'] = {
                        "paths" : value.asDictionary['paths']
                    }
                elif isinstance(value, Polygon):
                    self._dict['geometry'] = {
                        "rings" : value.asDictionary['rings']
                    }
                else:
                    return False
                self._json = json.dumps(self._dict, default=_date_handler)
            elif arcpyFound and isinstance(value, arcpy.Geometry):
                if isinstance(value, arcpy.PointGeometry):
                    self.set_value( field_name, Point(value,value.spatialReference.factoryCode))
                elif isinstance(value, arcpy.Multipoint):
                    self.set_value( field_name,  MultiPoint(value,value.spatialReference.factoryCode))

                elif isinstance(value, arcpy.Polyline):
                    self.set_value( field_name,  Polyline(value,value.spatialReference.factoryCode))

                elif isinstance(value, arcpy.Polygon):
                    self.set_value( field_name, Polygon(value,value.spatialReference.factoryCode))

        else:
            return False
        return True
    #----------------------------------------------------------------------
    def get_value(self, field_name):
        """ returns a value for a given field name """
        if field_name in self.fields:
            return self._dict['attributes'][field_name]
        elif field_name.upper() in ['SHAPE', 'SHAPE@', "GEOMETRY"]:
            return self._dict['geometry']
        return None
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """returns the feature as a dictionary"""
        feat_dict = {}
        if self._geom is not None:
            if self._dict.has_key('feature'):
                feat_dict['geometry'] =  self._dict['feature']['geometry']
            elif self._dict.has_key('geometry'):
                feat_dict['geometry'] =  self._dict['geometry']
        if self._dict.has_key("feature"):
            feat_dict['attributes'] = self._dict['feature']['attributes']
        else:
            feat_dict['attributes'] = self._dict['attributes']
        return self._dict
    #----------------------------------------------------------------------
    @property
    def asRow(self):
        """ converts a feature to a list for insertion into an insert cursor
            Output:
               [row items], [field names]
               returns a list of fields and the row object
        """
        fields = self.fields
        row = [""] * len(fields)
        for k,v in self._attributes.items():
            row[fields.index(k)] = v
            del v
            del k
        if self.geometry is not None:
            row.append(self.geometry)
            fields.append("SHAPE@")
        return row, fields
    #----------------------------------------------------------------------
    @property
    def geometry(self):
        """returns the feature geometry"""
        if arcpyFound:
            if not self._wkid is None:
                sr = arcpy.SpatialReference(self._wkid)
            else:
                sr = None
            if self._geom is None:
                if self._dict.has_key('feature'):
                    self._geom = arcpy.AsShape(self._dict['feature']['geometry'], esri_json=True)
                elif self._dict.has_key('geometry'):
                    self._geom = arcpy.AsShape(self._dict['geometry'], esri_json=True)
            return self._geom
        return None
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """ returns a list of feature fields """
        if self._dict.has_key("feature"):
            self._attributes = self._dict['feature']['attributes']
        else:
            self._attributes = self._dict['attributes']
        return self._attributes.keys()
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """ returns the feature's geometry type """
        if self._geomType is None:
            if self.geometry is not None:
                self._geomType = self.geometry.type
            else:
                self._geomType = "Table"
        return self._geomType
    @staticmethod
    def fc_to_features(dataset):
        """
           converts a dataset to a list of feature objects
           Input:
              dataset - path to table or feature class
           Output:
              list of feature objects
        """
        if arcpyFound:
            desc = arcpy.Describe(dataset)
            fields = [field.name for field in arcpy.ListFields(dataset) if field.type not in ['Geometry']]
            date_fields = [field.name for field in arcpy.ListFields(dataset) if field.type =='Date']
            non_geom_fields = copy.deepcopy(fields)
            features = []
            if hasattr(desc, "shapeFieldName"):
                fields.append("SHAPE@JSON")
            del desc
            with arcpy.da.SearchCursor(dataset, fields) as rows:
                for row in rows:
                    row = list(row)
                    for df in date_fields:
                        if row[fields.index(df)] != None:
                            row[fields.index(df)] = int((_date_handler(row[fields.index(df)])))
                    template = {
                        "attributes" : dict(zip(non_geom_fields, row))
                    }
                    if "SHAPE@JSON" in fields:
                        template['geometry'] = \
                            json.loads(row[fields.index("SHAPE@JSON")])

                    features.append(
                        Feature(json_string=_unicode_convert(template))
                    )
                    del row
            return features
        return None
    #----------------------------------------------------------------------
    def __str__(self):
        """"""
        return json.dumps(self.asDictionary)

########################################################################
class MosaicRuleObject(object):
    """
    The image service uses a mosaic rule to mosaick multiple rasters on the
    fly. The mosaic rule parameter is used by many image service operations,
    for example, export image and identify operations.
    """
    __allowedMosaicMethods = [
        "esriMosaicNone",
        "esriMosaicCenter",
        "esriMosaicNadir",
        "esriMosaicViewpoint",
        "esriMosaicAttribute",
        "esriMosaicLockRaster",
        "esriMosaicNorthwest",
        "esriMosaicSeamline"
    ]
    __allowedMosaicOps = [
        "MT_FIRST",
        "MT_LAST",
        "MT_MIN",
        "MT_MAX",
        "MT_MEAN",
        "MT_BLEND",
        "MT_SUM"
    ]
    _mosaicMethod = None
    _where = None
    _sortField = None
    _sortValue = None
    _ascending = None
    _lockRasterIds = None
    _viewpoint = None
    _fids = None
    _mosaicOperation = None
    _itemRenderingRule = None
    #----------------------------------------------------------------------
    def __init__(self,
                 mosaicMethod,
                 where="",
                 sortField="",
                 sortValue="",
                 ascending=True,
                 lockRasterIds=[],
                 viewpoint=None,
                 fids=[],
                 mosaicOperation=None,
                 itemRenderingRule=""):
        """Constructor"""
        if mosaicMethod in self.__allowedMosaicMethods:
            self._mosaicMethod = mosaicMethod
        else:
            raise AttributeError("Invalid mosaic method.")
        self._where = where
        self._sortField = sortField
        self._sortValue = sortValue
        self._ascending = ascending
        self._localRasterIds = lockRasterIds
        self._itemRenderingRule = itemRenderingRule
        if isinstance(viewpoint, Point):
            self._viewpoint = viewpoint
        self._fids = fids
        if mosaicOperation is not None and \
           mosaicOperation in self.__allowedMosaicOps:
            self._mosaicOperation = mosaicOperation

    #----------------------------------------------------------------------
    @property
    def where(self):
        """
        Use where clause to define a subset of rasters used in the mosaic,
        be aware that the rasters may not be visible at all scales
        """
        return self._where
    #----------------------------------------------------------------------
    @where.setter
    def where(self, value):
        """
        Use where clause to define a subset of rasters used in the mosaic,
        be aware that the rasters may not be visible at all scales
        """
        if value != self._where:
            self._where = value
    #----------------------------------------------------------------------
    @property
    def mosaicMethod(self):
        """
        get/set the mosaic method
        """
        return self._mosaicMethod
    #----------------------------------------------------------------------
    @mosaicMethod.setter
    def mosaicMethod(self, value):
        """
        get/set the mosaic method
        """
        if value in self.__allowedMosaicMethods and \
           self._mosaicMethod != value:
            self._mosaicMethod = value
    #----------------------------------------------------------------------
    @property
    def sortField(self):
        """"""
        return self._sortField
    #----------------------------------------------------------------------
    @sortField.setter
    def sortField(self, value):
        """"""
        if self._sortField != value:
            self._sortField = value
    #----------------------------------------------------------------------
    @property
    def sortValue(self):
        """"""
        return self._sortValue
    #----------------------------------------------------------------------
    @sortValue.setter
    def sortValue(self, value):
        """"""
        if self._sortValue != value:
            self._sortValue = value

    #----------------------------------------------------------------------
    @property
    def ascending(self):
        """"""
        return self._ascending
    #----------------------------------------------------------------------
    @ascending.setter
    def ascending(self, value):
        """"""
        if isinstance(value, bool):
            self._ascending = value
    #----------------------------------------------------------------------
    @property
    def lockRasterIds(self):
        """"""
        return self._lockRasterIds
    #----------------------------------------------------------------------
    @lockRasterIds.setter
    def lockRasterIds(self, value):
        """"""
        if isinstance(self._lockRasterIds, list):
            self._lockRasterIds = value

    #----------------------------------------------------------------------
    @property
    def viewpoint(self):
        """"""
        return self._viewpoint
    #----------------------------------------------------------------------
    @viewpoint.setter
    def viewpoint(self, value):
        """"""
        if isinstance(value, Point):
            self._viewpoint = value
    #----------------------------------------------------------------------
    @property
    def fids(self):
        """"""
        return self._fids
    #----------------------------------------------------------------------
    @fids.setter
    def fids(self, value):
        """"""
        self._fids = value
    #----------------------------------------------------------------------
    @property
    def mosaicOperation(self):
        """"""
        return self._mosaicOperation
    #----------------------------------------------------------------------
    @mosaicOperation.setter
    def mosaicOperation(self, value):
        """"""
        if value in self.__allowedMosaicOps and \
           self._mosaicOperation != value:
            self._mosaicOperation = value
    #----------------------------------------------------------------------
    @property
    def itemRenderingRule(self):
        """"""
        return self._itemRenderingRule
    #----------------------------------------------------------------------
    @itemRenderingRule.setter
    def itemRenderingRule(self, value):
        """"""
        if self._itemRenderingRule != value:
            self._itemRenderingRule = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """
        gets the mosaic rule object as a dictionary
        """
        if self.mosaicMethod == "esriMosaicNone" or\
           self.mosaicMethod == "esriMosaicCenter" or \
           self.mosaicMethod == "esriMosaicNorthwest" or \
           self.mosaicMethod == "esriMosaicNadir":
            return {
                "mosaicMethod" : "esriMosaicNone",
                "where" : self._where,
                "ascending" : self._ascending,
                "fids" : self.fids,
                "mosaicOperation" : self._mosaicOperation
            }
        elif self.mosaicMethod == "esriMosaicViewpoint":
            return {
                "mosaicMethod" : "esriMosaicViewpoint",
                "viewpoint" : self._viewpoint.asDictionary,
                "where" : self._where,
                "ascending" : self._ascending,
                "fids" : self._fids,
                "mosaicOperation" : self._mosaicOperation
            }
        elif self.mosaicMethod == "esriMosaicAttribute":
            return {
                "mosaicMethod" : "esriMosaicAttribute",
                "sortField" : self._sortField,
                "sortValue" : self._sortValue,
                "ascending" : self._ascending,
                "where" : self._where,
                "fids" : self._fids,
                "mosaicOperation" : self._mosaicOperation
            }
        elif self.mosaicMethod == "esriMosaicLockRaster":
            return {
                "mosaicMethod" : "esriMosaicLockRaster",
                "lockRasterIds" : self._localRasterIds,
                "where" : self._where,
                "ascending" : self._ascending,
                "fids" : self._fids,
                "mosaicOperation" : self._mosaicOperation
            }
        elif self.mosaicMethod == "esriMosaicSeamline":
            return {
                "mosaicMethod" : "esriMosaicSeamline",
                "where" : self._where,
                "fids" : self._fids,
                "mosaicOperation" : self._mosaicOperation
            }
        else:
            raise AttributeError("Invalid Mosaic Method")
########################################################################
class FeatureSet(object):
    """
    This featureSet contains Feature objects, including the values for the
    fields requested by the user. For layers, if you request geometry
    information, the geometry of each feature is also returned in the
    featureSet. For tables, the featureSet does not include geometries.
    If a spatialReference is not specified at the featureSet level, the
    featureSet will assume the spatialReference of its first feature. If
    the spatialReference of the first feature is also not specified, the
    spatial reference will be UnknownCoordinateSystem.
    """
    _fields = None
    _features = None
    _hasZ = None
    _hasM = None
    _geometryType = None
    _spatialReference = None
    _objectIdFieldName = None
    _globalIdFieldName = None
    _displayFieldName = None
    _allowedGeomTypes = ["esriGeometryPoint","esriGeometryMultipoint","esriGeometryPolyline",
                         "esriGeometryPolygon","esriGeometryEnvelope"]
    #----------------------------------------------------------------------
    def __init__(self,
                 fields,
                 features,
                 hasZ=False,
                 hasM=False,
                 geometryType=None,
                 spatialReference=None,
                 displayFieldName=None,
                 objectIdFieldName=None,
                 globalIdFieldName=None):
        """Constructor"""
        self._fields = fields
        self._features = features
        self._hasZ = hasZ
        self._hasM = hasM
        self._geometryType = geometryType
        self._spatialReference = spatialReference
        self._displayFieldName = displayFieldName
        self._objectIdFieldName = objectIdFieldName
        self._globalIdFieldName = globalIdFieldName
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns object as dictionary"""
        return {
            "objectIdFieldName" : self._objectIdFieldName,
            "displayFieldName" : self._displayFieldName,
            "globalIdFieldName" : self._globalIdFieldName,
            "geometryType" : self._geometryType,
            "spatialReference" : self._spatialReference,
            "hasZ" : self._hasZ,
            "hasM" : self._hasM,
            "fields" : self._fields,
            "features" : [f.asDictionary for f in self._features]
        }
    #----------------------------------------------------------------------
    @property
    def toJSON(self):
        """converts the object to JSON"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    def __iter__(self):
        """featureset iterator on features in feature set"""
        for feature in self._features:
            yield feature
    #----------------------------------------------------------------------
    def __len__(self):
        """returns the length of features in feature set"""
        return len(self._features)
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(jsonValue):
        """returns a featureset from a JSON string"""
        jd = json.loads(jsonValue)
        features = []
        if jd.has_key('fields'):
            fields = jd['fields']
        else:
            fields = {'fields':[]}
        for feat in jd['features']:
            wkid = None
            if 'spatialReference' in jd and 'latestWkid' in jd['spatialReference']:
                wkid = jd['spatialReference']['latestWkid']
            features.append(Feature(json_string=feat, wkid=wkid))
        return FeatureSet(fields,
                          features,
                          hasZ=jd['hasZ'] if 'hasZ' in jd else False,
                          hasM=jd['hasM'] if 'hasM' in jd else False,
                          geometryType=jd['geometryType'] if 'geometryType' in jd else None,
                          objectIdFieldName=jd['objectIdFieldName'] if 'objectIdFieldName' in jd else None,
                          globalIdFieldName=jd['globalIdFieldName'] if 'globalIdFieldName' in jd else None,
                          displayFieldName=jd['displayFieldName'] if 'displayFieldName' in jd else None,
                          spatialReference=jd['spatialReference'] if 'spatialReference' in jd else None)
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """gets the featureset's fields"""
        return self._fields
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """gets the featureset's spatial reference"""
        return self._spatialReference
    #----------------------------------------------------------------------
    @spatialReference.setter
    def spatialReference(self, value):
        """sets the featureset's spatial reference"""
        if isinstance(value, SpatialReference):
            self._spatialReference = value
        elif isinstance(value, int):
            self._spatialReference = SpatialReference(wkid=value)
        elif isinstance(value, str) and \
             str(value).isdigit():
            self._spatialReference = SpatialReference(wkid=int(value))
    #----------------------------------------------------------------------
    @property
    def hasZ(self):
        """gets/sets the Z-property"""
        return self._hasZ
    #----------------------------------------------------------------------
    @hasZ.setter
    def hasZ(self, value):
        """gets/sets the Z-property"""
        if isinstance(value, bool):
            self._hasZ = value
    #----------------------------------------------------------------------
    @property
    def hasM(self):
        """gets/set the M-property"""
        return self._hasM
    #----------------------------------------------------------------------
    @hasM.setter
    def hasM(self, value):
        """gets/set the M-property"""
        if isinstance(value, bool):
            self._hasM = value
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """gets/sets the geometry Type"""
        return self._geometryType
    #----------------------------------------------------------------------
    @geometryType.setter
    def geometryType(self, value):
        """gets/sets the geometry Type"""
        if value in self._allowedGeomTypes:
            self._geometryType = value
    #----------------------------------------------------------------------
    @property
    def objectIdFieldName(self):
        """gets/sets the object id field"""
        return self._objectIdFieldName
    #----------------------------------------------------------------------
    @objectIdFieldName.setter
    def objectIdFieldName(self, value):
        """gets/sets the object id field"""
        self._objectIdFieldName = value
    #----------------------------------------------------------------------
    @property
    def globalIdFieldName(self):
        """gets/sets the globalIdFieldName"""
        return self._globalIdFieldName
    #----------------------------------------------------------------------
    @globalIdFieldName.setter
    def globalIdFieldName(self, value):
        """gets/sets the globalIdFieldName"""
        self._globalIdFieldName = value
    #----------------------------------------------------------------------
    @property
    def displayFieldName(self):
        """gets/sets the displayFieldName"""
        return self._displayFieldName
    #----------------------------------------------------------------------
    @displayFieldName.setter
    def displayFieldName(self, value):
        """gets/sets the displayFieldName"""
        self._displayFieldName = value
    #----------------------------------------------------------------------
    def save(self, saveLocation, outName):
        """
        Saves a featureset object to a feature class
        Input:
           saveLocation - output location of the data
           outName - name of the table the data will be saved to
        """
        tempDir =  tempfile.gettempdir()
        tempFile = os.path.join(tempDir, "%s.json" % uuid.uuid4().get_hex())
        with open(tempFile, 'wb') as writer:
            writer.write(str(self))
            writer.flush()
            writer.close()
        del writer
        res = json_to_featureclass(json_file=tempFile,
                                   out_fc=os.path.join(saveLocation, outName))
        os.remove(tempFile)
        return res
    #----------------------------------------------------------------------
    @property
    def features(self):
        """gets the features in the FeatureSet"""
        return self._features

