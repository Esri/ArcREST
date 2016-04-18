"""
"""
from __future__ import absolute_import
from ._base import BaseService
from ..connection import SiteConnection
import json
########################################################################
class GeoDataService(BaseService):
    """
    Represents a single mobile service layer
    """
    _url = None
    _con = None
    _json_dict = None
    _replicasResource = None
    _defaultWorkingVersion = None
    _workspaceType = None
    _replicas = None
    _serviceDescription = None
    _versions = None
    #----------------------------------------------------------------------
    def __init__(self, connection, url, initialize=False):
        """constructor"""
        self._con = connection
        self._url = url
        self._json_dict = None
        if initialize:
            self.__init(connection)
    #----------------------------------------------------------------------
    def __init(self, connection=None):
        """loads the properties"""
        params = {"f" : "json"}
        missing = {}
        if connection is None:
            connection = self._con
        result = connection.get(path_or_url=self._url, params=params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        if isinstance(result, dict):
            self._json_dict = result
            for k,v in result.items():
                if k in ['tables', 'layers']:
                    setattr(self, "_"+k, v)
                elif k in attributes:
                    setattr(self, "_" + k, v)
                else:
                    missing[k] = v
                    setattr(self, k, v)
                del k,v
        else:
            raise RuntimeError("Could not connect to the service: %s" % result)
        if len(missing.keys()) > 0:
            self.__dict__.update(missing)
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
        return self._con.post(path_or_url=url,
                             postdata=params)
