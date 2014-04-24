from base import BaseSymbol
import os
import json
import base64

########################################################################
class Color(BaseSymbol):
    """
       Color is represented as a four-element array. The four elements
       represent values for red, green, blue, and alpha in that order.
       Values range from 0 through 255. If color is undefined for a symbol,
       the color value is null.
    """
    _red = None
    _green = None
    _blue = None
    _alpha = None
    #----------------------------------------------------------------------
    def __init__(self, red=0, green=0, blue=0, alpha=255):
        """Constructor"""
        self._red = red
        self._green = green
        self._blue = blue
        self._alpha = alpha
    #----------------------------------------------------------------------
    @property
    def red(self):
        """ returns the red value """
        return self._red
    #----------------------------------------------------------------------
    @red.setter
    def red(self, value):
        """ sets the red value 0-255 """
        if value >= 0 and value <= 255:
            self._red = value
    #----------------------------------------------------------------------
    @property
    def green(self):
        """ returns the green value  """
        return self._green
    #----------------------------------------------------------------------
    @green.setter
    def green(self, value):
        """ sets the green value 0-255 """
        if value >= 0 and value <= 255:
            self._green = value
    #----------------------------------------------------------------------
    @property
    def blue(self):
        """ returns the blue value """
        return self._blue
    #----------------------------------------------------------------------
    @blue.setter
    def blue(self, value):
        """ sets the blue value 0-255 """
        if value >= 0 and value <= 255:
            self._blue = value
    #----------------------------------------------------------------------
    @property
    def alpha(self):
        """ returns the alpha value """
        return self._blue
    #----------------------------------------------------------------------
    @alpha.setter
    def alpha(self, value):
        """ sets the alpha value 0-255 """
        if value >= 0 and value <= 255:
            self._alpha = value
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the values as a string """
        return json.dumps([self._red, self._green, self._blue, self._alpha])
    #----------------------------------------------------------------------
    @property
    def asList(self):
        """ returns the value as the list object"""
        return [self._red, self._green, self._blue, self._alpha]
########################################################################
class SimpleMarkerSymbol(BaseSymbol):
    """
       Simple marker symbols can be used to symbolize point geometries. The
       type property for simple marker symbols is esriSMS. The angle
       property defines the number of degrees (0 to 360) that a marker
       symbol is rotated. The rotation is from East in a counter-clockwise
       direction where East is the 0 axis.
    """
    _type = "esriSMS"
    _styles = ("esriSMSCircle", "esriSMSCross", "esriSMSDiamond",
               "esriSMSSquare", "esriSMSX", "esriSMSTriangle")
    _style = None
    _color = None
    _size = None
    _angle = None
    _xoffset = None
    _yoffset = None
    _outlineColor = None
    _outlineWidth = None
    #----------------------------------------------------------------------
    def __init__(self, color,
                 style="esriSMSCircle",
                 size=8, angle=0,
                 xoffset=0, yoffset=0,
                 outlineColor=None,
                 outlineWidth=1
                 ):
        """Constructor"""
        if isinstance(color, (list, Color)):
            if color is list:
                self._color = color
            else:
                self._color = color.asList
        if style in self._styles:
            self._style = style
        else:
            self._style = "esriSMSCircle"
        self._size = size
        self._angle = angle
        self._xoffset = xoffset
        self._yoffset = yoffset
        if isinstance(outlineColor, (list, Color)):
            if color is list:
                self._outlineColor = color
            else:
                self._outlineColor = color.asList
        self._outlineWidth = outlineWidth
    def __str__(self):
        """  returns the object as a string """
        return json.dumps(self.asDictionary)
    @property
    def asDictionary(self):
        """ returns the object as a dictionary """
        template = {
            "type" : "esriSMS",
            "style" : self._style,
            "color" : self._color,
            "size" : self._size,
            "angle" : self._angle,
            "xoffset" : self._xoffset,
            "yoffset" : self._yoffset
        }
        if self._outlineColor is not None and \
           self._outlineWidth is not None:
            template["outline"] = {
                "color" : self._outlineColor,
                "width" : self._outlineWidth
            }
        return template
    #----------------------------------------------------------------------
    @property
    def color(self):
        """ returns the color """
        return self._color
    #----------------------------------------------------------------------
    @color.setter
    def color(self, value):
        """ sets the color """
        if isinstance(value, (list, Color)):
            if value is list:
                self._color = value
            else:
                self._color = value.asList
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the symbol type """
        return self._type
    #----------------------------------------------------------------------
    @property
    def style(self):
        """ returns the symbol style """
        return self._style
    #----------------------------------------------------------------------
    @style.setter
    def style(self, value):
        """ sets the style """
        if value in self._styles:
            self._style = value
    #----------------------------------------------------------------------
    @property
    def size(self):
        """ gets the size """
        return self._size
    #----------------------------------------------------------------------
    @size.setter
    def size(self, value):
        """ sets the size """
        self._size = value
    #----------------------------------------------------------------------
    @property
    def angle(self):
        """ gets the angle """
        return self._angle
    #----------------------------------------------------------------------
    @angle.setter
    def angle(self, value):
        """ sets the angle """
        self._angle = value
    #----------------------------------------------------------------------
    @property
    def xoffset(self):
        """ gets the x offset """
        return self._xoffset
    #----------------------------------------------------------------------
    @xoffset.setter
    def xoffset(self, value):
        """ sets the xoffset """
        if isinstace(value (int, float, long)):
            self._xoffset = value
    #----------------------------------------------------------------------
    @property
    def yoffset(self):
        """ gets the y offset value """
        return self._yoffset
    #----------------------------------------------------------------------
    @yoffset.setter
    def yoffset(self, value):
        """ sets the y offset """
        if isinstace(value (int, float, long)):
            self._yoffset = value
    #----------------------------------------------------------------------
    @property
    def outlineColor(self):
        """ gets the outline color """
        return self._outlineColor
    #----------------------------------------------------------------------
    @outlineColor.setter
    def outlineColor(self, value):
        """ sets the outline color """
        if isinstance(value, (list, Color)):
            if value is list:
                self._outlineColor = value
            else:
                self._outlineColor = value.asList
    #----------------------------------------------------------------------
    @property
    def outlineWidth(self):
        """ gets the outline width """
        return self._outlineWidth
    #----------------------------------------------------------------------
    @outlineWidth.setter
    def outlineWidth(self, value):
        """ sets the outline width """
        self._outlineWidth = value
########################################################################
class SimpleLineSymbol(BaseSymbol):
    """
       Simple line symbols can be used to symbolize polyline geometries or
       outlines for polygon fills. The type property for simple line
       symbols is esriSLS.
    """
    _type = "esriSLS"
    _style = None
    _width = None
    _color = None
    #----------------------------------------------------------------------
    def __init__(self, color, style="esriSLSSolid", width=1):
        """Constructor"""
        self._style = style
        self._width = width
        if isinstance(color, (list, Color)):
            if color is list:
                self._color = color
            else:
                self._color = color.asList
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the type """
        return "esriSLS"
    #----------------------------------------------------------------------
    @property
    def style(self):
        """ gets the style """
        return self._style
    #----------------------------------------------------------------------
    @style.setter
    def style(self, value):
        """ sets the style """
        self._style = value
    #----------------------------------------------------------------------
    @property
    def width(self):
        """ gets the width """
        return self._width
    #----------------------------------------------------------------------
    @width.setter
    def width(self, value):
        """ sets the width """
        self._width = value
    #----------------------------------------------------------------------
    @property
    def color(self):
        """ gets the color """
        return self._color
    #----------------------------------------------------------------------
    @color.setter
    def color(self, value):
        """ sets the color """
        if isinstance(value, (list, Color)):
            if value is list:
                self._color = value
            else:
                self._color = value.asList
    #----------------------------------------------------------------------
    def __str__(self):
        """ object as string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ object as dictionary """
        return {
            "type" : "esriSLS",
            "style" : self._style,
            "color" : self._color,
            "width" : self._width
        }
########################################################################
class SimpleFillSymbol(BaseSymbol):
    """
       Simple fill symbols can be used to symbolize polygon geometries. The
       type property for simple fill symbols is esriSFS.
    """
    allowed_style = ("esriSFSBackwardDiagonal",
                      "esriSFSCross",
                      "esriSFSDiagonalCross",
                      "esriSFSForwardDiagonal",
                      "esriSFSHorizontal",
                      "esriSFSNull",
                      "esriSFSSolid",
                      "esriSFSVertical")
    _type = "esriSFS"
    _style = None
    _color = None
    _outline = None
    #----------------------------------------------------------------------
    def __init__(self,
                 color,
                 style="esriSFSSolid",
                 outline=None
                 ):
        """Constructor"""
        if isinstance(color, (list, Color)):
            if color is list:
                self._color = color
            else:
                self._color = color.asList
        if isinstance(outline, SimpleLineSymbol):
            self._outline = outline.asDictionary
        self._style = style
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the symbol type """
        return self._type
    #----------------------------------------------------------------------
    @property
    def style(self):
        """ returns the style """
        return self._style
    #----------------------------------------------------------------------
    @style.setter
    def style(self, value):
        """ sets the style """
        self._style = value
    #----------------------------------------------------------------------
    @property
    def color(self):
        """ gets the color """
        return self._color
    #----------------------------------------------------------------------
    @color.setter
    def color(self, value):
        """ sets the color """
        if isinstance(value, (list, Color)):
            if value is list:
                self._color = value
            else:
                self._color = value.asList
    #----------------------------------------------------------------------
    @property
    def outline(self):
        """ gets the outline """
        return self._outline
    #----------------------------------------------------------------------
    @outline.setter
    def outline(self, value):
        """ sets the outline """
        if isinstance(value, SimpleLineSymbol):
            self._outline = value.asDictionary
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns object as string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns object as dictionary """
        template = {
            "type" : "esriSFS",
            "style" : self._style,
            "color" : self._color,
            "outline" : self._outline
        }
        return template
########################################################################
class PictureMarkerSymbol(BaseSymbol):
    """
       Picture marker symbols can be used to symbolize point geometries.
       The type property for picture marker symbols is esriPMS.
    """
    _type = "esriPMS"
    _url = None
    _imageDate = None
    _contentType = None
    _width = None
    _height = None
    _angle = None
    _xoffset = None
    _yoffset = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url=None,
                 imageData="",
                 contentType=None,
                 width=18,
                 height=18,
                 angle=0,
                 xoffset=0,
                 yoffset=0):
        """Constructor"""
        self._url = url
        self._imageDate = imageData
        self._contentType = contentType
        self._width = width
        self._height = height
        self._angle = angle
        self._xoffset = xoffset
        self._yoffset = yoffset
    @staticmethod
    def imageTobase64(path):
        """ converst an image to base 64 string """
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read())
    @staticmethod
    def base64ToImage(imgData, out_path, out_file):
        """ converts a base64 string to a file """
        fh = open(os.path.join(out_path, out_file), "wb")
        fh.write(imgData.decode('base64'))
        fh.close()
        del fh
        return os.path.join(out_path, out_file)
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the object as a string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a dictionary """
        template = {
            "type" : "esriPMS",
            "url" : self._url,
            "imageData" : self._imageDate,
            "contentType" : self._contentType,
            "width" : self._width,
            "height" : self._height,
            "angle" : self._angle,
            "xoffset" : self._xoffset,
            "yoffset" : self._yoffset
        }
        return template
########################################################################
class PictureFillSymbol(BaseSymbol):
    """
       Picture fill symbols can be used to symbolize polygon geometries.
       The type property for picture fill symbols is esriPFS.
    """
    _type = "esriPFS"
    _url = None
    _imageDate = None
    _contentType = None
    _width = None
    _height = None
    _angle = None
    _xoffset = None
    _yoffset = None
    _yscale = None
    _xscale = None
    _outline = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url=None,
                 imageData="",
                 contentType=None,
                 width=18,
                 height=18,
                 angle=0,
                 xoffset=0,
                 yoffset=0,
                 xscale=0,
                 yscale=0,
                 outline=None):
        """Constructor"""
        self._url = url
        self._imageDate = imageData
        self._contentType = contentType
        self._width = width
        self._height = height
        self._angle = angle
        self._xoffset = xoffset
        self._yoffset = yoffset
        self._xscale = xscale
        self._yscale = yscale
        if self._outline is not None and \
           self._outline is SimpleLineSymbol:
            self._outline = outline.asDictionary

    @staticmethod
    def imageTobase64(path):
        """ converst an image to base 64 string """
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read())
    @staticmethod
    def base64ToImage(imgData, out_path, out_file):
        """ converts a base64 string to a file """
        fh = open(os.path.join(out_path, out_file), "wb")
        fh.write(imgData.decode('base64'))
        fh.close()
        del fh
        return os.path.join(out_path, out_file)
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the object as a string """
        return json.dumps(self.asDictionary)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a dictionary """
        template = {
            "type" : "esriPMS",
            "url" : self._url,
            "imageData" : self._imageDate,
            "contentType" : self._contentType,
            "width" : self._width,
            "height" : self._height,
            "angle" : self._angle,
            "xoffset" : self._xoffset,
            "yoffset" : self._yoffset,
            "xscale" : self._xscale,
            "yscale" : self._yscale,
            "outline" : self._outline
        }
        return template