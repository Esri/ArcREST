"""
ArcGIS Server/AGOL Services
"""
from __future__ import absolute_import
from .geometryservice import GeometryService
from ._mapservice import MapService
from ._featureservice import FeatureService, FeatureLayer
from ._vectortile import VectorTileService
from ._imageservice import ImageService
from ._networkservice import NetworkService
from ._globeservice import GlobeService
from ._geocodeservice import GeocodeService
from ._geodataservice import GeoDataService
from ._mobileservice import MobileService
from ._sceneservice import SceneService
from . import geoprocessing

__version__ = "4.0.0"
__all__ = ['GeometryService', 'MapService',
           'FeatureService', 'FeatureLayer',
           'VectorTileService', 'ImageService',
           'NetworkService', 'GlobeService',
           'GeocodeService', 'GeoDataService',
           'MobileService', 'SceneService',
           'geoprocessing']