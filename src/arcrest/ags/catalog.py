from base import BaseAGSServer
from featureservice import FeatureService
from mapservice import MapService
from mobileservice import MobileService
from imageservice import ImageService
from gpservice import GPService
from geometryservice import GeometryService
from naservice import NAService
from geocodeservice import GeocodeService
from globeservice import GlobeService
from geodataservice import GeoDataService
import os
import sys

########################################################################
class Catalog(BaseAGSServer):
    """
       The Catalog resource is the root node and initial entry point into
       an ArcGIS Server host. This resource represents a catalog of folders
       and services published on the host.
       The current version of the server is also returned in the response
       (introduced at 9.3.1). The value of the version is a number such
       that its value at a future release is guaranteed to be greater than
       its value at a previous release.
    """
    _token = None
    _token_url = None
    _username = None
    _password = None
    _url = None
    _currentURL = None
    _acceptLanguage = None
    _currentVersion = None
    _resources = None
    _fullVersion = None
    _folders = None
    _services = None
    _currentVersion = None
    _folder = None
    #   Service Holders
    _mapServices = None
    _geoCodeService = None
    _gpService = None
    _geometryService = None
    _imageService = None
    _networkService = None
    _featureService = None
    _geoDataService = None
    _globeService = None
    _mobileService = None
    #----------------------------------------------------------------------
    def __init__(self, url, token_url=None, username=None, password=None, proxy_url=None, proxy_port=None):
        """Constructor
            Inputs:
               url - admin url
               token_url - url to generate token
               username - admin username
               password - admin password
        """
        self._url = url
        self._currentURL = url
        if self.token_url is not None:
            self._token_url = token_url
            self._username = username
            self._password = password
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
        self.__init()
        self._populateServices()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json",

        }
        if self._token is not None:
            params["token"] = self._token
        json_dict = self._do_get(url=self._currentURL, param_dict=params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k == "folders":
                if self._folders is None:
                    setattr(self, "_"+ k, v)
            elif k in attributes and \
                 k not in ('folders'):
                setattr(self, "_"+ k, v)
            else:
                print k, " - attribute not implmented."
            del k
            del v
    @property
    def folders(self):
        if self._folders is None:
            self.__init()
        return self._folders
    @property
    def currentVersion(self):
        if self._currentVersion is None:
            self._currentVersion
        return self._currentVersion
    @property
    def services(self):
        if self._services is None:
            self.__init()
        return self._services
    @property
    def folder(self):
        return self._folder
    @folder.setter
    def folder(self, folder):
        if folder in self.folders:
            self._currentURL = self._url + "/%s" % folder
            self._folder = folder
            self._services = None
            self._populateServices()
        elif folder == "" or folder == "root":
            self.currentURL = self._url
            self._folder = folder
            self._services = None
            self._populateServices()
    #----------------------------------------------------------------------
    @property
    def gpServices(self):
        """ returns all geoprocessing services in the current folder """
        if self._gpService is None:
            self._populateServices()
        return self._gpService
    #----------------------------------------------------------------------
    @property
    def geocodeServices(self):
        """ returns all geocoding services in the current folder """
        if self._geoCodeService is None:
            self._populateServices()
        return self._geoCodeService
    #----------------------------------------------------------------------
    @property
    def naServices(self):
        """ returns the NA services in the current folder """
        if self._networkService is None:
            self._populateServices
        return self._networkService
    #----------------------------------------------------------------------
    @property
    def mapServices(self):
        """ returns the map services in the current folder """
        if self._mapServices is None:
            self._populateServices
        return self._mapServices
    #----------------------------------------------------------------------
    @property
    def featureServices(self):
        """ returns the feature services in the current folder """
        if self._featureService is None:
            self._populateServices
        return self._featureService
    #----------------------------------------------------------------------
    @property
    def geometryService(self):
        """ returns the geometry service in the current folder """
        if self._geometryService is None:
            self._populateServices
        return self._geometryService
    #----------------------------------------------------------------------
    @property
    def imageServices(self):
        """ returns all the image services in the current folder """
        if self._imageService is None:
            self._populateServices
        return self._imageService
    #----------------------------------------------------------------------
    @property
    def mobileServices(self):
        """ returns the mobile services in the current folder """
        if self._mobileService is None:
            self._populateServices
        return self._mobileService
    #----------------------------------------------------------------------
    @property
    def globeServices(self):
        """ returns the globe services in the current folder """
        if self._globeService is None:
            self._populateServices
        return self._globeService
    #----------------------------------------------------------------------
    @property
    def geodataServices(self):
        """ returns all geodata services in the current folder """
        if self._geoDataService is None:
            self._populateServices
        return self._geoDataService
    #----------------------------------------------------------------------
    def _populateServices(self):
        """
           Populates all the service type properties.
        """
        self._mapServices = [] #
        self._geoCodeService = []
        self._gpService = [] #
        self._geometryService = []
        self._imageService = [] #
        self._networkService = []
        self._featureService = [] #
        self._geoDataService = []
        self._globeService = []
        self._mobileService = [] #
        for service in self.services:
            url = "%s/%s/%s" % (
                self._currentURL,
                service['name'].split("/")[len(service['name'].split("/"))-1],
                service['type']
            )
            if service['type'] == "FeatureServer":
                self._featureService.append(
                    FeatureService(
                        url=url,
                        username=self._username,
                        password=self._password,
                        token_url=self._token_url
                    )
                )
            elif service['type'] == "GPServer":
                self._gpService.append(
                    GPService(
                        url=url,
                        username=self._username,
                        password=self._password,
                        token_url=self._token_url
                    )
                )
            elif service['type'] == "MapServer":
                self._mapServices.append(
                    MapService(
                        url=url,
                        username=self._username,
                        password=self._password,
                        token_url=self._token_url
                    )
                )
            elif service['type'] == "ImageServer":
                self._imageService.append(
                    ImageService(url=url,
                                    username=self._username,
                                    password=self._password,
                                    token_url=self._token_url
                                    )
                )
            elif service['type'] == "MobileServer":
                self._mobileService.append(
                    MobileService(
                        url=url,
                        username=self._username,
                        password=self._password,
                        token_url=self._token_url
                    )
                )
            elif service['type'] == "GeometryServer":
                self._geometryService.append(
                    GeometryService(
                        url=url,
                        username=self._username,
                        password=self._password,
                        token_url=self._token_url
                    )
                )
            elif service['type'] == "GlobeServer":
                self._globeService.append(
                    GlobeService(
                        url=url,
                        username=self._username,
                        password=self._password,
                        token_url=self._token_url
                    )
                )
            elif service['type'] == "GeocodeServer":
                self._geoCodeService.append(
                    GeocodeService(
                        url=url,
                        username=self._username,
                        password=self._password,
                        token_url=self._token_url
                    )
                )
            elif service['type'] == "NAServer":
                self._networkService.append(
                    NAService(
                        url=url,
                        username=self._username,
                        password=self._password,
                        token_url=self._token_url
                    )
                )
            elif service['type'] == "GeoDataServer":
                self._networkService.append(
                    GeoDataService(
                        url=url,
                        username=self._username,
                        password=self._password,
                        token_url=self._token_url
                    )
                )




