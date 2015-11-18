"""
   Contains all the geoprocessing objects.
"""
from __future__ import absolute_import
from __future__ import print_function
import json
from ..common.general import local_time_to_online
from .._abstract.abstract import BaseGPObject
########################################################################
class GPMultiValue(BaseGPObject):
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
class GPRecordSet(BaseGPObject):
    """
    The parameter value for GPRecordSet is a JSON structure with the field
    features.
    The features field is an array of features. Each feature in turn
    contains an attributes field. The attributes field consists of
    key-value pairs where the key is a field name in the list of fields of
    the record set and the value is the value of the corresponding field.
    """
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
    @staticmethod
    def fromTable(table, paramName):
        """
        Converts a table to GPRecordSet object
        Inputs:
           table - path to the table
           paramName - name of the parameter
        """
        from ..common.spatial import recordset_to_json
        g = GPRecordSet()
        g.paramName = paramName
        g.value = json.loads(recordset_to_json(table))
        return g
########################################################################
class GPFeatureRecordSetLayer(BaseGPObject):
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
    def loadFeatures(self, path_to_fc):
        """
        loads a feature class features to the object
        """
        from ..common.spatial import featureclass_to_json
        v = json.loads(featureclass_to_json(path_to_fc))
        self.value = v
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
    @staticmethod
    def fromFeatureClass(fc, paramName):
        """
        returns a GPFeatureRecordSetLayer object from a feature class

        Input:
           fc - path to a feature class
           paramName - name of the parameter
        """
        from ..common.spatial import featureclass_to_json
        val = json.loads(featureclass_to_json(fc))
        v = GPFeatureRecordSetLayer()
        v.value = val
        v.paramName = paramName
        return v
########################################################################
class GPRasterDataLayer(BaseGPObject):
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
class GPRasterData(BaseGPObject):
    """
    The parameter value for GPRasterData is a JSON structure with the
    following fields:
     url - A URL to the location of the raster data file.
     format - A string representing the format of the raster.
    """
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
class GPDataFile(BaseGPObject):
    """
    The parameter value for GPDataFile is a JSON structure with a url
    field. The value of the url field is a URL to the location of the data
    file.
    """
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
class GPLinearUnit(BaseGPObject):
    """
    The parameter value for GPLinearUnit is a JSON structure with the
    following fields:
     distance - A double value.
     units - A string whose values can be "esriMeters", "esriMiles", and so on.
    """
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
class GPDate(BaseGPObject):
    """
    The value for GPDate data type is a number that represents the number
    of milliseconds since epoch (January 1, 1970) in UTC.
    """
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
        #from datetime import datetime
        #if isinstance(value, datetime):
            #v.value = local_time_to_online(value)
        #else:
            #v.value = value
        #v.paramName = j['paramName']
        return v
########################################################################
class GPBoolean(BaseGPObject):
    """
    represents the GP boolean object
    """
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
class GPLong(BaseGPObject):
    """
    represents the GP long object
    """
    _dataType = "GPLong"

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
class GPString(BaseGPObject):
    """
    represents the GP string object
    """
    _dataType = "GPString"

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
class GPDouble(BaseGPObject):
    """
    represents the GP double object
    """
    _dataType = "GPString"

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
