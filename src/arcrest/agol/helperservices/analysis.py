from __future__ import absolute_import
from ...ags._geoprocessing import *
from ..._abstract import abstract
########################################################################
class analysis(abstract.BaseAGOLClass):
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
        import arcrest
        import arcrest.agol as agol

        if __name__ == "__main__":
            username = "username"
            password = "password"
            sh = arcrest.AGOLTokenSecurityHandler(username, password)
            a = agol.analysis(securityHandler=sh)
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
                 securityHandler,
                 url=None,
                 proxy_url=None,
                 proxy_port=None):
        """Constructor"""
        if url is None:
            self._url = "https://www.arcgis.com/sharing/rest"
        else:
            if url.find("/sharing/rest") == -1:
                url = url + "/sharing/rest"
            self._url = url
        self._securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self.__init_url()
    #----------------------------------------------------------------------
    def __init_url(self):
        """loads the information into the class"""
        portals_self_url = "{}/portals/self".format(self._url)
        params = {
            "f" :"json"
        }
        res = self._get(url=portals_self_url,
                           param_dict=params,
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
        if "helperServices" in res:
            helper_services = res.get("helperServices")
            if "analysis" in helper_services:
                analysis_service = helper_services.get("analysis")
                if "url" in analysis_service:
                    self._analysis_url = analysis_service.get("url")
        self._gpService = GPService(url=self._analysis_url,
                  securityHandler=self._securityHandler,
                  proxy_url=self._proxy_url,
                  proxy_port=self._proxy_port,
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
        return self.gpService.tasks

