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

        self._operationalLayers = operationalLayers


        self._version = version

    def __str__(self):
        """returns object as string"""
        return ""
    def __iter__(self):
        pass

    @property
    def asDictionary(self):
        """ dictionary representation of the object """
        value_dict = {
            "version":self._version
        }

        if self._operationalLayers != None:
            value_dict['operationalLayers'] = self._operationalLayers 

        if self._baseMap != None:
            value_dict['baseMap'] = self._baseMap

        return value_dict

    def __str__(self):
        d = self.asDictionary

        if d.has_key('baseMap'):
            d['baseMap'] = json.loads(str(d['baseMap']))

        if d.has_key('operationalLayers'):
            d['operationalLayers'] = [ json.loads(str(l)) for l in d['operationalLayers']]

        return json.dumps(d)

