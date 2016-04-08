from __future__ import absolute_import
import json
from six.moves.urllib_parse import urlparse, urlunparse

class Portal(object):
    """

    """
    _con = None
    _root = None
    _generateToken = None
    def __init__(self, url, connection):
        """initializer"""
        self._con = connection
        self._root = self._validate_url(url)
        self._generateToken = "{root}/generateToken".format(root=self._root)
        self.__init() # loads properties @ runtime
    #----------------------------------------------------------------------
    def _validate_url(self, url):
        """ensures proper URL validation"""
        parsed = urlparse(url)
        if parsed.scheme == "":
            url = "https://{}".format(url)
            parsed = urlparse(url)
        path = parsed.path
        if path.strip() == '':
            return "{}/sharing/rest".format(url)
        elif path.strip().lower().find('/sharing/rest') > -1:
            return url
        if path.strip().lower().find('/sharing/') < -1:
            url = "{netloc}/{path}/sharing".format(netloc=parsed.netloc, path=path)
            url = self._validate_url(url=url)
        if path.strip().lower().find('/rest') < -1:
            url = "{netloc}/{path}/rest".format(netloc=parsed.netloc, path=path)
        return url
    #----------------------------------------------------------------------
    def __init(self):
        result = self._con.get(url=self._root, param_dict=params)
        if isinstance(result, dict):
            for k,v in result.items():
                setattr(self, k, v)
                del k,v
        elif isinstance(result, str):
            setattr(self, "error", result)



