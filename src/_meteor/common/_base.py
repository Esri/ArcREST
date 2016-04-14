""" BaseDict is a subclass of dict with attribute-style access.

    >>> b = BaseDict()
    >>> b.hello = 'world'
    >>> b.hello
    'world'
    >>> b['hello'] += "!"
    >>> b.hello
    'world!'
    >>> b.foo = BaseDict(lol=True)
    >>> b.foo.lol
    True
    >>> b.foo is b['foo']
    True

    It is safe to import * from this module:

        __all__ = ('BaseDict', 'munchify','unmunchify')

    un/munchify provide dictionary conversion; Munches can also be
    converted via BaseDict.to/fromDict().
"""
from .packages import six
import json

__version__ = '4.0.0'

__all__ = ('BaseDict')


########################################################################
class BaseDict(dict):
    """
    A dictionary that provides attribute-style access.
    """
    #----------------------------------------------------------------------
    def __str__(self):
        p = {}
        for k,v in six.iteritems(self):
            if k[0] != "_":
                p[k] = v
        return json.dumps(p)
    #----------------------------------------------------------------------
    def __getattr__(self, k):
        """
        Gets key if it exists, otherwise throws AttributeError.
        """
        try:
            # Throws exception if not in prototype chain
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)
    #----------------------------------------------------------------------
    def __setattr__(self, k, v):
        """ Sets attribute k if it exists, otherwise sets key k. A KeyError
            raised by set-item (only likely if you subclass BaseDict) will
            propagate as an AttributeError instead.
        """
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                self[k] = v
            except:
                raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)
    #----------------------------------------------------------------------
    def __delattr__(self, k):
        """ Deletes attribute k if it exists, otherwise deletes key k. A KeyError
            raised by deleting the key--such as when the key is missing--will
            propagate as an AttributeError instead.
        """
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)
    #----------------------------------------------------------------------
    @property
    def toDict(self):
        """
        Recursively converts a BaseDict back into a dictionary.
        """
        return self._obj_to_dict(self)
    #----------------------------------------------------------------------
    def __repr__(self):
        """
        String-form of a BaseDict.
        """
        return '%s(%s)' % (self.__class__.__name__, dict.__repr__(self))
    #----------------------------------------------------------------------
    def __dir__(self):
        return list(six.iterkeys(self))
    #----------------------------------------------------------------------
    __members__ = __dir__  # for python2.x compatibility
    #----------------------------------------------------------------------
    @staticmethod
    def fromDict(d):
        """
        Transforms a dictionary into a BaseDict via copy.
        """
        return BaseDict._dict_to_obj(d)
    #----------------------------------------------------------------------
    @staticmethod
    def _dict_to_obj(x):
        """
        Transforms a dictionary into a BaseDict via copy.
        """
        if isinstance(x, dict):
            return BaseDict((k, BaseDict._dict_to_obj(v)) for k, v in six.iteritems(x))
        elif isinstance(x, (list, tuple)):
            return type(x)(BaseDict._dict_to_obj(v) for v in x)
        else:
            return x
    #----------------------------------------------------------------------
    @staticmethod
    def _obj_to_dict(x):
        """ Recursively converts a BaseDict into a dictionary.
        """
        if isinstance(x, dict):
            return dict((k, BaseDict._obj_to_dict(v)) for k, v in six.iteritems(x))
        elif isinstance(x, (list, tuple)):
            return type(x)(BaseDict._obj_to_dict(v) for v in x)
        else:
            return x
