"""
   Contains all the geoprocessing objects.
"""
from __future__ import absolute_import
from __future__ import print_function
import json
########################################################################
class GPMultiValue(object):
    """
    The fully qualified data type for a GPMultiValue parameter is
    GPMultiValue:<memberDataType>, where memberDataType is one of the data
    types defined above (for example, GPMultiValue:GPString,
    GPMultiValue:GPLong, and so on).
    The parameter value for GPMultiValue data types is a JSON array. Each
    element in this array is of the data type as defined by the
    memberDataType suffix of the fully qualified GPMultiValue data type
    name.
    """
    _value = None
    _paramName = None
    _type = None
    #----------------------------------------------------------------------
    def __init__(self, gptype):
        """Constructor"""
        self._type = gptype
        self._dataType = "GPMultiValue:%s" % gptype
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        #if isinstance(value, bool):
        self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPMultiValue(gptype=j['dataType'])
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPRecordSet(object):
    """
    The parameter value for GPRecordSet is a JSON structure with the field
    features.
    The features field is an array of features. Each feature in turn
    contains an attributes field. The attributes field consists of
    key-value pairs where the key is a field name in the list of fields of
    the record set and the value is the value of the corresponding field.
    """
    _value = None
    _paramName = None
    _type = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPRecordSet"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        if isinstance(value, dict):
            self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPRecordSet()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPFeatureRecordSetLayer(object):
    """
    If the GP service is associated with a result map service, the default
    output for the GPFeatureRecordSetLayer parameter is a map image.
    However, you can explicitly request the feature data by using the
    returnType parameter in the URL and setting its value to data.
    If the GP service is not associated with a result map service or if the
    returnType parameter is set to the value data, the parameter value for
    GPFeatureRecordSetLayer is a JSON structure with the following
    properties:
        features-An array of features. Each feature is defined with the
         following properties:
          geometry-Points, lines, or polygons. The structure for the
           geometries is the same as the structure of the JSON geometry
           objects returned by the ArcGIS REST API.
        attributes-Key-value pairs, where the key is a field name in the
         list of fields of the record set and the value is the value of the
         corresponding field.
        spatialReference-The well known ID of a spatial reference.
        geometryType-The geometry type of the GPFeatureRecordsSetLayer.
        hasZ=true if the GPFeatureRecordSetLayer includes Z values.
        hasM=true if the GPFeatureRecordSetLayer includes M values.
        fields containing name,alias, and fieldType properties for the
        fields returned in the response.
    """
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPFeatureRecordSetLayer"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        if isinstance(value, dict):
            self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPFeatureRecordSetLayer()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPRasterDataLayer(object):
    """
    If the GP service is associated with a result map service, the default
    output for the GPRasterDataLayer parameter is a map image. However, you
    can explicitly request the raw raster data by using the returnType
    parameter in the URL and setting its value to data.
    If the GP service is not associated with a result map service, or if
    the returnType parameter is set to the value data, the parameter value
    for GPRasterDataLayer is a JSON structure with the following fields:
     url - A URL to the location of the raw raster data.
     format - A string representing the format of the raster.
    """
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPRasterDataLayer"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        if isinstance(value, dict):
            self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPRasterDataLayer()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v

########################################################################
class GPRasterData(object):
    """
    The parameter value for GPRasterData is a JSON structure with the
    following fields:
     url - A URL to the location of the raster data file.
     format - A string representing the format of the raster.
    """
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPRasterData"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        if isinstance(value, dict):
            self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPRasterData()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPDataFile(object):
    """
    The parameter value for GPDataFile is a JSON structure with a url
    field. The value of the url field is a URL to the location of the data
    file.
    """
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPDataFile"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        if isinstance(value, dict):
            self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPDataFile()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPLinearUnit(object):
    """
    The parameter value for GPLinearUnit is a JSON structure with the
    following fields:
     distance - A double value.
     units - A string whose values can be "esriMeters", "esriMiles", and so on.
    """
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPLinearUnit"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        if isinstance(value, dict):
            self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPLinearUnit()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPDate(object):
    """
    The value for GPDate data type is a number that represents the number
    of milliseconds since epoch (January 1, 1970) in UTC.
    """
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPDate"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        if isinstance(value, dict):
            self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPDate()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPBoolean(object):
    """
    represents the GP boolean object
    """
    _value = None
    _paramName = None
    _dataType = "GPBoolean"

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPBoolean"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPBoolean()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPLong(object):
    """
    represents the GP long object
    """
    _dataType = "GPLong"
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPLong"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPLong()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPString(object):
    """
    represents the GP string object
    """
    _dataType = "GPString"
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPString"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        #if isinstance(value, str):
        self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPString()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
########################################################################
class GPDouble(object):
    """
    represents the GP double object
    """
    _dataType = "GPString"
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dataType = "GPString"
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    def asDictionary(self):
        """returns object as dictionary"""
        return {
            "dataType" : self._dataType,
            "value" : self._value,
            "paramName" : self._paramName
        }
    #----------------------------------------------------------------------
    @property
    def value(self):
        """represents the object as a dictionary"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the object as a dictionary"""
        #if isinstance(value, float):
        self._value = value
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """returns the data type"""
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """gets/set the parameter name"""
        return self._paramName
    #----------------------------------------------------------------------
    @paramName.setter
    def paramName(self, value):
        """gets/set the parameter name"""
        if isinstance(value, str):
            self._paramName = value
    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """loads the GP object from a JSON string """
        j = json.loads(value)
        v = GPDouble()
        if "defaultValue" in j:
            v.value = j['defaultValue']
        else:
            v.value = j['value']
        if 'paramName' in j:
            v.paramName = j['paramName']
        elif 'name' in j:
            v.paramName = j['name']
        return v
