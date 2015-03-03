import json
########################################################################
class BaseRenderer(object):
    """base renderer object"""
    pass
########################################################################
class SimpleRenderer(BaseRenderer):
    """
    A simple renderer is a renderer that uses one symbol only
    """
    _type = "simple"
    _symbol = None
    _label = None
    _description = None
    _rotationType = None
    _rotationExpression = None
    _rotationTypes = ['arithmetic','geographic']
    #----------------------------------------------------------------------
    def __init__(self, symbol, label=None, description=None,
                 rotationType="aritmetic", rotationExpression=None):
        """Constructor"""
        self._symbol = symbol
        self._label = label
        self._description = description
        self._rotationExpression = rotationExpression
        self._rotationType = rotationType
    #----------------------------------------------------------------------
    @property
    def symbol(self):
        """gets/sets the symbol"""
        return self._symbol
    #----------------------------------------------------------------------
    @symbol.setter
    def symbol(self, value):
        """gets/sets the symbol"""
        if self._symbol != value:
            self._symbol = value
    #----------------------------------------------------------------------
    @property
    def label(self):
        """gets/sets the label"""
        return self._label
    #----------------------------------------------------------------------
    @label.setter
    def label(self, value):
        """gets/sets the label"""
        if self._label != value:
            self._label = value

    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets/sets the description"""
        return self._description
    #----------------------------------------------------------------------
    @description.setter
    def description(self, value):
        """gets/sets the description"""
        if self._description != value:
            self._description = value
    #----------------------------------------------------------------------
    @property
    def rotationExpression(self):
        """gets/sets the rotationExpression"""
        return self._rotationExpression
    #----------------------------------------------------------------------
    @rotationExpression.setter
    def rotationExpression(self, value):
        """gets/sets the rotationExpression"""
        if self._rotationExpression != value:
            self._rotationExpression = value
    #----------------------------------------------------------------------
    @property
    def rotationType(self):
        """gets/sets the rotationType"""
        return self._rotationType
    #----------------------------------------------------------------------
    @rotationType.setter
    def rotationType(self, value):
        """gets/sets the rotationType"""
        if self._rotationType.lower() in self._rotationTypes and \
           self._rotationType != value:
            self._rotationType = value
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns object as dictionary"""
        return {
            "type" : "simple",
              "symbol" :  self.symbol.value,
              "label" : self.label,
              "description" : self.description,
              "rotationType": self.rotationType,
              "rotationExpression": self.rotationExpression
        }
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)

########################################################################
class UniqueValueRenderer(BaseRenderer):
    """
    A simple renderer is a renderer that uses one symbol only
    """
    _type = "uniqueValue"
    _defaultSymbol = None
    _defaultLabel = None
    _rotationType = None
    _rotationExpression = None
    _rotationTypes = ['arithmetic','geographic']
    _field1 = None
    _field2 = None
    _field3 = None
    _fieldDelimiter = None
    _uniqueValueInfos = None

    #----------------------------------------------------------------------
    def __init__(self,
                 defaultSymbol,
                 defaultLabel,
                 field1,
                 field2=None,
                 field3=None,
                 fieldDelimiter=None,
                 rotationType="aritmetic",
                 rotationExpression=None):
        """Constructor"""
        self._defaultSymbol = defaultSymbol
        self._defaultLabel = defaultLabel
        self._rotationExpression = rotationExpression
        self._rotationType = rotationType
        self._field1 = field1
        self._field2 = field2
        self._field3 = field3
        self._fieldDelimiter = fieldDelimiter
        self._uniqueValueInfos = []
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the object as a dictionary"""
        return {}
    #----------------------------------------------------------------------
    def __str__(self):
        """object as string"""
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def defaultSymbol(self):
        """gets/sets the symbol"""
        return self._defaultSymbol
    #----------------------------------------------------------------------
    @defaultSymbol.setter
    def defaultSymbol(self, value):
        """gets/sets the symbol"""
        if self._defaultSymbol != value:
            self._defaultSymbol = value
    #----------------------------------------------------------------------
    @property
    def defaultLabel(self):
        """gets/sets the label"""
        return self._defaultLabel
    #----------------------------------------------------------------------
    @defaultLabel.setter
    def defaultLabel(self, value):
        """gets/sets the label"""
        if self._defaultLabel != value:
            self._defaultLabel = value
    #----------------------------------------------------------------------
    @property
    def rotationExpression(self):
        """gets/sets the rotationExpression"""
        return self._rotationExpression
    #----------------------------------------------------------------------
    @rotationExpression.setter
    def rotationExpression(self, value):
        """gets/sets the rotationExpression"""
        if self._rotationExpression != value:
            self._rotationExpression = value
    #----------------------------------------------------------------------
    @property
    def rotationType(self):
        """gets/sets the rotationType"""
        return self._rotationType
    #----------------------------------------------------------------------
    @rotationType.setter
    def rotationType(self, value):
        """gets/sets the rotationType"""
        if self._rotationType.lower() in self._rotationTypes and \
           self._rotationType != value:
            self._rotationType = value
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def field1(self):
        """gets/sets the field1"""
        return self._field1
    #----------------------------------------------------------------------
    @property
    def field2(self):
        """gets/sets the field2"""
        return self._field2
    #----------------------------------------------------------------------
    @property
    def field3(self):
        """gets/sets the field3"""
        return self._field3
    #----------------------------------------------------------------------
    @field1.setter
    def field1(self, value):
        """gets/sets the field1"""
        if self._field1 != value:
            self._field1 = value
    #----------------------------------------------------------------------
    @field2.setter
    def field2(self, value):
        """gets/sets the field2"""
        if self._field2 != value:
            self._field2 = value
    #----------------------------------------------------------------------
    @field3.setter
    def field3(self, value):
        """gets/sets the field3"""
        if self._field3 != value:
            self._field3 = value
    #----------------------------------------------------------------------
    @property
    def fieldDelimiter(self):
        """gets/sets the fieldDelimiter"""
        return self._fieldDelimiter
    #----------------------------------------------------------------------
    @fieldDelimiter.setter
    def fieldDelimiter(self, value):
        """gets/sets the fieldDelimiter"""
        if self._fieldDelimiter != value:
            self._fieldDelimiter = value
    #----------------------------------------------------------------------
    @property
    def uniqueValueInfos(self):
        """gets the uniqueValueInfos"""
        return self._uniqueValueInfos
    #----------------------------------------------------------------------
    def addUniqueValue(self, value, label, description, symbol):
        """
        adds a unique value to the renderer
        """
        if self._uniqueValueInfos is None:
            self._uniqueValueInfos = []
        self._uniqueValueInfos.append(
            {
                "value" : value,
                "label" : label,
                "description" : description,
                "symbol" : symbol
            }
        )
    #----------------------------------------------------------------------
    def removeUniqueValue(self, value):
        """removes a unique value in unique Value Info"""
        for v in self._uniqueValueInfos:
            if v['value'] == value:
                self._uniqueValueInfos.remove(v)
                return True
            del v
        return False
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns object as dictionary"""
        return {
            "type" : "uniqueValue",
            "field1" : self._field1,
            "field2" : self._field2,
            "field3" : self._field3,
            "fieldDelimiter" : self._fieldDelimiter,
            "defaultSymbol" :  self._defaultSymbol.value,
            "defaultLabel" : self._defaultLabel,
            "uniqueValueInfos" : self._uniqueValueInfos,
            "rotationType": self._rotationType,
            "rotationExpression": self._rotationExpression
        }
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)
########################################################################
class ClassBreakRenderer(BaseRenderer):
    """
    A simple renderer is a renderer that uses one symbol only
    """
    _type = "classBreaks"
    _defaultSymbol = None
    _defaultLabel = None
    _rotationType = None
    _rotationExpression = None
    _rotationTypes = ['arithmetic','geographic']
    _field = None
    _classBreakInfos = None
    _classificationMethod = None
    _normalizationType = None
    _normalizationField = None
    _normalizationTotal = None
    _backgroundFillSymbol = None
    _minValue = None
    #----------------------------------------------------------------------
    def __init__(self,
                 defaultSymbol,
                 defaultLabel,
                 field,
                 classificationMethod,
                 normalizationType=None,
                 normalizationField=None,
                 normalizationTotal=None,
                 backgroundFillSymbol=None,
                 minValue=None,
                 rotationType="aritmetic",
                 rotationExpression=None):
        """Constructor"""
        self._defaultSymbol = defaultSymbol
        self._defaultLabel = defaultLabel
        self._rotationExpression = rotationExpression
        self._rotationType = rotationType
        self._field = field
        self._classificationMethod = classificationMethod
        self._normalizationField = normalizationField
        self._normalizationTotal = normalizationTotal
        self._normalizationType = normalizationType
        self._backgroundFillSymbol = backgroundFillSymbol
        self._minValue = minValue
        self._classBreakInfos = []
    #----------------------------------------------------------------------
    @property
    def defaultSymbol(self):
        """gets/sets the symbol"""
        return self._defaultSymbol
    #----------------------------------------------------------------------
    @defaultSymbol.setter
    def defaultSymbol(self, value):
        """gets/sets the symbol"""
        if self._defaultSymbol != value:
            self._defaultSymbol = value
    #----------------------------------------------------------------------
    @property
    def defaultLabel(self):
        """gets/sets the label"""
        return self._defaultLabel
    #----------------------------------------------------------------------
    @defaultLabel.setter
    def defaultLabel(self, value):
        """gets/sets the label"""
        if self._defaultLabel != value:
            self._defaultLabel = value
    #----------------------------------------------------------------------
    @property
    def rotationExpression(self):
        """gets/sets the rotationExpression"""
        return self._rotationExpression
    #----------------------------------------------------------------------
    @rotationExpression.setter
    def rotationExpression(self, value):
        """gets/sets the rotationExpression"""
        if self._rotationExpression != value:
            self._rotationExpression = value
    #----------------------------------------------------------------------
    @property
    def rotationType(self):
        """gets/sets the rotationType"""
        return self._rotationType
    #----------------------------------------------------------------------
    @rotationType.setter
    def rotationType(self, value):
        """gets/sets the rotationType"""
        if self._rotationType.lower() in self._rotationTypes and \
           self._rotationType != value:
            self._rotationType = value
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def field(self):
        """gets/sets the field"""
        return self._field
    #----------------------------------------------------------------------
    @field.setter
    def field(self, value):
        """gets/sets the field"""
        if self._field != value:
            self._field = value
    #----------------------------------------------------------------------
    @property
    def classBreakInfos(self):
        """gets the class breaks"""
        return self._classBreakInfos
    #----------------------------------------------------------------------
    def addClassBreak(self, classMinValue, classMaxValue, label, description, symbol):
        """
        adds a classification break value to the renderer
        """
        if self._classBreakInfos is None:
            self._classBreakInfos = []
        self._classBreakInfos.append(
            {
                "classMinValue" : classMinValue,
                "classMaxValue" : classMaxValue,
                "label" : label,
                "description" : description,
                "symbol" :  symbol
            }
        )
    #----------------------------------------------------------------------
    def removeClassBreak(self, label):
        """removes a classification break value to the renderer"""
        for v in self._classBreakInfos:
            if v['label'] == label:
                self._classBreakInfos.remove(v)
                return True
            del v
        return False
    #----------------------------------------------------------------------
    @property
    def classificationMethod(self):
        """gets/sets the classificationMethod"""
        return self._classificationMethod
    #----------------------------------------------------------------------
    @classificationMethod.setter
    def classificationMethod(self, value):
        """gets/sets the classificationMethod"""
        if self._classificationMethod != value:
            self._classificationMethod = value
    #----------------------------------------------------------------------
    @property
    def normalizationField(self):
        """gets/sets the normalizationField"""
        return self._normalizationField
    #----------------------------------------------------------------------
    @normalizationField.setter
    def normalizationField(self, value):
        """gets/sets the normalizationField"""
        if self._normalizationField != value:
            self._normalizationField = value
    #----------------------------------------------------------------------
    @property
    def normalizationTotal(self):
        """gets/sets the normalizationTotal"""
        return self._normalizationTotal
    #----------------------------------------------------------------------
    @normalizationTotal.setter
    def normalizationTotal(self, value):
        """gets/sets the normalizationTotal"""
        if self._normalizationTotal != value:
            self._normalizationTotal = value
    #----------------------------------------------------------------------
    @property
    def normalizationType(self):
        """gets/sets the normalizationType"""
        return self._normalizationType
    #----------------------------------------------------------------------
    @normalizationTotal.setter
    def normalizationTotal(self, value):
        """gets/sets the normalizationType"""
        if self._normalizationType != value:
            self._normalizationType = value
    #----------------------------------------------------------------------
    @property
    def minValue(self):
        """gets/sets the minValue"""
        return self._minValue
    #----------------------------------------------------------------------
    @minValue.setter
    def minValue(self, value):
        """gets/sets the minValue"""
        if self._minValue != value:
            self._minValue = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns object as dictionary"""
        return {
            "type" : "classBreaks",
            "field" : self._field,
            "classificationMethod" : "<classification method>",
            "normalizationType" : self._normalizationType,
            "normalizationField" : self._normalizationField,
            "normalizationTotal" : self._normalizationTotal,
            "defaultSymbol": self._defaultSymbol.value,
            "defaultLabel": self.defaultLabel,
            "backgroundFillSymbol": self._backgroundFillSymbol,
            "minValue" : self._minValue,
            "classBreakInfos" : self.classBreakInfos,
            "rotationType": self._rotationType,
            "rotationExpression": self._rotationExpression
        }
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        return json.dumps(self.value)