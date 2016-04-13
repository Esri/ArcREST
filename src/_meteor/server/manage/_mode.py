from __future__ import absolute_import
from __future__ import print_function
from .._base import BaseServer
import json

class Mode(BaseServer):
    """
    ArcGIS Server site mode that allows you to control changes to your site.
    You can set the site mode to READ_ONLY to disallow the publishing of new
    services and block most administrative operations. Your existing services
    will continue to function as they did previously. Note that certain
    administrative operations such as adding and removing machines from a
    site are still available in READ_ONLY mode.
    """
    _url = None
    _con = None
    _json_dict = None
    _json = None
    _siteMode = None
    _copyConfigLocal = None
    _lastModified = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 connection,
                 initialize=False):
        """Constructor"""
        if url.lower().endswith('/mode'):
            self._url = url
        else:
            self._url = url + "/mode"
        self._con = connection
        if initialize:
            self.__init(connection)
    #----------------------------------------------------------------------
    def __init(self, connection=None):
        """ populates server admin information """
        params = {
            "f" : "json"
        }
        if connection:
            json_dict = connection.get(path_or_url=self._url,
                                       params=params)
        else:
            json_dict = self._con.get(path_or_url=self._url, params=params)
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                setattr(self, k,v)
            del k,v
    #----------------------------------------------------------------------
    @property
    def siteMode(self):
        """The current mode of the site. Response can be READ_ONLY or EDITABLE."""
        if self._siteMode is None:
            self.__init()
        return self._siteMode
    #----------------------------------------------------------------------
    @property
    def copyConfigLocal(self):
        """Whether the site configuration files will be copied to the local
        repository upon switching to READ_ONLY. Response can be true or false."""
        if self._copyConfigLocal is None:
            self.__init()
        return self._copyConfigLocal
    #----------------------------------------------------------------------
    @property
    def lastModified(self):
        """Time stamp indicating the last time the site mode was modified."""
        if self._lastModified is None:
            self.__init()
        return self._lastModified
