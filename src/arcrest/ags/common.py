"""
   contains all the common JSON objects as defined
   at in the common object type in the ArcGIS REST
   API.
"""
import arcpy
from geometry import *
import types
import os
import copy
import json
from base import Geometry
import datetime
import calendar
import time
from time import gmtime, strftime,mktime
import featureservice
import layer

def create_SpatialReference(sr):
    """ creates an arcpy.spatial reference object """
    return arcpy.SpatialReference(sr)

def _date_handler(obj):
    if isinstance(obj, datetime.datetime):
        return local_time_to_online(obj)
    elif isinstance(obj, (featureservice.FeatureService,
                          layer.FeatureLayer,
                          layer.TableLayer)):
        return dict(obj)
    else:
        return obj
def relative_path_to_absolute(path):
    if not os.path.isabs(path):
        sciptPath = os.getcwd()
        return os.path.join(sciptPath,path)
    else:
        return path

#----------------------------------------------------------------------
def get_attachment_data(attachmentTable, sql,
                        nameField="ATT_NAME", blobField="DATA",
                        contentTypeField="CONTENT_TYPE",
                        rel_object_field="REL_OBJECTID"):
    """ gets all the data to pass to a feature service """
    ret_rows = []
    with arcpy.da.SearchCursor(attachmentTable,
                               [nameField,
                                blobField,
                                contentTypeField,
                                rel_object_field],
                               where_clause=sql) as rows:
        for row in rows:
            temp_f = os.environ['temp'] + os.sep + row[0]
            writer = open(temp_f,'wb')
            writer.write(row[1])
            writer.flush()
            writer.close()
            del writer
            ret_rows.append({
                "name" : row[0],
                "blob" : temp_f,
                "content" : row[2],
                "rel_oid" : row[3]
            })
            del row
    return ret_rows


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
def create_feature_layer(ds, sql, name="layer"):
    """ creates a feature layer object """
    result = arcpy.MakeFeatureLayer_management(in_features=ds,
                                               out_layer=name,
                                               where_clause=sql)
    return result[0]
#----------------------------------------------------------------------
def get_records_with_attachments(attachment_table, rel_object_field="REL_OBJECTID"):
    """"""
    OIDs = []
    with arcpy.da.SearchCursor(attachment_table,
                               [rel_object_field]) as rows:
        for row in rows:
            if not row[0] in OIDs:
                OIDs.append("%s" % row[0])
            del row
    return OIDs
#----------------------------------------------------------------------
def get_OID_field(fs):
    """returns a featureset's object id field"""
    desc = arcpy.Describe(fs)
    if desc.hasOID:
        return desc.OIDFieldName
    return None
#----------------------------------------------------------------------
def featureclass_to_json(fc):
    """ converts a feature class to a json dictionary representation """
    featureSet = arcpy.FeatureSet(fc)# Load the feature layer into a feature set
    desc = arcpy.Describe(featureSet)# this will allow us to use the json property of the feature set
    return json.loads(desc.json)
#----------------------------------------------------------------------
def json_to_featureclass(json_file, out_fc):
    """ converts a json file (.json) to a feature class """
    return arcpy.JSONToFeatures_conversion(in_json_file=json_file,
                                    out_features=out_fc)[0]
#----------------------------------------------------------------------
def merge_feature_class(merges, out_fc, cleanUp=True):
    """ merges featureclass into a single feature class """
    if cleanUp == False:
        if len(merges) == 0:
            return None
        elif len(merges) == 1:
            desc = arcpy.Describe(merges[0])
            if hasattr(desc, 'shapeFieldName'):
                return arcpy.CopyFeatures_management(merges[0], out_fc)[0]
            else:
                return arcpy.CopyRows_management(merges[0], out_fc)[0]
        else:
            return arcpy.Merge_management(inputs=merges,
                                          output=out_fc)[0]
    else:
        if len(merges) == 0:
            return None
        elif len(merges) == 1:
            desc = arcpy.Describe(merges[0])
            if hasattr(desc, 'shapeFieldName'):
                merged = arcpy.CopyFeatures_management(merges[0], out_fc)[0]
            else:
                merged = arcpy.CopyRows_management(merges[0], out_fc)[0]
        else:
            merged = arcpy.Merge_management(inputs=merges,
                                        output=out_fc)[0]
        for m in merges:
            arcpy.Delete_management(m)
            del m
        return merged
#----------------------------------------------------------------------
def scratchFolder():
    """ returns the scratch foldre """
    return arcpy.env.scratchFolder
#----------------------------------------------------------------------
def scratchGDB():
    """ returns the arcpy scratch file geodatabase """
    return arcpy.env.scratchGDB
#----------------------------------------------------------------------
def getDateFields(fc):
    """
       Returns a list of fields that are of type DATE
       Input:
          fc - feature class or table path
       Output:
          List of date field names as strings
    """
    return [field.name for field in arcpy.ListFields(fc, field_type="Date")]
#----------------------------------------------------------------------
def toDateTime(unix_timestamp):
    """converts a unix time stamp to a datetime object """
    unix_timestamp = unix_timestamp/1000
    return datetime.datetime.fromtimestamp(unix_timestamp)
#----------------------------------------------------------------------
def insert_rows(fc,
                features,
                fields,
                includeOIDField=False,
                oidField=None):
    """ inserts rows based on a list features object """
    icur = None
    if includeOIDField:
        arcpy.AddField_management(fc, "FSL_OID", "LONG")
        fields.append("FSL_OID")
    if len(features) > 0:
        fields.append("SHAPE@")
        workspace = _unicode_convert(os.path.dirname(fc))
        with arcpy.da.Editor(workspace) as edit:
            date_fields = getDateFields(fc)
            icur = arcpy.da.InsertCursor(fc, fields)
            for feat in features:
                row = [""] * len(fields)
                drow = feat.asRow[0]
                dfields = feat.fields
                for field in fields:
                    if field in dfields or \
                       (includeOIDField and field == "FSL_OID"):
                        if field in date_fields:
                            row[fields.index(field)] = toDateTime(drow[dfields.index(field)])
                        elif field == "FSL_OID":
                            row[fields.index("FSL_OID")] = drow[dfields.index(oidField)]
                        else:
                            row[fields.index(field)] = drow[dfields.index(field)]
                    del field
                row[fields.index("SHAPE@")] = feat.geometry
                icur.insertRow(row)
                del row
                del drow
                del dfields
                del feat
            del features
            icur = None
            del icur
            del fields
        return fc
    else:
        return fc
#----------------------------------------------------------------------
def create_feature_class(out_path,
                         out_name,
                         geom_type,
                         wkid,
                         fields,
                         objectIdField):
    """ creates a feature class in a given gdb or folder """
    arcpy.env.overwriteOutput = True
    field_names = []
    fc =arcpy.CreateFeatureclass_management(out_path=out_path,
                                            out_name=out_name,
                                            geometry_type=lookUpGeometry(geom_type),
                                            spatial_reference=arcpy.SpatialReference(wkid))[0]
    for field in fields:
        if field['name'] != objectIdField:
            field_names.append(field['name'])
            arcpy.AddField_management(out_path + os.sep + out_name,
                                      field['name'],
                                      lookUpFieldType(field['type']))
    return fc, field_names
#----------------------------------------------------------------------
def lookUpGeometry(geom_type):
    """ converts ArcRest API geometry name to Python names
        Input:
           geom_type - string - name of geometry
        Output:
           name of python geometry type for create feature class function
    """
    if geom_type == "esriGeometryPoint":
        return "POINT"
    elif geom_type == "esriGeometryPolygon":
        return "POLYGON"
    elif geom_type == "esriGeometryLine":
        return "POLYLINE"
    else:
        return "POINT"
#----------------------------------------------------------------------
def lookUpFieldType(field_type):
    """ Converts the ArcGIS REST field types to Python Types
        Input:
           field_type - string - type of field as string
        Output:
           Python field type as string
    """
    if field_type == "esriFieldTypeDate":
        return "DATE"
    elif field_type == "esriFieldTypeInteger":
        return "LONG"
    elif field_type == "esriFieldTypeSmallInteger":
        return "SHORT"
    elif field_type == "esriFieldTypeDouble":
        return "DOUBLE"
    elif field_type == "esriFieldTypeString":
        return "TEXT"
    elif field_type == "esriFieldTypeBlob":
        return "BLOB"
    elif field_type == "esriFieldTypeSingle":
        return "FLOAT"
    elif field_type == "esriFieldTypeRaster":
        return "RASTER"
    elif field_type == "esriFieldTypeGUID":
        return "GUID"
    elif field_type == "esriFieldTypeGlobalID":
        return "TEXT"
    else:
        return "TEXT"

########################################################################
class Feature(object):
    """ returns a feature  """
    _geom = None
    _json = None
    _dict = None
    _geom = None
    _geomType = None
    _attributes = None
    #----------------------------------------------------------------------
    def __init__(self, json_string):
        """Constructor"""
        if type(json_string) is dict:
            self._json = json.dumps(json_string,
                                    default=_date_handler)
            self._dict = json_string
        elif type(json_string) is str:
            self._dict = json.loads(json_string)
            self._json = json_string
        else:
            raise TypeError("Invalid Input, only dictionary of string allowed")
    #----------------------------------------------------------------------
    def set_value(self, field_name, value):
        """ sets an attribute value for a given field name """
        if field_name in self.fields:
            self._dict['attributes'][field_name] = value
            self._json = json.dumps(self._dict, default=_date_handler)
        elif field_name.upper() in ['SHAPE', 'SHAPE@', "GEOMETRY"]:
            if isinstance(value, Geometry):
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
        for k,v in self._attributes.iteritems():
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
        if self._geom is None:
            if self._dict.has_key('feature'):
                self._geom = arcpy.AsShape(self._dict['feature']['geometry'], esri_json=True)
            elif self._dict.has_key('geometry'):
                self._geom = arcpy.AsShape(self._dict['geometry'], esri_json=True)
        return self._geom
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
        desc = arcpy.Describe(dataset)
        fields = [field.name for field in arcpy.ListFields(dataset) if field.type not in ['Geometry']]
        non_geom_fields = copy.deepcopy(fields)
        features = []
        if hasattr(desc, "shapeFieldName"):
            fields.append("SHAPE@JSON")
        del desc
        with arcpy.da.SearchCursor(dataset, fields) as rows:
            for row in rows:
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
#----------------------------------------------------------------------
def _unicode_convert(obj):
    """ converts unicode to anscii """
    if isinstance(obj, dict):
        return {_unicode_convert(key): \
                _unicode_convert(value) \
                for key, value in obj.iteritems()}
    elif isinstance(obj, list):
        return [_unicode_convert(element) for element in obj]
    elif isinstance(obj, unicode):
        return obj.encode('utf-8')
    else:
        return obj