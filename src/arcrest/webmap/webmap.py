"""
   Core classes contained here to create the webmap data structure
"""
import json
from layers import *
########################################################################
class WebMap(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self,
                 baseMap=None,
                 operationalLayers=None,
                 bookmarks=None,
                 popupInfo=None,
                 version="1.7"):
        """Constructor"""
        pass




########################################################################
class BaseMap(object):
    """
       Basemaps give the web map a geographic context. In the web map, the
       basemaps are held in an array of baseMapLayer objects. Typically,
       you will use one basemap layer that is drawn beneath all other
       layers, but you can also add a basemap layer on top of all other
       layers to depict boundaries, labels, or a road network.
    """
    _baseMapLayers = None
    _json = None
    _dictionary = None
    _title = None
    #----------------------------------------------------------------------
    def __init__(self, title, baseMapLayers=[]):
        """Constructor"""
        self._baseMapLayers = baseMapLayers
        self._title = title
    #----------------------------------------------------------------------
    @property
    def title(self):
        """ returns the title of the basemap  """
        return self._title
    #----------------------------------------------------------------------
    @title.setter
    def title(self, title):
        """ sets the new title """
        self._title = title
    #----------------------------------------------------------------------
    @property
    def baseMapLayers(self):
        """ returns a list of base map layers """
        return self._baseMapLayers
    #----------------------------------------------------------------------
    def addBaseMapLayer(self, baseMapLayer):
        """ adds a base map layer """
        if isinstance(baseMapLayer, BaseMapLayer):
            self._baseMapLayers.append(baseMapLayer)
            return True
        else:
            return False
    #----------------------------------------------------------------------
    def removeBaseMapLayer(self, index):
        """ removes a basemap layer by index """
        if index > len(self._baseMapLayers):
            return False
        self._baseMapLayers.remove(self._baseMapLayers[index])
        return True
    #----------------------------------------------------------------------
    def __str__(self):
        """ returns the string JSON representation of the basemap """
        template = {
            "title" : self._title,
            "baseMapLayers" : self._baseMapLayers
        }
        return json.dumps(template)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the value as a dictionary """
        template = {
                    "title" : self._title,
                    "baseMapLayers" : [lyr.asDictionary for lyr in self._baseMapLayers]
                }
        return template
