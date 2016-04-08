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
