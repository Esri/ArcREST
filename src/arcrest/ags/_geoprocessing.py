from __future__ import absolute_import
from __future__ import print_function
import json
from ._gpobjects import *
from .._abstract.abstract import BaseAGSServer, BaseGPObject
from ..common.general import local_time_to_online
########################################################################
class GPService(BaseAGSServer):
    """
    Geoprocessing is a fundamental part of enterprise GIS operations.
    Geoprocessing provides GIS users with data analysis, data management,
    and data conversion tools.
    A geoprocessing service represents a collection of published tools that
    perform tasks necessary for manipulating and analyzing geographic
    information across a wide range of disciplines. Each tool performs one
    or more operations, such as projecting a data set from one map
    projection to another, adding fields to a table, or creating buffer
    zones around features. A tool accepts input (such as feature sets,
    tables, and property values), executes operations using the input data,
    and generates output for presentation in a map or further processing by
    the client. Tools can be executed synchronously (in sequence) or
    asynchronously. When used with the REST API, a geoprocessing service
    should always be published as a pooled service.
    Use a geoprocessing service to do the following:
        List available tools and their input/output properties
        Execute a task synchronously
        Submit a job to a task asynchronously
        Get job details, including job status
        Display results using a map service
        Retrieve results for further processing by the client
    Many GIS tasks involve the repetition of work, and this creates the
    need for a framework to provide automation of workflows. Geoprocessing
    services answer this need by using a model to combine a series of
    operations in a sequence, then exposing the model as a tool.
    The REST API GP Service resource provides basic information associated
    with the service, such as the service description, the tasks provided,
    the execution type, and the result's map server name.
    The GP Service resource has operations that return results after a task
    is successfully completed. The supported operations are as follows:
    Execute task-Used when the execution type is synchronous. When a task
    is executed synchronously, a user must wait for the results.
    Submit job-Used when the execution type is asynchronous. When a job is
    submitted asynchronously, a user can do other things while awaiting
    notice that the task is completed.
    """
    _resultMapServerName = None
    _tasks = None
    _executionType = None
    _currentVersion = None
    _maximumRecords = None
    _serviceDescription = None
    _securityHandler = None
    _json = None
    _json_dict = None
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
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                if k == "tasks":
                    self._tasks = []
                    for t in v:
                        self._tasks.append(
                            GPTask(url=self._url + "/%s" % t,
                                   securityHandler=self._securityHandler,
                                   proxy_url=self._proxy_url,
                                   proxy_port=self._proxy_port,
                                   initialize=False)
                        )
                else:
                    setattr(self, "_"+ k, json_dict[k])
            else:
                print (k, " - attribute not implemented for gp service.")
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """returns the JSON response in key/value pairs"""
        if self._json_dict is None:
            self.__init()
        for k,v in self._json_dict.iteritems():
            yield [k,v]
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
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in GPTask.")
            del k,v

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
        for param in self._parameters:
            if not isinstance(param['defaultValue'], BaseGPObject):
                if param['dataType'] == "GPFeatureRecordSetLayer":
                    param['defaultValue'] = GPFeatureRecordSetLayer.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPString":
                    param['defaultValue'] = GPString.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPLong":
                    param['defaultValue'] = GPLong.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPDouble":
                    param['defaultValue'] = GPDouble.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPDate":
                    param['defaultValue'] = GPDate.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPBoolean":
                    param['defaultValue'] = GPBoolean.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPDataFile":
                    param['defaultValue'] = GPDataFile.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPLinearUnit":
                    param['defaultValue'] = GPLinearUnit.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPMultiValue":
                    param['defaultValue'] = GPMultiValue.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPRasterData":
                    param['defaultValue'] = GPRasterData.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPRasterDataLayer":
                    param['defaultValue'] = GPRasterDataLayer.fromJSON(json.dumps(param))
                elif param['dataType'] == "GPRecordSet":
                    param['defaultValue'] = GPRecordSet.fromJSON(json.dumps(param))
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
    def submitJob(self, inputs, method="POST",
                  outSR=None, processSR=None,
                  returnZ=False, returnM=False):
        """
           submits a job to the current task, and returns a job ID
           Inputs:
              inputs - list of GP object values
              method - string - either GET or POST.  The way the service is
                       submitted.
              outSR - spatial reference of output geometries
              processSR - spatial reference that the model will use to
               perform geometry operations
              returnZ - Z values will be included in the result if true
              returnM - M values will be included in the results if true
           Ouput:
              JOB ID as a string
        """
        url = self._url + "/submitJob"
        params = { "f" : "json" }
        if not outSR is None:
            params['env:outSR'] = outSR
        if not processSR is None:
            params['end:processSR'] = processSR
        params['returnZ'] = returnZ
        params['returnM'] = returnM
        if not inputs is None:
            for p in inputs:
                if isinstance(p, BaseGPObject):
                    params[p.paramName] = p.value
        if method.lower() == "get":
            res = self._do_get(url=url, param_dict=params,
                               securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
            jobUrl = self._url + "/jobs/%s" % res['jobId']
            return GPJob(url=jobUrl,
                          securityHandler=self._securityHandler,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port,
                          initialize=True)
        elif method.lower() == "post":
            res = self._do_post(url=url, param_dict=params,
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port)
            jobUrl = self._url + "/jobs/%s" % res['jobId']
            return GPJob(url=jobUrl,
                          securityHandler=self._securityHandler,
                          proxy_url=self._proxy_url,
                          proxy_port=self._proxy_port,
                          initialize=True)
        else:
            raise AttributeError("Invalid input: %s. Must be GET or POST" \
                                 % method)
    #----------------------------------------------------------------------
    def executeTask(self,
                    inputs,
                    outSR=None,
                    processSR=None,
                    returnZ=False,
                    returnM=False,
                    f="json",
                    method="POST"
                    ):
        """
        performs the execute task method
        """
        params = {
            "f" : f
        }
        url = self._url + "/execute"
        params = { "f" : "json" }
        if not outSR is None:
            params['env:outSR'] = outSR
        if not processSR is None:
            params['end:processSR'] = processSR
        params['returnZ'] = returnZ
        params['returnM'] = returnM
        for p in inputs:
            if isinstance(p, BaseGPObject):
                params[p.paramName] = p.value
            del p
        if method.lower() == "post":
            return self._do_post(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        else:
            return self._do_get(url=url,
                                 param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
########################################################################
class GPJob(BaseAGSServer):
    """
       Represents an ArcGIS GeoProcessing Job
    """
    _proxy_url = None
    _proxy_port = None
    _jobId = None
    _messages = None
    _results = None
    _jobStatus = None
    _inputs = None
    _json = None
    _securityHandler = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        if securityHandler is not None:
            self._securityHandler = securityHandler
            self._referer_url = securityHandler.referer_url
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as a string"""
        self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {"f" : "json"}
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                    if not attr.startswith('__') and \
                    not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print (k, " - attribute not implemented for GPJob.")
            del k,v
    #----------------------------------------------------------------------
    def cancelJob(self):
        """ cancels the job """
        params = {
            "f" : "json"
        }
        return self._do_get(url=self._url + "/cancel",
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def messages(self):
        """ returns the messages """
        self.__init()
        return self._messages
    #----------------------------------------------------------------------
    def _get_json(self, urlpart):
        """
        gets the result object dictionary
        """
        url = self._url + "/%s" % urlpart
        params = {
            "f" : "json",

        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self.proxy_port)
    #----------------------------------------------------------------------
    @property
    def results(self):
        """ returns the results """
        self.__init()
        for k,v in self._results.iteritems():
            param = self._get_json(v['paramUrl'])
            if param['dataType'] == "GPFeatureRecordSetLayer":
                self._results[k] = GPFeatureRecordSetLayer.fromJSON(json.dumps(param))
            elif param['dataType'].lower().find('gpmultivalue') > -1:
                self._results[k] = GPMultiValue.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPString":
                self._results[k] = GPString.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPLong":
                self._results[k] = GPLong.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPDouble":
                self._results[k] = GPDouble.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPDate":
                self._results[k] = GPDate.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPBoolean":
                self._results[k] = GPBoolean.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPDataFile":
                self._results[k] = GPDataFile.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPLinearUnit":
                self._results[k] = GPLinearUnit.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPMultiValue":
                self._results[k] = GPMultiValue.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPRasterData":
                self._results[k] = GPRasterData.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPRasterDataLayer":
                self._results[k] = GPRasterDataLayer.fromJSON(json.dumps(param))
            elif param['dataType'] == "GPRecordSet":
                self._results[k] = GPRecordSet.fromJSON(json.dumps(param))
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
        if  self._results is None:
            self.__init()
        parameter = self._results[parameterName]
        return parameter