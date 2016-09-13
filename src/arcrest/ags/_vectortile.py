"""

.. module:: _vectortile.py
   :platform: Windows, Linux
   :synopsis: Represents functions/classes that represents a vector tile
              service.
.. moduleauthor:: Esri

"""
from __future__ import absolute_import
from __future__ import print_function
import tempfile
from .._abstract.abstract import BaseAGSServer
import json
########################################################################
class VectorTileService(BaseAGSServer):
    """
    The vector tile service resource represents a vector service published
    with ArcGIS Server. The resource provides information about the service
    such as the tile info, spatial reference, initial and full extents.
    """
    _con = None
    _url = None
    _json = None
    _json_dict = None
    _tileInfo = None
    _tiles = None
    _name = None
    _tileMap = None
    _maxScale = None
    _capabilities = None
    _defaultStyles = None
    _currentVersion = None
    _resourceInfo = None
    _initialExtent = None
    _maxzoom = None
    _fullExtent = None
    _minScale = None
    _type = None
    _exportTilesAllowed = None
    _url = None
    _proxy_port = None
    _proxy_host = None
    _securityHandler = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 initialize=False, proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        self._proxy_url= proxy_url
        self._proxy_port = proxy_port
        self._url = url
        self._securityHandler = securityHandler
        if initialize:
            self.init()
    #----------------------------------------------------------------------
    def init(self):
        """ loads the data into the class """
        params = {"f": "json"}
        json_dict = self._get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_port=self._proxy_port,
                                 proxy_url=self._proxy_url)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, v)
            else:
                setattr(self, k, v)
    #--------------------------------------------------------------------------
    @property
    def tileInfo(self):
        """gets the value tileInfo"""
        if self._tileInfo is None:
            self.init()
        return self._tileInfo
    #--------------------------------------------------------------------------
    @property
    def tiles(self):
        """gets the value tiles"""
        if self._tiles is None:
            self.init()
        return self._tiles
    #--------------------------------------------------------------------------
    @property
    def name(self):
        """gets the value name"""
        if self._name is None:
            self.init()
        return self._name
    #--------------------------------------------------------------------------
    @property
    def tileMap(self):
        """gets the value tileMap"""
        if self._tileMap is None:
            self.init()
        return self._tileMap
    #--------------------------------------------------------------------------
    @property
    def maxScale(self):
        """gets the value maxScale"""
        if self._maxScale is None:
            self.init()
        return self._maxScale
    #--------------------------------------------------------------------------
    @property
    def capabilities(self):
        """gets the value capabilities"""
        if self._capabilities is None:
            self.init()
        return self._capabilities
    #--------------------------------------------------------------------------
    @property
    def defaultStyles(self):
        """gets the value defaultStyles"""
        if self._defaultStyles is None:
            self.init()
        return self._defaultStyles
    #--------------------------------------------------------------------------
    @property
    def currentVersion(self):
        """gets the value currentVersion"""
        if self._currentVersion is None:
            self.init()
        return self._currentVersion
    #--------------------------------------------------------------------------
    @property
    def resourceInfo(self):
        """gets the value resourceInfo"""
        if self._resourceInfo is None:
            self.init()
        return self._resourceInfo
    #--------------------------------------------------------------------------
    @property
    def initialExtent(self):
        """gets the value initialExtent"""
        if self._initialExtent is None:
            self.init()
        return self._initialExtent
    #--------------------------------------------------------------------------
    @property
    def maxzoom(self):
        """gets the value maxzoom"""
        if self._maxzoom is None:
            self.init()
        return self._maxzoom
    #--------------------------------------------------------------------------
    @property
    def fullExtent(self):
        """gets the value fullExtent"""
        if self._fullExtent is None:
            self.init()
        return self._fullExtent
    #--------------------------------------------------------------------------
    @property
    def minScale(self):
        """gets the value minScale"""
        if self._minScale is None:
            self.init()
        return self._minScale
    #--------------------------------------------------------------------------
    @property
    def type(self):
        """gets the value type"""
        if self._type is None:
            self.init()
        return self._type
    #--------------------------------------------------------------------------
    @property
    def exportTilesAllowed(self):
        """gets the value exportTilesAllowed"""
        if self._exportTilesAllowed is None:
            self.init()
        return self._exportTilesAllowed
    #----------------------------------------------------------------------
    @property
    def styles(self):
        url = "{url}/styles".format(url=self._url)
        params = {"f" : "json"}
        return self._get(url=url,
                         param_dict=params,
                         securityHandler=self._securityHandler,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_host)
    #----------------------------------------------------------------------
    def tile_fonts(self, fontstack, stack_range, out_folder=None):
        """This resource returns glyphs in PBF format. The template url for
        this fonts resource is represented in Vector Tile Style resource."""
        url = "{url}/resources/fonts/{fontstack}/{stack_range}.pbf".format(
            url=self._url,
            fontstack=fontstack,
            stack_range=stack_range)
        params = {}
        if out_folder is None:
            out_folder = tempfile.gettempdir()
        return self._get(url=url,
                         param_dict=params,
                         out_folder=out_folder,
                         securityHandler=self._securityHandler,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_host)
    #----------------------------------------------------------------------
    def vector_tile(self, level, row, column, out_folder=None):
        """This resource represents a single vector tile for the map. The
        bytes for the tile at the specified level, row and column are
        returned in PBF format. If a tile is not found, an HTTP status code
        of 404 (Not found) is returned."""
        url = "{url}/tile/{level}/{row}/{column}.pdf".format(url=self._url,
                                                             level=level,
                                                             row=row,
                                                             column=column)
        params = {}
        if out_folder is None:
            out_folder = tempfile.gettempdir()
        return self._get(url=url,
                         param_dict=params,
                         out_folder=out_folder,
                         securityHandler=self._securityHandler,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_host)
    #----------------------------------------------------------------------
    def tile_sprite(self, out_format="sprite.json", out_folder=None):
        """
        This resource returns sprite image and metadata
        """
        url = "{url}/resources/sprites/{f}".format(url=self._url,
                                                   f=out_format)
        if out_folder is None:
            out_folder = tempfile.gettempdir()
        return self._get(url=url,
                         param_dict={},
                         out_folder=out_folder,
                         securityHandler=self._securityHandler,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_host)
    #----------------------------------------------------------------------
    @property
    def info(self):
        """This returns relative paths to a list of resource files"""
        url = "{url}/resources/info".format(url=self._url)
        params = {"f" : "json"}
        return self._get(url=url,
                         param_dict=params,
                         securityHandler=self._securityHandler,
                         proxy_port=self._proxy_port,
                         proxy_url=self._proxy_host)