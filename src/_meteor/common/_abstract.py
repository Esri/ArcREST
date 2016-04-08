from collections import OrderedDict
import six
from .web._base import BaseWebOperations
########################################################################
class BaseSecurityHandler(BaseWebOperations):
    """ All Security Objects inherit from this class """
    _token = None
    _valid = True
    _message = ""
    _is_portal = False
    #----------------------------------------------------------------------
    @property
    def message(self):
        """ returns any messages """
        return self._message
    #----------------------------------------------------------------------
    @property
    def valid(self):
        """ returns boolean wether handler is valid """
        return self._valid
########################################################################
class BaseServiceMap(OrderedDict):
    _map = None
    #----------------------------------------------------------------------
    def __init__(self, value=None):
        """Initializer object"""
        self.__init(value=value)
    #----------------------------------------------------------------------
    def __init(self, value):
        self._map = OrderedDict()
        if value:
            if isinstance(value, dict):
                for k,v in six.iteritems(value):
                    if isinstance(v, dict):
                        v = BaseServiceMap(value=v)
                    self._map[k] = v
                    del k,v
    #----------------------------------------------------------------------
    def items(self):
        return six.iteritems(self._map)
    #----------------------------------------------------------------------
    def iteritems(self):
        return six.iteritems(self._map)
    #----------------------------------------------------------------------
    def __iter__(self):
        return self._map.__iter__()
    #----------------------------------------------------------------------
    def next(self):
        return self._map.next()
    #----------------------------------------------------------------------
    def __setitem__(self, k, v):
        self._map[k] = v
    #----------------------------------------------------------------------
    def __getitem__(self, k):
        if k not in self._map:
            # if parameter k DNE, create a empty object as BaseServiceMap
            self[k] = BaseServiceMap()
        return self._map[k]
    #----------------------------------------------------------------------
    def __setattr__(self, k, v):
        if k == '_map':
            super(BaseServiceMap, self).__setattr__(k,v)
        else:
            self[k] = v
    #----------------------------------------------------------------------
    def __getattr__(self, k):
        if k == '_map':
            super(BaseServiceMap, self).__getattr__(k)
        else:
            return self[k]
    #----------------------------------------------------------------------
    def __delattr__(self, key):
        return self._map.__delitem__(key)
    #----------------------------------------------------------------------
    def __contains__(self, k):
        return self._map.__contains__(k)
    #----------------------------------------------------------------------
    def __str__(self):
        """represents the object as a string"""
        return json.dumps(self.as_dictionary())
    #----------------------------------------------------------------------
    def __repr__(self):
        return str(self)
    #----------------------------------------------------------------------
    def __geo_interface__(self):
        """"""
        raise NotImplementedError("__geo_interface__() is not implmented on this service")
    #----------------------------------------------------------------------
    def as_dictionary(self, publicOnly=True):
        """
        recursively iterate the object inorder to conver the BaseServiceMap object
        to a traditional dictionary type object.

        """
        vals = {}
        for k,v in self.items():
            if publicOnly:
                if k[0].find("_") < 0:
                    if type(v) is BaseServiceMap:
                        vals[k] = v.as_dictionary()
                    else:
                        vals[k] = v
            else:
                if type(v) is BaseServiceMap:
                    vals[k] = v.as_dictionary()
                else:
                    vals[k] = v
            del k,v
        return vals
    #----------------------------------------------------------------------
    def values(self):
        return self._map.values()
    #----------------------------------------------------------------------
    def __cmp__(self, value):
        value = BaseServiceMap.compare(value)
        return self._map.__cmp__(value)
    #----------------------------------------------------------------------
    def __eq__(self, value):
        value = BaseServiceMap.compare(value)
        if not isinstance(value, dict):
            return False
        return self._map.__eq__(value)
    #----------------------------------------------------------------------
    def __ge__(self, value):
        value = BaseServiceMap.compare(value)
        return self._map.__ge__(value)
    #----------------------------------------------------------------------
    def __gt__(self, value):
        value = BaseServiceMap.compare(value)
        return self._map.__gt__(value)
    #----------------------------------------------------------------------
    def __le__(self, value):
        value = BaseServiceMap.compare(value)
        return self._map.__le__(value)
    #----------------------------------------------------------------------
    def __lt__(self, value):
        value = BaseServiceMap.compare(value)
        return self._map.__lt__(value)
    #----------------------------------------------------------------------
    def __ne__(self, value):
        value = BaseServiceMap.compare(value)
        return self._map.__ne__(value)
    #----------------------------------------------------------------------
    def __delitem__(self, key):
        return self._map.__delitem__(key)
    #----------------------------------------------------------------------
    def __len__(self):
        return self._map.__len__()
    #----------------------------------------------------------------------
    def clear(self):
        self._map.clear()
    #----------------------------------------------------------------------
    def copy(self):
        return copy.deepcopy(self)
    #----------------------------------------------------------------------
    def get(self, key, default=None):
        return self._map.get(key, default)
    #----------------------------------------------------------------------
    def has_key(self, key):
        return key in self._map
    #----------------------------------------------------------------------
    def iterkeys(self):
        return self._map.iterkeys()
    #----------------------------------------------------------------------
    def itervalues(self):
        return self._map.itervalues()
    #----------------------------------------------------------------------
    def keys(self):
        return self._map.keys()
    #----------------------------------------------------------------------
    def pop(self, key, default=None):
        return self._map.pop(key, default)
    #----------------------------------------------------------------------
    def popitem(self):
        return self._map.popitem()
    #----------------------------------------------------------------------
    def setdefault(self, key, default=None):
        self._map.setdefault(key, default)
    #----------------------------------------------------------------------
    def update(self, *args, **kwargs):
        if len(args) != 0:
            self._map.update(*args)
        self._map.update(kwargs)
    #----------------------------------------------------------------------
    def viewitems(self):
        return self._map.viewitems()
    #----------------------------------------------------------------------
    def viewkeys(self):
        return self._map.viewkeys()
    #----------------------------------------------------------------------
    def viewvalues(self):
        return self._map.viewvalues()
    #----------------------------------------------------------------------
    @classmethod
    def fromkeys(cls, seq, value=None):
        """
        creates a BaseServiceMap object from a set of keys with default values
        This allows the creation of template objects.
        """
        val = BaseServiceMap()
        val._map = OrderedDict.fromkeys(seq, value)
        return val
    #----------------------------------------------------------------------
    @classmethod
    def compare(self, value):
        if type(value) is BaseServiceMap:
            return value._map
        else:
            return value

