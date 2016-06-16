"""

"""

from __future__ import absolute_import
from __future__ import print_function
import json
try:
    import arcpy
    arcpyFound = True
except ImportError:
    arcpyFound = False

########################################################################
class SpatialReference(object):
    """ creates a spatial reference instance
    A spatial reference can be defined using a well-known ID (wkid) or
    well-known text (wkt). The default tolerance and resolution values for
    the associated coordinate system are used. The xy and z tolerance
    values are 1 mm or the equivalent in the unit of the coordinate system.
    If the coordinate system uses feet, the tolerance is 0.00328083333 ft.
    The resolution values are 10x smaller or 1/10 the tolerance values.
    Thus, 0.0001 m or 0.0003280833333 ft. For geographic coordinate systems
    using degrees, the equivalent of a mm at the equator is used.
    The well-known ID (WKID) for a given spatial reference can occasionally
    change. For example, the WGS 1984 Web Mercator (Auxiliary Sphere)
    projection was originally assigned WKID 102100, but was later changed
    to 3857. To ensure backward compatibility with older spatial data
    servers, the JSON wkid property will always be the value that was
    originally assigned to an SR when it was created.
    An additional property, latestWkid, identifies the current WKID value
    (as of a given software release) associated with the same spatial
    reference.
    A spatial reference can optionally include a definition for a vertical
    coordinate system (VCS), which is used to interpret the z-values of a
    geometry. A VCS defines units of measure, the location of z = 0, and
    whether the positive vertical direction is up or down. When a vertical
    coordinate system is specified with a WKID, the same caveat as mentioned
    above applies. There are two VCS WKID properties: vcsWkid and
    latestVcsWkid. A VCS WKT can also be embedded in the string value of
    the wkt property. In other words, the WKT syntax can be used to define
    an SR with both horizontal and vertical components in one string. If
    either part of an SR is custom, the entire SR will be serialized with
    only the wkt property.
    Starting at 10.3, Image Service supports image coordinate systems

    Parameters
     :wkid: well known id
     :wkt: well known text
     :latestWkid: the latest/current WKID
     :vcswkid: Well known id for a vertical coordinate system
     :lastestVcsWkid: the latest/current WKID for vertical coordinate
      systems
    """
    _wkid = None
    _wkt = None
    _latestWkid = None
    _vcswkid = None
    _latestVcsWkid = None
    #----------------------------------------------------------------------
    def __init__(self, wkid=None,
                 wkt=None, latestWkid=None,
                 vcswkid=None, lastestVcsWkid=None):
        """Constructor"""
        if wkid is None and wkt is None:
            raise ValueError("A WKT or WKID must be given.")
        self._wkid = wkid
        self._wkt = wkt
        self._latestWkid = latestWkid
        self._vcswkid = vcswkid
        self._latestVcsWkid = lastestVcsWkid
    #----------------------------------------------------------------------
    def __str__(self):
        """object as string"""
        return json.dumps(self.as_dict)
    #----------------------------------------------------------------------
    @property
    def lastestVcsWkid(self):
        """ get/set the lastestVcsWkid """
        return self._latestVcsWkid
    #----------------------------------------------------------------------
    @lastestVcsWkid.setter
    def lastestVcsWkid(self, value):
        """ get/set the lastestVcsWkid """
        self._latestVcsWkid = value
    #----------------------------------------------------------------------
    @property
    def vcswkid(self):
        """ get/set the vcswkid """
        return self._vcswkid
    #----------------------------------------------------------------------
    @vcswkid.setter
    def vcswkid(self, value):
        """ get/set the latestWkid """
        self._vcswkid = value
    #----------------------------------------------------------------------
    @property
    def latestWkid(self):
        """ get/set the latestWkid """
        return self._wkid
    #----------------------------------------------------------------------
    @latestWkid.setter
    def latestWkid(self, latestWkid):
        """ get/set the latestWkid """
        self._latestWkid = latestWkid
    #----------------------------------------------------------------------
    @property
    def wkid(self):
        """ get/set the wkid """
        return self._wkid
    #----------------------------------------------------------------------
    @wkid.setter
    def wkid(self, wkid):
        """ get/set the wkid """
        self._wkid = wkid
    #----------------------------------------------------------------------
    @property
    def wkt(self):
        """ get/set the wkt """
        return self._wkt
    #----------------------------------------------------------------------
    @wkt.setter
    def wkt(self, wkt):
        """ get/set the wkt """
        self._wkt = wkt
    #----------------------------------------------------------------------
    @property
    def as_dict(self):
        """returns the wkid id for use in json calls"""
        return self.value
    #----------------------------------------------------------------------
    @property
    def as_arcpy(self):
        """returns an arcpy.SpatialReference object"""
        if arcpyFound:
            if self.wkid:
                return arcpy.SpatialReference(self.wkid)
            else:
                return arcpy.SpatialReference(text=self.wkt)
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the wkid id for use in json calls"""
        if self._wkid:
            template = {}
            keys = ['wkid', 'latestWkid', 'vcsWkid', 'latestVcsWkid']
            for key in keys:
                value = getattr(self, "_%s" % key, None)
                if value:
                    template[key] = value
                del key, value
            del keys
            return template
        else:
            return {
                "wkt" : self._wkt
            }
    @staticmethod
    def from_json(value):
        if isinstance(value, str):
            value = json.loads(value)
        if isinstance(value, dict):
            return (SpatialReference(**value))
        return None