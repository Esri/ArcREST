"""
Server Control Package
"""
from __future__ import absolute_import
from .server import Catalog
from .manage import AGSAdministration

__all__ = ['AGSAdministration', 'Catalog']
__version__ = "4.0.0"