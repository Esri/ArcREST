import json
import arcpy
import time
import copy
import datetime

from geometry import Point, MultiPoint, Polyline, Polygon
from base import Geometry, BaseDefinition, BaseDomain
#----------------------------------------------------------------------
def featureclassToFeatureSet(fc_path):
    """ converts a feature class to a feature set """
    fs = arcpy.FeatureSet()
    fs.load(fc_path)
    return fs
#----------------------------------------------------------------------
def tableToRecordSet(table_path):
    """ converts a table to a recordset object """
    rs = arcpy.RecordSet()
    rs.load(table_path)
    return rs
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
            if not value is None:
                self._dict['attributes'][field_name] = _unicode_convert(value)
                self._json = json.dumps(self._dict, default=_date_handler)
            else:
                pass
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
            elif isinstance(value, arcpy.Geometry):
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
                    row[fields.index(df)] = int(json.dumps(_date_handler(row[fields.index(df)])))
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
########################################################################
class Format(object):
    """
       The format object can be used with numerical or date fields to
       provide more detail about how values should be displayed in web map
       pop-up windows.
    """
    _places = None
    _dateFormat = None
    _digitalSeparator = None
    #----------------------------------------------------------------------
    def __init__(self, dateFormat=None,
                 digitsSeparator=False,
                 places=None):
        """Constructor"""
        self._dateFormat = dateFormat
        self._digitalSeparator = digitsSeparator
        self._places = places
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        return json.dumps(self.asDictionary)

    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        template = {}
        if self._dateFormat is not None:
            template['dateFormat'] = self._dateFormat
        if self._digitalSeparator is not None:
            template['digitalSeparator'] = self._digitalSeparator
        if self._places is not None:
            template['places'] = self._places
        return template
########################################################################
class FieldInfo(object):
    """
       Defines how a field in the dataset participates (or does not
       participate) in a pop-up window.
    """
    _fieldName = None
    _label = None
    _isEditable = None
    _tooltip = None
    _visible = None
    _stringFieldOption = None
    _format = None
    #----------------------------------------------------------------------
    def __init__(self, fieldName, label, isEditable=True,
                 tooltip="", visible=True, stringFieldOption="",
                 format=None):
        """Constructor"""
        self._fieldName = fieldName
        self._label = label
        self._isEditable = isEditable
        self._tooltip = tooltip
        self._visible = visible
        self._stringFieldOption = stringFieldOption
        if isinstance(format, Format):
            self._format = format
    def __str__(self):
        """ object as string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        template = {
            "fieldName" : self._fieldName,
            "label" : self._label,
            "isEditable" : self._isEditable,
            "tooltip" : self._tooltip,
            "visible" : self._visible
        }
        if self._format is not None:
            template['format'] = self._format.asDictionary
        return template
########################################################################
class Field(object):
    """
       Contains information about an attribute field. This field can come
       from a feature collection or a single layer in a map service. Used
       in layerDefinition.
    """
    _name = None
    _alias = None
    _type = None
    _length = None
    _editable = None
    _nullable = None
    _domain = None
    #----------------------------------------------------------------------
    def __init__(self, name, type,
                 alias="", length=None,
                 editable=True, nullable=True,
                 domain=None):
        """Constructor"""
        self._name = name
        self._type = type
        self._alias = alias
        self._length = length
        self._editable = editable
        self._nullable = nullable
        self._domain = domain
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ returns the name """
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """ sets the name field """
        self._name = value
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ gets the field type """
        return self._type
    #----------------------------------------------------------------------
    @type.setter
    def type(self, value):
        """ sets the field type """
        self._type = value
    #----------------------------------------------------------------------
    @property
    def alias(self):
        """ gets the field alias """
        return self._alias
    #----------------------------------------------------------------------
    @alias.setter
    def alias(self, value):
        """ sets the alias """
        self._alias = value
    #----------------------------------------------------------------------
    @property
    def length(self):
        """ gets the length value for field """
        return self._length
    #----------------------------------------------------------------------
    @length.setter
    def length(self, value):
        """ sets the length value """
        self._length = value
    #----------------------------------------------------------------------
    @property
    def editable(self):
        """ gets the editable value """
        return self._editable
    #----------------------------------------------------------------------
    @editable.setter
    def editable(self, value):
        """ sets the editable value """
        self._editable = value
    #----------------------------------------------------------------------
    @property
    def nullable(self):
        """ gets the nullable value """
        return self._nullable
    #----------------------------------------------------------------------
    @nullable.setter
    def nullable(self, value):
        """ sets the nullable value """
        self._nullable = value
    #----------------------------------------------------------------------
    @property
    def domain(self):
        """gets the domain value"""
        return self._domain
    #----------------------------------------------------------------------
    @domain.setter
    def domain(self, value):
        """ sets the domain """
        if isinstance(value, BaseDomain):
            self._domain = value

########################################################################
class DrawningInfo(BaseDefinition):
    """
       The drawingInfo object contains drawing information for a feature
       collection or a single layer in a map service. This object is used
       in layerDefinition.
    """
    _renderer = None
    _fixedSymbols = None
    #----------------------------------------------------------------------
    def __init__(self, renderer, fixedSymbols=False):
        """Constructor"""
        self._renderer = renderer
        self._fixedSymbols = fixedSymbols
    def __str__(self):
        """ returns object as string """
        return json.dumps(self.asDictionary)
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        return {
            "renderer" : self._renderer.asDictionary,
            "fixedSymbols" : self._fixedSymbols
        }
########################################################################
class Template(object):
    """
       Templates describe features that can be created in a layer.
       Templates are used with map notes, other feature collections, and
       editable web-based CSV layers. They are not used with ArcGIS feature
       services, which already have feature templates defined in the
       service.
       Templates are defined as properties of the layer definition when
       there are no types defined; otherwise, templates are defined as
       properties of the types.
    """
    _name = None
    _description = None
    _drawingTool = None
    _protoType = None

    #----------------------------------------------------------------------
    def __init__(self, name, description, drawingTool=None, protoType=None):
        """Constructor"""
        self._name = name
        self._description = description
        self._drawingTool = drawingTool
        self._protoType = protoType
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a dictionary """
        template = {
            "name" : self._name,
            "description" : self._description
        }
        if self._protoType is not None:
            template['protoType'] = self._protoType
        if self._drawingTool is not None:
            template['drawingTool'] = self._drawingTool
        return template
    def __str__(self):
        """ returns object as a string """
        return json.dumps(self.asDictionary)
########################################################################
class Type(object):
    """
       Types contain information about the combinations of attributes
       allowed for features in the dataset. Each feature in the dataset can
       have a type, indicated in its typeIdField, which is used in
       layerDefinition.
    """
    _domains = {}
    _id = None
    _name = None
    _templates = []
    #----------------------------------------------------------------------
    def __init__(self, id, name):
        """Constructor"""
        self._id = id
        self._name = name
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        template = {
            "id" : self._id,
            "name" : self._name,
            "domains" : self._domains,
            "templates" : self._templates
        }
        return template
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as dictionary """
        return json.dumps(self.asDictionary)

    #----------------------------------------------------------------------
    def addTemplate(self, template):
        """ adds a template to the Type """
        if isinstance(template, Template):
            self._templates.append(
                template.asDictionary
            )
    #----------------------------------------------------------------------
    def removeAllTemplates(self):
        """ clears the templates """
        self._templates = []
    #----------------------------------------------------------------------
    def removeTemplate(self, index):
        """ removes a template from the template collection """
        if index <= len(self._templates) - 1:
            self._templates.remove(self._templates[index])
    #----------------------------------------------------------------------
    @property
    def templates(self):
        """ gets the templates """
        return self._templates
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ gets the names """
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """ sets the name """
        self._name = value
    #----------------------------------------------------------------------
    @property
    def id(self):
        """ gets the id """
        return self._id
    #----------------------------------------------------------------------
    @id.setter
    def id(self, value):
        """ sets the id value """
        self._id = value
    #----------------------------------------------------------------------
    def addDomain(self, domainField, domainObject):
        """"""
        if isinstance(domainObject, BaseDomain) == False:
            return
        if self._domains is None:
            self._domains = {}
        self._domains[domainField] = domainObject.asDictionary
    #----------------------------------------------------------------------
    def removeDomain(self, domainField):
        """ removes a domain from the Type """
        if domainField in self._domains:
            return self._domains.pop(domainField, None)
########################################################################
class LocationInfo(object):
    """
       The locationInfo object defines how location information will be
       retrieved from a CSV file referenced through the web.
    """
    _lat = None
    _long = None
    _type = "coordinates"

    #----------------------------------------------------------------------
    def __init__(self, latitudeFieldName, longitudeFieldName):
        """Constructor"""
        self._lat = latitudeFieldName
        self._long = longitudeFieldName
    #----------------------------------------------------------------------
    def __str__(self):
        """ converts object to string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ converts object to dictionary """
        return {
            "latitudeFieldName" : self._lat,
            "locationType" : self._type,
            "longitudeFieldName" : self._long
        }
########################################################################
class MediaInfo(object):
    """
       Defines an image or a chart to be displayed in a pop-up window.
    """
    _type = None
    _value = None
    _caption = None
    _title = None
    #----------------------------------------------------------------------
    def __init__(self, caption, title, type, value):
        """Constructor"""
        self._type = type
        self._caption = caption
        self._title = title
        if isinstance(value, Value):
            self._value = value.asDictionary
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        return {
              "title": self._title,
              "type": self._type,
              "caption": "{%s}" % self._caption,
              "value": self._value
            }
########################################################################
class Value(object):
    """
       The value object contains information for pop-up windows about how
       images should be retrieved or charts constructed.
    """
    _fields = None
    _linkURL = None
    _normalizeField = None
    _sourceURL = None
    #----------------------------------------------------------------------
    def __init__(self, fields=None, linkURL=None,
                 normalizeField=None, sourceURL=None):
        """Constructor"""
        self._fields = fields
        self._linkURL = linkURL
        self._normalizeField = normalizeField
        self._sourceURL = sourceURL
    def __str__(self):
        """object as string"""
        return json.dumps(self.asDictionary)
    @property
    def asDictionary(self):
        """ object as dictionary """
        template = {}
        if self._fields is not None:
            template['fields'] = self._fields
        if self._linkURL is not None:
            template['linkURL'] = self._linkURL
        if self._normalizeField is not None:
            template['normalizeField'] = self._normalizeField
        if self._sourceURL is not None:
            template['sourceURL'] = self._sourceURL
        return template
########################################################################
class LayerDefinition(BaseDefinition):
    """
       The layerDefinition object defines the attribute schema and drawing
       information for a layer drawn using client-side graphics. This can
       include a feature collection, a CSV file referenced through the web,
       or a single layer in an ArcGIS map service.
    """

    #----------------------------------------------------------------------
    def __init__(self,
                 name,
                 drawingInfo,
                 type,#Feature Layer or a Table.
                 fields=None,
                 objectIdField=None,
                 displayField=None,
                 geometryType=None,
                 hasAttachments=False,
                 minScale=0,
                 maxScale=0,
                 templates=None,
                 typeIdField=None,
                 types=None,
                 definitionExpression=""
                 ):
        """Constructor"""
        self._name = name
        self._objectIdField = objectIdField
        self._displayField = displayField
        self._drawningInfo = drawingInfo
        self._fields = fields
        self._geometryType = geometryType
        self._hasAttachments = hasAttachments
        self._minScale = minScale
        self._maxScale = maxScale
        self._templates = templates
        self._type = self._type
        self._typeIdField = typeIdField
        self._types = types
        self._definitionExpression = definitionExpression
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        template = {
            "drawingInfo" : self._drawningInfo.asDictionary,
            "name" : self._name,
            "minScale" : self._minScale,
            "maxScale" : self._maxScale
        }
        if self._objectIdField is not None:
            template['objectIdField'] = self._objectIdField
        if self._fields is not None:
            template['fields'] = self._fields
        if self._definitionExpression is not None:
            template['definitionExpression'] = self._definitionExpression
        if self._displayField is not None:
            template['displayField'] = self._displayField
        if self._geometryType is not None:
            template['geometryType'] = self._geometryType
        if self._type is not None:
            template['type'] = self._type
        if self._hasAttachments is not None:
            template['hasAttachments'] = self._hasAttachments
        if self._templates is not None:
            template['templates'] = self._templates
        if self._types is not None:
            template['types'] = self._types
        return template
########################################################################
class PopupInfo(object):
    """
       Defines the look and feel of pop-up windows when users click or
       query a feature.
    """
    _title = None
    _description = None
    _showAttachments = None
    _mediaInfos = []
    _fieldInfos = []
    #----------------------------------------------------------------------
    def __init__(self, title, description, showAttachments=False):
        """Constructor"""
        self._title = title
        self._description = description
        self._showAttachments = showAttachments
    #----------------------------------------------------------------------
    def addMediaInfo(self, mediaInfo):
        """ adds a media info object to PopupInfo Object """
        if isinstance(mediaInfo, MediaInfo):
            self._mediaInfos.append(
                mediaInfo.asDictionary
            )
            return True
        return False
    #----------------------------------------------------------------------
    def removeMediaInfo(self, index):
        """ removes a mediainfo object from the container """
        if index <= len(self._mediaInfos) -1:
            self._mediaInfos.remove(self._mediaInfos[index])
            return True
        return False
    #----------------------------------------------------------------------
    @property
    def mediaInfos(self):
        """ returns all the media ifor objects """
        return self._mediaInfos
    #----------------------------------------------------------------------
    def addFieldInfo(self, fieldInfo):
        """ adds a field info object to the holder """
        if isinstance(fieldInfo, FieldInfo):
            self._fieldInfos.append(
                fieldInfo.asDictionary
            )
            return True
        return False
    #----------------------------------------------------------------------
    def removeFieldInfo(self, index):
        """ removes a value from the field info """
        if index <= len(self._fieldInfos) - 1:
            self._fieldInfos.remove(self._fieldInfos[index])
            return True
        return False
    #----------------------------------------------------------------------
    @property
    def fieldInfos(self):
        """ gets the field info objects """
        return self._fieldInfos
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the object as a string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a dictionary """
        template = {
            "title" : self._title,
            "fieldInfos" : self._fieldInfos,
            "description" : self._description,
            "showAttachments" : self._showAttachments,
            "mediaInfos" : self._mediaInfos
        }












