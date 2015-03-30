"""
This module contains the JSON domain objects.
Domains specify the set of valid values for a field.
"""
import json
########################################################################
class CodedValueDomain(object):
    """
    Coded value domain specifies an explicit set of valid values for a
    field. Each valid value is assigned a unique name. The type property
    for coded value domains is codedValue.
    """
    _type = "codedValue"
    _name = None
    _codedValues = None

    #----------------------------------------------------------------------
    def __init__(self, name):
        """Constructor"""
        self._name = name
        self._codedValues = []
    #----------------------------------------------------------------------
    @property
    def value(self):
        """gets the value as a dictionary"""
        return {
            "type" : self._type,
            "name" : self._name,
            "codedValues" : self._codedValues
        }
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the domain type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets/sets the domain name"""
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """gets/sets the domain name"""
        if self._name != value:
            self._name = value
    #----------------------------------------------------------------------
    @property
    def codedValues(self):
        """gets the coded values"""
        return self._codedValues
    #----------------------------------------------------------------------
    def addCodedValue(self, name, code):
        """
        adds a coded value to the domain

        Inputs:
           name - name of the domain
           code - value
        """
        i = {"name" : name, "code" : code}
        if i not in self._codedValues:
            self._codedValues.append(i)
    #----------------------------------------------------------------------
    def removeCodedValue(self, name):
        """removes a codedValue by name"""
        for i in self._codedValues:
            if i['name'] == name:
                self._codedValues.remove(i)
                return True
        return False
########################################################################
class InheritedDomain(object):
    """
    Inherited domains apply to domains on subtypes. It implies that the
    domain for a field at the subtype level is the same as the domain for
    the field at the layer level.
    """
    _type = "inherited"

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    #----------------------------------------------------------------------
    @property
    def value(self):
        """gets the value as a dictionary"""
        return {
            "type" : self._type,
        }
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the domain type"""
        return self._type
########################################################################
class RangeDomain(object):
    """
    Range domain specifies a range of valid values for a field. The type
    property for range domains is range.
    """
    _type = "range"
    _name = None
    _rangeMin = None
    _rangeMax = None

    #----------------------------------------------------------------------
    def __init__(self, name, minValue, maxValue):
        """Constructor"""
        self._name = name
        self._rangeMin = minValue
        self._rangeMax = maxValue
    #----------------------------------------------------------------------
    @property
    def value(self):
        """gets the value as a dictionary"""
        return {
            "type" : self._type,
            "name" : self._name,
            "range" : [self._rangeMin, self._rangeMax]
        }
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)

    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the domain type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets/sets the domain name"""
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """gets/sets the domain name"""
        if self._name != value:
            self._name = value
    #----------------------------------------------------------------------
    @property
    def minValue(self):
        """gets/sets the min value"""
        return self._rangeMin
    #----------------------------------------------------------------------
    @minValue.setter
    def minValue(self, value):
        """gets/sets the min value"""
        if isinstance(value, [int, float, long]):
            self._rangeMin = value
    #----------------------------------------------------------------------
    @property
    def maxValue(self):
        """gets/sets the max value"""
        return self._rangeMax
    #----------------------------------------------------------------------
    @maxValue.setter
    def maxValue(self, value):
        """gets/sets the min value"""
        if isinstance(value, [int, float, long]):
            self._rangeMax = value