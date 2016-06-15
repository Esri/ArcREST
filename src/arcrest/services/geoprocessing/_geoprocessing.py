"""
Performs and handles all GP operations
"""
from __future__ import absolute_import
import json
from ._gpobjects import GPBoolean, GPDataFile, GPDate
from ._gpobjects import GPDouble, GPFeatureRecordSetLayer, GPLinearUnit
from ._gpobjects import GPLong, GPMultiValue, GPRasterData
from ._gpobjects import GPRasterDataLayer, GPRecordSet, GPString
from ...common._base import BaseService
########################################################################
class GPService(BaseService):
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
    _tasks = None
    _con = None
    _url = None
    _json_dict = None
    _resultMapServerName = None
    _tasks = None
    _executionType = None
    _currentVersion = None
    _maximumRecords = None
    _serviceDescription = None
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        if self._currentVersion is None:
            self.init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def resultMapServerName(self):
        """ returns the result mapserver name """
        if self._resultMapServerName is None:
            self.init()
        return self._resultMapServerName
    #----------------------------------------------------------------------
    def _load_tasks(self):
        """ loads the GPTask into GPTask Objects """
        self._tasks = []
        if self._json_dict is None:
            self.init(connection=self._con)
        json_dict = dict(self)
        if isinstance(json_dict, dict) and \
           json_dict.has_key("tasks"):
            for l in json_dict['tasks']:
                self._tasks.append(GPTask(
                        connection=self._con,
                        url=self._url + "/%s" % l,
                        initialize=True))
                del l
    #----------------------------------------------------------------------
    @property
    def tasks(self):
        """ returns the tasks in the GP service """
        if self._tasks is None:
            self.init()
        self._load_tasks()
        return self._tasks
    #----------------------------------------------------------------------
    @property
    def executionType(self):
        """ returns the execution type """
        if self._executionType is None:
            self.init()
        return self._executionType
    #----------------------------------------------------------------------
    @property
    def maximumRecords(self):
        """ the maximum number of rows returned from service """
        if self._maximumRecords is None:
            self.init()
        return self._maximumRecords
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """ returns the service description """
        if self._serviceDescription is None:
            self.init()
        return self._serviceDescription
########################################################################
class GPTask(BaseService):
    """ This is the GP task that performs the operation """
    _url = None
    _con = None
    _json_dict = None
    _parameters = None
    _category = None
    _displayName = None
    _name = None
    _parameters = None
    _executionType = None
    _helpUrl = None
    _description = None
    #----------------------------------------------------------------------
    @property
    def executionType(self):
        """ returns the execution type """
        if self._executionType is None:
            self.init()
        return self._executionType
    #----------------------------------------------------------------------
    @property
    def helpUrl(self):
        """ returns the help url """
        if self._helpUrl is None:
            self.init()
        return self._helpUrl
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the description of the service """
        if self._description is None:
            self.init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def category(self):
        """ returns the category """
        if self._category is None:
            self.init()
        return self._category
    #----------------------------------------------------------------------
    @property
    def displayName(self):
        """ returns the tools display name """
        if self._displayName is None:
            self.init()
        return self._displayName
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ returns the name of the service """
        if self._name is None:
            self.init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def parameters(self):
        """ returns the default parameters """
        if self._json_dict is None:
            self.init(self._con)
        if "parameters" in self._json_dict:
            for param in self.parameters:
                if isinstance(param['defaultValue'], (dict,str, list)):
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
    def getJob(self, jobID):
        """ returns the results or status of a job """
        url = self._url + "/jobs/%s" % (jobID)
        return GPJob(connection=self._con, url=url)
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
                if isinstance(p, dict):
                    params[p.paramName] = p
                else:
                    params[p.paramName] = p.value
        if method.lower() == "get":
            res = self._con.get(path_or_url=url, params=params)
            jobUrl = self._url + "/jobs/%s" % res['jobId']
            return GPJob(connection=self._con, url=jobUrl,
                          initialize=True)
        elif method.lower() == "post":
            res = self._con.post(path_or_url=url, params=params)
            jobUrl = self._url + "/jobs/%s" % res['jobId']
            return GPJob(url=jobUrl,
                         connection=self._con,
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
            if isinstance(p, dict):
                params[p.paramName] = p
            else:
                params[p.paramName] = p.value
            del p
        if method.lower() == "post":
            return self._con.post(path_or_url=url, postdata=params)
        else:
            return self._con.get(path_or_url=url, params=params)
########################################################################
class GPJob(BaseService):
    """
       Represents an ArcGIS GeoProcessing Job
    """
    _jobId = None
    _json_dict = None
    _con = None
    _url = None
    _results = None
    _messages = None
    _jobStatus = None
    _inputs = None
    #----------------------------------------------------------------------
    def cancelJob(self):
        """ cancels the job """
        params = {
            "f" : "json"
        }
        return self._con.get(path_or_url=self._url + "/cancel",
                            params=params)
    #----------------------------------------------------------------------
    @property
    def messages(self):
        """ returns the messages """
        self.init()
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
        return self._con.get(path_or_url=url,
                            params=params)
    #----------------------------------------------------------------------
    @property
    def results(self):
        """ returns the results """
        self.init()
        if isinstance(self._results, dict):
            for k,v in self._results.items():
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
        else:
            return self._results
    #----------------------------------------------------------------------
    @property
    def jobStatus(self):
        """ returns the job status """
        self.init()
        return self._jobStatus
    #----------------------------------------------------------------------
    @property
    def jobId(self):
        """ returns the job ID """
        if self._jobId is None:
            self.init()
        return self._jobId
    #----------------------------------------------------------------------
    @property
    def inputs(self):
        """ returns the inputs of a service """
        self.init()
        return self._inputs
    #----------------------------------------------------------------------
    def getParameterValue(self, parameterName):
        """ gets a parameter value """
        if  self._results is None:
            self.init()
        parameter = self._results[parameterName]
        return parameter