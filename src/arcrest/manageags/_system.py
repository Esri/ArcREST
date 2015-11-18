from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseAGSServer
import json
########################################################################
class System(BaseAGSServer):
    """
    The System resource is a collection of miscellaneous server-wide
    resources such as server properties, server directories, the
    configuration store, Web Adaptors, and licenses.
    """
    _json = None
    _json_dict = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _url = None
    _resources = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        self._securityHandler = securityHandler
        if url.lower().endswith("/system"):
            self._url = url
        else:
            self._url = url + "/system"
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json = json.dumps(json_dict)
        self._json_dict = json_dict
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in System.")
            del k
            del v
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        return json.dumps(self._json)
    #----------------------------------------------------------------------
    @property
    def resources(self):
        """gets the resources"""
        if self._resources is None:
            self.__init()
        return self._resources
    #----------------------------------------------------------------------
    @property
    def serverProperties(self):
        """gets the server properties for the site as an object"""
        return ServerProperties(url=self._url + "/properties",
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                               proxy_port=self._proxy_port,
                               initialize=True)
    #----------------------------------------------------------------------
    @property
    def serverDirectories(self):
        """returns the server directory object in a list"""
        directs = []
        url = self._url + "/directories"
        params = {
            "f" : "json"
        }
        res = self._do_get(url=url,
                           param_dict=params,
                           securityHandler=self._securityHandler,
                           proxy_url=self._proxy_url,
                           proxy_port=self._proxy_port)
        for direct in res['directories']:
            url = url + "/%s" % direct["name"]
            directs.append(
                ServerDirectory(url=url,
                                securityHandler=self._securityHandler,
                                proxy_url=self._proxy_url,
                                proxy_port=self._proxy_port,
                                initialize=True))
        return directs
    #----------------------------------------------------------------------
    @property
    def licenses(self):
        """
        The licenses resource lists the current license level of ArcGIS for
        Server and all authorized extensions. Contact Esri Customer Service
        if you have questions about license levels or expiration properties.
        """
        url = self._url + "/licenses"
        params = {
            "f" : "json"
        }

        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def Jobs(self):
        """get the Jobs object"""
        url = self._url + "/jobs"
        return Jobs(url=url,
                    securityHandler=self._securityHandler,
                    proxy_url=self._proxy_url,
                    proxy_port=self._proxy_port,
                    initialize=True)
    #----------------------------------------------------------------------
    @property
    def webAdaptors(self):
        """
        This operation lists all the Web Adaptors that have been registered
        with the site. The server will trust all these Web Adaptors and
        will authorize calls from these servers.
        To configure a new Web Adaptor with the server, you'll need to use
        the configuration web page or the command line utility. For full
        instructions, see Configuring the Web Adaptor after installation.
        """
        url = self._url + "/webadaptors"
        params = {
            "f" : "json"
        }
        return self._do_get(url=url, param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def webAdaptorsConfiguration(self):
        """
        The Web Adaptors configuration is a resource for all the
        configuration parameters shared across all the Web Adaptors in the
        site. Most importantly, this resource lists the shared key that is
        used by all the Web Adaptors to encrypt key data bits in the
        incoming requests to the server.
        """
        url = self._url + "/webadaptors/config"
        params = {
            "f" : "json"
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def updateWebAdaptorsConfiguration(self, webAdaptorConfig):
        """
        You can use this operation to change the configuration parameters
        and shared key.

        Inputs:
           webAdaptorConfig - the sharedkey attribute must always be
            present in this JSON
        """
        url = self._url + "/webadaptors/config/update"
        params = {
            "f" : "json",
            "webAdaptorConfig" : webAdaptorConfig
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    @property
    def configurationStore(self):
        """returns the ConfigurationStore object for this site"""
        url = self._url + "/configstore"

        return ConfigurationStore(url=url,
                                  securityHandler=self._securityHandler,
                                  proxy_url=self._proxy_url,
                                  proxy_port=self._proxy_port)
########################################################################
class ConfigurationStore(BaseAGSServer):
    """"""
    _url = None
    _proxy_url = None
    _json = None
    _proxy_port = None
    _securityHandler = None
    _json_dict = None
    _type = None
    _connectionString = None
    _class = None
    _status = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self.securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
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
            if k == "class":
                self._class = v
            elif k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in Configuration store.")
            del k
            del v
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        return json.dumps(self._json)
    #----------------------------------------------------------------------
    @property
    def type(self):
        """gets the configuration store type"""
        if self._type is None:
            self.__init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def connectionString(self):
        """gets the connection string"""
        if self._connectionString is None:
            self.__init()
        return self._connectionString
    #----------------------------------------------------------------------
    @property
    def classValue(self):
        """gets the class value"""
        if self._class is None:
            self.__init()
        return self._class
    #----------------------------------------------------------------------
    @property
    def status(self):
        """gets the status value"""
        if self._status is None:
            self.__init()
        return self._status
    #----------------------------------------------------------------------
    def edit(self, typeValue,
             connectionString,
             move=True,
             runAsync=False):
        """
        You can use this operation to update the configuration store.
        Typically, this operation is used to change the location of the
        store.
        When ArcGIS Server is installed, the default configuration store
        uses local paths. As the site grows (more server machines are
        added), the location of the store must be updated to use a shared
        file system path. On the other hand, if you know at the onset that
        your site will have two or more server machines, you can start from
        a shared path while creating a site and skip this step altogether.

        Inputs:
           typeValue - Type of the configuration store. Values: FILESYSTEM
           connectionString - A file path or connection URL to the physical
            location of the store.
           move - default True - A boolean to indicate if you want to move
            the content of the current store to the new store.
           runAsync - default False - Decides if this operation must run
            asynchronously.
        """
        url = self._url + "/edit"
        params = {
            "f" : "json",
            "type" : typeValue,
            "connectionString" : connectionString,
            "move" : move,
            "runAsync" : runAsync
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
########################################################################
class Jobs(BaseAGSServer):
    """
    This resource is a collection of all the administrative jobs
    (asynchronous operations) created within your site. When operations
    that support asynchronous execution are run, the server creates a new
    job entry that can be queried for its current status and messages.
    """
    _json = None
    _jobs = None
    _json_dict = None
    _url = None
    _securityHandler = None
    _proxy_url = None
    _proxy_port = None

    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        self._proxy_url = proxy_url
        self._proxy_port = proxy_port
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ populates server admin information """
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json = json.dumps(json_dict)
        self._json_dict = json_dict
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print( k, " - attribute not implemented in Jobs.")
            del k
            del v
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        return json.dumps(self._json)
    #----------------------------------------------------------------------
    @property
    def jobs(self):
        """gets the job ids"""
        if self._jobs is None:
            self.__init()
        return self._jobs
    #----------------------------------------------------------------------
    def getJobDetails(self, jobId):
        """
        A job represents the asynchronous execution of an operation. You
        can acquire progress information by periodically querying the job.

        Inputs:
           jobId - id of the job
        """
        url = self._url + "/%s" % jobId
        params = {
            "f" : "json"
        }
        return self._do_get(url=url,
                            param_dict=params,
                            securityHandler=self._securityHandler,
                            proxy_url=self._proxy_url,
                            proxy_port=self._proxy_port)
########################################################################
class ServerProperties(BaseAGSServer):
    """
    The Server has configuration parameters that can be govern some of its
    intricate behavior. The Server Properties resource is a container for
    such properties. These properties are available to all server objects
    and extensions through the server environment interface.
    The properties include:
     CacheSizeForSecureTileRequests - An integer that specifies the
      number of users whose token information will be cached. This
      increases the speed of tile retrieval for cached services. If not
      specified, the default cache size is 200,000. Both REST and SOAP
      services honor this property. You'll need to manually restart
      ArcGIS Server in order for this change to take effect.
     DisableAdminDirectoryCache - Disables browser caching of the
      Administrator Directory pages. The default is false. To disable
      browser caching, set this property to true.
     disableIPLogging - When a possible cross-site request forgery
      (CSRF) attack is detected, the server logs a message containing
      the possible IP address of the attacker. If you do not want IP
      addresses listed in the logs, set this property to true. Also,
      HTTP request referrers are logged at FINE level by the REST and
      SOAP handlers unless this property is set to true.
     javaExtsBeginPort - Specifies a start port of the port range used
      for debugging Java server object extensions.
      Example: 8000
     javaExtsEndPort - Specifies an end port of the port range used for
      debugging Java server object extensions.
      Example: 8010
     localTempFolder - Defines the local folder on a machine that can
      be used by GIS services and objects. If this property is not
      explicitly set, the services and objects will revert to using the
      system's default temporary directory.

      Note:
      If this property is used, you must create the temporary directory
      on every server machine in the site. Example: /tmp/arcgis.

      messageFormat - Defines the transmission protocol supported by
       the services catalog in the server.
       Values: esriServiceCatalogMessageFormatBin,
               esriServiceCatalogMessageFormatSoap,
               esriServiceCatalogMessageFormatSoapOrBin
      messageVersion - Defines the version supported by the services
       catalog in the server. Example: esriArcGISVersion101
      PushIdentityToDatabase - Propogates the credentials of the logged
       -in user to make connections to an Oracle database. This
       property is only supported for use with Oracle databases.
       Values: true | false
      suspendDuration - Specifies the duration for which the ArcGIS
       service hosting processes should suspend at startup. This
       duration is specified in milliseconds. This is an optional
       property that takes effect when suspendServiceAtStartup is set
       to true. If unspecified and suspension of service at startup is
       requested, then the default suspend duration is 30 seconds.
       Example: 10000 (meaning 10 seconds)
      suspendServiceAtStartup - Suspends the ArcGIS service hosting
       processes at startup. This will enable attaching to those
       processes and debugging code that runs early in the lifecycle of
       server extensions soon after they are instantiated.
       Values: true | false
      uploadFileExtensionWhitelist - This specifies what files are
       allowed to be uploaded through the file upload API by
       identifying the allowable extensions. It is a list of comma
       separated extensions without dots. If this property is not
       specified a default list is used. This is the default list: soe,
       sd, sde, odc, csv, txt, zshp, kmz, and geodatabase.

     Note:
     Updating this list overrides the default list completely. This
     means if you set this property to a subset of the default list
     then only those items in the subset will be accepted for upload.
     Example: sd, so, sde, odc.

     uploadItemInfoFileExtensionWhitelist - This specifies what files
      are allowed to be uploaded through the service iteminfo upload
      API by identifying the allowable extensions. It should be a list
      of comma separated extensions without dots. If this property is
      not specified a default list is used. This is the default list:
      xml, img, png, gif, jpg, jpeg, bmp.

    Note:
    This list overrides the default list completely. This means if you
    set this property to a subset of the default list then only those
    items in the subset will be accepted for upload. Example: png, svg,
    gif, jpg, tiff, bmp.

    WebContextURL - Defines the web front end as seen by your users.
     Example: http://mycompany.com/gis
    """
    _url = None
    _json = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
                 initialize=False):
        """Constructor"""
        if url.lower().endswith('/properties'):
            self._url = url
        else:
            self._url = url + "/properties"
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
                print( k, " - attribute not implemented in ServerProperties.")
            del k
            del v
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        return json.dumps(self._json)
    #----------------------------------------------------------------------
    def updateServerProperties(self, properties):
        """
        This operation allows you to update the server property
        """
        url = self._url + "/update"
        params = {
            "f" : "json",
            "properties" : properties
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
########################################################################
class ServerDirectory(BaseAGSServer):
    """
    Server directories are used by GIS services as a location to output
    items such as map images, tile caches, and geoprocessing results. In
    addition, some directories contain configurations that power the GIS
    services.
    In a Site with more than one server machine these directories must be
    available on network shares, accessible to every machine in the site.

    The following directory types can be registered with the server:
     Output - Stores various information generated by services, such as map
      images. Instances: One or more
     Cache - Stores tile caches used by map, globe, and image services for
      rapid performance. Instances: One or more
     Jobs - Stores results and other information from geoprocessing
      services. Instances: One or more
     System - Stores files that are used internally by the GIS server.
      Instances: One Server directories that contain output of various GIS
      services can be periodically cleaned to remove old unused files. By
      using the cleanup mode and maximum file age parameters, you control
      when when you would like the files in these directories to be
      cleaned.

    All the output server directories are automatically virtualized (they
    can be accessed over a URL) for you through the ArcGIS Server REST API.
    """
    _json = None
    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _url = None
    _name = None
    _physicalPath = None
    _directoryType = None
    _cleanupMode = None
    _maxFileAge = None
    _description = None
    _virtualPath = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler,
                 proxy_url=None,
                 proxy_port=None,
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
                print( k, " - attribute not implemented in ServerDirectory.")
            del k
            del v
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as a string"""
        return json.dumps(self._json)
    #----------------------------------------------------------------------
    @property
    def name(self):
        """gets the directory name"""
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def physicalPath(self):
        """gets the physical path"""
        if self._physicalPath is None:
            self.__init()
        return self._physicalPath
    #----------------------------------------------------------------------
    @property
    def directoryType(self):
        """gets the directoryType value"""
        if self._directoryType is None:
            self.__init()
        return self._directoryType
    #----------------------------------------------------------------------
    @property
    def cleanupMode(self):
        """gets the cleanupMode value"""
        if self._cleanupMode is None:
            self.__init()
        return self._cleanupMode
    #----------------------------------------------------------------------
    @property
    def maxFileAge(self):
        """gets the maxFileAge value"""
        if self._maxFileAge is None:
            self.__init()
        return self._maxFileAge
    #----------------------------------------------------------------------
    @property
    def description(self):
        """gets the description value"""
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def virtualPath(self):
        """gets the virtualPath value"""
        if self._virtualPath is None:
            self.__init()
        return self._virtualPath
    #----------------------------------------------------------------------
    def edit(self,
             physicalPath,
             cleanupMode,
             maxFileAge,
             description):
        """
        The server directory's edit operation allows you to change the path
        and clean up properties of the directory. This operation updates
        the GIS service configurations (and points them to the new path)
        that are using this directory, causing them to restart. It is
        therefore recommended that any edit to the server directories be
        performed when the server is not under load.
        This operation is mostly used when growing a single machine site to
        a multiple machine site configuration, which requires that the
        server directories and configuration store be put on a
        network-accessible file share.

        Inputs:
           physicalPath - The absolute physical path of the server
            directory.
           cleanupMode - Defines if files in the server directory needs to
            be cleaned up. The default is NONE.
           maxFileAge - Defines how long a file in the directory needs to
            be kept before it is deleted.
           description - An optional description for the server directory
        """
        url = self._url + "/edit"
        params = {
            "f" : "json",
            "physicalPath" : physicalPath,
            "cleanupMode" : cleanupMode,
            "maxFileAge" : maxFileAge,
            "description" : description
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def clean(self):
        """
        Cleans the content (files and folders) within the directory that
        have passed their expiration date. Every server directory has the
        max file age and cleanup mode parameter that govern when a file
        created inside is supposed to be cleaned up. The server directory
        cleaner automatically cleans up the content within server
        directories at regular intervals. However, you can explicitly clean
        the directory by invoking this operation.
        """
        url = self._url + "/clean"
        params = {
            "f" : "json"
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
    #----------------------------------------------------------------------
    def unregisterDirectory(self):
        """
        Unregisters a server directory. Once a directory has been
        unregistered, it can no longer be referenced (used) from within a
        GIS service.
        """
        url = self._url + "/unregister"
        params = {
            "f" : "json"
        }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
