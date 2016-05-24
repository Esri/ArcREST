from __future__ import absolute_import
from ...services.geoprocessing._geoprocessing import *
from ...common.geometry import Polygon, Polyline, Point, SpatialReference, Envelope
########################################################################
class hydrology(object):
    """
    The data being operated on are maintained by Esri and made available to
    you through these tasks. A primary benefit of using these data sources
    is that a lot of the hard work has already been done, freeing you up to
    just work on performing analysis instead of having to worry about
    compiling, processing and storing very large datasets of continental
    and global scales on your local machine or network.

    Find out more here:
    https://developers.arcgis.com/rest/elevation/api-reference/source-data-for-hydrology-analysis-tasks.htm

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
            if "hydrology" in helper_services:
                analysis_service = helper_services.get("elevation")
                if "url" in analysis_service:
                    self._analysis_url = analysis_service.get("url")
        self._gpService = GPService(connection=self._con,
                                    url=self._analysis_url,
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