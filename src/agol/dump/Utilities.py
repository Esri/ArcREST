import os
import urllib
import ConfigParser
import arcpy
import json
class FeatureServiceError(Exception):
    """ raised when feature service occurs """
    pass
class UtilitesError(Exception):
    """ raised when error occurs in utility module functions """
    pass
def getScratchFolder():
    """ returns the scratch folder for arcgis desktop/server """
    return arcpy.env.scratchFolder
def getScratchGDB():
    """ returns the scratch gdb used by arcgis desktop or server """
    return arcpy.env.scratchGDB
#----------------------------------------------------------------------
def trace(file_name):
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback
    import sys
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, file_name, synerror
#----------------------------------------------------------------------
def __unicode_convert(obj):
    """ Converts an object from a unicode to utf-8 string"""
    try:
        if isinstance(obj, dict):
            return {__unicode_convert(key): __unicode_convert(value) for key, value in obj.iteritems()}
        elif isinstance(obj, list):
            return [__unicode_convert(element) for element in obj]
        elif isinstance(obj, unicode):
            return obj.encode('utf-8')
        else:
            return obj
    except:
        line, filename, synerror = trace(__file__)
        raise UtilitesError({

            "function": "__unicode_convert",
            "line": line,
            "filename": __file__,
            "synerror": synerror,
                            }
                            )
#----------------------------------------------------------------------
def getToken(username=None, password=None, expiration=60, referer=None):
    """ Gets a token for arcgis.com """
    try:
        tokenUrl  = 'https://arcgis.com/sharing/rest/generateToken'
        query_dict = {'username': username,
                      'password': password,
                      'expiration': str(expiration),
                      'referer': referer,
                      'f': 'json'}

        query_string = urllib.urlencode(query_dict)
        token = json.loads(urllib.urlopen(tokenUrl + "?f=json", query_string).read())
        if "token" not in token:
            return None
        else:
            httpPrefix = "http://www.arcgis.com/sharing/rest"
            if token['ssl'] == True:
                httpPrefix = "https://www.arcgis.com/sharing/rest"
            return token['token'], httpPrefix
    except:
        line, filename, synerror = trace(__file__)
        raise UtilitesError({
                    "function": "getToken",
                    "line": line,
                    "filename": __file__,
                    "synerror": synerror,
                                    }
                                    )
#----------------------------------------------------------------------
def get_config_value(config_file, section, variable):
    """ extracts a config file value """
    try:
        parser = ConfigParser.SafeConfigParser()
        parser.read(config_file)
        return parser.get(section, variable)
    except:
        return None
#----------------------------------------------------------------------
def message(msg, level):
    """ Outputs messages to arcpy windows """
    if level == "ERROR":
        arcpy.AddError(msg)
    elif level == "WARNING":
        arcpy.AddWarning(msg)
    elif level == "INFO":
        arcpy.AddMessage(msg)
#----------------------------------------------------------------------
def featureclass_to_json(fc, sanitize=True):
    """ Converts a feature class of feature layer
        to json.
        Input:
           fc - string - path to feature class
        Output:
           JSON string
    """
    featureSet = arcpy.FeatureSet(fc)# Load the feature layer into a feature set
    desc = arcpy.Describe(featureSet)# this will allow us to use the json property of the feature set
    data = json.loads(desc.json)
    if sanitize:
        return __unicode_convert(data)
    return data
#----------------------------------------------------------------------
def __lookUpGeometry(geom_type):
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
def __lookUpFieldType(field_type):
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
def get_OID_field(fs):
    """returns a featureset's object id field"""
    desc = arcpy.Describe(fs)
    if desc.hasOID:
        return desc.OIDFieldName
    return None
#----------------------------------------------------------------------
def get_records_with_attachments(attachment_table, rel_object_field="REL_OBJECTID"):
    """"""
    OIDs = []
    with arcpy.da.SearchCursor(attachment_table, [rel_object_field]) as rows:
        for row in rows:
            if not row[0] in OIDs:
                OIDs.append("%s" % row[0])
            del row
    return OIDs
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
def create_feature_layer(ds, sql, name="layer"):
    """ creates a feature layer object """
    result = arcpy.MakeFeatureLayer_management(in_features=ds, 
                                               out_layer=name, 
                                               where_clause=sql)
    return result[0]
#----------------------------------------------------------------------
def delete_ds(ds):
    """deletes the dataset"""
    arcpy.Delete_management(ds)
    return True
    
#----------------------------------------------------------------------
def dictionary_to_feature_class(json_dict, out_fc):
    """ Converts a dictionary of features from a feature services
        to a local feature class
        Inputs:
           json_dict - dictionary - derived dictionary from feature service
           out_fc - string - full path of where the feature class will be
                             saved.
        Output:
           path of saved feature class as string
    """
    arcpy.env.overwriteOutput = True
    oid_fld = json_dict['objectIdFieldName']
    field_names = []
    geomType = json_dict['geometryType']
    sr = arcpy.SpatialReference(json_dict['spatialReference']['latestWkid'])
    arcpy.CreateFeatureclass_management(out_path=os.path.dirname(out_fc),
                                        out_name=os.path.basename(out_fc),
                                        geometry_type=__lookUpGeometry(geomType),
                                        spatial_reference=sr)
    for field in json_dict['fields']:
        if field['name'] != json_dict['objectIdFieldName']:
            field_names.append(field['name'])
            arcpy.AddField_management(out_fc,
                                      field['name'],
                                      __lookUpFieldType(field['type']))
    field_names.append("SHAPE@")
    icur = arcpy.da.InsertCursor(out_fc, field_names)
    for feature in json_dict['features']:
        template = feature['geometry']
        template['spatialReference'] = json_dict['spatialReference']['latestWkid']
        geom = arcpy.AsShape(json.dumps(template), True)
        row = [""] * len(field_names)
        for k, v in feature['attributes'].iteritems():
            if k != oid_fld:
                row[field_names.index(k)] = v
        row[field_names.index("SHAPE@")] = geom
        icur.insertRow(row)
        del row
        del geom
        del template
    del icur
    del field_names
    del oid_fld
    del sr
    return out_fc
#----------------------------------------------------------------------
def sync_to_featureclass(out_workspace, fc_name, fields, wkid,
                         geomType, features, objectIdField):
    """ converts the sync replication to a local feature class
        Inputs:
           out_workspace - string - geodatabase path of the save location
           fc_name - string - name of feature class
           fields - list of dictionaries obtained from feature service
           wkid - spatial reference entry from feature service
           geomType -string - feature service geometry type
           features - list - items to add to feature class
           objectIdField - string - nice of OID field
        Ouput:
           location of feature class as string.

    """
    arcpy.env.overwriteOutput = True
    field_names = ["SHAPE@"]
    sr = arcpy.SpatialReference(wkid['latestWkid'])
    out_fc = arcpy.CreateFeatureclass_management(out_path=out_workspace,
                                                 out_name=fc_name,
                                                 geometry_type=__lookUpGeometry(geomType),
                                                 spatial_reference=sr)[0]
    for field in fields:
        if field['name'] != objectIdField:
            field_names.append(field['name'])
            arcpy.AddField_management(out_fc,
                                      field['name'],
                                      __lookUpFieldType(field['type']))
    icur = arcpy.da.InsertCursor(out_fc, field_names)
    for feature in features:
        template = feature['geometry']
        template['spatialReference'] = wkid['latestWkid']
        geom = arcpy.AsShape(json.dumps(template), True)
        row = [""] * len(field_names)
        for k, v in feature['attributes'].iteritems():
            if k != objectIdField:
                row[field_names.index(k)] = v
        row[field_names.index("SHAPE@")] = geom
        icur.insertRow(row)
        del row
        del geom
        del template
    del icur
    del field_names
    return out_fc
def process_attachements(rows,
                         fields,
                         join_fc,
                         gdb,
                         table_name="attachments",
                         working_folder=arcpy.env.scratchFolder):
    """ creates and handles the attachments
        Inputs:
           rows - list - attachments rows to insert to table
           fields - list - fields for insert cursor
           join_fc - string - path of file geodatabase feature class
                              that will have attachments enabled.
           gdb - string - path to geodatabase
           table_name - string - name of attachments table
           working_folder - string - path to where attachments are stored.
        Output:
           boolean. True successful/False failed.
    """
    tbl = arcpy.CreateTable_management(out_path=gdb,
                                       out_name=table_name)[0]
    arcpy.AddField_management(tbl, "ParentID", "TEXT", field_length=1320)
    arcpy.AddField_management(tbl, "PATH", "TEXT", field_length=1320)
    icur = arcpy.da.InsertCursor(tbl, ['ParentID', "PATH"])
    for row in rows:
        icur.insertRow(__unicode_convert(row))
        del row
    del rows
    del icur
    arcpy.EnableAttachments_management(in_dataset=join_fc)
    arcpy.AddAttachments_management(in_dataset=join_fc,
                                    in_join_field="GlobalID",
                                    in_match_table=tbl,
                                    in_match_join_field="ParentID",
                                    in_match_path_field="PATH",
                                    in_working_folder=working_folder)
    return True