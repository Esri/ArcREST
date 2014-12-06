from .._abstract.abstract import BaseAGSServer, BaseGPObject
from ..common.spatial import featureclass_to_json, recordset_to_json
from ..common.general import local_time_to_online
from ..security import security

import urllib
import json
import time
import datetime

########################################################################
class GPService(BaseAGSServer):
    """ An instasnce of a publish geoprocessing service """
    _currentVersion = None
    _resultMapServerName = None
    _tasks = None
    _executionType = None
    _maximumRecords = None
    _serviceDescription = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    #----------------------------------------------------------------------
    def __init__(self,
                 url,
                 securityHandler=None,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        if securityHandler is not None:
            self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url  
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the GP tools """
        params = {
            "f" : "json"
        }
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
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
                                              securityHandler=self._securityHandler,
                                              proxy_url=self._proxy_url,
                                              proxy_port=self._proxy_port)
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
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _url = None
    _category = None
    _displayName = None
    _name = None
    _parameters = None
    _executionType = None
    _helpUrl = None
    _description = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url  
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token
        json_dict = self._do_get(url=self._url, param_dict=params,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
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
                     securityHandler=self._securityHandler,
                     proxy_port=self._proxy_port,
                     proxy_url=self._proxy_url)
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
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token
        for k, v in inputs.iteritems():
            if isinstance(v, BaseGPObject):
                params[k] = v.value
        if method.lower() == "get":
            return self._do_get(url=url, param_dict=params,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
        elif method.lower() == "post":
            return self._do_post(url=url, param_dict=params,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
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
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        if securityHandler is not None:
            self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url  
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token
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
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token
        return self._do_get(url=self._url + "/cancel",
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
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
    def getAllResults(self):
        """ returns all results for a GP tool """
        res = {}
        params = {
            "f" : "json",
            "token" : self._securityHandler.token
        }
        for k,v in self._results.iteritems():
            res[k] = self._do_get(url=self._url + "/%s" % v['paramUrl'],
                                  param_dict=params,
                                  proxy_url=self._proxy_url, proxy_port=self._proxy_port)
        return res
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
        if self._securityHandler is not None:
            params['token'] = self._securityHandler.token

        return self._do_get(url=paramURL,
                            param_dict=params,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)



########################################################################
class GPString(BaseGPObject):
    """string object"""
    _value = None
    _paramName = None
    #----------------------------------------------------------------------
    def __init__(self, value):
        """Constructor"""
        #paramName,
        #self._paramName = paramName
        if isinstance(value, str):
            self._value = value
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
    @property
    def value(self):
        """ returns the value"""
        return self._value
        #return {"paramName":self._paramName,
                #"dataType":"GPString",
                #"value":self._value}
    @value.setter
    def value(self, value):
        """ sets the value"""
        if isinstance(value, str):
            self._value = value
########################################################################
class GPBoolean(BaseGPObject):
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
class GPLong(BaseGPObject):
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
class GPDouble(BaseGPObject):
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
class GPLinearUnit(BaseGPObject):
    """GP double object"""
    _value = None
    _units = None
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
class GPDate(BaseGPObject):
    """GP date object"""
    _value = None
    #----------------------------------------------------------------------
    def __init__(self, dateObject):
        """Constructor"""
        if isinstance(dateObject, datetime.datetime):
            self._value = dateObject
        elif isinstance(dateObject, long):
            self._value = dateObject
        elif dateObject is None:
            self._value = None
        else:
            raise AttributeError("Invalid Input of type: %s" % type(dateObject))
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the value"""
        return self._value
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """ sets the value"""
        if isinstance(value, datetime.datetime):
            self._value = local_time_to_online(value)
        elif isinstance(value, long):
            self._value = value
        else:
            raise AttributeError("Invalid Input of type: %s" % type(value))
########################################################################
class GPDataFile(BaseGPObject):
    """ represents a data file object for GP task """

    _url = None
    _format = None
    _itemId = None
    #----------------------------------------------------------------------
    def __init__(self, url=None, format=None, itemId=None):
        """Constructor"""
        if itemId is None and url is None:
            raise AttributeError("You must provide a URL or itemId")
        self._url = url
        self._format = format
        self._itemId = itemId
    #----------------------------------------------------------------------
    @property
    def url(self):
        """gets/sets the url"""
        return self._url
    #----------------------------------------------------------------------
    @url.setter
    def url(self, value):
        """gets/sets the url"""
        if self._url != value:
            self._url = value
    #----------------------------------------------------------------------
    @property
    def format(self):
        """gets/sets the format"""
        return self._format
    #----------------------------------------------------------------------
    @format.setter
    def format(self, value):
        """gets/sets the format"""
        if self._format != value:
            self._format
    #----------------------------------------------------------------------
    @property
    def itemId(self):
        """gets/sets the itemId"""
        return self._itemId
    #----------------------------------------------------------------------
    @itemId.setter
    def itemId(self, value):
        """gets/sets the itemId"""
        if self._itemId != value:
            self._itemId = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ gets the value """
        if self._itemId is not None:
            return {"itemID" : self._itemId }
        elif self._url is not None and \
             self._format is not None:
            return { "url" : self._url,
                     "format" : self._format }

########################################################################
class GPFeatureRecordSetLayer(BaseGPObject):
    """
       Returns the GPFeatureRecordSetLayer
    """
    _fc = None
    #----------------------------------------------------------------------
    def __init__(self, fc):
        """Constructor"""
        self._fc = fc
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ returns the value """
        return featureclass_to_json(self._fc)
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """ sets the value """
        self._fc = value


########################################################################
class GPRecordSet(BaseGPObject):
    """
    represents the GPRecordSet GP Object
    """
    _table = None
    #----------------------------------------------------------------------
    def __init__(self, table):
        """Constructor
           Inputs:
              table - path to the table
        """
        self._table = table
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ gets/sets the table """
        return recordset_to_json(self._table)
    #----------------------------------------------------------------------
    @value.setter
    def value(self, value):
        """gets/sets the table"""
        if self._table != value:
            self._table = value
########################################################################
class GPRasterData(BaseGPObject):
    """
    represents the GP Raster Dataset
    """
    _url = None
    _format = None
    _itemId = None
    #----------------------------------------------------------------------
    def __init__(self, url=None, format=None, itemId=None):
        """Constructor"""
        if itemId is None and url is None:
            raise AttributeError("You must provide a URL or itemId")


        self._url = url
        self._format = format
        self._itemId = itemId
    #----------------------------------------------------------------------
    @property
    def url(self):
        """gets/sets the url"""
        return self._url
    #----------------------------------------------------------------------
    @url.setter
    def url(self, value):
        """gets/sets the url"""
        if self._url != value:
            self._url = value
    #----------------------------------------------------------------------
    @property
    def format(self):
        """gets/sets the format"""
        return self._format
    #----------------------------------------------------------------------
    @format.setter
    def format(self, value):
        """gets/sets the format"""
        if self._format != value:
            self._format
    #----------------------------------------------------------------------
    @property
    def itemId(self):
        """gets/sets the itemId"""
        return self._itemId
    #----------------------------------------------------------------------
    @itemId.setter
    def itemId(self, value):
        """gets/sets the itemId"""
        if self._itemId != value:
            self._itemId = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ gets the value """
        if self._itemId is not None:
            return {"itemID" : self._itemId }
        elif self._url is not None and \
             self._format is not None:
            return { "url" : self._url,
                     "format" : self._format }
########################################################################
class GPRasterDataLayer(BaseGPObject):
    """
    represents the GP Raster Data Layer
    """
    _url = None
    _format = None
    _itemId = None
    #----------------------------------------------------------------------
    def __init__(self, url=None, format=None, itemId=None):
        """Constructor"""
        if itemId is None and url is None:
            raise AttributeError("You must provide a URL or itemId")


        self._url = url
        self._format = format
        self._itemId = itemId
    #----------------------------------------------------------------------
    @property
    def url(self):
        """gets/sets the url"""
        return self._url
    #----------------------------------------------------------------------
    @url.setter
    def url(self, value):
        """gets/sets the url"""
        if self._url != value:
            self._url = value
    #----------------------------------------------------------------------
    @property
    def format(self):
        """gets/sets the format"""
        return self._format
    #----------------------------------------------------------------------
    @format.setter
    def format(self, value):
        """gets/sets the format"""
        if self._format != value:
            self._format
    #----------------------------------------------------------------------
    @property
    def itemId(self):
        """gets/sets the itemId"""
        return self._itemId
    #----------------------------------------------------------------------
    @itemId.setter
    def itemId(self, value):
        """gets/sets the itemId"""
        if self._itemId != value:
            self._itemId = value
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ gets the value """
        if self._itemId is not None:
            return {"itemID" : self._itemId }
        elif self._url is not None and \
             self._format is not None:
            return { "url" : self._url,
                     "format" : self._format }



########################################################################
class GPMultiValue(BaseGPObject):
    """ reprsents the GP MultiValue Object """
    _values = None
    #----------------------------------------------------------------------
    def __init__(self, values):
        """Constructor"""
        self._values = []
        if values is not None:
            if isinstance(values, list):
                for v in values:
                    self._values.append(v)
                    del v
            else:
                self._values.append(values)
    #----------------------------------------------------------------------
    @property
    def value(self):
        """ gets the value """
        return [v.value for v in self._values]
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
    _choiceList = None
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
    def choiceList(self):
        """ returns the choiceList """
        if self._choiceList is None:
            self.__init()
        return self._choiceList
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




