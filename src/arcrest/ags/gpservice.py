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
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._url = url
        if username is not None and \
           password is not None and \
           token_url is not None:
            self._username = username
            self._password = password
            self._token_url = token_url
            if not username is None and \
             not password is None and \
             not username is "" and \
             not password is "":
                if not token_url is None:
                    res = self.generate_token(tokenURL=token_url,
                                                  proxy_port=proxy_port,
                                                proxy_url=proxy_url)
                else:   
                    res = self.generate_token(proxy_port=self._proxy_port,
                                                           proxy_url=self._proxy_url)                
                if res is None:
                    print "Token was not generated"
                elif 'error' in res:
                    print res
                else:
                    self._token = res[0]
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
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._url = url
        if username is not None and \
           password is not None and \
           token_url is not None:
            self._username = username
            self._password = password
            self._token_url = token_url
            if not username is None and \
             not password is None and \
             not username is "" and \
             not password is "":
                if not token_url is None:
                    res = self.generate_token(tokenURL=token_url,
                                                  proxy_port=proxy_port,
                                                proxy_url=proxy_url)
                else:   
                    res = self.generate_token(proxy_port=self._proxy_port,
                                                           proxy_url=self._proxy_url)                
                if res is None:
                    print "Token was not generated"
                elif 'error' in res:
                    print res
                else:
                    self._token = res[0]
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
            if k == "parameters":
                self._parameters = []
                for param in v:
                    self._parameters.append(
                        GPInputParameterInfo(param, True)
                    )
                    del param
            elif k in attributes:
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
    #----------------------------------------------------------------------
    def submitJob(self, inputs, method="GET",
                  returnZ=False, returnM=False):
        """
           submits a job to the current task, and returns a job ID
           Inputs:
              inputs - dictionary - value should be a Key/Value list of GP
                       objects that line up with the input names.
              method - string - either GET or POST.  The way the service is
                       submitted.
           Ouput:
              JOB ID as a string
        """
        url = self._url + "/submitJob"
        params = { "f" : "json" }
        params['returnZ'] = returnZ
        params['returnM'] = returnM
        if self._token is not None:
            params['token'] = self._token
        for k in inputs:
            params[k] = inputs[k]
        if method.lower() == "get":
            return self._do_get(url=url, param_dict=params)
        elif method.lower() == "post":
            return self._do_post(url=url, param_dict=params)
        else:
            raise AttributeError("Invalid input: %s. Must be GET or POST" \
                                 % method)

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
                 initialize=False, proxy_url=None, proxy_port=None):
        """Constructor"""
        self._url = url
        if username is not None and \
           password is not None and \
           token_url is not None:
            self._username = username
            self._password = password
            self._token_url = token_url
            if not username is None and \
             not password is None and \
             not username is "" and \
             not password is "":
                if not token_url is None:
                    res = self.generate_token(tokenURL=token_url,
                                                  proxy_port=proxy_port,
                                                proxy_url=proxy_url)
                else:   
                    res = self.generate_token(proxy_port=self._proxy_port,
                                                           proxy_url=self._proxy_url)                
                if res is None:
                    print "Token was not generated"
                elif 'error' in res:
                    print res
                else:
                    self._token = res[0]
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
        elif isinstance(dateObject, long):
            self._value = dateObject
        else:
            raise AttributeError("Invalid Input of type: %s" % type(dateObject))
    #----------------------------------------------------------------------
    def _timestamp(self):
        "Return POSIX timestamp as float"
        if isinstance(self._value, long):
            return self._value
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
        elif isinstance(value, long):
            self._value = value
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
########################################################################
class GPDataFile(object):
    """ represents a data file object for GP task """

    #----------------------------------------------------------------------
    def __init__(self, json_value):
        """Constructor"""
        pass
########################################################################
class GPFeatureRecordSetLayer(object):
    """
       Returns the GPFeatureRecordSetLayer
    """
    _json = None
    _dictionary = None

    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        """Constructor"""
        pass
########################################################################
class GPRecordSet(object):
    """"""
    _fields = None
    _features = None
    _exceededTransferLimit = None
    _displayFieldName = None
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        """Constructor
           Inputs:
              json_dict - dictionary representation of the GPRecordSet
              -- or --
              features - list of rows
              displayFieldname - primary display field
              fields - list of dictionaries describing the fields
        """
        if "json_dict" in kwargs and \
           kwargs['json_dict'] is not None:
            json_dict = kwargs['json_dict']
            self._fields = json_dict['fields']
            self._exceededTransferLimit = json_dict['exceededTransferLimit']
            self._features = json_dict['features']
            self._displayFieldName = json_dict['displayFieldName']
        elif "features" in kwargs and \
             "fields" in kwargs:
            self._fields = kwargs['fields']
            self._features = kwargs['features']
            if "displayFieldName" in kwargs:
                self._displayFieldName = kwargs['displayFieldName']
            else:
                self._displayFieldName = ""
            if "exceededTransferLimit" in kwargs:
                self._exceededTransferLimit = kwargs['exceededTransferLimit']
            else:
                self._exceededTransferLimit = False
        else:
            raise AttributeError("Invalid Inputs, please consult the documentation")
        pass
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """ returns the fields for the GPRecordSet """
        return self._fields
    #----------------------------------------------------------------------
    @property
    def features(self):
        """ returns the rows in the recordset """
        return self._features
    #----------------------------------------------------------------------
    @property
    def displayFieldName(self):
        """ returns the displayField Name """
        return self._displayFieldName
    #----------------------------------------------------------------------
    @property
    def exceededTransferLimit(self):
        """ returns the value for exceededTransferLimit property """
        return self._exceededTransferLimit
    #----------------------------------------------------------------------
    def addRecord(self, row):
        """ adds a dictionary value to the features list """
        if self._features is None:
            self._features = []
        if isinstance(row, dict):
            self._features.append(row)
            return True
        return False
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the value as a dictionary """
        return {
            "fields" : self._fields,
            "features" : self._features,
            "exceededTransferLimit" : self._exceededTransferLimit,
            "displayFieldName" : self._displayFieldName
        }
########################################################################
class GPMultiValue(object):
    """ reprsents the GP MultiValue Object """

    #----------------------------------------------------------------------
    def __init__(self, json_dict, GPType):
        """Constructor"""
        pass




########################################################################
class GPInputParameterInfo(object):
    """ Provides information about the input parameters """
    _parameterType = None
    _category = None
    _direction = None
    _displayName = None
    _name = None
    _dataType = None
    _defaultValue = None
    _description = None
    _value = None
    _dict = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, value, initialize=False):
        """Constructor"""
        if isinstance(value, str):
            self._json = value
            self._dict = json.loads(value)
        elif isinstance(value, dict):
            self._dict = value
            self._json = json.dumps(value)
        else:
            raise AttributeError("Invalid input, value must be string or dictionary")
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates the classes properties """
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in self._dict.iteritems():
            if k == "defaultValue":
                if len(self._dict['dataType'].split(':')) > 1:
                    split = self._dict['dataType'].split(':')
                    self._defaultValue = GPMultiValue(json_dict=v, GPType=split[1])
                if self._dict['dataType'] == "GPFeatureRecordSetLayer":
                    self._defaultValue = GPFeatureRecordSetLayer(json_dict=v)
                elif self._dict['dataType'] == "GPString":
                    self._defaultValue = GPString(v)
                elif self._dict['dataType'] == "GPBoolean":
                    self._defaultValue = GPBoolean(v)
                elif self._dict['dataType'] == "GPLong":
                    self._defaultValue = GPLong(v)
                elif self._dict['dataType'] == "GPLinearUnit":
                    self._defaultValue = GPLinearUnit(distance=v['distance'],
                                                      units=v['units'])
                elif self._dict['dataType'] == "GPDate":
                    self._defaultValue = GPDate(v)
                elif self._dict['dataType'] == "GPDouble":
                    self._defaultValue = GPDouble(v)
                elif self._dict['dataType'] == "GPDataFile":
                    self._defaultValue = GPDataFile(v)
                elif self._dict['dataType'] == "GPRecordSet":
                    self._defaultValue = GPRecordSet(json_dict=v)
            elif k in attributes:
                setattr(self, "_"+ k, self._dict[k])
            else:
                print k, " - attribute not implmented for GPInputParameters."
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the parameter's decription """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def defaultValue(self):
        """ returns the Input's default value """
        if self._defaultValue is None:
            self.__init()
        return self._defaultValue
    #----------------------------------------------------------------------
    @property
    def dataType(self):
        """ returns the data type for the input """
        if self._dataType is None:
            self.__init()
        return self._dataType
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ returns the input name """
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def displayName(self):
        """ returns the display name """
        if self._displayName is None:
            self.__init()
        return self._displayName
    #----------------------------------------------------------------------
    @property
    def direction(self):
        """ returns the parameter direction """
        if self._direction is None:
            self.__init()
        return self._direction
    #----------------------------------------------------------------------
    @property
    def category(self):
        """ returns the category """
        if self._category is None:
            self.__init()
        return self._category
    #----------------------------------------------------------------------
    @property
    def parameterType(self):
        """ returns the parameter type """
        if self._parameterType is None:
            self.__init()
        return self._parameterType
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


