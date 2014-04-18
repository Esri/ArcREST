"""
   Contains all the information regarding the layers that can be created in
   the ArcGIS Webmap JSON
"""
import base
import json
########################################################################
class KMZLayer(base.BaseOperationalLayer):
    """
       Reprsents a KMZ/KML operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class WMSLayer(base.BaseOperationalLayer):
    """
       Reprsents a WMS operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class CSVLayer(base.BaseOperationalLayer):
    """
       Reprsents a CSV operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class MapNotesLayer(base.BaseOperationalLayer):
    """
       Reprsents a Map Notes operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class FeatureCollectionLayer(base.BaseOperationalLayer):
    """
       Reprsents a Feature Collection operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class AGSFeatureServiceLayer(base.BaseOperationalLayer):
    """
       Reprsents a AGS Feature Service operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class AGSMapServiceLayer(base.BaseOperationalLayer):
    """
       Reprsents a AGS Map Service operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class AGOLLayer(base.BaseOperationalLayer):
    """
       Reprsents a AGOL service operational layer
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class BaseMapLayer(object):
    """
       A basemap layer is a layer that provides geographic context to the
       map. The web map contains an array of baseMapLayer objects. The
       isReference property determines whether the layer is drawn on top of
       all operational layers (true) or below them (false). Basemap layers
       cannot be drawn between operational layers.
       All basemap layers used in a web map need to have the same spatial
       reference and tiling scheme. All operational layers in the map are
       drawn or requested in the spatial reference of the basemap layers.
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the basemap layer as a string """
        return ""
    #----------------------------------------------------------------------
    def __dict__(self):
        """ returns the object as a dictionary """
        return {}







if __name__ == "__main__":
    print BaseMap(title="test").__dict__()
    print str(BaseMap(title="test"))



