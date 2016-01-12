from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseAGSServer
from datetime import datetime
import csv, json
########################################################################
class Log(BaseAGSServer):
    """ Log of a server """
    _url = None
    _securityHandler = None
    _operations = None
    _resources = None
    _proxy_port = None
    _proxy_url = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor
            Inputs:
               url - admin url
               securityHandler - Handler that handles site security
               username - admin username
               password - admin password
        """
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        self._url = url
        self._securityHandler = securityHandler
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
                print( k, " - attribute not implemented in Logs.")
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
    def operations(self):
        """ returns the operations """
        if self._operations is None:
            self.__init()
        return self._operations
    #----------------------------------------------------------------------
    @property
    def resources(self):
        """ returns the log resources """
        if self._resources is None:
            self.__init()
        return self._resources
    #----------------------------------------------------------------------
    def countErrorReports(self, machine="*"):
        """ This operation counts the number of error reports (crash
            reports) that have been generated on each machine.
            Input:
               machine - name of the machine in the cluster.  * means all
                         machines.  This is default
            Output:
               dictionary with report count and machine name
        """
        params = {
            "f": "json",
            "machine" : machine
        }
        return self._post(url=self._url + "/countErrorReports",
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def clean(self):
        """ Deletes all the log files on all server machines in the site.  """
        params = {
            "f" : "json",
        }
        return self._post(url=self._url + "/clean",
                             param_dict=params,
                             securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def logSettings(self):
        """ returns the current log settings """
        params = {
            "f" : "json"
        }
        sURL = self._url + "/settings"
        return self._get(url=sURL, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)['settings']
    #----------------------------------------------------------------------
    def editLogSettings(self,
                        logLevel="WARNING",
                        logDir=None,
                        maxLogFileAge=90,
                        maxErrorReportsCount=10):
        """
           The log settings are for the entire site.
           Inputs:
             logLevel -  Can be one of [OFF, SEVERE, WARNING, INFO, FINE,
                         VERBOSE, DEBUG].
             logDir - File path to the root of the log directory
             maxLogFileAge - number of days that a server should save a log
                             file.
             maxErrorReportsCount - maximum number of error report files
                                    per machine
        """
        lURL = self._url + "/settings/edit"
        allowed_levels =  ("OFF", "SEVERE", "WARNING", "INFO", "FINE", "VERBOSE", "DEBUG")
        currentSettings= self.logSettings
        currentSettings["f"] ="json"

        if logLevel.upper() in allowed_levels:
            currentSettings['logLevel'] = logLevel.upper()
        if logDir is not None:
            currentSettings['logDir'] = logDir
        if maxLogFileAge is not None and \
           isinstance(maxLogFileAge, int):
            currentSettings['maxLogFileAge'] = maxLogFileAge
        if maxErrorReportsCount is not None and \
           isinstance(maxErrorReportsCount, int) and\
           maxErrorReportsCount > 0:
            currentSettings['maxErrorReportsCount'] = maxErrorReportsCount
        return self._post(url=lURL, param_dict=currentSettings,
                             securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def query(self,
              startTime=None,
              endTime=None,
              sinceServerStart=False,
              level="WARNING",
              services="*",
              machines="*",
              server="*",
              codes=[],
              processIds=[],
              export=False,
              exportType="CSV", #CSV or TAB
              out_path=None
              ):
        """
           The query operation on the logs resource provides a way to
           aggregate, filter, and page through logs across the entire site.
           Inputs:

        """
        allowed_levels = ("SEVERE", "WARNING", "INFO",
                          "FINE", "VERBOSE", "DEBUG")
        qFilter = {
            "services": "*",
            "machines": "*",
            "server" : "*"
        }
        if len(processIds) > 0:
            qFilter['processIds'] = processIds
        if len(codes) > 0:
            qFilter['codes'] = codes
        params = {
            "f" : "json",
            "sinceServerStart" : sinceServerStart,
            "pageSize" : 10000
        }
        if startTime is not None and \
           isinstance(startTime, datetime):
            params['startTime'] = startTime.strftime("%Y-%m-%dT%H:%M:%S")
        if endTime is not None and \
           isinstance(endTime, datetime):
            params['endTime'] = endTime.strftime("%Y-%m-%dT%H:%M:%S")
        if level.upper() in allowed_levels:
            params['level'] = level
        if server != "*":
            qFilter['server'] = server.split(',')
        if services != "*":
            qFilter['services'] = services.split(',')
        if machines != "*":
            qFilter['machines'] = machines.split(",")
        params['filter'] = qFilter
        if export == True and \
           out_path is not None:
            messages = self._post(self._url + "/query", params,
                                     securityHandler=self._securityHandler,
                                     proxy_url=self._proxy_url,
                                     proxy_port=self._proxy_port)

            with open(name=out_path, mode='wb') as f:
                hasKeys = False
                if exportType == "TAB":
                    csvwriter = csv.writer(f, delimiter='\t')
                else:
                    csvwriter = csv.writer(f)
                for message in messages['logMessages']:
                    if hasKeys == False:
                        csvwriter.writerow(message.keys())
                        hasKeys = True
                    csvwriter.writerow(message.values())
                    del message
            del messages
            return out_path
        else:
            return self._post(self._url + "/query", params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
