"""
   Core classes contained here to create the webmap data structure
"""
import json
import types
from webmapobjects import *
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
        if isinstance(baseMap, (BaseMap, types.NoneType)):
            self._baseMap = baseMap
        else:
            raise TypeError('baseMap must be of type baseMap')

    def __str__(self):
        """returns object as string"""
        return ""
    def __iter__(self):
        pass