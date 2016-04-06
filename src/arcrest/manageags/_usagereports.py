from __future__ import absolute_import
from __future__ import print_function
from ..packages import six
from .._abstract.abstract import BaseAGSServer
import json
########################################################################
class UsageReports(BaseAGSServer):
    """
    This resource is a collection of all the usage reports created within
    your site. The Create Usage Report operation lets you define a new
    usage report.
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _json = None
    _metrics = None
    _reports = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        if url.lower().endswith('/usagereports'):
            self._url = url
        else:
            self._url = url + "/usagereports"
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json"
        }
        json_dict = self._get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in UsageReports.")
            del k
            del v
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        return json.dumps(self._json)
    #----------------------------------------------------------------------
    @property
    def metrics(self):
        """gets the metrics values"""
        if self._metrics is None:
            self.__init()
        return self._metrics
    #----------------------------------------------------------------------
    @property
    def reports(self):
        """returns a list of reports on the server"""
        if self._metrics is None:
            self.__init()
        self._reports = []
        for r in self._metrics:
            url = self._url + "/%s" % six.moves.urllib.parse.quote_plus(r['reportname'])
            self._reports.append(UsageReport(url=url,
                                             securityHandler=self._securityHandler,
                                             proxy_url=self._proxy_url,
                                             proxy_port=self._proxy_port,
                                             initialize=True))
            del url
        return self._reports
    #----------------------------------------------------------------------
    @property
    def usageReportSettings(self):
        """
        The usage reports settings are applied to the entire site. A GET
        request returns the current usage reports settings. When usage
        reports are enabled, service usage statistics are collected and
        persisted to a statistics database. When usage reports are
        disabled, the statistics are not collected. The samplingInterval
        parameter defines the duration (in minutes) during which the usage
        statistics are sampled or aggregated (in-memory) before being
        written out to the statistics database. Database entries are
        deleted after the interval specified in the maxHistory parameter (
        in days), unless the maxHistory parameter is 0, for which the
        statistics are persisted forever.
        """
        params = {
            "f" : "json"
        }
        url = self._url + "/settings"
        return self._get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def editUsageReportSettings(self, samplingInterval,
                                enabled=True, maxHistory=0):
        """
        The usage reports settings are applied to the entire site. A POST
        request updates the usage reports settings.

        Inputs:
           samplingInterval - Defines the duration (in minutes) for which
             the usage statistics are aggregated or sampled, in-memory,
             before being written out to the statistics database.
           enabled - default True - Can be true or false. When usage
             reports are enabled, service usage statistics are collected
             and persisted to a statistics database. When usage reports are
             disabled, the statistics are not collected.
           maxHistory - default 0 - Represents the number of days after
             which usage statistics are deleted after the statistics
             database. If the maxHistory parameter is set to 0, the
             statistics are persisted forever.
        """
        params = {
            "f" : "json",
            "maxHistory" : maxHistory,
            "enabled" : enabled,
            "samplingInterval"  : samplingInterval
        }
        url = self._url + "/settings/edit"
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def createUsageReport(self,
                          reportname,
                          queries,
                          metadata,
                          since="LAST_DAY",
                          fromValue=None,
                          toValue=None,
                          aggregationInterval=None
                          ):
        """
        Creates a new usage report. A usage report is created by submitting
        a JSON representation of the usage report to this operation.

        Inputs:
           reportname - the unique name of the report
           since - the time duration of the report. The supported values
              are: LAST_DAY, LAST_WEEK, LAST_MONTH, LAST_YEAR, CUSTOM
              LAST_DAY represents a time range spanning the previous 24
                 hours.
              LAST_WEEK represents a time range spanning the previous 7
                 days.
              LAST_MONTH represents a time range spanning the previous 30
                 days.
              LAST_YEAR represents a time range spanning the previous 365
                 days.
              CUSTOM represents a time range that is specified using the
                 from and to parameters.
           fromValue - optional value - The timestamp (milliseconds since
              UNIX epoch, namely January 1, 1970, 00:00:00 GMT) for the
              beginning period of the report. Only valid when since is
              CUSTOM
           toValue - optional value - The timestamp (milliseconds since
              UNIX epoch, namely January 1, 1970, 00:00:00 GMT) for the
              ending period of the report.Only valid when since is
              CUSTOM.
           aggregationInterval - Optional. Aggregation interval in minutes.
              Server metrics are aggregated and returned for time slices
              aggregated using the specified aggregation interval. The time
              range for the report, specified using the since parameter
              (and from and to when since is CUSTOM) is split into multiple
              slices, each covering an aggregation interval. Server metrics
              are then aggregated for each time slice and returned as data
              points in the report data.
              When the aggregationInterval is not specified, the following
              defaults are used:
                 LAST_DAY: 30 minutes
                 LAST_WEEK: 4 hours
                 LAST_MONTH: 24 hours
                 LAST_YEAR: 1 week
                 CUSTOM: 30 minutes up to 1 day, 4 hours up to 1 week, 1
                 day up to 30 days, and 1 week for longer periods.
             If the samplingInterval specified in Usage Reports Settings is
             more than the aggregationInterval, the samplingInterval is
             used instead.
           queries - A list of queries for which to generate the report.
              You need to specify the list as an array of JSON objects
              representing the queries. Each query specifies the list of
              metrics to be queries for a given set of resourceURIs.
              The queries parameter has the following sub-parameters:
                 resourceURIs - Comma separated list of resource URIs for
                 which to report metrics. Specifies services or folders
                 for which to gather metrics.
                    The resourceURI is formatted as below:
                       services/ - Entire Site
                       services/Folder/  - Folder within a Site. Reports
                         metrics aggregated across all services within that
                         Folder and Sub-Folders.
                       services/Folder/ServiceName.ServiceType - Service in
                         a specified folder, for example:
                         services/Map_bv_999.MapServer.
                       services/ServiceName.ServiceType - Service in the
                         root folder, for example: Map_bv_999.MapServer.
                 metrics - Comma separated list of metrics to be reported.
                   Supported metrics are:
                    RequestCount - the number of requests received
                    RequestsFailed - the number of requests that failed
                    RequestsTimedOut - the number of requests that timed out
                    RequestMaxResponseTime - the maximum response time
                    RequestAvgResponseTime - the average response time
                    ServiceActiveInstances - the maximum number of active
                      (running) service instances sampled at 1 minute
                      intervals, for a specified service
           metadata - Can be any JSON Object. Typically used for storing
              presentation tier data for the usage report, such as report
              title, colors, line-styles, etc. Also used to denote
              visibility in ArcGIS Server Manager for reports created with
              the Administrator Directory. To make any report created in
              the Administrator Directory visible to Manager, include
              "managerReport":true in the metadata JSON object. When this
              value is not set (default), reports are not visible in
              Manager. This behavior can be extended to any client that
              wants to interact with the Administrator Directory. Any
              user-created value will need to be processed by the client.

        Example:
        >>> queryObj = [{
           "resourceURIs": ["services/Map_bv_999.MapServer"],
           "metrics": ["RequestCount"]
        }]
        >>> obj.createReport(
           reportname="SampleReport",
           queries=queryObj,
           metadata="This could be any String or JSON Object.",
           since="LAST_DAY"
        )
        """
        url = self._url + "/add"

        params = {
            "f" : "json",
            "usagereport": {
            "reportname" : reportname,
            "since" : since,
            "metadata" : metadata}
        }
        if isinstance(queries, dict):
            params["usagereport"]["queries"] = [queries]
        elif isinstance(queries, list):
            params["usagereport"]["queries"] = queries
        if aggregationInterval is not None:
            params["usagereport"]['aggregationInterval'] = aggregationInterval
        if since.lower() == "custom":
            params["usagereport"]['to'] = toValue
            params["usagereport"]['from'] = fromValue
        res =  self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_port=self._proxy_port,
                             proxy_url=self._proxy_url)
        #  Refresh the metrics object
        self.__init()
        return res

########################################################################
class UsageReport(BaseAGSServer):
    """
    A Usage Report is used to obtain ArcGIS Server usage data for specified
    resources during a given time period. It specifies the parameters for
    obtaining server usage data, time range (since from and to parameters),
    aggregation interval, and queries (which specify the metrics to be
    gathered for a collection of server resources, such as folders and
    services).
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _json = None
    _reportname = None
    _since = None
    _from = None
    _to = None
    _aggregationInterval = None
    _queries = None
    _metadata = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json"
        }
        json_dict = self._get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json = json.dumps(json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.items():
            if k.lower() == "from":
                self._from = v
            elif k.lower() == "to":
                self._to = v
            elif k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print (k, " - attribute not implemented in manageags.UsageReport.")
            del k
            del v
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    @property
    def reportname(self):
        """gets the report name"""
        if self._reportname is None:
            self.__init()
        return self._reportname
    #----------------------------------------------------------------------
    @property
    def since(self):
        """gets/sets the since value"""
        if self._since is None:
            self.__init()
        return self._since
    #----------------------------------------------------------------------
    @since.setter
    def since(self, value):
        """gets/sets the since value"""
        self._since = value
    #----------------------------------------------------------------------
    @property
    def fromValue(self):
        """gets/sets the from value"""
        if self._from is None:
            self.__init()
        return self._from
    #----------------------------------------------------------------------
    @fromValue.setter
    def fromValue(self, value):
        """gets/sets the from value"""
        self._from = value
    #----------------------------------------------------------------------
    @property
    def toValue(self):
        """gets/sets the toValue"""
        if self._to is None:
            self.__init()
        return self._to
    #----------------------------------------------------------------------
    @toValue.setter
    def toValue(self, value):
        """gets/sets the toValue"""
        self._to = value
    #----------------------------------------------------------------------
    @property
    def aggregationInterval(self):
        """gets/sets the aggregationInterval value"""
        if self._aggregationInterval is None:
            self.__init()
        return self._aggregationInterval
    #----------------------------------------------------------------------
    @aggregationInterval.setter
    def aggregationInterval(self, value):
        """gets/sets the aggregationInterval value"""
        self._aggregationInterval = value
    #----------------------------------------------------------------------
    @property
    def queries(self):
        """gets/sets the query values"""
        if self._queries is None:
            self.__init()
        return self._queries
    #----------------------------------------------------------------------
    @queries.setter
    def queries(self, value):
        """gets/sets the query values"""
        self._queries = value
    #----------------------------------------------------------------------
    @property
    def metadata(self):
        """gets/sets the metadata value"""
        if self._metadata is None:
            self.__init()
        return self._metadata
    #----------------------------------------------------------------------
    @metadata.setter
    def metadata(self, value):
        """gets/sets the metadata value"""
        self._metadata = value
    #----------------------------------------------------------------------
    def edit(self):
        """
        Edits the usage report. To edit a usage report, you need to submit
        the complete JSON representation of the usage report which
        includes updates to the usage report properties. The name of the
        report cannot be changed when editing the usage report.

        Values are changed in the class, to edit a property like
        metrics, pass in a new value.  Changed values to not take until the
        edit() is called.

        Inputs:
           None
        """

        usagereport_dict = {
            "reportname": self.reportname,
            "queries": self._queries,
            "since": self.since,
            "metadata": self._metadata,
            "to" : self._to,
            "from" : self._from,
            "aggregationInterval" : self._aggregationInterval
        }
        params = {
            "f" : "json",
            "usagereport" : json.dumps(usagereport_dict)
        }
        url = self._url + "/edit"
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def delete(self):
        """deletes the current report"""
        url = self._url + "/delete"
        params = {
            "f" : "json",
        }
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def query(self, queryFilter):
        """
        Retrieves server usage data for the report. This operation
        aggregates and filters server usage statistics for the entire
        ArcGIS Server site. The report data is aggregated in a time slice,
        which is obtained by dividing up the time duration by the default
        (or specified) aggregationInterval parameter in the report. Each
        time slice is represented by a timestamp, which represents the
        ending period of that time slice.
        In the JSON response, the queried data is returned for each metric-
        resource URI combination in a query. In the report-data section,
        the queried data is represented as an array of numerical values. A
        response of null indicates that data is not available or requests
        were not logged for that metric in the corresponding time-slice.

        Inputs:
           queryFilter - The report data can be filtered by the machine
             where the data is generated. The filter accepts a comma
             separated list of machine names; * represents all machines.

             Examples:
               # filters for the specified machines
               {"machines": ["WIN-85VQ4T2LR5N", "WIN-239486728937"]}
               # no filtering; all machines are accepted
               {"machines": "*"}
        """
        params = {
            "f" : "json",
            "filter" : queryFilter
        }
        url = self._url + "/data"
        return self._post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
