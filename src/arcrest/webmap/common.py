"""
Implementation of the common data object for webmap specification
found on the REST API help page.
"""
import json

########################################################################
class Value(object):
    """
    The value object contains information for pop-up windows about how images should be retrieved or charts constructed. For more information on how this object is used, see mediaInfo and popupInfo.
    """
    _fields = None
    _linkURL = None
    _normalizeField = None
    _sourceURL = None

    #----------------------------------------------------------------------
    def __init__(self, fields=None,
                 linkURL=None,
                 normalizeField=None,
                 sourceURL=None):
        """Constructor"""
        if self._fields is None:
            self._fields = []
        else:
            self._fields = fields
        self._linkURL = linkURL
        self._normalizeField = normalizeField
        self._sourceURL = sourceURL
    def __str__(self):
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    def value(self):
        """"""
        v = {}
        if self._fields:
            v['fields'] = self._fields
        if self._linkURL:
            v['linkURL'] = self._linkURL
        if self._normalizeField:
            v['normalizeField'] = self._normalizeField
        if self._sourceURL:
            v['sourceURL'] = self._sourceURL
        return v
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """gets the fields"""
        return self._fields
    #----------------------------------------------------------------------
    def add_field(self, value):
        """adds a field to fields"""
        if self._fields is None:
            self._fields = []
        if value not in self._fields:
            self._fields.append(value)
    #----------------------------------------------------------------------
    def remove_field(self, value):
        """removes a field by name"""
        if isinstance(self._fields, list) and \
           value in self._fields:
            self._fields.remove(value)
    #----------------------------------------------------------------------
    @property
    def linkURL(self):
        """gets/sets the linkURL"""
        return self._linkURL
    #----------------------------------------------------------------------
    @linkURL.setter
    def linkURL(self, value):
        """gets/sets the linkURL"""
        if self._linkURL != value:
            self._linkURL = value
    #----------------------------------------------------------------------
    @property
    def normalizeField(self):
        """gets/sets the normalizeField"""
        return self._normalizeField
    #----------------------------------------------------------------------
    @normalizeField.setter
    def normalizeField(self, value):
        """gets/sets the normalizeField"""
        if self._normalizeField != value:
            self._normalizeField = value
    #----------------------------------------------------------------------
    @property
    def sourceURL(self):
        """gets/sets the sourceURL"""
        return self._sourceURL
    #----------------------------------------------------------------------
    @sourceURL.setter
    def sourceURL(self, value):
        """gets/sets the normalizeField"""
        if self._sourceURL != value:
            self._sourceURL = value
    @staticmethod
    def from_json(text):
        """converts a string of text into the object"""
        v = json.loads(text)
        obj = Value()
        if "fields" in v:
            obj._fields = v['fields']
        if "linkURL" in v:
            obj.linkURL = v['linkURL']
        if "normalizeField" in v:
            obj.normalizeField = v['normalizeField']
        if "sourceURL" in v:
            obj.sourceURL = v['sourceURL']
        return obj
########################################################################
class Template(object):
    """
    Templates describe features that can be created in a layer. Templates
    are used with map notes, other feature collections, and editable
    web-based CSV layers. They are not used with ArcGIS feature services,
    which already have feature templates defined in the service.
    Templates are defined as properties of the layer definition when there
    are no types defined; otherwise, templates are defined as properties of
    the types.

    Inputs:
       description - A string containing a detailed description of the
        template.
       drawingTool - An optional string that can define a client-side
        drawing tool to be used with this feature. For example, the map
        notes used by the ArcGIS.com map viewer use the following strings
        to represent the viewer's different drawing tools:
          esriFeatureEditToolPolygon | esriFeatureEditToolTriangle |
          esriFeatureEditToolRectangle | esriFeatureEditToolLeftArrow |
          esriFeatureEditToolRightArrow | esriFeatureEditToolEllipse |
          esriFeatureEditToolUpArrow | esriFeatureEditToolDownArrow |
          esriFeatureEditToolCircle | esriFeatureEditToolFreehand |
          esriFeatureEditToolLine | esriFeatureEditToolText |
          esriFeatureEditToolPoint
       name - A string containing a user-friendly name for the template.
        This name can appear on a menu of feature choices displayed in the
        client editing environment.
       prototype - a feature object representing a prototyprical feature
        for the template.
    """
    _name = None
    _description = None
    _prototype = None
    _drawingTool = None
    _allowed_drawing = ["esriFeatureEditToolPolygon", "esriFeatureEditToolTriangle",
                        "esriFeatureEditToolRectangle",
                        "esriFeatureEditToolLeftArrow","esriFeatureEditToolRightArrow",
                        "esriFeatureEditToolEllipse",
                        "esriFeatureEditToolUpArrow","esriFeatureEditToolDownArrow",
                        "esriFeatureEditToolCircle","esriFeatureEditToolFreehand",
                        "esriFeatureEditToolLine","esriFeatureEditToolText",
                        "esriFeatureEditToolPoint"]
    #----------------------------------------------------------------------
    def __init__(self, name, description,
                 prototype, drawingTool=None):
        """Constructor"""
        self.name = name
        self.description = description
        self.prototype = prototype
        if drawingTool in self._allowed_drawing:
            self._drawingTool = drawingTool
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets/sets the name"""
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """gets/sets the name"""
        if value:
            self._name = value
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets/sets the description"""
        return self._description
    #----------------------------------------------------------------------
    @description.settter
    def description(self, value):
        """gets/sets the description"""
        if value:
            self._description = value
    #----------------------------------------------------------------------
    @property
    def prototype(self):
        """gets/sets the prototype feature object"""
        return self._prototype
    @prototype.setter
    def prototype(self, value):
        if value:
            if isinstance(value, [dict, str]):
                self._prototype = Feature.from_json(
                    json.dumps(value))
            self._prototype = value
    #----------------------------------------------------------------------
    @property
    def drawingTool(self):
        """gets/sets the drawing tool"""
        return self._drawingTool
    #----------------------------------------------------------------------
    @drawingTool.setter
    def drawingTool(self, value):
        if value and \
           value in self._allowed_drawing:
            self._drawingTool = value
    #----------------------------------------------------------------------
    @staticmethod
    def from_json(text):
        """converts a string of text into the object"""
        v = json.loads(text)
        if "name" in v and \
           "description" in v and \
           "prototype" in v:
            obj = Template(name=v['name'],
                           description=v['description'],
                           prototype=v['prototype'])
        if "drawingTool" in v:
            obj.drawingTool = v['drawingTool']
        return obj
    #----------------------------------------------------------------------
    def __str__(self):
            return json.dumps(self.value)
    #----------------------------------------------------------------------
    def value(self):
        """"""
        v = {}
        if self._description:
            v['description'] = self._description
        if self._drawingTool:
            v['drawingTool'] = self._drawingTool
        if self._name:
            v['name'] = self._name
        if self._prototype:
            v['prototype'] = self._prototype.value
        return v
########################################################################
class Type(object):
    """
    Types contain information about the combinations of attributes allowed
    for features in the dataset. Each feature in the dataset can have a
    type, indicated in its typeIdField, which is used in layerDefinition.

    Inputs:
       domains -
       id - unique numerical ID for the type
       name - A string containing a user-friendly name for the type. This
        can be shown on a menu of feature types that editors can create in
        the collection.
       templates - An array of template objects describing features that
        can be created in this layer. Templates are used with map notes,
        other feature collections, and editable web-based CSV layers. They
        are not used with ArcGIS feature services, which already have
        feature templates defined in the service.
    """
    _id = None
    _name = None
    _domains = None
    _templates = None
    #----------------------------------------------------------------------
    def __init__(self, id, name, domains=None, templates=None):
        """Constructor"""
        self._id = id
        self._name = name
        if isinstance(domains, dict):
            self._domains = domains
        else:
            self._domains = {}
        if isinstance(templates, list):
            self._templates = templates
        else:
            self._templates = []
    #----------------------------------------------------------------------
    @property
    def id(self):
        """gets/sets the id"""
        return self._id
    #----------------------------------------------------------------------
    @id.property
    def id(self, value):
        """gets/sets the type id"""
        if value:
            self._id = value
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets/sets the name"""
        return self._name
    #----------------------------------------------------------------------
    @name.setter
    def name(self, value):
        """gets/sets the name"""
        if name:
            self._name = name
    #----------------------------------------------------------------------
    def add_domain(self, key, value):
        """add domain value to the domains list"""
        if isinstance(self._domains, dict):
            self._domains[key] = value
        elif self._domains is None:
            self._domains = {}
            self.add_domain(key, value)
    #----------------------------------------------------------------------
    def remove_domain(self, key):
        if key in self._domains:
            del self._domains[key]
    #----------------------------------------------------------------------
    @property
    def domains(self):
        """gets/sets the domains"""
        return self._domains
    #----------------------------------------------------------------------
    @domains.setter
    def domains(self, value):
        """gets/sets the domains"""
        if isinstance(value, dict) and \
           value != self._domains:
            self._domains = value
    #----------------------------------------------------------------------
    @property
    def templates(self):
        """gets/sets the templates"""
        return self._templates
    #----------------------------------------------------------------------
    @templates.setter
    def templates(self, value):
        """gets/sets the templates"""
        if isinstance(value, list):
            self._templates = value
    def add_template(self, template):
        if isinstance(template, Template):
            self._templates.append(template)
    def remove_template(self, value):
        """removes a value from the templates"""
        try:
            self._templates.remove(value)
        except:
            pass
    @staticmethod
    def from_json(text):
        """creates the object from JSON"""
        v = json.loads(text)










