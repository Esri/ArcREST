from __future__ import absolute_import
from ._base import BaseService
from ..connection import SiteConnection
import json

########################################################################
class MobileService(BaseService):
    """
    Represents a single globe layer
    """
    _url = None
    _json_dict = None
    _con = None