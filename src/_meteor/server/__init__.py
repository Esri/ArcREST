"""
Server Control Package
"""
from __future__ import absolute_import
from .catalog import Catalog
from .manage import AGSAdministration
from .manage._services import Services

__all__ = ['AGSAdministration', 'Catalog']
__version__ = "4.0.0"