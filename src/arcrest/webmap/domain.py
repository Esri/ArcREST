"""
   Contains all domain types
"""
from base import BaseDomain
import json

########################################################################
class RangeDomain(BaseDomain):
    """
       Range domain specifies a range of valid values for a field. The type
       property for range domains is range.
    """
    _type = "range"
    _domainName = None
    range = None
    #----------------------------------------------------------------------
    def __init__(self, domainName, range):
        """Constructor"""
        self._range = None
        self._domainName = domainName
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the object type """
        return self._type
    #----------------------------------------------------------------------
    @property
    def domainName(self):
        """ gets the domain name """
        return self._domainName
    #----------------------------------------------------------------------
    @domainName.setter
    def domainName(self, value):
        """ sets the domain name """
        self._domainName = value
    #----------------------------------------------------------------------
    @property
    def range(self):
        """ gets the range value """
        return self._range
    #----------------------------------------------------------------------
    @range.setter
    def range(self, value):
        """ sets the range value """
        self._range = value
    #----------------------------------------------------------------------
    def __str__(self):
        """ object as string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ object as dictionary """
        return {
            "type": "range",
            "name": self._domainName,
            "range": self._range
        }

########################################################################
class CodedValueDomain(BaseDomain):
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
    def type(self):
        """ returns the object type """
        return self._type
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the object as a string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as dictionary """
        return {
            "type" : self._type,
            "name" : self._name,
            "codedValues" : self._codedValues
        }
    #----------------------------------------------------------------------
    def add_codedValue(self, name, code):
        """ adds a value to the coded value list """
        if self._codedValues is None:
            self._codedValues = []
        self._codedValues.append(
            {"name": name, "code": code}
        )
    #----------------------------------------------------------------------
    def clearAllDomains(self):
        """ removes all domains from object """
        self._codedValues = []
    #----------------------------------------------------------------------
    @property
    def codedValues(self):
        """ returns all coded values for a domain """
        return self._codedValues


















