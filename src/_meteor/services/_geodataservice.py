"""
"""
from __future__ import absolute_import
from ..common._base import BaseService
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
    @property
    def defaultWorkingVersion(self):
        """returns the default working version name"""
        if self._defaultWorkingVersion is None:
            self.init()
        return self._defaultWorkingVersion
    #----------------------------------------------------------------------
    @property
    def workspaceType(self):
        """returns the workspace type"""
        if self._workspaceType is None:
            self.init()
        return self._workspaceType
    #----------------------------------------------------------------------
    @property
    def replicas(self):
        """returns a list of replices"""
        if self._replicas is None:
            self.init()
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
            self.init()
        return self._serviceDescription
    #----------------------------------------------------------------------
    @property
    def versions(self):
        """returns a list of the versions"""
        if self._versions is None:
            self.init()
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
