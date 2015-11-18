from __future__ import absolute_import
from ...ags._geoprocessing import *
from ...common.geometry import Polygon, Polyline, Point, SpatialReference, Envelope
from ..._abstract import abstract

########################################################################
class elevationSync(abstract.BaseAGOLClass):
    """
    These are synchronus gp tasks.

    The Elevation Analysis services provide a group of capabilities for
    performing analytical operations against data hosted and managed by
    Esri. This allows you to perform certain common analytical tasks
    quickly and easily, without having to collect, maintain, or update an
    authoritative set of base data. That's done for you.

    Inputs:
       securityHandler - arcgis online security handler
       url - orginization url
          ex: http://www.arcgis.com
       proxy_url - IP/address of proxy
       proxy_port - port # of proxy is on.
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _service_url = None
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
        res = self._do_get(url=portals_self_url,
                           param_dict=params,
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
        if "helperServices" in res:
            helper_services = res.get("helperServices")
            if "elevationSync" in helper_services:
                analysis_service = helper_services.get("elevation")
                if "url" in analysis_service:
                    self._analysis_url = analysis_service.get("url")
        self._gpService = GPService(url=self._analysis_url,
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port,
                                    initialize=False)
    #----------------------------------------------------------------------
    @property
    def tasks(self):
        """returns a list of GPTask objects for GPService"""
        if self._gpService is None:
            self.__init_url()
        return self._gpService.tasks
    #----------------------------------------------------------------------
    @property
    def gpService(self):
        """returns the geoprocessing service object"""
        if self._gpService is None:
            self.__init_url()
        return self._gpService

########################################################################
class elevation(abstract.BaseAGOLClass):
    """
    The Elevation Analysis services provide a group of capabilities for
    performing analytical operations against data hosted and managed by
    Esri. This allows you to perform certain common analytical tasks
    quickly and easily, without having to collect, maintain, or update an
    authoritative set of base data. That's done for you.

    Inputs:
       securityHandler - arcgis online security handler
       url - orginization url
          ex: http://www.arcgis.com
       proxy_url - IP/address of proxy
       proxy_port - port # of proxy is on.
    """
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None
    _service_url = None
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
        res = self._do_get(url=portals_self_url,
                           param_dict=params,
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
        if "helperServices" in res:
            helper_services = res.get("helperServices")
            if "elevation" in helper_services:
                analysis_service = helper_services.get("elevation")
                if "url" in analysis_service:
                    self._analysis_url = analysis_service.get("url")
        self._gpService = GPService(url=self._analysis_url,
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port,
                                    initialize=False)
    #----------------------------------------------------------------------
    @property
    def tasks(self):
        """returns a list of GPTask objects for GPService"""
        if self._gpService is None:
            self.__init_url()
        return self._gpService.tasks
    #----------------------------------------------------------------------
    @property
    def gpService(self):
        """returns the geoprocessing service object"""
        if self._gpService is None:
            self.__init_url()
        return self._gpService

