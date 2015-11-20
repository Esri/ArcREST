from __future__ import absolute_import
from __future__ import print_function
import json

class BaseSymbol(object):
    """base symbol class"""
    pass
########################################################################
class SimpleMarkerSymbol(BaseSymbol):
    """
    Simple marker symbols can be used to symbolize point geometries. The
    type property for simple marker symbols is esriSMS. The angle property
    defines the number of degrees (0 to 360) that a marker symbol is
    rotated. The rotation is from East in a counter-clockwise direction
    where East is the 0 degrees axis.
    """
    _type = "esriSMS"
    _style = None
    _color = None
    _size = None
    _angle = None
    _xoffset = None
    _yoffset = None
    _outline = None
    _styles = ['esriSMSCircle', 'esriSMSCross',
               'esriSMSDiamond', 'esriSMSSquare',
               'esriSMSX', 'esriSMSTriangle']

    #----------------------------------------------------------------------
    def __init__(self, style, color,
                 size, angle=0, xoffset=0,
                 yoffset=0, outlineColor=None,
                 outlineWidth=1):
        """Constructor"""
        if style in self._styles:
            self._style = style
        else:
            raise AttributeError("Invalid Style, items must be: %s" % ",".join(self._styles)
                                 )
        self._color = color
        self._size = size
        self._angle = angle
        self._xoffset = xoffset
        self._yoffset = yoffset
        if not outlineColor is None:
            self._outline = {
                "color" : outlineColor,
                "width" : outlineWidth
            }
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def style(self):
        """gets/sets the style"""
        return self._style
    #----------------------------------------------------------------------
    @style.setter
    def style(self, value):
        """gets/sets the style"""
        if self._style != value and \
           value in self._styles:
            self._style = value
    #----------------------------------------------------------------------
    @property
    def angle(self):
        """gets/sets the angle"""
        return self._angle
    #----------------------------------------------------------------------
    @angle.setter
    def angle(self, value):
        """gets/sets the angle"""
        if self._angle != value and \
           isinstance(value, (int, float, long)):
            self._angle = value
    #----------------------------------------------------------------------
    @property
    def color(self):
        """gets/sets the color"""
        return self._color
    #----------------------------------------------------------------------
    @color.setter
    def color(self, value):
        """gets/sets the color"""
        if self._color != value and \
           isinstance(value, Color):
            self._color = value
    #----------------------------------------------------------------------
    @property
    def size(self):
        """gets/sets the size"""
        return self._size
    #----------------------------------------------------------------------
    @size.setter
    def size(self, value):
        """gets/sets the size"""
        if self._size != value and \
           isinstance(value, (int, float, long)):
            self._size = value
    #----------------------------------------------------------------------
    @property
    def xoffset(self):
        """gets/sets the xoffset"""
        return self._xoffset
    #----------------------------------------------------------------------
    @xoffset.setter
    def xoffset(self, value):
        """gets/sets the xoffset"""
        if self._xoffset != value and \
           isinstance(value, (int, float, long)):
            self._xoffset = value
    #----------------------------------------------------------------------
    @property
    def yoffset(self):
        """gets/sets the yoffset"""
        return self._yoffset
    #----------------------------------------------------------------------
    @yoffset.setter
    def yoffset(self, value):
        """gets/sets the yoffset"""
        if self._yoffset != value and \
           isinstance(value, (int, float, long)):
            self._yoffset = value
    #----------------------------------------------------------------------
    @property
    def outlineWidth(self):
        """gets/sets the outlineWidth"""
        if self._outline is None:
            return None
        return self._outline['width']
    #----------------------------------------------------------------------
    @outlineWidth.setter
    def outlineWidth(self, value):
        """gets/sets the outlineWidth"""
        if isinstance(value, (int, float, long)) and \
           not self._outline is None:
            self._outline['width'] = value
    #----------------------------------------------------------------------
    @property
    def outlineColor(self):
        """gets/sets the outlineColor"""
        if self._outline is None:
            return None
        return self._outline['color']
    #----------------------------------------------------------------------
    @outlineColor.setter
    def outlineColor(self, value):
        """gets/sets the outlineColor"""
        if isinstance(value, Color) and \
           not self._outline is None:
            self._outline['color'] = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the object as dictionary"""
        if self._outline is None:
            return {
                "type" : "esriSMS",
                "style" : self._style,
                "color" : self._color.value,
                "size" : self._size,
                "angle" : self._angle,
                "xoffset" : self._xoffset,
                "yoffset" : self._yoffset
            }
        else:
            return {
                "type" : "esriSMS",
                "style" : self._style,
                "color" : self._color.value,
                "size" : self._size,
                "angle" : self._angle,
                "xoffset" : self._xoffset,
                "yoffset" : self._yoffset,
                "outline" : {
                    "width" : self._outline['width'],
                    "color" : self._color.value
                }
            }
    #----------------------------------------------------------------------
    def __str__(self):
        """object as string"""
        return json.dumps(self.value)
########################################################################
class SimpleLineSymbol(BaseSymbol):
    """
    Simple line symbols can be used to symbolize polyline geometries or
    outlines for polygon fills. The type property for simple line symbols
    is esriSLS.
    """
    _type = "esriSLS"
    _style = None
    _styles = ['esriSLSDash','esriSLSDashDot','esriSLSDashDotDot','esriSLSDot','esriSLSNull','esriSLSSolid']
    _color = None
    _width = None
    #----------------------------------------------------------------------
    def __init__(self, style, color, width=1):
        """Constructor"""
        if not isinstance(color, Color):
            raise AttributeError("color must be a Color object")
        self._color = color
        self._width = width
        if style in self._styles:
            self._style = style
        else:
            raise AttributeError("Invalid line style.")
    #----------------------------------------------------------------------
    @property
    def color(self):
        """gets/sets the color"""
        return self._color
    #----------------------------------------------------------------------
    @color.setter
    def color(self, value):
        """gets/sets the color"""
        if self._color != value and \
           isinstance(value, Color):
            self._color = value
    #----------------------------------------------------------------------
    @property
    def width(self):
        """gets/sets the width"""
        return self._width
    #----------------------------------------------------------------------
    @width.setter
    def width(self, value):
        """gets/sets the width"""
        if self._width != value and \
           isinstance(value, (int, float, long)):
            self._width = value

    def __str__(self):
        """ returns object as string """
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def value(self):
        """gets the color value"""
        return {
            "type" : self._type,
            "style" : self._style,
            "color" : self._color.value,
            "width" : self._width
        }
########################################################################
class SimpleFillSymbol(BaseSymbol):
    """
    Simple fill symbols can be used to symbolize polygon geometries. The
    type property for simple fill symbols is esriSFS.
    """
    _type = "esriSFS"
    _style = None
    _styles = ['esriSFSBackwardDiagonal','esriSFSCross','esriSFSDiagonalCross',
               'esriSFSForwardDiagonal','esriSFSHorizontal','esriSFSNull',
               'esriSFSSolid','esriSFSVertical']
    _color = None
    _outline = None
    #----------------------------------------------------------------------
    def __init__(self, style, color, outline=None):
        """Constructor"""
        if style in self._styles:
            self._style = style
        else:
            raise AttributeError("Invalid style type")
        if isinstance(color, Color):
            self._color = color
        else:
            raise AttributeError("Invalid type: color must be type Color")
        if not outline is None:
            if isinstance(outline, SimpleLineSymbol):
                self._outline = outline
            else:
                raise AttributeError("Invalid type: outline must be type SimpleLineSymbol")
        else:
            self._outline = None
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the type"""
        return self._type
    #----------------------------------------------------------------------
    @property
    def style(self):
        """gets/sets the style"""
        return self._style
    #----------------------------------------------------------------------
    @style.setter
    def style(self, value):
        """gets/sets the style"""
        if self._style != value and \
           value in self._styles:
            self._style = value
    #----------------------------------------------------------------------
    @property
    def color(self):
        """gets/sets the color"""
        return self._color
    #----------------------------------------------------------------------
    @color.setter
    def color(self, value):
        """gets/sets the color"""
        if self._color != value and \
           isinstance(value, Color):
            self._color = value
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def value(self):
        """gets the color value"""
        if self._outline is None:
            return {
                "type" : self._type,
                "style" : self._style,
                "color" : self._color.value,
            }
        else:
            return {
                "type" : self._type,
                "style" : self._style,
                "color" : self._color.value,
                "outline" : self._outline.value
            }
########################################################################
class Color(object):
    """
    Color is represented as a four-element array. The four elements
    represent values for red, green, blue, and alpha in that order. Values
    range from 0 through 255. If color is undefined for a symbol, the color
    value is null.
    """
    _red = None
    _green = None
    _blue = None
    _alpha = None

    #----------------------------------------------------------------------
    def __init__(self, red, green, blue, alpha=255):
        """Constructor"""
        self._red = red
        self._green = green
        self._blue = blue
        self._alpha = alpha
    #----------------------------------------------------------------------
    @property
    def red(self):
        """gets/sets the red value"""
        return self._red
    #----------------------------------------------------------------------
    @red.setter
    def red(self, value):
        """gets/sets the red value"""
        if value != self._red and \
           isinstance(value, int):
            self._red = value
    #----------------------------------------------------------------------
    @property
    def green(self):
        """gets/sets the green value"""
        return self._green
    #----------------------------------------------------------------------
    @green.setter
    def green(self, value):
        """gets/sets the green value"""
        if value != self._green and \
           isinstance(value, int):
            self._green = value
    #----------------------------------------------------------------------
    @property
    def blue(self):
        """gets/sets the blue value"""
        return self._blue
    #----------------------------------------------------------------------
    @blue.setter
    def blue(self, value):
        """gets/sets the blue value"""
        if value != self._blue and \
           isinstance(value, int):
            self._blue = value
    #----------------------------------------------------------------------
    @property
    def alpha(self):
        """gets/sets the alpha value"""
        return self._alpha
    #----------------------------------------------------------------------
    @alpha.setter
    def alpha(self, value):
        """gets/sets the alpha value"""
        if value != self._alpha and \
           isinstance(value, int):
            self._alpha = value
    def __str__(self):
        """ returns object as string """
        return json.dumps(self.value)
    #----------------------------------------------------------------------
    @property
    def value(self):
        """gets the color value"""
        return [self._red,
                self._green,
                self._blue,
                self._alpha]



