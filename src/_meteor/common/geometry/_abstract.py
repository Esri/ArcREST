"""
"""
from __future__ import division
from __future__  import print_function
from __future__ import absolute_import
from abc import ABCMeta, abstractmethod
from six import with_metaclass
###########################################################################

class AbstractGeometry(with_metaclass(ABCMeta)):
    """Abstract base geometry"""
    def __init__(self):
        """initializer"""
        super(AbstractGeometry, self).__init__()
    @abstractmethod
    def __lt__(self, value):
        """determines if the values is less than another object"""
        raise NotImplementedError()
    @abstractmethod
    def __le__(self, value):
        """determines if the values is less than or equal to another object"""
        raise NotImplementedError()
    @abstractmethod
    def __gt__(self, value):
        """determines if the value object is greater than another object"""
        raise NotImplementedError()
    @abstractmethod
    def __ge__(self, value):
        """determines if the value object is greater than or equal to another object"""
        raise NotImplementedError()
    @abstractmethod
    def __eq__(self, value):
        """determines if the values is equal to other object"""
        raise NotImplementedError()
    @abstractmethod
    def __ne__(self, value):
        """determines if the values is not equal to other object"""
        raise NotImplementedError()
    @abstractmethod
    def __iter__(self):
        while False:
            yield None
    @abstractmethod
    def __str__(self):
        raise NotImplementedError()
    @abstractmethod
    def __geo_interface__(self):
        raise NotImplementedError()
    @classmethod
    @abstractmethod
    def from_json(value):
        """creates object from JSON string"""
        raise NotImplementedError()
    @property
    @abstractmethod
    def as_dict(self):
        """returns object as dictionary"""
        raise NotImplementedError()