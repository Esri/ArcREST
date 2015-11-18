from __future__ import absolute_import
from __future__ import print_function
from .._abstract.abstract import BaseAGSServer
import json
########################################################################
class GeoDataService(BaseAGSServer):
    """
    Represents a single mobile service layer
    """
    _url = None
    _proxy_url = None
    _proxy_port = None
    _securityHandler = None
    _json = None
    _json_dict = None
    _replicasResource = None
    _defaultWorkingVersion = None
    _workspaceType = None
    _replicas = None
    _serviceDescription = None
    _versions = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 securityHandler=None,
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
        """ inializes the properties """
        params = {
            "f" : "json",
        }
        json_dict = self._do_get(self._url, params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        self._json_dict = json_dict
        self._json = json.dumps(self._json_dict)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                if k == "versions" and json_dict[k]:
                    self._versions = []
                    for version in v:
                        self._versions.append(
                            Version(url=self._url + "/versions/%s" % version,
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port,
                                    initialize=False))
                elif k == "replicas" and json_dict[k]:
                    self._replicas = []
                    for version in v:
                        self._replicas.append(
                            Replica(url=self._url + "/replicas/%s" % version,
                                    securityHandler=self._securityHandler,
                                    proxy_url=self._proxy_url,
                                    proxy_port=self._proxy_port,
                                    initialize=False))
                else:
                    setattr(self, "_"+ k, v)
            else:
                print (k, " - attribute not implemented for GeoData Service")
    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """
        returns key/value pair
        """
        attributes = json.loads(str(self))
        for att in attributes.keys():
            yield [att, getattr(self, att)]
    #----------------------------------------------------------------------
    @property
    def defaultWorkingVersion(self):
        """returns the default working version name"""
        if self._defaultWorkingVersion is None:
            self.__init()
        return self._defaultWorkingVersion
    #----------------------------------------------------------------------
    @property
    def workspaceType(self):
        """returns the workspace type"""
        if self._workspaceType is None:
            self.__init()
        return self._workspaceType
    #----------------------------------------------------------------------
    @property
    def replicas(self):
        """returns a list of replices"""
        if self._replicas is None:
            self.__init()
        return self._replicas
    #----------------------------------------------------------------------
    @property
    def replicasResource(self):
        """returns a list of replices"""
        if self._replicasResource is None:
            self._replicasResource = {}
            for replica in self.replicas:
                self._replicasResource["replicaName"] = replica.name
                self._replicasResource["replicaID"] = replica.guid
        return self._replicasResource
    #----------------------------------------------------------------------
    @property
    def serviceDescription(self):
        """returns the service description"""
        if self._serviceDescription is None:
            self.__init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def versions(self):
        """returns a list of the versions"""
        if self._versions is None:
            self.__init()
        return self._versions
    #----------------------------------------------------------------------
    def unRegisterReplica(self,replicaGUID):
        """ unRegisterReplica operation is performed on a Geodata Service
        resource (POST only). This operation unregisters a replica on the
        geodata service. Unregistering a replica is only supported when
        logged in as an admin user. You can provide arguments to the
        unRegisterReplica operation.
        Inputs:
            replicaID - The ID of the replica. The ID of a replica can be
                        found by accessing the Geodata Service Replicas
                        resource. """

        url = self._url + "/unRegisterReplica"
        params = { "f" : "json",
                   "replicaID" : replicaGUID
                 }
        return self._do_post(url=url,
                             param_dict=params,
                             securityHandler=self._securityHandler,
                             proxy_url=self._proxy_url,
                             proxy_port=self._proxy_port)
########################################################################
class Version(BaseAGSServer):
    """represents a version in a geodata service"""

    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _url = None
    _json = None

    _name = None
    _description = None
    _created = None
    _modified = None
    _access = None
    _parentVersion = None
    _childVersions = None
    _ancestorVersions = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print (k, " - attribute not implemented in Version.")
            del k,v

    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """
        returns key/value pair
        """
        attributes = json.loads(str(self))
        for att in attributes.keys():
            yield [att, getattr(self, att)]

    #----------------------------------------------------------------------
    @property
    def name(self):
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def description(self):
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def created(self):
        if self._created is None:
            self.__init()
        return self._created
    #----------------------------------------------------------------------
    @property
    def modified(self):
        if self._modified is None:
            self.__init()
        return self._modified
    #----------------------------------------------------------------------
    @property
    def access(self):
        if self._access is None:
            self.__init()
        return self._access
    #----------------------------------------------------------------------
    @property
    def parentVersion(self):
        if self._parentVersion is None:
            self.__init()
        return self._parentVersion
    #----------------------------------------------------------------------
    @property
    def childVersions(self):
        if self._childVersions is None:
            self.__init()
        return self._childVersions
    #----------------------------------------------------------------------
    @property
    def ancestorVersions(self):
        if self._ancestorVersions is None:
            self.__init()
        return self._ancestorVersions

########################################################################
class Replica(BaseAGSServer):
    """represents a replica in a geodata service"""

    _securityHandler = None
    _proxy_port = None
    _proxy_url = None
    _url = None

    _name = None
    _id = None
    _replicaVersion = None
    _guid = None
    _role = None
    _replicaOwner = None
    _serviceName = None
    _accessType = None
    _myGenerationNumber = None
    _sibGenerationNumber = None
    _sibMyGenerationNumber = None
    _replicaState = None
    _sibConnectionString = None
    _modelType = None
    _singleGeneration = None
    _spatialRelation = None
    _queryGeometryType = None
    _queryGeometry = None
    _transferRelatedObjects = None
    _layers = None
    _reconcilePolicy = None
    _json = None
    #----------------------------------------------------------------------
    def __init__(self, url, securityHandler=None,
                 proxy_url=None, proxy_port=None,
                 initialize=False):
        """Constructor"""
        self._url = url
        self._securityHandler = securityHandler
        if not securityHandler is None:
            self._referer_url = securityHandler.referer_url
        self._proxy_port = proxy_port
        self._proxy_url = proxy_url
        if initialize:
            self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes all the properties """
        params = {
            "f" : "json"
        }
        json_dict = self._do_get(url=self._url, param_dict=params,
                                 securityHandler=self._securityHandler,
                                 proxy_url=self._proxy_url,
                                 proxy_port=self._proxy_port)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
            else:
                print (k, " - attribute not implemented in Replica.")
            del k, v

    #----------------------------------------------------------------------
    def __str__(self):
        """returns object as string"""
        if self._json is None:
            self.__init()
        return self._json
    #----------------------------------------------------------------------
    def __iter__(self):
        """
        returns key/value pair
        """
        attributes = json.loads(str(self))
        for att in attributes.keys():
            yield [att, getattr(self, att)]

    #----------------------------------------------------------------------
    @property
    def name(self):
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def sibGenerationNumber(self):
        if self._sibGenerationNumber is None:
            self.__init()
        return self._sibGenerationNumber
    #----------------------------------------------------------------------
    @property
    def queryGeometry(self):
        if self._queryGeometry is None:
            self.__init()
        return self._queryGeometry
    #----------------------------------------------------------------------
    @property
    def singleGeneration(self):
        if self._singleGeneration is None:
            self.__init()
        return self._singleGeneration
    #----------------------------------------------------------------------
    @property
    def modelType(self):
        if self._modelType is None:
            self.__init()
        return self._modelType
    #----------------------------------------------------------------------
    @property
    def layers(self):
        if self._layers is None:
            self.__init()
        return self._layers
    #----------------------------------------------------------------------
    @property
    def queryGeometryType(self):
        if self._queryGeometryType is None:
            self.__init()
        return self._queryGeometryType
    #----------------------------------------------------------------------
    @property
    def accessType(self):
        if self._accessType is None:
            self.__init()
        return self._accessType
    #----------------------------------------------------------------------
    @property
    def replicaVersion(self):
        if self._replicaVersion is None:
            self.__init()
        return self._replicaVersion
    #----------------------------------------------------------------------
    @property
    def spatialRelation(self):
        if self._spatialRelation is None:
            self.__init()
        return self._spatialRelation
    #----------------------------------------------------------------------
    @property
    def transferRelatedObjects(self):
        if self._transferRelatedObjects is None:
            self.__init()
        return self._transferRelatedObjects
    #----------------------------------------------------------------------
    @property
    def serviceName(self):
        if self._serviceName is None:
            self.__init()
        return self._serviceName
    #----------------------------------------------------------------------
    @property
    def role(self):
        if self._role is None:
            self.__init()
        return self._role
    #----------------------------------------------------------------------
    @property
    def myGenerationNumber(self):
        if self._myGenerationNumber is None:
            self.__init()
        return self._myGenerationNumber
    #----------------------------------------------------------------------
    @property
    def replicaState(self):
        if self._replicaState is None:
            self.__init()
        return self._replicaState
    #----------------------------------------------------------------------
    @property
    def sibConnectionString(self):
        if self._sibConnectionString is None:
            self.__init()
        return self._sibConnectionString
    #----------------------------------------------------------------------
    @property
    def guid(self):
        if self._guid is None:
            self.__init()
        return self._guid
    #----------------------------------------------------------------------
    @property
    def sibMyGenerationNumber(self):
        if self._sibMyGenerationNumber is None:
            self.__init()
        return self._sibMyGenerationNumber
    #----------------------------------------------------------------------
    @property
    def id(self):
        if self._id is None:
            self.__init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def reconcilePolicy(self):
        if self._reconcilePolicy is None:
            self.__init()
        return self._reconcilePolicy
    #----------------------------------------------------------------------
    @property
    def replicaOwner(self):
        if self._replicaOwner is None:
            self.__init()
        return self._replicaOwner
