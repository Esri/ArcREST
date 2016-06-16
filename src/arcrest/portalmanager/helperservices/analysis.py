from __future__ import absolute_import
from ...services.geoprocessing import GPService
########################################################################
class analysis(object):
    """
       ArcGIS Online is a collaborative, cloud-based platform that lets
       members of an organization create, share, and access maps,
       applications, and data, including authoritative basemaps published
       by Esri. Through ArcGIS Online, you get access to Esri's secure
       cloud, where you can manage, create, store, and access hosted web
       services.
       ArcGIS Online includes the Spatial Analysis service. The Spatial
       Analysis service contains a number of tasks, listed below, that you
       can access and use in your applications. Using Spatial Analysis
       service tasks consumes credits. For more information on credits, see
       see Service credits overview which includes access to an interactive
       Service Credits Estimator.

       Site Reference: https://developers.arcgis.com/rest/analysis/

       Inputs:
          securityHandler - ArcGIS Online security handler object
          url - optional url to the site.
             ex: http://www.arcgis.com/sharing/rest
          proxy_url - optional proxy IP
          proxy_port - optional proxy port required if proxy_url specified
       Basic Usage:

        username = "username"
        password = "password"
        con = Connection(baseurl="http://www.arcgis.com/sharing/rest",product_type="AGO",
                         security_method="BUILT-IN", username=username, password=password)
        a = analysis(connection=con, url=None)
        for task in a.tasks:
            if task.name.lower() == "aggregatepoints":
                for params in task.parameters:
                    print( params)
    """
    _proxy_url = None
    _proxy_port = None
    _url = None
    _analysis_url = None
    _securityHandler = None
    _gpService = None
    #----------------------------------------------------------------------
    def __init__(self,
                 connection,
                 url=None):
        """Constructor"""
        if url is None:
            self._url = "https://www.arcgis.com/sharing/rest"
        else:
            if url.find("/sharing/rest") == -1:
                url = url + "/sharing/rest"
            self._url = url
        self._con = connection
        self.__init_url(connection)
    #----------------------------------------------------------------------
    def __init_url(self, connection=None):
        """loads the information into the class"""
        if connection is None:
            self._con = connection
        portals_self_url = "{}/portals/self".format(self._url)
        params = {
            "f" :"json"
        }
        res = self._con.get(path_or_url=portals_self_url,
                           params=params)
        if "helperServices" in res:
            helper_services = res.get("helperServices")
            if "analysis" in helper_services:
                analysis_service = helper_services.get("analysis")
                if "url" in analysis_service:
                    self._analysis_url = analysis_service.get("url")
        self._gpService = GPService(connection=self._con,
                                    url=self._analysis_url,
                                    initialize=False)
    #----------------------------------------------------------------------
    @property
    def gpService(self):
        """returns the geoprocessing object"""
        if self._gpService is None:
            self.__init_url()
        return self._gpService
    #----------------------------------------------------------------------
    @property
    def tasks(self):
        """returns the available analysis tasks"""
        if self._gpService is None:
            self.__init_url()
        try:
            return self.gpService.tasks
        except:
            return None

