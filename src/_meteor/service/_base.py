from __future__ import absolute_import
import json
###########################################################################
class BaseService(object):
    _url = None
    _con = None
    _json_dict = None
    def __init__(self, connection, url, initialize=False):
        """constructor"""
        self._con = connection
        self._url = url
        self._json_dict = None
        if initialize:
            self.__init(connection)
    #----------------------------------------------------------------------
    def __init(self, connection):
        """loads the properties"""
        params = {"f" : "json"}
        result = connection.get(path_or_url=self._url, params=params)
        if isinstance(result, dict):
            self._json_dict = result
            for k,v in result.items():
                setattr(self, k, v)
                del k,v
        else:
            raise RuntimeError("Could not connect to the service: %s" % result)
    #----------------------------------------------------------------------
    def refresh(self):
        """reloads all the services properties"""
        self.__init(connection=self._con)
    #----------------------------------------------------------------------
    def __str__(self):
        """object as string"""
        if self._json_dict is None:
            self.__init(connection=self._con)
        return json.dumps(self._json_dict)
    #----------------------------------------------------------------------
    def __repr__(self):
        """representation object"""
        return "{classtype}({data})".format(
            classtype=self.__class__.__name__,
            data=self.__str__())
    #----------------------------------------------------------------------
    def __iter__(self):
        """creates iterable for classes properties"""
        for k,v in self.__dict__.items():
            yield k,v

