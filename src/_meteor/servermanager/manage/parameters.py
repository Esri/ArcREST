import json

########################################################################
class Extension(object):
    """
    represents a service extension
    """
    _typeName = None
    _capabilities = None
    _enabled = None
    _maxUploadFileSize = None
    _allowedUploadFileTypes = None
    _properties = None
    _allowedExtensions = ["naserver", "mobileserver",
                          "kmlserver", "wfsserver",
                          "schematicsserver", "featureserver",
                          "wcsserver", "wmsserver"]
    #----------------------------------------------------------------------
    def __init__(self, typeName,
                 capabilities,
                 enabled,
                 maxUploadFileSize,
                 allowedUploadFileType,
                 properties):
        """Constructor"""
        self._typeName = typeName
        self._capabilities = capabilities
        self._enabled = enabled
        self._maxUploadFileSize = maxUploadFileSize
        self._allowedUploadFileTypes = allowedUploadFileType
        self._properties = properties
    #----------------------------------------------------------------------
    @property
    def properties(self):
        """gets/sets the extension properties"""
        return self._properties
    #----------------------------------------------------------------------
    @properties.setter
    def properties(self, value):
        """gets/sets the extension properties"""
        if isinstance(value, dict):
            self._properties = value
    #----------------------------------------------------------------------
    @property
    def typeName(self):
        """gets the extension type"""
        return self._typeName
    #----------------------------------------------------------------------
    @property
    def capabilities(self):
        """gets/sets the capabilities"""
        return self._capabilities
    #----------------------------------------------------------------------
    @capabilities.setter
    def capabilities(self, value):
        """gets/sets the capabilities"""
        if self._capabilities != value:
            self._capabilities = value
    #----------------------------------------------------------------------
    @property
    def enabled(self):
        """gets/sets the extension is enabled"""
        return self._enabled
    #----------------------------------------------------------------------
    @enabled.setter
    def enabled(self, value):
        """gets/sets the extension is enabled"""
        if isinstance(value, bool):
            self._enabled = value
    #----------------------------------------------------------------------
    @property
    def maxUploadFileSize(self):
        """sets/gets the maxUploadFileSize"""
        return self._maxUploadFileSize
    #----------------------------------------------------------------------
    @maxUploadFileSize.setter
    def maxUploadFileSize(self, value):
        """sets/gets the maxUploadFileSize"""
        if isinstance(value, int):
            self._maxUploadFileSize = value
    #----------------------------------------------------------------------
    @property
    def allowedUploadFileTypes(self):
        """gets/sets the allowedUploadFileTypes"""
        return self._allowedUploadFileTypes
    #----------------------------------------------------------------------
    @allowedUploadFileTypes.setter
    def allowedUploadFileTypes(self, value):
        """gets/sets the allowedUploadFileTypes"""
        self._allowedUploadFileTypes = value
    #----------------------------------------------------------------------
    def __str__(self):
        """returns the object as JSON"""
        return json.dumps({
            "typeName": self._typeName,
            "capabilities": self._capabilities,
            "enabled": self._enabled,
            "maxUploadFileSize": self._maxUploadFileSize,
            "allowedUploadFileTypes": self._allowedUploadFileTypes,
            "properties": self._properties
        })
    #----------------------------------------------------------------------
    @property
    def value(self):
        """returns the object as a dictionary"""
        return json.loads(str(self))

    #----------------------------------------------------------------------
    @staticmethod
    def fromJSON(value):
        """returns the object from json string or dictionary"""
        if isinstance(value, str):
            value = json.loads(value)
        elif isinstance(value, dict): pass
        else:
            raise AttributeError("Invalid input")
        return Extension(typeName=value['typeName'],
                         capabilities=value['capabilities'],
                         enabled=value['enabled'] == "true",
                         maxUploadFileSize=value['maxUploadFileSize'],
                         allowedUploadFileType=value['allowedUploadFileTypes'],
                         properties=value['properties'])
########################################################################
class ClusterProtocol(object):
    """
    The clustering protocol defines a channel which is used by server
    machines within a cluster to communicate with each other. A server
    machine will communicate with its peers information about the status of
    objects running within it for load balancing and fault tolerance.
    ArcGIS Server supports the TCP clustering protocols where server
    machines communicate with each other over a TCP channel (port).

    Inputs:
       tcpClusterPort - The port to use when configuring a TCP based
       protocol. By default, the server will pick up the next value in the
       assigned ports on all machines.
    """
    _tcpClusterPort = None
    #----------------------------------------------------------------------
    def __init__(self, tcpClusterPort):
        """Constructor"""
        self._tcpClusterPort = int(tcpClusterPort)
    #----------------------------------------------------------------------
    @property
    def tcpClusterPort(self):
        """
        The port to use when configuring a TCP based protocol. By default,
        the server will pick up the next value in the assigned ports on
        all machines.
        """
        return self._tcpClusterPort
    #----------------------------------------------------------------------
    def __str__(self):
        """"""
        return json.dumps({
            "tcpClusterPort" : self._tcpClusterPort
        })
    #----------------------------------------------------------------------
    @property
    def value(self):
        """
        returns the tcpClusterPort as a dictionary
        """
        return {
            "tcpClusterPort" : self._tcpClusterPort
        }






