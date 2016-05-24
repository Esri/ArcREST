"""
Server Control Package
"""
from __future__ import absolute_import
from .server.ags import Catalog as AGSCatalog
from .manage import AGSAdministration
from .manage._services import Services

__all__ = ['AGSAdministration', 'AGSCatalog']
__version__ = "5.0.0"