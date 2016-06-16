"""
Geometry package contains all the objects that create and manage geometries
"""
from __future__ import absolute_import
from ._spatialreference import SpatialReference
from ._point import Point
from ._multipoint import MultiPoint
from ._polyline import Polyline
from ._polygon import Polygon
from ._envelope import Envelope
__version__ = "4.0.0"
__all__ = ['Envelope', 'Point', 'MultiPoint',
           'Polygon', 'Polyline', 'SpatialReference']