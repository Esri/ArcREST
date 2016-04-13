"""

.. module:: _vectortile.py
   :platform: Windows, Linux
   :synopsis: Represents functions/classes that represents a vector tile
              service.
.. moduleauthor:: Esri

"""
from __future__ import absolute_import
import json
import tempfile
from ..connection import SiteConnection
from ._base import BaseService
########################################################################
class VectorTileService(BaseService):
    """
    The vector tile service resource represents a vector service published
    with ArcGIS Server. The resource provides information about the service
    such as the tile info, spatial reference, initial and full extents.
    """
    _con = None
    _url = None
    #----------------------------------------------------------------------
    @property
    def styles(self):
        url = "{url}/styles".format(url=self._url)
        params = {"f" : "json"}
        return self._con.get(path_or_url=url, params=params)
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
        return self._con.get(path_or_url=url,
                             params=params,
                             out_folder=out_folder)
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
        return self._con.get(path_or_url=url,
                             params=params,
                             out_folder=out_folder)
    #----------------------------------------------------------------------
    def tile_sprite(self, out_format="sprite.json", out_folder=None):
        """
        This resource returns sprite image and metadata
        """
        url = "{url}/resources/sprites/{f}".format(url=self._url,
                                                   f=out_format)
        if out_folder is None:
            out_folder = tempfile.gettempdir()
        return self._con.get(path_or_url=url,
                             params={},
                             out_folder=out_folder)
    #----------------------------------------------------------------------
    @property
    def info(self):
        """This returns relative paths to a list of resource files"""
        url = "{url}/resources/info".format(url=self._url)
        params = {"f" : "json"}
        return self._con.get(path_or_url=url,
                             params=params)