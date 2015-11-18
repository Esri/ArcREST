from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseRenderer
import json

########################################################################
class SimpleRenderer(BaseRenderer):
    """ A simple renderer is a renderer that uses one symbol only. The type
        property for simple renderers is simple.
    """
    _type = "simple"
    _symbol = None
    _label = None
    _description = None
    _rotationType = None
    _rotationExpression = None
    #----------------------------------------------------------------------
    def __init__(self, symbol, label, description="",
                 rotationType="geographic", rotationExpression=""):
        """Constructor"""
        self._symbol = symbol
        self._label = label
        self._description = description
        self._rotationType = rotationType
        self._rotationExpression = rotationExpression
    #----------------------------------------------------------------------
    def __str__(self):
        """ provides a string reprsentation of the object """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ provides a dictionary representation of the object """
        template = {
            "type" : "simple",
            "symbol" :  self._symbol.asDictionary,
            "label" : self._label,
            "description" : self._description,
            "rotationType": self._rotationType,
            "rotationExpression": self._rotationExpression
        }
        return template
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ gets the type value """
        return self._type

########################################################################
class UniqueValueRenderer:
    """
       A unique value renderer symbolizes groups of features that have
       matching field values. The type property for unique value renderers
       is uniqueValue. The rotationType property controls the origin and
       direction of rotation. If the rotationType is defined as arithmetic,
       the symbol is rotated from East in a counter-clockwise direction
       where East is the 0 axis. If the rotationType is defined as
       geographic, the symbol is rotated from North in a clockwise
       direction where North is the 0 axis.
    """
    _type = "uniqueValue"
    _field1 = None
    _field2 = None
    _field3 = None
    _fieldDelimiter = None
    _defaultSymbol = None
    _defaultLabel = None
    _uniqueValueInfos = None
    _rotationType = None
    _rotationExpression = None
    #----------------------------------------------------------------------
    def __init__(self,
                 field1,
                 defaultSymbol,
                 defaultLabel="Other Values",
                 field2=None,
                 field3=None,
                 fieldDelimiter="",
                 uniqueValueInfos=[],
                 rotationType="geographic",
                 rotationExpression=""):
        """Constructor"""
        self._field1 = field1
        self._field2 = field2
        self._field3 = field3
        self._defaultSymbol = defaultSymbol
        self._defaultLabel = defaultLabel
        self._fieldDelimiter = fieldDelimiter
        self._uniqueValueInfos = uniqueValueInfos
        self._rotationType = rotationType
        self._rotationExpression = rotationExpression
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the type """
        return self._type
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the object as string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        template = {
            "type" : "uniqueValue",
            "field1" : self._field1,
            "field2" : self._field2,
            "field3" : self._field3,
            "fieldDelimiter" : self._fieldDelimiter,
            "defaultSymbol" :  self._defaultSymbol.asDictionary,
            "defaultLabel" : self._defaultLabel,
            "uniqueValueInfos" : self._uniqueValueInfos,
            "rotationType": self._rotationType,
            "rotationExpression": self._rotationExpression
        }
        return template
########################################################################
class ClassBreaksRenderer:
    """
       A class breaks renderer symbolizes each feature based on the value
       of some numeric field. The type property for class breaks renderers
       is classBreaks.
    """
    _type = "classBreaks"

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ gets the object type """
        return self._type














