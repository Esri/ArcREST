import urllib
import json
import time
import datetime
from base import BaseAGSServer

########################################################################
class GPService(BaseAGSServer):
    """ An instasnce of a publish geoprocessing service """
    _url = None
    _username = None
    _password = None
    _token = None
    _token_url = None
    _currentVersion = None
    _resultMapServerName = None
    _tasks = None
    _executionType = None
    _maximumRecords = None
    _serviceDescription = None
    #----------------------------------------------------------------------
    def __init__(self, url, username=None, password=None, token_url=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        if username is not None and \
           password is not None and \
           token_url is not None:
            self._username = username
            self._password = password
            self._token_url = token_url
            self._token = self.generate_token()[0]
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the GP tools """
        params = {
            "f" : "json"
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(url=self._url, param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                if k == "tasks":
                    self._tasks = []
                    for t in v:
                        self._tasks.append(
                            GPTask(url=self._url + "/%s" % urllib.quote_plus(t),
                                              username=self._username,
                                              password=self._password,
                                              token_url=self._token_url)
                        )
                else:
                    setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented for gp service."

    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def resultMapServerName(self):
        """ returns the result mapserver name """
        if self._resultMapServerName is None:
            self.__init()
        return self._resultMapServerName
    #----------------------------------------------------------------------
    @property
    def tasks(self):
        """ returns the tasks in the GP service """
        if self._tasks is None:
            self.__init()
        return self._tasks
    #----------------------------------------------------------------------
    @property
    def executionType(self):
        """ returns the execution type """
        if self._executionType is None:
            self.__init()
        return self._executionType
    #----------------------------------------------------------------------
    @property
    def maximumRecords(self):
        """ the maximum number of rows returned from service """
        if self._maximumRecords is None:
            self.__init()
        return self._maximumRecords
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the service description """
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    #TODO - upload items
    def uploadItems(self):
        pass
    #TODO - upload information
    def uploadInfo(self):
        pass
    #TODO register Item
    def registerItem(self):
        pass
########################################################################
class GPTask(BaseAGSServer):
    """ This is the GP task that performs the operation """
    _token = None
    _username = None
    _password = None
    _token_url = None
    _url = None
    _category = None
    _displayName = None
    _name = None
    _parameters = None
    _executionType = None
    _helpUrl = None
    _description = None
    #----------------------------------------------------------------------
    def __init__(self, url, username=None, password=None, token_url=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        if username is not None and \
           password is not None and \
           token_url is not None:
            self._username = username
            self._password = password
            self._token_url = token_url
            self._token = self.generate_token()[0]
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(url=self._url, param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented."
    #----------------------------------------------------------------------
    @property
    def category(self):
        """ returns the category """
        if self._category is None:
            self.__init()
        return self._category
    #----------------------------------------------------------------------
    @property
    def displayName(self):
        """ returns the tools display name """
        if self._displayName is None:
            self.__init()
        return self._displayName
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ returns the name of the service """
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def parameters(self):
        """ returns the default parameters """
        if self._parameters is None:
            self.__init()
        return self._parameters
    #----------------------------------------------------------------------
    @property
    def executionType(self):
        """ returns the execution type """
        if self._executionType is None:
            self.__init()
        return self._executionType
    #----------------------------------------------------------------------
    @property
    def helpUrl(self):
        """ returns the help url """
        if self._helpUrl is None:
            self.__init()
        return self._helpUrl
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the description of the service """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    def getJob(self, jobID):
        """ returns the results or status of a job """
        url = self._url + "/jobs/%s" % (jobID)
        return GPJob(url=url,
                     username=self._username,
                     password=self._password,
                     token_url=self._token_url)

########################################################################
class GPJob(BaseAGSServer):
    """
       Represents an ArcGIS GeoProcessing Job
    """
    _jobId = None
    _messages = None
    _results = None
    _jobStatus = None
    _inputs = None
    #----------------------------------------------------------------------
    def __init__(self, url, username=None, password=None, token_url=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        if username is not None and \
           password is not None and \
           token_url is not None:
            self._username = username
            self._password = password
            self._token_url = token_url
            self._token = self.generate_token()[0]
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(url=self._url, param_dict=params)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print k, " - attribute not implmented for GPJob."
    #----------------------------------------------------------------------
    def cancelJob(self):
        """ cancels the job """
        params = {
            "f" : "json"
        }
        if self._token is not None:
            params['token'] = self._token
        return self._do_get(url=self._url + "/cancel", param_dict=params)
    #----------------------------------------------------------------------
    @property
    def messages(self):
        """ returns the messages """
        self.__init()
        return self._messages
    #----------------------------------------------------------------------
    @property
    def results(self):
        """ returns the results """
        self.__init()
        return self._results
    #----------------------------------------------------------------------
    @property
    def jobStatus(self):
        """ returns the job status """
        self.__init()
        return self._jobStatus
    #----------------------------------------------------------------------
    @property
    def jobId(self):
        """ returns the job ID """
        if self._jobId is None:
            self.__init()
        return self._jobId
    #----------------------------------------------------------------------
    @property
    def inputs(self):
        """ returns the inputs of a service """
        self.__init()
        return self._inputs
    #----------------------------------------------------------------------
    def getParameterValue(self, parameterName):
        """ gets a parameter value """
        if self._inputs is None:
            self.__init()
        parameter = self.inputs[parameterName]['paramUrl']
        paramURL = self._url + "/%s" % (parameter)
        params = {
            "f" : "json"
        }
        if self._token is not None:
            params['token'] = self._token

        return self._do_get(url=paramURL,
                            param_dict=params)



########################################################################
class GPString(object):
    """string object"""
    _value = None
    #----------------------------------------------------------------------
    def __init__(self, value):
        """Constructor"""
        if isinstance(value, str):
            self._value = value
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
    @property
    def value(self):
        """ returns the value"""
        return self._value
    @value.setter
    def value(self, value):
        """ sets the value"""
        if isinstance(value, str):
            self._value = value
########################################################################
class GPBoolean(object):
    """GP boolean object"""
    _value = None
    #----------------------------------------------------------------------
    def __init__(self, value):
        """Constructor"""
        if isinstance(value, bool):
            self._value = value
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
    @property
    def value(self):
        """ returns the value"""
        return self._value
    @value.setter
    def value(self, value):
        """ sets the value"""
        if isinstance(value, bool):
            self._value = value
########################################################################
class GPLong(object):
    """GP long object"""
    _value = None
    #----------------------------------------------------------------------
    def __init__(self, value):
        """Constructor"""
        if isinstance(value, int) or \
           isinstance(value, long):
            self._value = value
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
    @property
    def value(self):
        """ returns the value"""
        return self._value
    @value.setter
    def value(self, value):
        """ sets the value"""
        if isinstance(value, int) or \
           isinstance(value, long):
            self._value = value
########################################################################
class GPDouble(object):
    """GP double object"""
    _value = None
    #----------------------------------------------------------------------
    def __init__(self, value):
        """Constructor"""
        if isinstance(value, int) or \
           isinstance(value, long):
            self._value = float(value)
        elif isinstance(value, float):
            self._value = value
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the value"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """ sets the value"""
        if isinstance(value, int) or \
           isinstance(value, long):
            self._value = float(value)
        elif isinstance(value, float):
            self._value = value
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
########################################################################
class GPLinearUnit(object):
    """GP double object"""
    _value = None
    #----------------------------------------------------------------------
    def __init__(self, distance, units):
        """Constructor"""
        self._value = {"distance": distance,
                       "units" : units}
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the value"""
        return self._value
    #----------------------------------------------------------------------
    @property
    def units(self):
        """ returns the units """
        return self._value['units']
    #----------------------------------------------------------------------
    @units.setter
    def units(self, value):
        """ sets the units value """
        self._units['units'] = value
    #----------------------------------------------------------------------
    @property
    def distance(self):
        """ returns the distance value """
        return self._value['distance']
    #----------------------------------------------------------------------
    @distance.setter
    def distance(self, value):
        """ sets the distance value """
        if isinstance(value, (int, float, long)):
            self._value['distance'] = value
        else:
            raise AttributeError("Invalid input type of: %s" % type(value))
########################################################################
class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)
########################################################################
class GPDate(object):
    """GP date object"""
    from arcpy import time as arcpyTime

    _value = None
    _EPOCH = datetime.datetime(1970, 1, 1, tzinfo=UTC())
    #----------------------------------------------------------------------
    def __init__(self, dateObject):
        """Constructor"""
        if isinstance(dateObject, datetime.datetime):
            self._value = dateObject
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
    #----------------------------------------------------------------------
    def _timestamp(self):
        "Return POSIX timestamp as float"
        if self._value.tzinfo is None:
            return  int(time.mktime((self._value.year,
                                 self._value.month,
                                 self._value.day,
                                 self._value.hour,
                                 self._value.minute,
                                 self._value.second,
                                 -1, -1, -1)) + self._value.microsecond / 1e6) * 1000
        else:
            return int(self._value - self._EPOCH).total_seconds() * 1000
    @property
    def value(self):
        """ returns the value"""
        return self._timestamp()
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """ sets the value"""
        if isinstance(value, datetime.datetime):
            self._value = value
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
########################################################################
class GPFeatureRecordSetLayer(object):
    """
       Returns the GPFeatureRecordSetLayer
    """
    _json = None
    _dictionary = None

    #----------------------------------------------------------------------
    def __init__(self, json_string):
        """Constructor"""
        pass
########################################################################
class GPRecordSet(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass
########################################################################
class GPInputParameter(object):
    """ """
    _dataType = None
    _paramName = None
    _value = None
    _dict = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, value):
        """Constructor"""
        if isinstance(value, str):
            param = json.loads(value)
            self._dataType = param['dataType']
            self._paramName = param['paramName']
            self._value = param['value']
            self._json = value
            self._dict = param
        elif isinstance(value, dict):
            self._dataType = value['dataType']
            self._paramName = value['paramName']
            self._value = value['value']
            self._dict = value
            self._json = json.dumps(param)
        else:
            raise AttributeError("Invalid input, value must be string or dictionary")
    #----------------------------------------------------------------------
    def __dict__(self):
        """ returns the value as a dictionary """
        return self._dict
    #----------------------------------------------------------------------
    def __str__(self):
        """ return the class as a string """
        return self._json
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns the value as JSON """
        return self._json
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the value as dictionary """
        return self._dict
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """ returns the dataType """
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def paramName(self):
        """"""
        return self._paramName
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the value """
        return self._value












