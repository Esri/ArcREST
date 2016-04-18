from __future__ import absolute_import
import json
###########################################################################
class BaseService(object):
    _url = None
    _con = None
    _json_dict = None
    #----------------------------------------------------------------------
    def __str__(self):
        return json.dumps(self._json_dict)
    #----------------------------------------------------------------------
    @property
    def as_dict(self):
        return self._json_dict
    #----------------------------------------------------------------------
    def __repr__(self):
        return self.__str__()
    #----------------------------------------------------------------------
    def __iter__(self):
        """iterator"""
        if self._json_dict is None:
            yield None
        else:
            for k,v in self._json_dict.items():
                yield k,v

