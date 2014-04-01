"""
   contains all the common JSON objects as defined
   at in the common object type in the ArcGIS REST
   API.
"""
import json
import arcpy

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