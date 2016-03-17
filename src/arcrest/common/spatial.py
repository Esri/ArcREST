"""
Contains all the spatial functions
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import os, datetime
try:
    import arcpy
    from arcpy import env
    arcpyFound = True
except:
    arcpyFound = False
#----------------------------------------------------------------------
def create_feature_layer(ds, sql, name="layer"):
    """ creates a feature layer object """
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    result = arcpy.MakeFeatureLayer_management(in_features=ds,
                                               out_layer=name,
                                               where_clause=sql)
    return result[0]
#----------------------------------------------------------------------
def featureclass_to_json(fc):
    """converts a feature class to JSON"""
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    desc = arcpy.Describe(fc)
    if desc.dataType == "Table" or desc.dataType == "TableView":
        return recordset_to_json(table=fc)
    else:
        return arcpy.FeatureSet(fc).JSON
#----------------------------------------------------------------------
def recordset_to_json(table):
    """ converts the table to JSON """
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    return arcpy.RecordSet(table).JSON
#----------------------------------------------------------------------
def json_to_featureclass(json_file, out_fc):
    """ converts a json file (.json) to a feature class """
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    return arcpy.JSONToFeatures_conversion(in_json_file=json_file,
                                    out_features=out_fc)[0]
#----------------------------------------------------------------------
def table_to_json(table):
    """ returns a table as JSON """
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    return arcpy.RecordSet(table).JSON
#----------------------------------------------------------------------
def get_attachment_data(attachmentTable, sql,
                        nameField="ATT_NAME", blobField="DATA",
                        contentTypeField="CONTENT_TYPE",
                        rel_object_field="REL_OBJECTID"):
    """ gets all the data to pass to a feature service """
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
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
def get_records_with_attachments(attachment_table, rel_object_field="REL_OBJECTID"):
    """"""
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    OIDs = []
    with arcpy.da.SearchCursor(attachment_table,
                               [rel_object_field]) as rows:
        for row in rows:
            if not str(row[0]) in OIDs:
                OIDs.append("%s" % str(row[0]))
            del row
    del rows
    return OIDs
#----------------------------------------------------------------------
def get_OID_field(fs):
    """returns a featureset's object id field"""
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    desc = arcpy.Describe(fs)
    if desc.hasOID:
        return desc.OIDFieldName
    return None
#----------------------------------------------------------------------
def merge_feature_class(merges, out_fc, cleanUp=True):
    """ merges featureclass into a single feature class """
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
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
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    return arcpy.env.scratchFolder
#----------------------------------------------------------------------
def scratchGDB():
    """ returns the arcpy scratch file geodatabase """
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    return env.scratchGDB
#----------------------------------------------------------------------
def getDateFields(fc):
    """
       Returns a list of fields that are of type DATE
       Input:
          fc - feature class or table path
       Output:
          List of date field names as strings
    """
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    return [field.name for field in arcpy.ListFields(fc, field_type="Date")]
#----------------------------------------------------------------------
def insert_rows(fc,
                features,
                fields,
                includeOIDField=False,
                oidField=None):
    """ inserts rows based on a list features object """
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
    icur = None
    if includeOIDField:
        arcpy.AddField_management(fc, "FSL_OID", "LONG")
        fields.append("FSL_OID")
    if len(features) > 0:
        fields.append("SHAPE@")
        workspace = os.path.dirname(fc)
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
    if arcpyFound == False:
        raise Exception("ArcPy is required to use this function")
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
#----------------------------------------------------------------------
def toDateTime(unix_timestamp):
    """converts a unix time stamp to a datetime object """
    unix_timestamp = unix_timestamp/1000
    return datetime.datetime.fromtimestamp(unix_timestamp)
#----------------------------------------------------------------------
def _unicode_convert(obj):
    """ converts unicode to anscii """
    if isinstance(obj, dict):
        return {_unicode_convert(key): \
                _unicode_convert(value) \
                for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_unicode_convert(element) for element in obj]
    elif isinstance(obj, unicode):
        return obj.encode('utf-8')
    else:
        return obj
